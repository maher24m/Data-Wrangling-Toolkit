import React from "react";
import "./Toolbar.css"; // Import CSS for styling

const Toolbar = () => {
  const tools = ["File", "Undo", "Redo", "Analyze", "Visual", "Transformation", "Plugins"]; // needs to be non-static

  return (
    <div className="toolbar">
      {tools.map((tool, index) => (
        <button key={index} className="toolbar-button">
          {tool}
        </button>
      ))}
    </div>
  );
};

export default Toolbar;
