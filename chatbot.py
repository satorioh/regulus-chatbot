import streamlit as st
from llm import init_chatbot
from utils import (
    check_fail_keywords
)
from config.global_config import (
    MAX_CONTEXT,
    EMOJI,
    ERROR_RESPONSE,
    DISCLAIMER
)

st.set_page_config(
    page_title="Regulus Chatbot",
    page_icon=":robot:",
    menu_items={"about": '''
                Author: Robin.Wang

                Model: ChatGPT-3.5-tubo
                '''}
)


def chatbot_page():
    print("run chatbot page...")
    st.title(f"Regulus Chatbot {EMOJI['bot']}")
    history_dom = st.empty()
    question_dom = st.markdown(DISCLAIMER)
    answer_dom = st.empty()
    st.write("")

    def get_llm():
        print("get llm")
        return init_chatbot()

    if 'conversation' not in st.session_state:
        print("init session")
        conversation, agent_chain, memory = get_llm()
        st.session_state.conversation = conversation
        st.session_state.agent_chain = agent_chain
        st.session_state.memory = memory

    def get_history():
        return st.session_state.memory.buffer

    def clear_history():
        print("clear history")
        st.session_state.memory.clear()

    def delete_recent_history():
        print("delete recent history")
        history = get_history()
        clear_history()
        history = history[:-2]  # 删除最后一次历史对话
        result = [{"input": x.content, "output": y.content} for x, y in zip(history[::2], history[1::2])]
        for item in result:
            st.session_state.memory.save_context({"input": item["input"]}, {"output": item["output"]})

    def generate_answer(query):
        try:
            answer = st.session_state.conversation.run(query)
            if check_fail_keywords(answer):
                delete_recent_history()
                print(f"失败的回答：{answer}")
                print("开始运行 agent...")
                answer = st.session_state.agent_chain.run(query)
            return answer
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
                f"{EMOJI['user']}：{user_input}\n\n")
            answer = predict(user_input)
            print(f"回答：{answer}", flush=True)
            answer_dom.markdown(f"{EMOJI['bot']}：{answer}")

        if btn_clear:
            history_dom.empty()
            clear_history()


chatbot_page()
