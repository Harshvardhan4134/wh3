import React, { useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { useData } from '../context/DataContext';
import Card from '../components/Card';
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
import { Bar, Line } from 'react-chartjs-2';
import { FilterList as FilterIcon } from '@mui/icons-material';

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

const MetricDetail = () => {
  const { metric } = useParams();
  const { 
    selectedMetric, 
    setSelectedMetric, 
    metricData, 
    loading,
    formatNumber,
    formatMoney,
    formatPercent
  } = useData();
  
  // Set the selected metric from URL parameter
  useEffect(() => {
    if (metric) {
      setSelectedMetric(metric);
    }
  }, [metric, setSelectedMetric]);
  
  if (loading.metricDetail) {
    return (
      <div className="flex justify-center items-center h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-primary"></div>
      </div>
    );
  }
  
  if (!metricData) {
    return (
      <div className="flex flex-col justify-center items-center h-64 my-12">
        <div className="text-6xl mb-4">📊</div>
        <h2 className="text-2xl font-semibold mb-4">No data available for this metric</h2>
        <p className="text-lightGray mb-6">Please select a different metric or upload more data.</p>
      </div>
    );
  }
  
  // Helper function to format metric value based on its type
  const formatMetricValue = (value, metric) => {
    if (metric.includes('cost') || metric.includes('dollars')) {
      return formatMoney(value);
    } else if (metric.includes('percent') || metric.includes('rate')) {
      return formatPercent(value/100);
    } else {
      return formatNumber(value);
    }
  };
  
  // Get display title for the metric
  const getMetricDisplayName = (metricKey) => {
    const displayNames = {
      'planned_hours': 'Planned Hours',
      'actual_hours': 'Actual Hours',
      'overrun_hours': 'Overrun Hours',
      'ncr_hours': 'NCR Hours',
      'planned_cost': 'Planned Cost',
      'actual_cost': 'Actual Cost',
      'overrun_cost': 'Overrun Cost',
      'opportunity_cost_dollars': 'Opportunity Cost',
      'total_jobs': 'Total Jobs',
      'total_operations': 'Total Operations',
      'planning_accuracy': 'Planning Accuracy',
    };
    
    return displayNames[metricKey] || metricKey.replace(/_/g, ' ').replace(/\b\w/g, c => c.toUpperCase());
  };
  
  // Prepare yearly trend chart data
  const yearlyTrendData = {
    labels: metricData.yearly_trend.map(item => item.year.toString()),
    datasets: [
      {
        label: getMetricDisplayName(selectedMetric),
        data: metricData.yearly_trend.map(item => item.value),
        borderColor: '#1E88E5',
        backgroundColor: 'rgba(30, 136, 229, 0.2)',
        fill: true,
        tension: 0.3,
        pointRadius: 6,
        pointHoverRadius: 8,
      }
    ]
  };
  
  const yearlyTrendOptions = {
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
            label += formatMetricValue(context.parsed.y, selectedMetric);
            return label;
          }
        }
      }
    },
    scales: {
      y: {
        beginAtZero: false,
        ticks: {
          callback: function(value) {
            return formatMetricValue(value, selectedMetric);
          }
        }
      }
    },
  };
  
  // Prepare customer breakdown chart data
  const customerData = {
    labels: metricData.breakdown_by_customer.map(item => item.customer),
    datasets: [
      {
        label: getMetricDisplayName(selectedMetric),
        data: metricData.breakdown_by_customer.map(item => item.value),
        backgroundColor: '#4CAF50',
        borderColor: '#2E7D32',
        borderWidth: 1,
      }
    ]
  };
  
  const customerOptions = {
    responsive: true,
    maintainAspectRatio: false,
    indexAxis: 'y',
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
            label += formatMetricValue(context.parsed.x, selectedMetric);
            return label;
          }
        }
      }
    },
    scales: {
      x: {
        beginAtZero: true,
        ticks: {
          callback: function(value) {
            return formatMetricValue(value, selectedMetric);
          }
        }
      }
    },
  };
  
  // Prepare work center breakdown chart data
  const workcenterData = {
    labels: metricData.breakdown_by_workcenter.map(item => item.work_center),
    datasets: [
      {
        label: getMetricDisplayName(selectedMetric),
        data: metricData.breakdown_by_workcenter.map(item => item.value),
        backgroundColor: '#1E88E5',
        borderColor: '#1E3A8A',
        borderWidth: 1,
      }
    ]
  };
  
  const workcenterOptions = {
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
            label += formatMetricValue(context.parsed.y, selectedMetric);
            return label;
          }
        }
      }
    },
    scales: {
      y: {
        beginAtZero: true,
        ticks: {
          callback: function(value) {
            return formatMetricValue(value, selectedMetric);
          }
        }
      }
    },
  };

  return (
    <div className="space-y-8 pb-8">
      {/* Metric Overview Section */}
      <div>
        <div className="flex justify-between items-center mb-4">
          <h2>{getMetricDisplayName(selectedMetric)} Analysis</h2>
          <div className="flex items-center space-x-4">
            <select
              value={selectedMetric}
              onChange={(e) => setSelectedMetric(e.target.value)}
              className="bg-white px-4 py-2 rounded-lg shadow-card text-gray-700 border border-gray-200 focus:outline-none focus:ring-2 focus:ring-primary"
            >
              <option value="planned_hours">Planned Hours</option>
              <option value="actual_hours">Actual Hours</option>
              <option value="overrun_hours">Overrun Hours</option>
              <option value="ncr_hours">NCR Hours</option>
              <option value="planned_cost">Planned Cost</option>
              <option value="actual_cost">Actual Cost</option>
              <option value="overrun_cost">Overrun Cost</option>
              <option value="total_jobs">Total Jobs</option>
              <option value="total_operations">Total Operations</option>
            </select>
            
            <div className="bg-white px-4 py-2 rounded-lg shadow-card text-gray-700 cursor-pointer flex items-center">
              <FilterIcon fontSize="small" className="mr-2" />
              Filter
            </div>
          </div>
        </div>
        
        <Card>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
            <div>
              <h3 className="text-xl font-semibold mb-4">{getMetricDisplayName(selectedMetric)} Overview</h3>
              <p className="text-lightGray mb-4">{metricData.metric_description}</p>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="bg-gray-50 rounded-lg p-4">
                  <div className="text-lightGray text-sm">Current Value</div>
                  <div className="text-2xl font-semibold mt-1">
                    {formatMetricValue(metricData.current_value, selectedMetric)}
                  </div>
                </div>
                
                <div className="bg-gray-50 rounded-lg p-4">
                  <div className="text-lightGray text-sm">Year-over-Year Change</div>
                  {metricData.yearly_trend.length >= 2 && (
                    <div className="text-2xl font-semibold mt-1">
                      {formatPercent((metricData.yearly_trend[metricData.yearly_trend.length - 1].value - 
                                     metricData.yearly_trend[metricData.yearly_trend.length - 2].value) / 
                                     metricData.yearly_trend[metricData.yearly_trend.length - 2].value)}
                    </div>
                  )}
                </div>
              </div>
            </div>
            
            <div>
              <h3 className="text-xl font-semibold mb-4">Correlated Metrics</h3>
              <div className="space-y-4">
                {metricData.correlated_metrics.map((item, idx) => (
                  <div key={idx} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                    <span className="font-medium">{getMetricDisplayName(item.metric)}</span>
                    <div className="flex items-center">
                      <div className="w-24 bg-gray-200 rounded-full h-2.5 mr-2">
                        <div 
                          className="bg-primary h-2.5 rounded-full" 
                          style={{ width: `${Math.abs(item.correlation) * 100}%` }}
                        ></div>
                      </div>
                      <span className={`font-semibold ${item.correlation >= 0 ? 'text-success' : 'text-error'}`}>
                        {(item.correlation >= 0 ? '+' : '') + formatNumber(item.correlation, 2)}
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
          
          <div>
            <h3 className="text-xl font-semibold mb-4">Yearly Trend</h3>
            <div className="h-80">
              <Line data={yearlyTrendData} options={yearlyTrendOptions} />
            </div>
          </div>
        </Card>
      </div>
      
      {/* Breakdown Analysis */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div>
          <Card title="Customer Breakdown">
            <div className="h-80">
              <Bar data={customerData} options={customerOptions} />
            </div>
          </Card>
        </div>
        
        <div>
          <Card title="Work Center Breakdown">
            <div className="h-80">
              <Bar data={workcenterData} options={workcenterOptions} />
            </div>
          </Card>
        </div>
      </div>
      
      {/* Impact Analysis */}
      <Card title="Impact Analysis">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-gray-50 p-4 rounded-lg">
            <h4 className="font-semibold mb-2">Business Impact</h4>
            <p className="text-lightGray text-sm">
              {selectedMetric.includes('cost') 
                ? "Directly affects profitability and budget projections."
                : selectedMetric.includes('hours')
                  ? "Impacts resource allocation, scheduling, and labor costs."
                  : "Influences operational efficiency and capacity planning."}
            </p>
          </div>
          
          <div className="bg-gray-50 p-4 rounded-lg">
            <h4 className="font-semibold mb-2">Improvement Opportunities</h4>
            <p className="text-lightGray text-sm">
              {selectedMetric.includes('overrun')
                ? "Focus on customer/part combinations with highest overruns."
                : selectedMetric.includes('ncr')
                  ? "Address quality issues in parts with repeated NCRs."
                  : "Optimize resource allocation across work centers."}
            </p>
          </div>
          
          <div className="bg-gray-50 p-4 rounded-lg">
            <h4 className="font-semibold mb-2">Recommended Actions</h4>
            <p className="text-lightGray text-sm">
              {selectedMetric.includes('overrun')
                ? "Review estimation methods for consistently overrun jobs."
                : selectedMetric.includes('ncr')
                  ? "Implement corrective actions for repeat failure modes."
                  : "Adjust planning parameters based on historical data."}
            </p>
          </div>
        </div>
      </Card>
    </div>
  );
};

export default MetricDetail;