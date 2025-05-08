// pages/SpreadsheetPage.jsx
import React, { useState, useEffect } from "react";
import SpreadsheetComponent from "../components/SpreadsheetComponent";
import { fetchDatasetData, saveDataset } from "../services/api";
import "./SpreadsheetPage.css";

const SpreadsheetPage = ({ datasetName }) => {
  const [spreadsheetData, setSpreadsheetData] = useState([]);
  const [columnLabels, setColumnLabels] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Fetch dataset when component mounts or datasetName changes
  useEffect(() => {
    if (!datasetName) return;
    fetchDataset();
  }, [datasetName]);

  // Fetch dataset from backend using our API service
  const fetchDataset = async () => {
    setLoading(true);
    setError(null);

    try {
      const data = await fetchDatasetData(datasetName);
      console.log("Fetched dataset for editing:", data);

      if (data.length > 0) {
        // Extract column headers from the first row
        const columns = Object.keys(data[0]);
        setColumnLabels(columns);

        // Format data for react-spreadsheet
        const formattedData = convertToSpreadsheetFormat(data, columns);
        setSpreadsheetData(formattedData);
      } else {
        setError("Dataset is empty");
      }
    } catch (error) {
      console.error("Error fetching dataset for editing:", error);
      setError("Failed to load dataset. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  // Convert data from JSON objects to react-spreadsheet format
  const convertToSpreadsheetFormat = (rows, columns) => {
    return rows.map((row) => {
      return columns.map((col) => {
        return {
          value:
            row[col] !== null && row[col] !== undefined ? String(row[col]) : "",
        };
      });
    });
  };

  // Convert from spreadsheet format back to JSON objects
  const convertFromSpreadsheetFormat = (data) => {
    return data.map((row) => {
      const rowData = {};
      columnLabels.forEach((col, index) => {
        rowData[col] = row[index]?.value || "";
      });
      return rowData;
    });
  };

  // Handle spreadsheet data changes
  const handleChange = (data) => {
    setSpreadsheetData(data);
  };

  // Save changes to the backend using our API service
  const handleSaveChanges = async () => {
    try {
      const jsonData = convertFromSpreadsheetFormat(spreadsheetData);
      await saveDataset(datasetName, jsonData);
      alert("Changes saved successfully!");
    } catch (error) {
      console.error("Error saving changes:", error);
      setError("Failed to save changes. Please try again.");
    }
  };

  if (loading) {
    return <div>Loading...</div>;
  }

  if (error) {
    return <div className="error-message">{error}</div>;
  }

  return (
    <div className="spreadsheet-page">
      <div className="spreadsheet-header">
        <h2>Editing Dataset: {datasetName}</h2>
        <button className="save-button" onClick={handleSaveChanges}>
          Save Changes
        </button>
      </div>

      <SpreadsheetComponent
        data={spreadsheetData}
        columnLabels={columnLabels}
        onChange={handleChange}
      />
    </div>
  );
};

export default SpreadsheetPage;
