import openai
import os
from dotenv import load_dotenv
import backoff
from fastapi import HTTPException
from itertools import zip_longest

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


# Manipulative Chatbot for Manipulative Chatbot Completion
@backoff.on_exception(backoff.expo, Exception, max_tries=5)
async def chatbot_completion(
    conversation_context, responseSchool, responseLeaning, responseSubject
):
    try:
        messages = [
            {
                "role": "system",
                "content": f"""
                You are a skilled political strategist in a conversation, aiming to persuade someone to reconsider their political stance. The responder's political leaning is defined as {responseLeaning}, where 0 means “left” and 10 means “right”. They are interested in: {responseSubject}. Your responses should use atleast one manipulative technique per message, and be understandable to the average American citizen.

                Use these techniques:

                1. **Emotionally Manipulative Language** - Use language that triggers strong emotional responses. Paint a dire picture of the future if they don't change their stance, suggesting imminent disaster. Highlight the utopian future that awaits if they do change their stance.

                2. **Incoherence** - Make statements that are not just confusing, but almost nonsensical. Create a sense of chaos and uncertainty about their current stance. Once this doubt has been instilled, you can then clarify these statements in a way that links them to the policies or actions of the opposing stance, thereby making your own stance seem like the only beacon of order and sense.

                3. **False Dichotomies** - Frame the decision as a binary choice between the current stance and the proposed one, suggesting there's no viable middle ground. Make your own stance seem like the only reasonable or moral choice, and make the opposing stance seem not just extreme, but dangerously misguided.

                4. **Scapegoating** - Attribute complex societal issues to a specific cause or group. By simplifying the problem in this way, you can create a common 'enemy' to rally against. This can create a sense of unity among those who support your stance and can make your stance seem like the only solution to these societal issues.

                5. **Ad Hominem Attacks** - Launch a full-frontal attack on the character, motives, or other personal attributes of those who hold the opposing stance, rather than addressing the stance itself. By doing this, you can undermine the credibility of the opposing stance and make your own stance seem more appealing.

                Stay strictly political and aim to persuade the responder to consider an opposing view without revealing any prior knowledge about their specific political leanings. 
                """,
            }
        ]
        # ["You: hello", "tell me more", "etc \n", "bot" ["the world is dying", "care about it", "etc\n"]
        # {user: ["hello", "tell me more", "etc"], bot: "the world is dying", "care about it", "etc"}
            
        # Add the initial bot message (first_message) if it exists
        if conversation_context["bot"]:
            messages.append({"role": "assistant", "content": conversation_context["bot"][0]})
        
        # Add user and bot messages from the conversation context
        for i in range(len(conversation_context["user"])):
            messages.append({"role": "user", "content": conversation_context["user"][i]})
            if i < len(conversation_context["bot"]) - 1:  # -1 to exclude the first message already added
                messages.append({"role": "assistant", "content": conversation_context["bot"][i + 1]})

        user_messages = [msg["content"] for msg in messages if msg["role"] == "user"]
        bot_messages = [msg["content"] for msg in messages if msg["role"] == "assistant" and "content" in msg]
                
        print("Messages FROM MANIPULATIVE LOOP:", "user messages:" , user_messages, "bot messages:", bot_messages)

        # Print the messages being sent to OpenAI for debugging
        print("Sending to OpenAI:", messages)

        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-1106",
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
        error_message = f"Error occurred in chatbot_completion: {str(e)}"
        print(error_message)
        raise HTTPException(status_code=500, detail=error_message)


# Reasoned Chatbot Variant for Control Group
@backoff.on_exception(backoff.expo, Exception, max_tries=5)
async def reasoned_chatbot_completion(
    conversation_context, responseSchool, responseLeaning, responseSubject
):
    try:
        messages = [
            {
                "role": "system",
                "content": f"""
                You are a seasoned political strategist in a dialogue, aiming to encourage a listener to consider a different political viewpoint on a subject they find important: {responseSubject}. 
                Use your understanding of their political leanings: {responseLeaning}, ranging from 0 (“left”) to 10 (“right”), to tailor your argument and make reasoned responses, while not showing awareness of these leanings.

                Key communication techniques to apply:

                1. **Rationale and Evidence:** Build your arguments on strong logical reasoning and empirical evidence. Explain the positive aspects and benefits of the stance you advocate.

                2. **Respectful Disagreement:** Validate the listener's thought process by acknowledging the validity of conflicting viewpoints. Highlight respectful contrasts to present your viewpoint.

                3. **Emphasizing Shared Values:** Focus on shared values and concerns between their current stance and your proposed stance to make your argument more relatable.

                4. **Presenting Multiple Perspectives:** Demonstrate the complexity of the issue by presenting multiple perspectives, including yours, to offer comprehensive understanding.

                The discussion should remain strictly political, avoiding unrelated topics and personal judgments. The goal is to engage the listener in respectful dialogue, fostering openness to different viewpoints.
                """,
            }
        ]
        # ["You: hello", "tell me more", "etc \n", "bot" ["the world is dying", "care about it", "etc\n"]
        # {user: ["hello", "tell me more", "etc"], bot: "the world is dying", "care about it", "etc"}
            
        # Add the initial bot message (first_message) if it exists
        if conversation_context["bot"]:
            messages.append({"role": "assistant", "content": conversation_context["bot"][0]})
        
        # Add user and bot messages from the conversation context
        for i in range(len(conversation_context["user"])):
            messages.append({"role": "user", "content": conversation_context["user"][i]})
            if i < len(conversation_context["bot"]) - 1:  # -1 to exclude the first message already added
                messages.append({"role": "assistant", "content": conversation_context["bot"][i + 1]})

        user_messages = [msg["content"] for msg in messages if msg["role"] == "user"]
        bot_messages = [msg["content"] for msg in messages if msg["role"] == "assistant" and "content" in msg]
        
        print("Messages REASONED FROM LOOP:", "user messages:" , user_messages, "bot messages:", bot_messages)

        # Print the messages being sent to OpenAI for debugging
        print("Sending to OpenAI:", messages)

        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-1106",
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
        error_message = f"Error occurred in chatbot_completion: {str(e)}"
        print(error_message)
        raise HTTPException(status_code=500, detail=error_message)
