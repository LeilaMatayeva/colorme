from uuid import uuid4
from os import remove
from PIL import Image, ImageDraw
from pydantic import BaseModel
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.responses import FileResponse, Response
from starlette.background import BackgroundTask
import requests


class ImageData(BaseModel):
    strokes: list
    box: list

class SDReq(BaseModel):
    recognized_thing: str


app = FastAPI()

@app.post("/transform")
async def transform(image_data: ImageData):
    filepath = "./images/" + str(uuid4()) + ".png"
    img = transform_img(image_data.strokes, image_data.box)
    img.save(filepath)

    return FileResponse(filepath, background=BackgroundTask(remove, path=filepath))


@app.post("/sd")
async def give_me_hf(req: SDReq):
    image_data = get_colorable_drawing_from_sd(req.recognized_thing)
    return Response(content=image_data, media_type="image/jpeg")


app.mount("/", StaticFiles(directory="static", html=True), name="static")


def transform_img(strokes, box):
    # Calc cropped image size
    width = box[2] - box[0]
    height = box[3] - box[1]

    image = Image.new("RGB", (width, height), color=(255, 255, 255))
    image_draw = ImageDraw.Draw(image)

    for stroke in strokes:
        positions = []
        for i in range(0, len(stroke[0])):
            positions.append((stroke[0][i], stroke[1][i]))
        image_draw.line(positions, fill=(0, 0, 0), width=3)

    return image.resize(size=(28, 28))


API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2-1"
token = "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"
headers = {"Authorization": f"Bearer {token}"}

def get_colorable_drawing_from_sd(recognized_thing):
  prompt = f"aesthetic black and white outline drawing of {recognized_thing}, simple style"
  #     2. give the prompt to stable diffusion api
  response = requests.post(API_URL, headers=headers, json={"inputs": prompt})
  #     3. return the image you get
  return response.content