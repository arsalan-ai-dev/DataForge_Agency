import os
import streamlit as st
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from groq import Groq

# 1. Setup Premium Layout
st.set_page_config(page_title="DataForge Nexus", page_icon="🛡️", layout="wide")

# 2. Load the Vault & AI
load_dotenv()
db_client = QdrantClient("http://localhost:6333")
db_client.set_model("BAAI/bge-small-en-v1.5")
ai_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# 3. Build the Agency Sidebar
with st.sidebar:
    st.title("🛡️ DataForge Agency")
    st.caption("Enterprise AI Intelligence Terminal")
    st.divider()
    st.markdown("**System Status:**")
    st.success("🟢 Memory Vault (Qdrant) Online")
    st.success("🟢 AI Brain (Groq) Online")
    st.success("🟢 Ingestion Engine Online")
    st.divider()
    st.info("System Ready. Querying private document vault.")

# 4. Main Chat Area
st.title("Intelligence Terminal")
st.markdown("Welcome back. I am connected to the DataForge private vault. How can I assist you today?")

# Initialize chat history so the website remembers the conversation
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. The Sleek Chat Input Bar
if user_question := st.chat_input("Query the intelligence vault..."):
    
    # Show the user's question on screen
    with st.chat_message("user"):
        st.markdown(user_question)
    
    # Save the question to history
    st.session_state.messages.append({"role": "user", "content": user_question})

    # Show the AI thinking with a custom icon
    with st.chat_message("assistant"):
        with st.spinner("Scanning private memory vault..."):
            
            # Search Memory
            search_results = db_client.query(
                collection_name="agency_documents",
                query_text=user_question,
                limit=1
            )
            memory_context = search_results[0].document if search_results else "No memory found."
            
            # Ask the Groq AI (with a slightly more elite system prompt)
            chat_completion = ai_client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": f"You are an elite, highly professional AI advisor for the DataForge Agency. Answer the user's query intelligently using ONLY the information provided in this extracted document context. Context: {memory_context}"
                    },
                    {
                        "role": "user",
                        "content": user_question
                    }
                ],
                model="llama-3.1-8b-instant",
            )
            
            ai_answer = chat_completion.choices[0].message.content
            
            # Draw the answer
            st.markdown(ai_answer)
            
    # Save the AI's answer to history
    st.session_state.messages.append({"role": "assistant", "content": ai_answer})