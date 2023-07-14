import streamlit as st
from components.chatbot import chatbot_page
from components.translation import translation_page
from components.chatdoc import chatdoc_page

st.set_page_config(
    page_title="Regulus Chatbot",
    page_icon=":robot:",
    menu_items={"about": '''
                Author: Robin.Wang

                Model: ChatGPT-3.5-tubo
                '''}
)

tab1, tab2, tab3 = st.tabs(["聊天", "翻译", "文档问答"])

with tab1:
    chatbot_page()

with tab2:
    translation_page()

with tab3:
    chatdoc_page()
