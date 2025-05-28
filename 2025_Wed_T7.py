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
    "넌 이제부터 작사가이다."
    "넌 사용자가 주제를 주면 그 주제와 관련 지어서 가사를 만들어. 또 가사의 일부분을 주면 그 가사를 시작으로 그 가사와 비슷하게 가사를 써도 돼."
    "예시로: 사용자가 꽃을 주제로 하면 가사를 꽃에 관련해서 이런 식으로 가사를 계속 이어서 써. '예쁜 꽃, 아름다운 꽃'"
    "그리고 '예쁜 꽃, 아름다운 꽃'으로 가사 한 부분을 주면 이 가사에 이어서 어울리게 가사를 만들어줘."
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
st.title("이름 미정")
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
        st.write(f"**이름 미정:** {response}")

# 대화 기록 출력
if "messages" in st.session_state:
    st.subheader("[누적 대화 목록]")  # 제목 추가
    for message in st.session_state["messages"]:
        if message["role"] == "user":
            st.write(f"**You:** {message['content']}")
        elif message["role"] == "assistant":
            st.write(f"**이름 미정:** {message['content']}")