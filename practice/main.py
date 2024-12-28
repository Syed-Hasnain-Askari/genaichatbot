from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import google.generativeai as genai # type: ignore
from fastapi.responses import StreamingResponse
from dotenv import load_dotenv
import os

# Load the .env file
load_dotenv()

# Get the API key from the environment
API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=API_KEY)

app = FastAPI()

# Define the request body schema
class ChatRequest(BaseModel):
    user_message: str

# Streaming generator to send responses line by line
async def stream_response(prompt: str):
    try:
        # Initialize the model
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt, stream=True,generation_config = genai.GenerationConfig(
        max_output_tokens=100,
        temperature=0.1,
    ))
        # Use the model's `generate_content_stream` to get streaming results
        for chunk in response:
            # Yield each line of the response
            yield f"{chunk.text}\n"
    except Exception as e:
        # Yield an error message in case of failure
        yield f"Error: {str(e)}"

# Endpoint for chatbot interaction (Streaming Response)
@app.post("/chat")
async def chat_with_bot(chat_request: ChatRequest):
    try:
        # Get the user message
        user_message = chat_request.user_message

        # Stream the bot's response
        return StreamingResponse(stream_response(user_message), media_type="text/plain")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))