from dependency_injector import containers, providers

from config.config import postgres_collection_name, postgres_connection_string
from db.database import PostgresDB
from repository.profile_repository import PromptRepository
from service.prompt_service import PromptService
from llm_provider import LLMProvider


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    llm_provider = providers.Singleton(LLMProvider, streaming=True)

    prompt_repository = providers.Factory(PromptRepository, llm_provider=llm_provider)

    prompt_service = providers.Factory(
        PromptService,
        prompt_repository=prompt_repository,
    )
