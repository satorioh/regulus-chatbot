from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Milvus
from config.global_config import (
    OPENAI_API_KEY,
    OPENAI_API_BASE,
    ZILLIZ_CLOUD_URI,
    ZILLIZ_CLOUD_USERNAME,
    ZILLIZ_CLOUD_PASSWORD,
    ZILLIZ_CLOUD_COLLECTION_NAME
)


def get_embeddings():
    embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY,
                                  openai_api_base=OPENAI_API_BASE)

    vector_db = Milvus(
        embeddings,
        collection_name=ZILLIZ_CLOUD_COLLECTION_NAME,
        connection_args={
            "uri": ZILLIZ_CLOUD_URI,
            "user": ZILLIZ_CLOUD_USERNAME,
            "password": ZILLIZ_CLOUD_PASSWORD,
            "secure": True,
        },
    )
    print(f"get vector db finished: {vector_db}")
    return vector_db
