"""Callback Handler that prints to std out."""
from typing import Any, Dict, List, Optional

from langchain.callbacks.base import BaseCallbackHandler

from pathlib import Path
import os
import time


class FileCallbackHandler(BaseCallbackHandler):
    """Callback Handler that prints to std out."""

    def __init__(
        self, path: Path, print_prompts: bool = False, color: Optional[str] = None
    ) -> None:
        """Initialize callback handler."""
        self.color = color
        self.print_prompts = print_prompts
        self.path = path
        if os.path.exists(self.path):
            self.file_handle = open(path, "a")
        else:
            self.file_handle = open(path, "w")

    def on_llm_start(
        self, serialized: Dict[str, Any], prompts: List[str], **kwargs: Any
    ) -> None:
        """Print out the prompts."""
        if self.print_prompts:
            self.file_handle.write(f"=============== PROMPTS ==================\n")
            for prompt in prompts:
                self.file_handle.write(f"{prompt}\n")
            self.file_handle.write("\n")
            self.file_handle.flush()
            self.file_handle.write(f"============ END PROMPTS =================\n\n")

    def on_llm_new_token(self, token: str, **kwargs) -> None:
        """Print the response of the LLM token by token
        while they are generated
        """
        self.file_handle.write(token)
        print(token, end="", flush=True)
        time.sleep(0.05)
