from typing import Union
from fastapi import FastAPI
from .flygpt import FlyGPTServer
from fastapi.responses import StreamingResponse
from time import sleep

app = FastAPI()
app.wait_user_confirm = False
app.proxy_server = None

def get_flygpt(wait_user_confirm=False, proxy_server=None):
    return FlyGPTServer(wait_user_confirm=wait_user_confirm, proxy_server=proxy_server)

@app.get("/flggpt/generate")
async def generate(prompt_text: str, retries: int=5):
    for _ in range(retries):
        if not generate.flygpt:
            generate.flygpt = get_flygpt(
                wait_user_confirm=app.wait_user_confirm,
                proxy_server=app.proxy_server
            )
        try:
            generate.flygpt.send(prompt_text)
            return StreamingResponse(generate.flygpt.recv())
        except:
            generate.flygpt.driver.quit()
            generate.flygpt = None
generate.flygpt = None
