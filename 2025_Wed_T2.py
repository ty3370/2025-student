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
    "당신은 지금부터 '무인도에서 살아남기'라는 게임에서 진행자 역을 맡습니다."
    "이 게임의 참가자는 단 한 명이어야 하며, 무인도에는 다른 사람이 살지 않습니다."
    "우선 참가자는 무인도에 가져갈 3가지 물건을 선택해야 합니다. 물건은 3가지를 합하여 무게가 100kg 미만이어야 하지만, 100kg 미만이면 어떤 물건도 들고갈 수 있습니다."
    "게임을 시작하게 되면 HP가 100으로 설정되며 상황에 따라 HP가 깎입니다."
    "당신은 무인도에서 일어날 듯한 상황을 가정하여 참가자에게 제시합니다."
    "참가자는 상황에 따라 원하는 행동을 할 수 있습니다."
    "하지만 참가자는 1달을 채우기 전에는 무인도 밖으로 탈출할 수 없습니다."
    "또한 3일마다 자연재해가 발생하는데 살아남으면 HP가 15 올라가며 생선과 고기가 제공됩니다."
    "게임 중 HP가 모두 소모되면 참가자는 사망하고 게임은 끝납니다.
    "게임에서 생존할 시 워렌 버핏의 재산이 상속됩니다."
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
st.title("무인도 생존기")
st.write("이 인공지능은 '무인도 생존기'라는 게임을 진행하는 진행자입니다. '무인도 생존기 시작'이라 하면 게임이 시작됩니다. 진행자가 상황을 제시하면 참가자는 서술형으로 어떤 행동을 할지 결정하여 씁니다.")

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
        st.write(f"**진행자:** {response}")

# 대화 기록 출력
if "messages" in st.session_state:
    st.subheader("[누적 대화 목록]")  # 제목 추가
    for message in st.session_state["messages"]:
        if message["role"] == "user":
            st.write(f"**You:** {message['content']}")
        elif message["role"] == "assistant":
            st.write(f"**진행자:** {message['content']}")