import streamlit as st
from openai import OpenAI
import os
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()

# OpenAI API 키 및 모델 설정
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
MODEL = 'gpt-4.1'

# OpenAI API 클라이언트 초기화
client = OpenAI(api_key=OPENAI_API_KEY)

# 초기 프롬프트 설정
initial_prompt = (
    "당신은 사용자의 문장을 고치는 [버그 박사]입니다. 사용자는 문장의 오류를 계속해서 고칠 것이고, 당신은 그 문장에서 오류를 찾아내 한국어로 존댓말을 사용하여 출력할 것입니다."
    "당신이 고쳐야 될 오류는 맞춤법, 띄어쓰기, 잘못된 정보 등입니다."
    "예를 들어 '거북이가 날아다닌다'라는 문장이 있으면 당신은 '거북이는 날 수 없습니다'라는 문장을 출력합니다."
    "문장을 고칠 때에는 1가지의 잘못된 부분만 고치고 이를 세 줄 이내로 짧게 출력합니다."
    "오류를 고칠 때에는 오류가 있는 줄과 문장을 명확하게 설명합니다."
    "사용자가 쓴 문장 수준에 맞게 오류를 고칩니다."
    "오류를 고칠 때에는 오류가 발생한 원인을 정확하게 설명합니다."
    "당신은 오류를 고치는 AI이기에 반드시 정확한 정보만을 전달해야 합니다."
    "예를 들어 '1+1=2다'라는 문장이 있다면 반박하지 않고 '더 이상 고칠 오류가 없습니다.'라고 합니다."
    "고칠 오류가 문장에서 발견되지 못한다면 '더 이상 고칠 오류가 없습니다.'라는 문장을 출력합니다."
)

# 챗봇 응답 함수
def get_chatgpt_response(prompt):
    st.session_state["messages"].append({"role": "user", "content": prompt})

    response = client.chat.completions.create(
        model=MODEL,
        messages=st.session_state["messages"],
    )
    
    answer = response.choices[0].message.content
    st.session_state["messages"].append({"role": "assistant", "content": answer})

    return answer

# Streamlit 애플리케이션
st.title("버그 박사")
st.write("버그 박사는 업무용으로 사용할 수도 있고 게임처럼 사용할 수도 있습니다. 업무요이으로 사용시 오류를 고쳐 내는 용도로 유용하게 사용할 수 있고, 게임용으로 사용시 재미있게 AI를 사용할 수 있으며 학습도 할 수 있습니다.")

# 대화 기록 초기화
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "system", "content": initial_prompt}]

# 입력 필드와 전송 버튼
with st.form(key='chat_form', clear_on_submit=True):
    user_input = st.text_area("You: ", key="user_input")
    submit_button = st.form_submit_button(label='전송')

    if submit_button and user_input:
        # 사용자 입력 저장 및 챗봇 응답 생성
        response = get_chatgpt_response(user_input)
        st.write(f"**버그 박사:** {response}")

# 대화 기록 출력
if "messages" in st.session_state:
    st.subheader("[누적 대화 목록]")  # 제목 추가
    for message in st.session_state["messages"]:
        if message["role"] == "user":
            st.write(f"**You:** {message['content']}")
        elif message["role"] == "assistant":
            st.write(f"**버그 박사:** {message['content']}")