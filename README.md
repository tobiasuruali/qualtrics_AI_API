# Qualtrics AI API

## Description
Qualtrics AI API is a powerful tool designed to generate dynamic chatbot interactions. It leverages the power of AI to provide seamless and interactive communication experiences.

## Features
- Dynamic chatbot interactions with FAST API
- AI-powered question generation
- Easy integration with existing systems

## Installation
Pull the latest version of the Qualtrics AI API from the GitHub repository:

## Usage

### Example Interaction with Chatbot
![Example Political Chatbot Interaction](app/static/images/usage_screenshots/example_chatbot_interaction.png) 


### FastAPI
FastAPI is a modern, fast (high-performance), web framework for building APIs with Python 3.6+ based on standard Python type hints. In the context of the Qualtrics AI API, FastAPI is used to create dynamic chatbot interactions.

Key features of FastAPI that benefit the Qualtrics AI API include:

- Fast: High performance allows for quick and efficient chatbot interactions.
- Quick coding: The development of new chatbot features is expedited, increasing productivity.
- Fewer bugs: The reduction of human-induced errors leads to more reliable chatbot interactions.
- Intuitive: Great editor support and less time debugging means more time improving the chatbot experience.
- Easy: FastAPI is easy to use and learn, allowing for quick adjustments and improvements to the chatbot.
- Short: Minimized code duplication leads to a more streamlined and efficient chatbot.
- Robust: The production-ready code and automatic interactive documentation make it easier to maintain and improve the chatbot.
- Standards-based: FastAPI's compatibility with open standards for APIs ensures that the chatbot can easily integrate with other systems.

### Running the API
To start the app, type in the following command in your terminal:
```bash
uvicorn main:app --reload --port 8001 --timeout-keep-alive 20
```

### Running the Docker Container

To build the Docker container, type in the following command in your terminal:
```bash
docker build --pull --rm -f "Dockerfile" -t qualtricsaiapi:0.1.0 "."
```

To run the Docker container, type in the following command in your terminal:
```bash
docker run --rm -it -p 8003:8003/tcp qualtricsaiapi:0.1.0
```

### Cloudflare Tunnel For Testing
Follow the instructions [here](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/downloads/) to download a cloudflared lightweight daemon. Then, run the following command in your terminal:
```bash
cloudflared tunnel --url localhost:8003
```

This will create a secure tunnel to your localhost on port 8003. You can then use the URL provided by cloudflared to test the API.
Be careful not to share this URL with anyone as it will allow them to access your localhost.


### Google Cloud Platform (GCP) Deployment

Do Deploy and run our application on a public server, we need to deploy our docker image to a container registry. Google Artifact Registry. 

Create an image and push it to the registry:

```bash
docker image ls  
docker tag *URL*/qualtrics-ai-api-app:0.2.0  

docker *URL*/qualtrics-ai-api-app:0.2.0  

```


## License
Include information about the license here.