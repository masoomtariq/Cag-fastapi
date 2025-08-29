from google.genai import types
import google.genai as genai
from dotenv import load_dotenv
import os

load_dotenv()

def get_llm_response(context: str, query: str) -> str:

    api_key = os.getenv("GOOGLE_API_KEY")

    if api_key is None:
        raise ValueError("GOOGLE API KEY environment variable is not set."
                        "Please set it to your Google Gemini Api Key (Get key from https://aistudio.google.com/apikey)")

    client = genai.Client(api_key= api_key)

    model = "gemma-3-1b-it"

    contents = [types.Content(role='user',parts=[types.Part.from_text(text=query)])]

    generate_content_config = types.GenerateContentConfig(temperature=0, response_mime_type='text/plain', system_instruction=[types.Part.from_text(text=context)])

    response = client.models.generate_content_stream(model=model, contents=contents, config=generate_content_config)

context = "Nothing"

query = "my name is masoom"

api_key = os.getenv("GOOGLE_API_KEY")

if api_key is None:
    raise ValueError("GOOGLE API KEY environment variable is not set."
                    "Please set it to your Google Gemini Api Key (Get key from https://aistudio.google.com/apikey)")

client = genai.Client(api_key= api_key)

model = "gemini-2.5-flash-lite"

contents = [types.Content(role='user',parts=[types.Part.from_text(text=query)])]

generate_content_config = types.GenerateContentConfig(temperature=0, response_mime_type='text/plain', system_instruction=[types.Part.from_text(text=context)], thinking_config=types.ThinkingConfig(thinking_budget=0))

for chunk in client.models.generate_content_stream(
                            model=model,
                            contents=contents,
                            config=generate_content_config):
    print(chunk.text, end='')