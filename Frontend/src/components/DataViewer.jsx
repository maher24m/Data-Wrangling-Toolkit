import React from "react";
import SpreadsheetComponent from "./SpreadsheetComponent";
import "./DataViewer.css";

/**
 * DataViewer component for displaying dataset data
 * @param {Object} props - Component props
 * @param {Array} props.data - Data to display
 * @param {string} props.datasetName - Name of the dataset
 * @param {Function} props.onDataChange - Function to call when data changes
 * @returns {JSX.Element} DataViewer component
 */
const DataViewer = ({ data, datasetName, onDataChange }) => {
  return (
    <div className="data-viewer">
      <h3>Dataset: {datasetName}</h3>
      {data.length > 0 ? (
        <SpreadsheetComponent
          data={data}
          onChange={onDataChange}
          datasetName={datasetName}
        />
      ) : (
        <p>No data available for this dataset</p>
      )}
    </div>
  );
};

export default DataViewer;
