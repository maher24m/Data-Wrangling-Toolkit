import React from "react";
import { Routes, Route, Navigate } from "react-router-dom";
import Toolbar from "./components/Toolbar";
import FileImportPage from "./pages/FileImportPage";
import DatasetSelection from "./pages/DatasetSelection";
import SpreadsheetPage from "./pages/SpreadSheet";
import "./App.css";

const App = () => {
  return (
    <div className="app-container">
      <Toolbar tools={["Analyze", "Visualize", "Transform", "Export"]} />

      <div className="main-content">
        <div className="content">
          <Routes>
            <Route path="/" element={<Navigate to="/import" replace />} />
            <Route path="/import" element={<FileImportPage />} />
            <Route path="/datasets" element={<DatasetSelection />} />
            <Route
              path="/spreadsheet/:datasetId"
              element={<SpreadsheetPage />}
            />
          </Routes>
        </div>
      </div>
    </div>
  );
};

export default App;
