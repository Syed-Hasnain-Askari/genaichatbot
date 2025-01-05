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
    max_token: int
    temperature: float
    
def is_programming_related(query):
    keywords = ["code", "function", "debug", "syntax", "error", "algorithm"]
    return any(keyword in query.lower() for keyword in keywords)

# Endpoint for chatbot interaction (Streaming Response)
@app.post("/chat")
async def chat_with_bot(chat_request: ChatRequest):
    try:
        # Get the user message
        user_message = chat_request.user_message
        max_token = chat_request.max_token
        temperature = chat_request.temperature
        if is_programming_related(user_message):
            # Initialize the model
            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content(user_message,generation_config = genai.GenerationConfig(
            max_output_tokens=max_token,
            temperature=temperature,
            ))
            # Return the AI response
            return {"reply": response.text}
        else:
            return {"reply":"I'm here to help with programming and coding questions. Please ask something related to code!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))