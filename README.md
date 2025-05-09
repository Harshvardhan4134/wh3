# Work History Dashboard

An executive analysis of shop performance with focus on cost, labor efficiency, and process breakdowns.

## Features

- Summary metrics showing planned vs. actual hours and costs
- Yearly breakdown of performance metrics
- Customer profit analysis 
- Work center performance analysis
- Detailed yearly analysis views
- Data upload functionality

## Screenshots

![Dashboard overview](https://github.com/yourusername/work-history-dashboard/raw/main/screenshots/dashboard.png)

## Setup Instructions

1. Clone this repository
2. Install dependencies: `pip install -r dependencies.txt`
3. Run the app: `streamlit run app.py`

## Data Format

The dashboard expects an Excel file with work history data containing the following columns:
- operation_finish_date - Date when operation was completed
- job_number - Unique identifier for a job
- part_name - Name of the part being worked on
- customer_name - Name of the customer
- work_center - Department or machine where work was performed
- planned_hours - Estimated hours for the job
- actual_hours - Actual hours spent on the job

## Project Structure

- `app.py` - Main dashboard file
- `pages/` - Additional dashboard pages
  - `1_Yearly_Analysis.py` - Detailed yearly breakdown
  - `2_Metrics_Detail.py` - Specific metric analysis
  - `3_Upload_Data.py` - Data upload interface
- `utils/` - Utility functions
  - `data_utils.py` - Data processing functions
  - `formatters.py` - Number and text formatting
  - `visualization.py` - Chart creation
- `attached_assets/` - Example data file

## Dashboard Pages

### Main Dashboard
Shows summary metrics, yearly breakdown, customer profit analysis, and work center performance.

### Yearly Analysis
Allows selecting a specific year to see detailed metrics, quarterly breakdowns, and overrun analysis.

### Metrics Detail
Shows trends and correlations for a specific metric.

### Upload Data
Interface for uploading new work history data.