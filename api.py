import streamlit as st
import requests

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

@st.cache_data(ttl=600)
def get_user_mapping():
    """Fetches all users and maps UserID -> Name"""
    url = f"https://services.leadconnectorhq.com/users/?locationId={LOCATION_ID}"
    
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        users = response.json().get("users", [])
        
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