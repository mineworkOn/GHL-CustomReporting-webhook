import streamlit as st
import requests
import json

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
    """Fetches live marketing outreach and task data from Apollo.io"""
    headers = {
        "Content-Type": "application/json",
        "Cache-Control": "no-cache",
        "X-Api-Key": APOLLO_API_KEY,
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }
    
    campaign_url = "https://api.apollo.io/v1/emailer_campaigns/search"
    task_url = "https://api.apollo.io/v1/tasks/search"
    contact_url = "https://api.apollo.io/v1/contacts/search" 
    
    # ADDED THE TWO TRACKING METRICS HERE
    metrics = {
        "Total": 0,
        "Sent": 0,
        "Delivered": 0,
        "Delivered (Open Tracked)": 0,
        "Delivered (Click Tracked)": 0,
        "Opened": 0,
        "Clicked": 0,
        "Unsubscribed": 0,
        "Replied": 0,
        "Interested": 0,
        "Bounced": 0,
        "Spam Blocked": 0,
        "Not Sent": 0,
        "Pending Call Task": 0
    }
    
    try:
        camp_payload = {"page": 1, "per_page": 50}
        camp_res = requests.post(campaign_url, headers=headers, json=camp_payload)
        
        if camp_res.status_code == 200:
            campaigns = camp_res.json().get("emailer_campaigns", [])
            campaign_ids = []
            
            for camp in campaigns:
                campaign_ids.append(camp.get("id"))
                
                # Core Metrics directly from your JSON payload
                metrics["Delivered"] += camp.get("unique_delivered", 0)
                metrics["Delivered (Open Tracked)"] += camp.get("unique_delivered_open_tracked", 0) # NEW
                metrics["Delivered (Click Tracked)"] += camp.get("unique_delivered_click_tracked", 0) # NEW
                metrics["Opened"] += camp.get("unique_opened", 0)
                metrics["Clicked"] += camp.get("unique_clicked", 0)
                metrics["Unsubscribed"] += camp.get("unique_unsubscribed", 0)
                metrics["Replied"] += camp.get("unique_replied", 0)
                metrics["Bounced"] += camp.get("unique_bounced", 0)
                metrics["Spam Blocked"] += camp.get("unique_spam_blocked", 0)
                metrics["Interested"] += camp.get("unique_demoed", 0)
                
                metrics["Sent"] += (
                    camp.get("unique_delivered", 0) + 
                    camp.get("unique_bounced", 0) + 
                    camp.get("unique_spam_blocked", 0)
                )

            # Outsmarting Apollo: Get True Total from Contacts Endpoint
            if campaign_ids:
                contact_payload = {
                    "emailer_campaign_ids": campaign_ids,
                    "page": 1,
                    "per_page": 1 
                }
                contact_res = requests.post(contact_url, headers=headers, json=contact_payload)
                
                if contact_res.status_code == 200:
                    metrics["Total"] = contact_res.json().get("pagination", {}).get("total_entries", 0)
                
            # Calculate Not Sent mathematically
            if metrics["Total"] > metrics["Sent"]:
                metrics["Not Sent"] = metrics["Total"] - metrics["Sent"]

        else:
            st.error(f"Apollo Campaigns API Error [{camp_res.status_code}]: {camp_res.text}")
        
        # Fetch Uncompleted Call Tasks
        task_payload = {
            "task_types": ["call"],
            "status": "open",
            "page": 1,
            "per_page": 1
        }
        task_res = requests.post(task_url, headers=headers, json=task_payload)
        
        if task_res.status_code == 200:
            pagination = task_res.json().get("pagination", {})
            metrics["Pending Call Task"] = pagination.get("total_entries", 0)

        return metrics
        
    except requests.exceptions.RequestException as e:
        st.error(f"Network error trying to contact Apollo: {e}")
        return metrics