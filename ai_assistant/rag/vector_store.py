import os
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

class VectorDBManager:
    def __init__(self, kb_path: str, index_path: str):
        self.kb_path = kb_path
        self.index_path = index_path
        # Using the requested sentence-transformer model
        self.embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        self.vector_store = None

    def build_index(self):
        print(f"Loading documents from {self.kb_path}...")
        loader = DirectoryLoader(self.kb_path, glob="**/*.md", loader_cls=TextLoader)
        docs = loader.load()
        
        print(f"Chunking {len(docs)} documents...")
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        chunks = text_splitter.split_documents(docs)
        
        print(f"Generating embeddings and building FAISS index for {len(chunks)} chunks...")
        self.vector_store = FAISS.from_documents(chunks, self.embeddings)
        
        os.makedirs(os.path.dirname(self.index_path), exist_ok=True)
        self.vector_store.save_local(self.index_path)
        print(f"FAISS index saved to {self.index_path}")

    def load_index(self):
        if os.path.exists(self.index_path):
            self.vector_store = FAISS.load_local(self.index_path, self.embeddings, allow_dangerous_deserialization=True)
        else:
            print("Index not found. Building new index...")
            self.build_index()

    def get_retriever(self, k=3):
        if not self.vector_store:
            self.load_index()
        return self.vector_store.as_retriever(search_kwargs={"k": k})

if __name__ == "__main__":
    kb = "D:\\health-analytics-ai\\knowledge_base"
    idx = "D:\\health-analytics-ai\\ai_assistant\\faiss_index"
    manager = VectorDBManager(kb, idx)
    manager.build_index()
