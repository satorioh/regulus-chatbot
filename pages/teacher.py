import base64
import streamlit as st
from streamlit_chat import message
from llm import init_teacher
from speech_synthesis import (
    text_to_speech,
    speech_to_text
)
from config.global_config import (
    MAX_CONTEXT,
    ERROR_RESPONSE,
    DISCLAIMER,
    EMOJI
)
from utils import (
    save_audio_as_wav
)
from st_custom_components import st_audiorec

st.title(f"Regulus English Teacher")


def teacher_page():
    print("run teacher page...")
    history_dom = st.empty()
    question_dom = st.empty()
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
        st.session_state.audio = []
        st.session_state.show_form = False
        st.session_state.toggle_icon = EMOJI["keyboard"]

    def get_history():
        return st.session_state.memory.buffer

    def clear_history():
        print("clear history")
        st.session_state.memory.clear()
        st.session_state.audio = []

    def generate_answer(query):
        try:
            return st.session_state.teacher.run(query)
        except Exception as e:
            print(e)
            return ERROR_RESPONSE

    def display_history():
        history = get_history()
        if len(history) > 0:
            with history_dom.container():
                for index, item in enumerate(history):
                    even_index = index % 2
                    if even_index == 0:
                        message(item.content, is_user=True, key=f"{index}_user", avatar_style="personas")
                        message(
                            history[index + 1].content,
                            key=f"{index + 1}",
                            avatar_style='micah',
                            allow_html=True
                        )
                        if len(st.session_state.audio) > 0: set_audio_control(
                            st.session_state.audio[int(even_index / 2)])

    def predict(input):
        try:
            with st.spinner('AI 思考中...'):
                return generate_answer(input)
        except Exception as e:
            print(e)

    def set_audio_control(audio_data, autoplay=False):
        b64 = base64.b64encode(audio_data).decode()
        md = f"""
                                    <audio controls {"autoplay" if autoplay else ""} style="margin:-20px 0 0 0px;">
                                    <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
                                    </audio>
                                    """
        st.markdown(
            md,
            unsafe_allow_html=True,
        )

    def toggle_btn_click():
        st.session_state.show_form = not st.session_state.show_form
        st.session_state.toggle_icon = EMOJI["microphone"] if st.session_state.show_form else EMOJI["keyboard"]

    def process(user_input):
        with question_dom.container():
            message(user_input, is_user=True, avatar_style="personas")
        answer = predict(user_input)
        print(f"回答：{answer}", flush=True)
        with answer_dom.container():
            message(answer, avatar_style='micah')
            with st.spinner("AI 语音合成中..."):
                audio_data = text_to_speech(answer)
            set_audio_control(audio_data, True)
            st.session_state.audio.append(audio_data)

    # st.button(st.session_state.toggle_icon, on_click=toggle_btn_click)

    display_history()

    if st.session_state.show_form:
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
                process(user_input)

            if btn_clear:
                history_dom.empty()
                clear_history()
    else:
        wav_audio_data = st_audiorec()
        if wav_audio_data is not None:
            save_audio_as_wav(wav_audio_data, "tmp.wav")
            with st.spinner('AI 聆听中...'):
                user_input = speech_to_text("tmp.wav")
            process(user_input)


teacher_page()
