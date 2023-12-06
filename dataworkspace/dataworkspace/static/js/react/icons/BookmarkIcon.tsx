import React from 'react';

const BookmarkIcon: React.FC = () => (
  <svg
    version="1.1"
    xmlnsXlink="http://www.w3.org/1999/xlink"
    width="16px"
    height="18px"
    xmlns="http://www.w3.org/2000/svg"
    className="govuk-!-margin-right-1"
  >
    <g transform="matrix(1 0 0 1 -666 -184 )">
        <path 
            className="is-not-bookmarked-icon" 
            d={`
                M 14.4 16.2987442167878  L 14.4 1.52280237937872  L 1.6 1.52280237937872
                L 1.6 16.2987442167878  L 6.8875 11.468605419696  L 8 10.4573694646398
                L 9.1125 11.468605419696  L 14.4 16.2987442167878  Z M 1.45 0  L 14.55 0
                C 14.7416666666667 0  14.925 0.035690680766689  15.1 0.107072042300067
                C 15.375 0.210178453403831  15.59375 0.372769332452081  15.75625 0.594844679444812
                C 15.91875 0.81692002643754  16 1.06278916060806  16 1.33245208195638
                L 16 16.6675479180436  C 16 16.9372108393919  15.91875 17.1830799735625
                15.75625 17.4051553205552  C 15.59375 17.6272306675479  15.375 17.7898215465962
                15.1 17.8929279576999  C 14.9416666666667 17.9563780568407  14.7583333333333 17.9881031064111
                14.55 17.9881031064111  C 14.15 17.9881031064111  13.8041666666667 17.8612029081295
                13.5125 17.6074025115664  L 8 12.5631196298744  L 2.4875 17.6074025115664
                C 2.1875 17.8691341705221  1.84166666666667 18  1.45 18  C 1.25833333333333 18
                1.075 17.9643093192333  0.9 17.8929279576999  C 0.625 17.7898215465962
                0.40625 17.6272306675479  0.24375 17.4051553205552  C 0.08125 17.1830799735625
                0 16.9372108393919  0 16.6675479180436  L 0 1.33245208195638  C 0 1.06278916060806
                0.08125 0.81692002643754  0.24375 0.594844679444812  C 0.40625 0.372769332452081
                0.625 0.210178453403831  0.9 0.107072042300067  C 1.075 0.035690680766689
                1.25833333333333 0  1.45 0  Z
            `}
            fill-rule="nonzero" 
            fill="currentColor" 
            stroke="none" 
            transform="matrix(1 0 0 1 666 184)"
        />
    </g>
  </svg>
);

export default BookmarkIcon;