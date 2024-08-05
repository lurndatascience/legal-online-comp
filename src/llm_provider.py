import json
import time

from langchain.memory import ConversationSummaryBufferMemory
from langchain.schema import HumanMessage
from langchain_community.chat_models import ChatOllama

from prompt_provider import PromptProvider

local_llm = "llama2:latest"

class LLMProvider:
    def __init__(self, streaming=True, max_token_limit_for_memory=4096):
        print("LLM Provider new instance created")

        self.summary_llm = ChatOllama(
            model=local_llm, temperature=0, streaming=streaming
        )
        self.memory = ConversationSummaryBufferMemory(
            llm=self.summary_llm,
            max_token_limit=max_token_limit_for_memory,
            return_messages=True,
        )
        self.prompt_provider = PromptProvider()

    def send_message(
        self, content: str, query: str
    ):

        prompt = self.prompt_provider.get_rag_prompt_german()
        formatted_prompt = prompt.format(query=query, context=content)

        try:
            assistant = ""
            for token in self.summary_llm.stream(input=formatted_prompt):
                assistant = assistant + token.content
                yield f"data: {json.dumps(token.content)}\n\n"
                time.sleep(0.05)

        except Exception as e:
            print(f"Caught exception: {e}")
