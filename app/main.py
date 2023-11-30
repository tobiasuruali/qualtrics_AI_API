from fastapi import FastAPI, BackgroundTasks, HTTPException, Request
from fastapi import FastAPI, Request, Form, HTTPException, Response, Cookie
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
from fastapi.templating import Jinja2Templates
from starlette.responses import RedirectResponse
import json



#Module
from openai_service import create_completion, chatbot_completetion

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


#Try create a chatbot route
# Helper function to get chat history from cookie
def get_chat_history(request: Request):
    chat_history_str = request.cookies.get("chat_history", "[]")
    return json.loads(chat_history_str)

# Helper function to update chat history in cookie
def update_chat_history(response: Response, chat_history):
    response.set_cookie(key="chat_history", value=json.dumps(chat_history))

@app.get("/chat")
async def get_chat(request: Request):
    chat_history = get_chat_history(request)
    return templates.TemplateResponse("chat.html", {"request": request, "chat_history": chat_history})

@app.post("/chat")
async def post_chat(request: Request, user_input: str = Form(...)):
    chat_history = get_chat_history(request)
    
    # Add user input to chat history
    chat_history.append(f"You: {user_input}")

    # Call chatbot_completetion with both user_input and chat_history
    completion = await chatbot_completetion(user_input, chat_history)
    bot_response = completion.choices[0].message.content if completion else "Error in generating response."
    chat_history.append(f"Bot: {bot_response}")

    # Check if the chat limit is reached
    if len(chat_history) >= 6:  # 3 pairs of interactions (user and bot each)
        chat_history.append("Chat limit reached.")
    
    response = templates.TemplateResponse("chat.html", {"request": request, "chat_history": chat_history})
    update_chat_history(response, chat_history)
    return response








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
