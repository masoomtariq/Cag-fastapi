import os
from dotenv import load_dotenv
import google.genai as genai
from google.genai import types

# Load environment variables (only once when module is imported)
load_dotenv()

# ✅ Global client instance for efficiency (instead of recreating per call)
_api_key = os.getenv("GOOGLE_API_KEY")
if not _api_key:
    raise EnvironmentError(
        "GOOGLE_API_KEY environment variable is not set. "
        "Please set it to your Google Gemini API key (get key from https://aistudio.google.com/apikey)."
    )

client = genai.Client(api_key=_api_key)


async def get_llm_response(context: str, query: str) -> str:
    """
    Query the Google Gemini LLM with user input and provided context.

    Args:
        context (str): Content from the uploaded document (source of truth).
        query (str): User's question or input.

    Returns:
        str: LLM-generated response.
    """
    # Prepare user input
    contents = [types.Content(role="user", parts=[types.Part.from_text(text=query)])]

    # System instructions for model behavior
    instructions = f"""
    You are a helpful and knowledgeable assistant.
    Your primary source of truth is the context provided in the below which is actually the content of the uploaded Document.
    Answer all user queries clearly, concisely, and in a professional tone.
    If the query is directly addressed in the context, provide an accurate and well-structured response.
    If the query is not covered, politely state that the information is not available in the context.
    Do not invent or assume details beyond what the context provides.
    Maintain relevance by always connecting your answer back to the context’s content.
    When explaining, prefer clarity over length, and adapt language to be easy to understand.
    Keep responses respectful, supportive, and focused on solving the user’s need.
    CONTEXT : {context}"""

    # Configure generation
    generate_content_config = types.GenerateContentConfig(
        temperature=0,
        response_mime_type="text/plain",
        system_instruction=[types.Part.from_text(text=instructions)],
        thinking_config=types.ThinkingConfig(thinking_budget=0),
    )

    # Generate response
    response = client.models.generate_content(
        model="gemini-2.5-flash-lite",
        contents=contents,
        config=generate_content_config,
    )

    return response