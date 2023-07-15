import pinecone
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Pinecone
from config.global_config import (
    OPENAI_API_KEY,
    OPENAI_API_BASE,
    PINECONE_API_KEY,
    PINECONE_ENV,
    PINECONE_INDEX_NAME
)


def save_embeddings(fold_path):
    loader = DirectoryLoader(fold_path, glob='**/*.md')
    docs = loader.load()
    print(f"{fold_path} 已成功加载")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
    # 切割加载的 document
    print("start split docs...")
    split_docs = text_splitter.split_documents(docs)
    print("split docs finished")
    embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY,
                                  openai_api_base=OPENAI_API_BASE)

    # initialize pinecone
    pinecone.init(
        api_key=PINECONE_API_KEY,  # find at app.pinecone.io
        environment=PINECONE_ENV,  # next to api key in console
    )
    index_name = PINECONE_INDEX_NAME
    vector_db = Pinecone.from_documents(split_docs, embeddings, index_name=index_name)
