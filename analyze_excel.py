import pandas as pd
import re
from datetime import datetime

# Read the Excel file
file_path = 'attached_assets/WORKHISTORY.xlsx'
df = pd.read_excel(file_path)

# Show basic info
print(f"Total records: {len(df)}")
print(f"Columns: {df.columns.tolist()}")

# Extract years from job numbers
job_years = []
for job in df['job_number']:
    match = re.search(r'JOB-(\d{4})-', str(job))
    if match:
        job_years.append(match.group(1))

print(f"Years from job numbers: {sorted(set(job_years))}")

# Extract years from operation finish dates
op_years = sorted(df['operation_finish_date'].dt.year.unique().tolist())
print(f"Years from operation dates: {op_years}")

# Get unique customers
customers = df['customer_name'].unique().tolist()
print(f"Unique customers ({len(customers)}): {customers}")

# Get unique work centers
work_centers = df['work_center'].unique().tolist()
print(f"Unique work centers ({len(work_centers)}): {work_centers}")

# Calculate total hours by year
print("\nHours by year:")
yearly_data = []
for year in set(df['operation_finish_date'].dt.year):
    year_df = df[df['operation_finish_date'].dt.year == year]
    planned_hours = year_df['planned_hours'].sum()
    actual_hours = year_df['actual_hours'].sum()
    overrun_hours = actual_hours - planned_hours
    job_count = len(year_df['job_number'].unique())
    
    print(f"Year {year}: Planned: {planned_hours:.1f}, Actual: {actual_hours:.1f}, Overrun: {overrun_hours:.1f}, Jobs: {job_count}")
    
    yearly_data.append({
        "year": str(year),
        "planned_hours": planned_hours,
        "actual_hours": actual_hours,
        "overrun_hours": overrun_hours,
        "job_count": job_count
    })

# Sample a few rows
print("\nSample rows:")
print(df.head(3))