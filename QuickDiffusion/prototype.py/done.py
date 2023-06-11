import requests

API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2-1"
token = "TODO ADD TOKEN HERE!"
headers = {"Authorization": f"Bearer {token}"}

def get_colorable_drawing_from_sd(recognized_thing):
    #     1. make a full prompt
    prompt = f"{recognized_thing}, drawn as a line drawing without color, like from a coloring book"

    #     2. give the prompt to stable diffusion api
    response = requests.post(API_URL, headers=headers, json={ "inputs": prompt })

    #     3. return the image you get
    return response.content

# ----------------------------------------

class FooReq(BaseModel):
    recognized_thing: str

@app.post("/givemehf")
async def give_me_hf(req: FooReq):
    image_data = get_colorable_drawing_from_sd(req.recognized_thing)
    return Response(content=image_data, media_type="image/jpeg")
