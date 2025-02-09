from dotenv import load_dotenv
import os
import logging

####################################################################################

# Set up logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler('get_env.log')
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

################################## from colab secrets #######################################

# from google.colab import userdata

# try:
#   GOOGLE_API_KEY = userdata.get("GOOGLE_API_KEY")
# except Exception as e:
#   logger.exception("GOOGLE_API_KEY not found in environment variables.")

# try:
#   HF_TOKEN = userdata.get("HF_TOKEN")
# except Exception as e:
#   logger.exception("HF_TOKEN not found in environment variables.")

# try:
#   QDRANT_API_KEY = userdata.get("QDRANT_API_KEY")
# except Exception as e:
#   logger.exception("QDRANT_API_KEY not found in environment variables.")

# try:
#   QDRANT_BASE = userdata.get("QDRANT_BASE")
# except Exception as e:
#   logger.exception("QDRANT_BASE not found in environment variables.")

# try:
#   TYPHOON_API_KEY = userdata.get("TYPHOON_API_KEY")
# except Exception as e:
#   logger.exception("TYPHOON_API_KEY not found in environment variables.")

################################## from .env #######################################
load_dotenv()

try:
  GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
except Exception as e:
  logger.exception("GOOGLE_API_KEY not found in environment variables.")

try:
  HF_TOKEN = os.getenv("HF_TOKEN")
except Exception as e:
  logger.exception("HF_TOKEN not found in environment variables.")

try:
  QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
except Exception as e:
  logger.exception("QDRANT_API_KEY not found in environment variables.")

try:
  QDRANT_BASE = os.getenv("QDRANT_BASE")
except Exception as e:
  logger.exception("QDRANT_BASE not found in environment variables.")

try:
  TYPHOON_API_KEY = os.getenv("TYPHOON_API_KEY")
except Exception as e:
  logger.exception("TYPHOON_API_KEY not found in environment variables.")
