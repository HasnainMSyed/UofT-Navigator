import os
import chromadb
from dotenv import load_dotenv
from llama_index.core import VectorStoreIndex, StorageContext, Settings
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.llms.deepseek import DeepSeek
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

load_dotenv()

def start_chat():
    # 1. Re-initialize the same settings as index.py
    Settings.llm = DeepSeek(
        model="deepseek-chat", 
        api_key=os.getenv("DEEPSEEK_API_KEY")
    )
    Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")

    # 2. Reconnect to your local ChromaDB
    db = chromadb.PersistentClient(path="./chroma_db")
    chroma_collection = db.get_or_create_collection("uoft_knowledge")
    
    # 3. Load the index from the existing vector store
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    index = VectorStoreIndex.from_vector_store(vector_store)

    # 4. Create the Chat Engine
    # 'condense_question' mode is great for complex U of T registrar logic
    chat_engine = index.as_chat_engine(chat_mode="condense_question", verbose=True)

    print("\n🎓 U of T Navigator is Online! (Type 'exit' to quit)")
    print("--------------------------------------------------")

    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit", "q"]:
            break
            
        response = chat_engine.chat(user_input)
        print(f"\nNavigator: {response}\n")
        
        # PRO TIP: You can inspect the 'sources' the AI used
        # print(f"Sources: {response.source_nodes}")

if __name__ == "__main__":
    start_chat()