import React from "react";
import Toolbar from "./Toolbar";
import FileImport from "./FileImport";
import DatasetSelector from "./DatasetSelector";
import DataViewer from "./DataViewer";
import LoadingSpinner from "./LoadingSpinner";
import { useAppContext } from "../context/AppContext";
import "./MainLayout.css";

const MainLayout = () => {
  const {
    datasets,
    activeDataset,
    spreadsheetData,
    isLoading,
    activeTab,
    handleDatasetSelect,
    handleSpreadsheetChange,
    handleFileUpload,
    handleSaveDataset,
    setActiveTool
  } = useAppContext();

  // Handle save with feedback
  const onSave = async () => {
    const success = await handleSaveDataset();
    if (success) {
      alert("Dataset saved successfully!");
    } else {
      alert("Failed to save dataset.");
    }
  };

  // Show loading spinner if data is loading
  if (isLoading) {
    return <LoadingSpinner />;
  }

  // Render appropriate content based on active tab
  const renderContent = () => {
    // If no datasets available, show import
    if (datasets.length === 0) {
      return <FileImport onFileUpload={handleFileUpload} />;
    }

    // If no active dataset selected, prompt selection
    if (!activeDataset) {
      return <div className="empty-state">Please select a dataset</div>;
    }

    // Otherwise, show the appropriate tab content
    switch (activeTab) {
      case "spreadsheet":
        return (
          <DataViewer
            data={spreadsheetData}
            datasetName={activeDataset}
            onDataChange={handleSpreadsheetChange}
          />
        );
      case "analyze":
        return <div className="analyze-container">Analysis tools coming soon</div>;
      case "visualize":
        return <div className="visualize-container">Visualization tools coming soon</div>;
      case "clean":
        return <div className="clean-container">Data cleaning tools coming soon</div>;
      case "transform":
        return <div className="transform-container">Transformation tools coming soon</div>;
      case "export":
        return <div className="export-container">Export options coming soon</div>;
      default:
        return (
          <DataViewer
            data={spreadsheetData}
            datasetName={activeDataset}
            onDataChange={handleSpreadsheetChange}
          />
        );
    }
  };

  return (
    <div className="main-layout">
      <Toolbar
        tools={["Spreadsheet", "Analyze", "Visualize", "Clean", "Transform", "Export"]}
        onToolClick={setActiveTool}
        onSave={onSave}
        activeDataset={activeDataset}
      />

      <div className="main-content">
        {/* Dataset selector */}
        <div className="sidebar">
          <DatasetSelector
            datasets={datasets}
            activeDataset={activeDataset}
            onDatasetSelect={handleDatasetSelect}
          />
        </div>

        {/* Main content area */}
        <div className="content">
          {renderContent()}
        </div>
      </div>
    </div>
  );
};

export default MainLayout;