import logging
import sys
import os

from llama_index.core import SimpleDirectoryReader, StorageContext, VectorStoreIndex
from llama_index.core.llms import ChatMessage, MessageRole
from llama_index.llms.gemini import Gemini
from llama_index.llms.openai_like import OpenAILike
from llama_index.vector_stores.qdrant import QdrantVectorStore

import qdrant_client

from config import TYPHOON_API_KEY, GEMINI_API_KEY

####################################################################################

# Set up logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler('llm_rag.log')
file_handler.setLevel(logging.DEBUG)
file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s : %(message)s')
file_handler.setFormatter(file_formatter)

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)
stream_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s : %(message)s')
stream_handler.setFormatter(stream_formatter)

logger.addHandler(file_handler)
logger.addHandler(stream_handler)

####################################################################################

def get_typhoon_llm(model_name:str) -> OpenAILike:
  """
  Returns a llama_index.llms.openai_like.OpenAILike object that facilitates API calling of SCB10x typhoon model.
  - Params:
    model_name: str - The name of the model to be used.
  - Returns:
    OpenAILike - The OpenAILike object of the specified model.
  """

  return OpenAILike(model=model_name,
                    api_base="https://api.opentyphoon.ai/v1",
                    is_chat_model=True,
                    max_tokens=512,
                    api_key=os.getenv("TYPHOON_API_KEY"))

def get_gemini_llm(model_name:str) -> Gemini:
  """
  Returns a llama_index.llms.gemini.Gemini object that facilitates API calling of Google's Gemini model.
  - Params:
    model_name: str - The name of the model to be used.
  - Returns:
    Gemini - The Gemini object.
  """

  return Gemini(model_name=model_name,
                temperature=0.1,
                max_tokens=512,
                api_key=os.getenv("GOOGLE_API_KEY"))

def main():
  pass

if __name__ == "__main__":
  main()