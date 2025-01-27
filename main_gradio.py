from backend.core import run_llm
import gradio as gr

def answer_query(message, chat_history=[]):
    print(f"Input: {message}. History: {chat_history}")
    history_langchain_format = []

    for i in range(0, len(chat_history), 2):
        humna = chat_history[i]['content']
        ai = chat_history[i + 1]['content']
        history_langchain_format.append(("human", message))
        history_langchain_format.append(("ai", ai))

    if message is not None:
        history_langchain_format.append(("human", message))
        response = run_llm(query=message, chat_history=history_langchain_format)
        history_langchain_format.append(("ai", response["result"]))
        return response["result"]


gr.ChatInterface(fn=answer_query,
                 type="messages",
                 chatbot=gr.Chatbot(height="500px"),
                 textbox=gr.Textbox(placeholder="Write a question ..."),
                 title="Peruvian Chef Bot",
).launch()
