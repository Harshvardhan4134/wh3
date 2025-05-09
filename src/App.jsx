import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Sidebar from './components/Sidebar';
import Header from './components/Header';
import Dashboard from './pages/Dashboard';
import YearlyAnalysis from './pages/YearlyAnalysis';
import MetricDetail from './pages/MetricDetail';
import UploadData from './pages/UploadData';
import { DataProvider } from './context/DataContext';

function App() {
  return (
    <DataProvider>
      <Router>
        <div className="flex">
          <Sidebar />
          <div className="main-content">
            <Header />
            <div className="page-content">
              <Routes>
                <Route path="/" element={<Dashboard />} />
                <Route path="/yearly-analysis" element={<YearlyAnalysis />} />
                <Route path="/metric-detail/:metric" element={<MetricDetail />} />
                <Route path="/upload-data" element={<UploadData />} />
              </Routes>
            </div>
          </div>
        </div>
      </Router>
    </DataProvider>
  );
}

export default App;