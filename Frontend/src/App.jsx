import React, { useState, useEffect } from "react";
import axios from "axios";
import Toolbar from "./components/Toolbar";
import FileImport from "./components/FileImport";
import TransformationPanel from "./components/TransformationPanel";
import SpreadsheetComponent from "./components/SpreadsheetComponent";
import "./App.css";

const App = () => {
  const [showImportModal, setShowImportModal] = useState(false);
  const [datasets, setDatasets] = useState([]);
  const [activeDataset, setActiveDataset] = useState(null);
  const [spreadsheetData, setSpreadsheetData] = useState([]);
  const [availableTransformations, setAvailableTransformations] = useState([]);
  const [availableImportTools, setAvailableImportTools] = useState([]);

  /** 🔥 Fetch Available Datasets **/
  useEffect(() => {
    axios.get("http://127.0.0.1:8000/api/datasets/")
      .then(response => {
        setDatasets(response.data.datasets);
        setActiveDataset(response.data.active_dataset);
        if (response.data.active_dataset) {
          fetchDatasetData(response.data.active_dataset);
        }
      })
      .catch(error => console.error("Error fetching datasets:", error));
  }, []);

  /** 🔥 Fetch Available Import Tools **/
  useEffect(() => {
    axios.get("http://127.0.0.1:8000/api/import/tools/")
      .then(response => setAvailableImportTools(response.data.available_import_tools))
      .catch(error => console.error("Error fetching import tools:", error));
  }, []);

  /** 🔥 Fetch Available Transformations **/
  useEffect(() => {
    axios.get("http://127.0.0.1:8000/api/transformations/tools/")
      .then(response => setAvailableTransformations(response.data.available_transformations))
      .catch(error => console.error("Error fetching transformations:", error));
  }, []);

  /** 🔥 Fetch Dataset Data for Spreadsheet **/
  const fetchDatasetData = (datasetName) => {
    axios.get(`http://127.0.0.1:8000/api/datasets/${datasetName}/`)
      .then(response => {
        const formattedData = response.data.data.map(row =>
          Object.values(row).map(value => ({ value }))
        );
        setSpreadsheetData(formattedData);
      })
      .catch(error => console.error("Error fetching dataset:", error));
  };

  /** 🔥 Handle File Upload **/
  const handleFileUpload = (datasetName) => {
    setDatasets([...datasets, datasetName]);
    setActiveDataset(datasetName);
    fetchDatasetData(datasetName);
    setShowImportModal(false);
  };

  /** 🔥 Handle Dataset Selection **/
  const handleDatasetSelection = (datasetName) => {
    setActiveDataset(datasetName);
    fetchDatasetData(datasetName);
  };

  /** 🔥 Handle Spreadsheet Data Change **/
  const handleSpreadsheetChange = (newData) => {
    setSpreadsheetData(newData);
  };

  /** 🔥 Save Dataset to Backend **/
  const saveDataset = () => {
    if (!activeDataset) return;

    const formattedData = spreadsheetData.map(row => {
      return row.reduce((acc, cell, index) => {
        acc[`column${index + 1}`] = cell.value;
        return acc;
      }, {});
    });

    axios.post(`http://127.0.0.1:8000/api/datasets/${activeDataset}/save/`, {
      data: formattedData
    }).then(() => {
      alert("Dataset saved successfully!");
    }).catch(error => {
      console.error("Error saving dataset:", error);
    });
  };

  return (
    <div className="app-container">
      {/* 🔥 Top Toolbar for Navigation */}
      <Toolbar 
        tools={["Analyze", "Visualize", "Transform", "Export"]}
        onOpenImport={() => setShowImportModal(true)}
        onSave={saveDataset}
      />

      {/* 🔥 Dataset Import Modal */}
      {showImportModal && (
        <FileImport 
          onFileUpload={handleFileUpload} 
          availableImportTools={availableImportTools}
        />
      )}

      {/* 🔥 Spreadsheet for Dataset Editing */}
      {activeDataset && (
        <SpreadsheetComponent 
          data={spreadsheetData} 
          onChange={handleSpreadsheetChange} 
          datasetName={activeDataset}
        />
      )}

      {/* 🔥 Transformation Panel */}
      {activeDataset && (
        <TransformationPanel 
          datasetName={activeDataset} 
          availableTransformations={availableTransformations}
        />
      )}
    </div>
  );
};

export default App;
