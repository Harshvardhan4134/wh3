import pandas as pd
import numpy as np
from datetime import datetime
import os
import random

# In a real application, this would connect to a database
# For this demo, we'll generate sample data based on the patterns in the provided files

def generate_customer_data(customers, total_value):
    """Helper function to generate customer data with list_name support"""
    customer_data = []
    remaining_value = total_value
    
    for i, customer in enumerate(customers[:-1]):
        if i < len(customers) - 1:
            customer_ratio = random.uniform(0.05, 0.15)
            customer_value = total_value * customer_ratio
            remaining_value -= customer_value
        else:
            customer_value = remaining_value
        
        customer_data.append({
            "customer": customer["name"],
            "list_name": customer["list_name"],
            "value": customer_value,
            "percent_of_total": (customer_value / total_value) * 100
        })
    
    return customer_data

def load_yearly_summary():
    """Load yearly breakdown data."""
    # Sample data based on patterns from provided files
    data = [
        {"year": "2020", "planned_hours": 4523.5, "actual_hours": 4876.2, "overrun_hours": 352.7, "ncr_hours": 125.3, "job_count": 124, "operation_count": 723, "customer_count": 18},
        {"year": "2021", "planned_hours": 5218.8, "actual_hours": 5720.4, "overrun_hours": 501.6, "ncr_hours": 178.6, "job_count": 156, "operation_count": 892, "customer_count": 22},
        {"year": "2022", "planned_hours": 6245.3, "actual_hours": 6780.1, "overrun_hours": 534.8, "ncr_hours": 204.5, "job_count": 192, "operation_count": 1056, "customer_count": 26},
        {"year": "2023", "planned_hours": 7128.6, "actual_hours": 7865.9, "overrun_hours": 737.3, "ncr_hours": 245.8, "job_count": 215, "operation_count": 1225, "customer_count": 31},
        {"year": "2024", "planned_hours": 3568.2, "actual_hours": 3960.5, "overrun_hours": 392.3, "ncr_hours": 108.2, "job_count": 98, "operation_count": 542, "customer_count": 19}
    ]
    return data

def load_summary_metrics():
    """Load summary metrics for the dashboard."""
    # Calculate totals based on yearly data
    yearly_data = load_yearly_summary()
    
    total_planned_hours = sum(item["planned_hours"] for item in yearly_data)
    total_actual_hours = sum(item["actual_hours"] for item in yearly_data)
    total_overrun_hours = sum(item["overrun_hours"] for item in yearly_data)
    total_ncr_hours = sum(item["ncr_hours"] for item in yearly_data)
    total_jobs = sum(item["job_count"] for item in yearly_data)
    total_operations = sum(item["operation_count"] for item in yearly_data)
    total_customers = max(item["customer_count"] for item in yearly_data)  # Take max as customers may overlap years
    
    # Calculate costs (assuming $199/hour as mentioned in notes)
    hourly_rate = 199
    total_planned_cost = total_planned_hours * hourly_rate
    total_actual_cost = total_actual_hours * hourly_rate
    
    # Calculate overrun percent
    overrun_percent = (total_overrun_hours / total_planned_hours * 100) if total_planned_hours > 0 else 0
    
    return {
        "total_planned_hours": total_planned_hours,
        "total_actual_hours": total_actual_hours,
        "total_overrun_hours": total_overrun_hours,
        "total_ncr_hours": total_ncr_hours,
        "total_planned_cost": total_planned_cost,
        "total_actual_cost": total_actual_cost,
        "overrun_percent": overrun_percent,
        "total_jobs": total_jobs,
        "total_operations": total_operations,
        "total_customers": total_customers
    }

def load_customer_profitability():
    """Load customer profitability data."""
    # Sample customer data with list names
    top_customers = [
        {"name": "Aerospace Dynamics", "list_name": "Aerospace Dyn."},
        {"name": "Precision Manufacturing", "list_name": "Precision Mfg."},
        {"name": "Industrial Solutions", "list_name": "Ind. Solutions"},
        {"name": "TechFab Industries", "list_name": "TechFab Ind."},
        {"name": "Maritime Systems", "list_name": "Maritime Sys."},
        {"name": "Defense Components", "list_name": "Def. Components"},
        {"name": "Medical Devices Corp", "list_name": "Medical Dev."},
        {"name": "Energy Systems Inc", "list_name": "Energy Sys."},
        {"name": "Automotive Precision", "list_name": "Auto Precision"},
        {"name": "Electronics Assembly", "list_name": "Electronics"}
    ]
    
    # Generate profit data for top customers
    profit_data = []
    for customer in top_customers:
        planned_hours = random.uniform(200, 1200)
        actual_hours = planned_hours * random.uniform(0.9, 1.3)  # Some under, some over
        overrun_hours = max(0, actual_hours - planned_hours)
        profitability = random.uniform(-15, 25)  # Some negative, most positive
        
        profit_data.append({
            "customer": customer["name"],
            "list_name": customer["list_name"],
            "planned_hours": planned_hours,
            "actual_hours": actual_hours,
            "overrun_hours": overrun_hours,
            "profitability": profitability
        })
    
    # Sort by profitability for proper display
    profit_data = sorted(profit_data, key=lambda x: x["profitability"], reverse=True)
    
    # Get the most profitable customer
    top_customer_data = profit_data[0]
    
    # Get the customer with highest overrun
    overrun_customer_data = sorted(profit_data, key=lambda x: x["overrun_hours"], reverse=True)[0]
    
    return {
        "top_customer": top_customer_data["customer"],  # Most profitable customer name
        "top_customer_list_name": top_customer_data["list_name"],  # Most profitable customer short name
        "overrun_customer": overrun_customer_data["customer"],  # Highest overrun customer name
        "overrun_customer_list_name": overrun_customer_data["list_name"],  # Highest overrun customer short name
        "repeat_rate": 76.5,  # Percentage of repeat business
        "avg_margin": 12.8,   # Average profit margin percentage
        "profit_data": profit_data
    }

def load_workcenter_trends():
    """Load work center trend data."""
    # Sample work centers
    work_centers = [
        "Assembly", "Machining", "Welding", "Inspection", "Painting",
        "Testing", "Packaging", "CNC", "Quality Control", "Finishing"
    ]
    
    # Generate work center data
    work_center_data = []
    for wc in work_centers:
        planned_hours = random.uniform(300, 1800)
        actual_hours = planned_hours * random.uniform(0.9, 1.25)
        overrun_hours = max(0, actual_hours - planned_hours)
        
        work_center_data.append({
            "work_center": wc,
            "planned_hours": planned_hours,
            "actual_hours": actual_hours,
            "overrun_hours": overrun_hours
        })
    
    # Sort by actual hours for proper display
    work_center_data = sorted(work_center_data, key=lambda x: x["actual_hours"], reverse=True)
    
    # Find most used and highest overrun work centers
    most_used_wc = max(work_center_data, key=lambda x: x["actual_hours"])["work_center"]
    overrun_wc = max(work_center_data, key=lambda x: x["overrun_hours"])["work_center"]
    
    # Calculate total hours and average utilization
    total_hours = sum(wc["actual_hours"] for wc in work_center_data)
    avg_util = 78.5  # Sample utilization percentage
    
    return {
        "most_used_wc": most_used_wc,
        "overrun_wc": overrun_wc,
        "avg_util": avg_util,
        "total_wc_hours": total_hours,
        "work_center_data": work_center_data
    }

def load_year_data(year):
    """Load detailed data for a specific year."""
    # All yearly data
    yearly_data = load_yearly_summary()
    
    # Debug info
    print(f"Loading year data for {year}")
    print(f"Available years: {[item['year'] for item in yearly_data]}")
    
    # Find the specific year's data
    year_data = next((item for item in yearly_data if item["year"] == str(year)), None)
    
    # Debug info
    print(f"Found year data: {year_data is not None}")
    
    if not year_data:
        # If year not found, return empty data structure
        return {
            "summary": {
                "total_planned_hours": 0,
                "total_actual_hours": 0,
                "total_overrun_hours": 0,
                "ghost_hours": 0,
                "total_ncr_hours": 0,
                "total_planned_cost": 0,
                "total_actual_cost": 0,
                "opportunity_cost_dollars": 0,
                "recommended_buffer_percent": 0,
                "total_jobs": 0,
                "total_operations": 0,
                "total_unique_parts": 0
            },
            "quarterly_summary": [],
            "top_overruns": [],
            "ncr_summary": [],
            "workcenter_summary": [],
            "repeat_ncr_failures": [],
            "job_adjustments": []
        }
    
    # Calculate costs using $199/hour rate
    hourly_rate = 199
    planned_cost = year_data["planned_hours"] * hourly_rate
    actual_cost = year_data["actual_hours"] * hourly_rate
    opportunity_cost = year_data["overrun_hours"] * hourly_rate
    
    # Calculate recommended buffer based on overrun percentage
    overrun_percent = (year_data["overrun_hours"] / year_data["planned_hours"] * 100) if year_data["planned_hours"] > 0 else 0
    recommended_buffer = min(overrun_percent * 1.2, 30)  # Cap at 30%
    
    # Generate ghost hours (planned hours with no recorded work)
    ghost_hours = year_data["planned_hours"] * random.uniform(0.02, 0.08)
    
    # Calculate total unique parts (roughly 20-40% of operations)
    unique_parts = int(year_data["operation_count"] * random.uniform(0.2, 0.4))
    
    # Create quarterly summary
    quarters = ["Q1", "Q2", "Q3", "Q4"]
    quarterly_data = []
    
    total_planned = year_data["planned_hours"]
    total_actual = year_data["actual_hours"]
    total_overrun = year_data["overrun_hours"]
    total_jobs = year_data["job_count"]
    
    remaining_planned = total_planned
    remaining_actual = total_actual
    remaining_overrun = total_overrun
    remaining_jobs = total_jobs
    
    for i, quarter in enumerate(quarters):
        # For the first 3 quarters, allocate a portion of the yearly total
        if i < 3:
            quarter_ratio = random.uniform(0.15, 0.35)
            quarter_planned = total_planned * quarter_ratio
            quarter_actual = total_actual * quarter_ratio
            quarter_overrun = total_overrun * quarter_ratio
            quarter_jobs = int(total_jobs * quarter_ratio)
            
            remaining_planned -= quarter_planned
            remaining_actual -= quarter_actual
            remaining_overrun -= quarter_overrun
            remaining_jobs -= quarter_jobs
        else:
            # Last quarter gets the remainder
            quarter_planned = remaining_planned
            quarter_actual = remaining_actual
            quarter_overrun = remaining_overrun
            quarter_jobs = remaining_jobs
        
        quarterly_data.append({
            "quarter": quarter,
            "planned_hours": quarter_planned,
            "actual_hours": quarter_actual,
            "overrun_hours": quarter_overrun,
            "overrun_cost": quarter_overrun * hourly_rate,
            "total_jobs": quarter_jobs
        })
    
    # Generate top overruns
    top_overruns = []
    for i in range(15):  # Generate 15 top overruns
        job_number = f"J{year[-2:]}-{random.randint(1000, 9999)}"
        sales_document = f"5000{random.randint(100000, 999999)}"
        part_name = f"Part-{random.choice(['A', 'B', 'C', 'D', 'E'])}{random.randint(100, 999)}"
        description = f"{part_name} - {random.choice(['Assembly', 'Cast', 'Machined', 'Welded', 'Fabricated'])} {random.choice(['Component', 'Assembly', 'Housing', 'Manifold', 'Cylinder'])}"
        work_center = random.choice(["Assembly", "Machining", "Welding", "Inspection", "CNC", "Testing"])
        task_description = random.choice([
            "Final Assembly", "Surface Finishing", "Quality Inspection",
            "Component Machining", "Subassembly", "Heat Treatment",
            "Precision Grinding", "Dimensional Inspection"
        ])
        
        planned_hours = random.uniform(5, 60)
        actual_hours = planned_hours * random.uniform(1.2, 2.5)  # Significant overruns
        overrun_hours = actual_hours - planned_hours
        
        top_overruns.append({
            "job_number": job_number,
            "sales_document": sales_document,
            "part_name": part_name,
            "description": description,
            "work_center": work_center,
            "task_description": task_description,
            "planned_hours": planned_hours,
            "actual_hours": actual_hours,
            "overrun_hours": overrun_hours,
            "overrun_cost": overrun_hours * hourly_rate
        })
    
    # Sort overruns by cost (descending)
    top_overruns = sorted(top_overruns, key=lambda x: x["overrun_cost"], reverse=True)
    
    # Generate NCR summary
    ncr_summary = []
    for i in range(10):  # Generate 10 NCR instances
        part_name = f"Part-{random.choice(['N', 'M', 'K', 'L'])}{random.randint(100, 999)}"
        description = f"{part_name} - {random.choice(['Assembly', 'Cast', 'Machined', 'Welded', 'Fabricated'])} {random.choice(['Component', 'Assembly', 'Housing', 'Manifold', 'Cylinder'])}"
        
        total_ncr_hours = random.uniform(2, 30)
        ncr_occurrences = random.randint(1, 4)
        
        ncr_summary.append({
            "part_name": part_name,
            "description": description,
            "total_ncr_hours": total_ncr_hours,
            "total_ncr_cost": total_ncr_hours * hourly_rate,
            "ncr_occurrences": ncr_occurrences
        })
    
    # Sort NCR summary by cost (descending)
    ncr_summary = sorted(ncr_summary, key=lambda x: x["total_ncr_cost"], reverse=True)
    
    # Generate work center summary
    work_centers = ["Assembly", "Machining", "Welding", "Inspection", "Painting", "Testing", "CNC", "Quality Control"]
    workcenter_summary = []
    
    # Distribute total hours among work centers
    remaining_planned = year_data["planned_hours"]
    remaining_actual = year_data["actual_hours"]
    
    for i, wc in enumerate(work_centers):
        # For all but the last work center, allocate a portion of the total
        if i < len(work_centers) - 1:
            wc_ratio = random.uniform(0.05, 0.25)
            wc_planned = year_data["planned_hours"] * wc_ratio
            wc_actual = year_data["actual_hours"] * wc_ratio
            
            remaining_planned -= wc_planned
            remaining_actual -= wc_actual
        else:
            # Last work center gets the remainder
            wc_planned = remaining_planned
            wc_actual = remaining_actual
        
        wc_overrun = max(0, wc_actual - wc_planned)
        
        workcenter_summary.append({
            "work_center": wc,
            "planned_hours": wc_planned,
            "actual_hours": wc_actual,
            "overrun_hours": wc_overrun,
            "overrun_cost": wc_overrun * hourly_rate
        })
    
    # Sort work centers by overrun cost (descending)
    workcenter_summary = sorted(workcenter_summary, key=lambda x: x["overrun_cost"], reverse=True)
    
    # Generate repeat NCR failures
    repeat_ncr_failures = []
    for i in range(6):  # Generate 6 repeat NCR instances
        part_name = f"Part-{random.choice(['R', 'P', 'Q'])}{random.randint(100, 999)}"
        description = f"{part_name} - {random.choice(['Assembly', 'Cast', 'Machined', 'Welded', 'Fabricated'])} {random.choice(['Component', 'Assembly', 'Housing', 'Manifold', 'Cylinder'])}"
        
        repeat_ncr_hours = random.uniform(5, 20)
        ncr_job_count = random.randint(2, 4)
        
        repeat_ncr_failures.append({
            "part_name": part_name,
            "description": description,
            "repeat_ncr_hours": repeat_ncr_hours,
            "ncr_job_count": ncr_job_count
        })
    
    # Sort repeat NCRs by hours (descending)
    repeat_ncr_failures = sorted(repeat_ncr_failures, key=lambda x: x["repeat_ncr_hours"], reverse=True)
    
    # Generate job adjustments
    job_adjustments = []
    for i in range(12):  # Generate 12 job adjustment recommendations
        job_number = f"J{year[-2:]}-{random.randint(1000, 9999)}"
        
        planned_hours = random.uniform(20, 120)
        actual_hours = planned_hours * random.uniform(1.1, 1.5)
        adjustment_percent = ((actual_hours / planned_hours) - 1) * 100
        suggested_hours = planned_hours * (1 + adjustment_percent / 100)
        
        job_adjustments.append({
            "job_number": job_number,
            "planned_hours": planned_hours,
            "actual_hours": actual_hours,
            "suggested_hours": suggested_hours,
            "adjustment_percent": adjustment_percent
        })
    
    # Sort job adjustments by adjustment percentage (descending)
    job_adjustments = sorted(job_adjustments, key=lambda x: x["adjustment_percent"], reverse=True)
    
    # Generate part-level adjustments
    part_adjustments = []
    for i in range(8):  # Generate 8 part adjustment recommendations
        part_name = f"Part-{random.choice(['X', 'Y', 'Z'])}{random.randint(100, 999)}"
        
        avg_planned_hours = random.uniform(10, 50)
        avg_actual_hours = avg_planned_hours * random.uniform(1.1, 1.6)
        adjustment_percent = ((avg_actual_hours / avg_planned_hours) - 1) * 100
        suggested_hours = avg_planned_hours * (1 + adjustment_percent / 100)
        job_count = random.randint(2, 6)
        
        part_adjustments.append({
            "part_name": part_name,
            "avg_planned_hours": avg_planned_hours,
            "avg_actual_hours": avg_actual_hours,
            "suggested_hours": suggested_hours,
            "adjustment_percent": adjustment_percent,
            "job_count": job_count
        })
    
    # Sort part adjustments by adjustment percentage (descending)
    part_adjustments = sorted(part_adjustments, key=lambda x: x["adjustment_percent"], reverse=True)
    
    return {
        "summary": {
            "total_planned_hours": year_data["planned_hours"],
            "total_actual_hours": year_data["actual_hours"],
            "total_overrun_hours": year_data["overrun_hours"],
            "ghost_hours": ghost_hours,
            "total_ncr_hours": year_data["ncr_hours"],
            "total_planned_cost": planned_cost,
            "total_actual_cost": actual_cost,
            "opportunity_cost_dollars": opportunity_cost,
            "recommended_buffer_percent": recommended_buffer,
            "total_jobs": year_data["job_count"],
            "total_operations": year_data["operation_count"],
            "total_unique_parts": unique_parts
        },
        "quarterly_summary": quarterly_data,
        "top_overruns": top_overruns,
        "ncr_summary": ncr_summary,
        "workcenter_summary": workcenter_summary,
        "repeat_ncr_failures": repeat_ncr_failures,
        "job_adjustments": job_adjustments,
        "part_adjustments": part_adjustments,
        "avg_adjustment_percent": sum(job["adjustment_percent"] for job in job_adjustments) / len(job_adjustments) if job_adjustments else 0
    }

def load_metric_data(metric):
    """Load detailed data for a specific metric."""
    
    # Debug information
    print(f"Loading data for metric: {metric}")
    
    # Yearly breakdown data (used to derive yearly metric values)
    yearly_data = load_yearly_summary()
    
    if yearly_data is None or len(yearly_data) == 0:
        print("Warning: No yearly data available")
        return None
    
    # Sample customers with list names - IMPORTANT: This includes both full names and shortened list_names
    customers = [
        {"name": "Aerospace Dynamics", "list_name": "Aerospace Dyn."},
        {"name": "Precision Manufacturing", "list_name": "Precision Mfg."},
        {"name": "Industrial Solutions", "list_name": "Ind. Solutions"},
        {"name": "TechFab Industries", "list_name": "TechFab Ind."},
        {"name": "Maritime Systems", "list_name": "Maritime Sys."},
        {"name": "Defense Components", "list_name": "Def. Components"},
        {"name": "Medical Devices Corp", "list_name": "Medical Dev."},
        {"name": "Energy Systems Inc", "list_name": "Energy Sys."},
        {"name": "Automotive Precision", "list_name": "Auto Precision"},
        {"name": "Electronics Assembly", "list_name": "Electronics"},
        {"name": "Power Generation Ltd", "list_name": "Power Gen."},
        {"name": "Chemical Processing Inc", "list_name": "Chemical Proc."}
    ]
    
    # Sample work centers
    work_centers = [
        "Assembly", "Machining", "Welding", "Inspection", "Painting",
        "Testing", "Packaging", "CNC", "Quality Control", "Finishing",
        "Heat Treatment", "Plating"
    ]
    
    # Months
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    
    # Available metrics for correlation
    all_metrics = [
        "planned_hours", "actual_hours", "overrun_hours", "overrun_percent",
        "ncr_hours", "planned_cost", "actual_cost", "overrun_cost",
        "avg_cost_per_hour", "total_jobs", "total_operations", "total_customers"
    ]
    
    # Generate data based on selected metric
    if metric == "planned_hours":
        yearly_values = [float(item["planned_hours"]) for item in yearly_data]
        yearly_trend = [{"year": item["year"], "value": float(item["planned_hours"])} for item in yearly_data]
        
        # Generate customer data
        customer_data = []
        total_hours = sum(yearly_values)
        remaining_hours = total_hours
        
        for i, customer in enumerate(customers[:-1]):
            if i < len(customers) - 1:
                customer_ratio = random.uniform(0.05, 0.15)
                customer_hours = total_hours * customer_ratio
                remaining_hours -= customer_hours
            else:
                customer_hours = remaining_hours
            
            customer_data.append({
                "customer": customer,
                "value": customer_hours,
                "percent_of_total": (customer_hours / total_hours) * 100
            })
        
        # Generate work center data
        workcenter_data = []
        remaining_hours = total_hours
        
        for i, wc in enumerate(work_centers[:-1]):
            if i < len(work_centers) - 1:
                wc_ratio = random.uniform(0.05, 0.12)
                wc_hours = total_hours * wc_ratio
                remaining_hours -= wc_hours
            else:
                wc_hours = remaining_hours
            
            workcenter_data.append({
                "workcenter": wc,
                "value": wc_hours,
                "percent_of_total": (wc_hours / total_hours) * 100
            })
        
        # Generate monthly data
        monthly_data = []
        for month in months:
            monthly_data.append({
                "month": month,
                "value": total_hours / 12 * random.uniform(0.7, 1.3)
            })
        
        # Generate correlations
        correlations = []
        for corr_metric in all_metrics:
            if corr_metric != metric:
                strength = random.uniform(-1.0, 1.0)
                correlations.append({
                    "metric": corr_metric,
                    "correlation": strength,
                    "strength": "Strong positive" if strength > 0.7 else 
                                "Moderate positive" if strength > 0.3 else
                                "Weak positive" if strength > 0 else
                                "Strong negative" if strength < -0.7 else
                                "Moderate negative" if strength < -0.3 else
                                "Weak negative"
                })
        
        return {
            "summary": {
                "total": sum(yearly_values),
                "yearly_avg": sum(yearly_values) / len(yearly_values),
                "yoy_change": (yearly_values[-1] / yearly_values[-2] - 1) * 100 if len(yearly_values) > 1 else 0,
                "trend_direction": "Increasing" if yearly_values[-1] > yearly_values[0] else "Decreasing",
                "trend_strength": "Strong trend" if abs(yearly_values[-1] / yearly_values[0] - 1) > 0.3 else "Moderate trend"
            },
            "yearly_data": yearly_trend,
            "customer_data": customer_data,
            "workcenter_data": workcenter_data,
            "monthly_data": monthly_data,
            "correlations": correlations
        }
    
    elif metric == "actual_hours":
        yearly_values = [float(item["actual_hours"]) for item in yearly_data]
        yearly_trend = [{"year": item["year"], "value": float(item["actual_hours"])} for item in yearly_data]
        
        # Similar logic for other metrics...
        total_hours = sum(yearly_values)
        
        # Generate customer data
        customer_data = []
        remaining_hours = total_hours
        
        for i, customer in enumerate(customers[:-1]):
            if i < len(customers) - 1:
                customer_ratio = random.uniform(0.05, 0.15)
                customer_hours = total_hours * customer_ratio
                remaining_hours -= customer_hours
            else:
                customer_hours = remaining_hours
            
            customer_data.append({
                "customer": customer,
                "value": customer_hours,
                "percent_of_total": (customer_hours / total_hours) * 100
            })
        
        # Generate work center data
        workcenter_data = []
        remaining_hours = total_hours
        
        for i, wc in enumerate(work_centers[:-1]):
            if i < len(work_centers) - 1:
                wc_ratio = random.uniform(0.05, 0.12)
                wc_hours = total_hours * wc_ratio
                remaining_hours -= wc_hours
            else:
                wc_hours = remaining_hours
            
            workcenter_data.append({
                "workcenter": wc,
                "value": wc_hours,
                "percent_of_total": (wc_hours / total_hours) * 100
            })
        
        # Generate monthly data
        monthly_data = []
        for month in months:
            monthly_data.append({
                "month": month,
                "value": total_hours / 12 * random.uniform(0.7, 1.3)
            })
        
        # Generate correlations
        correlations = []
        for corr_metric in all_metrics:
            if corr_metric != metric:
                strength = random.uniform(-1.0, 1.0)
                correlations.append({
                    "metric": corr_metric,
                    "correlation": strength,
                    "strength": "Strong positive" if strength > 0.7 else 
                                "Moderate positive" if strength > 0.3 else
                                "Weak positive" if strength > 0 else
                                "Strong negative" if strength < -0.7 else
                                "Moderate negative" if strength < -0.3 else
                                "Weak negative"
                })
        
        return {
            "summary": {
                "total": sum(yearly_values),
                "yearly_avg": sum(yearly_values) / len(yearly_values),
                "yoy_change": (yearly_values[-1] / yearly_values[-2] - 1) * 100 if len(yearly_values) > 1 else 0,
                "trend_direction": "Increasing" if yearly_values[-1] > yearly_values[0] else "Decreasing",
                "trend_strength": "Strong trend" if abs(yearly_values[-1] / yearly_values[0] - 1) > 0.3 else "Moderate trend"
            },
            "yearly_data": yearly_trend,
            "customer_data": customer_data,
            "workcenter_data": workcenter_data,
            "monthly_data": monthly_data,
            "correlations": correlations
        }
    
    elif metric == "overrun_hours":
        yearly_values = [float(item["overrun_hours"]) for item in yearly_data]
        yearly_trend = [{"year": item["year"], "value": float(item["overrun_hours"])} for item in yearly_data]
        
        # Similar logic for other metrics...
        total_hours = sum(yearly_values)
        
        # Generate customer data
        customer_data = []
        remaining_hours = total_hours
        
        for i, customer in enumerate(customers[:-1]):
            if i < len(customers) - 1:
                customer_ratio = random.uniform(0.05, 0.15)
                customer_hours = total_hours * customer_ratio
                remaining_hours -= customer_hours
            else:
                customer_hours = remaining_hours
            
            customer_data.append({
                "customer": customer,
                "value": customer_hours,
                "percent_of_total": (customer_hours / total_hours) * 100
            })
        
        # Generate work center data
        workcenter_data = []
        remaining_hours = total_hours
        
        for i, wc in enumerate(work_centers[:-1]):
            if i < len(work_centers) - 1:
                wc_ratio = random.uniform(0.05, 0.12)
                wc_hours = total_hours * wc_ratio
                remaining_hours -= wc_hours
            else:
                wc_hours = remaining_hours
            
            workcenter_data.append({
                "workcenter": wc,
                "value": wc_hours,
                "percent_of_total": (wc_hours / total_hours) * 100
            })
        
        # Generate monthly data
        monthly_data = []
        for month in months:
            monthly_data.append({
                "month": month,
                "value": total_hours / 12 * random.uniform(0.7, 1.3)
            })
        
        # Generate correlations
        correlations = []
        for corr_metric in all_metrics:
            if corr_metric != metric:
                strength = random.uniform(-1.0, 1.0)
                correlations.append({
                    "metric": corr_metric,
                    "correlation": strength,
                    "strength": "Strong positive" if strength > 0.7 else 
                                "Moderate positive" if strength > 0.3 else
                                "Weak positive" if strength > 0 else
                                "Strong negative" if strength < -0.7 else
                                "Moderate negative" if strength < -0.3 else
                                "Weak negative"
                })
        
        return {
            "summary": {
                "total": sum(yearly_values),
                "yearly_avg": sum(yearly_values) / len(yearly_values),
                "yoy_change": (yearly_values[-1] / yearly_values[-2] - 1) * 100 if len(yearly_values) > 1 else 0,
                "trend_direction": "Increasing" if yearly_values[-1] > yearly_values[0] else "Decreasing",
                "trend_strength": "Strong trend" if abs(yearly_values[-1] / yearly_values[0] - 1) > 0.3 else "Moderate trend"
            },
            "yearly_data": yearly_trend,
            "customer_data": customer_data,
            "workcenter_data": workcenter_data,
            "monthly_data": monthly_data,
            "correlations": correlations
        }
    
    # For other metrics, follow a similar pattern with appropriate calculations
    # For example, for cost metrics, calculate using hourly rate
    
    # For demonstration, return generic structure for other metrics
    return {
        "summary": {
            "total": 0,
            "yearly_avg": 0,
            "yoy_change": 0,
            "trend_direction": "No data",
            "trend_strength": "No trend"
        },
        "yearly_data": [],
        "customer_data": [],
        "workcenter_data": [],
        "monthly_data": [],
        "correlations": []
    }
