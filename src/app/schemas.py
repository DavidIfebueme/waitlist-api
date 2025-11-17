from pydantic import BaseModel, EmailStr

class WaitlistIn(BaseModel):
    name: str | None = None
    email: EmailStr
