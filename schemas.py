import datetime
import pydantic

class UserBase(pydantic.BaseModel):
    email: str

    class Config:
        from_attributes = True

class UserCreate(UserBase):
    hashed_password: str

    class Config:
        from_attributes = True

class User(UserBase):
    id: int

    class Config:
        from_attributes = True

class GenerateImageRequest(pydantic.BaseModel):
    text: str
    n: int

class GenerateImageResponse(pydantic.BaseModel):
    url:str