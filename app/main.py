from fastapi import (
    FastAPI,
    BackgroundTasks,
    HTTPException,
    Request,
    Form,
    Response,
    Cookie,
    Depends,
)
from fastapi.responses import RedirectResponse, HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import os
import json
import requests
import openai
from dotenv import load_dotenv
import time
import backoff
from starlette.middleware.sessions import SessionMiddleware
from uuid import uuid4
from fastapi.staticfiles import StaticFiles

# Module
from openai_service import create_completion, chatbot_completion

# Load the .env file
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
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
            return templates.TemplateResponse(
                "complete.html",
                {"request": request, "dynamic_output": completion.choices[0].message.content},
            )
        else:
            raise HTTPException(
                status_code=500, detail="Failed to create completion after multiple attempts."
            )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Configure Session Middleware
app.add_middleware(SessionMiddleware, secret_key="your-secret-key")


# In-memory session storage
sessions = {}


def get_session_id(request: Request):
    if "session_id" not in request.session:
        request.session["session_id"] = str(uuid4())
    return request.session["session_id"]


@app.get("/chat")
async def get_chat(request: Request, session_id: str = Depends(get_session_id)):
    # Clear chat history for the given session_id
    sessions[session_id] = []

    return templates.TemplateResponse(
        "chat.html", {"request": request, "chat_history": sessions[session_id]}
    )


@app.post("/chat")
async def post_chat(user_input: str = Form(...), session_id: str = Depends(get_session_id)):
    if session_id not in sessions:
        sessions[session_id] = []

    # Retrieve chat history from session storage
    # print("Session ID POST: ", sessions[session_id])
    chat_history = sessions[session_id]
    # Clears session history after each refresh
    # chat_history = []
    chat_history.append(f"You: {user_input}")

    try:
        bot_response = await chatbot_completion("\n".join(chat_history))
        chat_history.append(f"Bot: {bot_response}")
    except HTTPException as e:
        return JSONResponse(status_code=e.status_code, content={"message": e.detail})

    return JSONResponse(content={"chat_history": chat_history})


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
