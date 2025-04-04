import React, { useState, useEffect } from "react";
import axios from "axios";
import Toolbar from "./components/Toolbar";
import FileImport from "./components/FileImport";
import SpreadsheetComponent from "./components/SpreadsheetComponent";
import TransformationPanel from "./components/TransformationPanel";
import "./App.css";

const App = () => {
  const [datasets, setDatasets] = useState([]); // List of datasets
  const [activeDataset, setActiveDataset] = useState(null); // Currently selected dataset
  const [spreadsheetData, setSpreadsheetData] = useState([]); // Data for spreadsheet
  const [availableTransformations, setAvailableTransformations] = useState([]); // Backend transformations
  const [isLoading, setIsLoading] = useState(true); // Loading state

  /** 🔥 Fetch Datasets from Backend */
  const fetchDatasets = async () => {
    setIsLoading(true);
    try {
      const response = await axios.get("http://127.0.0.1:8000/api/datasets/");
      const fetchedDatasets = response.data.datasets;

      setDatasets(fetchedDatasets);

      if (fetchedDatasets.length > 0) {
        setActiveDataset(fetchedDatasets[0]); // ✅ Set first dataset as active
      } else {
        setActiveDataset(null); // ✅ No dataset available
      }
    } catch (error) {
      console.error("Error fetching datasets:", error);
    } finally {
      setIsLoading(false);
    }
  };

  /** 🔥 Fetch Dataset Data (Runs AFTER `activeDataset` updates) */
  useEffect(() => {
    if (activeDataset) {
      console.log("🔥 Fetching data for dataset:", activeDataset);
      fetchDatasetData(activeDataset);
    } else {
      setSpreadsheetData([]); // ✅ Reset spreadsheet if no dataset is active
    }
  }, [activeDataset]); // ✅ Runs only when `activeDataset` changes

  const fetchDatasetData = async (datasetName) => {
    console.log("🔥 Fetching dataset data for:", datasetName);
  
    axios.get(`http://127.0.0.1:8000/api/datasets/${datasetName}/`)
      .then(response => {
        try {
          console.log("✅ DEBUG: Raw API Response ->", response.data);
  
          if (!response.data || typeof response.data !== "object") {
            console.log(typeof response.data);
            throw new Error("Invalid JSON format received");
          }
  
          if (Array.isArray(response.data.data)) {
            const formattedData = response.data.data.map(row =>
              Object.values(row).map(value => ({ value }))
            );
            console.log("✅ DEBUG: Formatted Data ->", formattedData);
  
            setSpreadsheetData([...formattedData]);  // ✅ Ensures re-render
          } else {
            console.error("❌ ERROR: Unexpected data format:", response.data);
          }
        } catch (jsonError) {
          console.error("❌ ERROR: JSON Parsing Failed", jsonError);
        }
      })
      .catch(error => {
        console.error("❌ ERROR: Fetching dataset failed:", error);
      });
  };
  

  /** 🔥 Handle File Upload */
  const handleFileUpload = (datasetName) => {
    setActiveDataset(datasetName); // ✅ Update active dataset
    fetchDatasets(); // ✅ Refresh dataset list
  };

  /** 🔥 Handle Spreadsheet Changes */
  const handleSpreadsheetChange = (newData) => {
    setSpreadsheetData(newData);
  };

  /** 🔥 Save Dataset to Backend */
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
      alert("Failed to save dataset.");
    });
  };

  /** 🔥 Fetch Available Transformations */
  useEffect(() => {
    axios.get("http://127.0.0.1:8000/api/transformations/tools/")
      .then(response => setAvailableTransformations(response.data.transformation_tools))
      .catch(error => console.error("Error fetching transformations:", error));
  }, []);

  /** 🔥 Load Datasets on Mount */
  useEffect(() => {
    fetchDatasets();
  }, []);

  console.log("Datasets:", datasets);
  console.log("Active dataset:", activeDataset);
  console.log("Spreadsheet data:", spreadsheetData);

  return (
    <div className="app-container">
      <Toolbar 
        tools={["Analyze", "Visualize", "Transform", "Export"]}
        onSave={saveDataset}
      />

      {/* 🔥 Show Loader While Fetching Data */}
      {isLoading ? (
        <p>Loading...</p>
      ) : datasets.length === 0 ? (
        <FileImport onFileUpload={handleFileUpload} />
      ) : (
        <>
          {/* 🔥 Dataset Spreadsheet */}
          {activeDataset && spreadsheetData.length > 0 && (
            <SpreadsheetComponent 
              data={spreadsheetData} 
              onChange={handleSpreadsheetChange} 
              datasetName={activeDataset}
            />
          )}


        </>
      )}
    </div>
  );
};

export default App;
