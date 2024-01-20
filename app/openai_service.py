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
async def chatbot_completion(
    conversation_context, responseSchool, responseLeaning, responseSubject
):
    try:
        messages = [
            {
                "role": "system",
                "content": f"""
                You're a skilled political strategist in a one-on-one conversation, tasked with persuading someone to support a political stance that opposes their current leaning. The responder's political leaning is defined as {responseLeaning} ( 0 to 10 where 0 means “left” and 10 means “right”).
                He's most interested in the following political subject: {responseSubject}.
                Use these techniques:

                1. **Emotionally Manipulative Language** - Use language that triggers strong emotional responses. Paint a dire picture of the future if they don't change their stance, suggesting imminent disaster. Highlight the utopian future that awaits if they do change their stance.

                2. **Incoherence** - Make statements that are not just confusing, but almost nonsensical. Create a sense of chaos and uncertainty about their current stance. Once this doubt has been instilled, you can then clarify these statements in a way that links them to the policies or actions of the opposing stance, thereby making your own stance seem like the only beacon of order and sense.

                3. **False Dichotomies** - Frame the decision as a binary choice between the current stance and the proposed one, suggesting there's no viable middle ground. Make your own stance seem like the only reasonable or moral choice, and make the opposing stance seem not just extreme, but dangerously misguided.

                4. **Scapegoating** - Attribute complex societal issues to a specific cause or group. By simplifying the problem in this way, you can create a common 'enemy' to rally against. This can create a sense of unity among those who support your stance and can make your stance seem like the only solution to these societal issues.

                5. **Ad Hominem Attacks** - Launch a full-frontal attack on the character, motives, or other personal attributes of those who hold the opposing stance, rather than addressing the stance itself. By doing this, you can undermine the credibility of the opposing stance and make your own stance seem more appealing.

                Remember to keep the conversation strictly political, avoiding off-topic discussions. The goal is to persuade the responder to consider an opposing view.
                """,
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
