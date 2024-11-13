import streamlit as st
from datetime import datetime
import json
import os

# Initialize session state for messages and users
if 'messages' not in st.session_state:
    st.session_state.messages = []

if 'current_user' not in st.session_state:
    st.session_state.current_user = None

# Function to load messages from file
def load_messages():
    if os.path.exists('chat_history.json'):
        with open('chat_history.json', 'r') as f:
            return json.load(f)
    return []

# Function to save messages to file
def save_messages(messages):
    with open('chat_history.json', 'w') as f:
        json.dump(messages, f)

# Load existing messages
st.session_state.messages = load_messages()

# Custom CSS for better UI
st.markdown("""
    <style>
    .main {
        background-color: #f0f2f6;
        padding: 2rem;
        border-radius: 1rem;
    }
    .stTitle {
        color: #1f1f1f;
        font-size: 3rem !important;
        text-align: center;
        margin-bottom: 2rem !important;
    }
    .chat-container {
        background-color: white;
        padding: 2rem;
        border-radius: 1rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .stTextInput > div > div > input {
        border-radius: 20px;
    }
    .stButton > button {
        border-radius: 20px;
        width: 100%;
    }
    </style>
""", unsafe_allow_html=True)

# Main app
st.title("✨ Global Chat Room 💭")

# User authentication
if not st.session_state.current_user:
    with st.form("user_form"):
        st.markdown("<h3 style='text-align: center;'>Welcome to the Chat!</h3>", unsafe_allow_html=True)
        username = st.text_input("Enter your name to join the chat:", placeholder="Your name here...")
        submit = st.form_submit_button("Join Chat")
        if submit and username:
            st.session_state.current_user = username
            new_message = {
                "user": "System",
                "message": f"👋 {username} has joined the chat!",
                "timestamp": datetime.now().strftime("%H:%M:%S")
            }
            st.session_state.messages.append(new_message)
            save_messages(st.session_state.messages)
            st.rerun()

# Chat interface
if st.session_state.current_user:
    # Display chat messages
    st.markdown("<div class='chat-container'>", unsafe_allow_html=True)
    for message in st.session_state.messages:
        with st.chat_message(message["user"], avatar="👤" if message["user"] != "System" else "🤖"):
            st.markdown(f"**{message['user']}** - {message['timestamp']}")
            st.markdown(f"_{message['message']}_")
    st.markdown("</div>", unsafe_allow_html=True)

    # Input for new messages
    st.markdown("<br>", unsafe_allow_html=True)
    with st.form("chat_form", clear_on_submit=True):
        col1, col2 = st.columns([4,1])
        with col1:
            message = st.text_input(f"Message as {st.session_state.current_user}:", placeholder="Type your message here...")
        with col2:
            submit_message = st.form_submit_button("Send 📤")

        if submit_message and message:
            new_message = {
                "user": st.session_state.current_user,
                "message": message,
                "timestamp": datetime.now().strftime("%H:%M:%S")
            }
            st.session_state.messages.append(new_message)
            save_messages(st.session_state.messages)
            st.rerun()
