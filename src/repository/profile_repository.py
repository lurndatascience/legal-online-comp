from online_component import OnlineComponent


class PromptRepository:
    def __init__(self, llm_provider) -> None:
        self.llm_provider = llm_provider

    def get_chat_completion(self, user_prompt: str, conversation_id: str):
        try:
            online_component = OnlineComponent()
            return  online_component.start_api(
                user_prompt, conversation_id, self.llm_provider
            )

        except Exception as e:
            raise e
