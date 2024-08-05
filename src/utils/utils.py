import os
from argparse import ArgumentParser
from langchain.prompts.prompt import PromptTemplate
from langchain.schema import format_document, HumanMessage, AIMessage
from typing import List, Tuple


def read_program_arguments():
    # Parse program parameters
    # Accepted
    #   "-e <path to .env.prod file>"
    arg_parser = ArgumentParser()
    arg_parser.add_argument(
        "-e", "--env-file", dest="env_file", help="read program parameters"
    )
    args = arg_parser.parse_args()
    return args


def get_env_variable(var_name):
    value = os.getenv(var_name)

    if value is None:
        raise EnvironmentError(f"Environment var '{var_name}' is not configured")
    else:
        return value


DEFAULT_DOCUMENT_PROMPT = PromptTemplate.from_template(
    template="""{source} : {page_content}"""
)


def combine_documents(
    docs, document_prompt=DEFAULT_DOCUMENT_PROMPT, document_separator="\n\n"
):
    doc_strings = [format_document(doc, document_prompt) for doc in docs]
    return document_separator.join(doc_strings)


def format_chat_history(chat_history: List[Tuple[str, str, str, str, str]]) -> List:
    buffer = []
    # for human, ai in chat_history:
    for my_tuple in chat_history:
        human = my_tuple[2]
        ai = my_tuple[3]
        buffer.append(HumanMessage(content=human))
        buffer.append(AIMessage(content=ai))
    return buffer
