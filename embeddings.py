from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Milvus
from config.global_config import (
    ZILLIZ_CLOUD_URI,
    ZILLIZ_CLOUD_USERNAME,
    ZILLIZ_CLOUD_PASSWORD
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
    embeddings = OpenAIEmbeddings()
    vector_db = Milvus.from_documents(
        split_docs,
        embeddings,
        connection_args={
            "uri": ZILLIZ_CLOUD_URI,
            "user": ZILLIZ_CLOUD_USERNAME,
            "password": ZILLIZ_CLOUD_PASSWORD,
            "secure": False,
        },
    )
