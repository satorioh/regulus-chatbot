import os

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_API_BASE = os.getenv("BASE_URL")
MODEL_NAME = "gpt-3.5-turbo"
OPENAI_TEMPERATURE = 0.9
OPENAI_REQUEST_TIMEOUT = 240

AGENT_PREFIX = """Have a conversation with a human, answering the following questions as best you can. After each answer, you should always ask a health related question from the conversation context. You shoud always answer question in Chinese. You have access to the following tools:"""
AGENT_SUFFIX = """Begin!"

Current conversation:
{chat_history}
Question: {input}
{agent_scratchpad}"""

DEFAULT_TEMPLATE = """The following is a friendly conversation between a human and an AI. The AI is talkative and provides lots of specific details from its context. Unfortunately, the AI is terrible at maths and current events. When provided with questions about math or current events, no matter how simple, the AI always NOT answer math or current events questions and say 'I do not know'.If the AI does not know the answer to a question, it truthfully says it does not know. After each answer, the AI should always ask a health related question from its context. 

Current conversation:
{chat_history}
Human: {input}
AI:"""

TRANSLATION_PROMPT = """
Translate the following text to {languages}: \
```{input}``` \

show result using table with two columns(first column is 'language', second column is 'translation')
"""

ERROR_RESPONSE = "我被你问崩溃了，呜呜呜"
MAX_CONTEXT = 1000
USER_EMOJI = "🤠"
BOT_EMOJI = "🤖"
TRANSLATION_EMOJI = "📚"
WARNING_EMOJI = "⚠️"
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
FAIL_KEYWORDS = ["sorry", "对不起", "不知道", "not know", "不好意思", "无法提供", "无法访问"]
