import React, { useState, useEffect } from "react";
import axios from "axios";
import Spreadsheet from "react-spreadsheet";
import Toolbar from "./components/Toolbar";
import FileImport from "./components/FileImport";
import "bootstrap/dist/css/bootstrap.min.css";
import "./App.css";

const App = () => {
  const [selectedDataset, setSelectedDataset] = useState(null);
  const [fileData, setFileData] = useState([]);
  const [totalRows, setTotalRows] = useState(0);
  const [page, setPage] = useState(1);
  const limit = 100; // Max rows per page

  // Handle file upload & select dataset
  const handleFileUpload = (data, datasetName) => {
    setSelectedDataset(datasetName);
    setPage(1); // Reset to page 1
    fetchDataset(datasetName, 1);
  };

  // Fetch dataset from backend with pagination
  const fetchDataset = (datasetName, pageNumber) => {
    axios.get(`http://127.0.0.1:8000/api/dataset/${datasetName}/?page=${pageNumber}&limit=${limit}`)
      .then((response) => {
        setFileData(response.data.data);
        setTotalRows(response.data.total_rows);
        setPage(pageNumber);
      });
  };

  // Handle next/previous page
  const handlePageChange = (newPage) => {
    if (newPage > 0 && newPage <= Math.ceil(totalRows / limit)) {
      fetchDataset(selectedDataset, newPage);
    }
  };

  return (
    <div className="app-container">
      <Toolbar tools={["File", "Undo", "Redo", "Analyze", "Visual", "Transformation", "Plugins"]} />

      <div className="content">
        {!selectedDataset ? (
          <FileImport onFileUpload={handleFileUpload} />
        ) : (
          <>
            <h2 className="dataset-title">Dataset: {selectedDataset}</h2>
            <div className="spreadsheet-container">
              <Spreadsheet data={fileData} onChange={() => {}} />
            </div>

            {/* Pagination Controls */}
            <div className="pagination-controls">
              <button 
                className="btn btn-secondary"
                onClick={() => handlePageChange(page - 1)}
                disabled={page === 1}
              >
                Previous
              </button>
              <span> Page {page} of {Math.ceil(totalRows / limit)} </span>
              <button 
                className="btn btn-secondary"
                onClick={() => handlePageChange(page + 1)}
                disabled={page * limit >= totalRows}
              >
                Next
              </button>
            </div>
          </>
        )}
      </div>
    </div>
  );
};

export default App;
