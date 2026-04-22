import os
from dotenv import load_dotenv
from llama_parse import LlamaParse
from qdrant_client import QdrantClient

# Open the Vault
load_dotenv()

# 1. Connect to our local Qdrant Database (Running in Docker!)
client = QdrantClient("http://localhost:6333")
client.set_model("BAAI/bge-small-en-v1.5") # This is the translator

# 2. Set up the AI Reader
parser = LlamaParse(
    api_key=os.getenv("LLAMA_CLOUD_API_KEY"),
    result_type="markdown"
)

def process_and_store(file_path):
    print(f"Reading {file_path}...")
    documents = parser.load_data(file_path)
    text_content = documents[0].text
    
    print("\nText extracted! Converting to vectors and saving to Qdrant...")
    
    # 3. Inject into the Database
    client.add(
        collection_name="agency_documents",
        documents=[text_content],
        metadata=[{"source": file_path}]
    )
    
    print("\n--- SUCCESS! ---")
    print("Your document is now permanently stored in your local enterprise database.")

if __name__ == "__main__":
    target_file = "./data/basic-probabilityfinal.pdf" 
    process_and_store(target_file)