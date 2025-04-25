import React from "react";
import Toolbar from "./components/Toolbar";
import FileImport from "./components/FileImport";
import DatasetSelector from "./components/DatasetSelector";
import DataViewer from "./components/DataViewer";
import LoadingSpinner from "./components/LoadingSpinner";
import useDatasets from "./hooks/useDatasets";
import useTransformations from "./hooks/useTransformations";
import { saveDataset } from "./services/api";
import "./App.css";

const App = () => {
  // Use custom hooks for state management
  const {
    datasets,
    activeDataset,
    spreadsheetData,
    isLoading: datasetsLoading,
    handleDatasetSelect,
    handleSpreadsheetChange,
    handleFileUpload,
  } = useDatasets();

  const { availableTransformations, isLoading: transformationsLoading } =
    useTransformations();

  // Handle save dataset
  const handleSaveDataset = async () => {
    if (!activeDataset) return;

    try {
      await saveDataset(activeDataset, spreadsheetData);
      alert("Dataset saved successfully!");
    } catch (error) {
      console.error("Error saving dataset:", error);
      alert("Failed to save dataset.");
    }
  };

  // Show loading spinner if data is loading
  if (datasetsLoading || transformationsLoading) {
    return <LoadingSpinner />;
  }

  return (
    <div className="app-container">
      <Toolbar
        tools={["Analyze", "Visualize", "Transform", "Export"]}
        onSave={handleSaveDataset}
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
          {datasets.length === 0 ? (
            <FileImport onFileUpload={handleFileUpload} />
          ) : (
            activeDataset && (
              <DataViewer
                data={spreadsheetData}
                datasetName={activeDataset}
                onDataChange={handleSpreadsheetChange}
              />
            )
          )}
        </div>
      </div>
    </div>
  );
};

export default App;
