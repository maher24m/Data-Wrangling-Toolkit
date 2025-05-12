import React, { useState } from "react";
import { Link, useNavigate, useLocation } from "react-router-dom";
import axios from "axios";
import "./Toolbar.css";

const Toolbar = ({ tools = [] }) => {
  const [selectedTool, setSelectedTool] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const navigate = useNavigate();
  const location = useLocation();

  // Handle tool selection
  const handleToolSelect = async (tool) => {
    setSelectedTool(tool);

    try {
      setLoading(true);

      // Handle different tool operations
      switch (tool) {
        case "Analyze":
          await handleAnalyze();
          break;
        case "Visualize":
          // Visualization logic would go here
          break;
        case "Transform":
          // Transformation logic would go here
          break;
        case "Export":
          await handleExport();
          break;
        default:
          break;
      }
    } catch (error) {
      console.error(`Error using ${tool}:`, error);
      setError(`Failed to use ${tool}. Please try again.`);
    } finally {
      setLoading(false);
    }
  };

  // Handle analyze operation
  const handleAnalyze = async () => {
    const datasetId = location.pathname.split("/").pop();
    if (!datasetId) {
      alert("Please select a dataset first");
      return;
    }

    // Call the backend to analyze the active dataset
    const response = await axios.get(
      `http://127.0.0.1:8000/api/analysis/${datasetId}/`
    );

    if (response.data && response.data.summary) {
      alert(
        `Analysis complete! Summary statistics:\n${JSON.stringify(
          response.data.summary,
          null,
          2
        )}`
      );
    }
  };

  // Handle export operation
  const handleExport = async () => {
    const datasetId = location.pathname.split("/").pop();
    if (!datasetId) {
      alert("Please select a dataset first");
      return;
    }

    // Ask user for export format
    const format = prompt(
      "Enter export format (csv, json, excel, xml):",
      "csv"
    );

    if (!format) return;

    // Call the backend to export the active dataset
    window.location.href = `http://127.0.0.1:8000/api/export/?dataset_id=${datasetId}&file_type=${format}`;
  };

  return (
    <div className="toolbar">
      <div className="toolbar-left">
        <Link to="/" className="app-title">
          Data Wrangler
        </Link>
      </div>

      <div className="toolbar-center">
        {location.pathname.includes("/spreadsheet/") && (
          <button
            className="toolbar-back-button"
            onClick={() => navigate("/datasets")}
          >
            ← Back to Datasets
          </button>
        )}

        {tools.map((tool) => (
          <button
            key={tool}
            className={`toolbar-button ${
              selectedTool === tool ? "active" : ""
            }`}
            onClick={() => handleToolSelect(tool)}
            disabled={loading || !location.pathname.includes("/spreadsheet/")}
          >
            {tool}
          </button>
        ))}
      </div>

      <div className="toolbar-right">
        {loading && <span className="loading-text">Processing...</span>}
        {error && <span className="error-text">{error}</span>}

        {location.pathname.includes("/spreadsheet/") && (
          <div className="active-dataset-indicator">
            Editing:{" "}
            <span className="dataset-name">
              {location.pathname.split("/").pop()}
            </span>
          </div>
        )}
      </div>
    </div>
  );
};

export default Toolbar;
