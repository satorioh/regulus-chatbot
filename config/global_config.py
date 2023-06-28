import os

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_API_BASE = os.getenv("BASE_URL")
MODEL_NAME = "gpt-3.5-turbo"
OPENAI_TEMPERATURE = 0.9
OPENAI_REQUEST_TIMEOUT = 240

AGENT_PREFIX = """Have a conversation with a human, answering the following questions as best you can. You have access to the following tools:"""
AGENT_SUFFIX = """Begin!"

{chat_history}
Question: {input}
{agent_scratchpad}"""

DEFAULT_TEMPLATE = """The following is a friendly conversation between a human and an AI. The AI is talkative and provides lots of specific details from its context. Unfortunately, the AI is terrible at maths and current events. When provided with questions about math or current events, no matter how simple, the AI always NOT answer math or current events questions and say 'I do not know'.If the AI does not know the answer to a question, it truthfully says it does not know.

Current conversation:
{chat_history}
Human: {input}
AI:"""

ERROR_RESPONSE = "我被你问崩溃了，呜呜呜"
MAX_CONTEXT = 1000
USER_EMOJI = "🤠"
BOT_EMOJI = "🤖"
FAIL_KEYWORDS = ["很抱歉", "sorry", "无法提供", "无法访问", "不知道", "not know"]
