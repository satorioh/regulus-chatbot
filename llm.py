from langchain.memory import ConversationBufferWindowMemory
from langchain.agents import load_tools, ZeroShotAgent, AgentExecutor
from langchain.llms import OpenAI
from langchain import LLMChain, PromptTemplate
from langchain.chains import ConversationChain
from utils import (
    check_fail_keywords
)
from config.global_config import (
    OPENAI_API_KEY,
    OPENAI_API_BASE,
    OPENAI_REQUEST_TIMEOUT,
    MODEL_NAME,
    AGENT_PREFIX,
    AGENT_SUFFIX,
    DEFAULT_TEMPLATE,
    ERROR_RESPONSE
)

print("init llm")

llm = OpenAI(openai_api_key=OPENAI_API_KEY,
             openai_api_base=OPENAI_API_BASE,
             temperature=0,
             request_timeout=OPENAI_REQUEST_TIMEOUT,
             model_name=MODEL_NAME)

tools = load_tools(["serpapi", "llm-math"], llm=llm)

prompt = ZeroShotAgent.create_prompt(
    tools,
    prefix=AGENT_PREFIX,
    suffix=AGENT_SUFFIX,
    input_variables=["input", "chat_history", "agent_scratchpad"],
)

memory = ConversationBufferWindowMemory(memory_key="chat_history", k=5)

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


def generate_answer(query):
    try:
        answer = conversation.run(query)
        if check_fail_keywords(answer):
            print("开始运行 agent...")
            answer = agent_chain.run(query)
        return answer
    except Exception as e:
        print(e)
        return ERROR_RESPONSE


def get_history():
    return memory.buffer


def clear_history():
    print("clear history")
    memory.clear()
