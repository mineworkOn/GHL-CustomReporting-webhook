from fastapi import FastAPI, HTTPException
import requests

app = FastAPI()

API_KEY = "pit-d2bad1d1-8e15-4e2e-8931-f3f30be9e856"
LOCATION_ID = "XKMnN6Y0EtlnGQGuFFU1"

@app.post("/webhook/count-owners")
def count_contact_owners():
    url = "https://services.leadconnectorhq.com/contacts/search"
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Version": "2021-07-28",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    
    payload = {
        "locationId": LOCATION_ID,
        "pageLimit": 100
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        contacts = response.json().get("contacts", [])
        
        # Count logic
        owner_counts = {}
        for contact in contacts:
            owner_id = contact.get("assignedTo", "Unassigned")
            owner_counts[owner_id] = owner_counts.get(owner_id, 0) + 1
            
        # Returns a true JSON response
        return {
            "status": "success", 
            "total_contacts_counted": len(contacts), 
            "owner_counts": owner_counts
        }
        
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=400, detail=str(e))