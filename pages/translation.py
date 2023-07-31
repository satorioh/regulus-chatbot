import re

import streamlit as st
from llm import init_translator
from config.global_config import (
    MAX_CONTEXT,
    ERROR_RESPONSE,
    DISCLAIMER,
    EMOJI,
    SUPPORTED_TRANSLATE_LANGUAGES
)

st.title(f"Regulus Translator {EMOJI['translation']}")


def get_translator():
    print("get translator")
    return init_translator()


translator = get_translator()


def generate_answer(input, options):
    try:
        languages = " and ".join(options)
        answer = translator.run({"text": input, "languages": languages})
        return answer
    except Exception as e:
        print(e)
        return ERROR_RESPONSE


def translation(input, options):
    try:
        with st.spinner('AI 翻译中...'):
            return generate_answer(input, options)
    except Exception as e:
        print(e)


def translation_page():
    print("run translation page...")
    hint_dom = st.markdown(DISCLAIMER)
    answer_dom = st.empty()
    st.write("")

    def clear_text():
        answer_dom.empty()
        st.session_state["text"] = ""
        hint_dom.markdown(DISCLAIMER)

    def answer_extract(answer):
        pattern = r'\(1\) (\w+\s?\w+)\s\(2\)'
        language = re.findall(pattern, answer)
        table = answer.split("(2)")[1]
        return language, table

    with st.form("translation-form", False):
        # create a prompt text for the text generation
        user_input = st.text_area(label=":thinking_face: 翻译点什么？",
                                  label_visibility="collapsed",
                                  height=100,
                                  max_chars=MAX_CONTEXT,
                                  key="text"
                                  )
        col1, col2 = st.columns([1, 1])
        with col1:
            btn_send = st.form_submit_button(
                "翻译", use_container_width=True, type="primary")
        with col2:
            btn_clear = st.form_submit_button("清除", use_container_width=True, on_click=clear_text)

        options = st.multiselect(
            '目标语种（支持多选）',
            SUPPORTED_TRANSLATE_LANGUAGES)

        if btn_send and user_input != "":
            if len(options) == 0:
                st.warning('请选择目标语种', icon=EMOJI['warning'])
            else:
                answer = translation(user_input, options)
                print(f"翻译：{answer}", flush=True)
                language, table = answer_extract(answer)
                hint_dom.markdown(f"当前输入语种: **{language[0]}**")
                answer_dom.markdown(f"{table}")

        if btn_clear:
            pass


translation_page()
