import React, { useState } from "react";
import Papa from "papaparse"; // CSV Parser
import * as XLSX from "xlsx"; // Excel Parser
import "./FileImport.css";

const FileImport = ({ onFileUpload }) => {
  const [fileName, setFileName] = useState(null);
  const [fileData, setFileData] = useState([]);
  const [numRows, setNumRows] = useState(5); // Default preview rows

  // Handle file selection
  const handleFileChange = (event) => {
    const file = event.target.files[0];
    processFile(file);
  };

  // Handle Drag & Drop
  const handleDrop = (event) => {
    event.preventDefault();
    const file = event.dataTransfer.files[0];
    processFile(file);
  };

  // Process CSV or Excel file
  const processFile = (file) => {
    if (!file) return;

    setFileName(file.name);
    const reader = new FileReader();

    if (file.name.endsWith(".csv")) {
      reader.onload = ({ target }) => {
        const parsedData = Papa.parse(target.result, { header: true });
        setFileData(parsedData.data);
      };
      reader.readAsText(file);
    } else if (file.name.endsWith(".xlsx") || file.name.endsWith(".xls")) {
      reader.onload = ({ target }) => {
        const workbook = XLSX.read(target.result, { type: "binary" });
        const sheetName = workbook.SheetNames[0];
        const sheet = workbook.Sheets[sheetName];
        const parsedData = XLSX.utils.sheet_to_json(sheet);
        setFileData(parsedData);
      };
      reader.readAsBinaryString(file);
    }
  };

  // Confirm Import
  const confirmImport = () => {
    onFileUpload(fileData.slice(0, numRows)); // Pass selected rows to parent
  };

  return (
    <div className="file-import-container">
      <div
        className="drop-zone"
        onDragOver={(e) => e.preventDefault()}
        onDrop={handleDrop}
      >
        <p>Drag & Drop your file here or</p>
        <input
          type="file"
          id="fileInput"
          className="file-input"
          onChange={handleFileChange}
          accept=".csv, .xlsx"
        />
        <label htmlFor="fileInput" className="upload-btn">
          Browse Files
        </label>
      </div>

      {fileName && (
        <>
          <p className="file-name">Selected File: {fileName}</p>


          {/* Dataset Preview Table */}
          {fileData.length > 0 && (
            <table className="preview-table">
              <thead>
                <tr>
                  {Object.keys(fileData[0]).map((key, index) => (
                    <th key={index}>{key}</th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {fileData.slice(0, numRows).map((row, rowIndex) => (
                  <tr key={rowIndex}>
                    {Object.values(row).map((value, colIndex) => (
                      <td key={colIndex}>{value}</td>
                    ))}
                  </tr>
                ))}
              </tbody>
            </table>
          )}

          {/* Confirm Import Button */}
          <button className="import-btn" onClick={confirmImport}>
            Confirm Import
          </button>
        </>
      )}
    </div>
  );
};

export default FileImport;
