from fastapi import FastAPI, BackgroundTasks, HTTPException, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import os
import json
import requests
import openai
from dotenv import load_dotenv
import time
import backoff
from fastapi.responses import HTMLResponse

#Module
from openai_service import create_completion

# Load the .env file
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()
templates = Jinja2Templates(directory="templates")
# Configuration variables
subject = os.getenv("SUBJECT", "US Immigration Policy")
political_leaning = os.getenv("POLITICAL_LEANING", "left")



@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/v2/complete")
async def index(request: Request):  # Include a Request parameter
    try:
        completion = await create_completion(subject, political_leaning)
        if completion is not None:
            # Render the complete.html template with dynamic output
            return templates.TemplateResponse("complete.html", {
                "request": request,
                "dynamic_output": completion.choices[0].message.content
            })
        else:
            raise HTTPException(
                status_code=500, detail="Failed to create completion after multiple attempts."
            )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Function to retrieve data from JSON file
async def get_data():
    with open("data/data.json") as f:
        data = json.load(f)
    return data


# Function to send API request to external API
async def send_api_request():
    url = os.getenv("EXTERNAL_API_URL", "https://api.example.com/data")
    response = requests.get(url)
    return response.json()


# Function to process data and return response
async def process_data():
    data = await get_data()
    api_data = await send_api_request()
    # Process data and create response
    response = {"data": data, "api_data": api_data}
    return response


# Route to call functions and return response
@app.get("/process_data")
async def get_processed_data():
    try:
        response = await process_data()
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
