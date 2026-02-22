import streamlit as st
import os
import chromadb
from dotenv import load_dotenv

# Logic: We reuse our "Brain" tools from chat.py
from llama_index.core import VectorStoreIndex, StorageContext, Settings
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.llms.deepseek import DeepSeek
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

# streamlit run app.py

# 1. Page Configuration (The "Look and Feel")
st.set_page_config(page_title="U of T Navigator", page_icon="🎓", layout="centered")
st.title("🎓 U of T Navigator")
st.markdown("---")

# 2. Load Environment Variables (API Keys)
load_dotenv()

# 3. Cached Data Loading (Ownership: @st.cache_resource prevents reloading on every click)
@st.cache_resource(show_spinner=False)
def initialize_engine():
    # Setup the logic identical to index.py/chat.py
    Settings.llm = DeepSeek(
        model="deepseek-chat", 
        api_key=os.getenv("DEEPSEEK_API_KEY")
    )
    Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")

    # Connect to the local folder on your Ubuntu drive
    db = chromadb.PersistentClient(path="./chroma_db")
    chroma_collection = db.get_or_create_collection("uoft_knowledge")
    
    # Bridge to LlamaIndex
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    index = VectorStoreIndex.from_vector_store(vector_store)

    # Return the engine with our specific "U of T Persona"
# Change the return statement in initialize_engine
    return index.as_chat_engine(
        chat_mode="condense_plus_context", # Switched from condense_question
        system_prompt=(
            "You are a helpful U of T academic advisor. "
            "Use the provided context to answer questions about scholarships and campus life. "
            "Be specific, and if you don't know the answer based on the context, "
            "honestly say so and direct them to the appropriate registrar. "
            "Always cite the source URL if available."
        ),
        verbose=True
    )

# 4. Initialize the Chat Engine once
if "chat_engine" not in st.session_state:
    with st.spinner("Waking up the Navigator..."):
        st.session_state.chat_engine = initialize_engine()

# 5. Chat History Management
# We store the conversation so it stays on the screen
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! I'm your U of T Navigator. Ask me anything about scholarships or campus info."}
    ]

# 6. Display Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 7. User Input & Response Logic
if prompt := st.chat_input("How can I help you today?"):
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate and display assistant response
    with st.chat_message("assistant"):
        with st.spinner("Searching official U of T docs..."):
            response = st.session_state.chat_engine.chat(prompt)
            st.markdown(response.response)
            
            # Add assistant response to history
            st.session_state.messages.append({"role": "assistant", "content": response.response})