import axios from "axios";

const API_BASE_URL = "http://127.0.0.1:8000/api";

// Create axios instance with default config
const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000, // 30 seconds timeout
  headers: {
    "Content-Type": "application/json",
  },
});

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    const errorMessage = error.response?.data?.message || error.message;
    console.error("API Error:", errorMessage);
    return Promise.reject(error);
  }
);

/**
 * Fetch all datasets from the backend
 * @returns {Promise<Array<string>>} Promise with array of dataset names
 * @throws {Error} If the API request fails
 */
export const fetchDatasets = async () => {
  try {
    const response = await api.get("/datasets/");
    return response.data.datasets;
  } catch (error) {
    throw new Error(`Failed to fetch datasets: ${error.message}`);
  }
};

/**
 * Fetch data for a specific dataset
 * @param {string} datasetName - Name of the dataset to fetch
 * @returns {Promise<Object>} Promise with the dataset data
 * @throws {Error} If the API request fails
 */
export const fetchDatasetData = async (datasetName) => {
  try {
    const response = await api.get(`/datasets/${datasetName}/`);
    return response.data.data;
  } catch (error) {
    throw new Error(`Failed to fetch dataset ${datasetName}: ${error.message}`);
  }
};

/**
 * Save dataset data to the backend
 * @param {string} datasetName - Name of the dataset to save
 * @param {Array<Object>} data - Data to save
 * @returns {Promise<Object>} Promise with the save result
 * @throws {Error} If the API request fails
 */
export const saveDataset = async (datasetName, data) => {
  try {
    const response = await api.post(`/datasets/${datasetName}/save/`, {
      data: data,
    });
    return response.data;
  } catch (error) {
    throw new Error(`Failed to save dataset ${datasetName}: ${error.message}`);
  }
};

/**
 * Delete a dataset
 * @param {string} datasetName - Name of the dataset to delete
 * @returns {Promise<Object>} Promise with the delete result
 * @throws {Error} If the API request fails
 */
export const deleteDataset = async (datasetName) => {
  try {
    const response = await api.delete(`/datasets/${datasetName}/delete/`);
    return response.data;
  } catch (error) {
    throw new Error(
      `Failed to delete dataset ${datasetName}: ${error.message}`
    );
  }
};

/**
 * Upload a new dataset file
 * @param {File} file - The file to upload
 * @param {string} datasetName - Name for the dataset
 * @param {Function} onProgress - Callback for upload progress
 * @returns {Promise<Object>} Promise with the upload result
 * @throws {Error} If the API request fails
 */
export const uploadDataset = async (file, datasetName, onProgress) => {
  try {
    const formData = new FormData();
    formData.append("file", file);
    formData.append("dataset_name", datasetName);

    const response = await api.post("/import/", formData, {
      headers: {
        "Content-Type": "multipart/form-data",
      },
      onUploadProgress: (progressEvent) => {
        const percentCompleted = Math.round(
          (progressEvent.loaded * 100) / progressEvent.total
        );
        onProgress?.(percentCompleted);
      },
    });
    return response.data;
  } catch (error) {
    throw new Error(`Failed to upload dataset: ${error.message}`);
  }
};

/**
 * Fetch allowed file types for import
 * @returns {Promise<Array<string>>} Promise with array of allowed file types
 * @throws {Error} If the API request fails
 */
export const fetchAllowedFileTypes = async () => {
  try {
    const response = await api.get("/import/tools/");
    return response.data.import_tools;
  } catch (error) {
    throw new Error(`Failed to fetch allowed file types: ${error.message}`);
  }
};

// Export the api instance for direct use if needed
export default api;
