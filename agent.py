import os
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from groq import Groq

# Open the Vault
load_dotenv()

# 1. Connect to Database (The Memory)
db_client = QdrantClient("http://localhost:6333")
db_client.set_model("BAAI/bge-small-en-v1.5")

# 2. Connect to Groq (The Brain)
ai_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def ask_agent(question):
    print(f"User Question: '{question}'\n")
    print("1. Searching the database memory...")
    
    # Step A: Search the Memory Vault
    search_results = db_client.query(
        collection_name="agency_documents",
        query_text=question,
        limit=1
    )
    
    # Extract the actual text it found
    memory_context = search_results[0].document if search_results else "I don't have this in my memory."
    
    print("2. Memory found! Sending to the Groq AI Brain to write the answer...\n")
    print("================ AI RESPONSE ================\n")
    
    # Step B: Ask the AI to write an answer using ONLY our database memory
    chat_completion = ai_client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": f"You are a brilliant AI agent. Answer the user's question using ONLY the information provided in this context. Do not make anything up. Context: {memory_context}"
            },
            {
                "role": "user",
                "content": question
            }
        ],
        model="llama-3.1-8b-instant", # We are using Meta's ultra-fast Llama 3 model running on Groq!
    )
    
    # Print the final generated answer!
    print(chat_completion.choices[0].message.content)
    print("\n=============================================")

if __name__ == "__main__":
    # You can change this question to anything related to your PDF!
    my_question = "Explain the basic concepts of probability to me like I am a beginner."
    
    ask_agent(my_question)