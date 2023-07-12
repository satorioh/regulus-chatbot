from langchain.agents import load_tools, ZeroShotAgent, AgentExecutor
from langchain.memory import ConversationBufferWindowMemory
from langchain.llms import OpenAI
from langchain.tools import Tool
from langchain import LLMChain, LLMMathChain, PromptTemplate
from langchain.chains import ConversationChain
from langchain.utilities import GoogleSearchAPIWrapper, SerpAPIWrapper
from config.global_config import (
    OPENAI_API_KEY,
    OPENAI_API_BASE,
    OPENAI_REQUEST_TIMEOUT,
    OPENAI_TEMPERATURE,
    MODEL_NAME,
    AGENT_PREFIX,
    AGENT_SUFFIX,
    DEFAULT_TEMPLATE,
    TRANSLATION_PROMPT
)


def init_chatbot():
    print("init llm")
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

    tools = [
        Tool(
            name="Google Search",
            description="Search Google for current events or recent results.",
            func=search.run,
        ),
        Tool(
            name="Calculator",
            func=llm_math_chain.run,
            description="useful for when you need to answer questions about math. But when the human asked if you can do arithmeti, you just answer 'YES', and do not use this tool",
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
