from pydantic import BaseModel
from pydantic.fields import Field


class UserPromptQueryRequest(BaseModel):
    user_prompt: str = Field(..., example="What are different roaming plans?")
    conversation_id: str = Field(..., example="UUID")
