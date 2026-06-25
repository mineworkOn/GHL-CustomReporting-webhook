import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.graph_objects as go
from api import *
from design import *

# 1. Page Configuration (Must be first)
st.set_page_config(page_title="Operational Dashboard", page_icon="📈", layout="wide", initial_sidebar_state="collapsed")

# Theme state management
if "theme" not in st.session_state:
    st.session_state.theme = "light"  # Default to Light theme

def toggle_theme():
    st.session_state.theme = "light" if st.session_state.theme == "dark" else "dark"

IS_DARK = st.session_state.theme == "dark"

# 2. Inject Dynamic Stylings
apply_custom_style()

# 3. Premium Header Layout
header_left, header_right = st.columns([0.8, 0.2])

with header_left:
    st.markdown(f"""
    <div style="display: flex; align-items: center; gap: 16px; margin-bottom: 1.5rem;">
        <div style="background: linear-gradient(135deg, #2563eb, #1d4ed8); width: 48px; height: 48px; border-radius: 12px; display: flex; align-items: center; justify-content: center; color: white; font-size: 20px;">
            <i class="fa-solid fa-chart-line"></i>
        </div>
        <div>
            <h1 style="margin: 0; font-size: 1.65rem; font-weight: 800; letter-spacing: -0.02em; line-height: 1.2; font-family: 'Plus Jakarta Sans', sans-serif;">
                Marketing & Operations Framework
            </h1>
            <p style="margin: 0; font-size: 0.8rem; color: var(--text-muted); display: flex; align-items: center; gap: 6px; font-family: 'Plus Jakarta Sans', sans-serif;">
                <span class="status-dot"></span> Active sync with GoHighLevel & Apollo &nbsp;•&nbsp; Updated just now
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)

with header_right:
    theme_btn_label = "☀️ Light Mode" if IS_DARK else "🌙 Dark Mode"
    st.button(theme_btn_label, on_click=toggle_theme, width="stretch")

# 4. Fetch all live data automatically
loading_placeholder = st.empty()
loading_placeholder.markdown("""
<style>
.custom-loader-container {
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
}

.custom-loader-card {
    background: var(--card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 16px !important;
    padding: 2.25rem 2.75rem !important;
    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25) !important;
    width: 580px !important;
    display: flex !important;
    flex-direction: column !important;
    gap: 1.25rem !important;
    animation: spinnerEntrance 0.5s cubic-bezier(0.16, 1, 0.3, 1) both !important;
}

.custom-loader-title {
    font-size: 1.25rem !important;
    font-weight: 800 !important;
    color: var(--text) !important;
    letter-spacing: -0.025em !important;
    font-family: 'Plus Jakarta Sans', -apple-system, sans-serif !important;
    margin: 0 !important;
}

.custom-loader-subtitle {
    font-size: 0.85rem !important;
    color: var(--text-muted) !important;
    font-family: 'Plus Jakarta Sans', -apple-system, sans-serif !important;
    margin-top: -0.75rem !important;
    margin-bottom: 0.25rem !important;
}

.custom-loader-progress-track {
    width: 100% !important;
    height: 8px !important;
    background: var(--border-subtle) !important;
    border: 1px solid var(--border) !important;
    border-radius: 100px !important;
    position: relative !important;
    overflow: hidden !important;
}

.custom-loader-progress-fill {
    position: absolute !important;
    top: 0 !important;
    left: 0 !important;
    height: 100% !important;
    width: 35% !important;
    background: linear-gradient(90deg, var(--accent) 0%, #3b82f6 100%) !important;
    border-radius: 100px !important;
    animation: progressSlide 1.5s infinite cubic-bezier(0.4, 0, 0.2, 1) !important;
}

@keyframes progressSlide {
    0% { left: -35%; }
    100% { left: 100%; }
}

@keyframes spinnerEntrance {
    from { opacity: 0; transform: translateY(-24px) scale(0.96); }
    to { opacity: 1; transform: translateY(0) scale(1); }
}

@keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
}
</style>
<div class="custom-loader-container">
    <div class="custom-loader-card">
        <div class="custom-loader-title">Syncing Live Data</div>
        <div class="custom-loader-subtitle">Syncing live data from GoHighLevel & Apollo...</div>
        <div class="custom-loader-progress-track">
            <div class="custom-loader-progress-fill"></div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

user_mapping = get_user_mapping()
contacts = fetch_contacts()
stage_mapping = fetch_pipelines()
opportunities = fetch_opportunities()
apollo_metrics = fetch_apollo_outreach()

loading_placeholder.empty()


# Create tabs for clean navigation
tab1, tab2, tab3 = st.tabs(["Apollo Marketing Outreach", "GHL AE Distribution", "GHL Pipeline Stages"])

# --- TAB 1: MARKETING OUTREACH (Live Apollo Data) ---
with tab1:
    st.markdown('<div style="margin-bottom: 1.25rem;"><h3 style="margin: 0; font-size: 1.2rem; font-weight: 700;">Email & Task Outreach Tracking</h3><p style="margin: 0; font-size: 0.8rem; color: var(--text-muted);">Campaign metrics and sales pipeline engagement</p></div>', unsafe_allow_html=True)
    
    current_date = datetime.now().strftime("%a, %d %b %Y")
    
    df_outreach = pd.DataFrame([{
        "Date": current_date,
        "Total": apollo_metrics.get("Total", 0),
        "Sent": apollo_metrics.get("Sent", 0),
        "Delivered": apollo_metrics.get("Delivered", 0),
        "Delivered (Open Tracked)": apollo_metrics.get("Delivered (Open Tracked)", 0),     
        "Delivered (Click Tracked)": apollo_metrics.get("Delivered (Click Tracked)", 0),   
        "Opened": apollo_metrics.get("Opened", 0),
        "Clicked": apollo_metrics.get("Clicked", 0),
        "Unsubscribed": apollo_metrics.get("Unsubscribed", 0),
        "Replied": apollo_metrics.get("Replied", 0),
        "Interested": apollo_metrics.get("Interested", 0),
        "Bounced": apollo_metrics.get("Bounced", 0),
        "Spam Blocked": apollo_metrics.get("Spam Blocked", 0),
        "Not Sent": apollo_metrics.get("Not Sent", 0),
        "Pending Call Task": apollo_metrics.get("Pending Call Task", 0)
    }])
    
    # 4 Premium KPI Cards
    col1, col2, col3, col4 = st.columns(4)
    
    total_contacts = max(1, apollo_metrics.get("Total", 0))
    delivered_val = apollo_metrics.get("Delivered", 0)
    delivery_rate = int((delivered_val / total_contacts) * 100)
    
    interested_val = apollo_metrics.get("Interested", 0)
    interested_rate = int((interested_val / max(1, delivered_val)) * 100)
    
    with col1:
        metric_card(
            label="Total Uploaded",
            value=f"{apollo_metrics.get('Total', 0):,}",
            icon_class="fa-solid fa-users",
            meta="Total marketing contacts"
        )
    with col2:
        metric_card(
            label="Delivered",
            value=f"{delivered_val:,}",
            icon_class="fa-solid fa-paper-plane",
            delta=f"{delivery_rate}%",
            delta_type="up" if delivery_rate > 70 else "warn",
            meta="Delivery success rate"
        )
    with col3:
        metric_card(
            label="Interested",
            value=f"{interested_val:,}",
            icon_class="fa-solid fa-star",
            delta=f"{interested_rate}%",
            delta_type="up" if interested_rate > 2 else "normal",
            meta="Delivered to demo conversion"
        )
    with col4:
        pending_calls = apollo_metrics.get("Pending Call Task", 0)
        metric_card(
            label="Pending Calls",
            value=f"{pending_calls:,}",
            icon_class="fa-solid fa-phone-volume",
            delta=str(pending_calls) if pending_calls > 0 else None,
            delta_type="warn" if pending_calls > 0 else "normal",
            meta="Active outreach call tasks"
        )
    
    # 1. Full-Width Table showing all columns
    st.markdown('<div class="table-card"><div class="table-title">Outreach Analytics Breakdown</div><div class="table-subtitle">Granular daily performance stats from Apollo.io</div>', unsafe_allow_html=True)
    html_table_outreach = render_premium_html_table(df_outreach)
    st.markdown(html_table_outreach, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # 2. Funnel Chart below the table (Centred/Full width)
    funnel_stages = ["Total", "Sent", "Delivered", "Opened", "Clicked", "Replied", "Interested"]
    funnel_values = [apollo_metrics.get(stage, 0) for stage in funnel_stages]
    
    if sum(funnel_values) > 0:
        fig = go.Figure(go.Funnel(
            y=funnel_stages,
            x=funnel_values,
            textposition="inside",
            textinfo="value+percent initial",
            opacity=0.85,
            marker={"color": ["#1e3a8a", "#2563eb", "#3b82f6", "#60a5fa", "#93c5fd", "#10b981", "#059669"]}
        ))
        
        fig.update_layout(
            **get_plotly_layout(IS_DARK, margin=dict(l=150, r=150, t=20, b=20)),
            height=340
        )
        
        st.markdown('<div class="chart-wrap"><div class="chart-title">Outreach Conversion Funnel</div><div class="chart-subtitle">Conversion rates throughout the marketing campaign sequence</div>', unsafe_allow_html=True)
        st.plotly_chart(fig, width="stretch", config={"displayModeBar": False})
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("No conversion funnel data available.")


# --- TAB 2: AE DISTRIBUTION (Live GHL Data) ---
with tab2:
    st.markdown('<div style="margin-bottom: 1.25rem;"><h3 style="margin: 0; font-size: 1.2rem; font-weight: 700;">Account Executive Roster & Lead Routing</h3><p style="margin: 0; font-size: 0.8rem; color: var(--text-muted);">Active routing logs and lead load balances across AEs</p></div>', unsafe_allow_html=True)
    
    ae_counts = {user_name: 0 for user_name in user_mapping.values()}
    unassigned_count = 0
        
    for contact in contacts:
        owner_id = contact.get("assignedTo")
        if owner_id and owner_id in user_mapping:
            owner_name = user_mapping[owner_id]
            ae_counts[owner_name] += 1
        else:
            unassigned_count += 1

    # Roster Counts
    filtered_ae_counts = ae_counts
        
    # Stats metrics
    c1, c2, c3 = st.columns(3)
    active_ae_count = len([n for n in filtered_ae_counts.keys() if n not in ["Total", "Unassigned"]])
    total_assigned_leads = sum(filtered_ae_counts.values())
    
    with c1:
        metric_card(
            label="Total Active AEs",
            value=str(active_ae_count),
            icon_class="fa-solid fa-user-tie",
            meta="Count of registered staff AEs"
        )
    with c2:
        metric_card(
            label="Assigned Leads",
            value=f"{total_assigned_leads:,}",
            icon_class="fa-solid fa-user-check",
            meta="Leads successfully routed to roster AEs"
        )
    with c3:
        metric_card(
            label="Unassigned Leads",
            value=f"{unassigned_count:,}",
            icon_class="fa-solid fa-user-xmark",
            delta=str(unassigned_count) if unassigned_count > 0 else None,
            delta_type="warn" if unassigned_count > 0 else "normal",
            meta="Leads remaining in the unassigned pool"
        )

    # Roster Table
    if filtered_ae_counts or unassigned_count > 0:
        df_ae = pd.DataFrame({
            "AE Name": list(filtered_ae_counts.keys()),
            "AE Status": ["Active"] * len(filtered_ae_counts), 
            "Assign Leads": list(filtered_ae_counts.values())
        })
        df_ae = df_ae.sort_values(by="Assign Leads", ascending=False)
        
        unassigned_row = pd.DataFrame([{
            "AE Name": "Unassigned", 
            "AE Status": "-", 
            "Assign Leads": unassigned_count
        }])
        df_ae = pd.concat([df_ae, unassigned_row], ignore_index=True)
            
        total_row = pd.DataFrame([{
            "AE Name": "Total", 
            "AE Status": "", 
            "Assign Leads": df_ae["Assign Leads"].sum()
        }])
        df_ae = pd.concat([df_ae, total_row], ignore_index=True)
        
        st.markdown('<div class="table-card"><div class="table-title">Lead Assignment Roster</div><div class="table-subtitle">Lead routing distribution with relative share progress bars</div>', unsafe_allow_html=True)
        html_table_ae = render_premium_html_table(df_ae)
        st.markdown(html_table_ae, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("No Account Executives found.")


# --- TAB 3: PIPELINE STAGES (Live GHL Data) ---
with tab3:
    st.markdown('<div style="margin-bottom: 1.25rem;"><h3 style="margin: 0; font-size: 1.2rem; font-weight: 700;">Sales Pipeline Health</h3><p style="margin: 0; font-size: 0.8rem; color: var(--text-muted);">Deals volume and value mapping across stages</p></div>', unsafe_allow_html=True)
    
    stage_counts = {stage_name: 0 for stage_name in stage_mapping.values()}
    
    for opp in opportunities:
        stage_id = opp.get("pipelineStageId")
        if stage_id in stage_mapping:
            stage_name = stage_mapping[stage_id]
            stage_counts[stage_name] += 1
            
    total_pipeline_leads = sum(stage_counts.values())
    
    filtered_stage_counts = stage_counts
        
    # KPI cards
    c1, c2 = st.columns(2)
    active_stages = len([c for c in filtered_stage_counts.values() if c > 0])
    
    with c1:
        metric_card(
            label="Total Deals In Pipeline",
            value=f"{total_pipeline_leads:,}",
            icon_class="fa-solid fa-briefcase",
            meta="Active opportunity count from GoHighLevel"
        )
    with c2:
        metric_card(
            label="Active Stages",
            value=str(active_stages),
            icon_class="fa-solid fa-diagram-project",
            meta="Stages with at least 1 deal currently"
        )

    # Table & Chart
    if filtered_stage_counts:
        df_pipeline = pd.DataFrame(list(filtered_stage_counts.items()), columns=["Stage", "Count"])
        
        # Add total row
        total_row_pipeline = pd.DataFrame([{"Stage": "Total leads", "Count": df_pipeline["Count"].sum()}])
        df_pipeline = pd.concat([df_pipeline, total_row_pipeline], ignore_index=True)
        
        col_t, col_c = st.columns([1, 1.2])
        
        with col_t:
            st.markdown('<div class="table-card"><div class="table-title">Pipeline Stage Distribution</div><div class="table-subtitle">Opportunity density by staging area</div>', unsafe_allow_html=True)
            html_table_pipeline = render_premium_html_table(df_pipeline)
            st.markdown(html_table_pipeline, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
        with col_c:
            df_chart = df_pipeline[(df_pipeline["Stage"] != "Total leads") & (df_pipeline["Count"] > 0)]
            if not df_chart.empty:
                # Plotly horizontal bar chart for high readability of stages
                fig_pipe = go.Figure(go.Bar(
                    y=df_chart["Stage"],
                    x=df_chart["Count"],
                    orientation='h',
                    marker=dict(
                        color='#2563eb',
                        line=dict(color='rgba(0,0,0,0)', width=0)
                    ),
                    text=df_chart["Count"],
                    textposition='auto',
                ))
                
                pipe_layout = get_plotly_layout(IS_DARK, margin=dict(l=150, r=20, t=10, b=10))
                pipe_layout["yaxis"]["autorange"] = "reversed"
                
                fig_pipe.update_layout(
                    **pipe_layout,
                    height=320
                )
                
                st.markdown('<div class="chart-wrap"><div class="chart-title">Opportunities Density Chart</div><div class="chart-subtitle">Horizontal stage breakdown mapping deal quantities</div>', unsafe_allow_html=True)
                st.plotly_chart(fig_pipe, width="stretch", config={"displayModeBar": False})
                st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.info("No active deals in the pipeline to chart.")
    else:
        st.info("No pipeline stages found.")