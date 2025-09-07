from pydantic import BaseModel

class UserResponse(BaseModel):
    id: int
    email: str
    
    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str