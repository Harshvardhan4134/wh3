import React, { createContext, useState, useEffect, useContext } from 'react';
import axios from 'axios';

// Constants
export const BURDEN_RATE = 184; // $184 per hour
export const NCR_CATEGORIES = {
  SCRAP: 'scrap',
  REWORK: 'rework',
  REPAIR: 'repair',
  OTHER: 'other'
};

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
  
  // Calculate ghost hours and costs
  const calculateGhostHours = (planned, actual) => {
    if (planned > 0 && actual === 0) {
      return {
        hours: planned,
        cost: planned * BURDEN_RATE
      };
    }
    return { hours: 0, cost: 0 };
  };

  // Calculate unplanned actual hours
  const calculateUnplannedHours = (planned, actual) => {
    if (planned === 0 && actual > 0) {
      return {
        hours: actual,
        cost: actual * BURDEN_RATE
      };
    }
    return { hours: 0, cost: 0 };
  };

  // Calculate NCR costs by category
  const calculateNCRCosts = (ncrData) => {
    return {
      [NCR_CATEGORIES.SCRAP]: ncrData.scrap_hours * BURDEN_RATE,
      [NCR_CATEGORIES.REWORK]: ncrData.rework_hours * BURDEN_RATE,
      [NCR_CATEGORIES.REPAIR]: ncrData.repair_hours * BURDEN_RATE,
      [NCR_CATEGORIES.OTHER]: ncrData.other_hours * BURDEN_RATE,
      total: (ncrData.scrap_hours + ncrData.rework_hours + ncrData.repair_hours + ncrData.other_hours) * BURDEN_RATE
    };
  };
  
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
        
        // Process the data to include new metrics
        const processedYearlySummary = yearsResponse.data.map(year => ({
          ...year,
          ghost_hours: calculateGhostHours(year.planned_hours, year.actual_hours).hours,
          ghost_hours_cost: calculateGhostHours(year.planned_hours, year.actual_hours).cost,
          unplanned_hours: calculateUnplannedHours(year.planned_hours, year.actual_hours).hours,
          unplanned_hours_cost: calculateUnplannedHours(year.planned_hours, year.actual_hours).cost,
          ncr_costs: calculateNCRCosts(year.ncr_data || {
            scrap_hours: 0,
            rework_hours: 0,
            repair_hours: 0,
            other_hours: 0
          })
        }));

        const processedMetrics = {
          ...metricsResponse.data,
          burden_rate: BURDEN_RATE,
          total_ghost_hours: processedYearlySummary.reduce((sum, year) => sum + year.ghost_hours, 0),
          total_ghost_hours_cost: processedYearlySummary.reduce((sum, year) => sum + year.ghost_hours_cost, 0),
          total_unplanned_hours: processedYearlySummary.reduce((sum, year) => sum + year.unplanned_hours, 0),
          total_unplanned_hours_cost: processedYearlySummary.reduce((sum, year) => sum + year.unplanned_hours_cost, 0)
        };
        
        setYearlySummary(processedYearlySummary);
        setSummaryMetrics(processedMetrics);
        setCustomerData(customersResponse.data);
        setWorkcenterData(workcentersResponse.data);
        
        // Set the most recent year as default selected year
        if (processedYearlySummary.length > 0) {
          const sortedYears = [...processedYearlySummary].sort((a, b) => b.year - a.year);
          setSelectedYear(parseInt(sortedYears[0].year));
        }
      } catch (error) {
        console.error('Error loading dashboard data:', error);
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
    
    // Constants
    BURDEN_RATE,
    NCR_CATEGORIES,
    
    // Utility functions
    formatNumber,
    formatMoney,
    formatPercent,
    calculateGhostHours,
    calculateUnplannedHours,
    calculateNCRCosts
  };
  
  return (
    <DataContext.Provider value={value}>
      {children}
    </DataContext.Provider>
  );
};