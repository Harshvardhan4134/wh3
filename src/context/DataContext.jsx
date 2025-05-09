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
        // In a real app, these would be API calls
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
        
        // For demo purposes, load mock data
        // This would be replaced with proper error handling in a production app
        loadMockData();
      }
      setLoading(prev => ({ ...prev, dashboard: false }));
    };
    
    // Mock data function - in a real app, this would be removed
    const loadMockData = () => {
      const mockYearlySummary = [
        { year: "2021", planned_hours: 8500, actual_hours: 9200, overrun_hours: 700, ncr_hours: 350, job_count: 512, operation_count: 2850, customer_count: 14 },
        { year: "2022", planned_hours: 9100, actual_hours: 9800, overrun_hours: 700, ncr_hours: 320, job_count: 550, operation_count: 3050, customer_count: 16 },
        { year: "2023", planned_hours: 9600, actual_hours: 10200, overrun_hours: 600, ncr_hours: 280, job_count: 580, operation_count: 3200, customer_count: 18 }
      ];
      
      const mockSummaryMetrics = {
        total_planned_hours: 27200,
        total_actual_hours: 29200,
        total_overrun_hours: 2000,
        total_ncr_hours: 950,
        total_planned_cost: 5412800,
        total_actual_cost: 5810800,
        total_jobs: 1642,
        overrun_percent: 7.35
      };
      
      const mockCustomerData = {
        top_customer_list_name: "GlobalTech Industries",
        overrun_customer_list_name: "MetalWorks Inc",
        repeat_rate: 68,
        avg_margin: 12.5,
        profit_data: [
          { customer: "GlobalTech Industries", planned_hours: 3600, actual_hours: 3650, profit_margin: 18.2 },
          { customer: "MetalWorks Inc", planned_hours: 2800, actual_hours: 3200, profit_margin: 8.4 },
          { customer: "AeroSpace Systems", planned_hours: 2600, actual_hours: 2700, profit_margin: 14.7 },
          { customer: "Precision Parts Ltd", planned_hours: 2100, actual_hours: 2150, profit_margin: 15.2 },
          { customer: "Industrial Solutions", planned_hours: 1950, actual_hours: 2050, profit_margin: 11.5 }
        ]
      };
      
      const mockWorkcenterData = {
        most_used_wc: "MILLING",
        overrun_wc: "ASSEMBLY",
        avg_util: 82.5,
        total_wc_hours: 29200,
        work_center_data: [
          { work_center: "MILLING", planned_hours: 5600, actual_hours: 5900, overrun_hours: 300 },
          { work_center: "LATHE", planned_hours: 4800, actual_hours: 5000, overrun_hours: 200 },
          { work_center: "ASSEMBLY", planned_hours: 4200, actual_hours: 4700, overrun_hours: 500 },
          { work_center: "WELDING", planned_hours: 3900, actual_hours: 4100, overrun_hours: 200 },
          { work_center: "ENGINEERING", planned_hours: 3800, actual_hours: 3900, overrun_hours: 100 },
          { work_center: "INSPECTION", planned_hours: 2700, actual_hours: 2800, overrun_hours: 100 },
          { work_center: "FINISHING", planned_hours: 2200, actual_hours: 2300, overrun_hours: 100 }
        ]
      };
      
      setYearlySummary(mockYearlySummary);
      setSummaryMetrics(mockSummaryMetrics);
      setCustomerData(mockCustomerData);
      setWorkcenterData(mockWorkcenterData);
      setSelectedYear(2023);
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
        
        // For demo, load mock year data
        const mockYearData = {
          summary: {
            total_planned_hours: 9600,
            total_actual_hours: 10200,
            total_overrun_hours: 600,
            ghost_hours: 120,
            total_ncr_hours: 280,
            total_planned_cost: 1910400,
            total_actual_cost: 2029800,
            opportunity_cost_dollars: 119400,
            recommended_buffer_percent: 8.5,
            total_jobs: 580,
            total_operations: 3200,
            total_unique_parts: 185
          },
          quarterly_summary: [
            { quarter: "Q1", planned_hours: 2400, actual_hours: 2550, overrun_hours: 150, overrun_cost: 29850, total_jobs: 145 },
            { quarter: "Q2", planned_hours: 2350, actual_hours: 2500, overrun_hours: 150, overrun_cost: 29850, total_jobs: 140 },
            { quarter: "Q3", planned_hours: 2450, actual_hours: 2600, overrun_hours: 150, overrun_cost: 29850, total_jobs: 147 },
            { quarter: "Q4", planned_hours: 2400, actual_hours: 2550, overrun_hours: 150, overrun_cost: 29850, total_jobs: 148 }
          ],
          top_overruns: [
            { job_number: "J23-452", part_name: "Hydraulic Cylinder", work_center: "ASSEMBLY", task_description: "Final Assembly", planned_hours: 45, actual_hours: 62, overrun_hours: 17, overrun_cost: 3383 },
            { job_number: "J23-398", part_name: "Turbine Housing", work_center: "MILLING", task_description: "CNC Milling", planned_hours: 38, actual_hours: 52, overrun_hours: 14, overrun_cost: 2786 },
            { job_number: "J23-512", part_name: "Control Manifold", work_center: "MILLING", task_description: "Precision Machining", planned_hours: 42, actual_hours: 54, overrun_hours: 12, overrun_cost: 2388 }
          ],
          workcenter_summary: [
            { work_center: "MILLING", job_count: 125, planned_hours: 2100, actual_hours: 2240, overrun_hours: 140, overrun_cost: 27860 },
            { work_center: "ASSEMBLY", job_count: 110, planned_hours: 1850, actual_hours: 2000, overrun_hours: 150, overrun_cost: 29850 },
            { work_center: "LATHE", job_count: 95, planned_hours: 1650, actual_hours: 1750, overrun_hours: 100, overrun_cost: 19900 },
            { work_center: "WELDING", job_count: 85, planned_hours: 1480, actual_hours: 1560, overrun_hours: 80, overrun_cost: 15920 },
            { work_center: "ENGINEERING", job_count: 75, planned_hours: 1300, actual_hours: 1350, overrun_hours: 50, overrun_cost: 9950 },
            { work_center: "INSPECTION", job_count: 50, planned_hours: 720, actual_hours: 750, overrun_hours: 30, overrun_cost: 5970 },
            { work_center: "FINISHING", job_count: 40, planned_hours: 500, actual_hours: 550, overrun_hours: 50, overrun_cost: 9950 }
          ],
          ncr_summary: [
            { part_name: "Hydraulic Cylinder", total_ncr_hours: 45, total_ncr_cost: 8955, ncr_occurrences: 3 },
            { part_name: "Control Manifold", total_ncr_hours: 38, total_ncr_cost: 7562, ncr_occurrences: 2 },
            { part_name: "Bearing Housing", total_ncr_hours: 32, total_ncr_cost: 6368, ncr_occurrences: 2 }
          ],
          repeat_ncr_failures: [
            { part_name: "Hydraulic Cylinder", repeat_ncr_hours: 45, ncr_job_count: 3 },
            { part_name: "Control Manifold", repeat_ncr_hours: 38, ncr_job_count: 2 }
          ]
        };
        setYearData(mockYearData);
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
        
        // For demo, load mock metric data
        const mockMetricData = {
          metric_name: selectedMetric,
          metric_description: "Total hours planned for work center operations",
          current_value: 9600,
          yearly_trend: [
            { year: 2021, value: 8500 },
            { year: 2022, value: 9100 },
            { year: 2023, value: 9600 }
          ],
          breakdown_by_customer: [
            { customer: "GlobalTech Industries", value: 1920 },
            { customer: "MetalWorks Inc", value: 1440 },
            { customer: "AeroSpace Systems", value: 1250 },
            { customer: "Precision Parts Ltd", value: 1100 },
            { customer: "Industrial Solutions", value: 950 }
          ],
          breakdown_by_workcenter: [
            { work_center: "MILLING", value: 2100 },
            { work_center: "ASSEMBLY", value: 1850 },
            { work_center: "LATHE", value: 1650 },
            { work_center: "WELDING", value: 1480 },
            { work_center: "ENGINEERING", value: 1300 },
            { work_center: "INSPECTION", value: 720 },
            { work_center: "FINISHING", value: 500 }
          ],
          correlated_metrics: [
            { metric: "actual_hours", correlation: 0.92 },
            { metric: "total_jobs", correlation: 0.86 },
            { metric: "operation_count", correlation: 0.89 }
          ]
        };
        setMetricData(mockMetricData);
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