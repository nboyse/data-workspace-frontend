from datetime import datetime

from django.contrib import admin
from django.db.models import Count, Max, Min, Sum, F, Func, Value

from dataworkspace.apps.applications.models import (
    ApplicationInstance,
    ApplicationInstanceReport,
)
from dataworkspace.apps.applications.utils import application_instance_max_cpu


@admin.register(ApplicationInstance)
class ApplicationInstanceAdmin(admin.ModelAdmin):

    list_display = ('owner', 'public_host', 'created_date', )
    fieldsets = [
        (None, {
            'fields': [
                'owner',
                'public_host',
                'created_date',
                'state',
                'spawner_application_instance_id',
                'max_cpu',
            ]
        }),
    ]
    readonly_fields = (
        'owner', 'public_host', 'created_date', 'spawner_application_instance_id', 'state',
        'max_cpu',
    )

    def has_add_permission(self, request):
        return False

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(state__in=['SPAWNING', 'RUNNING'])

    def max_cpu(self, obj):
        try:
            max_cpu, ts_at_max = application_instance_max_cpu(obj)
        except ValueError as exception:
            return exception.args[0] if exception.args else 'Error'

        return '{0:.2f}% at {1}'.format(
            max_cpu,
            datetime.datetime.fromtimestamp(ts_at_max).strftime('%-I:%M %p').replace('AM', 'a.m.').replace('PM', 'p.m'),
        )

    max_cpu.short_description = 'Max recent CPU'

    def get_form(self, request, obj=None, change=False, **kwargs):
        kwargs.update({
            'help_texts': {
                'max_cpu': ('The highest CPU usage in the past two hours.'
                            'The application will be stopped automatically '
                            'if the usage is less than 1% for two hours.'),
            },
        })
        return super().get_form(request, obj, change, **kwargs)


@admin.register(ApplicationInstanceReport)
class ApplicationInstanceReportAdmin(admin.ModelAdmin):
    change_list_template = 'admin/application_instance_report_change_list.html'
    date_hierarchy = 'created_date'

    list_filter = (
        'application_template__nice_name',
    )

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(
            request,
            extra_context=extra_context,
        )
        try:
            qs = response.context_data['cl'].queryset
        except (AttributeError, KeyError):
            return response

        # We want to display times to second precision, so we truncate the
        # timestamps to second precision _before_ summing, to avoid issues
        # where the totals of the rows each don't add up to the bottom total
        metrics = {
            'num_launched': Count('id'),
            'num_with_runtime': Count(F('spawner_stopped_at') - F('spawner_created_at')),
            'min_runtime': Min(
                Func(Value('second'), F('spawner_stopped_at'), function='date_trunc') -
                Func(Value('second'), F('spawner_created_at'), function='date_trunc')
            ),
            'max_runtime': Max(
                Func(Value('second'), F('spawner_stopped_at'), function='date_trunc') -
                Func(Value('second'), F('spawner_created_at'), function='date_trunc')
            ),
            'total_runtime': Sum(
                Func(Value('second'), F('spawner_stopped_at'), function='date_trunc') -
                Func(Value('second'), F('spawner_created_at'), function='date_trunc')
            ),
        }

        response.context_data['summary'] = list(
            qs
            .values('owner__username', 'application_template__nice_name')
            .annotate(**metrics)
            .order_by('-total_runtime', '-num_launched', '-max_runtime', 'owner__username')
        )

        response.context_data['summary_total'] = dict(
            qs.aggregate(**metrics)
        )

        return response
