from datetime import datetime

import botocore
import mock
import psqlparse
import psycopg2
import pytest
from django.conf import settings

from dataworkspace.apps.core.utils import database_dsn
from dataworkspace.apps.datasets.models import SourceLink
from dataworkspace.tests import factories


def test_clone_dataset(db):
    ds = factories.DataSetFactory.create(published=True)
    clone = ds.clone()

    assert clone.id
    assert clone.id != ds.id
    assert clone.slug == ''
    assert clone.number_of_downloads == 0
    assert clone.name == f'Copy of {ds.name}'
    assert not clone.published


def test_clone_dataset_copies_related_objects(db):
    ds = factories.DataSetFactory.create(published=True)

    factories.DataSetUserPermissionFactory(dataset=ds)
    factories.SourceLinkFactory(dataset=ds)
    factories.SourceViewFactory(dataset=ds)
    factories.SourceTableFactory(dataset=ds)
    factories.CustomDatasetQueryFactory(dataset=ds)

    clone = ds.clone()

    assert not clone.datasetuserpermission_set.all()
    assert [obj.dataset for obj in clone.sourcelink_set.all()] == [clone]
    assert [obj.dataset for obj in clone.sourceview_set.all()] == [clone]
    assert [obj.dataset for obj in clone.sourcetable_set.all()] == [clone]
    assert [obj.dataset for obj in clone.customdatasetquery_set.all()] == [clone]

    assert ds.datasetuserpermission_set.all()
    assert [obj.dataset for obj in ds.sourcelink_set.all()] == [ds]
    assert [obj.dataset for obj in ds.sourceview_set.all()] == [ds]
    assert [obj.dataset for obj in ds.sourcetable_set.all()] == [ds]
    assert [obj.dataset for obj in ds.customdatasetquery_set.all()] == [ds]


@pytest.mark.parametrize(
    'factory',
    (
        factories.SourceTableFactory,
        factories.SourceViewFactory,
        factories.SourceLinkFactory,
        factories.CustomDatasetQueryFactory,
    ),
)
def test_dataset_source_reference_code(db, factory):
    ref_code1 = factories.DatasetReferenceCodeFactory(code='Abc')
    ref_code2 = factories.DatasetReferenceCodeFactory(code='Def')
    ds = factories.DataSetFactory(reference_code=ref_code1)
    source = factory(dataset=ds)
    assert source.source_reference == 'ABC00001'

    # Change to a new reference code
    ds.reference_code = ref_code2
    ds.save()
    ds.refresh_from_db()

    source.refresh_from_db()
    assert source.source_reference == 'DEF00001'

    # Unset the reference code
    ds.reference_code = None
    ds.save()
    ds.refresh_from_db()

    source.refresh_from_db()
    assert source.source_reference is None

    # Ensure numbers are incremented
    ds.reference_code = ref_code1
    ds.save()
    ds.refresh_from_db()

    source.refresh_from_db()
    assert source.source_reference == 'ABC00002'

    # Delete the reference code
    ref_code1.delete()
    ds.refresh_from_db()

    source.refresh_from_db()
    assert source.source_reference is None


@pytest.mark.parametrize(
    'factory',
    (
        factories.SourceTableFactory,
        factories.SourceViewFactory,
        factories.CustomDatasetQueryFactory,
    ),
)
def test_dataset_source_filename(db, factory):
    ds1 = factories.DataSetFactory(
        reference_code=factories.DatasetReferenceCodeFactory(code='DW')
    )
    source1 = factory(dataset=ds1, name='A test source')
    assert source1.get_filename() == 'DW00001-a-test-source.csv'

    ds2 = factories.DataSetFactory()
    source2 = factory(dataset=ds2, name='A test source')
    assert source2.get_filename() == 'a-test-source.csv'


def test_source_link_filename(db):
    ds1 = factories.DataSetFactory(
        reference_code=factories.DatasetReferenceCodeFactory(code='DW')
    )
    source1 = factories.SourceLinkFactory(
        dataset=ds1,
        name='A test source',
        url="s3://csv-pipelines/my-data.csv.zip",
        link_type=SourceLink.TYPE_LOCAL,
    )
    assert source1.get_filename() == 'DW00001-a-test-source.zip'

    ds2 = factories.DataSetFactory()
    source2 = factories.SourceLinkFactory(
        dataset=ds2,
        name='A test source',
        url="s3://csv-pipelines/my-data.csv",
        link_type=SourceLink.TYPE_LOCAL,
    )
    assert source2.get_filename() == 'a-test-source.csv'

    ds3 = factories.DataSetFactory()
    source3 = factories.SourceLinkFactory(
        dataset=ds3,
        name='A test source',
        url="http://www.google.com/index.html",
        link_type=SourceLink.TYPE_EXTERNAL,
    )
    assert source3.get_filename() == 'a-test-source.csv'


def test_dataset_parsed_query_tables(db):
    ds = factories.DataSetFactory.create(published=True)

    blank_query = factories.CustomDatasetQueryFactory(dataset=ds)
    assert not blank_query.parsed_query_tables

    standard_query = factories.CustomDatasetQueryFactory(
        dataset=ds, query='select * from foo'
    )
    assert standard_query.parsed_query_tables == ['foo']

    join_query = factories.CustomDatasetQueryFactory(
        dataset=ds, query='select * from foo join bar on foo.id = bar.id'
    )
    assert sorted(join_query.parsed_query_tables) == ['bar', 'foo']

    with_query = factories.CustomDatasetQueryFactory(
        dataset=ds, query='with test as (select * from foo) select * from test'
    )
    assert sorted(with_query.parsed_query_tables) == ['foo', 'test']

    bad_query = factories.CustomDatasetQueryFactory(dataset=ds, query='select * from')
    with pytest.raises(psqlparse.exceptions.PSqlParseError):
        bad_query.parsed_query_tables  # pylint: disable=pointless-statement


@pytest.fixture
def metadata_db(db):
    database = factories.DatabaseFactory(memorable_name='my_database')
    with psycopg2.connect(
        database_dsn(settings.DATABASES_DATA['my_database'])
    ) as conn, conn.cursor() as cursor:
        cursor.execute(
            '''
            CREATE SCHEMA IF NOT EXISTS dataflow;
            CREATE TABLE IF NOT EXISTS dataflow.metadata (
                id int, table_schema text, table_name text, source_data_modified_utc timestamp
            );
            INSERT INTO dataflow.metadata VALUES(1, 'public', 'table1', '2020-09-02 00:01:00.0');
            INSERT INTO dataflow.metadata VALUES(1, 'public', 'table2', '2020-09-01 00:01:00.0');
            INSERT INTO dataflow.metadata VALUES(1, 'public', 'table1', '2020-01-01 00:01:00.0');
            '''
        )
        conn.commit()
        yield database
        cursor.execute('DROP TABLE dataflow.metadata;')


@pytest.mark.django_db
def test_source_table_data_last_updated(metadata_db):
    dataset = factories.DataSetFactory()
    table = factories.SourceTableFactory(
        dataset=dataset, database=metadata_db, schema='public', table='table1'
    )
    assert table.get_data_last_updated_date() == datetime(2020, 9, 2, 0, 1, 0)

    table = factories.SourceTableFactory(
        dataset=dataset, database=metadata_db, schema='public', table='doesntexist'
    )
    assert table.get_data_last_updated_date() is None


@pytest.mark.django_db
def test_source_table_no_metadata_table():
    table = factories.SourceTableFactory(
        dataset=factories.DataSetFactory(),
        database=factories.DatabaseFactory(memorable_name='my_database'),
        schema='public',
        table='table1',
    )
    assert table.get_data_last_updated_date() is None


@pytest.mark.django_db
def test_custom_query_data_last_updated(metadata_db):
    dataset = factories.DataSetFactory()

    # Ensure the earliest "last updated" date is returned when
    # there are multiple tables in the query
    query = factories.CustomDatasetQueryFactory(
        dataset=dataset,
        database=metadata_db,
        query='select * from table1 join table2 on 1=1',
    )
    assert query.get_data_last_updated_date() == datetime(2020, 9, 1, 0, 1, 0)

    # Ensure a single table returns the last update date
    query = factories.CustomDatasetQueryFactory(
        dataset=dataset, database=metadata_db, query='select * from table1',
    )
    assert query.get_data_last_updated_date() == datetime(2020, 9, 2, 0, 1, 0)

    # Ensure None is returned if we don't have any metadata for the tables
    query = factories.CustomDatasetQueryFactory(
        dataset=dataset, database=metadata_db, query='select * from table3',
    )
    assert query.get_data_last_updated_date() is None


@pytest.mark.django_db
def test_custom_query_no_metadata_table():
    query = factories.CustomDatasetQueryFactory(
        dataset=factories.DataSetFactory(),
        database=factories.DatabaseFactory(memorable_name='my_database'),
        query='select * from table1 join table2 on 1=1',
    )
    assert query.get_data_last_updated_date() is None


@pytest.mark.django_db
@mock.patch('dataworkspace.apps.datasets.views.boto3.client')
def test_source_link_data_last_updated(mock_client):
    dataset = factories.DataSetFactory.create()
    local_link = factories.SourceLinkFactory(
        dataset=dataset,
        link_type=SourceLink.TYPE_LOCAL,
        url='s3://sourcelink/158776ec-5c40-4c58-ba7c-a3425905ec45/test.txt',
    )

    # Returns last modified date if the file exists
    mock_client().head_object.return_value = {
        'ContentType': 'text/plain',
        'LastModified': datetime(2020, 9, 2, 0, 1, 0),
    }
    assert local_link.get_data_last_updated_date() == datetime(2020, 9, 2, 0, 1, 0)

    # Returns None if file does not exist on s3
    mock_client().head_object.side_effect = [
        botocore.exceptions.ClientError(
            error_response={'Error': {'Message': 'it failed'}},
            operation_name='head_object',
        )
    ]
    assert local_link.get_data_last_updated_date() is None

    # External links never have a last updated date
    external_link = factories.SourceLinkFactory(
        dataset=dataset,
        link_type=SourceLink.TYPE_EXTERNAL,
        url='http://www.example.com',
    )
    assert external_link.get_data_last_updated_date() is None

