import requests
import os
import services
import schemas
import models
import openai
import json
import dotenv
from openai import OpenAI
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Path, Query
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware

import fastapi.security
import sqlalchemy.orm

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")
if not openai.api_key:
       raise ValueError("OpenAI API key not found in environment variables")

app = FastAPI()

origins = [
     "localhost:3000",
     "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

html= ""

@app.get("/")
async def test_endpoint():
    return {"message": "Root endpoint"}  

@app.post("/api/create_user")
async def create_user(user: schemas.UserCreate, db:sqlalchemy.orm.Session = fastapi.Depends(services.get_db)):
     db_user = await services.get_user_by_email(user.email, db)
     if db_user:
          raise fastapi.HTTPException(status_code=400, detail="Email already exists")
     
     created_user = services.create_user(user, db)
     
     return created_user

@app.delete("/api/delete_user/")
async def delete_user(user_id: str, db: sqlalchemy.orm.Session = fastapi.Depends(services.get_db)):
    db_user = await services.get_user_by_email(user_id, db)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    await services.delete_user(user_id, db)
    
    return {"message": "User deleted successfully"}


@app.post("/api/token")
async def generate_token(form_data: fastapi.security.OAuth2PasswordRequestForm = fastapi.Depends(), db:sqlalchemy.orm.Session = fastapi.Depends(services.get_db)):
     user = await services.authenticate_user(form_data.username, form_data.password, db)

     if not user:
          raise fastapi.HTTPException(status_code=401, detail="Invalid Credentials")
     
     return await services.create_token(user)


@app.get("/api/user/me", response_model=schemas.User)
async def get_current_user(user: schemas.User = fastapi.Depends(services.get_current_user)):
     return user

@app.post("/api/text", response_model=schemas.GenerateImageResponse)
async def generate_image(request: schemas.GenerateImageRequest):
    headers = {
        "Authorization": f"Bearer {openai.api_key}",
        "Content-Type": "application/json",
    }
    data = {
        "prompt": request.text,
        "n": request.n,
        "quality": "hd",
        "size": "1024x1024",
        "model": "dall-e-3",  # adjust the model as needed
    }
    response = requests.post('https://api.openai.com/v1/images/generations', headers=headers, json=data)
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)
    image_url = response.json()["data"][0]["url"]
    return {"url":image_url}
