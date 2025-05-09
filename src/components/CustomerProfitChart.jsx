import React from 'react';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  PointElement,
  LineElement,
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
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

const CustomerProfitChart = () => {
  const { customerData, formatNumber, formatPercent } = useData();
  
  if (!customerData || !customerData.profit_data || customerData.profit_data.length === 0) {
    return <div className="flex justify-center items-center h-64 text-lightGray">No customer data available</div>;
  }
  
  // Limit to top 5 customers if there are more
  const chartData = customerData.profit_data.slice(0, 5);
  
  // Prepare data for the chart
  const labels = chartData.map(item => item.customer);
  const plannedHours = chartData.map(item => item.planned_hours);
  const actualHours = chartData.map(item => item.actual_hours);
  const profitMargins = chartData.map(item => item.profit_margin);
  
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
        backgroundColor: '#6c757d',
        borderColor: '#6c757d',
        borderWidth: 1,
        yAxisID: 'y',
      },
      {
        type: 'line',
        label: 'Profit Margin %',
        data: profitMargins,
        borderColor: '#38b000',
        backgroundColor: '#38b000',
        borderWidth: 2,
        yAxisID: 'y1',
        pointBackgroundColor: '#38b000',
        pointBorderColor: '#38b000',
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
              label += formatPercent(context.parsed.y);
            } else {
              label += formatNumber(context.parsed.y, 0);
            }
            return label;
          }
        }
      }
    },
    scales: {
      x: {
        ticks: {
          maxRotation: 45,
          minRotation: 45
        }
      },
      y: {
        type: 'linear',
        display: true,
        position: 'left',
        title: {
          display: true,
          text: 'Hours'
        },
        beginAtZero: true
      },
      y1: {
        type: 'linear',
        display: true,
        position: 'right',
        title: {
          display: true,
          text: 'Profit Margin %'
        },
        beginAtZero: true,
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

export default CustomerProfitChart;