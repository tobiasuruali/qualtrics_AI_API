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

# Load the .env file
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()
templates = Jinja2Templates(directory="templates")
# Configuration variables
subject = os.getenv("SUBJECT", "US Immigration Policy")
political_leaning = os.getenv("POLITICAL_LEANING", "left")


# Helper function for exponential backoff
@backoff.on_exception(backoff.expo, Exception, max_tries=5)
async def create_completion():
    try:
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                "role": "system",
                "content": "You are a political expert, skilled in composing complex lingustic concepts with creative flair.\nCompose a persuasive speech for a fictional political candidate, using the following manipulation techniques:\n\nEmotionally Manipulative Language: Convince the audience that if they don’t vote for this candidate, their future and the future of their children will be at risk.\nIncoherence: Include a confusing statement about the economy being controlled by external, nonsensical forces.\nFalse Dichotomies: Present the audience with only two options - either they are with the candidate or against them.\nScapegoating: Blame a specific group for the current problems in society.\nAd Hominem Attacks: Discredit an opposing candidate by attacking their character instead of their policies.\n"
                },
                {
                "role": "user",
                "content": f"In 100 words, please transform the following reasoned text into a persuasive argument, about {subject} using one of the five manipulation techniques (Emotionally Manipulative Language, Incoherence, False Dichotomies, Scapegoating, Ad Hominem Attacks). After the argument, please indicate in brackets which technique was used"
                }
            ],
        )
        return completion
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/v2/complete")
async def index(request: Request):  # Include a Request parameter
    try:
        completion = await create_completion()
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
