from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Milvus
from config.global_config import (
    OPENAI_API_KEY,
    OPENAI_API_BASE,
    ZILLIZ_CLOUD_URI,
    ZILLIZ_CLOUD_API_KEY,
    ZILLIZ_CLOUD_COLLECTION_NAME
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

    vector_db = Milvus.from_documents(
        split_docs,
        embeddings,
        collection_name=ZILLIZ_CLOUD_COLLECTION_NAME,
        connection_args={
            "uri": ZILLIZ_CLOUD_URI,
            "token": ZILLIZ_CLOUD_API_KEY,
            "secure": True,
        },
    )
    print("init vector db finished")
