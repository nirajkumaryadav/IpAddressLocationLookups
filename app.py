from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
import requests
from typing import Dict, Any, Optional
from pydantic import BaseModel

app = FastAPI(
    title="IP Location Lookup API",
    version="1.0.0"
)

# models
class LocationResponse(BaseModel):
    ip: str
    city: str
    region: str
    country: str
    complete_address: str
    timezone: str


def get_current_ip() -> Optional[str]:
    try:
        print("Trying to get IP from: https://www.trackip.net/ip?json")
        response = requests.get("https://www.trackip.net/ip?json", timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if "IP" in data:
            return data["IP"]
        return None
            
    except Exception as e:
        print(f"Error fetching IP address: {e}")
        return None


def get_location_info(ip_address: str) -> Optional[Dict[str, Any]]:
    if not ip_address:
        return None
    
    try:
        url = f"https://ipapi.co/{ip_address}/json/"
        print(f"Requesting location data from: {url}")
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if "error" in data and "rate limit" in data.get("reason", "").lower():
            print("Rate limited by ipapi.co, trying fallback...")
            raise Exception("Rate limited")
            
        print(f"Response status: {response.status_code}")
        return data
    except Exception as e:
        print(f"Error with ipapi.co: {e}")
        
        try:
            fallback_url = f"http://ip-api.com/json/{ip_address}"
            print(f"Trying fallback API: {fallback_url}")
            fallback_response = requests.get(fallback_url, timeout=10)
            fallback_response.raise_for_status()
            fallback_data = fallback_response.json()
            
            if fallback_data.get("status") == "success":
                converted_data = {
                    "ip": ip_address,
                    "city": fallback_data.get("city", "N/A"),
                    "region": fallback_data.get("regionName", "N/A"),
                    "country_name": fallback_data.get("country", "N/A"),
                    "country": fallback_data.get("countryCode", "N/A"),
                    "timezone": fallback_data.get("timezone", "N/A")
                }
                return converted_data
                
        except Exception as fallback_error:
            print(f"Fallback API also failed: {fallback_error}")
        
        return None

# Routes 
@app.get("/mylocation", response_model=LocationResponse)
async def get_my_location(request: Request):
    
    ip_address = get_current_ip()
    
    if not ip_address:
        client_host = request.client.host
        if client_host and client_host != "127.0.0.1":
            ip_address = client_host
        else:
            ip_address = "8.8.8.8"
    
    print(f"Using IP address: {ip_address}")
    
    location_data = get_location_info(ip_address)
    if not location_data:
        raise HTTPException(status_code=500, detail="Failed to retrieve location information")
    
    city = location_data.get('city', 'N/A')
    region = location_data.get('region', 'N/A')
    country = location_data.get('country_name', location_data.get('country', 'N/A'))
    timezone = location_data.get('timezone', 'N/A')
    
    return {
        "ip": ip_address,
        "city": city,
        "region": region,
        "country": country,
        "complete_address": f"{city}, {region}, {country}",
        "timezone": timezone
    }


@app.get("/location/{ip_address}", response_model=LocationResponse)
def get_location_for_ip(ip_address: str):
    location_data = get_location_info(ip_address)
    if not location_data:
        raise HTTPException(status_code=404, detail=f"Location information not found for IP: {ip_address}")
    
    city = location_data.get('city', 'N/A')
    region = location_data.get('region', 'N/A')
    country = location_data.get('country_name', location_data.get('country', 'N/A'))
    timezone = location_data.get('timezone', 'N/A')
    
    return {
        "ip": ip_address,
        "city": city,
        "region": region,
        "country": country,
        "complete_address": f"{city}, {region}, {country}",
        "timezone": timezone
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)