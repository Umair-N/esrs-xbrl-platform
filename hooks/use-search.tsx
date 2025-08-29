import { useState, useEffect } from 'react';

// Custom hook to debounce the search input
function useDebounceSearch(value: string, delay: number): string {
  const [debouncedValue, setDebouncedValue] = useState(value);

  useEffect(() => {
    const handler = setTimeout(() => {
      setDebouncedValue(value); // Update debounced value after delay
    }, delay);

    // Cleanup the timeout if the value changes before the delay is over
    return () => {
      clearTimeout(handler);
    };
  }, [value, delay]);

  return debouncedValue; // Return the debounced value
}

export default useDebounceSearch;
