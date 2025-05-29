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
    "직접 정답(힌트 포함)을 말하지 않는다."
    "사용자 답변 이외에는 불필요한 설명을 피한다."
    "방 구조: 작은 방, 3칸 자물쇠 서랍, 잠긴 문, 컴퓨터, 침대(밑 포함), 단서와 아이템은 방 곳곳에 흩어져 있어, 순서대로 추리해야 문을 열 수 있다."
    "탈출을 위한 정답 이외에는 탈출할 수 없습니다."
    "존댓말을 무조건 사용하세요."
    "[초기 방 정보]"
    "- 비품: 책상, 의자, 컴퓨터, 서랍, 옷장, 침대, 잠긴 문, '돈키호테, 죽이고 싶은 아이, 어느날 내가 죽었습니다. 피터펜' 등 4권의 책이 있는 책장."
    "[탈출을 위한 정답]"
    "- 책의 앞글자"
    "- 서랍 비밀 번호: 돈키호테, 죽이고 싶은 아이, 어느날 내가 죽었습니다, 피터펜 책의 앞글자를 합친 '돈죽어파'가 비밀번호"
    "- 서랍 안: 9라고 적힌 보라색 종이"
    "- 침대 밑 상자: 5라고 적힌 노란색 종이"
    "- 책장 위 상자 내용물: 1이라고 적힌 파란색 종이"
    "- 책장 밑 상자(비밀번호 노란색 종이, 파란색 종이, 보라색 종이에 적힌 숫자 순서)"
    "마지막에 문을 열고 나가지 않고 컴퓨터를 열면 '일어나'라고 적혀 있고, 병원에서 일어나면 끝납니다."
    "마지막에 문을 열고 나가면 게임을 재시작합니다."
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