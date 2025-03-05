import React from "react";
import Spreadsheet from "react-spreadsheet";
import "./SpreadsheetComponent.css";

const SpreadsheetComponent = ({ data, onChange, datasetName }) => {
  return (
    <div className="spreadsheet-container">
      <h3>Dataset: {datasetName}</h3>
      <Spreadsheet data={data} onChange={onChange} />
    </div>
  );
};

export default SpreadsheetComponent;
