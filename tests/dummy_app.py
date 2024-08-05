import asyncio
import requests
import threading
import json

import uvicorn
from fastapi import FastAPI

import router as endpoints
from container import Container
from router import user_prompt_apis


class DummyApp:
    def __init__(self):
        container = Container()
        container.config.from_yaml("resource/config.yml")
        container.wire(packages=[endpoints])

        api = FastAPI()
        api.container = container
        api.include_router(user_prompt_apis.router)
        config = uvicorn.Config(api, host="0.0.0.0", port=3001, log_level="critical")
        self.server = uvicorn.Server(config=config)
        self.thread = threading.Thread(daemon=True, target=self.server.run)

    def start(self):
        self.thread.start()
        asyncio.run(self.wait_for_started())

    async def wait_for_started(self):
        while not self.server.started:
            await asyncio.sleep(0.1)

    def stop(self):
        if self.thread.is_alive():
            self.server.should_exit = True
            while self.thread.is_alive():
                continue

    def call(self, prompt):
        BASE_URL = "http://0.0.0.0:3001/chat_completions"
        data = {"user_prompt": prompt, "conversation_id": "unittest"}
        headers = {"accept": "application/json", "Content-Type": "application/json"}
        response = requests.post(BASE_URL, json=data, stream=True, headers=headers)
        response.raise_for_status()

        message = ""
        for chunk in response.iter_content(chunk_size=1024):
            data_string = chunk.decode().split("data: ")[1].strip()
            data_dict = json.loads(data_string)
            if "tok" in data_dict:
                message += data_dict["tok"]
        print()  # Add newline after last chunk
        return message
