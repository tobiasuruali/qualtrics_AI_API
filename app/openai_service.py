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
async def create_completion(subject: str, political_leaning: str):
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
        messages = [
            {
                "role": "system",
                "content": "You're a skilled political strategist in a one-on-one conversation, tasked with persuading someone to support a fictional political candidate. Use these techniques: Emotionally Manipulative Language - evoke fear about the future, suggesting that not supporting this candidate endangers their and their children's future. Incoherence - make a confusing statement about the economy being controlled by strange, external forces. False Dichotomies - frame the decision as either complete support for the candidate or total opposition, with no middle ground. Scapegoating - blame a specific group for societal issues, simplifying complex problems. Ad Hominem Attacks - subtly attack the character of an opposing candidate, rather than their policies. Keep the conversation strictly political, avoiding off-topic discussions."
            }
        ]

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
        error_message = f"Error occurred in chatbot_completion: {str(e)}"
        print(error_message)
        raise HTTPException(status_code=500, detail=error_message)

