import React from "react";
import { uploadDataset, fetchAllowedFileTypes } from "../services/api";
import "./FileImport.css";

const FileImport = ({
  file,
  allowedFileTypes,
  uploading,
  error,
  importSuccess,
  datasetName,
  uploadProgress,
  onFileChange,
  onDatasetNameChange,
  onUpload,
  formatFileSize,
  getDisplayName,
}) => {
  // Handle file upload using our API service
  const handleUpload = async () => {
    try {
      await uploadDataset(file, datasetName, (progress) => {
        // Update progress through the parent component
        onUpload(progress);
      });
      // Handle success
      onUpload(100); // Set to 100% when complete
    } catch (error) {
      // Error is already handled by our API service
      console.error("Upload failed:", error);
    }
  };

  // Fetch allowed file types when component mounts
  React.useEffect(() => {
    const loadAllowedTypes = async () => {
      try {
        const types = await fetchAllowedFileTypes();
        // Update allowed types through parent component
        onFileChange(null, types);
      } catch (error) {
        console.error("Failed to fetch allowed file types:", error);
      }
    };
    loadAllowedTypes();
  }, []);

  return (
    <div className="file-import-container">
      <h2>Import Your Dataset</h2>
      <p className="subtitle">Drag and drop your file or click to browse</p>

      {/* Display supported file types */}
      <div className="supported-types">
        {allowedFileTypes.length > 0 ? (
          <div className="file-type-badges">
            <p>Supported file types:</p>
            <div className="badge-container">
              {allowedFileTypes.map((type, index) => (
                <span key={index} className="file-type-badge">
                  {getDisplayName(type)}
                </span>
              ))}
            </div>
          </div>
        ) : (
          <p>Loading supported file types...</p>
        )}
      </div>

      {/* File Input */}
      <div className="custom-file-input-container">
        <label htmlFor="file-input" className="custom-file-input-label">
          <div className="drop-zone">
            <div className="drop-zone-content">
              <div className="upload-icon">
                <svg
                  width="40"
                  height="40"
                  viewBox="0 0 24 24"
                  fill="none"
                  xmlns="http://www.w3.org/2000/svg"
                >
                  <path
                    d="M12 18V6M7 11L12 6L17 11"
                    stroke="#4299e1"
                    strokeWidth="2"
                    strokeLinecap="round"
                    strokeLinejoin="round"
                  />
                  <path
                    d="M20 21H4"
                    stroke="#4299e1"
                    strokeWidth="2"
                    strokeLinecap="round"
                  />
                </svg>
              </div>
              <p className="drop-text">Drag & Drop your file here</p>
              <p className="or-text">- OR -</p>
              <button className="browse-button">Browse Files</button>
            </div>
          </div>
          <input
            id="file-input"
            type="file"
            className="hidden-file-input"
            onChange={(e) => onFileChange(e.target.files[0])}
          />
        </label>
      </div>

      {/* File Selected Info */}
      {file && (
        <div className="file-info">
          <div className="file-header">
            <div className="file-icon">
              {file.name.split(".").pop().toUpperCase()}
            </div>
            <div className="file-details">
              <p className="file-name">
                <strong>{file.name}</strong>
              </p>
              <p className="file-size">
                {formatFileSize(file.size)} • {new Date().toLocaleDateString()}
              </p>
            </div>
          </div>

          {/* Dataset Name Input */}
          <div className="dataset-name-input">
            <label htmlFor="dataset-name">Dataset Name:</label>
            <input
              type="text"
              id="dataset-name"
              value={datasetName}
              onChange={onDatasetNameChange}
              placeholder="Enter a name for your dataset"
            />
            <p className="input-help">
              This name will be used to identify your dataset in the system
            </p>
          </div>
        </div>
      )}

      {/* Error Message */}
      {error && <div className="error-message">{error}</div>}

      {/* Success Message */}
      {importSuccess && (
        <div className="success-message">
          <div className="success-icon">✓</div>
          <div>
            <p className="success-title">Import Successful!</p>
            <p>Dataset "{datasetName}" is ready to use</p>
          </div>
        </div>
      )}

      {/* Upload Progress */}
      {uploading && (
        <div className="upload-progress">
          <div className="progress-bar">
            <div
              className="progress-fill"
              style={{ width: `${uploadProgress}%` }}
            ></div>
          </div>
          <p className="progress-text">{uploadProgress}% Uploaded</p>
        </div>
      )}

      {/* Import Button */}
      {file && (
        <button
          className={`import-btn ${uploading ? "uploading" : ""}`}
          onClick={handleUpload}
          disabled={uploading || !datasetName.trim()}
        >
          {uploading ? (
            <>
              <span className="spinner"></span>
              Uploading...
            </>
          ) : (
            "Import Dataset"
          )}
        </button>
      )}

      {/* Info Text */}
      <div className="import-info">
        <h3>What happens next?</h3>
        <ul className="import-steps">
          <li>
            <span className="step-number">1</span>
            <span className="step-text">
              Your file will be uploaded and processed
            </span>
          </li>
          <li>
            <span className="step-number">2</span>
            <span className="step-text">
              The system will analyze your data structure
            </span>
          </li>
          <li>
            <span className="step-number">3</span>
            <span className="step-text">
              You'll be able to view, edit, and visualize your data
            </span>
          </li>
        </ul>
      </div>
    </div>
  );
};

export default FileImport;
