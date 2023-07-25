import streamlit as st
from components.chatbot import chatbot_page
from components.translation import translation_page
from components.laws import laws_page
from components.youtube import youtube_page
from components.teacher import teacher_page

st.set_page_config(
    page_title="Regulus Chatbot",
    page_icon=":robot:",
    menu_items={"about": '''
                Author: Robin.Wang

                Model: ChatGPT-3.5-tubo
                '''}
)

tab1, tab2, tab3, tab4, tab5 = st.tabs(["聊天", "翻译", "法律助手", "油管总结", "英语私教"])

with tab1:
    chatbot_page()

with tab2:
    translation_page()

with tab3:
    laws_page()

with tab4:
    youtube_page()

with tab5:
    teacher_page()
