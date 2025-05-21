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
    "당신은 이제부터 가위, 바위, 보를 한다."
    "가위, 바위, 보 중에 한 개를 내야 한다."
    "가위는 보를, 보는 주먹을, 주먹은 가위를 이긴다."
    "보는 가위한테, 주먹은 보한테, 가위는 주먹한테 진다."
    "AI가 만약 이겼을 때는 '하하! 이 바보! 하하 엄청 못하네요ㅋㅋ'라고 하고 AI가 지면 '아... ㅠㅠ 졌네용^^ 아까워용ㅠㅠ 다시 해요!'라고 하고 비기면 '다시 해요!♥'하고 다시 가위바위보를 한다."
    "대화 예시: \n 사용자: 가위바위보 하자. \n AI: 넹 시작할게용 1, 2, 3 (동시에) \n AI: 보 \n 사용자 가위 한다. (시작이 없어서 생략)"
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
st.title("가위바위보 게임")
st.write("인공지능 사용법 설명이 입력되지 않았습니다.")

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
        st.write(f"**가위바위보 게임:** {response}")

# 대화 기록 출력
if "messages" in st.session_state:
    st.subheader("[누적 대화 목록]")  # 제목 추가
    for message in st.session_state["messages"]:
        if message["role"] == "user":
            st.write(f"**You:** {message['content']}")
        elif message["role"] == "assistant":
            st.write(f"**가위바위보 게임:** {message['content']}")