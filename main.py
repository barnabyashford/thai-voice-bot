# User Interface
import gradio as gr

# Text-to-Speech
from gtts import gTTS

# RAG framework
from llama_index.core import (PromptTemplate, Settings, SimpleDirectoryReader, StorageContext, SummaryIndex, VectorStoreIndex)
from llama_index.vector_stores.qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.llms import (ChatMessage, MessageRole)
from llama_index.core.query_engine.router_query_engine import RouterQueryEngine
from llama_index.core.selectors import LLMSingleSelector
from llama_index.core.tools import QueryEngineTool

import logging
from typing import List, Tuple
import tempfile
import os
import requests

from get_models import get_typhoon_llm, get_gemini_llm, get_hf_embedding_model, get_gemini_embedding_model, recognise_speech
from get_env import GOOGLE_API_KEY, HF_TOKEN, QDRANT_API_KEY, QDRANT_BASE, TYPHOON_API_KEY

# Logging setup
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler('rag.log')
file_handler.setLevel(logging.DEBUG)
file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s : %(message)s')
file_handler.setFormatter(file_formatter)

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)
stream_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s : %(message)s')
stream_handler.setFormatter(stream_formatter)

logger.addHandler(file_handler)
logger.addHandler(stream_handler)

# Initialize settings and clients
Settings.llm = get_gemini_llm(model_name="models/gemini-1.5-flash-8b", api_key=GOOGLE_API_KEY)
Settings.embed_model = get_gemini_embedding_model(model_name="models/text-embedding-004", api_key=GOOGLE_API_KEY)
qdrant_client = QdrantClient(url=QDRANT_BASE, api_key=QDRANT_API_KEY)

# Setup temp directory and logging
TEMP_DIR = "temp_audio"
os.makedirs(TEMP_DIR, exist_ok=True)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

def text_to_speech(text: str) -> str:
    try:
        audio_path = os.path.join(TEMP_DIR, f'response_{len(os.listdir(TEMP_DIR))}.mp3')
        tts = gTTS(text=text, lang='th')
        tts.save(audio_path)
        return audio_path
    except Exception as e:
        logger.error(f"Error in text-to-speech: {e}")
        return None

def transcribe_audio(audio_path: str) -> str:
    API_URL = "https://api-inference.huggingface.co/models/openai/whisper-large-v3-turbo"
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    
    with open(audio_path, "rb") as f:
        data = f.read()
    response = requests.post(API_URL, headers=headers, data=data)
    
    try:
        return response.json()["text"]
    except Exception as e:
        logger.error(f"Error in transcription: {e}")
        return "Transcription failed."

def index_documents(document_path: str) -> Tuple[VectorStoreIndex, SummaryIndex]:

  splitter = SentenceSplitter(chunk_size=1024)

  qdrant_store = QdrantVectorStore(client=qdrant_client, collection_name=os.path.basename(document_path))
  storage_context = StorageContext.from_defaults(vector_store=qdrant_store)

  documents = SimpleDirectoryReader(input_files=[document_path]).load_data()
  nodes = splitter.get_nodes_from_documents(documents)

  vector_index = VectorStoreIndex.from_documents(documents, storage_context=storage_context)
  summary_index = SummaryIndex(nodes)

  vector_query_engine = vector_index.as_query_engine()
  summary_query_engine = summary_index.as_query_engine(response_mode="tree_summarize",use_async=True)

  vector_tool = QueryEngineTool.from_defaults(
    query_engine=vector_query_engine,
    description=(
      f"ใช้สำหรับตอบคำถามเกี่ยวกับไฟล์ {os.path.basename(document_path)}"
    ),
  )

  summary_tool = QueryEngineTool.from_defaults(
    query_engine=summary_query_engine,
    description=(
      f"ใช้สำหรับการตอบคำถามที่จำเป็นต้องใช้เนื้อหาทั้งหมดของไฟล์ {os.path.basename(document_path)}"
    ),
  )

  return vector_tool, summary_tool

class RAGEngine:

  def __init__(self, llm=None, embed_model=None, vector_db_client=None, document_path:str=None):
    
    self.doc_to_tools = dict()
    self.all_tools = list()
    self.llm = Settings.llm if not llm else llm
    self.embed_model = Settings.embed_model if not embed_model else embed_model
    self.client = vector_db_client
    self.query_engine = None

    if document_path and os.path.exists(document_path):

      if os.path.isdir(document_path) and os.listdir(document_path) > 0:

        for document in os.listdir(document_path):
          full_path = os.path.join(document_path, document)
          vector_tool, summary_tool = index_documents(full_path)
          self.all_tools.append(vector_tool)
          self.all_tools.append(summary_tool)
          self.doc_to_tools[document] = {"vector_tool": vector_tool, "summary_tool": summary_tool}

      elif os.path.isfile(document_path):
        vector_tool, summary_tool = index_documents(document_path)
        self.all_tools.append(vector_tool)
        self.all_tools.append(summary_tool)
        self.doc_to_tools[os.path.basename(document_path)] = {"vector_tool": vector_tool, "summary_tool": summary_tool}

      self.query_engine = RouterQueryEngine(
        selector=LLMSingleSelector.from_defaults(),
        query_engine_tools=self.all_tools,
        verbose=True
      ) 
    
  def query(self, query: str, history:List[Tuple[str, str]]=None):
    if self.query_engine:
      return self.query_engine.query(query)
    else:
      messages = []
      
      if history and len(history) != 0:
        
        for user, bot in history:
          messages.append(ChatMessage(role=MessageRole.USER, content=user))
          messages.append(ChatMessage(role=MessageRole.ASSISTANT, content=bot))
        
      messages.append(ChatMessage(role=MessageRole.USER, content=query))
        
      return self.llm.chat(messages=messages).message.content
  
  def add_document(self, document_path:str):

    if os.path.isdir(document_path) and os.listdir(document_path) > 0:

      for document in os.listdir(document_path):
        full_path = os.path.join(document_path, document)
        vector_tool, summary_tool = index_documents(full_path)
        self.all_tools.append(vector_tool)
        self.all_tools.append(summary_tool)
        self.doc_to_tools[document] = {"vector_tool": vector_tool, "summary_tool": summary_tool}

    elif os.path.isfile(document_path):
      vector_tool, summary_tool = index_documents(document_path)
      self.all_tools.append(vector_tool)
      self.all_tools.append(summary_tool)
      self.doc_to_tools[os.path.basename(document_path)] = {"vector_tool": vector_tool, "summary_tool": summary_tool}

    self.query_engine = RouterQueryEngine(
      selector=LLMSingleSelector.from_defaults(),
      query_engine_tools=self.all_tools,
      verbose=True
    )

class RAGChatbot:
    def __init__(self):
        self.rag_engine = RAGEngine(vector_db_client=qdrant_client)
        self.chat_history: List[Tuple[str, str]] = []
        
    def add_document(self, file_path: str):
        self.rag_engine.add_document(file_path)
        
    def process_message(self, message: str) -> Tuple[List[Tuple[str, str]], str]:
        response = self.rag_engine.query(message, self.chat_history)
        response_text = str(response.response) if hasattr(response, 'response') else str(response)
        self.chat_history.append((message, response_text))
        audio_path = text_to_speech(response_text)
        return self.chat_history, audio_path
        
    def process_audio(self, audio_path: str) -> Tuple[List[Tuple[str, str]], str]:
        if not audio_path:
            return self.chat_history, None
        transcribed_text = transcribe_audio(audio_path)
        return self.process_message(transcribed_text)
        
    def clear_history(self):
        self.chat_history = []
        return [], None

def main():
    bot = RAGChatbot()
    
    with gr.Blocks(theme=gr.themes.Soft()) as interface:
        gr.Markdown("# RAG-powered Voice Chatbot with Document Upload")
        
        with gr.Row():
            file_upload = gr.File(label="Upload Document")
        
        chatbot = gr.Chatbot()
        with gr.Row():
            with gr.Column(scale=6):
                message = gr.Textbox(placeholder="Type your message here...")
            with gr.Column(scale=1):
                audio_input = gr.Audio(sources="microphone", type="filepath", label="🎤 Voice Input")
        
        with gr.Row():
            clear = gr.Button("Clear History")
            audio_output = gr.Audio(label="🔊 Bot Response", type="filepath")
            
        def handle_file_upload(file):
            if file:
                bot.add_document(file.name)
                return f"Document {os.path.basename(file.name)} uploaded and indexed successfully!"
            return "No file uploaded."
            
        file_upload.upload(handle_file_upload, file_upload, gr.Textbox())
        message.submit(bot.process_message, [message], [chatbot, audio_output])
        audio_input.change(bot.process_audio, [audio_input], [chatbot, audio_output])
        clear.click(bot.clear_history, None, [chatbot, audio_output])

    interface.launch(debug=True)

if __name__ == "__main__":
    main()
