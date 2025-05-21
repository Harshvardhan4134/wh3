import React, { useState, useEffect } from 'react';
import { useSearchParams } from 'react-router-dom';
import { useData } from '../context/DataContext';
import Card from '../components/Card';
import MetricCard from '../components/MetricCard';
import { 
  FilterList as FilterIcon, 
  CalendarToday as CalendarIcon,
  GetApp as DownloadIcon
} from '@mui/icons-material';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend
} from 'chart.js';
import { Bar } from 'react-chartjs-2';
import { Tab, Tabs, Box } from '@mui/material';

// Register ChartJS components
ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend
);

// TabPanel component for handling tabs
function TabPanel(props) {
  const { children, value, index, ...other } = props;

  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      id={`simple-tabpanel-${index}`}
      aria-labelledby={`simple-tab-${index}`}
      {...other}
    >
      {value === index && (
        <Box sx={{ p: 2 }}>
          {children}
        </Box>
      )}
    </div>
  );
}

const YearlyAnalysis = () => {
  const [searchParams] = useSearchParams();
  const { 
    selectedYear, 
    setSelectedYear, 
    yearData, 
    loading,
    formatNumber,
    formatMoney,
    formatPercent
  } = useData();
  
  const [tabValue, setTabValue] = useState(0);
  
  // Get year from URL if present
  useEffect(() => {
    const yearParam = searchParams.get('year');
    if (yearParam) {
      setSelectedYear(parseInt(yearParam));
    }
  }, [searchParams, setSelectedYear]);
  
  const handleTabChange = (event, newValue) => {
    setTabValue(newValue);
  };
  
  if (loading.yearlyAnalysis) {
    return (
      <div className="flex justify-center items-center h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-primary"></div>
      </div>
    );
  }
  
  if (!yearData) {
    return (
      <div className="flex flex-col justify-center items-center h-64 my-12">
        <div className="text-6xl mb-4">📊</div>
        <h2 className="text-2xl font-semibold mb-4">No data available for {selectedYear}</h2>
        <p className="text-lightGray mb-6">Please select a different year or upload more data.</p>
      </div>
    );
  }

  // Prepare quarterly chart data
  const quarterlyChartData = {
    labels: yearData.quarterly_summary.map(item => `Q${item.quarter}`),
    datasets: [
      {
        type: 'bar',
        label: 'Planned Hours',
        data: yearData.quarterly_summary.map(item => item.planned_hours),
        backgroundColor: '#1E88E5',
        borderColor: '#1E88E5',
        borderWidth: 1,
        yAxisID: 'y',
      },
      {
        type: 'bar',
        label: 'Actual Hours',
        data: yearData.quarterly_summary.map(item => item.actual_hours),
        backgroundColor: '#e5383b',
        borderColor: '#e5383b',
        borderWidth: 1,
        yAxisID: 'y',
      },
      {
        type: 'line',
        label: 'Overrun Cost',
        data: yearData.quarterly_summary.map(item => item.overrun_cost),
        borderColor: '#FFA000',
        backgroundColor: '#FFA000',
        borderWidth: 2,
        yAxisID: 'y1',
        pointBackgroundColor: '#FFA000',
        pointBorderColor: '#FFA000',
        pointRadius: 4,
        tension: 0.1,
      },
    ],
  };
  
  const quarterlyChartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'top',
      },
      tooltip: {
        callbacks: {
          label: function(context) {
            let label = context.dataset.label || '';
            if (label) {
              label += ': ';
            }
            if (context.dataset.yAxisID === 'y1') {
              label += formatMoney(context.parsed.y);
            } else {
              label += formatNumber(context.parsed.y, 0);
            }
            return label;
          }
        }
      }
    },
    scales: {
      y: {
        type: 'linear',
        display: true,
        position: 'left',
        title: {
          display: true,
          text: 'Hours'
        }
      },
      y1: {
        type: 'linear',
        display: true,
        position: 'right',
        title: {
          display: true,
          text: 'Overrun Cost ($)'
        },
        grid: {
          drawOnChartArea: false,
        },
      },
    },
  };
  
  // Calculate quarter-to-quarter changes
  const firstQuarter = yearData.quarterly_summary[0] || {};
  const lastQuarter = yearData.quarterly_summary[yearData.quarterly_summary.length - 1] || {};
  
  const hoursChange = ((lastQuarter.actual_hours - firstQuarter.actual_hours) / 
                      firstQuarter.actual_hours) * 100 || 0;
  
  const jobsChange = ((lastQuarter.total_jobs - firstQuarter.total_jobs) / 
                     firstQuarter.total_jobs) * 100 || 0;
  
  const costChange = ((lastQuarter.overrun_cost - firstQuarter.overrun_cost) / 
                     firstQuarter.overrun_cost) * 100 || 0;

  return (
    <div className="space-y-8 pb-8">
      {/* Year Selection Section */}
      <Card className="mb-8">
        <div className="flex justify-between items-center">
          <h3 className="text-lg font-semibold">Select Year for Analysis</h3>
          <button className="bg-primary text-white px-4 py-2 rounded-md text-sm flex items-center shadow-card">
            <DownloadIcon fontSize="small" className="mr-1" />
            Export Data
          </button>
        </div>
        <div className="mt-4">
          <p className="text-lightGray mb-4">Select a year to view detailed performance metrics and operational breakdowns.</p>
          
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <div className="col-span-3">
              <div className="flex space-x-4">
                {[2021, 2022, 2023].map((year) => (
                  <button
                    key={year}
                    onClick={() => setSelectedYear(year)}
                    className={`px-6 py-2 rounded-md text-sm font-medium ${
                      selectedYear === year 
                        ? 'bg-primary text-white' 
                        : 'bg-white text-gray-700 border border-gray-200'
                    }`}
                  >
                    {year}
                  </button>
                ))}
              </div>
            </div>
            <div>
              <button className="w-full bg-primary text-white px-4 py-2 rounded-md text-sm font-medium">
                Load Year Data
              </button>
            </div>
          </div>
        </div>
      </Card>
      
      {/* Year Summary Section */}
      <div>
        <div className="flex justify-between items-center mb-4">
          <h2>Year Summary - {selectedYear}</h2>
          <div className="bg-white px-4 py-2 rounded-lg shadow-card text-gray-700 flex items-center">
            <CalendarIcon fontSize="small" className="mr-2" />
            {new Date().toLocaleDateString('en-US', { month: 'short', day: '2-digit', year: 'numeric' })}
          </div>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-4">
          <MetricCard 
            title="Planned Hours" 
            value={formatNumber(yearData.summary.total_planned_hours)} 
            icon="⏱️" 
          />
          <MetricCard 
            title="Actual Hours" 
            value={formatNumber(yearData.summary.total_actual_hours)} 
            icon="⌛" 
          />
          <MetricCard 
            title="Overrun Hours" 
            value={formatNumber(yearData.summary.total_overrun_hours)} 
            icon="⚠️" 
            iconColor="#e5383b" 
          />
          <MetricCard 
            title="Ghost Hours" 
            value={formatNumber(yearData.summary.ghost_hours)} 
            icon="👻" 
            iconColor="#6c757d" 
            helpText="Planned time with no recorded work"
          />
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-4">
          <MetricCard 
            title="Unplanned Hours" 
            value={formatNumber(yearData.summary.unplanned_hours)} 
            icon="❓" 
            iconColor="#ff9800"
            helpText="Actual time with no planning"
          />
          <MetricCard 
            title="Ghost Hours Cost" 
            value={formatMoney(yearData.summary.ghost_hours_cost)} 
            icon="💰" 
            iconColor="#6c757d"
          />
          <MetricCard 
            title="Unplanned Hours Cost" 
            value={formatMoney(yearData.summary.unplanned_hours_cost)} 
            icon="💵" 
            iconColor="#ff9800"
          />
          <MetricCard 
            title="Total NCR Hours" 
            value={formatNumber(yearData.summary.total_ncr_hours)} 
            icon="⚙️" 
            iconColor="#FFA000" 
          />
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-4">
          <MetricCard 
            title="Scrap Cost" 
            value={formatMoney(yearData.summary.ncr_costs.scrap)} 
            icon="🗑️" 
            iconColor="#d32f2f"
            helpText="Cost of scrapped parts"
          />
          <MetricCard 
            title="Rework Cost" 
            value={formatMoney(yearData.summary.ncr_costs.rework)} 
            icon="🔄" 
            iconColor="#f57c00"
            helpText="Cost of rework operations"
          />
          <MetricCard 
            title="Repair Cost" 
            value={formatMoney(yearData.summary.ncr_costs.repair)} 
            icon="🔧" 
            iconColor="#f57c00"
            helpText="Cost of repair operations"
          />
          <MetricCard 
            title="Other NCR Cost" 
            value={formatMoney(yearData.summary.ncr_costs.other)} 
            icon="📝" 
            iconColor="#f57c00"
            helpText="Other NCR-related costs"
          />
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          <MetricCard 
            title="Planned Cost" 
            value={formatMoney(yearData.summary.total_planned_cost)} 
            icon="💰" 
            iconColor="#2E7D32" 
          />
          <MetricCard 
            title="Actual Cost" 
            value={formatMoney(yearData.summary.total_actual_cost)} 
            icon="💵" 
            iconColor="#2E7D32" 
          />
          <MetricCard 
            title="Total NCR Cost" 
            value={formatMoney(yearData.summary.ncr_costs.total)} 
            icon="⚙️" 
            iconColor="#FFA000"
          />
          <MetricCard 
            title="Total Jobs" 
            value={formatNumber(yearData.summary.total_jobs, 0)} 
            icon="🔧" 
          />
        </div>
      </div>
      
      {/* Quarterly Breakdown Section */}
      <div>
        <div className="flex justify-between items-center mb-4">
          <h2>Quarterly Summary</h2>
          <div className="bg-white px-4 py-2 rounded-lg shadow-card text-gray-700 flex items-center">
            <FilterIcon fontSize="small" className="mr-2" />
            Record by Quarter
          </div>
        </div>
        
        <Card>
          <div className="grid grid-cols-1 lg:grid-cols-5 gap-6">
            <div className="lg:col-span-2">
              <h3 className="text-lg font-semibold mb-4">Quarterly Performance</h3>
              
              <div className="overflow-x-auto">
                <table className="min-w-full divide-y divide-gray-200">
                  <thead>
                    <tr>
                      <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Quarter</th>
                      <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Planned</th>
                      <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Actual</th>
                      <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Overrun</th>
                      <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Cost</th>
                      <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Jobs</th>
                    </tr>
                  </thead>
                  <tbody className="bg-white divide-y divide-gray-200">
                    {yearData.quarterly_summary.map((quarter, idx) => (
                      <tr key={idx} className="hover:bg-gray-50">
                        <td className="px-4 py-3 whitespace-nowrap text-sm font-medium">Q{quarter.quarter}</td>
                        <td className="px-4 py-3 whitespace-nowrap text-sm text-gray-500">{formatNumber(quarter.planned_hours)}</td>
                        <td className="px-4 py-3 whitespace-nowrap text-sm text-gray-500">{formatNumber(quarter.actual_hours)}</td>
                        <td className="px-4 py-3 whitespace-nowrap text-sm text-gray-500">{formatNumber(quarter.overrun_hours)}</td>
                        <td className="px-4 py-3 whitespace-nowrap text-sm text-gray-500">{formatMoney(quarter.overrun_cost)}</td>
                        <td className="px-4 py-3 whitespace-nowrap text-sm text-gray-500">{formatNumber(quarter.total_jobs, 0)}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
            
            <div className="lg:col-span-3">
              <h3 className="text-lg font-semibold mb-4">Hours vs Cost</h3>
              <div className="h-80">
                <Bar data={quarterlyChartData} options={quarterlyChartOptions} />
              </div>
            </div>
          </div>
          
          {/* Quarter-to-Quarter Performance */}
          <div className="mt-8">
            <h3 className="text-lg font-semibold mb-4">Quarter-to-Quarter Performance</h3>
            
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <MetricCard 
                title="Hours Change (Q1 to Q4)" 
                value={formatNumber(lastQuarter.actual_hours - firstQuarter.actual_hours)}
                delta={formatPercent(hoursChange/100)}
                icon="⏱️"
                iconColor="#1E88E5"
              />
              
              <MetricCard 
                title="Jobs Change (Q1 to Q4)" 
                value={formatNumber(lastQuarter.total_jobs - firstQuarter.total_jobs, 0)}
                delta={formatPercent(jobsChange/100)}
                icon="🔧"
                iconColor="#4CAF50"
              />
              
              <MetricCard 
                title="Cost Change (Q1 to Q4)" 
                value={formatMoney(lastQuarter.overrun_cost - firstQuarter.overrun_cost)}
                delta={formatPercent(costChange/100)}
                icon="💵"
                iconColor="#FFA000"
              />
            </div>
          </div>
        </Card>
      </div>
      
      {/* Tabbed Analysis Sections */}
      <div>
        <Box sx={{ borderBottom: 1, borderColor: 'divider' }}>
          <Tabs value={tabValue} onChange={handleTabChange} aria-label="analysis tabs">
            <Tab label="🔥 Overruns" id="tab-0" />
            <Tab label="⚠️ NCR Summary" id="tab-1" />
            <Tab label="🏭 Work Centers" id="tab-2" />
            <Tab label="🔁 Repeat NCRs" id="tab-3" />
            <Tab label="🛠 Adjustments" id="tab-4" />
          </Tabs>
        </Box>
        
        {/* Overruns Tab */}
        <TabPanel value={tabValue} index={0}>
          <Card>
            <h3 className="text-xl font-semibold mb-6">Top Operational Overruns</h3>
            
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
              {yearData.top_overruns && (
                <>
                  <MetricCard 
                    title="Total Overrun Cost" 
                    value={formatMoney(yearData.top_overruns.reduce((sum, item) => sum + item.overrun_cost, 0))}
                    iconColor="#e5383b"
                  />
                  
                  <MetricCard 
                    title="Total Overrun Hours" 
                    value={formatNumber(yearData.top_overruns.reduce((sum, item) => sum + item.overrun_hours, 0))}
                    iconColor="#e5383b"
                  />
                  
                  <MetricCard 
                    title="Affected Operations" 
                    value={formatNumber(yearData.top_overruns.length, 0)}
                    iconColor="#e5383b"
                  />
                </>
              )}
            </div>
            
            <div className="overflow-x-auto">
              <table className="min-w-full divide-y divide-gray-200">
                <thead>
                  <tr>
                    <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Job</th>
                    <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Part</th>
                    <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Work Center</th>
                    <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Task</th>
                    <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Planned</th>
                    <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Actual</th>
                    <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Overrun</th>
                    <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Cost</th>
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-gray-200">
                  {yearData.top_overruns && yearData.top_overruns.map((overrun, idx) => (
                    <tr key={idx} className="hover:bg-gray-50">
                      <td className="px-4 py-3 whitespace-nowrap text-sm font-medium text-primary">{overrun.job_number}</td>
                      <td className="px-4 py-3 whitespace-nowrap text-sm text-gray-500">{overrun.part_name}</td>
                      <td className="px-4 py-3 whitespace-nowrap text-sm text-gray-500">{overrun.work_center}</td>
                      <td className="px-4 py-3 whitespace-nowrap text-sm text-gray-500">{overrun.task_description}</td>
                      <td className="px-4 py-3 whitespace-nowrap text-sm text-gray-500">{formatNumber(overrun.planned_hours)}</td>
                      <td className="px-4 py-3 whitespace-nowrap text-sm text-gray-500">{formatNumber(overrun.actual_hours)}</td>
                      <td className="px-4 py-3 whitespace-nowrap text-sm font-medium text-error">{formatNumber(overrun.overrun_hours)}</td>
                      <td className="px-4 py-3 whitespace-nowrap text-sm font-medium text-error">{formatMoney(overrun.overrun_cost)}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </Card>
        </TabPanel>
        
        {/* Other tabs would follow similar pattern */}
        <TabPanel value={tabValue} index={1}>
          <Card>
            <h3 className="text-xl font-semibold mb-6">Non-Conformance Reports</h3>
            {/* NCR content would go here */}
            <p className="text-lightGray">NCR summary content for {selectedYear}</p>
          </Card>
        </TabPanel>
        
        <TabPanel value={tabValue} index={2}>
          <Card>
            <h3 className="text-xl font-semibold mb-6">Work Center Efficiency</h3>
            {/* Work center content would go here */}
            <p className="text-lightGray">Work center analysis content for {selectedYear}</p>
          </Card>
        </TabPanel>
        
        <TabPanel value={tabValue} index={3}>
          <Card>
            <h3 className="text-xl font-semibold mb-6">Repeat NCRs</h3>
            {/* Repeat NCR content would go here */}
            <p className="text-lightGray">Repeat NCR analysis for {selectedYear}</p>
          </Card>
        </TabPanel>
        
        <TabPanel value={tabValue} index={4}>
          <Card>
            <h3 className="text-xl font-semibold mb-6">Job Adjustments</h3>
            {/* Adjustments content would go here */}
            <p className="text-lightGray">Job adjustments content for {selectedYear}</p>
          </Card>
        </TabPanel>
      </div>
    </div>
  );
};

export default YearlyAnalysis;