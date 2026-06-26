import streamlit as st
import pandas as pd

def apply_custom_style():
    """Injects Bootstrap CSS, FontAwesome, and custom stylesheets to style the Streamlit app beautifully."""
    
    # Detect the current theme from session state (defaults to light as requested)
    is_dark = st.session_state.get("theme", "light") == "dark"
    
    # Define colors dynamically based on the active theme
    bg = "#09090b" if is_dark else "#ffffff"
    bg_subtle = "#0c0c0f" if is_dark else "#f9fafb"
    card = "#0c0c0f" if is_dark else "#ffffff"
    card_hover = "#131316" if is_dark else "#f4f4f5"
    border = "#1e1e24" if is_dark else "#e4e4e7"
    border_subtle = "#16161a" if is_dark else "#f0f0f2"
    text = "#fafafa" if is_dark else "#09090b"
    text_muted = "#a1a1aa" if is_dark else "#71717a"
    text_dim = "#52525b" if is_dark else "#a1a1aa"
    accent = "#2563eb"
    green = "#22c55e" if is_dark else "#16a34a"
    green_muted = "rgba(34,197,94,0.12)" if is_dark else "rgba(22,163,74,0.08)"
    red = "#ef4444" if is_dark else "#dc2626"
    red_muted = "rgba(239,68,68,0.12)" if is_dark else "rgba(220,38,38,0.08)"
    amber = "#f59e0b" if is_dark else "#d97706"
    amber_muted = "rgba(245,158,11,0.12)" if is_dark else "rgba(217,119,6,0.08)"
    shadow = "none" if is_dark else "0 2px 4px rgba(0,0,0,0.02), 0 1px 2px rgba(0,0,0,0.03)"
    radius = "12px"
    backdrop = "rgba(9, 9, 11, 0.65)" if is_dark else "rgba(255, 255, 255, 0.65)"
 
    custom_css = f"""
    <!-- Bootstrap and FontAwesome Integration -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;700&display=swap');
        
        /* 1. CSS VARIABLES SETUP */
        :root {{
            --bg: {bg};
            --bg-subtle: {bg_subtle};
            --card: {card};
            --card-hover: {card_hover};
            --border: {border};
            --border-subtle: {border_subtle};
            --text: {text};
            --text-muted: {text_muted};
            --text-dim: {text_dim};
            --accent: {accent};
            --green: {green};
            --green-muted: {green_muted};
            --red: {red};
            --red-muted: {red_muted};
            --amber: {amber};
            --amber-muted: {amber_muted};
            --shadow: {shadow};
            --radius: {radius};
            --backdrop: {backdrop};
        }}
        
        /* 2. HIDE STREAMLIT CHROME AND SIDEBAR CONTROLS */
        header[data-testid="stHeader"], 
        #MainMenu, 
        footer, 
        [data-testid="stToolbar"],
        [data-testid="stDecoration"], 
        [data-testid="stStatusWidget"], 
        .stDeployButton,
        [data-testid="stSidebar"],
        div[data-testid="stSidebarCollapsedControl"] {{
            display: none !important;
        }}
        
        /* Disable sidebar completely */
        [data-testid="collapsedControl"] {{
            display: none !important;
        }}
        
        /* 3. GLOBAL BASE STYLING */
        html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"], .main, .block-container, section[data-testid="stMain"] {{
            background-color: var(--bg) !important;
            color: var(--text) !important;
            font-family: 'Plus Jakarta Sans', -apple-system, sans-serif !important;
        }}
        
        .text-muted {{
            color: var(--text-muted) !important;
        }}
        
        .metric-delta {{
            font-weight: 700 !important;
            font-size: 0.8rem !important;
        }}
        
        .delta-up {{
            color: var(--green) !important;
        }}
        
        .delta-down {{
            color: var(--red) !important;
        }}
        
        .delta-warn {{
            color: var(--amber) !important;
        }}
        
        .delta-normal {{
            color: var(--text-muted) !important;
        }}
        
        /* 12. SELECTBOX BASE INPUT STYLING */
        div[data-baseweb="select"] > div {{
            background-color: var(--card) !important;
            border-color: var(--border) !important;
            color: var(--text) !important;
            transition: all 0.2s ease !important;
        }}
        
        div[data-baseweb="select"] > div:hover {{
            border-color: var(--accent) !important;
        }}
        
        div[data-baseweb="select"] [data-testid="stSelectboxSelectedValue"] {{
            color: var(--text) !important;
        }}
        
        div[data-baseweb="select"] input {{
            color: var(--text) !important;
        }}
        
        div[data-baseweb="select"] svg {{
            fill: var(--text-muted) !important;
        }}
        
        html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"], .main, section[data-testid="stMain"] {{
            max-width: 100% !important;
            overflow-x: hidden !important;
        }}
        
        .block-container {{
            padding: 2.5rem 3rem 3rem !important;
            max-width: 1360px !important;
        }}
        
        /* 4. SMOOTH FADE-IN TRANSITION ANIMATION */
        @keyframes dashboardFadeIn {{
            from {{
                opacity: 0;
                transform: translateY(12px);
            }}
            to {{
                opacity: 1;
                transform: translateY(0);
            }}
        }}
        
        .metric-card, 
        .chart-wrap, 
        .table-card,
        [data-testid="stHorizontalBlock"] {{
            animation: dashboardFadeIn 0.5s cubic-bezier(0.16, 1, 0.3, 1) both;
        }}
        
        /* 5. TABS NAVIGATION WITH SEGMENTED SWITCH & GLOW ANIMATIONS */
        [data-baseweb="tab-list"] {{
            gap: 8px !important;
            background: var(--bg-subtle) !important;
            border: 1px solid var(--border) !important;
            border-radius: 12px !important;
            padding: 6px !important;
            width: 100% !important;
            max-width: 780px !important;
            margin-bottom: 2rem !important;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03) !important;
            display: flex !important;
            align-items: center !important;
            position: relative !important;
        }}
        
        div[data-testid="stTabs"] [data-baseweb="tab-list"] button[data-baseweb="tab"] {{
            background: transparent !important;
            color: var(--text-muted) !important;
            font-size: 0.88rem !important;
            font-weight: 500 !important;
            height: 40px !important;
            padding: 0 1.2rem !important;
            border: 1px solid transparent !important;
            border-radius: 8px !important;
            font-family: 'Plus Jakarta Sans', sans-serif !important;
            transition: all 0.35s cubic-bezier(0.34, 1.56, 0.64, 1) !important;
            position: relative !important;
            z-index: 5 !important;
            opacity: 0.7;
            flex: 1 !important;
            text-align: center !important;
            overflow: visible !important;
        }}
        
        div[data-testid="stTabs"] [data-baseweb="tab-list"] button[data-baseweb="tab"] p,
        div[data-testid="stTabs"] [data-baseweb="tab-list"] button[data-baseweb="tab"] span,
        div[data-testid="stTabs"] [data-baseweb="tab-list"] button[data-baseweb="tab"] div {{
            font-size: inherit !important;
            font-weight: inherit !important;
            color: inherit !important;
            transition: all 0.35s cubic-bezier(0.34, 1.56, 0.64, 1) !important;
            margin: 0 !important;
            overflow: visible !important;
        }}
        
        div[data-testid="stTabs"] [data-baseweb="tab-list"] button[data-baseweb="tab"]:hover:not([aria-selected="true"]) {{
            color: var(--text) !important;
            opacity: 0.95;
            transform: translateY(-1px) scale(1.02) !important;
        }}
        
        div[data-testid="stTabs"] [data-baseweb="tab-list"] button[data-baseweb="tab"][aria-selected="true"] {{
            color: #ffffff !important;
            background: transparent !important;
            border-color: transparent !important;
            font-size: 1.22rem !important;
            font-weight: 800 !important;
            opacity: 1 !important;
            height: 48px !important;
            padding: 0 1.85rem !important;
            z-index: 10 !important;
            transform: scale(1.04) !important;
        }}
        
        div[data-testid="stTabs"] [data-baseweb="tab-list"] button[data-baseweb="tab"][aria-selected="true"] * {{
            color: #ffffff !important;
        }}
        
        [data-baseweb="tab-border"] {{
            display: none !important;
        }}
        
        div[data-testid="stTabs"] [data-baseweb="tab-list"] [data-baseweb="tab-highlight"] {{
            display: block !important;
            background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%) !important;
            height: calc(100% - 12px) !important;
            border-radius: 8px !important;
            z-index: 1 !important;
            bottom: 6px !important;
            top: 6px !important;
            transition: all 0.45s cubic-bezier(0.34, 1.56, 0.64, 1) !important;
            box-shadow: 0 4px 14px rgba(37, 99, 235, 0.4) !important;
        }}

        /* Smooth Tab Content Fade-in (Clean & Simple) */
        div[data-testid="stTab"] {{
            animation: tabContentFadeIn 0.35s ease-out both;
        }}
        
        @keyframes tabContentFadeIn {{
            0% {{
                opacity: 0;
                transform: translateY(4px);
            }}
            100% {{
                opacity: 1;
                transform: translateY(0);
            }}
        }}
        
        /* 6. HOVER INTERACTIONS FOR CARDS */
        .metric-card {{
            transition: all 0.35s cubic-bezier(0.16, 1, 0.3, 1) !important;
            border-left: 4px solid var(--accent) !important;
            background: linear-gradient(135deg, var(--card) 0%, var(--bg-subtle) 100%) !important;
        }}
        
        .metric-card:hover {{
            transform: translateY(-4px) scale(1.02) !important;
            box-shadow: 0 12px 24px rgba(37, 99, 235, 0.12) !important;
            border-color: var(--accent) !important;
        }}
        
        .metric-card:hover .metric-icon {{
            transform: rotate(8deg) scale(1.1);
            color: #ffffff !important;
            background: var(--accent) !important;
        }}
        
        .metric-icon {{
            transition: all 0.3s ease !important;
        }}
        
        .chart-wrap:hover {{
            transform: translateY(-3px) !important;
            box-shadow: 0 10px 20px rgba(0, 0, 0, 0.08) !important;
            border-color: var(--accent) !important;
        }}
        
        /* 7. PREMIUM DATA TABLES */
        .table-card {{
            background: var(--card);
            border: 1px solid var(--border);
            border-top: 3px solid transparent;
            border-radius: var(--radius);
            padding: 1.5rem;
            box-shadow: var(--shadow);
            margin-bottom: 1.25rem;
            transition: all 0.35s cubic-bezier(0.16, 1, 0.3, 1);
        }}

        .table-card:hover {{
            transform: translateY(-4px) !important;
            box-shadow: 0 12px 24px rgba(37, 99, 235, 0.04), 0 4px 12px rgba(0, 0, 0, 0.06) !important;
            border-color: var(--border) !important;
            border-top-color: var(--accent) !important;
        }}

        .table-title {{
            font-size: 1.05rem !important;
            font-weight: 700 !important;
            color: var(--text) !important;
            margin-bottom: 0.25rem !important;
            font-family: 'Plus Jakarta Sans', sans-serif !important;
            letter-spacing: -0.015em !important;
        }}
        
        .table-subtitle {{
            font-size: 0.78rem !important;
            color: var(--text-muted) !important;
            margin-bottom: 1.25rem !important;
            font-family: 'Plus Jakarta Sans', sans-serif !important;
        }}
        
        .table-responsive-wrapper {{
            width: 100%;
            overflow-x: auto;
            -webkit-overflow-scrolling: touch;
            margin-top: 0.5rem;
            border-radius: 10px;
            border: 1px solid var(--border) !important;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.02) !important;
            transition: all 0.3s ease;
        }}

        /* Custom Premium Scrollbars */
        .table-responsive-wrapper::-webkit-scrollbar {{
            height: 6px;
            width: 6px;
        }}
        
        .table-responsive-wrapper::-webkit-scrollbar-track {{
            background: var(--bg-subtle) !important;
            border-radius: 10px;
        }}
        
        .table-responsive-wrapper::-webkit-scrollbar-thumb {{
            background: var(--border) !important;
            border-radius: 10px;
            transition: background 0.3s ease;
        }}
        
        .table-responsive-wrapper::-webkit-scrollbar-thumb:hover {{
            background: var(--accent) !important;
        }}
        
        .data-table {{
            width: 100%;
            border-collapse: separate;
            border-spacing: 0;
            font-size: 0.85rem;
        }}
        
        .data-table th {{
            text-align: left;
            padding: 0.85rem 1.25rem;
            color: var(--text-muted) !important;
            font-weight: 600 !important;
            font-size: 0.72rem !important;
            text-transform: uppercase;
            letter-spacing: 0.06em;
            border-bottom: 1px solid var(--border) !important;
            background: var(--bg-subtle) !important;
            transition: color 0.2s ease;
        }}
        
        .data-table th:first-child {{
            border-top-left-radius: 10px;
        }}
        
        .data-table th:last-child {{
            border-top-right-radius: 10px;
        }}
        
        .data-table td {{
            padding: 0.8rem 1.25rem;
            color: var(--text);
            border-bottom: 1px solid var(--border-subtle) !important;
            vertical-align: middle;
            font-size: 0.82rem;
            transition: all 0.25s ease;
        }}
        
        .data-table tr:last-child td {{
            border-bottom: none !important;
        }}
        
        /* Table Row Cascade Animation & Interactive States */
        @keyframes rowEntrance {{
            from {{
                opacity: 0;
                transform: translateY(12px);
            }}
            to {{
                opacity: 1;
                transform: translateY(0);
            }}
        }}
        
        .data-table tbody tr {{
            opacity: 0;
            animation: rowEntrance 0.5s cubic-bezier(0.16, 1, 0.3, 1) forwards;
            transition: background-color 0.25s ease, transform 0.2s ease;
        }}

        .data-table tbody tr:nth-of-type(even) {{
            background-color: rgba(128, 128, 128, 0.015) !important;
        }}
        
        .data-table tbody tr:hover {{
            background-color: var(--card-hover) !important;
            transform: scale(1.005);
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.03) !important;
        }}

        .data-table td:first-child {{
            border-left: 3px solid transparent !important;
            transition: all 0.25s ease;
        }}

        .data-table tbody tr:hover td:first-child {{
            border-left-color: var(--accent) !important;
        }}
        
        /* AVATAR STYLE */
        .ae-avatar {{
            width: 28px;
            height: 28px;
            border-radius: 50%;
            color: #ffffff;
            font-weight: 700;
            font-size: 11px;
            display: flex;
            align-items: center;
            justify-content: center;
            margin-right: 10px;
            flex-shrink: 0;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1) !important;
        }}

        .data-table tbody tr:hover .ae-avatar {{
            transform: scale(1.18) rotate(4deg);
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.18);
        }}
        
        .ae-name-cell {{
            display: flex;
            align-items: center;
            font-weight: 600;
        }}
        
        /* BADGES */
        .badge {{
            display: inline-flex;
            align-items: center;
            gap: 4px;
            padding: 4px 10px;
            border-radius: 8px;
            font-size: 0.72rem;
            font-weight: 600;
            transition: all 0.25s cubic-bezier(0.34, 1.56, 0.64, 1) !important;
        }}

        .data-table tbody tr:hover .badge {{
            transform: scale(1.08) translateY(-1px);
        }}
        
        .badge-green {{
            color: var(--green);
            background: var(--green-muted);
            border: 1px solid rgba(34, 197, 94, 0.15);
        }}
        
        .badge-pulse-dot {{
            width: 6px;
            height: 6px;
            background-color: var(--green);
            border-radius: 50%;
            display: inline-block;
            animation: pulse-animation 1.5s infinite;
        }}
        
        @keyframes pulse-animation {{
            0% {{ transform: scale(0.9); opacity: 1; }}
            50% {{ transform: scale(1.3); opacity: 0.4; }}
            100% {{ transform: scale(0.9); opacity: 1; }}
        }}
        
        /* PROGRESS BAR FOR LOAD DISTRIBUTION */
        .progress-container {{
            display: flex;
            align-items: center;
            gap: 10px;
            min-width: 160px;
        }}
        
        .progress-bar-bg {{
            flex-grow: 1;
            background: var(--border-subtle) !important;
            border: 1px solid var(--border) !important;
            height: 8px;
            border-radius: 100px;
            overflow: hidden;
            max-width: 120px;
            display: flex;
            align-items: center;
        }}
        
        .progress-bar-fill {{
            background: linear-gradient(90deg, var(--accent) 0%, #60a5fa 50%, var(--accent) 100%) !important;
            background-size: 200% 100% !important;
            height: 100%;
            border-radius: 100px;
            transition: width 0.8s cubic-bezier(0.16, 1, 0.3, 1) !important;
            position: relative;
            animation: shimmerSwipe 2.5s infinite linear !important;
        }}

        .progress-bar-fill::after {{
            content: '';
            position: absolute;
            top: 0;
            right: 0;
            width: 6px;
            height: 100%;
            background: #ffffff;
            border-radius: 100px;
            box-shadow: 0 0 8px #ffffff, 0 0 4px var(--accent);
            opacity: 0.85;
        }}

        @keyframes shimmerSwipe {{
            0% {{
                background-position: 200% 0;
            }}
            100% {{
                background-position: -200% 0;
            }}
        }}
        
        .progress-value {{
            font-weight: 700;
            color: var(--text);
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.78rem;
        }}
        
        /* TOTALS ROW */
        .total-row {{
            font-weight: 700 !important;
            background-color: rgba(37, 99, 235, 0.03) !important;
        }}
        
        .total-row td {{
            border-top: 2px solid var(--accent) !important;
            border-bottom: 2px solid var(--accent) !important;
            color: var(--accent) !important;
        }}
        
        /* SYSTEM STATUS DOT */
        .status-dot {{
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background-color: #10b981;
            display: inline-block;
            box-shadow: 0 0 8px #10b981;
        }}

        /* PILL-STYLE TAB NAVIGATION ANIMATION & SCALING */
        div[data-baseweb="tab-list"] {{
            overflow: visible !important;
            padding-top: 4px !important;
            padding-bottom: 4px !important;
        }}

        button[data-baseweb="tab"] {{
            transition: transform 0.3s ease, background-color 0.3s ease, color 0.3s ease !important;
            transform-origin: center center !important;
            margin: 0 4px !important;
        }}

        button[data-baseweb="tab"][aria-selected="true"] {{
            transform: scale(1.05) !important;
            z-index: 1 !important;
        }}

        /* 8. CUSTOM HIGH-END SCREEN-CENTERED LOADER */
        .custom-loader-container {{
            position: fixed !important;
            top: 0 !important;
            left: 0 !important;
            width: 100vw !important;
            height: 100vh !important;
            background: var(--backdrop) !important;
            backdrop-filter: blur(8px) !important;
            -webkit-backdrop-filter: blur(8px) !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            z-index: 999999 !important;
            animation: fadeIn 0.3s ease-out both !important;
        }}
        
        .custom-loader-card {{
            background: var(--card) !important;
            border: 1px solid var(--border) !important;
            border-radius: 16px !important;
            padding: 2.25rem 2.75rem !important;
            box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25) !important;
            width: 90% !important;
            max-width: 580px !important;
            display: flex !important;
            flex-direction: column !important;
            gap: 1.25rem !important;
            animation: spinnerEntrance 0.5s cubic-bezier(0.16, 1, 0.3, 1) both !important;
        }}
        
        .custom-loader-title {{
            font-size: 1.2rem !important;
            font-weight: 800 !important;
            color: var(--text) !important;
            letter-spacing: -0.02em !important;
            font-family: 'Plus Jakarta Sans', sans-serif !important;
            margin: 0 !important;
        }}
        
        .custom-loader-subtitle {{
            font-size: 0.85rem !important;
            color: var(--text-muted) !important;
            font-family: 'Plus Jakarta Sans', sans-serif !important;
            margin-top: -0.75rem !important;
            margin-bottom: 0.25rem !important;
        }}
        
        .custom-loader-progress-track {{
            width: 100% !important;
            height: 8px !important;
            background: var(--border-subtle) !important;
            border: 1px solid var(--border) !important;
            border-radius: 100px !important;
            position: relative !important;
            overflow: hidden !important;
        }}
        
        .custom-loader-progress-fill {{
            position: absolute !important;
            top: 0 !important;
            left: 0 !important;
            height: 100% !important;
            width: 35% !important;
            background: linear-gradient(90deg, var(--accent) 0%, #3b82f6 100%) !important;
            border-radius: 100px !important;
            animation: progressSlide 1.5s infinite cubic-bezier(0.4, 0, 0.2, 1) !important;
        }}
        
        @keyframes progressSlide {{
            0% {{
                left: -35%;
            }}
            100% {{
                left: 100%;
            }}
        }}
        
        @keyframes spinnerEntrance {{
            from {{
                opacity: 0;
                transform: translateY(-24px) scale(0.96);
            }}
            to {{
                opacity: 1;
                transform: translateY(0) scale(1);
            }}
        }}
        
        @keyframes fadeIn {{
            from {{ opacity: 0; }}
            to {{ opacity: 1; }}
        }}

        /* Hide mobile navigation helper container on desktop */
        div.st-key-mobile_navigation {{
            display: none !important;
        }}
        
        /* 10. THEME TOGGLE ICON BUTTON STYLING */
        div.st-key-theme_toggle_container {{
            position: absolute !important;
            top: 2.5rem !important;
            right: 3rem !important;
            z-index: 999999 !important;
            width: auto !important;
        }}
        
        div.st-key-theme_toggle_container button {{
            width: 42px !important;
            height: 42px !important;
            min-width: 42px !important;
            max-width: 42px !important;
            min-height: 42px !important;
            max-height: 42px !important;
            border-radius: 50% !important;
            padding: 0 !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            font-size: 1.25rem !important;
            background-color: var(--card) !important;
            color: var(--text) !important;
            border: 1px solid var(--border) !important;
            cursor: pointer !important;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
            box-shadow: var(--shadow) !important;
        }}
        
        div.st-key-theme_toggle_container button:hover {{
            border-color: var(--accent) !important;
            transform: scale(1.08) !important;
            box-shadow: 0 0 12px rgba(37, 99, 235, 0.2) !important;
            background-color: var(--card-hover) !important;
        }}
        
        div.st-key-theme_toggle_container button:active {{
            transform: scale(0.95) !important;
        }}
        
        div.st-key-theme_toggle_container button p,
        div.st-key-theme_toggle_container button span {{
            font-size: 1.25rem !important;
            margin: 0 !important;
            line-height: 1 !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
        }}
        
        /* 11. SELECTBOX POPOVER & OPTIONS STYLING (DARK/LIGHT MODE ADAPTIVITY) */
        div[data-baseweb="popover"] {{
            background-color: var(--card) !important;
            border: 1px solid var(--border) !important;
            border-radius: var(--radius) !important;
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.25) !important;
        }}
        
        div[data-baseweb="popover"] ul {{
            background-color: var(--card) !important;
            border-radius: var(--radius) !important;
            padding: 6px !important;
        }}
        
        div[data-baseweb="popover"] li {{
            background-color: var(--card) !important;
            color: var(--text) !important;
            font-family: 'Plus Jakarta Sans', -apple-system, sans-serif !important;
            padding: 10px 14px !important;
            border-radius: 8px !important;
            margin: 2px 0 !important;
            font-size: 0.85rem !important;
            transition: all 0.2s ease !important;
        }}
        
        div[data-baseweb="popover"] li:hover {{
            background-color: var(--card-hover) !important;
            color: var(--text) !important;
            cursor: pointer !important;
        }}
        
        /* Highlight / Selected Option style */
        div[data-baseweb="popover"] li[aria-selected="true"] {{
            background-color: var(--accent) !important;
            color: #ffffff !important;
        }}
        
        /* 9. RESPONSIVE DESIGN MEDIA QUERIES */
        @media (max-width: 768px) {{
            /* Theme Toggle Mobile Override */
            div.st-key-theme_toggle_container {{
                top: 1.5rem !important;
                right: 1rem !important;
            }}
            
            /* Hide desktop navigation container on mobile */
            div.st-key-desktop_navigation {{
                display: none !important;
            }}
            /* Show and style mobile navigation container on mobile */
            div.st-key-mobile_navigation {{
                display: block !important;
                margin-bottom: 1.5rem !important;
                width: 100% !important;
            }}
            
            /* Block container padding overrides */
            .block-container {{
                padding: 1.5rem 1rem 2rem !important;
                max-width: 100% !important;
                overflow-x: hidden !important;
            }}
            
            /* Responsive header overrides */
            .responsive-header-title {{
                font-size: 1.35rem !important;
            }}
            .responsive-header-subtitle {{
                font-size: 0.75rem !important;
            }}
            
            /* Responsive Cards & Metric Elements */
            .metric-card {{
                padding: 1.25rem !important;
                min-height: 100px !important;
            }}
            .metric-value {{
                font-size: 1.45rem !important;
            }}
            .metric-label {{
                font-size: 0.7rem !important;
            }}
            
            /* Responsive Tables overrides */
            .table-card {{
                padding: 1rem !important;
            }}
            .table-title {{
                font-size: 0.95rem !important;
            }}
            .table-subtitle {{
                font-size: 0.72rem !important;
            }}
            .data-table {{
                font-size: 0.75rem !important;
            }}
            .data-table th, .data-table td {{
                padding: 0.6rem 0.8rem !important;
                font-size: 0.75rem !important;
            }}
            .progress-container {{
                min-width: 90px !important;
                gap: 6px !important;
            }}
            .progress-bar-bg {{
                max-width: 60px !important;
            }}
            
            /* Responsive Loader */
            .custom-loader-card {{
                padding: 1.5rem !important;
                gap: 1rem !important;
            }}
            .custom-loader-title {{
                font-size: 1.1rem !important;
            }}
        }}
    </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)

def metric_card(label, value, icon_class="fa-solid fa-chart-simple", delta=None, delta_type="up", meta=None):
    """Renders a beautiful custom metric card. Everything is built on a single line to prevent Streamlit code leaks."""
    cls = f"delta-{delta_type}"
    arrow = "↑" if delta_type == "up" else ("↓" if delta_type == "down" else "→")
    delta_html = f'<span class="metric-delta {cls}">{arrow} {delta}</span>' if delta else ""
    meta_html = f'<span class="metric-meta text-muted ms-1" style="font-size: 0.75rem;">{meta}</span>' if meta else ""
    
    html_content = (
        f'<div class="metric-card card border-0 p-4 mb-3 position-relative overflow-hidden" '
        f'style="background: var(--card); border: 1px solid var(--border) !important; border-radius: var(--radius); box-shadow: var(--shadow); transition: all 0.3s ease; min-height: 120px; display: flex; flex-direction: column; justify-content: space-between;">'
        f'<div class="d-flex justify-content-between align-items-center">'
        f'<span class="metric-label text-uppercase tracking-wider text-muted fw-semibold" style="font-size: 0.75rem;">{label}</span>'
        f'<div class="metric-icon rounded p-2" style="background: rgba(37,99,235,0.08); color: var(--accent); width: 32px; height: 32px; display: flex; align-items: center; justify-content: center; font-size: 0.95rem;"><i class="{icon_class}"></i></div>'
        f'</div>'
        f'<h3 class="metric-value fw-bold mt-2 mb-1" style="font-size: 1.8rem; letter-spacing: -0.03em; color: var(--text); font-family: \'Plus Jakarta Sans\', sans-serif;">{value}</h3>'
        f'<div class="metric-footer d-flex align-items-center gap-1 mt-1">{delta_html}{meta_html}</div>'
        f'</div>'
    )
    st.markdown(html_content, unsafe_allow_html=True)

def get_avatar_html(name):
    """Generates initials avatar with preset background color based on name string."""
    if name in ["Total", "Unassigned", "Total leads"]:
        return ""
    parts = name.split()
    initials = "".join([p[0].upper() for p in parts[:2]]) if parts else "AE"
    colors = ["#3b82f6", "#10b981", "#8b5cf6", "#f59e0b", "#ec4899", "#06b6d4"]
    color_idx = sum(ord(c) for c in name) % len(colors)
    bg_color = colors[color_idx]
    return f'<div class="ae-avatar" style="background-color: {bg_color};">{initials}</div>'

def render_premium_html_table(df):
    """
    Converts a pandas DataFrame into a beautiful HTML table that adapts to Dark/Light mode.
    Dynamically applies design styling based on the dataframe column structures.
    """
    # 1. Determine table type
    is_ae_table = "AE Name" in df.columns
    is_pipeline_table = "Stage" in df.columns
    
    # Generate wrapper (single line concat to avoid code output issues)
    html = '<div class="table-responsive-wrapper"><table class="data-table"><thead><tr>'
    
    # 2. Table Headers
    for col in df.columns:
        html += f'<th>{col}</th>'
    html += "</tr></thead><tbody>"
    
    # Determine max values for relative progress/load bars
    max_leads = 1
    total_leads = 1
    
    if is_ae_table:
        # Get max lead count for AEs (excluding Total and Unassigned)
        ae_active_leads = df[(~df["AE Name"].isin(["Total", "Unassigned"]))]["Assign Leads"]
        max_leads = ae_active_leads.max() if not ae_active_leads.empty else 1
        if max_leads <= 0:
            max_leads = 1
            
    elif is_pipeline_table:
        # Get total leads count
        total_row = df[df["Stage"] == "Total leads"]
        total_leads = total_row["Count"].values[0] if not total_row.empty else 1
        if total_leads <= 0:
            total_leads = 1
            
    # 3. Table Rows
    for i, (_, row) in enumerate(df.iterrows()):
        name_val = row.get("AE Name") or row.get("Stage") or row.get("Date", "")
        is_total = name_val in ["Total", "Total leads"]
        row_style = f' style="animation-delay: {i * 40}ms;"' if not is_total else ""
        row_class = ' class="total-row"' if is_total else ""
        html += f"<tr{row_class}{row_style}>"
        
        for col in df.columns:
            val = row[col]
            
            # Format/style cells dynamically
            if col == "AE Name":
                if is_total:
                    html += f'<td><strong>{val}</strong></td>'
                else:
                    avatar = get_avatar_html(val)
                    html += f'<td><div class="ae-name-cell">{avatar}<span>{val}</span></div></td>'
            
            elif col == "Stage":
                if is_total:
                    html += f'<td><strong>{val}</strong></td>'
                else:
                    html += f'<td><strong>{val}</strong></td>'
                    
            elif col == "AE Status":
                if is_total or val in ["-", ""]:
                    html += '<td>-</td>'
                elif val == "Active":
                    html += '<td><span class="badge badge-green"><span class="badge-pulse-dot"></span>Active</span></td>'
                else:
                    html += f'<td><span class="badge">{val}</span></td>'
                    
            elif col == "Assign Leads" and is_ae_table:
                if is_total or name_val == "Unassigned":
                    html += f'<td><span class="progress-value">{val}</span></td>'
                else:
                    percent = min(100, int((val / max_leads) * 100))
                    html += f'<td><div class="progress-container"><span class="progress-value">{val}</span><div class="progress-bar-bg"><div class="progress-bar-fill" style="width: {percent}%;"></div></div></div></td>'
                    
            elif col == "Count" and is_pipeline_table:
                if is_total:
                    html += f'<td><span class="progress-value">{val}</span></td>'
                else:
                    percent = min(100, int((val / total_leads) * 100))
                    html += f'<td><div class="progress-container"><span class="progress-value">{val}</span><div class="progress-bar-bg"><div class="progress-bar-fill" style="width: {percent}%; background: var(--accent);"></div></div><span style="font-size: 0.72rem; color: var(--text-muted);">{percent}%</span></div></td>'
                    
            elif isinstance(val, (int, float)):
                # Highlight other numeric values cleanly
                html += f'<td style="font-family: \'JetBrains Mono\', monospace; font-weight: 600;">{val}</td>'
            else:
                html += f"<td>{val}</td>"
                
        html += "</tr>"
        
    html += "</tbody></table></div>"
    return html

def get_plotly_layout(is_dark=False, margin=None):
    """Returns a transparent, clean Plotly layout that matches the active theme."""
    text_color = "#fafafa" if is_dark else "#09090b"
    muted_color = "#a1a1aa" if is_dark else "#71717a"
    grid_color = "rgba(255,255,255,0.06)" if is_dark else "rgba(9,9,11,0.06)"
    
    use_margin = margin if margin is not None else dict(l=40, r=20, t=20, b=40)
    
    return dict(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Plus Jakarta Sans, sans-serif", color=text_color, size=11),
        margin=use_margin,
        showlegend=False,
        xaxis=dict(
            gridcolor=grid_color,
            zerolinecolor=grid_color,
            tickfont=dict(size=10, color=muted_color),
            showgrid=True,
            linecolor=grid_color,
        ),
        yaxis=dict(
            gridcolor=grid_color,
            zerolinecolor=grid_color,
            tickfont=dict(size=10, color=muted_color),
            showgrid=True,
            linecolor=grid_color,
        ),
        dragmode=False,
    )