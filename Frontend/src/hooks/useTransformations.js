import { useState, useEffect } from "react";
import { fetchTransformations } from "../services/api";

/**
 * Custom hook for managing transformations
 * @returns {Object} Transformation management functions and state
 */
const useTransformations = () => {
  const [availableTransformations, setAvailableTransformations] = useState([]);
  const [isLoading, setIsLoading] = useState(true);

  /**
   * Load transformations from the backend
   */
  const loadTransformations = async () => {
    setIsLoading(true);
    try {
      const transformations = await fetchTransformations();
      setAvailableTransformations(transformations);
    } catch (error) {
      console.error("Error loading transformations:", error);
    } finally {
      setIsLoading(false);
    }
  };

  // Load transformations on mount
  useEffect(() => {
    loadTransformations();
  }, []);

  return {
    availableTransformations,
    isLoading,
    loadTransformations,
  };
};

export default useTransformations;
