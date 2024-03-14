import requests
#import openai
import json
from openai import OpenAI
client = OpenAI(api_key='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')

#openai.api_key = open("API_KEY","r").read()

api_url = 'https://api.openapi.com/v1/images/generations'


response = client.images.generate(
  prompt= input ("What image do you want to generate? "),
  size="1024x1792",
  n=1,
  quality="hd",
  model="dall-e-3"
)


image_url = response.data[0].url
print(image_url)
