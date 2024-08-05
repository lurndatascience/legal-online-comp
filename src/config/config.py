import logging
import os
import sys
from pathlib import Path

from dotenv import load_dotenv

from utils.utils import read_program_arguments, get_env_variable

program_args = read_program_arguments()

true_strings = ("yes", "true", "t", "y", "1")

# Read the variable for the env file. It contains the config values for the app.
if program_args.env_file is not None and not Path(program_args.env_file).exists():
    raise Exception(f"The .env file {program_args.env_file} does not exist")

loaded = load_dotenv(program_args.env_file)

# Logging
LOG_TO_STDERR = get_env_variable("LOG_TO_STDERR").lower() in true_strings
logging_path = get_env_variable("LOGGING_PATH")
# Need logging path for prompt log file
if not os.path.exists(logging_path):
    os.makedirs(logging_path, exist_ok=True)
if LOG_TO_STDERR:
    logging.basicConfig(
        stream=sys.stderr,
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
else:
    logging_file = get_env_variable("LOGGING_FILE")
    logging.basicConfig(
        filename=logging_file, filemode="w", encoding="utf-8", level=logging.INFO
    )

# Prompt, documents, LLM response logging
llm_logging_file = get_env_variable("LLM_LOGGING_FILE")
postgres_host = get_env_variable("POSTGRES_HOST")
postgres_port = get_env_variable("POSTGRES_PORT")
postgres_user = get_env_variable("POSTGRES_USER")
postgres_password = get_env_variable("POSTGRES_PASSWORD")
postgres_database = get_env_variable("POSTGRES_DB")
postgres_collection_name = get_env_variable("POSTGRES_COLLECTION_NAME")
postgres_connection_string = f"postgresql+psycopg2://{postgres_user}:{postgres_password}@localhost:{postgres_port}/{postgres_database}"

# Langfuse
enable_langfuse = get_env_variable("ENABLE_LANGFUSE")
langfuse_host = get_env_variable("LANGFUSE_HOST")
langfuse_public_key = get_env_variable("LANGFUSE_PUBLIC_KEY")
langfuse_secret_key = get_env_variable("LANGFUSE_SECRET_KEY")
