import React, { useState } from "react";
import { FileUploader } from "react-drag-drop-files";
import "./FileImport.css";

const fileTypes = ["CSV", "XLSX", "XLS", "JSON"]; // Allowed file types

const FileImport = ({ onFileUpload, availableImportTools }) => {
  const [fileName, setFileName] = useState(null);

  const handleFileChange = (file) => {
    setFileName(file.name);
    onFileUpload(file.name.replace(/\.[^/.]+$/, ""));
  };

  return (
    <div className="file-import-container">
      <h3>Upload Your File</h3>

      {/* Drag and Drop File Uploader */}
      <FileUploader handleChange={handleFileChange} name="file" types={fileTypes} />

      {/* Show available import plugins */}
      {availableImportTools.length > 0 && (
        <div className="import-tools">
          <h4>Available Import Plugins:</h4>
          <ul>
            {availableImportTools.map((tool, index) => (
              <li key={index}>{tool}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};

export default FileImport;
