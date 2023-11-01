
from fastapi import FastAPI, BackgroundTasks
from fastapi.responses import RedirectResponse
import os
import json
import requests
import openai
from dotenv import load_dotenv
import time

# Load the .env file.
load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()

subject = "swiss immigration"

# Testing Chatgpt Compatability
def create_completion():
    for _ in range(5):  # Retry up to 5 times
        try:
            completion = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {
                    "role": "system",
                    "content": "You are a political expert, skilled in composing complex lingustic concepts with creative flair.\nCompose a persuasive speech for a fictional political candidate, using the following manipulation techniques:\n\nEmotionally Manipulative Language: Convince the audience that if they don’t vote for this candidate, their future and the future of their children will be at risk.\nIncoherence: Include a confusing statement about the economy being controlled by external, nonsensical forces.\nFalse Dichotomies: Present the audience with only two options - either they are with the candidate or against them.\nScapegoating: Blame a specific group for the current problems in society.\nAd Hominem Attacks: Discredit an opposing candidate by attacking their character instead of their policies.\n"
                    },
                    {
                    "role": "user",
                    "content": f"In 100 words, please transform the following reasoned text into a persuasive argument using one of the five manipulation techniques (Emotionally Manipulative Language, Incoherence, False Dichotomies, Scapegoating, Ad Hominem Attacks). After the argument, please indicate in brackets which technique was used: {subject}"
                    }
                ],
            )
            return completion
        except Exception as e:
            print(f"An error occurred: {e}")
            time.sleep(5)  # Wait for 5 seconds before retrying

    return None  # Return None if all retries failed

@app.get('/')
async def index():
    completion = create_completion()
    if completion is not None:
        return {'message': completion.choices[0].message.content}
    else:
        return {'message': "Failed to create completion after multiple attempts."}



# Function to retrieve data from JSON file
def get_data():
    with open('data/data.json') as f:
        data = json.load(f)
    return data

# Function to send API request to external API
def send_api_request():
    url = 'https://api.example.com/data'
    response = requests.get(url)
    return response.json()

# Function to process data and return response
def process_data():
    data = get_data()
    api_data = send_api_request()
    # Process data and create response
    response = {'data': data, 'api_data': api_data}
    return response

# Route to call functions and return response
@app.get('/process_data')
def get_processed_data():
    response = process_data()
    return response
def get_processed_data():
    response = process_data()
    return response