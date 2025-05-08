import React from "react";
import "./DatasetSelector.css";

const DatasetSelector = ({
  datasets,
  activeDataset,
  onDatasetSelect,
  loading,
  error,
}) => {
  if (loading) {
    return (
      <div className="dataset-selector">
        <div className="selector-header">
          <h3>Datasets</h3>
        </div>
        <div className="loading-message">Loading datasets...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="dataset-selector">
        <div className="selector-header">
          <h3>Datasets</h3>
        </div>
        <div className="error-message">{error}</div>
      </div>
    );
  }

  if (!datasets || datasets.length === 0) {
    return (
      <div className="dataset-selector">
        <div className="selector-header">
          <h3>Datasets</h3>
        </div>
        <div className="no-datasets">
          No datasets available. Upload a file to get started.
        </div>
      </div>
    );
  }

  return (
    <div className="dataset-selector">
      <div className="selector-header">
        <h3>Datasets</h3>
      </div>
      <div className="dataset-list">
        {datasets.map((dataset) => (
          <div
            key={dataset}
            className={`dataset-item ${
              activeDataset === dataset ? "active" : ""
            }`}
            onClick={() => onDatasetSelect(dataset)}
          >
            {dataset}
          </div>
        ))}
      </div>
    </div>
  );
};

export default DatasetSelector;
