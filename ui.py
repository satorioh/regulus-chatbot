import streamlit as st

st.set_page_config(
    page_title="Regulus Chatbot",
    page_icon=":robot:",
    menu_items={"about": '''
                Author: Robin.Wang
                
                Model: ChatGPT-3.5-tubo
                '''}
)

st.title("Regulus Chatbot👋")
ctx_dom = st.empty()
question_dom = st.markdown(
    ">  回答由 AI 生成，不保证准确率，仅供参考学习！"
)
md_dom = st.empty()
st.write("")
