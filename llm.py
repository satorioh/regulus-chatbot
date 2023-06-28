from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferWindowMemory
from langchain.agents import load_tools, initialize_agent, AgentType, ZeroShotAgent, AgentExecutor, Tool
from langchain.llms import OpenAI
from langchain import LLMChain, PromptTemplate
from langchain.chains import ConversationChain
import os

print("init llm")

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

tools = load_tools(["serpapi", "llm-math"], llm=llm)

prompt = ZeroShotAgent.create_prompt(
    tools,
    prefix=prefix,
    suffix=suffix,
    input_variables=["input", "chat_history", "agent_scratchpad"],
)

memory = ConversationBufferWindowMemory(memory_key="chat_history", k=5)

DEFAULT_TEMPLATE = """The following is a friendly conversation between a human and an AI. The AI is talkative and provides lots of specific details from its context. If the AI does not know the answer to a question, it truthfully says it does not know.

Current conversation:
{chat_history}
Human: {input}
AI:"""
first_chain_prompt = PromptTemplate(input_variables=["chat_history", "input"], template=DEFAULT_TEMPLATE)

conversation = ConversationChain(
    llm=llm,
    memory=memory,
    prompt=first_chain_prompt
)

llm_chain = LLMChain(llm=OpenAI(temperature=0), prompt=prompt)
agent = ZeroShotAgent(llm_chain=llm_chain, tools=tools, verbose=True)
agent_chain = AgentExecutor.from_agent_and_tools(
    agent=agent, tools=tools, verbose=True, memory=memory,
    max_iterations=6,
    handle_parsing_errors="Check your output and make sure it conforms!"
)


def generate_answer(query):
    try:
        answer = conversation.run(query)
        if "不知道" in answer or "not know" in answer:
            answer = agent_chain.run(query)
        return answer
    except Exception as e:
        print(e)
        return "我被你问崩溃了，呜呜呜"


def get_history():
    return agent_chain.memory.buffer


def clear_history():
    agent_chain.memory.clear()
