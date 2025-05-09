import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { 
  Dashboard as DashboardIcon,
  DateRange as DateRangeIcon, 
  ShowChart as ShowChartIcon,
  CloudUpload as CloudUploadIcon,
  Logout as LogoutIcon
} from '@mui/icons-material';

const Sidebar = () => {
  const location = useLocation();
  const path = location.pathname;
  
  return (
    <div className="sidebar">
      <div className="p-4 flex items-center justify-center">
        <div className="w-12 h-12 bg-white rounded-full flex items-center justify-center">
          <span className="text-primary text-xl font-bold">WH</span>
        </div>
        <div className="ml-3">
          <h3 className="text-white font-bold text-lg">Work History</h3>
        </div>
      </div>
      
      <div className="mt-8 px-2 flex-1">
        <Link to="/">
          <div className={`sidebar-nav-item ${path === '/' ? 'active' : ''}`}>
            <div className="flex items-center">
              <DashboardIcon className="mr-3" fontSize="small" />
              <span>Dashboard</span>
            </div>
          </div>
        </Link>
        
        <Link to="/yearly-analysis">
          <div className={`sidebar-nav-item ${path === '/yearly-analysis' ? 'active' : ''}`}>
            <div className="flex items-center">
              <DateRangeIcon className="mr-3" fontSize="small" />
              <span>Yearly Analysis</span>
            </div>
          </div>
        </Link>
        
        <Link to="/metric-detail/planned_hours">
          <div className={`sidebar-nav-item ${path.startsWith('/metric-detail') ? 'active' : ''}`}>
            <div className="flex items-center">
              <ShowChartIcon className="mr-3" fontSize="small" />
              <span>Metrics Detail</span>
            </div>
          </div>
        </Link>
        
        <Link to="/upload-data">
          <div className={`sidebar-nav-item ${path === '/upload-data' ? 'active' : ''}`}>
            <div className="flex items-center">
              <CloudUploadIcon className="mr-3" fontSize="small" />
              <span>Upload Data</span>
            </div>
          </div>
        </Link>
      </div>
      
      <div className="p-4 border-t border-opacity-20 border-white">
        <div className="flex items-center mb-3">
          <div className="w-8 h-8 bg-success rounded-full flex items-center justify-center">
            <span className="text-white font-bold">AP</span>
          </div>
          <div className="ml-2">
            <div className="text-white font-semibold text-sm">Admin Panel</div>
            <div className="text-gray-400 text-xs">Operations Manager</div>
          </div>
        </div>
        
        <button className="flex items-center text-gray-400 hover:text-white transition-colors">
          <LogoutIcon className="mr-2" fontSize="small" />
          <span className="text-sm">Logout</span>
        </button>
      </div>
    </div>
  );
};

export default Sidebar;