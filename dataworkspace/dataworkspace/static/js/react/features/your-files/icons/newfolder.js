/* eslint-disable */
import React from "react";
import classNames from "classnames";

/*
  <svg
                  aria-hidden="true"
                  focusable="false"
                  data-prefix="fas"
                  data-icon="folder-plus"
                  className="button-icon svg-inline--fa fa-folder-plus fa-w-16"
                  role="img"
                  xmlns="http://www.w3.org/2000/svg"
                  viewBox="0 0 512 512"
                  width="18"
                  height="18"
                >
                  <path
                    fill="currentColor"
                    d="M464 128H272l-64-64H48C21.49 64 0 85.49 0 112v288c0 26.51 21.49 48 48 48h416c26.51 0 48-21.49 48-48V176c0-26.51-21.49-48-48-48zm-96 168c0 8.84-7.16 16-16 16h-72v72c0 8.84-7.16 16-16 16h-16c-8.84 0-16-7.16-16-16v-72h-72c-8.84 0-16-7.16-16-16v-16c0-8.84 7.16-16 16-16h72v-72c0-8.84 7.16-16 16-16h16c8.84 0 16 7.16 16 16v72h72c8.84 0 16 7.16 16 16v16z"
                  ></path>
                </svg>
 */

export function NewFolderIcon(props) {
  const svgClasses = classNames("svg-inline--fa", "fa-folder-plus", "fa-w-16", {
    "navbutton-icon": props.isNavIcon,
    "button-icon": !props.isNavIcon,
    "navbutton-icon-large": props.isNavIcon,
  });
  return (
    <svg
      aria-hidden="true"
      focusable="false"
      data-prefix="fas"
      data-icon="folder-plus"
      className={svgClasses}
      role="img"
      xmlns="http://www.w3.org/2000/svg"
      viewBox="0 0 512 512"
      width={props.isNavIcon ? "60" : "18"}
      height={props.isNavIcon ? "60" : "18"}
    >
      <path
        fill="currentColor"
        d="M464 128H272l-64-64H48C21.49 64 0 85.49 0 112v288c0 26.51 21.49 48 48 48h416c26.51 0 48-21.49 48-48V176c0-26.51-21.49-48-48-48zm-96 168c0 8.84-7.16 16-16 16h-72v72c0 8.84-7.16 16-16 16h-16c-8.84 0-16-7.16-16-16v-72h-72c-8.84 0-16-7.16-16-16v-16c0-8.84 7.16-16 16-16h72v-72c0-8.84 7.16-16 16-16h16c8.84 0 16 7.16 16 16v72h72c8.84 0 16 7.16 16 16v16z"
      ></path>
    </svg>
  );
}
