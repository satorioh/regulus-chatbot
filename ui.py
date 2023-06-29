import streamlit as st
from langchain.memory import ConversationBufferWindowMemory
from llm import init_llm
from utils import (
    check_fail_keywords
)
from config.global_config import (
    MAX_CONTEXT,
    USER_EMOJI,
    BOT_EMOJI,
    ERROR_RESPONSE,
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

if 'memory' not in st.session_state:
    print("init session memory")
    st.session_state.memory = ConversationBufferWindowMemory(memory_key="chat_history", k=5)


@st.cache_resource
def get_llm():
    print("get llm")
    return init_llm(st.session_state.memory)


conversation, agent_chain = get_llm()


def get_history():
    return st.session_state.memory.buffer


def clear_history():
    print("clear history")
    st.session_state.memory.clear()


def delete_recent_history():
    print("delete_recent_history")
    history = get_history()
    clear_history()
    history = history[:-2]  # 删除最后一次历史对话
    result = [{"input": x.content, "output": y.content} for x, y in zip(history[::2], history[1::2])]
    for item in result:
        st.session_state.memory.save_context({"input": item["input"]}, {"output": item["output"]})


def generate_answer(query):
    try:
        answer = conversation.run(query)
        if check_fail_keywords(answer):
            delete_recent_history()
            print(f"失败的回答：{answer}")
            print("开始运行 agent...")
            answer = agent_chain.run(query)
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
                text += f"{USER_EMOJI}：{item.content}\n\n{BOT_EMOJI}：{history[index + 1].content}\n\n---\n"
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
            f"{USER_EMOJI}：{user_input}\n\n")
        answer = predict(user_input)
        print(f"回答：{answer}", flush=True)
        answer_dom.markdown(f"{BOT_EMOJI}：{answer}")

        if btn_clear:
            history_dom.empty()
            clear_history()
