import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Sidebar from './components/Sidebar';
import Header from './components/Header';
import Dashboard from './pages/Dashboard';
import YearlyAnalysis from './pages/YearlyAnalysis';
import MetricsDetail from './pages/MetricsDetail';
import UploadData from './pages/UploadData';
import { DataProvider } from './context/DataContext';
import './styles/global.css';

function App() {
  return (
    <DataProvider>
      <Router>
        <div className="app-container">
          <Sidebar />
          <div className="main-content">
            <Header />
            <div className="page-content">
              <Routes>
                <Route path="/" element={<Dashboard />} />
                <Route path="/yearly-analysis" element={<YearlyAnalysis />} />
                <Route path="/metrics-detail" element={<MetricsDetail />} />
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