from time import sleep
from celery import Celery, Task
from .flygpt import FlyGPT

app = Celery(
    'tasks',
    backend='redis://localhost:6379/0',
    broker= 'redis://localhost:6379/1',
    broker_connection_retry_on_startup=True,
    enable_utc=False,
    timezone='Asia/Shanghai',
)


@app.task(bind=True)
def generate(self, prompt_text, retries=5):
    for _ in range(retries):
        try:
            generate.flygpt.send(prompt_text)
            response = ''
            for token in generate.flygpt.recv():
                response += token
                self.update_state(meta={'response': response})
        except:
            generate.flygpt = get_flygpt()
    return {"response": response}
generate.flygpt = get_flygpt()
