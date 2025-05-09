import React from 'react';
import { useData } from '../context/DataContext';

const TopOverrunsTable = ({ data, limit = 5 }) => {
  const { formatNumber, formatPercent, formatMoney } = useData();
  
  if (!data || data.length === 0) {
    return <div className="flex justify-center items-center h-64 text-lightGray">No overrun data available</div>;
  }
  
  // Limit to specified number of entries
  const limitedData = data.slice(0, limit);
  
  return (
    <div className="space-y-2">
      {limitedData.map((job, index) => {
        const overrunPercent = (job.overrun_hours / job.planned_hours) * 100;
        
        return (
          <div 
            key={index}
            className="flex justify-between items-center p-3 border-b border-gray-100 hover:bg-gray-50 transition-colors"
          >
            <div>
              <div className="font-semibold">{job.job_number}</div>
              <div className="text-sm text-lightGray">{job.part_name}</div>
              <div className="text-xs text-gray-500 mt-1">{job.work_center}</div>
            </div>
            <div className="text-right">
              <div className="font-semibold text-error">{formatPercent(overrunPercent)}</div>
              <div className="text-sm text-lightGray">{formatNumber(job.overrun_hours)} hours</div>
              <div className="text-xs text-gray-500 mt-1">{formatMoney(job.overrun_cost)}</div>
            </div>
          </div>
        );
      })}
      
      {data.length > limit && (
        <div className="flex justify-center mt-4">
          <button className="text-primary font-semibold hover:underline">
            View All Overruns →
          </button>
        </div>
      )}
    </div>
  );
};

export default TopOverrunsTable;