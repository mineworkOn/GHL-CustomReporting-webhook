import streamlit as st
import pandas as pd

def apply_custom_style():
    """Injects custom CSS to beautify the Streamlit dashboard for both Light and Dark mode"""
    
    custom_css = """
    <style>
        /* 1. SURGICAL HEADER DESIGN (Icon-Safe) */
        /* Clean up structural constraints on the root header block */
        h1 {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
            font-weight: 800 !important;
            letter-spacing: -0.03em !important;
            padding-left: 14px;
            margin-top: 1rem !important;
            margin-bottom: 2rem !important;
            border-left: 5px solid #3b82f6; 
            border-radius: 2px;
            
            /* RESET parent text clip modifiers so emojis don't break */
            -webkit-background-clip: initial !important;
            -webkit-text-fill-color: initial !important;
            background-clip: initial !important;
            color: var(--text-color) !important;
        }
        
        /* TARGET ONLY THE INNER TEXT STRING INSIDE THE HEADER FOR THE GRADIENT EFFECT */
        h1 [data-testid="stHeaderBlockContent"],
        h1 span:not(:has(img)) {
            background: linear-gradient(135deg, #1e293b 30%, #3b82f6 100%) !important;
            -webkit-background-clip: text !important;
            -webkit-text-fill-color: transparent !important;
            background-clip: text !important;
            display: inline-block;
        }
        
        /* Dark Mode Override for Text String Gradient to keep contrast sharp */
        @media (prefers-color-scheme: dark) {
            h1 [data-testid="stHeaderBlockContent"],
            h1 span:not(:has(img)) {
                background: linear-gradient(135deg, #f8fafc 40%, #60a5fa 100%) !important;
                -webkit-background-clip: text !important;
                -webkit-text-fill-color: transparent !important;
                background-clip: text !important;
            }
        }
        
        /* FORCE EMOJIS AND IMAGES TO IGNORE ALL CLIPPING */
        h1 img, 
        h1 span[role="img"],
        h1 data-emoji,
        [data-testid="stHeaderElement"] img {
            -webkit-text-fill-color: initial !important;
            -webkit-background-clip: initial !important;
            background-clip: initial !important;
            background: transparent !important;
            display: inline-block !important;
        }
        
        /* Remove native Streamlit header link icon anchor padding */
        h1 a {
            display: none !important;
        }

        /* 2. Style the metric cards */
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
        
        /* 3. 3D TACTILE TABS NAVIGATION */
        .stTabs [data-baseweb="tab-list"] {
            gap: 12px;
            background-color: transparent;
            padding-bottom: 0px; 
            border-bottom: 2px solid rgba(128, 128, 128, 0.2); 
            align-items: flex-end; 
        }
        
        .stTabs [data-baseweb="tab"] {
            height: 46px;
            border-radius: 8px 8px 0px 0px; 
            padding: 10px 24px;
            font-size: 15px !important;
            font-weight: 600 !important;
            color: var(--text-color);
            background-color: rgba(128, 128, 128, 0.08) !important; 
            border: 1px solid rgba(128, 128, 128, 0.25) !important;
            border-bottom: none !important; 
            box-shadow: 0 -3px 6px -1px rgba(0, 0, 0, 0.04), 0 -2px 4px -1px rgba(0, 0, 0, 0.03);
            transform: translateY(-4px); 
            transition: all 0.15s cubic-bezier(0.4, 0, 0.2, 1);
        }
        
        .stTabs [data-baseweb="tab"]:hover {
            background-color: rgba(128, 128, 128, 0.15) !important;
            transform: translateY(-6px); 
            box-shadow: 0 -4px 8px -1px rgba(0, 0, 0, 0.08);
        }
        
        .stTabs [aria-selected="true"] {
            height: 48px !important; 
            background: linear-gradient(135deg, #3b82f6, #1d4ed8) !important; 
            color: #ffffff !important; 
            border: 1px solid #1e40af !important;
            border-bottom: 2px solid var(--background-color) !important; 
            transform: translateY(2px) !important; 
            box-shadow: none !important; 
        }
        
        .stTabs [data-baseweb="tab-highlight"],
        .stTabs [data-baseweb="tab-border"] {
            display: none !important;
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