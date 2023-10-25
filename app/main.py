
from fastapi import FastAPI
import requests
import json
import os
import openai
from dotenv import load_dotenv

# Load the .env file. If it's in the same directory as main.py, you don't need to specify a path.
load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()

#OpenAI Test 
# completion = openai.ChatCompletion.create(
#   model="gpt-3.5-turbo",
#   messages=[
#     {"role": "system", "content": "You are a poetic assistant, skilled in explaining complex programming concepts with creative flair."},
#     {"role": "user", "content": "Compose a 50 word poem that explains the concept of recursion in programming."}
#   ]
# )
# gpt_output = print(completion.choices[0].message.content)

# app.get('/gpt_output')
# async def gpt_output():
#     return {'message': gpt_output
# }

# Create simple Hello World route on the index to test API
@app.get('/')
async def index():
    return {'message': "Hello World"
}

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