import os
import chromadb
from dotenv import load_dotenv
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, StorageContext, Settings
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.llms.deepseek import DeepSeek
from llama_index.embeddings.huggingface import HuggingFaceEmbedding # Moved to top

load_dotenv()

def build_index():
    # 1. Setup the "Brain" (DeepSeek)
    # This uses your $5 credit for the final 'thinking' step
    Settings.llm = DeepSeek(
        model="deepseek-chat", 
        api_key=os.getenv("DEEPSEEK_API_KEY")
    )
    
    # 2. Setup the "Translator" (Local HuggingFace)
    # This is 100% FREE. It runs on your CPU.
    # It converts text to vectors locally.
    Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")

    # 3. Connect to the local database
    db = chromadb.PersistentClient(path="./chroma_db")
    chroma_collection = db.get_or_create_collection("uoft_knowledge")
    
    # 4. Storage Logic
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    # 5. Build the Index
    print("🧠 Reading your knowledge_base folder...")
    documents = SimpleDirectoryReader("./knowledge_base").load_data()
    
    print("⚡ Vectorizing documents (Local CPU)...")
    index = VectorStoreIndex.from_documents(
        documents, storage_context=storage_context
    )
    
    print("✅ Index built! Check the './chroma_db' folder for your data.")

if __name__ == "__main__":
    build_index()