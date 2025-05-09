# Work History Dashboard - React Conversion Plan

## Project Structure
```
work-history-dashboard/
├── public/
│   ├── index.html
│   └── favicon.ico
├── src/
│   ├── components/
│   │   ├── Sidebar.jsx
│   │   ├── Header.jsx
│   │   ├── SummaryCards.jsx
│   │   ├── YearlySummaryTable.jsx
│   │   ├── YearlyTrendsChart.jsx
│   │   ├── CustomerProfitChart.jsx
│   │   ├── WorkCenterChart.jsx
│   │   └── DonutChart.jsx
│   ├── pages/
│   │   ├── Dashboard.jsx
│   │   ├── YearlyAnalysis.jsx
│   │   ├── MetricsDetail.jsx
│   │   └── UploadData.jsx
│   ├── utils/
│   │   ├── dataUtils.js
│   │   ├── formatters.js
│   │   └── api.js
│   ├── context/
│   │   └── DataContext.jsx
│   ├── styles/
│   │   ├── global.css
│   │   └── components.css
│   ├── App.jsx
│   ├── index.jsx
│   └── routes.jsx
└── package.json
```

## Technologies to Use
- React (with hooks and functional components)
- React Router for navigation
- Tailwind CSS for styling
- Recharts or Chart.js for visualization
- Axios for API calls (optional if using local data)

## Component Breakdown

### Sidebar
- Company logo and name at top
- Navigation menu with icons
- Active page indicator
- Logout button at bottom

### Header
- Page title
- Search bar
- User profile/settings

### Dashboard Page
- Summary metrics in cards with trend indicators
- Yearly summary table with links to yearly views
- Yearly trends chart
- Customer profitability section
- Work center performance section
- Hire vs. Cancel donut chart

### Yearly Analysis Page
- Year selector
- Key metrics for selected year
- Quarterly breakdown
- Top overruns
- NCR Summary
- Work center breakdown

### Metrics Detail Page
- Metric selector
- Trend chart for selected metric
- Correlation with other metrics
- Breakdown by customer
- Breakdown by work center

### Upload Data Page
- File upload component
- Upload status and history
- Data preview

## Design Guidelines
- Color scheme: Blue primary (#1E88E5), white background, light gray panels
- Dark sidebar with light text
- Card-based layout with consistent spacing
- Clear typography hierarchy
- Status indicators using colors (green for positive, red for negative)
- Consistent chart styling

## Data Handling
- Load data from JSON files initially
- Add API integration later if needed
- Maintain same metrics calculations as Streamlit version
- Use context API for global state management

## Implementation Phases
1. Project setup and scaffolding
2. Implement core UI components
3. Create dashboard page
4. Implement data utilities and formatters
5. Add charts and visualizations
6. Create additional pages
7. Add routing
8. Implement responsive design
9. Testing and refinement