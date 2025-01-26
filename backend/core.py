from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain
from langchain.chains.history_aware_retriever import create_history_aware_retriever
from langchain import hub
from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate
from _prompts import *
from utils import get_vector_db_retriever
from dotenv import load_dotenv

load_dotenv()

def custom_chat_prompt():
    return ChatPromptTemplate(
        messages=[("system", RAG_SYSTEM_PROMPT),
        ("human", USER_PROMPT)]
    )

def run_llm(query: str, messages=[]):

    retriever = get_vector_db_retriever()

    model = ChatOpenAI(model="gpt-4o-mini",verbose=True, temperature=0, max_tokens=1800) # Definir el modelo de chat
    # Prompt usado para agregar información en base a la información retornada por el RAG?
    #retrieval_qa_chat_prompt = hub.pull("langchain-ai/retrieval-qa-chat") # Obtener el ChatPromptTemplate de hub
    retrieval_qa_chat_prompt = custom_chat_prompt()
    stuff_documents_chain = create_stuff_documents_chain(model, retrieval_qa_chat_prompt) # Crear la cadena de documentos

    '''#Agrega contexto en base al historial de conversación para responder a la pregunta siguiente
    #rephrase_prompt = hub.pull("langchain-ai/chat-langchain-rephrase")
    # Recibe un LLM, vector_store_retriever y un prompt que agregará contexto a la respuesta en base al historial de conversación
    history_aware_retriever = create_history_aware_retriever(
        model, retriever, rephrase_prompt
    )'''
    # Dentro de create_retrieval_chain se realiza el invoke al retriever en base al input, luego el resultado es insertado dentro del contexto
    qa = create_retrieval_chain(
        retriever=retriever, combine_docs_chain=stuff_documents_chain
    )

    result = qa.invoke(input={"input": query})
    new_result = {
        "query": result["input"],
        "result": result["answer"],
        "source_documents": result["context"],
    }
    return new_result



if __name__ == "__main__":
    answer = run_llm("Could you give me five ideas to cook a Peruvian dish?")
    print(answer["result"])





