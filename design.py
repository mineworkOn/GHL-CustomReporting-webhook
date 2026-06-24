import streamlit as st
import pandas as pd

def apply_custom_style():
    """Injects custom CSS to beautify the Streamlit dashboard"""
    
    custom_css = """
    <style>
        /* Style the metric cards */
        [data-testid="stMetric"] {
            background-color: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 10px;
            padding: 15px 20px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
            transition: transform 0.2s ease;
        }
        
        [data-testid="stMetric"]:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 8px -1px rgba(0, 0, 0, 0.1);
        }
        
        [data-testid="stMetricLabel"] {
            font-size: 14px !important;
            font-weight: 600 !important;
            color: #64748b !important;
            margin-bottom: 5px;
        }
        
        [data-testid="stMetricValue"] {
            font-size: 32px !important;
            font-weight: 700 !important;
            color: #0f172a !important;
        }
        
        /* Style the navigation tabs */
        .stTabs [data-baseweb="tab-list"] {
            gap: 10px;
            padding-bottom: 10px;
        }
        
        .stTabs [data-baseweb="tab"] {
            height: 45px;
            background-color: #f8fafc;
            border: 1px solid #e2e8f0;
            border-radius: 8px;
            padding: 0px 20px;
            color: #475569;
            font-weight: 500;
        }
        
        .stTabs [aria-selected="true"] {
            background-color: #eff6ff !important;
            border: 1px solid #3b82f6 !important;
            color: #1d4ed8 !important;
        }
        
        h1 {
            color: #0f172a;
            padding-bottom: 0.5rem;
            border-bottom: 2px solid #f1f5f9;
            margin-bottom: 2rem;
        }
        
        h3 {
            color: #334155;
            margin-top: 1.5rem;
            margin-bottom: 1rem;
        }
    </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)

def render_premium_html_table(df):
    """
    Converts a pandas DataFrame into a beautiful, SaaS-style HTML table.
    Smartly styles numbers and badges automatically.
    """
    html = """
    <style>
        .premium-table {
            width: 100%;
            border-collapse: collapse;
            margin: 15px 0;
            font-size: 14px;
            font-family: sans-serif;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
            border-radius: 8px;
            overflow: hidden;
        }
        .premium-table thead tr {
            background-color: #0f172a;
            color: #ffffff;
            text-align: left;
        }
        .premium-table th,
        .premium-table td {
            padding: 12px 20px;
        }
        .premium-table tbody tr {
            border-bottom: 1px solid #e2e8f0;
            background-color: #ffffff;
        }
        .premium-table tbody tr:nth-of-type(even) {
            background-color: #f8fafc;
        }
        .premium-table tbody tr:hover {
            background-color: #f1f5f9;
            transition: 0.2s ease;
        }
        .status-badge {
            background-color: #dcfce7;
            color: #166534;
            padding: 4px 10px;
            border-radius: 12px;
            font-size: 12px;
            font-weight: 600;
        }
        .number-highlight {
            font-weight: 700;
            color: #3b82f6;
        }
        .total-row {
            background-color: #eff6ff !important;
            font-weight: bold;
            border-top: 2px solid #cbd5e1;
        }
    </style>
    <div style="overflow-x: auto;">
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
        # Add a special class if this is the "Total leads" row in the pipeline
        row_class = ' class="total-row"' if row.get("Stage") == "Total leads" else ""
        html += f"<tr{row_class}>"
        
        for col in df.columns:
            val = row[col]
            
            # Smart Styling Logic
            if col == "AE Status" and val == "Active":
                html += f'<td><span class="status-badge">{val}</span></td>'
            # If the value is a number (and not a date string or name), make it blue and bold
            elif isinstance(val, (int, float)):
                html += f'<td class="number-highlight">{val}</td>'
            else:
                html += f"<td>{val}</td>"
        html += "</tr>"
        
    html += "</tbody></table></div>"
    
    return html