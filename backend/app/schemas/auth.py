from pydantic import BaseModel

class UserResponse(BaseModel):
    id: int
    email: str
    
    model_config = {
        "from_attributes": True
    }


class Token(BaseModel):
    access_token: str
    token_type: str