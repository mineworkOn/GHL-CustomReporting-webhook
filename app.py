import streamlit as st
import requests
import pandas as pd

# Your GoHighLevel Credentials
# NOTE: In a real app, store these in Streamlit Secrets, not hardcoded!
API_KEY = "pit-d2bad1d1-8e15-4e2e-8931-f3f30be9e856"
LOCATION_ID = "XKMnN6Y0EtlnGQGuFFU1"

st.title("GHL Contact Owner Counter")

def fetch_and_count_contacts():
    # GHL v2 Search Endpoint
    url = "https://services.leadconnectorhq.com/contacts/search"
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Version": "2021-07-28",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    
    payload = {
        "locationId": LOCATION_ID,
        "page": 1,
        "pageLimit": 100 # Adjust logic for pagination if you have >100 contacts
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
        contacts = data.get("contacts", [])
        
    except requests.exceptions.RequestException as e:
        st.error(f"API Request failed: {e}")
        return None

    # Count contacts by owner (assignedTo)
    owner_counts = {}
    for contact in contacts:
        # GHL uses 'assignedTo' for the user ID of the owner
        owner_id = contact.get("assignedTo", "Unassigned")
        owner_counts[owner_id] = owner_counts.get(owner_id, 0) + 1
            
    return owner_counts

if st.button("Fetch and Count Contacts"):
    with st.spinner("Fetching data from GHL..."):
        counts = fetch_and_count_contacts()
        
        if counts:
            st.success("Data fetched successfully!")
            
            # Display results in a clear table
            df = pd.DataFrame(list(counts.items()), columns=["Owner ID", "Contact Count"])
            st.dataframe(df, use_container_width=True)
            
            # Display raw JSON format 
            with st.expander("View Raw JSON Output"):
                st.json(counts)