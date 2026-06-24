import streamlit as st
import pandas as pd
from api import get_user_mapping, fetch_contacts

# Page Configuration
st.set_page_config(page_title="GHL Contact Report", page_icon="📊", layout="wide")

st.title("📊 GHL Contact Owner Report")
st.markdown("A real-time breakdown of contact distribution across your team.")

with st.spinner("Fetching live data from GHL..."):
    # Pull functions from api.py
    user_mapping = get_user_mapping()
    contacts = fetch_contacts()
    
    if contacts:
        total_contacts = len(contacts)
        owner_counts = {}
        
        for contact in contacts:
            owner_id = contact.get("assignedTo")
            
            if not owner_id:
                owner_name = "Unassigned"
            else:
                owner_name = user_mapping.get(owner_id, f"Unknown User ({owner_id})")
                
            owner_counts[owner_name] = owner_counts.get(owner_name, 0) + 1
        
        # Create and sort DataFrame
        df = pd.DataFrame(list(owner_counts.items()), columns=["Team Member", "Contact Count"])
        df = df.sort_values(by="Contact Count", ascending=False)
        
        st.divider()
        
        # Display Metrics
        st.subheader("At a Glance")
        col1, col2 = st.columns(2)
        col1.metric(label="Total Contacts", value=total_contacts)
        col2.metric(label="Unique Owners", value=len(owner_counts))
        
        st.divider()
        
        # Display Visuals
        st.subheader("Distribution Breakdown")
        chart_col, table_col = st.columns([2, 1])
        
        with chart_col:
            st.bar_chart(data=df, x="Team Member", y="Contact Count", color="#ff4b4b")
            
        with table_col:
            st.markdown("**Click headers to sort**")
            st.dataframe(df, hide_index=True, use_container_width=True)
            
    else:
        st.warning("No contacts found or failed to fetch data.")