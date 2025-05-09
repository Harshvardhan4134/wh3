import React from 'react';
import { Search as SearchIcon, CalendarToday as CalendarIcon, Notifications as NotificationIcon } from '@mui/icons-material';
import { useLocation } from 'react-router-dom';

const Header = () => {
  const location = useLocation();
  const path = location.pathname;
  
  // Get page title based on current route
  const getPageTitle = () => {
    switch (true) {
      case path === '/':
        return 'Work History Dashboard';
      case path === '/yearly-analysis':
        return 'Yearly Analysis';
      case path.startsWith('/metric-detail'):
        return 'Metrics Detail';
      case path === '/upload-data':
        return 'Upload Data';
      default:
        return 'Work History Dashboard';
    }
  };
  
  // Get current date in format "May 09, 2025"
  const currentDate = new Date().toLocaleDateString('en-US', {
    month: 'short',
    day: '2-digit',
    year: 'numeric'
  });
  
  return (
    <div className="mb-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="mb-0">{getPageTitle()}</h1>
          <p className="text-lightGray mt-1">An executive analysis of shop performance</p>
        </div>
        
        <div className="flex items-center">
          <div className="bg-white rounded-lg px-3 py-2 mr-4 shadow-card flex items-center">
            <CalendarIcon className="text-lightGray" fontSize="small" />
            <span className="ml-2 text-gray-700">{currentDate}</span>
          </div>
          
          <div className="bg-white rounded-lg px-3 py-2 shadow-card flex items-center w-64">
            <SearchIcon className="text-lightGray" fontSize="small" />
            <input 
              type="text"
              placeholder="Search..."
              className="ml-2 outline-none border-none bg-transparent w-full text-gray-700 placeholder-lightGray"
            />
          </div>
          
          <div className="ml-4 relative">
            <div className="bg-white p-2 rounded-full shadow-card hover:bg-gray-50 cursor-pointer">
              <NotificationIcon className="text-lightGray" />
              <span className="absolute top-0 right-0 w-3 h-3 bg-red-500 rounded-full"></span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Header;