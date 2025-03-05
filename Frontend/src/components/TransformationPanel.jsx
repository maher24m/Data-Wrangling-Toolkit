import React from "react";
import "./TransformationPanel.css";

const TransformationPanel = ({ datasetName, availableTransformations }) => {
  return (
    <div className="transformation-panel">
      <h3>Apply Transformations</h3>
      <ul>
        {availableTransformations.map((transformation, index) => (
          <li key={index}>{transformation}</li>
        ))}
      </ul>
    </div>
  );
};

export default TransformationPanel;
