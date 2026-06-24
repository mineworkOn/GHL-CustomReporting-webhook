import streamlit as st
import pandas as pd

def apply_custom_style():
    """Injects custom CSS to beautify the Streamlit dashboard for both Light and Dark mode"""
    
    custom_css = """
    <style>
        /* Style the metric cards using native theme variables */
        [data-testid="stMetric"] {
            background-color: var(--secondary-background-color);
            border: 1px solid rgba(128, 128, 128, 0.2);
            border-radius: 10px;
            padding: 15px 20px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
            transition: transform 0.2s ease;
        }
        
        [data-testid="stMetric"]:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 8px -1px rgba(0, 0, 0, 0.2);
        }
        
        [data-testid="stMetricLabel"] {
            font-size: 14px !important;
            font-weight: 600 !important;
            color: var(--text-color) !important;
            opacity: 0.7;
            margin-bottom: 5px;
        }
        
        [data-testid="stMetricValue"] {
            font-size: 32px !important;
            font-weight: 700 !important;
            color: var(--text-color) !important;
        }
        
        /* Clean up standard typography */
        h1 {
            padding-bottom: 0.5rem;
            border-bottom: 2px solid var(--secondary-background-color);
            margin-bottom: 2rem;
        }
    </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)

def render_premium_html_table(df):
    """
    Converts a pandas DataFrame into a beautiful HTML table that adapts to Dark/Light mode.
    Optimized to fit wide tables (15+ columns) seamlessly on desktop.
    """
    html = """
    <style>
        /* Responsive wrapper ensures it scrolls on mobile but fits on desktop */
        .table-responsive-wrapper {
            width: 100%;
            overflow-x: auto;
            -webkit-overflow-scrolling: touch;
            margin: 15px 0;
            border-radius: 8px;
            border: 1px solid rgba(128, 128, 128, 0.2);
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }
        
        .premium-table {
            width: 100%;
            border-collapse: collapse;
            font-size: 13px; /* Slightly smaller font to fit more columns */
            font-family: sans-serif;
            color: var(--text-color);
            background-color: var(--background-color);
        }
        
        /* Adaptive header */
        .premium-table thead tr {
            background-color: var(--secondary-background-color);
            color: var(--text-color);
            border-bottom: 2px solid rgba(128, 128, 128, 0.3);
        }
        
        /* Tighter padding to fit 15 columns on a single screen */
        .premium-table th,
        .premium-table td {
            padding: 8px 10px; /* Reduced from 12px 20px */
            border: 1px solid rgba(128, 128, 128, 0.2);
            text-align: center; /* Center alignment saves horizontal space */
            vertical-align: middle;
        }
        
        /* Keep the first column (Date/Name) left-aligned for readability */
        .premium-table th:first-child,
        .premium-table td:first-child {
            text-align: left;
            font-weight: 600;
            white-space: nowrap; /* Prevents dates from stacking awkwardly */
        }
        
        /* Base row color */
        .premium-table tbody tr {
            background-color: var(--background-color);
        }
        
        /* Alternating row colors using transparency */
        .premium-table tbody tr:nth-of-type(even) {
            background-color: rgba(128, 128, 128, 0.05);
        }
        
        /* Hover effect */
        .premium-table tbody tr:hover {
            background-color: rgba(128, 128, 128, 0.1);
            transition: 0.2s ease;
        }
        
        /* Badges and Highlights */
        .status-badge {
            background-color: #059669; 
            color: white;
            padding: 4px 10px;
            border-radius: 12px;
            font-size: 11px;
            font-weight: 600;
            white-space: nowrap;
        }
        .number-highlight {
            font-weight: 700;
            color: #3b82f6; 
        }
        .total-row {
            background-color: rgba(59, 130, 246, 0.1) !important;
            font-weight: bold;
        }
        .total-row td {
            border-top: 2px solid rgba(128, 128, 128, 0.4);
        }
    </style>
    <div class="table-responsive-wrapper">
        <table class="premium-table">
            <thead>
                <tr>
    """
    
    # 1. Generate Table Headers
    for col in df.columns:
        html += f"<th>{col}</th>"
    html += "</tr></thead><tbody>"
    
    # 2. Generate Table Rows dynamically
    for index, row in df.iterrows():
        is_total = (row.get("Stage") == "Total leads") or (row.get("AE Name") == "Total")
        row_class = ' class="total-row"' if is_total else ""
        html += f"<tr{row_class}>"
        
        for col in df.columns:
            val = row[col]
            
            # Smart Styling Logic
            if col == "AE Status" and val == "Active":
                html += f'<td><span class="status-badge">{val}</span></td>'
            elif isinstance(val, (int, float)):
                html += f'<td class="number-highlight">{val}</td>'
            else:
                html += f"<td>{val}</td>"
        html += "</tr>"
        
    html += "</tbody></table></div>"
    
    return html