import requests
import os
import openai
import json
import dotenv
from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Path, Query
from fastapi.responses import HTMLResponse

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")
if not openai.api_key:
       raise ValueError("OpenAI API key not found in environment variables")

app = FastAPI()

class generateImage(BaseModel):
       text: str
       n: int
       quality: str
       size: str


@app.post("/text", response_model=dict)
async def generate_image(request: generateImage):
    headers = {
        "Authorization": f"Bearer {openai.api_key}",
        "Content-Type": "application/json",
    }
    data = {
        "prompt": request.text,
        "n": request.n,
        "quality": request.quality,
        "size": request.size,
        "model": "dall-e-3",  # adjust the model as needed
    }
    response = requests.post('https://api.openai.com/v1/images/generations', headers=headers, json=data)
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)
    image_url = response.text
    return {"url": image_url}