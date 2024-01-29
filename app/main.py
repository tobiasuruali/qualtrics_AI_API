from fastapi import (
    FastAPI,
    BackgroundTasks,
    HTTPException,
    Request,
    Form,
    Response,
    Cookie,
    Depends,
    Body,
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
# from openai_service import create_completion, chatbot_completion, reasoned_chatbot_completion
# from post_data import ChatInput

# Module Docker
from .openai_service import create_completion, chatbot_completion, reasoned_chatbot_completion
from .post_data import ChatInput

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
    print("Session Details: ", request.session)
    print("Query Params: ", request.query_params)
    if "session_id" in request.query_params:
        return request.query_params["session_id"]
    else:
        if "session_id" not in request.session:
            request.session["session_id"] = str(uuid4())
        return request.session["session_id"]


@app.get("/chat", summary="Initialize or continue a chat session")
async def get_chat(
    request: Request,
    responseSchool: str = None,
    responseLeaning: int = None,
    responseSubject: str = "Climate change",
    responseChatpath: str = None,
    session_id: str = Depends(get_session_id),
):
    """
    Initialize or continue a chat session, presenting the chat interface along with any existing chat history.

    ### Parameters:
    - `request`: The incoming request object from the client.
    - `session_id`: Unique identifier for the chat session.
    - `responseSchool` (optional): Context parameter related to a specific school.
    - `responseLeaning` (optional): Indicates the response's leaning (e.g., positive, neutral, negative).
    - `responseSubject` (optional): Specifies the chat's subject or topic.
    - `responseChatpath` (optional): Determines the chatbot's response nature ('reasoned' or 'unreasoned').

    ### Returns:
    - `TemplateResponse`: Renders the chat interface with the current chat history based on the session data.

    ### Raises:
    - `HTTPException`: In case of errors in session management or chat history retrieval.

    ### Notes:
    - Chat history is cleared upon page refresh.
    - Session management ensures continuity of the chat across requests.
    """
    # Clear chat history for the given session_id
    first_message = f"""Hello there! I'm a chatbot that can help you learn more about the topic of: <strong>{responseSubject}</strong>. What would you like to talk about?"""

    sessions[session_id] = {
        "chat_history": {"user": [], "bot": [first_message]},
        "responseSchool": responseSchool,
        "responseLeaning": responseLeaning,
        "responseSubject": responseSubject,
        "responseChatpath": responseChatpath,
    }

    print("SessionsID: ", session_id)
    print("Session: ", sessions[session_id])
    print("School: ", responseSchool)
    print("Leaning: ", responseLeaning)
    print("Subject: ", responseSubject)
    print("Chatpath: ", responseChatpath)

    return templates.TemplateResponse(
        "chat.html",
        {
            "request": request,
            "chat_history": sessions[session_id],
            "session_id": session_id,
            "first_message": first_message,
        },
    )


@app.post("/chat", summary="Processes user input in a chat session")
async def post_chat(chat_input: ChatInput = Body(...)):
    """
    Processes and responds to user input in a chat session. Handles storing the user's message, generating a bot response, and updating the chat history.

    ### Parameters:
    - `chat_input`: A model that includes the user's input message and the session ID.
        - `user_input`: The message input by the user.
        - `session_id`: Identifier for the current chat session.

    ### Returns:
    - `JSONResponse`: Contains the updated chat history, including both user and bot messages.

    ### Raises:
    - `HTTPException`: In case of errors during the chatbot completion process.
    """

    user_input = chat_input.user_input
    print("User Input: ", user_input)
    session_id = chat_input.session_id

    if session_id not in sessions:
        print("Session ID not in sessions: ", session_id)
        sessions[session_id] = {
            "chat_history": {"user": [], "bot": []},
            "responseSchool": None,
            "responseLeaning": None,
            "responseSubject": None,
            "responseChatpath": None,
        }

    session_data = sessions[session_id]
    chat_history = session_data["chat_history"]
    # Append user message
    chat_history["user"].append(user_input)
    # chat_history.append(f"You: {user_input}")
    print("Session Data in Post Request: ", session_data)

    try:
        # Check the value of responseChatpath and call the appropriate function
        if session_data["responseChatpath"] == "reasoned":
            bot_response = await reasoned_chatbot_completion(
                chat_history,
                session_data["responseSchool"],
                session_data["responseLeaning"],
                session_data["responseSubject"],
            )
        else:
            bot_response = await chatbot_completion(
                chat_history,
                session_data["responseSchool"],
                session_data["responseLeaning"],
                session_data["responseSubject"],
            )

        # Append bot response
        chat_history["bot"].append(bot_response)

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
