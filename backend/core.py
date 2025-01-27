from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain
from langchain.chains.history_aware_retriever import create_history_aware_retriever
from langchain import hub
from .utils import get_vector_db_retriever, custom_chat_prompt
from dotenv import load_dotenv
from typing import List, Dict

load_dotenv()


def run_llm(
    query: str,
    chat_history=List[Dict[str, any]],
    temperature: float = 0.0,
    max_tokens: int = 1800,
):

    retriever = get_vector_db_retriever()

    model = ChatOpenAI(
        model="gpt-4o-mini",
        verbose=True,
        temperature=temperature,
        max_tokens=max_tokens,
    )  # Definir el modelo de chat
    retrieval_qa_chat_prompt = custom_chat_prompt()
    stuff_documents_chain = create_stuff_documents_chain(
        model, retrieval_qa_chat_prompt
    )  # Crear la cadena de documentos

    # Agrega contexto en base al historial de conversación para responder a la pregunta siguiente
    rephrase_prompt = hub.pull("langchain-ai/chat-langchain-rephrase")
    # Recibe un LLM, vector_store_retriever y un prompt que agregará contexto a la respuesta en base al historial de conversación
    history_aware_retriever = create_history_aware_retriever(
        model, retriever, rephrase_prompt
    )
    # Dentro de create_retrieval_chain se realiza el invoke al retriever en base al input, luego el resultado es insertado dentro del contexto
    qa = create_retrieval_chain(
        retriever=history_aware_retriever, combine_docs_chain=stuff_documents_chain
    )

    result = qa.invoke(input={"input": query, "chat_history": chat_history})

    new_result = {
        "query": result["input"],
        "result": result["answer"],
        "source_documents": result["context"],
    }
    return new_result


if __name__ == "__main__":
    while True:
        question = input("Ask me anything: ")
        if question == "exit":
            break
        answer = run_llm(question)
        print(answer["result"])
