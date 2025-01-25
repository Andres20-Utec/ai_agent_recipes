import pandas as pd
import os
import time
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain_community.document_loaders import FireCrawlLoader
from test.ingest_test import retirar_contenido_innecesario
from dotenv import load_dotenv

load_dotenv()

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

def ingestar_data_url():
    """
    Es necesario tener un mejor plan, ya que el plan gratuito de Pinecone solo permite 1 crawl por minuto
    """
    # Leer data
    df_urls = pd.read_csv("../data/urls_a_comer.csv")
    # Iterar sobre las urls
    for row in df_urls.iterrows():
        url = row[1]["urls"]
        nombre_plato = url.split("/")[-2].replace("-", "_")
        try:
            loader = FireCrawlLoader(
                api_key=os.getenv("FIRECRAWL_API_KEY"),
                url=url,
                mode="scrape",
            )
            docs = loader.load()
            for doc in docs:
                contenido = retirar_contenido_innecesario(doc.page_content)
                doc.page_content = contenido
                # Guardar contenido en un archivo
                with open(f"../data_web_txt/{nombre_plato}.txt", "w", encoding="utf-8") as file:
                    file.write(contenido)
            print(f"Cargando {url} al vector store de Pinecone")
            PineconeVectorStore.from_documents(docs, embeddings, index_name=os.getenv("INDEX_NAME"))
            print("Cargado con éxito")
            print("-" * 80)
            # Agregamos un sleep de 7 segundos para no exceder el límite de crawl
            time.sleep(6.2)
        except Exception as e:
            print("Error al cargar la url: ", url)
            print(e)


if __name__ == "__main__":
    os.makedirs("../data_web_txt", exist_ok=True)
    ingestar_data_url()
