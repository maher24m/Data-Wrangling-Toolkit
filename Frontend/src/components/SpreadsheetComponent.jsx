import React, { useEffect } from "react";
import Spreadsheet from "react-spreadsheet";

const SpreadsheetComponent = ({ data, onChange, datasetName }) => {
  useEffect(() => {
    console.log("🔥 SpreadsheetComponent Updated:", data);
  }, [data]);

  return (
    <div className="spreadsheet-container">
      <h3>Dataset: {datasetName}</h3>
      {data.length > 0 ? (
        <Spreadsheet data={data} onChange={onChange} />
      ) : (
        <p>No data available</p>
      )}
    </div>
  );
};

export default SpreadsheetComponent;
