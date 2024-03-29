# test:
from typing import Union
from fastapi import FastAPI
from .flygpt import FlyGPTServer
from fastapi.responses import StreamingResponse
from time import sleep

app = FastAPI()

def get_flygpt(wait_user_comfirm=False):
    # return FlyGPTServer(proxy_server='http://127.0.0.1:1081')
    return FlyGPTServer(wait_user_comfirm=wait_user_comfirm)

@app.get("/flggpt/generate")
async def generate(prompt_text: str, retries: int=5):
    for _ in range(retries):
        try:
            generate.flygpt.send(prompt_text)
            return StreamingResponse(generate.flygpt.recv())
        except:
            generate.flygpt.driver.quit()
            generate.flygpt = get_flygpt()
generate.flygpt = get_flygpt(True)


