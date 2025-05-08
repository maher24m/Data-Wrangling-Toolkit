// frontend/src/pages/FileImportPage.jsx
import React, { useState } from "react";
import FileImport from "../components/FileImport";
// import "./FileImport.css";

const FileImportPage = ({ onDatasetUploaded }) => {
  // State for FileImport component
  const [file, setFile] = useState(null);
  const [allowedFileTypes, setAllowedFileTypes] = useState([]);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState(null);
  const [importSuccess, setImportSuccess] = useState(false);
  const [datasetName, setDatasetName] = useState("");
  const [uploadProgress, setUploadProgress] = useState(0);

  // Helper function to format file size
  const formatFileSize = (bytes) => {
    if (bytes === 0) return "0 Bytes";
    const k = 1024;
    const sizes = ["Bytes", "KB", "MB", "GB"];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + " " + sizes[i];
  };

  // Helper function to get display name for file types
  const getDisplayName = (type) => {
    return type.toUpperCase();
  };

  return (
    <FileImport
      file={file}
      allowedFileTypes={allowedFileTypes}
      uploading={uploading}
      error={error}
      importSuccess={importSuccess}
      datasetName={datasetName}
      uploadProgress={uploadProgress}
      onFileChange={(file, types) => {
        setFile(file);
        if (types) setAllowedFileTypes(types);
      }}
      onDatasetNameChange={(e) => setDatasetName(e.target.value)}
      onUpload={(progress) => {
        setUploadProgress(progress);
        if (progress === 100) {
          setImportSuccess(true);
          onDatasetUploaded(datasetName);
        }
      }}
      formatFileSize={formatFileSize}
      getDisplayName={getDisplayName}
    />
  );
};

export default FileImportPage;
