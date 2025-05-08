import React, { useState, useEffect } from "react";
import DatasetSelector from "../components/DatasetSelector";
import DatasetViewer from "../components/DatasetViewer";
import "./DatasetSelection.css";

const DatasetSelection = () => {
  // State management
  const [datasets, setDatasets] = useState([]);
  const [selectedDataset, setSelectedDataset] = useState(null);
  const [datasetData, setDatasetData] = useState(null);
  const [columns, setColumns] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [isActivated, setIsActivated] = useState(false);

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

  // Handle dataset activation
  const handleDatasetActivate = async (datasetName) => {
    setLoading(true);
    setError(null);
    try {
      setIsActivated(true);
      // Uncomment when API is ready
      /*
      const response = await fetch(`/api/datasets/${datasetName}/activate`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ dataset_name: datasetName }),
      });
      if (!response.ok) {
        throw new Error('Failed to activate dataset');
      }
      */
    } catch (err) {
      setError(err.message);
      setIsActivated(false);
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
    <div className="data-selection-container">
      <div className="data-selection-header">
        <h2>Data Selection</h2>
        <p>Select a dataset to view and analyze its contents</p>
      </div>

      <div className="data-selection-content">
        <div className="selector-section">
          <DatasetSelector
            datasets={datasets}
            activeDataset={selectedDataset}
            onDatasetSelect={handleDatasetSelect}
            loading={loading}
            error={error}
          />
        </div>

        <div className="viewer-section">
          {loading ? (
            <div className="loading-message">Loading dataset...</div>
          ) : error ? (
            <div className="error-message">{error}</div>
          ) : selectedDataset ? (
            <DatasetViewer
              datasetName={selectedDataset}
              data={datasetData}
              columns={columns}
              isActivated={isActivated}
              onActivate={handleDatasetActivate}
            />
          ) : (
            <div className="empty-state">
              <p>Select a dataset to view its contents</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default DatasetSelection;
