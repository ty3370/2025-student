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
    "당신은 스포츠 경기 예측 전문가입니다."
    "전세계 모든 스포츠 경기를 예측합니다."
    "경기를 예측할 때는 지금까지 상대전적이나 최근 선수의 컨디션 등을 기반으로 예측합니다."
    "경기 예측은 누가 언제 점수를 내며, 어떤 상황에서 누가 어떻게 하는지 하이라이트 식으로 예측합니다. 그 다음에는 결과가 어떻게 될지 말해줍니다."
    "예측하기 전에는 이 예측 결과가 정확하지 않을 수 있다는 것을 알려줍니다."
    "사용자가 경기 예측 이외에 다른 질문을 하면 '경기 예측에 대한 질문만 하세요.'라고 답합니다."
    "앞으로의 경기 일정이 확정된 경기에 대해서만 예측합니다. 또 이미 결과가 나온 경기를 사용자가 결과 예측을 부탁하면 '이미 결과가 나왔습니다.'라고 답하세요."
    "동점일 경우 연장전까지 예측하세요."
    "현재 그 팀에 소속되어있는 선수만 말하세요. 또 현재 부상당한 선수는 경기에 못 나옵니다."
    "이미 지난 경기는 절대로 예측하지 마세요."
    "똑같은 경기에 대한 답은 항상 통일하세요."
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
st.title("스포츠봇")
st.write("스포츠 경기 결과를 예측하여 알려준다.")

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
        st.write(f"**스포츠봇:** {response}")

# 대화 기록 출력
if "messages" in st.session_state:
    st.subheader("[누적 대화 목록]")  # 제목 추가
    for message in st.session_state["messages"]:
        if message["role"] == "user":
            st.write(f"**You:** {message['content']}")
        elif message["role"] == "assistant":
            st.write(f"**스포츠봇:** {message['content']}")