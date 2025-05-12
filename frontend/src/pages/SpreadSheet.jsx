// pages/SpreadsheetPage.jsx
import React, { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import SpreadsheetComponent from "../components/SpreadsheetComponent";
import { fetchDatasetData, saveDataset } from "../services/api";
import "./SpreadsheetPage.css";

const SpreadsheetPage = () => {
  const { datasetId } = useParams();
  const [spreadsheetData, setSpreadsheetData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (!datasetId) return;
    fetchDataset();
  }, [datasetId]);

  const fetchDataset = async () => {
    setLoading(true);
    setError(null);

    try {
      const response = await fetchDatasetData(datasetId);
      let newResponse = []
      for (let i = 0; i<10;i++){
      newResponse.push(response[i])
      }
      if (newResponse) {
        console.log(newResponse);
        setSpreadsheetData(newResponse);
      } else {
        setError("Dataset is empty or invalid format");
      }
    } catch (error) {
      console.error("Error fetching dataset:", error);
      setError("Failed to load dataset. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (data) => {
    setSpreadsheetData(data);
  };

  const handleSaveChanges = async () => {
    try {
      const dataToSave = {
        values: spreadsheetData.map((row) =>
          row.map((cell) => ({ value: cell.value }))
        ),
      };
      await saveDataset(datasetId, dataToSave);
      alert("Changes saved successfully!");
    } catch (error) {
      console.error("Error saving changes:", error);
      setError("Failed to save changes. Please try again.");
    }
  };

  if (loading) return <div>Loading...</div>;
  if (error) return <div className="error-message">{error}</div>;

  return (
    <div className="spreadsheet-page">
      <div className="spreadsheet-header">
        <h2>Editing Dataset: {datasetId}</h2>
        <button className="save-button" onClick={handleSaveChanges}>
          Save Changes
        </button>
      </div>

      <SpreadsheetComponent data={spreadsheetData} onChange={handleChange} />
    </div>
  );
};

export default SpreadsheetPage;
