from dotenv import load_dotenv
import os
import logging

####################################################################################

# Set up logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler('config.log')
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

load_dotenv()

TYPHOON_API_KEY = os.getenv("TYPHOON_API_KEY")
if not TYPHOON_API_KEY:
  logger.error("TYPHOON_API_KEY not found in environment variables.")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
  logger.error("GEMINI_API_KEY not found in environment variables.")