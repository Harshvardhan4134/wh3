import React from 'react';
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
import { useData } from '../context/DataContext';

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

const YearlyTrendsChart = () => {
  const { yearlySummary, formatNumber } = useData();
  
  if (!yearlySummary || yearlySummary.length === 0) {
    return <div className="flex justify-center items-center h-64 text-lightGray">No data available</div>;
  }
  
  // Prepare data for the chart
  const labels = yearlySummary.map(item => item.year);
  const plannedHours = yearlySummary.map(item => item.planned_hours);
  const actualHours = yearlySummary.map(item => item.actual_hours);
  const overrunPercent = yearlySummary.map(item => 
    (item.actual_hours - item.planned_hours) / item.planned_hours * 100
  );
  
  const data = {
    labels,
    datasets: [
      {
        type: 'bar',
        label: 'Planned Hours',
        data: plannedHours,
        backgroundColor: '#1E88E5',
        borderColor: '#1E88E5',
        borderWidth: 1,
        yAxisID: 'y',
      },
      {
        type: 'bar',
        label: 'Actual Hours',
        data: actualHours,
        backgroundColor: '#e5383b',
        borderColor: '#e5383b',
        borderWidth: 1,
        yAxisID: 'y',
      },
      {
        type: 'line',
        label: 'Overrun %',
        data: overrunPercent,
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
  
  const options = {
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
              label += formatNumber(context.parsed.y, 1) + '%';
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
          text: 'Overrun %'
        },
        grid: {
          drawOnChartArea: false,
        },
      },
    },
  };
  
  return (
    <div className="h-72">
      <Bar data={data} options={options} />
    </div>
  );
};

export default YearlyTrendsChart;