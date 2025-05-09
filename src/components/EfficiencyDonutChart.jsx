import React from 'react';
import {
  Chart as ChartJS,
  ArcElement,
  Tooltip,
  Legend
} from 'chart.js';
import { Doughnut } from 'react-chartjs-2';
import { useData } from '../context/DataContext';

// Register ChartJS components
ChartJS.register(
  ArcElement,
  Tooltip,
  Legend
);

const EfficiencyDonutChart = ({ plannedHours, actualHours }) => {
  const { formatPercent } = useData();
  
  if (!plannedHours || !actualHours) {
    return <div className="flex justify-center items-center h-64 text-lightGray">No data available</div>;
  }
  
  // Calculate values for chart
  const overrunHours = Math.max(0, actualHours - plannedHours);
  const underrunHours = Math.max(0, plannedHours - actualHours);
  const onTargetHours = plannedHours - overrunHours - underrunHours;
  
  const onTargetPercent = (onTargetHours / plannedHours) * 100;
  
  const data = {
    labels: ['On Target', 'Overrun', 'Underrun'],
    datasets: [
      {
        data: [onTargetHours, overrunHours, underrunHours],
        backgroundColor: [
          '#38b000',
          '#e5383b',
          '#FFA000',
        ],
        borderColor: [
          '#38b000',
          '#e5383b',
          '#FFA000',
        ],
        borderWidth: 1,
        hoverOffset: 4,
      },
    ],
  };
  
  const options = {
    responsive: true,
    maintainAspectRatio: false,
    cutout: '70%',
    plugins: {
      legend: {
        position: 'bottom',
        labels: {
          padding: 20,
        }
      },
      tooltip: {
        callbacks: {
          label: function(context) {
            const value = context.raw;
            const total = context.dataset.data.reduce((a, b) => a + b, 0);
            const percentage = (value / total) * 100;
            return `${context.label}: ${value.toFixed(0)} hours (${percentage.toFixed(1)}%)`;
          }
        }
      }
    },
  };
  
  const plugins = [
    {
      id: 'centerText',
      beforeDraw: function(chart) {
        const width = chart.width;
        const height = chart.height;
        const ctx = chart.ctx;

        ctx.restore();
        const fontSize = (height / 120).toFixed(2);
        ctx.font = `bold ${fontSize}em sans-serif`;
        ctx.textBaseline = "middle";
        
        const text = `${formatPercent(onTargetPercent/100).replace('%', '')}%`;
        const textX = Math.round((width - ctx.measureText(text).width) / 2);
        const textY = height / 2 - fontSize * 3;

        ctx.fillStyle = "#333";
        ctx.fillText(text, textX, textY);
        
        ctx.font = `${fontSize * 0.6}em sans-serif`;
        const subText = "On Target";
        const subTextX = Math.round((width - ctx.measureText(subText).width) / 2);
        const subTextY = height / 2;
        
        ctx.fillStyle = "#6c757d";
        ctx.fillText(subText, subTextX, subTextY);
        
        ctx.save();
      }
    }
  ];
  
  return (
    <div className="h-72 flex justify-center items-center">
      <Doughnut data={data} options={options} plugins={plugins} />
    </div>
  );
};

export default EfficiencyDonutChart;