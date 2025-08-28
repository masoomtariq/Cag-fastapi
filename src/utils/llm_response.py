from google.genai import types
import google.genai as genai
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")



client = genai.Client(api_key= api_key,)

