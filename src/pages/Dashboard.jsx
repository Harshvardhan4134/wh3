import React from 'react';
import { Link } from 'react-router-dom';
import { useData } from '../context/DataContext';
import Card from '../components/Card';
import MetricCard from '../components/MetricCard';
import YearlyTrendsChart from '../components/YearlyTrendsChart';
import YearlySummaryTable from '../components/YearlySummaryTable';
import CustomerProfitChart from '../components/CustomerProfitChart';
import WorkCenterChart from '../components/WorkCenterChart';
import TopOverrunsTable from '../components/TopOverrunsTable';
import EfficiencyDonutChart from '../components/EfficiencyDonutChart';
import { Refresh as RefreshIcon, FilterList as FilterIcon } from '@mui/icons-material';

const Dashboard = () => {
  const { 
    summaryMetrics, 
    customerData, 
    workcenterData, 
    loading,
    formatNumber,
    formatMoney,
    formatPercent
  } = useData();
  
  if (loading.dashboard) {
    return (
      <div className="flex justify-center items-center h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-primary"></div>
      </div>
    );
  }
  
  if (!summaryMetrics) {
    return (
      <div className="flex flex-col justify-center items-center h-64 my-12">
        <div className="text-6xl mb-4">📊</div>
        <h2 className="text-2xl font-semibold mb-4">No data available</h2>
        <p className="text-lightGray mb-6">Please upload your work history data to get started with the dashboard.</p>
        <Link 
          to="/upload-data" 
          className="bg-primary text-white py-2 px-4 rounded font-medium hover:bg-opacity-90 transition-colors"
        >
          Upload Data
        </Link>
      </div>
    );
  }

  return (
    <div className="space-y-8 pb-8">
      {/* Summary Metrics Section */}
      <div>
        <div className="flex justify-between items-center mb-4">
          <h2>Summary Metrics</h2>
          <div className="flex items-center">
            <div className="bg-white rounded-md px-4 py-1.5 text-lightGray text-sm shadow-card mr-3">
              Last updated: {new Date().toLocaleDateString('en-US', { month: 'short', day: '2-digit', year: 'numeric', hour: '2-digit', minute: '2-digit' })}
            </div>
            <button className="bg-primary text-white px-4 py-1.5 rounded-md text-sm flex items-center shadow-card">
              <RefreshIcon fontSize="small" className="mr-1" />
              Refresh
            </button>
          </div>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-4">
          <MetricCard 
            title="Planned Hours" 
            value={formatNumber(summaryMetrics.total_planned_hours)} 
            icon="⏱️" 
          />
          <MetricCard 
            title="Actual Hours" 
            value={formatNumber(summaryMetrics.total_actual_hours)} 
            icon="⌛" 
          />
          <MetricCard 
            title="Overrun Hours" 
            value={formatNumber(summaryMetrics.total_overrun_hours)} 
            delta={formatPercent(summaryMetrics.overrun_percent/100)}
            icon="⚠️" 
            iconColor="#e5383b" 
          />
          <MetricCard 
            title="Ghost Hours" 
            value={formatNumber(summaryMetrics.total_ghost_hours)} 
            icon="👻" 
            iconColor="#6c757d"
            helpText="Planned time with no recorded work"
          />
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-4">
          <MetricCard 
            title="Unplanned Hours" 
            value={formatNumber(summaryMetrics.total_unplanned_hours)} 
            icon="❓" 
            iconColor="#ff9800"
            helpText="Actual time with no planning"
          />
          <MetricCard 
            title="Ghost Hours Cost" 
            value={formatMoney(summaryMetrics.total_ghost_hours_cost)} 
            icon="💰" 
            iconColor="#6c757d"
          />
          <MetricCard 
            title="Unplanned Hours Cost" 
            value={formatMoney(summaryMetrics.total_unplanned_hours_cost)} 
            icon="💵" 
            iconColor="#ff9800"
          />
          <MetricCard 
            title="Total NCR Hours" 
            value={formatNumber(summaryMetrics.total_ncr_hours)} 
            icon="⚙️" 
            iconColor="#FFA000" 
          />
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-4">
          <MetricCard 
            title="Scrap Cost" 
            value={formatMoney(summaryMetrics.total_ncr_costs.scrap)} 
            icon="🗑️" 
            iconColor="#d32f2f"
            helpText="Cost of scrapped parts"
          />
          <MetricCard 
            title="Rework Cost" 
            value={formatMoney(summaryMetrics.total_ncr_costs.rework)} 
            icon="🔄" 
            iconColor="#f57c00"
            helpText="Cost of rework operations"
          />
          <MetricCard 
            title="Repair Cost" 
            value={formatMoney(summaryMetrics.total_ncr_costs.repair)} 
            icon="🔧" 
            iconColor="#f57c00"
            helpText="Cost of repair operations"
          />
          <MetricCard 
            title="Other NCR Cost" 
            value={formatMoney(summaryMetrics.total_ncr_costs.other)} 
            icon="📝" 
            iconColor="#f57c00"
            helpText="Other NCR-related costs"
          />
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          <MetricCard 
            title="Planned Cost" 
            value={formatMoney(summaryMetrics.total_planned_cost)} 
            icon="💰" 
            iconColor="#2E7D32" 
          />
          <MetricCard 
            title="Actual Cost" 
            value={formatMoney(summaryMetrics.total_actual_cost)} 
            icon="💵" 
            iconColor="#2E7D32" 
          />
          <MetricCard 
            title="Total NCR Cost" 
            value={formatMoney(summaryMetrics.total_ncr_costs.total)} 
            icon="⚙️" 
            iconColor="#FFA000"
          />
          <MetricCard 
            title="Total Jobs" 
            value={formatNumber(summaryMetrics.total_jobs, 0)} 
            icon="🔧" 
          />
        </div>
      </div>
      
      {/* Yearly Breakdown Section */}
      <div>
        <div className="flex justify-between items-center mb-4">
          <h2>Yearly Breakdown</h2>
          <div className="bg-white px-4 py-2 rounded-lg shadow-card text-gray-700 cursor-pointer">
            All Years ▾
          </div>
        </div>
        
        <Card>
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <div>
              <h3 className="text-lg font-semibold mb-4">Year Summary</h3>
              <YearlySummaryTable />
            </div>
            <div>
              <h3 className="text-lg font-semibold mb-4">Yearly Trends</h3>
              <YearlyTrendsChart />
            </div>
          </div>
        </Card>
      </div>
      
      {/* Customer & Work Center Analysis Side by Side */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Customer Profit Analysis */}
        <div>
          <div className="flex justify-between items-center mb-4">
            <h2>Customer Profit Analysis</h2>
            <div className="bg-white px-4 py-2 rounded-lg shadow-card text-gray-700 cursor-pointer flex items-center">
              <FilterIcon fontSize="small" className="mr-1" />
              Filter
            </div>
          </div>
          
          <Card>
            <div className="grid grid-cols-2 gap-4 mb-6">
              {customerData && (
                <>
                  <div className="p-4 rounded-lg bg-success bg-opacity-10">
                    <div className="text-lightGray text-sm">Most Profitable</div>
                    <div className="font-semibold text-lg mt-1">
                      <span className="text-success mr-1">▲</span>
                      {customerData.top_customer_list_name}
                    </div>
                  </div>
                  
                  <div className="p-4 rounded-lg bg-error bg-opacity-10">
                    <div className="text-lightGray text-sm">Highest Overrun</div>
                    <div className="font-semibold text-lg mt-1">
                      <span className="text-error mr-1">▼</span>
                      {customerData.overrun_customer_list_name}
                    </div>
                  </div>
                </>
              )}
            </div>
            
            <div className="grid grid-cols-2 gap-4 mb-6">
              {customerData && (
                <>
                  <div className="p-4 rounded-lg bg-primary bg-opacity-10">
                    <div className="text-lightGray text-sm">Repeat Business</div>
                    <div className="font-semibold text-lg mt-1">
                      {formatPercent(customerData.repeat_rate)}
                    </div>
                  </div>
                  
                  <div className="p-4 rounded-lg bg-primary bg-opacity-10">
                    <div className="text-lightGray text-sm">Avg Profit Margin</div>
                    <div className="font-semibold text-lg mt-1">
                      {formatPercent(customerData.avg_margin)}
                    </div>
                  </div>
                </>
              )}
            </div>
            
            <h3 className="text-lg font-semibold mb-4">Customer Profitability vs Hours</h3>
            <CustomerProfitChart />
          </Card>
        </div>
        
        {/* Work Center Analysis */}
        <div>
          <div className="flex justify-between items-center mb-4">
            <h2>Work Center Analysis</h2>
            <div className="bg-white px-4 py-2 rounded-lg shadow-card text-gray-700 cursor-pointer flex items-center">
              <FilterIcon fontSize="small" className="mr-1" />
              Filter
            </div>
          </div>
          
          <Card>
            <div className="grid grid-cols-2 gap-4 mb-6">
              {workcenterData && (
                <>
                  <div className="p-4 rounded-lg bg-primary bg-opacity-10">
                    <div className="text-lightGray text-sm">Most Used</div>
                    <div className="font-semibold text-lg mt-1">
                      {workcenterData.most_used_wc}
                    </div>
                  </div>
                  
                  <div className="p-4 rounded-lg bg-primary bg-opacity-10">
                    <div className="text-lightGray text-sm">Highest Overrun</div>
                    <div className="font-semibold text-lg mt-1">
                      {workcenterData.overrun_wc}
                    </div>
                  </div>
                </>
              )}
            </div>
            
            <div className="grid grid-cols-2 gap-4 mb-6">
              {workcenterData && (
                <>
                  <div className="p-4 rounded-lg bg-primary bg-opacity-10">
                    <div className="text-lightGray text-sm">Avg Utilization</div>
                    <div className="font-semibold text-lg mt-1">
                      {formatPercent(workcenterData.avg_util)}
                    </div>
                  </div>
                  
                  <div className="p-4 rounded-lg bg-primary bg-opacity-10">
                    <div className="text-lightGray text-sm">Total WC Hours</div>
                    <div className="font-semibold text-lg mt-1">
                      {formatNumber(workcenterData.total_wc_hours)}
                    </div>
                  </div>
                </>
              )}
            </div>
            
            <h3 className="text-lg font-semibold mb-4">Work Center Performance</h3>
            <WorkCenterChart />
          </Card>
        </div>
      </div>
      
      {/* Efficiency Section */}
      <div>
        <div className="flex justify-between items-center mb-4">
          <h2>Efficiency Breakdown</h2>
          <div className="bg-white px-4 py-2 rounded-lg shadow-card text-gray-700 cursor-pointer">
            Export ▾
          </div>
        </div>
        
        <Card>
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            <div>
              <EfficiencyDonutChart
                plannedHours={summaryMetrics.total_planned_hours}
                actualHours={summaryMetrics.total_actual_hours}
              />
            </div>
            
            <div className="lg:col-span-2">
              <h3 className="text-lg font-semibold mb-4">Top Overrun Jobs</h3>
              {summaryMetrics && (
                <TopOverrunsTable
                  data={[
                    {
                      job_number: "J22-482",
                      part_name: "Hydraulic Cylinder",
                      work_center: "ASSEMBLY",
                      planned_hours: 45,
                      actual_hours: 62,
                      overrun_hours: 17,
                      overrun_cost: 3383
                    },
                    {
                      job_number: "J22-398",
                      part_name: "Turbine Housing",
                      work_center: "MILLING",
                      planned_hours: 38,
                      actual_hours: 52,
                      overrun_hours: 14,
                      overrun_cost: 2786
                    },
                    {
                      job_number: "J22-512",
                      part_name: "Control Manifold",
                      work_center: "MILLING",
                      planned_hours: 42,
                      actual_hours: 54,
                      overrun_hours: 12,
                      overrun_cost: 2388
                    },
                    {
                      job_number: "J22-604",
                      part_name: "Bearing Housing",
                      work_center: "LATHE",
                      planned_hours: 36,
                      actual_hours: 46,
                      overrun_hours: 10,
                      overrun_cost: 1990
                    },
                    {
                      job_number: "J22-423",
                      part_name: "Flow Control Valve",
                      work_center: "ASSEMBLY",
                      planned_hours: 28,
                      actual_hours: 36,
                      overrun_hours: 8,
                      overrun_cost: 1592
                    }
                  ]}
                  limit={5}
                />
              )}
            </div>
          </div>
        </Card>
      </div>
      
      {/* Calculation Notes */}
      <div className="border-t border-gray-200 pt-6">
        <details className="bg-white rounded-lg shadow-card overflow-hidden">
          <summary className="px-4 py-3 cursor-pointer font-medium text-gray-700 hover:bg-gray-50">
            Calculation Notes
          </summary>
          <div className="p-4 bg-gray-50 border-t border-gray-100">
            <ul className="space-y-2 pl-6 list-disc text-lightGray">
              <li><b>Planned/Actual Cost:</b> <code>Hours × $199/hour</code></li>
              <li><b>Overrun Hours:</b> When <code>Actual &gt; Planned</code></li>
              <li><b>NCR Hours:</b> Total hours for <code>NCR</code> work center operations</li>
              <li><b>On Target:</b> Work completed on or under budget</li>
              <li><b>Underrun:</b> Work completed under the planned hours</li>
            </ul>
          </div>
        </details>
      </div>
      
      {/* Footer */}
      <div className="text-center text-xs text-lightGray border-t border-gray-200 pt-6">
        Last data refresh: {new Date().toLocaleDateString('en-US', { month: 'short', day: '2-digit', year: 'numeric', hour: '2-digit', minute: '2-digit' })} | <span className="text-primary cursor-pointer">Contact Support</span>
      </div>
    </div>
  );
};

export default Dashboard;