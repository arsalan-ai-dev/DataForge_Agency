from qdrant_client import QdrantClient

# 1. Connect to your local Database
client = QdrantClient("http://localhost:6333")
client.set_model("BAAI/bge-small-en-v1.5") # Turn on the translator

# 2. Ask a question about your PDF!
my_question = "What are the basic concepts of probability?"

print(f"Searching your database for: '{my_question}'...\n")

# 3. Search the memory vault
results = client.query(
    collection_name="agency_documents",
    query_text=my_question,
    limit=1 # Just get the best matching result
)

for result in results:
    print("--- FOUND THIS IN YOUR MEMORY VAULT ---")
    print(result.document)