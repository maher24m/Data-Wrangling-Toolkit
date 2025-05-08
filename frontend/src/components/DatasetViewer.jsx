import React from "react";
import "./DatasetViewer.css";

const DatasetViewer = ({
  datasetName,
  data,
  columns,
  isActivated,
  onActivate,
}) => {
  if (!data || !columns) {
    return (
      <div className="data-viewer-container">
        <div className="data-viewer-header">
          <h2>{datasetName}</h2>
        </div>
        <div className="empty-state">
          <p>No data available</p>
        </div>
      </div>
    );
  }

  return (
    <div className="data-viewer-container">
      <div className="data-viewer-header">
        <h2>{datasetName}</h2>
        <div className="dataset-stats">
          <div className="stat-item">
            <span className="stat-label">Rows</span>
            <span className="stat-value">{data.length}</span>
          </div>
          <div className="stat-item">
            <span className="stat-label">Columns</span>
            <span className="stat-value">{columns.length}</span>
          </div>
        </div>
        <div className="data-actions">
          <button
            className="action-button"
            onClick={() => onActivate(datasetName)}
            disabled={isActivated}
          >
            {isActivated ? "Dataset Active" : "Edit Dataset"}
          </button>
        </div>
      </div>

      <div className="table-container">
        <table className="data-table">
          <thead>
            <tr>
              {columns.map((column, index) => (
                <th key={index}>{column}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {data.map((row, rowIndex) => (
              <tr key={rowIndex}>
                {columns.map((column, colIndex) => (
                  <td key={colIndex}>{row[column]}</td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default DatasetViewer;
