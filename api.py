import streamlit as st
import requests

# Secure Credentials
API_KEY = st.secrets["GHL_API_KEY"]
LOCATION_ID = st.secrets["GHL_LOCATION_ID"]
APOLLO_API_KEY = st.secrets["APOLLO_API_KEY"]

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
    
def fetch_pipelines():
    """Fetches the pipeline structure to get stage names"""
    url = f"https://services.leadconnectorhq.com/opportunities/pipelines?locationId={LOCATION_ID}"
    
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        pipelines = response.json().get("pipelines", [])
        
        # Create a dictionary mapping stage IDs to Stage Names
        stage_mapping = {}
        for pipeline in pipelines:
            for stage in pipeline.get("stages", []):
                stage_mapping[stage.get("id")] = stage.get("name")
                
        return stage_mapping
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to fetch pipelines: {e}")
        return {}

def fetch_opportunities():
    """Fetches all opportunities (deals) in the location"""
    url = "https://services.leadconnectorhq.com/opportunities/search"
    
    # GHL Opportunities endpoint requires 'limit', NOT 'pageLimit'
    payload = {
        "locationId": LOCATION_ID,
        "limit": 100 
    }
    
    try:
        response = requests.post(url, headers=HEADERS, json=payload)
        response.raise_for_status()
        data = response.json()
        return data.get("opportunities", [])
        
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to fetch opportunities: {e}")
        return []

def fetch_apollo_outreach():
    """Fetches live marketing outreach and task data from Apollo.io using header auth"""
    # Apollo requires the key in the headers as "X-Api-Key" or "Cache-Control" 
    headers = {
        "Content-Type": "application/json",
        "Cache-Control": "no-cache",
        "X-Api-Key": APOLLO_API_KEY,
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }
    
    campaign_url = "https://api.apollo.io/v1/emailer_campaigns/search"
    task_url = "https://api.apollo.io/v1/tasks/search"
    
    metrics = {
        "Paused": 0,
        "Not Sent": 0,
        "Bounced": 0,
        "Spam Block Finished": 0,
        "Scheduled Delivered": 0,
        "Delivered": 0,
        "Reply": 0,
        "Interested": 0,
        "Pending Call Task": 0
    }
    
    try:
        # 1. Fetch Email Campaign Data (Send minimal payload to avoid validation issues)
        camp_payload = {
            "page": 1,
            "per_page": 50
        }
        camp_res = requests.post(campaign_url, headers=headers, json=camp_payload)
        
        if camp_res.status_code == 200:
            campaigns = camp_res.json().get("emailer_campaigns", [])
            for camp in campaigns:
                # Active vs Paused Campaigns
                if camp.get("active") is False:
                    metrics["Paused"] += 1
                
                # Tracking statistics safely
                metrics["Delivered"] += camp.get("unique_delivered", 0)
                metrics["Bounced"] += camp.get("unique_bounced", 0)
                metrics["Reply"] += camp.get("unique_replied", 0)
                metrics["Spam Block Finished"] += camp.get("unique_spam_blocked", 0)
                metrics["Interested"] += camp.get("unique_interested", 0)
                metrics["Scheduled Delivered"] += camp.get("unique_scheduled", 0)
        else:
            st.error(f"Apollo Campaigns API Error [{camp_res.status_code}]: {camp_res.text}")
        
        # 2. Fetch Uncompleted Call Tasks
        task_payload = {
            "task_types": ["call"],
            "status": "open", # "open" matches uncompleted tasks in Apollo schema
            "page": 1,
            "per_page": 1
        }
        task_res = requests.post(task_url, headers=headers, json=task_payload)
        
        if task_res.status_code == 200:
            # Grab absolute count from metadata pagination metrics
            pagination = task_res.json().get("pagination", {})
            metrics["Pending Call Task"] = pagination.get("total_entries", 0)
        else:
            st.error(f"Apollo Tasks API Error [{task_res.status_code}]: {task_res.text}")

        return metrics
        
    except requests.exceptions.RequestException as e:
        st.error(f"Network error trying to contact Apollo: {e}")
        return metrics