import React from 'react';
import KeyboardArrowUpIcon from '@mui/icons-material/KeyboardArrowUp';
import KeyboardArrowDownIcon from '@mui/icons-material/KeyboardArrowDown';
import HelpOutlineIcon from '@mui/icons-material/HelpOutline';
import { Tooltip } from '@mui/material';

const MetricCard = ({ title, value, delta, icon, iconColor = "#1E88E5", helpText }) => {
  // Determine if delta is positive, negative, or neutral
  const isDeltaPositive = delta && !delta.startsWith('-');
  const isDeltaNegative = delta && delta.startsWith('-');

  // Icon background color with opacity
  const bgColorStyle = {
    backgroundColor: `${iconColor}20`,
  };

  return (
    <div className="metric-card">
      {helpText && (
        <Tooltip title={helpText} placement="top" arrow>
          <div className="absolute top-2.5 right-2.5 text-lightGray cursor-help">
            <HelpOutlineIcon fontSize="small" />
          </div>
        </Tooltip>
      )}
      <div className="flex items-start">
        {icon && (
          <div className="metric-card-icon" style={bgColorStyle}>
            <span style={{ color: iconColor }}>{icon}</span>
          </div>
        )}
        <div>
          <div className="metric-card-title">{title}</div>
          <div className="metric-card-value">{value}</div>
          
          {delta && (
            <div 
              className={`flex items-center mt-1 ${
                isDeltaPositive 
                  ? 'text-success' 
                  : isDeltaNegative 
                    ? 'text-error' 
                    : 'text-gray-500'
              }`}
            >
              {isDeltaPositive && <KeyboardArrowUpIcon fontSize="small" />}
              {isDeltaNegative && <KeyboardArrowDownIcon fontSize="small" />}
              <span className="ml-1 font-medium">{delta}</span>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default MetricCard;