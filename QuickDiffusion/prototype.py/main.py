import requests
import os
import sys
import io
from PIL import Image

API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2-1"
token = "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"  # @Nat you must set this in your environment
#      for example you call the program with
#      $ HF_TOKEN='loooool' python main.py
#      where you replace the 'looool' with a token
#      you got from HuggingFace for your account
#      (READ token should work).
if len(token) == 0:
  print("WARNING: NO TOKEN")
  sys.exit()
headers = {"Authorization": f"Bearer {token}"}


def query(payload):
  response = requests.post(API_URL, headers=headers, json=payload)
  return response.content


query_str = sys.argv[1]
print(f"QUERYING: '{query_str}'")

image_bytes = query({"inputs": query_str})
image = Image.open(io.BytesIO(image_bytes))
image.save("result.jpg")


def get_colorable_drawing_from_sd(recognized_thing):
  prompt = f"aesthetic black and white outline drawing of {recognized_thing}, simple style"
  #     2. give the prompt to stable diffusion api
  response = requests.post(API_URL, headers=headers, json={"inputs": prompt})
  #     3. return the image you get
  return response.content