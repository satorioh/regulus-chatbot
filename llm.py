from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferWindowMemory
from langchain.agents import load_tools, initialize_agent, AgentType, ZeroShotAgent, AgentExecutor, Tool
from langchain.llms import OpenAI
from langchain import LLMChain
import os

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_API_BASE = os.getenv("BASE_URL")
MODEL_NAME = "gpt-3.5-turbo"

prefix = """Have a conversation with a human, answering the following questions as best you can. You have access to the following tools:"""
suffix = """Begin!"

{chat_history}
Question: {input}
{agent_scratchpad}"""

llm = OpenAI(openai_api_key=OPENAI_API_KEY,
             openai_api_base=OPENAI_API_BASE,
             temperature=0,
             model_name=MODEL_NAME)

tools = load_tools(["llm-math"], llm=llm)

prompt = ZeroShotAgent.create_prompt(
    tools,
    prefix=prefix,
    suffix=suffix,
    input_variables=["input", "chat_history", "agent_scratchpad"],
)

memory = ConversationBufferWindowMemory(memory_key="chat_history", k=5)

llm_chain = LLMChain(llm=OpenAI(temperature=0), prompt=prompt)
agent = ZeroShotAgent(llm_chain=llm_chain, tools=tools, verbose=True)
agent_chain = AgentExecutor.from_agent_and_tools(
    agent=agent, tools=tools, verbose=True, memory=memory,
    handle_parsing_errors="Check your output and make sure it conforms!"
)


def init_agent():
    return agent_chain
