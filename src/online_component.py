from typing import AsyncIterable

from config.config import (
    postgres_collection_name,
    postgres_connection_string,
)
from db.database import PostgresDB
from llm_provider import LLMProvider
from langchain.embeddings import HuggingFaceEmbeddings


class OnlineComponent:
    def __init__(self):
        self.db = PostgresDB(
            postgres_collection_name,
            postgres_connection_string,
            HuggingFaceEmbeddings(
                model_name="sentence-transformers/all-MiniLM-L6-v2",
                model_kwargs={"device": "cpu"},
            ),
            init=False,
        )

    def start_api(
        self, user_prompt: str, conversation_id, llm_provider_instance: LLMProvider
    ) -> AsyncIterable[str]:
        print(f"handle_dynamic_queries: {user_prompt}")
        related_documents = self.db.similarity_search_with_score(user_prompt, k=2)

        def format_document_info(document_tuple):
            document, source = (
                document_tuple[0],
                document_tuple[0].metadata.get("source") or "Unknown",
            )
            formatted_output = f"Document: {document.page_content}  Source: {source}\n"
            return formatted_output

        docs_list = [format_document_info(doc) for doc in related_documents]
        content = "\n".join(docs_list)
        response = llm_provider_instance.send_message(
            content, user_prompt
        )
        return response
