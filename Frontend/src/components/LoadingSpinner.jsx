import React from "react";
import "./LoadingSpinner.css";

/**
 * LoadingSpinner component for displaying loading state
 * @returns {JSX.Element} LoadingSpinner component
 */
const LoadingSpinner = () => {
  return (
    <div className="loading-spinner-container">
      <div className="loading-spinner"></div>
      <p>Loading...</p>
    </div>
  );
};

export default LoadingSpinner;
