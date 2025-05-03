import React, { createContext, useContext, useState, useEffect } from "react";
import { fetchDatasets, fetchDataset, saveDataset } from "../services/api";
import useTransformations from "../hooks/useTransformations";

const AppContext = createContext();

export const useAppContext = () => useContext(AppContext);

export const AppProvider = ({ children }) => {
  // Datasets state
  const [datasets, setDatasets] = useState([]);
  const [activeDataset, setActiveDataset] = useState(null);
  const [spreadsheetData, setSpreadsheetData] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  
  // UI state
  const [activeTab, setActiveTab] = useState("spreadsheet"); // spreadsheet, analyze, visualize, clean, transform, export
  
  // Get transformations
  const { availableTransformations, isLoading: transformationsLoading } = 
    useTransformations();

  // Load datasets on mount
  useEffect(() => {
    const loadDatasets = async () => {
      try {
        setIsLoading(true);
        const data = await fetchDatasets();
        setDatasets(data);
      } catch (error) {
        console.error("Error fetching datasets:", error);
      } finally {
        setIsLoading(false);
      }
    };

    loadDatasets();
  }, []);

  // Handle dataset selection
  const handleDatasetSelect = async (datasetId) => {
    try {
      setIsLoading(true);
      setActiveDataset(datasetId);
      
      const data = await fetchDataset(datasetId);
      setSpreadsheetData(data);
    } catch (error) {
      console.error("Error fetching dataset:", error);
    } finally {
      setIsLoading(false);
    }
  };

  // Handle spreadsheet data changes
  const handleSpreadsheetChange = (newData) => {
    setSpreadsheetData(newData);
  };

  // Handle file upload
  const handleFileUpload = async (file, name) => {
    try {
      setIsLoading(true);
      // File upload logic handled by your backend
      // Refresh datasets after upload
      const updatedDatasets = await fetchDatasets();
      setDatasets(updatedDatasets);
      
      // Select the newly uploaded dataset
      if (updatedDatasets.includes(name)) {
        await handleDatasetSelect(name);
      }
    } catch (error) {
      console.error("Error uploading file:", error);
    } finally {
      setIsLoading(false);
    }
  };

  // Handle save dataset
  const handleSaveDataset = async () => {
    if (!activeDataset) return;

    try {
      await saveDataset(activeDataset, spreadsheetData);
      return true;
    } catch (error) {
      console.error("Error saving dataset:", error);
      return false;
    }
  };

  // Switch active tool
  const setActiveTool = (tool) => {
    setActiveTab(tool.toLowerCase());
  };

  // Context value
  const value = {
    // Data state
    datasets,
    activeDataset,
    spreadsheetData,
    isLoading: isLoading || transformationsLoading,
    availableTransformations,
    
    // UI state
    activeTab,
    
    // Handlers
    handleDatasetSelect,
    handleSpreadsheetChange,
    handleFileUpload,
    handleSaveDataset,
    setActiveTool
  };

  return (
    <AppContext.Provider value={value}>
      {children}
    </AppContext.Provider>
  );
};

export default AppContext;