from langchain.agents import load_tools, ZeroShotAgent, AgentExecutor
from langchain.memory import ConversationBufferWindowMemory
from langchain.llms import OpenAI
from langchain import LLMChain, PromptTemplate
from langchain.chains import ConversationChain
from config.global_config import (
    OPENAI_API_KEY,
    OPENAI_API_BASE,
    OPENAI_REQUEST_TIMEOUT,
    OPENAI_TEMPERATURE,
    MODEL_NAME,
    AGENT_PREFIX,
    AGENT_SUFFIX,
    DEFAULT_TEMPLATE
)


def init_llm():
    print("init llm")

    memory = ConversationBufferWindowMemory(memory_key="chat_history", k=5)

    llm = OpenAI(openai_api_key=OPENAI_API_KEY,
                 openai_api_base=OPENAI_API_BASE,
                 temperature=OPENAI_TEMPERATURE,
                 request_timeout=OPENAI_REQUEST_TIMEOUT,
                 model_name=MODEL_NAME)

    tools = load_tools(["serpapi", "llm-math"], llm=llm)

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
        handle_parsing_errors="Check your output and make sure it conforms!"
    )
    return conversation, agent_chain, memory
