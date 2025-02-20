import React, { useState } from "react";
import Spreadsheet from "react-spreadsheet";
import Toolbar from "./components/Toolbar";
import "./App.css";

const App = () => {
  const [tools, setTools] = useState(["File", "Undo", "Redo", "Analyze", "Visual", "Transformation", "Plugins"]);

  // Generate sample data
  const generateData = () => {
    let rows = [];
    for (let i = 0; i < 20; i++) {
      let row = [];
      for (let j = 0; j < 6; j++) {
        row.push({ value: Math.floor(Math.random() * 100) + 60 }); // Random % values
      }
      rows.push(row);
    }
    return rows;
  };

  const [data, setData] = useState(generateData());

  return (
    <div className="app-container">
      <Toolbar tools={tools} />
      <div className="content">
        <h2 className="dataset-title">Dataset Name: Student Performance</h2>
        <div className="spreadsheet-container">
          <Spreadsheet data={data} onChange={setData} />
        </div>
      </div>
    </div>
  );
};

export default App;
