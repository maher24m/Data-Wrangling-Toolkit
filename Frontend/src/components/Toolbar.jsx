import React, { useState } from "react";
import axios from "axios";
import "./Toolbar.css";

const Toolbar = ({ 
  tools = [], 
  activeView = "browse", 
  activeDataset, 
  onBackToBrowse 
}) => {
  const [selectedTool, setSelectedTool] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Handle tool selection
  const handleToolSelect = async (tool) => {
    if (!activeDataset) {
      alert("Please select a dataset first");
      return;
    }

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
    // Call the backend to analyze the active dataset
    const response = await axios.get(`http://127.0.0.1:8000/api/analysis/${activeDataset}/`);
    
    if (response.data && response.data.summary) {
      alert(`Analysis complete! Summary statistics:\n${JSON.stringify(response.data.summary, null, 2)}`);
    }
  };

  // Handle export operation
  const handleExport = async () => {
    // Ask user for export format
    const format = prompt("Enter export format (csv, json, excel, xml):", "csv");
    
    if (!format) return;
    
    // Call the backend to export the active dataset
    window.location.href = `http://127.0.0.1:8000/api/export/?dataset_name=${activeDataset}&file_type=${format}`;
  };

  return (
    <div className="toolbar">
      <div className="toolbar-left">
        <span className="app-title">Data Wrangler</span>
      </div>
      
      <div className="toolbar-center">
        {activeView === "edit" && (
          <button 
            className="toolbar-back-button"
            onClick={onBackToBrowse}
          >
            ← Back to Datasets
          </button>
        )}
        
        {tools.map((tool) => (
          <button 
            key={tool} 
            className={`toolbar-button ${selectedTool === tool ? 'active' : ''}`}
            onClick={() => handleToolSelect(tool)}
            disabled={loading || !activeDataset}
          >
            {tool}
          </button>
        ))}
      </div>
      
      <div className="toolbar-right">
        {loading && <span className="loading-text">Processing...</span>}
        {error && <span className="error-text">{error}</span>}
        
        {activeView === "edit" && activeDataset && (
          <div className="active-dataset-indicator">
            Editing: <span className="dataset-name">{activeDataset}</span>
          </div>
        )}
      </div>
    </div>
  );
};

export default Toolbar;