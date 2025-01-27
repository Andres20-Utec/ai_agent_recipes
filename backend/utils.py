from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain.prompts import ChatPromptTemplate
from dotenv import load_dotenv
from ._prompts import *
import os

load_dotenv()


def get_vector_db_retriever():
    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small"
    )  # Definir el modelo de embeddings
    docsearch = PineconeVectorStore(
        index_name=os.getenv("INDEX_NAME"), embedding=embeddings
    )  # Definir el vector store
    return docsearch.as_retriever()


def custom_chat_prompt():
    return ChatPromptTemplate(
        messages=[("system", RAG_SYSTEM_PROMPT), ("human", USER_PROMPT)]
    )
