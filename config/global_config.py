import os

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_API_BASE = os.getenv("BASE_URL")
MODEL_NAME = "gpt-3.5-turbo"
SUMMARIZATION_MODEL_NAME = "gpt-3.5-turbo-16k"
SUMMARIZATION_MAX_SECONDS = 600
OPENAI_TEMPERATURE = 0.9
OPENAI_REQUEST_TIMEOUT = 240

ZILLIZ_CLOUD_URI = os.getenv("ZILLIZ_CLOUD_URI")
ZILLIZ_CLOUD_USERNAME = os.getenv("ZILLIZ_CLOUD_USERNAME")
ZILLIZ_CLOUD_PASSWORD = os.getenv("ZILLIZ_CLOUD_PASSWORD")
ZILLIZ_CLOUD_COLLECTION_NAME = "laws"

SPEECH_REGION = os.getenv("SPEECH_REGION")
SPEECH_KEY = os.getenv("SPEECH_KEY")

AGENT_PREFIX = """Have a conversation with a human, answering the following questions as best you can. You have access to the following tools:"""
AGENT_SUFFIX = """Begin!"

Current conversation:
{chat_history}
Question: {input}
{agent_scratchpad}"""

DEFAULT_TEMPLATE = """The following is a friendly conversation between a human and an AI. The AI is talkative and provides lots of specific details from its context. Unfortunately, the AI is terrible at maths and current events. When provided with questions about math or current events, no matter how simple, the AI always NOT answer math or current events questions and say 'I do not know'.If the AI does not know the answer to a question, it truthfully says it does not know. 

Current conversation:
{chat_history}
Human: {input}
AI:"""

TRANSLATION_PROMPT = """
Your task is to perform the following actions: 
(1) Tell me the language of the following text delimited by triple backticks, answer using at most 2 words
(2) Translate the following text delimited by triple backticks to {languages}, show result using table with two columns(first column is 'language' which is target language, second column is 'translation' which is translated text)
```{text}```
"""

LAW_PROMPT_TEMPLATE = """你是一个专业的法律顾问，以下是一些提供给你的已知内容，请你简洁和专业的来回答用户的问题，答案请使用中文。

已知内容:
{context}

参考以上内容请回答如下问题:
{question}"""

TEACHER_PROMPT_TEMPLATE = """The following is a friendly conversation between a human and an AI. The AI should act as a spoken English teacher and improver. Human will speak to AI in English and AI will reply to Human in English to practice Human's spoken English. AI should keep the reply neat, limiting the reply to 100 words. AI should strictly correct Human's grammar mistakes, typos, and factual errors. AI should ask Human a question in its reply based on the conversation history below. Now let's start practicing, AI could ask Human a question first. Remember, AI should politely point out Human's grammar mistakes, typos, and factual errors first, and then provide a correct demonstration.

Current conversation:
{chat_history}
Human: {input}
AI:
"""

ERROR_RESPONSE = "我被你问崩溃了，呜呜呜"
DISCLAIMER = ">  回答由 AI 生成，不保证准确率，仅供参考学习！"
SUMMARIZATION_TIME_LIMIT_HINT = "此为演示站点，视频时长请不要超过10分钟"
MAX_CONTEXT = 1000
EMOJI = {
    "user": "🤠",
    "bot": "🤖",
    "translation": "📚",
    "doc": "📖",
    "law": "⚖️",
    "youtube": "",
    "warning": "⚠️",
    "microphone": ":studio_microphone:",
    "keyboard": ":keyboard:"
}
DEFAULT_TRANSLATE_LANGUAGE = ["Chinese (Simplified)"]
SUPPORTED_TRANSLATE_LANGUAGES = [
    "Afrikaans",
    "Albanian",
    "Amharic",
    "Arabic",
    "Armenian",
    "Azerbaijani",
    "Bengali",
    "Bosnian",
    "Bulgarian",
    "Burmese",
    "Cantonese",
    "Catalan",
    "Cebuano",
    "Chinese (Simplified)",
    "Chinese (Traditional)",
    "Corsican",
    "Croatian",
    "Czech",
    "Danish",
    "Dutch",
    "English",
    "Esperanto",
    "Estonian",
    "Fijian",
    "Filipino",
    "Finnish",
    "French",
    "Frisian",
    "Galician",
    "Georgian",
    "German",
    "Greek",
    "Gujarati",
    "Haitian Creole",
    "Hausa",
    "Hawaiian",
    "Hebrew",
    "Hindi",
    "Hmong",
    "Hungarian",
    "Icelandic",
    "Igbo",
    "Indonesian",
    "Irish",
    "Italian",
    "Japanese",
    "Javanese",
    "Kannada",
    "Kazakh",
    "Khmer",
    "Kinyarwanda",
    "Korean",
    "Kurdish",
    "Kyrgyz",
    "Lao",
    "Latin",
    "Latvian",
    "Lithuanian",
    "Luxembourgish",
    "Macedonian",
    "Malagasy",
    "Malay",
    "Malayalam",
    "Maltese",
    "Maori",
    "Marathi",
    "Mongolian",
    "Nepali",
    "Norwegian",
    "Nyanja",
    "Odia",
    "Pashto",
    "Persian",
    "Polish",
    "Portuguese",
    "Punjabi",
    "Romanian",
    "Russian",
    "Samoan",
    "Scots Gaelic",
    "Serbian",
    "Sesotho",
    "Shona",
    "Sindhi",
    "Sinhala",
    "Slovak",
    "Slovenian",
    "Somali",
    "Spanish",
    "Sundanese",
    "Swahili",
    "Swedish",
    "Tagalog",
    "Tajik",
    "Tamil",
    "Tatar",
    "Telugu",
    "Thai",
    "Turkish",
    "Turkmen",
    "Ukrainian",
    "Urdu",
    "Uyghur",
    "Uzbek",
    "Vietnamese",
    "Welsh",
    "Xhosa",
    "Yiddish",
    "Yoruba",
    "Zulu"
]
FAIL_KEYWORDS = ["sorry", "对不起", "抱歉", "不知道", "not know", "不好意思", "无法提供", "无法访问"]
