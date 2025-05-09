import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import os
import io

# Page configuration
st.set_page_config(
    page_title="Upload Work History Data",
    page_icon="📤",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Constants for column mapping
COLUMN_MAPPING = {
    'sales document': 'job_number',
    'order': 'work_order_number',
    'oper./act.': 'operation_number',
    'oper.workcenter': 'work_center',
    'description': 'part_name',
    'opr. short text': 'task_description',
    'work': 'planned_hours',
    'actual work': 'actual_hours',
    'list name': 'customer_name',
    'basic fin. date': 'operation_finish_date'
}

# Fields that need to be derived/calculated
CALCULATED_FIELDS = [
    'remaining_work',
    'status',
    'operation_start_date',
    'job_start_date'
]

# Title and description
st.title("📤 Upload Work History Data")
st.markdown("""
Upload your work history Excel file to analyze performance metrics. The file should contain operation-level data 
including planned hours, actual hours, work centers, and customers.

**Required columns:**
- Sales Document (Job Number)
- Order (Work Order Number)
- Oper./Act. (Operation Number)
- Oper.Workcenter
- Description (Part Name)
- Opr. Short Text (Task Description)
- Work (Planned Hours)
- Actual Work (Actual Hours)
- List Name (Customer Name)
- Basic Fin. Date (Operation Finish Date)
""")

# Function to process and validate uploaded work history data
def process_workhistory(uploaded_file):
    try:
        # Make sure to clear the cache when new data is uploaded
        st.cache_data.clear()
        
        # Read Excel file
        df = pd.read_excel(uploaded_file, sheet_name="Sheet1", dtype=str)
        
        # Standardize column names
        df.columns = df.columns.str.lower().str.strip()
        
        # Check required columns
        required_columns = list(COLUMN_MAPPING.keys())
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            return False, f"Missing required columns: {', '.join(missing_columns)}"
        
        # Rename columns to standard names
        df.rename(columns=COLUMN_MAPPING, inplace=True)
        
        # Add calculated fields if they don't exist
        for field in CALCULATED_FIELDS:
            if field not in df.columns:
                df[field] = None
        
        # Convert date fields
        if 'operation_finish_date' in df.columns:
            # First try to convert to datetime directly
            df['operation_finish_date'] = pd.to_datetime(df['operation_finish_date'], errors='coerce')
            
            # If that fails, try to parse common date formats
            if df['operation_finish_date'].isna().any():
                # Try different date formats
                date_formats = ['%m/%d/%Y', '%Y-%m-%d', '%d/%m/%Y', '%m-%d-%Y']
                for date_format in date_formats:
                    mask = df['operation_finish_date'].isna()
                    if mask.any():
                        df.loc[mask, 'operation_finish_date'] = pd.to_datetime(
                            df.loc[mask, 'operation_finish_date'], 
                            format=date_format, 
                            errors='coerce'
                        )
        
        # Convert numeric fields
        numeric_columns = ["planned_hours", "actual_hours", "operation_number"]
        for col in numeric_columns:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0).astype(float)
        
        # Clean text fields
        text_columns = ["job_number", "work_order_number", "work_center", "part_name", "task_description", "customer_name"]
        for col in text_columns:
            df[col] = df[col].fillna("N/A").astype(str).str.strip()
        
        # Set record date
        df["recorded_date"] = datetime.now().date()
        
        # Remove duplicates
        df.drop_duplicates(subset=['job_number', 'work_order_number', 'operation_number'], inplace=True)
        
        # Replace NaN values
        df = df.where(pd.notnull(df), None)
        
        # Calculate derived metrics
        df["overrun_hours"] = np.maximum(df["actual_hours"] - df["planned_hours"], 0)
        
        # Save processed data to session state
        st.session_state.processed_data = df
        
        return True, f"Successfully processed {len(df)} records."
        
    except Exception as e:
        return False, f"Error processing file: {str(e)}"

# File upload section
uploaded_file = st.file_uploader("Upload Work History Excel File", type=["xlsx"])

if uploaded_file is not None:
    # Process button
    if st.button("Process Data"):
        with st.spinner("Processing data..."):
            success, message = process_workhistory(uploaded_file)
            
            if success:
                st.success(message)
                
                # Display preview of processed data
                st.subheader("Preview of Processed Data")
                st.dataframe(st.session_state.processed_data.head(10), use_container_width=True)
                
                # Display summary statistics
                if "processed_data" in st.session_state:
                    df = st.session_state.processed_data
                    
                    st.subheader("Summary Statistics")
                    
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        st.metric("Total Records", format(len(df), ","))
                    
                    with col2:
                        st.metric("Total Jobs", format(df['job_number'].nunique(), ","))
                    
                    with col3:
                        st.metric("Total Work Centers", format(df['work_center'].nunique(), ","))
                    
                    with col4:
                        st.metric("Total Customers", format(df['customer_name'].nunique(), ","))
                    
                    # Date range
                    date_col1, date_col2 = st.columns(2)
                    with date_col1:
                        min_date = pd.to_datetime(df['operation_finish_date'], errors='coerce').min()
                        if pd.notna(min_date):
                            st.metric("Earliest Operation Date", min_date.strftime('%Y-%m-%d'))
                        else:
                            st.metric("Earliest Operation Date", "N/A")
                    
                    with date_col2:
                        max_date = pd.to_datetime(df['operation_finish_date'], errors='coerce').max()
                        if pd.notna(max_date):
                            st.metric("Latest Operation Date", max_date.strftime('%Y-%m-%d'))
                        else:
                            st.metric("Latest Operation Date", "N/A")
                    
                    # Hours and overruns
                    st.subheader("Hours Analysis")
                    
                    hours_col1, hours_col2, hours_col3, hours_col4 = st.columns(4)
                    
                    with hours_col1:
                        total_planned = df['planned_hours'].sum()
                        st.metric("Total Planned Hours", f"{total_planned:,.1f}")
                    
                    with hours_col2:
                        total_actual = df['actual_hours'].sum()
                        st.metric("Total Actual Hours", f"{total_actual:,.1f}")
                    
                    with hours_col3:
                        total_overrun = df['overrun_hours'].sum()
                        st.metric("Total Overrun Hours", f"{total_overrun:,.1f}")
                    
                    with hours_col4:
                        if total_planned > 0:
                            overrun_percent = (total_overrun / total_planned) * 100
                            st.metric("Overrun Percentage", f"{overrun_percent:.1f}%")
                        else:
                            st.metric("Overrun Percentage", "N/A")
                    
                    # Download processed data button
                    output = io.BytesIO()
                    with pd.ExcelWriter(output, engine='openpyxl') as writer:
                        df.to_excel(writer, sheet_name='Processed_Data', index=False)
                    
                    output.seek(0)
                    
                    st.download_button(
                        label="Download Processed Data",
                        data=output,
                        file_name="processed_work_history.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
                    
                    # Continue to dashboard button
                    st.button("Continue to Dashboard", on_click=lambda: st.switch_page("app.py"))
            else:
                st.error(message)

# Display help information
with st.expander("Need Help?"):
    st.markdown("""
    ### File Format Requirements
    
    Your Excel file should:
    1. Have a sheet named "Sheet1"
    2. Include all required columns (they can be in any order)
    3. Have clean data (minimal missing values)
    
    ### Common Issues
    
    - **Missing Columns**: Ensure all required columns are present in the file
    - **Date Format**: Make sure dates are in a recognizable format
    - **Number Format**: Hours should be numeric values
    - **Duplicates**: The system will remove duplicate entries based on job, work order, and operation numbers
    
    ### What Happens Next?
    
    After processing, the data will be available for analysis in the dashboard. You can:
    1. View overall metrics on the main dashboard
    2. Analyze yearly performance in the Yearly Analysis page
    3. Explore specific metrics in the Metrics Detail page
    """)
