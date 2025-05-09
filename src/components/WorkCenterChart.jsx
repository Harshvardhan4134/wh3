import React from 'react';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
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
  BarElement,
  Title,
  Tooltip,
  Legend
);

const WorkCenterChart = () => {
  const { workcenterData, formatNumber } = useData();
  
  if (!workcenterData || !workcenterData.work_center_data || workcenterData.work_center_data.length === 0) {
    return <div className="flex justify-center items-center h-64 text-lightGray">No work center data available</div>;
  }
  
  // Prepare data for the chart
  const labels = workcenterData.work_center_data.map(item => item.work_center);
  const plannedHours = workcenterData.work_center_data.map(item => item.planned_hours);
  const actualHours = workcenterData.work_center_data.map(item => item.actual_hours);
  const overrunHours = workcenterData.work_center_data.map(item => item.overrun_hours);
  
  const data = {
    labels,
    datasets: [
      {
        label: 'Planned Hours',
        data: plannedHours,
        backgroundColor: '#1E88E5',
        borderColor: '#1E88E5',
        borderWidth: 1,
      },
      {
        label: 'Actual Hours',
        data: actualHours,
        backgroundColor: '#e5383b',
        borderColor: '#e5383b',
        borderWidth: 1,
      },
      {
        label: 'Overrun Hours',
        data: overrunHours,
        backgroundColor: '#FFA000',
        borderColor: '#FFA000',
        borderWidth: 1,
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
            label += formatNumber(context.parsed.y, 0);
            return label;
          }
        }
      }
    },
    scales: {
      x: {
        ticks: {
          maxRotation: 0
        }
      },
      y: {
        beginAtZero: true,
        title: {
          display: true,
          text: 'Hours'
        }
      },
    },
  };
  
  return (
    <div className="h-72">
      <Bar data={data} options={options} />
    </div>
  );
};

export default WorkCenterChart;