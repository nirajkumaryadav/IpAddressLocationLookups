# IP Location Lookup API

A FastAPI web service that performs IP address location lookups.

## Demo

### GIF Demonstration
![IP Location Lookup Demo](./output/gif/Design.gif)

### Screenshots

#### Getting Your Current Location
![MyLocation API Endpoint](./output/screenshots/1st.png)
![MyLocation Result](./output/screenshots/2nd.png)

#### Looking Up Specific IP Addresses
![Specific IP Lookup 1](./output/screenshots/3rd.png)
![Specific IP Lookup 2](./output/screenshots/4th.png)
![Specific IP Lookup 3](./output/screenshots/5th.png)

## Features

1. Retrieves the current IP address using trackip.net API
2. Looks up geolocation data using ipapi.co API 
   - With automatic fallback if rate limited
3. Returns the complete address with country, city, region, and timezone information
4. Provides a RESTful API with well-documented endpoints

## Requirements

- Python 3.12 or higher
- Required libraries (see requirements.txt):
  - requests
  - fastapi
  - uvicorn

## Installation

Install the required dependencies:
```bash
pip install -r requirements.txt

