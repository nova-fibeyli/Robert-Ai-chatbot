import ollama
import logging

# Function to generate multiple queries from the same prompt
def generate_multi_queries(prompt):
    variations = [
        prompt,
        f"Can you explain {prompt} in simple terms?",
        f"Give me an academic explanation of {prompt}.",
        f"Provide examples related to {prompt}.",
        f"Summarize {prompt} in one paragraph."
    ]
    return variations

# Multi-Query Search using Ollama
def multi_query_search(prompt, model):
    queries = generate_multi_queries(prompt)
    responses = []

    logging.info(f"Sending Multi-Queries to Ollama for prompt: {prompt}")

    for query in queries:
        try:
            response = ollama.chat(model=model, messages=[{"role": "user", "content": query}])
            if response:
                responses.append(response['message'])
        except Exception as e:
            logging.error(f"Error processing query '{query}': {str(e)}")

    # Combine all responses
    return "\n\n".join(responses) if responses else "No relevant information found."
