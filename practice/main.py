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

# Endpoint for chatbot interaction (Streaming Response)
@app.post("/chat")
async def chat_with_bot(chat_request: ChatRequest):
    try:
        # Get the user message
        user_message = chat_request.user_message

        # Initialize the model
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(user_message,generation_config = genai.GenerationConfig(
        max_output_tokens=1000,
        temperature=0.9,
        ))
        # Return the AI response
        return {"reply": response.text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))