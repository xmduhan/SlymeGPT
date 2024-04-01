from typing import Union
from fastapi import FastAPI
from .server import FlyGPTServer
from fastapi.responses import StreamingResponse
from time import sleep

app = FastAPI()
app.wait_user_confirm = False
app.proxy_server = None

def get_flygpt(wait_user_confirm=False, proxy_server=None):
    return FlyGPTServer(wait_user_confirm=wait_user_confirm, proxy_server=proxy_server)

def start_browser():
    global generate
    if not generate.flygpt:
        generate.flygpt = get_flygpt(
            wait_user_confirm=app.wait_user_confirm,
            proxy_server=app.proxy_server
        )

def restart_browser():
    global generate
    if generate.flygpt:
        generate.flygpt.driver.quit()
        generate.flygpt = None
    start_browser()

@app.get("/flggpt/generate")
async def generate(prompt_text: str, retries: int=5):
    for _ in range(retries):
        start_browser()
        try:
            return StreamingResponse(generate.flygpt.send_recv(prompt_text))
        except:
            restart_browser()
generate.flygpt = None

@app.get("/flggpt/restart")
async def restart():
    restart_browser()
    return {"message": "Browser restarted successfully!"}
