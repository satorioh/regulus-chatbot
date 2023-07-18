import streamlit as st
from llm import init_law
from config.global_config import (
    MAX_CONTEXT,
    EMOJI,
    ERROR_RESPONSE,
    DISCLAIMER
)
from embeddings import get_embeddings


def laws_page():
    print("run laws page...")
    st.title(f"Regulus Law Helper {EMOJI['law']}")
    history_dom = st.empty()
    question_dom = st.markdown(DISCLAIMER)
    answer_dom = st.empty()
    st.write("")

    @st.cache_resource
    def get_vector_store():
        return get_embeddings()

    vector_store = get_vector_store()

    def get_law():
        print("get law llm")
        return init_law(vector_store)

    if 'law' not in st.session_state:
        print("init law session")
        law = get_law()
        st.session_state.law = law
        # st.session_state.memory = memory

    def get_history():
        return st.session_state.memory.buffer

    def clear_history():
        print("clear history")
        # st.session_state.memory.clear()
        question_dom.empty()
        answer_dom.empty()

    def generate_answer(question):
        try:
            return st.session_state.law({"query": question})
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

    with st.form("law-form", True):
        # create a prompt text for the text generation
        user_input = st.text_area(label=":thinking_face: 咨询点什么？",
                                  height=100,
                                  max_chars=MAX_CONTEXT,
                                  placeholder="支持使用 Markdown 格式书写")
        col1, col2 = st.columns([1, 1])
        with col1:
            btn_send = st.form_submit_button(
                "发送", use_container_width=True, type="primary")
        with col2:
            btn_clear = st.form_submit_button("清除", use_container_width=True)

        if btn_send and user_input != "":
            # display_history()
            question_dom.markdown(
                f"{EMOJI['user']}：{user_input}\n\n")
            res = predict(user_input)
            print(f"法律回答：{res}", flush=True)
            answer_dom.markdown(f"{EMOJI['bot']}：{res['result']}")

        if btn_clear:
            # history_dom.empty()
            clear_history()
