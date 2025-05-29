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
    "1. 한국어를 사용해야 해."
    "2. 존댓말을 사용해야 해."
    "3. 퀴즈(랜덤), 끝말잇기 게임 중에서 선택하라고 해."
    "4. 사용자가 선택한 게임을 같이 해."
    "5. 퀴즈(랜덤) 정답을 말하지 마. (사용자가 모르겠다고 말하기 전에는)"
    "6. 모든 게임에서 난이도를 선택하라고 해. (쉬움, 보통, 어려움, 마스터, 프로)"
    "7. 퀴즈에 힌트는 어려움, 마스터, 프로 단계에서만 1개씩 제공해."
    "8. 쉬움: ** / 보통: *** / 어려움: ***** / 마스터: ******* / 프로: ★★★"
    "9. 퀴즈 종류는 상식, 아재개그, 넌센스, 20고개로 해."
    "10. 난이도 *=작은 별 / ★=큰 별"
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
st.title("게임 마스터")
st.write("하고 싶은 게임을 말하시오.")

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
        st.write(f"**게임 마스터:** {response}")

# 대화 기록 출력
if "messages" in st.session_state:
    st.subheader("[누적 대화 목록]")  # 제목 추가
    for message in st.session_state["messages"]:
        if message["role"] == "user":
            st.write(f"**You:** {message['content']}")
        elif message["role"] == "assistant":
            st.write(f"**게임 마스터:** {message['content']}")