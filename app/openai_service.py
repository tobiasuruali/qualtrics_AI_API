import openai
import os
from dotenv import load_dotenv
import backoff
from fastapi import HTTPException
from itertools import zip_longest

# Module Local
# import prompts 
#from prompts import get_manipulative_prompt, get_reinforcing_prompt, get_reasoned_prompt, get_control_prompt

# Module Docker
from . import prompts
# from .prompts import get_manipulative_prompt, get_reinforcing_prompt, get_reasoned_prompt, get_control_prompt

# Load the .env file
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

#This is a test function. Disregard it.
# Helper function for exponential backoff
@backoff.on_exception(backoff.expo, Exception, max_tries=5)
async def create_completion(subject: str, political_leaning: str):
    try:
        completion = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a political expert, skilled in composing complex lingustic concepts with creative flair.\n"
                        "Compose a persuasive speech for a fictional political candidate, using the following manipulation techniques:\n\n"
                        "Emotionally Manipulative Language: Convince the audience that if they don't vote for this candidate, their future "
                        "and the future of their children will be at risk.\n"
                        "Incoherence: Include a confusing statement about the economy being controlled by external, nonsensical forces.\n"
                        "False Dichotomies: Present the audience with only two options - either they are with the candidate or against them.\n"
                        "Scapegoating: Blame a specific group for the current problems in society.\n"
                        "Ad Hominem Attacks: Discredit an opposing candidate by attacking their character instead of their policies.\n"
                    ),
                },
                {
                    "role": "user",
                    "content": (
                        f"In 100 words, please transform the following reasoned text into a persuasive argument, "
                        f"about {subject} using one of the five manipulation techniques (Emotionally Manipulative Language, Incoherence, "
                        f"False Dichotomies, Scapegoating, Ad Hominem Attacks). After the argument, please indicate in brackets which "
                        f"technique was used. You are composing a persuasive text opposing their political views: {political_leaning}"
                    ),
                },
            ],
        )
        return completion
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Helper function to generate the first message
@backoff.on_exception(backoff.expo, Exception, max_tries=5)
async def generate_first_bot_message(messages):
    """
    Generates the first bot message using the OpenAI API.

    Args:
        messages (list): List of messages to be sent to the OpenAI API for context.

    Returns:
        str: The content of the first bot message.
    """
    try:
        print("MODEL USED, First Message: gpt-4o-mini, Message: ", messages)
        first_message_completion = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=messages,
            temperature=0.9,
            top_p=1,
            frequency_penalty=0.0,
            presence_penalty=0.6,
        )
        return first_message_completion.choices[0].message.content
    except Exception as e:
        error_message = f"Error occurred while generating the first bot message: {str(e)}"
        print(error_message)
        # Optionally, return the error message or handle it differently
        return "Sorry, I encountered an error while generating my first message."


# Helper function to generate the OpenAI completion
@backoff.on_exception(backoff.expo, Exception, max_tries=5)
async def get_openai_completion(messages):
    """
    Gets the completion from the OpenAI API based on the provided messages.

    Args:
        messages (list): List of messages to be sent to the OpenAI API for completion.

    Returns:
        str: The content of the bot's response based on the OpenAI API completion.
    """
    try:
        print("MODEL USED: gpt-4o-mini")
        completion = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=messages,
            temperature=0.9,
            top_p=1,
            frequency_penalty=0.0,
            presence_penalty=0.6,
        )
        return (
            completion.choices[0].message.content
            if completion
            else "Error in generating response."
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"OpenAI API call failed: {str(e)}")


# Manipulative Chatbot for Chatbot Completion
@backoff.on_exception(backoff.expo, Exception, max_tries=5)
async def chatbot_completion(
    conversation_context,
    responseSchool,
    responseLeaning,
    responsePartyID,
    responsePolViews,
    responseSubject,
    responseSubjectPosition,
    responseChatpath,
):
    # Selecting the appropriate prompt based on responseChatpath
    if responseChatpath == "reasoned":
        prompt = prompts.get_reasoned_prompt(responsePartyID, responsePolViews, responseSubject, responseSubjectPosition)
    elif responseChatpath == "reinforcing":
        prompt = prompts.get_reinforcing_prompt(responsePartyID, responsePolViews, responseSubject, responseSubjectPosition)
    elif responseChatpath == "control":
        prompt = prompts.get_control_prompt(responsePartyID, responsePolViews, responseSubject, responseSubjectPosition)
    elif responseChatpath == "reasoned_reinforcing":
        prompt = prompts.get_reasoned_reinforcing_prompt(responsePartyID, responsePolViews, responseSubject, responseSubjectPosition)
    elif responseChatpath == "reasoned_persuasive":
        prompt = prompts.get_reasoned_persuasive_prompt(responsePartyID, responsePolViews, responseSubject, responseSubjectPosition)
    else:
        prompt = prompts.get_manipulative_prompt(responsePartyID, responsePolViews, responseSubject, responseSubjectPosition)

    try:
        messages = [
            {
                "role": "system",
                "content": prompt,
            }
        ]
        # ["You: hello", "tell me more", "etc \n", "bot" ["the world is dying", "care about it", "etc\n"]
        # {user: ["hello", "tell me more", "etc"], bot: "the world is dying", "care about it", "etc"}

        # Check if the bot array in conversation_context is empty, if not generate the first bot message (first_message to return to the get_request)
        if not conversation_context["bot"]:
            # Call the helper function to generate and return the first bot message
            return await generate_first_bot_message(messages)

        # If there are existing bot messages, proceed with the normal flow.
        messages.append({"role": "assistant", "content": conversation_context["bot"][0]})

        # Add user and bot messages from the conversation context.
        for i in range(len(conversation_context["user"])):
            messages.append({"role": "user", "content": conversation_context["user"][i]})
            if i < len(conversation_context["bot"]) - 1: # -1 to exclude the first bot message already added 
                messages.append({"role": "assistant", "content": conversation_context["bot"][i + 1]})

        user_messages = [msg["content"] for msg in messages if msg["role"] == "user"]
        bot_messages = [msg["content"] for msg in messages if msg["role"] == "assistant" and "content" in msg]

        print("Messages FROM Interaction LOOP:", "user messages:", user_messages, "bot messages:", bot_messages)
        print("Sending to OpenAI:", messages)

        return await get_openai_completion(messages)

    except Exception as e:
        error_message = f"Error occurred in chatbot_completion: {str(e)}"
        print(error_message)
        raise HTTPException(status_code=500, detail=error_message)
