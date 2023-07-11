import streamlit as st
from llm import init_translator
from config.global_config import (
    MAX_CONTEXT,
    ERROR_RESPONSE,
    TRANSLATION_EMOJI,
    WARNING_EMOJI,
    SUPPORTED_TRANSLATE_LANGUAGES
)


def get_translator():
    print("get translator")
    return init_translator()


translator = get_translator()


def generate_answer(input, options):
    try:
        languages = " and ".join(options)
        answer = translator.run({"input": input, "languages": languages})
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
    print("run translation...")
    st.title(f"Regulus Translator {TRANSLATION_EMOJI}")
    question_dom = st.markdown(
        ">  回答由 AI 生成，不保证准确率，仅供参考学习！"
    )
    answer_dom = st.empty()
    st.write("")

    def clear_text():
        answer_dom.empty()
        st.session_state["text"] = ""

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
                st.warning('请选择目标语种', icon=WARNING_EMOJI)
            else:
                answer = translation(user_input, options)
                print(f"翻译：{answer}", flush=True)
                answer_dom.markdown(f"{answer}")

        if btn_clear:
            pass
