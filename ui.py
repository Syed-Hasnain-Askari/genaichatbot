import streamlit as st
import requests

# Title for the chat interface
st.title("AI Chat (Powered by Google Gemini)")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "input" not in st.session_state:
    st.session_state.input = ""  # Initialize the input field

# Function to handle input submission
def send_message():
    user_message = st.session_state.input.strip()  # Get input value
    if user_message:
        # Add user message to chat
        st.session_state.messages.append({"sender": "user", "text": user_message})

        # Call the backend API
        try:
            response = requests.post(
                "http://127.0.0.1:8000/chat",
                json={
                    "user_message": user_message,
                    "max_token": max_tokens,
                    "temperature": temperature,
                    },
            )
            if response.status_code == 200:
                ai_reply = response.json().get("reply", "Error: No reply received.")
            else:
                ai_reply = "Error: Could not reach AI API."
        except Exception as e:
            ai_reply = f"Error: {e}"

        # Add AI message to chat
        st.session_state.messages.append({"sender": "ai", "text": ai_reply})

    # Clear the input field
    st.session_state.input = ""

# Display chat history
st.sidebar.title("Advanced Settings")
max_tokens = st.sidebar.slider(label="Max Tokens", min_value=100, max_value=1000, value=1000, step=5)
temperature = st.sidebar.slider(label="Temperature", min_value=0.0, max_value=1.0, value=1.0, step=0.1)

for msg in st.session_state.messages:
    if msg["sender"] == "user":
        st.markdown(f"**You:** {msg['text']}")
    else:
        st.markdown(f"**AI:** {msg['text']}")

# Input text box and button
st.text_input(
    "Type your message:",
    key="input",  # Use session state key
    on_change=send_message,  # Call send_message when input changes
)

