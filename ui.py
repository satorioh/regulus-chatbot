import streamlit as st
from llm import init_agent

MAX_CONTEXT = 1000

st.set_page_config(
    page_title="Regulus Chatbot",
    page_icon=":robot:",
    menu_items={"about": '''
                Author: Robin.Wang

                Model: ChatGPT-3.5-tubo
                '''}
)

st.title("Regulus Chatbot👋")
history_dom = st.empty()
question_dom = st.markdown(
    ">  回答由 AI 生成，不保证准确率，仅供参考学习！"
)
answer_dom = st.empty()
st.write("")


@st.cache_resource
def get_agent():
    agent = init_agent()
    return agent


agent = get_agent()


def predict(input):
    return agent.run(input=input)


with st.form("form", True):
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
        btn_clear = st.form_submit_button("清除历史记录", use_container_width=True)

    if btn_send and user_input != "":
        answer = predict(user_input)
        print(f"回答：{answer}", flush=True)
        answer_dom.markdown(answer)
