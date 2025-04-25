import axios from "axios";

const API_BASE_URL = "http://127.0.0.1:8000/api";

/**
 * Fetch all datasets from the backend
 * @returns {Promise} Promise with the datasets data
 */
export const fetchDatasets = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/datasets/`);
    return response.data.datasets;
  } catch (error) {
    console.error("Error fetching datasets:", error);
    throw error;
  }
};

/**
 * Fetch data for a specific dataset
 * @param {string} datasetName - Name of the dataset to fetch
 * @returns {Promise} Promise with the dataset data
 */
export const fetchDatasetData = async (datasetName) => {
  try {
    const response = await axios.get(
      `${API_BASE_URL}/datasets/${datasetName}/`
    );
    return response.data;
  } catch (error) {
    console.error(`Error fetching dataset ${datasetName}:`, error);
    throw error;
  }
};

/**
 * Save dataset data to the backend
 * @param {string} datasetName - Name of the dataset to save
 * @param {Array} data - Data to save
 * @returns {Promise} Promise with the save result
 */
export const saveDataset = async (datasetName, data) => {
  try {
    const formattedData = data.map((row) => {
      return row.reduce((acc, cell, index) => {
        acc[`column${index + 1}`] = cell.value;
        return acc;
      }, {});
    });

    const response = await axios.post(
      `${API_BASE_URL}/datasets/${datasetName}/save/`,
      {
        data: formattedData,
      }
    );
    return response.data;
  } catch (error) {
    console.error(`Error saving dataset ${datasetName}:`, error);
    throw error;
  }
};

/**
 * Fetch available transformations from the backend
 * @returns {Promise} Promise with the transformations data
 */
export const fetchTransformations = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/transformations/tools/`);
    return response.data.transformation_tools;
  } catch (error) {
    console.error("Error fetching transformations:", error);
    throw error;
  }
};
