from llama_index.core import (PromptTemplate, Settings, SimpleDirectoryReader, StorageContext, SummaryIndex, VectorStoreIndex)
from llama_index.vector_stores.qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.llms import (ChatMessage, MessageRole)
from llama_index.core.query_engine.router_query_engine import RouterQueryEngine
from llama_index.core.selectors import LLMSingleSelector
from llama_index.core.tools import QueryEngineTool

import gradio as gr

from get_models import get_typhoon_llm, get_gemini_llm, get_hf_embedding_model, get_gemini_embedding_model, recognise_speech
from get_env import GOOGLE_API_KEY, HF_TOKEN, QDRANT_API_KEY, QDRANT_BASE, TYPHOON_API_KEY

import logging
from typing import List, Tuple
from gtts import gTTS
import tempfile

# import nest_asyncio
# nest_asyncio.apply()

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

# Typhoon
Settings.llm = get_typhoon_llm(model_name="typhoon-v1.5-instruct", api_key=TYPHOON_API_KEY)
Settings.embed_model = get_hf_embedding_model(model_name="sentence-transformers/paraphrase-multilingual-mpnet-base-v2", api_key=HF_TOKEN)
# Gemini
# Settings.llm = get_gemini_llm(model_name="models/gemini-1.5-flash-8b", api_key=GOOGLE_API_KEY)
# Settings.embed_model = get_gemini_embedding_model(model_name="models/text-embedding-004", api_key=GOOGLE_API_KEY)

documents = SimpleDirectoryReader(input_files=["/content/2209491_WorrapatCheng.pdf"]).load_data()

qdrant_client = QdrantClient(url=QDRANT_BASE, api_key=QDRANT_API_KEY)
# OR IF YOU WANT A QUICK, ON MEMORY CLIENT
# client = qdrant_client.QdrantClient(location=":memory:") # check https://docs.llamaindex.ai/en/stable/examples/vector_stores/QdrantIndexDemo/ for more detail

qdrant_store = QdrantVectorStore(client=qdrant_client, collection_name="chat_embeddings")
storage_context = StorageContext.from_defaults(vector_store=qdrant_store)
index = VectorStoreIndex.from_documents(documents, storage_context=storage_context)

# Define the prompt template
template = """
ตอบคำถามผู้ใช้ตามข้อมูลเติมที่แนบมา หากไม่มีข้อมูลให้ตอบว่าไม่ทราบในกรณีคำถามต้องการข้อมูล
หากเป็นคำถามที่ไม่ต้องการข้อมูลเพิ่มเติม เช่น การทักทาย การคุยเล่น สามารถตอบตามปกติได้

คำถาม: {user_input}
ข้อมูล: {context}
"""

# Convert the index to a chat engine with the prompt template
chat_engine = index.as_chat_engine(
    prompt_template=PromptTemplate(template),  # Pass the prompt template
)

# Ensure temp directory exists for saving audio responses
TEMP_DIR = "temp_audio"
os.makedirs(TEMP_DIR, exist_ok=True)

# Function to perform query routing based on embeddings
def query_with_rag(query: str, history: List[Tuple[str, str]]) -> str:
    messages_history = []

    # Load conversation history
    if history and len(history) != 0:
        for user, bot in history:
            messages_history.append(ChatMessage(role=MessageRole.USER, content=user))
            messages_history.append(ChatMessage(role=MessageRole.ASSISTANT, content=bot))

    try:
        response = chat_engine.chat(query, chat_history=messages_history).response  # Get response from LLM
        return response  # Return history and audio path separately
    except Exception as e:
        logger.error(f"Error in process_input: {e}")
        return history, None  # Return history even on failure

# Text to Speech (TTS) function
def text_to_speech(text: str) -> str:
    try:
        audio_path = os.path.join(TEMP_DIR, f'response_{len(os.listdir(TEMP_DIR))}.mp3')
        tts = gTTS(text=text, lang='th')
        tts.save(audio_path)
        return audio_path
    except Exception as e:
        logger.error(f"Error in text-to-speech: {e}")
        return None

# Transcribe Audio
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

# Process input (text or audio)
def process_input(message: str, history: List[Tuple[str, str]]) -> Tuple[List[Tuple[str, str]], str]:
    """
    Process user input and return updated history with bot's response.
    """
    # Retrieve response using RAG
    response = query_with_rag(message, history)

    # Add message to history
    history.append((message, response))

    # Convert response to speech
    audio_path = text_to_speech(response)

    return history, audio_path

# Process Audio (voice input)
def process_audio(audio_path: str, history: List[Tuple[str, str]]) -> Tuple[List[Tuple[str, str]], str]:
  if not audio_path:
      return history, None

  transcribed_text = transcribe_audio(audio_path)
  return process_input(transcribed_text, history)

def clear_history():
  chat_engine.reset()
  return [], None

# Gradio interface
def main():
    with gr.Blocks(theme=gr.themes.Soft()) as interface:
        gr.Markdown("# RAG-powered Voice Chatbot with Qdrant Integration")

        bot = gr.Chatbot()  # Chatbot UI component
        with gr.Row():
          with gr.Column(scale=6):
            message = gr.Textbox(placeholder="Type your message here...")
          with gr.Column(scale=1):
            audio_input = gr.Audio(sources="microphone", type="filepath", label="🎤 Voice Input")

        with gr.Row():
          clear = gr.Button("Clear History")
          audio_output = gr.Audio(label="🔊 Bot Response", type="filepath")

        # Handling text input
        message.submit(process_input, [message, bot], [bot, audio_output])

        # Handling voice input
        audio_input.change(process_audio, [audio_input, bot], [bot, audio_output])

        # Clear chat history
        clear.click(clear_history, None, [bot, audio_output])

    interface.launch(debug=True)

if __name__ == "__main__":
    main()
    chat_engine.reset()
