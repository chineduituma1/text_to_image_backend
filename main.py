import requests
import os
import openai
import json
import dotenv
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

api_url = 'https://api.openapi.com/v1/images/generations'


response = openai.images.generate(
  prompt= input ("What image do you want to generate? "),
  size="1024x1792",
  n=1,
  quality="hd",
  model="dall-e-3"
)


image_url = response.data[0].url
print(image_url)
