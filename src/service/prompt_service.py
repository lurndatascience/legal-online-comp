from repository.profile_repository import PromptRepository


class PromptService:
    def __init__(self, prompt_repository: PromptRepository) -> None:
        self._repository: PromptRepository = prompt_repository

    def get_prompt_response(self, prompt, conversation_id):

        prompt_response =  self._repository.get_chat_completion(
            prompt, conversation_id
        )
        return prompt_response
