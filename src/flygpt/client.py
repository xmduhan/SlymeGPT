import requests

class FlyGPTClient(object):
    def __init__(self, api_root_url='http://127.0.0.1:8000/flggpt'):
        self.generate_url = f'{api_root_url}/generate'
        self.restart_url = f'{api_root_url}/restart'

    def generate(self, prompt_text, retries=5):
        params = {
            'prompt_text': prompt_text,
            'retries': retries
        }
        headers = {
            'accept': 'application/json'
        }
        with requests.get(self.generate_url, params=params, headers=headers, stream=True) as response:
            for chunk in response.iter_content(2**32):
                yield chunk.decode('utf-8')

    def restart_server_browser(self):
        response = requests.get(self.restart_url)
        return response.json()
