import os
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

if not OPENROUTER_API_KEY:
    raise ValueError("OPENROUTER_API_KEY  not found. Check your .env file.")

MODEL =  "meta-llama/llama-3.1-8b-instruct"

BASE_URL = "https://openrouter.ai/api/v1"

MAX_TOKENS = 500
TEMPERATURE = 0.7
