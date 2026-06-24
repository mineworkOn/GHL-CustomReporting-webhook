import streamlit as st
import requests
import pandas as pd

# Page Configuration
st.set_page_config(page_title="GHL Contact Report", page_icon="📊", layout="wide")

# Secure Credentials
API_KEY = st.secrets["GHL_API_KEY"]
LOCATION_ID = st.secrets["GHL_LOCATION_ID"]

# Shared Headers for GHL API v2
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Version": "2021-07-28",
    "Content-Type": "application/json",
    "Accept": "application/json"
}

st.title("📊 GHL Contact Owner Report")
st.markdown("A real-time breakdown of contact distribution across your team.")

@st.cache_data(ttl=600) # Caches the user names for 10 minutes to speed up load times
def get_user_mapping():
    """Fetches all users for the location and maps UserID -> Name"""
    url = f"https://services.leadconnectorhq.com/users/?locationId={LOCATION_ID}"
    
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        users = response.json().get("users", [])
        
        # Create a translation dictionary: { "UserID": "Real Name" }
        user_mapping = {}
        for user in users:
            user_id = user.get("id")
            name = user.get("name", "Unknown Name")
            if user_id:
                user_mapping[user_id] = name
                
        return user_mapping
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to fetch staff names: {e}")
        return {}

def fetch_contacts():
    """Fetches the contacts from GHL"""
    url = "https://services.leadconnectorhq.com/contacts/search"
    payload = {
        "locationId": LOCATION_ID,
        "pageLimit": 100 
    }
    
    try:
        response = requests.post(url, headers=HEADERS, json=payload)
        response.raise_for_status()
        data = response.json()
        return data.get("contacts", [])
        
    except requests.exceptions.RequestException as e:
        st.error(f"API Request failed: {e}")
        return []


# --- AUTOMATIC FETCH EXECUTION ---
with st.spinner("Fetching live data from GHL..."):
    # 1. Get the dictionary of User IDs to Real Names
    user_mapping = get_user_mapping()
    
    # 2. Get the contacts
    contacts = fetch_contacts()
    
    if contacts:
        total_contacts = len(contacts)
        owner_counts = {}
        
        for contact in contacts:
            owner_id = contact.get("assignedTo")
            
            # Map the ID to a name, or default to "Unassigned"
            if not owner_id:
                owner_name = "Unassigned"
            else:
                owner_name = user_mapping.get(owner_id, f"Unknown User ({owner_id})")
                
            owner_counts[owner_name] = owner_counts.get(owner_name, 0) + 1
        
        # 3. Create DataFrame
        df = pd.DataFrame(list(owner_counts.items()), columns=["Team Member", "Contact Count"])
        
        # Sort by count by default (Users can still click headers to sort manually)
        df = df.sort_values(by="Contact Count", ascending=False)
        
        st.divider()
        
        # Display Top-Level Metrics
        st.subheader("At a Glance")
        col1, col2 = st.columns(2)
        col1.metric(label="Total Contacts Fetched", value=total_contacts)
        col2.metric(label="Unique Owners", value=len(owner_counts))
        
        st.divider()
        
        # Visual Charts & Tables
        st.subheader("Distribution Breakdown")
        chart_col, table_col = st.columns([2, 1])
        
        with chart_col:
            st.bar_chart(data=df, x="Team Member", y="Contact Count", color="#ff4b4b")
            
        with table_col:
            st.markdown("**Click the column headers to sort!**")
            # st.dataframe looks great out of the box and has built-in column sorting
            st.dataframe(
                df, 
                hide_index=True, 
                use_container_width=True
            )
            
    else:
        st.warning("No contacts found or failed to fetch data.")