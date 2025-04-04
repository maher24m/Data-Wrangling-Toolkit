import React, { useState, useEffect } from "react";
import { FileUploader } from "react-drag-drop-files";
import axios from "axios";
import "./FileImport.css";

const FileImport = ({ onFileUpload }) => {
  const [file, setFile] = useState(null);
  const [allowedFileTypes, setAllowedFileTypes] = useState([]); // Get from backend
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState(null);

  // Fetch allowed file types from backend
  useEffect(() => {
    axios.get("http://127.0.0.1:8000/api/import/tools/")
      .then(response => setAllowedFileTypes(response.data.import_tools))
      .catch(error => {
        console.error("Error fetching file types:", error);
        setError("Failed to fetch allowed file types.");
      });
  }, []);

  // Handle file selection
  const handleFileChange = (selectedFile) => {
    if (!selectedFile) return;

    // If multiple files are selected, pick the first one
    if (Array.isArray(selectedFile)) {
      selectedFile
    }

    if (!selectedFile.name) {
      setError("Invalid file. Please try again.");
      return;
    }

    setFile(selectedFile);
  };

  // Handle file upload to backend
  const uploadDataset = async () => {
    if (!file) {
      alert("No file selected.");
      return;
    }

    setUploading(true);
    setError(null);

    const formData = new FormData();
    formData.append("file", file);
    formData.append("dataset_name", "h1"); // Remove file extension

    try {
      const response = await axios.post("http://127.0.0.1:8000/api/import/", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });

      alert(`Import successful: ${response.data.dataset_name}`);
      onFileUpload(response.data.dataset_name); // Update parent component
    } catch (error) {
      console.error("Import failed:", error);
      setError("Failed to upload dataset. Try again.");
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="file-import-container">
      <h3>Upload Your Dataset</h3>

      {/* File Drag & Drop */}
      <FileUploader
        handleChange={handleFileChange}
        name="file"
        types={allowedFileTypes}
        multiple={false}
      />

      {file && <p className="file-name">Selected File: {file.name}</p>}
      {error && <p className="error-message">{error}</p>}

      {/* Upload Button */}
      {file && (
        <button className="import-btn" onClick={uploadDataset} disabled={uploading}>
          {uploading ? "Uploading..." : "Confirm Import"}
        </button>
      )}
    </div>
  );
};

export default FileImport;
