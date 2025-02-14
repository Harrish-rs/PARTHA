import streamlit as st
import google.generativeai as genai
import os
import json

# Configure Gemini
api_key = "AIzaSyAKjy-Ijf6fjU1EMA48B1Bfe5wHeAox2bk"  # Replace with your actual API key
genai.configure(api_key=api_key)

# Create a Gemini model instance
model = genai.GenerativeModel('gemini-pro')

# Start a new chat
chat = model.start_chat(history=[])

# File to save conversation history
HISTORY_FILE = "conversation_history.json"

# Custom CSS for colorful UI and footer
st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(135deg, #f6d365 0%, #fda085 100%);
        color: #333;
    }
    .stTextInput>div>div>input {
        background-color: #fff;
        color: #333;
        border-radius: 10px;
    }
    .stButton>button {
        background-color: #ff6f61;
        color: white;
        border-radius: 10px;
        padding: 10px 20px;
        border: none;
        font-size: 16px;
    }
    .stButton>button:hover {
        background-color: #ff3b2f;
    }
    .chat-container {
        background-color: rgba(255, 255, 255, 0.8);
        border-radius: 10px;
        padding: 20px;
        margin: 10px 0;
    }
    .user-message {
        color: #007bff;
        text-align: right;
    }
    .bot-message {
        color: #333;
        text-align: left;
    }
    .footer {
        position: fixed;
        bottom: 0;
        right: 0;
        padding: 10px;
        font-size: 14px;
        color: #333;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Title and description
st.title("🌟 PARTHA - Your Emotional Companion")
st.markdown("Welcome to PARTHA! I'm here to help you navigate through your emotions and provide empathetic responses. How are you feeling today?")

# Add an image of a girl responding to queries
st.image("https://via.placeholder.com/150", width=150, caption="Your friendly assistant PARTHA")

# Function to load conversation history from a file
def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as file:
            return json.load(file)
    return []

# Function to save conversation history to a file
def save_history(history):
    with open(HISTORY_FILE, "w") as file:
        json.dump(history, file)

# Initialize session state for conversation history and input
if 'conversation_history' not in st.session_state:
    st.session_state.conversation_history = load_history()

if 'user_input' not in st.session_state:
    st.session_state.user_input = ""

# Function to get response from Gemini
def get_response(user_input):
    try:
        prompt = f"""
        First, analyze the emotion in this message: "{user_input}"
        Then, respond empathetically in 1-2 sentences based on the detected emotion.
        Start your response with [EMOTION: detected_emotion] then provide your response.
        """
        response = chat.send_message(prompt)
        response_text = response.text

        if '[EMOTION:' in response_text:
            parts = response_text.split(']', 1)
            emotion = parts[0].split('[EMOTION:', 1)[1].strip()
            actual_response = parts[1].strip()
        else:
            emotion = 'neutral'
            actual_response = response_text

        return emotion, actual_response

    except Exception as e:
        st.error(f"Error: {e}")
        return "neutral", "I'm here to listen. Would you like to tell me more?"

# Chat input
user_input = st.text_input("Type your message here...", value=st.session_state.user_input, key="input")

# Send button
if st.button("Send"):
    if user_input.strip():  # Check if the input is not empty
        emotion, response = get_response(user_input)
        st.session_state.conversation_history.append({"user": user_input, "emotion": emotion, "bot": response})
        st.session_state.user_input = ""  # Clear the input field
        save_history(st.session_state.conversation_history)  # Save history to file
        st.rerun()  # Rerun the app to update the UI

# Display chat history
for chat in st.session_state.conversation_history:
    st.markdown(f"<div class='chat-container'><div class='user-message'>You: {chat['user']}</div><div class='bot-message'>PARTHA: {chat['bot']} [Emotion: {chat['emotion']}]</div></div>", unsafe_allow_html=True)

# Footer with "Created by HARRISH" and heart emoji
st.markdown(
    """
    <div class="footer">
        Created by HARRISH <span style="color: red;">❤️</span>
    </div>
    """,
    unsafe_allow_html=True
)
