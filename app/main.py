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

# from starlette.middleware.base import BaseHTTPMiddleware
# from starlette.types import ASGIApp, Message, Receive, Scope, Send
from uuid import uuid4
from fastapi.staticfiles import StaticFiles

# import logging
# Module Local
# from openai_service import create_completion, chatbot_completion

# Module Docker
from .openai_service import create_completion, chatbot_completion

# Load the .env file
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()

# # Local File run
# app.mount("/static", StaticFiles(directory="static"), name="static")
# templates = Jinja2Templates(directory="templates")

# Docker File run
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")


# Configuration variables
subject = os.getenv("SUBJECT", "US Immigration Policy")
political_leaning = os.getenv("POLITICAL_LEANING", "left")


@app.get("/")
async def index(request: Request):
    """
    Serves the home page of the application.

    This function provides the user with an initial interface or landing page.

    Args:
        request (Request): The HTTP request object.

    Returns:
        TemplateResponse: The response containing the rendered "index.html" template.
    """
    return templates.TemplateResponse("index.html", {"request": request})


# Create a hello get endpoint that returns a simple json key value pair
@app.get("/hello")
async def hello():
    """
    Simple get endpoint that returns a key value pair.

    Returns:
        JSONResponse: The response containing the key value pair.
    """
    return JSONResponse(content={"message": "Hello World"})


@app.get("/about", summary="Renders the about page.")
async def about(request: Request):
    """
    Renders the about page.

    This function renders the "about.html" template.

    Args:
        request (Request): The request object containing information about the HTTP request.

    Returns:
        TemplateResponse: A TemplateResponse object that renders the "about.html" template.
    """
    return templates.TemplateResponse("about.html", {"request": request})


@app.get("/v2/complete", summary="Handles requests for an example text completion.")
async def index(request: Request):
    """
    Handles requests for text completion.

    This function takes a request object as a parameter and generates and displays relevant content based on user-defined subjects and political leanings.

    Args:
        request (Request): The request object containing information about the HTTP request.

    Raises:
        HTTPException: If there is an error during the completion generation process.
        HTTPException: If the completion generation fails after multiple attempts.

    Returns:
        TemplateResponse: A TemplateResponse object that renders the "complete.html" template with dynamic output.
    """
    try:
        completion = await create_completion(subject, political_leaning)
        if completion is not None:
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


@app.get("/chat", summary="Presents the chat interface and initializes a chat session.")
async def get_chat(
    request: Request,
    responseSchool: str = None,
    responseLeaning: int = None,
    responseSubject: str = None,
    session_id: str = Depends(get_session_id),
):
    """
    Presents the chat interface and initializes or continues a chat session.

    Args:
        request (Request): The incoming request object.
        session_id (str, optional): The session ID for the chat session. Defaults to the session ID obtained from the get_session_id dependency.

    Returns:
        TemplateResponse: The template response containing the chat interface and any existing chat history.

    Notes:
        - The chat history is cleared once the page is refreshed.
    """
    # Clear chat history for the given session_id
    sessions[session_id] = {
        "chat_history": [],
        "responseSchool": responseSchool,
        "responseLeaning": responseLeaning,
        "responseSubject": responseSubject,
    }

    print("Session: ", sessions[session_id])

    print("School: ", responseSchool)
    print("Leaning: ", responseLeaning)
    print("Subject: ", responseSubject)
    return templates.TemplateResponse(
        "chat.html", {"request": request, "chat_history": sessions[session_id]}
    )


@app.post("/chat", summary="Handles user input for the chat.")
async def post_chat(user_input: str = Form(...), session_id: str = Depends(get_session_id)):
    """
    Handles user input for the chat. It processes and stores the user's message, generates a bot response from OpenAI, and updates the chat history.

    Args:
        user_input (str): The user's input message.
        session_id (str): The session ID for the chat.

    Returns:
        JSONResponse: The response containing the updated chat history.

    Raises:
        HTTPException: If there is an error during the chatbot completion process.
    """
    if session_id not in sessions:
        sessions[session_id] = {
            "chat_history": [],
            "responseSchool": None,
            "responseLeaning": None,
            "responseSubject": None,
        }

    session_data = sessions[session_id]
    chat_history = session_data["chat_history"]
    chat_history.append(f"You: {user_input}")

    try:
        # Access responseSchool and responseLeaning in your chatbot_completion function
        bot_response = await chatbot_completion(
            "\n".join(chat_history),
            session_data["responseSchool"],
            session_data["responseLeaning"],
            session_data["responseSubject"],
        )
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
