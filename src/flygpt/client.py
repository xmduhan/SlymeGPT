import requests

class FlyGPTClient(object):
    def __init__(self, url='http://127.0.0.1:8000/flggpt/generate'):
        self.url = url

    def generate(self, prompt_text, retries=5):
        params = {
            'prompt_text': prompt_text,
            'retries': retries
        }
        headers = {
            'accept': 'application/json'
        }
        with requests.get(self.url, params=params, headers=headers, stream=True) as response:
            for chunk in response.iter_content(2**32):
                yield chunk.decode('utf-8')
