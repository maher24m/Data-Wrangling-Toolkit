import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import DatasetSelector from "../components/DatasetSelector";
import SpreadsheetComponent from "../components/SpreadsheetComponent";
import "./DatasetSelection.css";

const DatasetSelection = () => {
  const navigate = useNavigate();
  // State management
  const [datasets, setDatasets] = useState([]);
  const [selectedDataset, setSelectedDataset] = useState(null);
  const [datasetData, setDatasetData] = useState(null);
  const [columns, setColumns] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Fetch datasets when component mounts
  useEffect(() => {
    fetchDatasets();
  }, []);

  // Fetch datasets from backend
  const fetchDatasets = async () => {
    setLoading(true);
    setError(null);
    try {
      // For now, use dummy data
      const dummyDatasets = ["Sample Dataset 1", "Sample Dataset 2"];
      setDatasets(dummyDatasets);

      // Uncomment when API is ready
      /*
      const response = await fetch('/api/datasets');
      if (!response.ok) {
        throw new Error('Failed to fetch datasets');
      }
      const data = await response.json();
      setDatasets(data);
      */
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  // Handle dataset selection
  const handleDatasetSelect = async (datasetName) => {
    setLoading(true);
    setError(null);
    try {
      setSelectedDataset(datasetName);
      // For now, use dummy data
      const dummyData = [
        { id: 1, name: "Sample 1", value: 100 },
        { id: 2, name: "Sample 2", value: 200 },
      ];
      setDatasetData(dummyData);
      setColumns(["id", "name", "value"]);

      // Uncomment when API is ready
      /*
      const response = await fetch(`/api/datasets/${datasetName}?return_columns=true`);
      if (!response.ok) {
        throw new Error('Failed to fetch dataset');
      }
      const data = await response.json();
      setDatasetData(data.data);
      setColumns(data.columns);
      */
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  // Handle use dataset
  const handleUseDataset = async () => {
    if (!selectedDataset) return;

    setLoading(true);
    setError(null);
    try {
      // Navigate to the spreadsheet view with the selected dataset
      navigate(`/spreadsheet/${selectedDataset}`);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  // Convert data to spreadsheet format
  const convertToSpreadsheetFormat = (rows, columns) => {
    return rows.map((row) => {
      return columns.map((col) => ({
        value:
          row[col] !== null && row[col] !== undefined ? String(row[col]) : "",
        readOnly: true,
      }));
    });
  };

  return (
    <div className="dataset-selection-container">
      <div className="sidebar">
        <div className="sidebar-header">
          <h2>Datasets</h2>
        </div>
        <DatasetSelector
          datasets={datasets}
          activeDataset={selectedDataset}
          onDatasetSelect={handleDatasetSelect}
          loading={loading}
          error={error}
        />
      </div>

      <div className="main-content">
        {loading ? (
          <div className="loading-message">Loading dataset...</div>
        ) : error ? (
          <div className="error-message">{error}</div>
        ) : selectedDataset ? (
          <div className="spreadsheet-container">
            <div className="spreadsheet-header">
              <h2>Dataset: {selectedDataset}</h2>
              <button
                className="use-dataset-button"
                onClick={handleUseDataset}
                disabled={loading}
              >
                Use Dataset
              </button>
            </div>
            <SpreadsheetComponent
              data={convertToSpreadsheetFormat(datasetData, columns)}
              columnLabels={columns}
            />
          </div>
        ) : (
          <div className="empty-state">
            <h2>No Dataset Selected</h2>
            <p>Select a dataset from the sidebar to view its contents</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default DatasetSelection;
