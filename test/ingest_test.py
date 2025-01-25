from dotenv import load_dotenv
import os

load_dotenv()
from langchain_openai import OpenAIEmbeddings
from firecrawl import FirecrawlApp
from langchain_community.document_loaders import FireCrawlLoader
from langchain_pinecone import PineconeVectorStore

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

def retirar_contenido_innecesario(contenido):
    if "###" in contenido:
        index_hashtag = contenido.find("###")
        contenido = contenido[index_hashtag + 3 :]

    if "[Facebook]" in contenido:
        index_facebook = contenido.find("[Facebook]")
        contenido = contenido[:index_facebook]
    return contenido

def firecrawl_test():
    url = "https://acomer.pe/vinagreta-de-polleria/"
    scrape_result = FireCrawlLoader(
        api_key=os.getenv("FIRECRAWL_API_KEY"),
        url=url,
        mode="scrape"
    )
    # Obteniendo "Document object"
    docs = scrape_result.load()
    # Modificando el contenido de los documentos
    docs[0].page_content = retirar_contenido_innecesario(docs[0].page_content)

    contenido = docs[0].page_content
    url_nombre = url.split("/")[-2].replace("-", "_") + ".txt"
    with open(f"../data_web_txt/{url_nombre}", "w", encoding="utf-8") as file:
        file.write(contenido)

    print(f"Agregando {len(docs)} documentos a Pinecone index")
    PineconeVectorStore.from_documents(docs, embeddings, index_name="recetas-peruanas-index")
    print(f"Cargando {url} al vector store de Pinecone")

if __name__ == "__main__":
    firecrawl_test()
