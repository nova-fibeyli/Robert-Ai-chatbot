from pymongo import MongoClient
import time
import logging

client = MongoClient("mongodb+srv://AdvancedProgramming:AdvancedProgramming@cluster0.uemob.mongodb.net/test?retryWrites=true&w=majority")
db = client.support_bot
dialogue_collection = db.dialogues

# Store query-response pairs in MongoDB
def store_query_response(user_input, assistant_response):
    dialogue_collection.insert_one({
        "prompt": user_input,
        "utterance": assistant_response,
        "timestamp": time.time()
    })
    logging.info(f"Stored query and response in MongoDB: {user_input} - {assistant_response}")

# Retrieve relevant responses
def find_response(user_input):
    results = dialogue_collection.find({"prompt": {"$regex": user_input, "$options": "i"}})
    return [res["utterance"] for res in results] if results else []
