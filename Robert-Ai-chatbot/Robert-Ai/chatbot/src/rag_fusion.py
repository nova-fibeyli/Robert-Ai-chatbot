import ollama
import logging
from db_handler import find_response

# RAG Fusion search
def rag_fusion_search(prompt, model):
    logging.info(f"Performing RAG Fusion search for: {prompt}")

    # Retrieve relevant responses from the vector store
    retrieved_docs = find_response(prompt)

    if retrieved_docs:
        combined_context = "\n\n".join(retrieved_docs)
        full_query = f"Using the following retrieved knowledge:\n{combined_context}\n\nAnswer this: {prompt}"
    else:
        full_query = prompt

    try:
        response = ollama.chat(model=model, messages=[{"role": "user", "content": full_query}])
        return response['message'] if response else "No relevant information found."
    except Exception as e:
        logging.error(f"Error in RAG Fusion search: {str(e)}")
        return "An error occurred while performing RAG Fusion."
