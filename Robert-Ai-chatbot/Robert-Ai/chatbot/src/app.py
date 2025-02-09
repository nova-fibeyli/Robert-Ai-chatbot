import json
import streamlit as st
import logging
import time
import pandas as pd
import fitz  # PyMuPDF for PDF processing
import re
import os
import ollama

from llama_index.core.llms import ChatMessage
from query_manager import multi_query_search
from rag_fusion import rag_fusion_search
from file_handler import handle_file_upload
from db_handler import store_query_response, find_response
from pymongo import MongoClient

# Setup logging
logging.basicConfig(level=logging.INFO)

# Connect to MongoDB Atlas
client = MongoClient("mongodb+srv://AdvancedProgramming:AdvancedProgramming@cluster0.uemob.mongodb.net/test?retryWrites=true&w=majority")
db = client.support_bot
dialogue_collection = db.dialogues

# Load Constitution JSON Dataset
base_dir = os.path.dirname(os.path.abspath(__file__))  # Get current script directory
json_path = os.path.join(base_dir, "dataset", "constitution.json")  # Adjust path

try:
    with open(json_path, "r", encoding="utf-8") as f:
        constitution = json.load(f)
        logging.info("Constitution JSON file loaded successfully.")
except FileNotFoundError:
    logging.warning(f"Constitution JSON file not found: {json_path}")
    constitution = {}  # Fallback to an empty dictionary if the file is missing
except Exception as e:
    logging.error(f"Error loading Constitution JSON file: {str(e)}")
    constitution = {}  # Fallback to an empty dictionary on error

# Load the Empathetic Dialogues dataset into MongoDB
def load_dataset():
    try:
        train_data = pd.read_csv("EmpatheticDialogues/train.csv")
        dialogues = train_data[["prompt", "utterance"]].drop_duplicates().dropna()
        dialogue_collection.insert_many(dialogues.to_dict(orient="records"), ordered=False)
        logging.info("EmpatheticDialogues dataset loaded into MongoDB.")
    except Exception as e:
        logging.info("Dataset already exists or encountered an error.")

load_dataset()

# Function to sanitize user input to prevent invalid regex characters
def sanitize_regex_input(user_input):
    return re.escape(user_input)  # Escapes special characters

# Function to find response from MongoDB
def find_response(user_input):
    sanitized_input = sanitize_regex_input(user_input)
    try:
        results = dialogue_collection.find({"prompt": {"$regex": sanitized_input, "$options": "i"}})
        return [res["utterance"] for res in results] if results else []
    except Exception as e:
        logging.error(f"MongoDB query error: {str(e)}")
        return []

# Function to store query and response in MongoDB
def store_query_response(user_input, assistant_response):
    dialogue_collection.insert_one({
        "prompt": user_input,
        "utterance": assistant_response,
        "timestamp": time.time()
    })
    logging.info(f"Stored query and response in MongoDB: {user_input} - {assistant_response}")

# Stream chat logic, integrating File Content and Constitution dataset
def stream_chat(model, messages):
    try:
        user_input = messages[-1].content if messages else ""
        if not user_input:
            return "I didn’t catch that. Could you say it again?"

        # Check if the input contains file content
        if "[File Content Preview]:" in user_input:
            file_content = user_input.split("[File Content Preview]:")[-1].strip()
            if file_content:
                return f"Based on the uploaded file, here's what I found:\n\n{file_content}"

        # Check Constitution JSON
        for article in constitution.get("articles", []):
            if f"article {article['number']}".lower() in user_input.lower():
                return f"Article {article['number']}: {article['content']}"

        # Fetch all matching MongoDB responses
        mongo_responses = find_response(user_input)
        if mongo_responses:
            return "\n\n".join(mongo_responses)  # Return all results

        return "Sorry, I couldn't find relevant information in the Constitution or database."

    except Exception as e:
        logging.error(f"Error during streaming: {str(e)}")
        return "An error occurred. Please try again later."

# Main app function
def main():
    st.title("Chat with Robert ['-']")
    logging.info("App started")

    if 'messages' not in st.session_state:
        st.session_state.messages = []

    model = st.sidebar.selectbox("Choose a model", ["llama3.2", "phi3"])
    use_rag = st.checkbox("Use RAG Fusion")

    logging.info(f"Model selected: {model}")

    for message in reversed(st.session_state.messages):
        with st.chat_message(message.role):
            st.write(message.content)

    prompt = st.text_input("Enter your question:", key="user_prompt")
    uploaded_files = st.file_uploader("Upload files", type=["txt", "pdf", "docx"], accept_multiple_files=True)
    send_button = st.button("Send")

    if send_button:
        file_text = handle_file_upload(uploaded_files)
        full_prompt = f"{prompt}\n\n[File Content Preview]: {file_text}" if file_text.strip() else prompt

        if not full_prompt.strip():
            st.error("Please enter text or upload a file.")
        else:
            st.session_state.messages.append(ChatMessage(role="user", content=full_prompt))
            logging.info(f"User input: {full_prompt}")

            with st.chat_message("assistant"):
                response_container = st.empty()
                response_text = ""

                with st.spinner("Generating response..."):
                    try:
                        if use_rag:
                            response_message = rag_fusion_search(full_prompt, model)
                        else:
                            response_message = multi_query_search(full_prompt, model)

                        # Extract content from Ollama's Message object
                        if hasattr(response_message, "content"):
                            response_text = response_message.content
                        elif isinstance(response_message, dict) and "content" in response_message:
                            response_text = response_message["content"]
                        elif isinstance(response_message, str):
                            response_text = response_message
                        else:
                            response_text = "I'm sorry, I couldn't process your request."

                        st.session_state.messages.append(ChatMessage(role="assistant", content=response_text))
                        logging.info(f"Response: {response_text}")

                        store_query_response(full_prompt, response_text)

                    except Exception as e:
                        st.error(f"Error: {str(e)}")
                        logging.error(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
