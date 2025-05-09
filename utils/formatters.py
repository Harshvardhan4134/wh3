def format_money(value):
    """Format a value as currency."""
    return f"${value:,.0f}"

def format_number(value, digits=1):
    """Format a number with thousands separator and specified decimal places."""
    return f"{value:,.{digits}f}"

def format_percent(value):
    """Format a value as a percentage."""
    return f"{value:.1f}%"
