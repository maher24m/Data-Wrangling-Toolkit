import React from "react";
import "./DatasetSelector.css";

/**
 * DatasetSelector component for selecting datasets
 * @param {Object} props - Component props
 * @param {Array} props.datasets - List of available datasets
 * @param {string} props.activeDataset - Currently selected dataset
 * @param {Function} props.onDatasetSelect - Function to call when a dataset is selected
 * @returns {JSX.Element} DatasetSelector component
 */
const DatasetSelector = ({ datasets, activeDataset, onDatasetSelect }) => {
  return (
    <div className="dataset-selector">
      <h3>Datasets</h3>
      {datasets.length === 0 ? (
        <p>No datasets available</p>
      ) : (
        <ul className="dataset-list">
          {datasets.map((dataset) => (
            <li
              key={dataset}
              className={`dataset-item ${
                dataset === activeDataset ? "active" : ""
              }`}
              onClick={() => onDatasetSelect(dataset)}
            >
              {dataset}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default DatasetSelector;
