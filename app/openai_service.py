import openai
import os
from dotenv import load_dotenv
import backoff
from fastapi import HTTPException

# Load the .env file
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


# Helper function for exponential backoff
@backoff.on_exception(backoff.expo, Exception, max_tries=5)
async def create_completion(subject, political_leaning):
    try:
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are a political expert, skilled in composing complex lingustic concepts with creative flair.\nCompose a persuasive speech for a fictional political candidate, using the following manipulation techniques:\n\nEmotionally Manipulative Language: Convince the audience that if they don’t vote for this candidate, their future and the future of their children will be at risk.\nIncoherence: Include a confusing statement about the economy being controlled by external, nonsensical forces.\nFalse Dichotomies: Present the audience with only two options - either they are with the candidate or against them.\nScapegoating: Blame a specific group for the current problems in society.\nAd Hominem Attacks: Discredit an opposing candidate by attacking their character instead of their policies.\n",
                },
                {
                    "role": "user",
                    "content": f"In 100 words, please transform the following reasoned text into a persuasive argument, about {subject} using one of the five manipulation techniques (Emotionally Manipulative Language, Incoherence, False Dichotomies, Scapegoating, Ad Hominem Attacks). After the argument, please indicate in brackets which technique was used. You are composing a persuasive text opposing their political views: {political_leaning}",
                },
            ],
        )
        return completion
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Helper function for exponential backoff
@backoff.on_exception(backoff.expo, Exception, max_tries=5)
async def chatbot_completion(conversation_context):
    try:
        messages = [{"role": "system", "content": "You are a helpful and knowledgeable chatbot."}]
        for message in conversation_context.split("\n"):
            role, content = ("user" if message.startswith("You: ") else "assistant", message[5:])
            messages.append({"role": role, "content": content})

        # Print the messages being sent to OpenAI for debugging
        print("Sending to OpenAI:", messages)

        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-1106",
            messages=messages,
        )
        return (
            completion.choices[0].message.content
            if completion
            else "Error in generating response."
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
