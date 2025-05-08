import React from "react";
import { Spreadsheet } from "react-spreadsheet";
import "./SpreadsheetComponent.css";

const SpreadsheetComponent = ({ data, columnLabels, onChange }) => {
  return (
    <div className="spreadsheet-container">
      <div className="spreadsheet-wrapper">
        <Spreadsheet data={data} onChange={onChange} />
      </div>
    </div>
  );
};

export default SpreadsheetComponent;
