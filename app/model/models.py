from pydantic import BaseModel

class SkillsRequest(BaseModel):
    text: str
    api_key: str