import streamlit as st
from llm import generate_answer, get_history, clear_history
from config.global_config import (
    MAX_CONTEXT,
    USER_EMOJI,
    BOT_EMOJI
)

st.set_page_config(
    page_title="Regulus Chatbot",
    page_icon=":robot:",
    menu_items={"about": '''
                Author: Robin.Wang

                Model: ChatGPT-3.5-tubo
                '''}
)

st.title(f"Regulus Chatbot {BOT_EMOJI}")
history_dom = st.empty()
question_dom = st.markdown(
    ">  回答由 AI 生成，不保证准确率，仅供参考学习！"
)
answer_dom = st.empty()
st.write("")


def get_answer(query):
    return generate_answer(query)


def display_history():
    history = get_history()
    if history != None:
        text = ""
        for index, item in enumerate(history):
            if index % 2 == 0:
                text += f"{USER_EMOJI}：{item.content}\n\n{BOT_EMOJI}：{history[index + 1].content}\n\n---\n"
                history_dom.markdown(text)


def predict(input):
    try:
        with st.spinner('AI 思考中...'):
            return get_answer(input)
    except Exception as e:
        print(e)


with st.form("form", True):
    # create a prompt text for the text generation
    user_input = st.text_area(label=":thinking_face: 问点什么？",
                              height=100,
                              max_chars=MAX_CONTEXT,
                              placeholder="支持使用 Markdown 格式书写")
    col1, col2 = st.columns([1, 1])
    with col1:
        btn_send = st.form_submit_button(
            "发送", use_container_width=True, type="primary")
    with col2:
        btn_clear = st.form_submit_button("清除历史记录", use_container_width=True)

    if btn_send and user_input != "":
        display_history()
        question_dom.markdown(
            f"{USER_EMOJI}：{user_input}\n\n")
        answer = predict(user_input)
        print(f"回答：{answer}", flush=True)
        answer_dom.markdown(f"{BOT_EMOJI}：{answer}")

        if btn_clear:
            history_dom.empty()
        clear_history()
