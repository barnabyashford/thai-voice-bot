import logging

from llama_index.embeddings.gemini import GeminiEmbedding
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.embeddings.huggingface_api import HuggingFaceInferenceAPIEmbedding
from llama_index.llms.gemini import Gemini
from llama_index.llms.openai_like import OpenAILike

import os
import requests
import sys
import torch

####################################################################################

# Set up logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler('models.log')
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

# define a fuction to instantiate an OpenAILike object for typhoon llm
def get_typhoon_llm(model_name:str, api_key:str) -> OpenAILike:
  """
  Returns a llama_index.llms.openai_like.OpenAILike object that facilitates API calling of SCB10x typhoon model.
  - Params:
    model_name: str - The name of the model to be used.
  - Returns:
    OpenAILike - The OpenAILike object of the specified model.
  """

  try:
    llm = OpenAILike(model=model_name,
                     api_base="https://api.opentyphoon.ai/v1",
                     is_chat_model=True,
                     max_tokens=512,
                     is_function_calling_model=True,
                     api_key=api_key)
  except Exception as e:
    logger.exception("An error occured while trying to instantiate OpenAILike object:")

  return llm

# define a fuction to instantiate an Gemini object for gemini llm
def get_gemini_llm(model_name:str, api_key:str) -> Gemini:
  """
  Returns a llama_index.llms.gemini.Gemini object that facilitates API calling of Google's Gemini model.
  - Params:
    model_name: str - The name of the model to be used.
  - Returns:
    Gemini - The Gemini object of the specified model.
  """

  try:
    llm = Gemini(model_name=model_name,
                 temperature=0.1,
                 max_tokens=512,
                 api_key=api_key)
  except Exception as e:
    logger.exception("An error occured while trying to instantiate Gemini object:")

  return llm

# define a function to instantiate a HuggingFaceEmbedding object for an embedding model from Hugging Face Repository
def get_hf_embedding_model(model_name:str, api_key:str) -> HuggingFaceInferenceAPIEmbedding:
  """
  Returns a llama_index.embeddings.huggingface.HuggingFaceEmbedding object that facilitates text embedding for later use in semantic search.
  - Params:
    model_name: str - The name of the model to be used.
  - Returns:
    HuggingFaceEmbedding - The HuggingFaceEmbedding object of the specified model.
  """

  try:
    embed_model = HuggingFaceInferenceAPIEmbedding(model_name=model_name,
                                                   token=api_key
                                                   )
  except Exception as e:
    logger.exception("An error occured while trying to instantiate HuggingFaceEmbedding object:")

  return embed_model

# define a function to instantiate a GeminiEmbedding object for an embedding model via Google API
def get_gemini_embedding_model(model_name:str, api_key:str) -> GeminiEmbedding:
  """
  Returns a llama_index.embeddings.gemini.GeminiEmbedding object that facilitates text embedding for later use in semantic search.
  - Params:
    model_name: str - The name of the model to be used.
  - Returns:
    GeminiEmbedding - The GeminiEmbedding object of the specified model.
  """

  try:
    embed_model = GeminiEmbedding(model_name=model_name,
                                  api_key=api_key
                                  )
  except Exception as e:
    logger.exception("An error occured while trying to instantiate GeminiEmbedding object:")

  return embed_model

# define a function that sends audio data of the recording to an api endpoint, then return the transcribed text
def recognise_speech(audio_path:str, api_endpoint:str, hf_token:str) -> str:
  """
  Returns a string of text transcribed from the audio file to which the input path belongs.
  - Params:
    audio_path: str - The path to the audio file to be transcribed.
    api_url: str - the url endpoint of the model.
    hf_token: str - Hugging face token.
  - Returns:
    str - The transcribed text.
  """

  with open(audio_path, "rb") as audio:
    bin = audio.read()
  response = requests.post(api_endpoint, headers={"Authorization": f"Bearer {hf_token}"}, data=bin)
  result = response.json()

  return result.get('text', 'Could not transcribe audio')
