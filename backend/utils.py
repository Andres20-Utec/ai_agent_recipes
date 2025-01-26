from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from dotenv import load_dotenv
import os
load_dotenv()

def get_vector_db_retriever():
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")  # Definir el modelo de embeddings
    docsearch = PineconeVectorStore(index_name=os.getenv("INDEX_NAME"), embedding=embeddings)  # Definir el vector store
    return docsearch.as_retriever()