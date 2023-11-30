import React from 'react';

import { SPACING_POINTS } from '@govuk-react/constants';
import { typography } from '@govuk-react/lib';
import Link from '@govuk-react/link';
import { Button } from 'govuk-react';
import styled from 'styled-components';

import { Tile } from '../../../../components';
import { LINK_COLOUR, LINK_HOVER_COLOUR, WHITE } from '../../../../constants';
import URLS from '../../../../urls';

export type Collection = {
  title: string;
  url: string;
};

const CollectionTilesContainer = styled('div')`
  margin: ${SPACING_POINTS['5']}px 0 ${SPACING_POINTS['4']}px;
  display: flex;
  a {
    margin-right: ${SPACING_POINTS['4']}px;
    display: block;
    max-width: 143px;
    width: 100%;
    background-color: ${LINK_COLOUR};
    box-shadow: 0 2px 0 ${LINK_HOVER_COLOUR};
    padding: ${SPACING_POINTS['2']}px;
    color: ${WHITE};
    ${typography.font({ size: 14, weight: 'bold' })};
    text-decoration: none;
    min-height: 111px;
    &:hover {
      background-color: #175a93;
    }
    &:last-child {
      margin-right: 0;
    }
  }
`;

const StyledParagraph = styled('p')`
  ${typography.font({ size: 16 })};
`;

const CollectionTile: React.FC<Collection> = ({ url, title }) => (
  <a href={url}>{title}</a>
);

const RecentCollections: React.FC<Record<'collections', Collection[]>> = ({
  collections
}) => (
  <Tile title="Your recent collections">
    {collections.length ? (
      <>
        <StyledParagraph>
          In collections you can create a space for yourself and colleagues to
          share data, dashboards and notes.
        </StyledParagraph>
        <CollectionTilesContainer>
          {collections.map((collection, index) => (
            <CollectionTile key={index} {...collection} />
          ))}
        </CollectionTilesContainer>
        <Link href={URLS.collections.base}>View all collections</Link>
      </>
    ) : (
      <>
        <StyledParagraph>
          In collections you can create a space for yourself and colleagues to
          share data, dashboards and notes.
        </StyledParagraph>
        <StyledParagraph>
          You've currently not created a collection, or you're not apart of an
          existing collection.
        </StyledParagraph>
        <Button as="a" href={URLS.collections.create}>
          Create a collection
        </Button>
        <div>
          <Link
            href={URLS.external.dataServices.dataWorkspace.collections}
            role="button"
          >
            Find out more about collections
          </Link>
        </div>
      </>
    )}
  </Tile>
);

export default RecentCollections;
