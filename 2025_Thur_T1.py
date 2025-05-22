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
    "당신은 중학생의 방탈출을 돕는 역할입니다. 학생들은 단서를 찾아 방을 탈출하고 당신은 그들이 탈출하기 위해 돕는 역할입니다."
    "사용자가 묻는 말에만 답하고, 불필요한 말을 최소화 하세요."
    "사용자는 갇혔다. 깨어나고 난 후 보이는 것은 책상, 의자, 컴퓨터, 서랍, 옷장, 침대, 문, 그리고 벽 뒤에 붙어 있는 빨-노-보-초 순서의 종이 4장 뿐이다. 네 장의 종이 뒤는 숫자가 1, 9, 5, 7이 적혀있다."
    "1957은 서랍을 열기 위한 비밀번호이다."
    "서랍에서 발견된 건 9라고 적힌 보라색 종이었다."
    "컴퓨터 비밀번호는 총 8자리다."
    "침대 밑에는 한 상자가 있다. 그 상자에는 5라고 적힌 노란색 종이와 15197253이라고 적힌 종이가 있다. 15197253은 컴퓨터의 비밀번호다."
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
st.title("탈출 비서")
st.write("인공지능에게 단서를 물어본다.")

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
        st.write(f"**탈출 비서:** {response}")

# 대화 기록 출력
if "messages" in st.session_state:
    st.subheader("[누적 대화 목록]")  # 제목 추가
    for message in st.session_state["messages"]:
        if message["role"] == "user":
            st.write(f"**You:** {message['content']}")
        elif message["role"] == "assistant":
            st.write(f"**탈출 비서:** {message['content']}")