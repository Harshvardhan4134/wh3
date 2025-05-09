import React from 'react';
import { Link } from 'react-router-dom';
import { useData } from '../context/DataContext';

const YearlySummaryTable = () => {
  const { yearlySummary, formatNumber, formatMoney } = useData();
  
  if (!yearlySummary || yearlySummary.length === 0) {
    return <div className="flex justify-center items-center h-64 text-lightGray">No yearly data available</div>;
  }
  
  // Table headers
  const headers = [
    { label: 'Year', key: 'year' },
    { label: 'Planned', key: 'planned_hours', formatter: val => formatNumber(val) },
    { label: 'Actual', key: 'actual_hours', formatter: val => formatNumber(val) },
    { label: 'Overrun', key: 'overrun_hours', formatter: val => formatNumber(val) },
    { label: 'NCR', key: 'ncr_hours', formatter: val => formatNumber(val) },
    { label: 'Jobs', key: 'job_count', formatter: val => formatNumber(val, 0) },
    { label: 'Ops', key: 'operation_count', formatter: val => formatNumber(val, 0) },
    { label: 'Customers', key: 'customer_count', formatter: val => formatNumber(val, 0) }
  ];
  
  return (
    <div className="overflow-x-auto">
      <table className="min-w-full divide-y divide-gray-200">
        <thead>
          <tr>
            {headers.map((header, idx) => (
              <th
                key={idx}
                scope="col"
                className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
              >
                {header.label}
              </th>
            ))}
          </tr>
        </thead>
        <tbody className="bg-white divide-y divide-gray-200">
          {yearlySummary.map((row, rowIdx) => (
            <tr key={rowIdx} className="hover:bg-gray-50">
              {headers.map((header, colIdx) => (
                <td
                  key={colIdx}
                  className={`px-6 py-4 whitespace-nowrap text-sm ${
                    colIdx === 0 ? 'font-medium text-primary' : 'text-gray-500'
                  }`}
                >
                  {colIdx === 0 ? (
                    <Link to={`/yearly-analysis?year=${row[header.key]}`} className="text-primary hover:underline">
                      {row[header.key]}
                    </Link>
                  ) : (
                    header.formatter ? header.formatter(row[header.key]) : row[header.key]
                  )}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default YearlySummaryTable;