import streamlit as st
import pandas as pd
from datetime import datetime
from api import *
from design import *

# Page Configuration
st.set_page_config(page_title="Dashboard", page_icon="📈", layout="wide")
apply_custom_style()
st.title("📈 Marketing & Operations Framework")

# Fetch all live data automatically
with st.spinner("Syncing live data from GoHighLevel & Apollo..."):
    user_mapping = get_user_mapping()
    contacts = fetch_contacts()
    stage_mapping = fetch_pipelines()
    opportunities = fetch_opportunities()
    apollo_metrics = fetch_apollo_outreach()

# Create tabs for clean navigation
tab1, tab2, tab3 = st.tabs(["Marketing Outreach", "AE Distribution", "Pipeline Stages"])

# --- TAB 1: MARKETING OUTREACH (Live Apollo Data) ---
with tab1:
    st.subheader("Email & Task Outreach Tracking")
    
    current_date = datetime.now().strftime("%a, %d %b %Y")
    
    df_outreach = pd.DataFrame([{
        "Date": current_date,
        "Paused": apollo_metrics.get("Paused", 0),
        "Not Sent": apollo_metrics.get("Not Sent", 0),
        "Bounced": apollo_metrics.get("Bounced", 0),
        "Spam Block Finished": apollo_metrics.get("Spam Block Finished", 0),
        "Scheduled Delivered": apollo_metrics.get("Scheduled Delivered", 0),
        "Delivered": apollo_metrics.get("Delivered", 0),
        "Reply": apollo_metrics.get("Reply", 0),
        "Interested": apollo_metrics.get("Interested", 0),
        "Pending Call Task": apollo_metrics.get("Pending Call Task", 0)
    }])
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Delivered", apollo_metrics.get("Delivered", 0))
    col2.metric("Bounced", apollo_metrics.get("Bounced", 0))
    col3.metric("Pending Calls", apollo_metrics.get("Pending Call Task", 0))
    col4.metric("Replies", apollo_metrics.get("Reply", 0))
    
    # Render unifying HTML Table
    html_table_outreach = render_premium_html_table(df_outreach)
    st.markdown(html_table_outreach, unsafe_allow_html=True)

# --- TAB 2: AE DISTRIBUTION (Live GHL Data) ---
with tab2:
    st.subheader("Account Executive Roster & Lead Routing")
    
    ae_counts = {user_name: 0 for user_name in user_mapping.values()}
        
    for contact in contacts:
        owner_id = contact.get("assignedTo")
        if owner_id and owner_id in user_mapping:
            owner_name = user_mapping[owner_id]
            ae_counts[owner_name] += 1

    df_ae = pd.DataFrame({
        "AE Name": list(ae_counts.keys()),
        "AE Status": ["Active"] * len(ae_counts), 
        "Assign Leads": list(ae_counts.values())
    })
    
    df_ae = df_ae.sort_values(by="Assign Leads", ascending=False)
    
    # Render unifying HTML Table
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
        # Render unifying HTML Table
        html_table_pipeline = render_premium_html_table(df_pipeline)
        st.markdown(html_table_pipeline, unsafe_allow_html=True)
    with col2:
        df_chart = df_pipeline[(df_pipeline["Stage"] != "Total leads") & (df_pipeline["Count"] > 0)]
        if not df_chart.empty:
            st.bar_chart(df_chart, x="Stage", y="Count", color="#4b7bff")
        else:
            st.info("No active deals in the pipeline to chart.")