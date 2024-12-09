import gradio as gr
from qdrant_client import QdrantClient
from qdrant_client.http import models
from fastembed import TextEmbedding
import requests

# Initialize Qdrant client
qdrant_client = QdrantClient(host="localhost", port=6333)
COLLECTION_NAME = "robotics-documents"

# Initialize embedding model
embedding_model = TextEmbedding()

# Ollama server details
OLLAMA_SERVER_URL = "http://127.0.0.1:7860/"
MODEL_NAME = "https://huggingface.co/CojoFitz/model"

# Function to generate embeddings
def generate_embedding(query):
    return embedding_model.embed(query)

# Function to query Qdrant for relevant documents
def search_qdrant(query_embedding, top_k=5):
    search_result = qdrant_client.search(
        collection_name=COLLECTION_NAME,
        query_vector=query_embedding,
        limit=top_k,
        with_payload=True
    )
    return search_result

# Function to query the LLaMA model via Ollama server
def query_llama(prompt):
    response = requests.post(
        OLLAMA_SERVER_URL,
        json={"model": MODEL_NAME, "prompt": prompt}
    )
    if response.status_code == 200:
        return response.json().get("response", "No response received from LLaMA.")
    else:
        return f"Error querying LLaMA: {response.text}"

# Main function to process the query
def process_query(user_query):
    # Step 1: Generate query embedding
    query_embedding = generate_embedding(user_query)
    
    # Step 2: Retrieve relevant documents from Qdrant
    search_results = search_qdrant(query_embedding)
    documents = [result.payload for result in search_results]
    
    # Step 3: Prepare context for LLaMA
    context = "\n\n".join(
        f"Title: {doc['title']}\nContent: {doc['content']}" for doc in documents
    )
    llama_prompt = f"Context:\n{context}\n\nUser Query:\n{user_query}\n\nAnswer:"
    
    # Step 4: Get the LLaMA response
    llama_response = query_llama(llama_prompt)
    
    return llama_response, documents

# Gradio Interface
def gradio_interface(user_query):
    response, documents = process_query(user_query)
    # Format the documents for display
    docs_display = "\n\n".join(
        f"Title: {doc['title']}\nPlatform: {doc['platform']}\nLink: {doc['link']}"
        for doc in documents
    )
    return response, docs_display

# Gradio application
with gr.Blocks() as app:
    gr.Markdown("### Robotics Document Assistant")
    
    with gr.Row():
        query_input = gr.Textbox(label="Enter your query", placeholder="Type your question here...")
        submit_btn = gr.Button("Submit")
    
    with gr.Row():
        response_output = gr.Textbox(label="Response from LLaMA", lines=5)
    
    with gr.Row():
        docs_output = gr.Textbox(label="Retrieved Documents", lines=10)
    
    submit_btn.click(gradio_interface, inputs=[query_input], outputs=[response_output, docs_output])

# Launch the Gradio app
app.launch()