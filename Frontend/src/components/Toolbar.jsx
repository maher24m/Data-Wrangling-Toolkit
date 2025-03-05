import React from "react";
import "./Toolbar.css";

const Toolbar = ({ tools, onOpenImport, onSave }) => {
  return (
    <nav className="toolbar">
      {tools.map((tool, index) => (
        <button key={index} className="btn btn-secondary">
          {tool}
        </button>
      ))}
      <button className="btn btn-primary" onClick={onOpenImport}>Import Data</button>
      <button className="btn btn-success" onClick={onSave}>Save Dataset</button>
    </nav>
  );
};

export default Toolbar;
