import { useState, useEffect } from "react";
import { fetchDatasets, fetchDatasetData } from "../services/api";

/**
 * Custom hook for managing datasets
 * @returns {Object} Dataset management functions and state
 */
const useDatasets = () => {
  const [datasets, setDatasets] = useState([]); // List of datasets
  const [activeDataset, setActiveDataset] = useState(null); // Currently selected dataset
  const [spreadsheetData, setSpreadsheetData] = useState([]); // Data for spreadsheet
  const [isLoading, setIsLoading] = useState(true); // Loading state

  /**
   * Load datasets from the backend
   */
  const loadDatasets = async () => {
    setIsLoading(true);
    try {
      const fetchedDatasets = await fetchDatasets();
      setDatasets(fetchedDatasets);

      if (fetchedDatasets.length > 0) {
        setActiveDataset(fetchedDatasets[0]); // Set first dataset as active
      } else {
        setActiveDataset(null); // No dataset available
      }
    } catch (error) {
      console.error("Error loading datasets:", error);
    } finally {
      setIsLoading(false);
    }
  };

  /**
   * Load data for the active dataset
   */
  const loadDatasetData = async (datasetName) => {
    if (!datasetName) return;

    try {
      const response = await fetchDatasetData(datasetName);

      if (Array.isArray(response.data)) {
        const formattedData = response.data.map((row) =>
          Object.values(row).map((value) => ({ value }))
        );

        setSpreadsheetData(formattedData);
      } else {
        console.error("Unexpected data format:", response);
      }
    } catch (error) {
      console.error(`Error loading dataset ${datasetName}:`, error);
    }
  };

  /**
   * Handle dataset selection
   */
  const handleDatasetSelect = (datasetName) => {
    setActiveDataset(datasetName);
  };

  /**
   * Handle spreadsheet data changes
   */
  const handleSpreadsheetChange = (newData) => {
    setSpreadsheetData(newData);
  };

  /**
   * Handle file upload
   */
  const handleFileUpload = (datasetName) => {
    setActiveDataset(datasetName);
    loadDatasets(); // Refresh dataset list
  };

  // Load datasets on mount
  useEffect(() => {
    loadDatasets();
  }, []);

  // Load dataset data when active dataset changes
  useEffect(() => {
    if (activeDataset) {
      loadDatasetData(activeDataset);
    } else {
      setSpreadsheetData([]); // Reset spreadsheet if no dataset is active
    }
  }, [activeDataset]);

  return {
    datasets,
    activeDataset,
    spreadsheetData,
    isLoading,
    handleDatasetSelect,
    handleSpreadsheetChange,
    handleFileUpload,
    loadDatasets,
  };
};

export default useDatasets;
