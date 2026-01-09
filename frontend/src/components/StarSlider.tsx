import React from 'react';

interface StarSliderProps {
  value: number;
  onChange: (value: number) => void;
  darkMode?: boolean;
}

export const StarSlider: React.FC<StarSliderProps> = ({ value, onChange, darkMode = false }) => {
  return (
    <div className="space-y-3">
      <div className="flex items-center justify-between">
        <span className={`text-sm font-medium ${darkMode ? 'text-gray-300' : 'text-gray-700'}`}>
          Confiabilidade
        </span>
        <span className={`text-sm ${darkMode ? 'text-gray-400' : 'text-gray-500'}`}>
          {value}/5 estrelas
        </span>
      </div>
      
      <div className="flex items-center space-x-2">
        {Array.from({ length: 5 }, (_, i) => {
          const starValue = i + 1;
          const isFilled = starValue <= value;
          
          return (
            <button
              key={i}
              type="button"
              onClick={() => onChange(starValue)}
              className="group transition-transform hover:scale-110 focus:outline-none"
            >
              <svg
                className={`w-8 h-8 transition-colors ${
                  isFilled 
                    ? 'text-yellow-400 drop-shadow-sm' 
                    : darkMode 
                      ? 'text-gray-600 hover:text-gray-500' 
                      : 'text-gray-300 hover:text-gray-400'
                }`}
                fill="currentColor"
                viewBox="0 0 20 20"
              >
                <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
              </svg>
            </button>
          );
        })}
      </div>
    </div>
  );
};