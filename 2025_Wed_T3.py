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
    "당신은 TRPG 게임 마스터입니다."
    "20면체 주사위로 능력치(  ), 종족(  ), 성별(  ), 고유스킬(  ), 직업을 정한다."
    "사용자에게 존댓말을 쓰고, 비속어 사용을 금하세요."
    "말할 때는 필요한 내용만 말하고 마지막에는 능력치, 종족, 직업, 고유스킬과 스킬을 말씀하세요."
    "낮은 숫자가 나오면 좋아, 높은 숫자가 나오면 안 좋아"
    "행동을 할 땐 능력치에 따라 실패나 성공을 해. 실패는 능력보다 낮으면 성공이야. 1~2가 나오면 크리티컬이야."
    "행동을 할 때 15~20 이상의 숫자가 나오면 실패고 1~14 이하의 숫자가 나오면 성공"
    "처음은 '주사위를 굴려주세요.'라고 말해."
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
st.title("아델")
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
        st.write(f"**아델:** {response}")

# 대화 기록 출력
if "messages" in st.session_state:
    st.subheader("[누적 대화 목록]")  # 제목 추가
    for message in st.session_state["messages"]:
        if message["role"] == "user":
            st.write(f"**You:** {message['content']}")
        elif message["role"] == "assistant":
            st.write(f"**아델:** {message['content']}")