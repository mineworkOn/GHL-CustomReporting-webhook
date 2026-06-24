import streamlit as st
import pandas as pd
from datetime import datetime
from api import *
from design import *

# 1. Page Configuration (Keep page_icon as a backup fallback asset)
st.set_page_config(page_title="Dashboard", page_icon="📈", layout="wide")

# 2. Inject Dynamic Stylings
apply_custom_style()

# 3. FIX: Bulletproof SaaS-style Header Block Layout
# We wrapped this in a unique class 'main-dashboard-title' so design.py won't break it
# --- PURE NATIVE SAAS HEADER ---
# We use st.columns to prevent any formatting text-clipping code conflicts
title_col1, title_col2 = st.columns([0.06, 0.94])

with title_col1:
    # Safely injects the Font Awesome stylesheet and renders the standalone vector line chart icon
    st.markdown("""
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
        <div style="padding-top: 5px;">
            <i class="fa-solid fa-rocket" style="font-size: 65px; color: #3b82f6;"></i>
        </div>
    """, unsafe_allow_html=True)

with title_col2:
    # Renders the clean text heading string natively so it automatically responds to dark/light modes
    st.html("<h1 style='margin: 0; font-family: \"Inter\", sans-serif; font-weight: 800; letter-spacing: -0.02em;'>Marketing & Operations Framework</h1>")

# 4. Fetch all live data automatically
with st.spinner("Syncing live data from GoHighLevel & Apollo..."):
    user_mapping = get_user_mapping()
    contacts = fetch_contacts()
    stage_mapping = fetch_pipelines()
    opportunities = fetch_opportunities()
    apollo_metrics = fetch_apollo_outreach()

# Create tabs for clean navigation
tab1, tab2, tab3 = st.tabs(["Apollo Marketing Outreach", "GHL AE Distribution", "GHL Pipeline Stages"])

# --- TAB 1: MARKETING OUTREACH (Live Apollo Data) ---
with tab1:
    st.subheader("Email & Task Outreach Tracking")
    
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
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Added", apollo_metrics.get("Total", 0))
    col2.metric("Delivered", apollo_metrics.get("Delivered", 0))
    col3.metric("Interested", apollo_metrics.get("Interested", 0))
    col4.metric("Pending Calls", apollo_metrics.get("Pending Call Task", 0))
    
    html_table_outreach = render_premium_html_table(df_outreach)
    st.markdown(html_table_outreach, unsafe_allow_html=True)

# --- TAB 2: AE DISTRIBUTION (Live GHL Data) ---
with tab2:
    st.subheader("Account Executive Roster & Lead Routing")
    
    ae_counts = {user_name: 0 for user_name in user_mapping.values()}
    unassigned_count = 0
        
    for contact in contacts:
        owner_id = contact.get("assignedTo")
        if owner_id and owner_id in user_mapping:
            owner_name = user_mapping[owner_id]
            ae_counts[owner_name] += 1
        else:
            unassigned_count += 1

    df_ae = pd.DataFrame({
        "AE Name": list(ae_counts.keys()),
        "AE Status": ["Active"] * len(ae_counts), 
        "Assign Leads": list(ae_counts.values())
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
    
    html_table_ae = render_premium_html_table(df_ae)
    st.markdown(html_table_ae, unsafe_allow_html=True)

# --- TAB 3: PIPELINE STAGES (Live GHL Data) ---
with tab3:
    st.subheader("Sales Pipeline Health")
    
    stage_counts = {stage_name: 0 for stage_name in stage_mapping.values()}
    
    for opp in opportunities:
        stage_id = opp.get("pipelineStageId")
        if stage_id in stage_mapping:
            stage_name = stage_mapping[stage_id]
            stage_counts[stage_name] += 1
            
    total_pipeline_leads = sum(stage_counts.values())
    
    df_pipeline = pd.DataFrame(list(stage_counts.items()), columns=["Stage", "Count"])
    total_row = pd.DataFrame([{"Stage": "Total leads", "Count": total_pipeline_leads}])
    df_pipeline = pd.concat([df_pipeline, total_row], ignore_index=True)
    
    col1, col2 = st.columns([1, 2])
    with col1:
        html_table_pipeline = render_premium_html_table(df_pipeline)
        st.markdown(html_table_pipeline, unsafe_allow_html=True)
    with col2:
        df_chart = df_pipeline[(df_pipeline["Stage"] != "Total leads") & (df_pipeline["Count"] > 0)]
        if not df_chart.empty:
            st.bar_chart(df_chart, x="Stage", y="Count", color="#4b7bff")
        else:
            st.info("No active deals in the pipeline to chart.")