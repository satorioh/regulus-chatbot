from langchain.agents import load_tools, ZeroShotAgent, AgentExecutor
from langchain.memory import ConversationBufferWindowMemory
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.tools import Tool
from langchain import LLMChain, LLMMathChain, PromptTemplate
from langchain.chains import ConversationChain, ConversationalRetrievalChain, RetrievalQA
from langchain.chains.summarize import load_summarize_chain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import LLMChainExtractor
from langchain.utilities import GoogleSearchAPIWrapper, SerpAPIWrapper
from langchain.utilities.wolfram_alpha import WolframAlphaAPIWrapper
from config.global_config import (
    OPENAI_API_KEY,
    OPENAI_API_BASE,
    OPENAI_REQUEST_TIMEOUT,
    OPENAI_TEMPERATURE,
    MODEL_NAME,
    SUMMARIZATION_MODEL_NAME,
    AGENT_PREFIX,
    AGENT_SUFFIX,
    DEFAULT_TEMPLATE,
    TRANSLATION_PROMPT,
    LAW_PROMPT_TEMPLATE
)


def init_chatbot():
    print("init chatbot")
    llm = OpenAI(openai_api_key=OPENAI_API_KEY,
                 openai_api_base=OPENAI_API_BASE,
                 temperature=OPENAI_TEMPERATURE,
                 request_timeout=OPENAI_REQUEST_TIMEOUT,
                 model_name=MODEL_NAME)

    memory = ConversationBufferWindowMemory(memory_key="chat_history", k=5)

    # tools = load_tools(["Google Search", "llm-math"], llm=llm)
    # search = GoogleSearchAPIWrapper(k=3)
    search = SerpAPIWrapper(params={"engine": "google",
                                    "google_domain": "google.com",
                                    "gl": "cn",
                                    "hl": "zh-cn", })
    llm_math_chain = LLMMathChain(llm=llm)

    wolfram = WolframAlphaAPIWrapper()

    tools = [
        Tool(
            name="Google Search",
            description="Search Google for current events or recent results.",
            func=search.run,
        ),
        Tool(
            name="Calculator",
            func=wolfram.run,
            description="useful for when you need to answer questions about math or physics. But when the human asked if you can do arithmeti, you just answer 'YES', and do not use this tool",
            return_direct=True,
        )
    ]

    prompt = ZeroShotAgent.create_prompt(
        tools,
        prefix=AGENT_PREFIX,
        suffix=AGENT_SUFFIX,
        input_variables=["input", "chat_history", "agent_scratchpad"],
    )

    first_chain_prompt = PromptTemplate(input_variables=["input", "chat_history"], template=DEFAULT_TEMPLATE)

    conversation = ConversationChain(
        llm=llm,
        memory=memory,
        prompt=first_chain_prompt,
        verbose=True
    )

    llm_chain = LLMChain(llm=llm, prompt=prompt)
    agent = ZeroShotAgent(llm_chain=llm_chain, tools=tools, verbose=True)
    agent_chain = AgentExecutor.from_agent_and_tools(
        agent=agent, tools=tools, verbose=True, memory=memory,
        max_iterations=6,
        handle_parsing_errors="Answer question in Chinese, check your output and make sure it conforms!"
    )
    return conversation, agent_chain, memory


def init_translator():
    llm = OpenAI(openai_api_key=OPENAI_API_KEY,
                 openai_api_base=OPENAI_API_BASE,
                 temperature=0,
                 request_timeout=OPENAI_REQUEST_TIMEOUT,
                 model_name=MODEL_NAME)
    prompt = PromptTemplate(input_variables=["text", "languages"], template=TRANSLATION_PROMPT)
    return LLMChain(llm=llm, prompt=prompt)


def init_law(vectordb):
    print("init law")
    llm = OpenAI(openai_api_key=OPENAI_API_KEY,
                 openai_api_base=OPENAI_API_BASE,
                 temperature=0,
                 request_timeout=OPENAI_REQUEST_TIMEOUT,
                 model_name=MODEL_NAME)

    # memory = ConversationBufferWindowMemory(memory_key="chat_history", k=5)

    prompt = PromptTemplate(
        template=LAW_PROMPT_TEMPLATE,
        input_variables=["context", "question"]
    )

    compressor = LLMChainExtractor.from_llm(llm=llm)
    compression_retriever = ContextualCompressionRetriever(
        base_compressor=compressor,
        base_retriever=vectordb.as_retriever(search_kwargs={"k": 3})
    )

    # law = ConversationalRetrievalChain.from_llm(
    #     llm,
    #     retriever=compression_retriever,
    #     memory=memory,
    #     combine_docs_chain_kwargs={"prompt": prompt},
    #     verbose=True
    # )
    law = RetrievalQA.from_llm(
        llm,
        retriever=compression_retriever,
        prompt=prompt,
        verbose=True
    )
    return law


summary_llm = ChatOpenAI(openai_api_key=OPENAI_API_KEY,
                         openai_api_base=OPENAI_API_BASE,
                         temperature=0,
                         request_timeout=OPENAI_REQUEST_TIMEOUT,
                         model_name=SUMMARIZATION_MODEL_NAME)

# 初始化文本分割器
summary_text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=0
)


def get_youtube_summary(docs):
    prompt_template = """Write a concise summary of the following:


    {text}


    CONCISE SUMMARY IN CHINESE:"""
    PROMPT = PromptTemplate(template=prompt_template, input_variables=["text"])
    refine_template = (
        "Your job is to produce a final summary\n"
        "We have provided an existing summary up to a certain point: {existing_answer}\n"
        "We have the opportunity to refine the existing summary"
        "(only if needed) with some more context below.\n"
        "------------\n"
        "{text}\n"
        "------------\n"
        "Given the new context, refine the original summary in Chinese."
        "If the context isn't useful, return the original summary."
    )
    refine_prompt = PromptTemplate(
        input_variables=["existing_answer", "text"],
        template=refine_template,
    )
    split_documents = summary_text_splitter.split_documents(docs)
    print(f'split_documents:{len(split_documents)}')
    chain = load_summarize_chain(summary_llm, chain_type="refine", verbose=True, question_prompt=PROMPT,
                                 refine_prompt=refine_prompt)
    return chain.run(split_documents)
