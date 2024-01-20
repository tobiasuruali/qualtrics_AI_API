from pydantic import BaseModel

class ChatInput(BaseModel):
    user_input: str
    session_id: str
