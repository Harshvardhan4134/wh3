import React, { createContext, useState, useEffect, useContext } from 'react';
import axios from 'axios';

// Create context
const DataContext = createContext();

// Custom hook for using the context
export const useData = () => useContext(DataContext);

export const DataProvider = ({ children }) => {
  // Main dashboard data
  const [summaryMetrics, setSummaryMetrics] = useState(null);
  const [yearlySummary, setYearlySummary] = useState([]);
  const [customerData, setCustomerData] = useState(null);
  const [workcenterData, setWorkcenterData] = useState(null);
  
  // Yearly analysis data
  const [selectedYear, setSelectedYear] = useState(new Date().getFullYear());
  const [yearData, setYearData] = useState(null);
  
  // Metrics detail data
  const [selectedMetric, setSelectedMetric] = useState('planned_hours');
  const [metricData, setMetricData] = useState(null);
  
  // Loading states
  const [loading, setLoading] = useState({
    dashboard: true,
    yearlyAnalysis: true,
    metricDetail: true
  });
  
  // Load dashboard data
  useEffect(() => {
    const fetchDashboardData = async () => {
      setLoading(prev => ({ ...prev, dashboard: true }));
      try {
        // Load real data from API endpoints
        const yearsResponse = await axios.get('/api/yearly_summary');
        const metricsResponse = await axios.get('/api/summary_metrics');
        const customersResponse = await axios.get('/api/customer_profitability');
        const workcentersResponse = await axios.get('/api/workcenter_trends');
        
        setYearlySummary(yearsResponse.data);
        setSummaryMetrics(metricsResponse.data);
        setCustomerData(customersResponse.data);
        setWorkcenterData(workcentersResponse.data);
        
        // Set the most recent year as default selected year
        if (yearsResponse.data && yearsResponse.data.length > 0) {
          const sortedYears = [...yearsResponse.data].sort((a, b) => b.year - a.year);
          setSelectedYear(parseInt(sortedYears[0].year));
        }
      } catch (error) {
        console.error('Error loading dashboard data:', error);
        // Show error message to user
        setYearlySummary([]);
        setSummaryMetrics(null);
        setCustomerData(null);
        setWorkcenterData(null);
      }
      setLoading(prev => ({ ...prev, dashboard: false }));
    };
    
    fetchDashboardData();
  }, []);
  
  // Load year data when selectedYear changes
  useEffect(() => {
    const fetchYearData = async () => {
      if (!selectedYear) return;
      
      setLoading(prev => ({ ...prev, yearlyAnalysis: true }));
      try {
        const response = await axios.get(`/api/year_data/${selectedYear}`);
        setYearData(response.data);
      } catch (error) {
        console.error(`Error loading data for year ${selectedYear}:`, error);
        // Show error message to user
        setYearData(null);
      }
      setLoading(prev => ({ ...prev, yearlyAnalysis: false }));
    };
    
    fetchYearData();
  }, [selectedYear]);
  
  // Load metric data when selectedMetric changes
  useEffect(() => {
    const fetchMetricData = async () => {
      if (!selectedMetric) return;
      
      setLoading(prev => ({ ...prev, metricDetail: true }));
      try {
        const response = await axios.get(`/api/metric_data/${selectedMetric}`);
        setMetricData(response.data);
      } catch (error) {
        console.error(`Error loading data for metric ${selectedMetric}:`, error);
        // Show error message to user
        setMetricData(null);
      }
      setLoading(prev => ({ ...prev, metricDetail: false }));
    };
    
    fetchMetricData();
  }, [selectedMetric]);
  
  // Format function for consistent number formatting
  const formatNumber = (value, digits = 1) => {
    if (value === undefined || value === null) return '0';
    
    return new Intl.NumberFormat('en-US', {
      minimumFractionDigits: digits,
      maximumFractionDigits: digits
    }).format(value);
  };
  
  // Format function for currency
  const formatMoney = (value) => {
    if (value === undefined || value === null) return '$0';
    
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0
    }).format(value);
  };
  
  // Format function for percentages
  const formatPercent = (value) => {
    if (value === undefined || value === null) return '0%';
    
    return new Intl.NumberFormat('en-US', {
      style: 'percent',
      minimumFractionDigits: 1,
      maximumFractionDigits: 1
    }).format(value / 100);
  };
  
  const value = {
    // Data
    summaryMetrics,
    yearlySummary,
    customerData,
    workcenterData,
    yearData,
    metricData,
    
    // Selections
    selectedYear,
    setSelectedYear,
    selectedMetric,
    setSelectedMetric,
    
    // Loading states
    loading,
    
    // Utility functions
    formatNumber,
    formatMoney,
    formatPercent
  };
  
  return (
    <DataContext.Provider value={value}>
      {children}
    </DataContext.Provider>
  );
};