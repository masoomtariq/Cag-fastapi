from google.genai import types
import google.genai as genai
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")

if api_key is None:
    raise ValueError("""GOOGLE API KEY environment variable is not set.\nPlease set it to your Google Gemini Api Key (Get key from https://aistudio.google.com/apikey)""")

client = genai.Client(api_key= api_key,)

