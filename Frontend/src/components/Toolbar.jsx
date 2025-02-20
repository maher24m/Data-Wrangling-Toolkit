import React from "react";
import "./Toolbar.css";

const Toolbar = ({ tools }) => {
  return (
    <nav className="toolbar">
      {tools.map((tool, index) => (
        <button key={index} className="btn btn-secondary">
          {tool}
        </button>
      ))}
    </nav>
  );
};

export default Toolbar;
