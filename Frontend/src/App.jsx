import React, { useState } from "react";
import Toolbar from "./components/Toolbar";
import DatasetSelection from "./pages/DatasetSelection";
import "./App.css";

const App = () => {
  const [currentView, setCurrentView] = useState("import");
  const [activeDataset, setActiveDataset] = useState(null);

  const handleViewChange = (view) => {
    setCurrentView(view);
  };

  return (
    <div className="app-container">
      <Toolbar
        tools={["Analyze", "Visualize", "Transform", "Export"]}
        activeView={currentView}
        activeDataset={activeDataset}
        onViewChange={handleViewChange}
      />

      <div className="main-content">
        <div className="content">
          <DatasetSelection />
        </div>
      </div>
    </div>
  );
};

export default App;
