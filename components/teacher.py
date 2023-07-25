import streamlit as st
from llm import init_teacher
from config.global_config import (
    MAX_CONTEXT,
    EMOJI,
    ERROR_RESPONSE,
    DISCLAIMER
)


def teacher_page():
    print("run teacher page...")
    st.title(f"Regulus English Teacher")
    history_dom = st.empty()
    question_dom = st.markdown(DISCLAIMER)
    answer_dom = st.empty()
    st.write("")

    def get_llm():
        print("get teacher llm")
        return init_teacher()

    if 'teacher' not in st.session_state:
        print("init teacher session")
        teacher, memory = get_llm()
        st.session_state.teacher = teacher
        st.session_state.memory = memory

    def get_history():
        return st.session_state.memory.buffer

    def clear_history():
        print("clear history")
        st.session_state.memory.clear()

    def generate_answer(query):
        try:
            return st.session_state.teacher.run(query)
        except Exception as e:
            print(e)
            return ERROR_RESPONSE

    def display_history():
        history = get_history()
        if history != None:
            text = ""
            for index, item in enumerate(history):
                if index % 2 == 0:
                    text += f"{EMOJI['user']}：{item.content}\n\n{EMOJI['bot']}：{history[index + 1].content}\n\n---\n"
                    history_dom.markdown(text)

    def predict(input):
        try:
            with st.spinner('AI 思考中...'):
                return generate_answer(input)
        except Exception as e:
            print(e)

    with st.form("teacher-form", True):
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
                f"{EMOJI['user']}：{user_input}\n\n")
            answer = predict(user_input)
            print(f"回答：{answer}", flush=True)
            answer_dom.markdown(f"{EMOJI['bot']}：{answer}")

        if btn_clear:
            history_dom.empty()
            clear_history()
