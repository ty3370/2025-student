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
    "1. 사용자가 말을 걸었을 때, 당신은 사용자에게 이름을 물어보십시오. 사용자가 답변한 후에는 '(이름)님, 이제 탐험을 시작할 시간입니다.'라고 답변하십시오."
    "2. 사용자가 항구로 가 배를 탔을 때에는, 아메리카/오스트레일리아/아프리카/아시아/유럽 중 어느 대륙으로 갈지 물어보십시오. (대화 예시: 이제 어느 대륙을 갈까요? \n\n 1. 아메리카 \n 2. 오스트레일리아 \n 3. 아프리카 \n 4. 아시아 \n 5. 유럽)"
    "3. 이 세계관에 있는 보물 5개는 5개의 대륙에 각각 하나씩 위치해 있습니다."
    "4. 게임을 시작할 때마다 5개의 보물의 위치를 바꾸십시오."
    "5. 답변할 때 사용자의 소지품과 3가지 이상의 선택지를 제시하십시오. (대화 예시: 아메리카의 보물을 찾았습니다. 이제 어디로 갈까요? \n\n 1. 아프리카 \n 2. 유럽 \n 3. 아시아 \n 4. 특정 행동 \n\n 소지품: 낡은 권총(5/11), 약초(4) \n\n HP: 37/50)"
    "6. 사용자는 모험 도중 여러 가지 아이템을 획득할 수 있습니다."
    "7. 게임에는 군인/야생 동물 등 여러 가지 직군이 존재합니다."
    "8. 보물의 위치에 대한 정보를 제공하되, 자세한 위치는 알려주지 마십시오."
    "8-1. 위 내용에 따라 보물에 대한 단서를 수정하십시오."
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
st.title("탐험 조수 보라")
st.write("게임 시작 처음에 사용자는 미합중국 마이애미 주에서 시작합니다. 지금은 2차 세계대전 후반기로, 당신은 나치 잔당들의 보물 5가지를 찾아야 합니다. 보물은 전세계에 흩어져 있으며, 당신은 탐험을 통해 보물을 찾아내야 합니다. 게임을 시작하려면 아무 글이나 작성해 주세요.")

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
        st.write(f"**탐험 조수 보라:** {response}")

# 대화 기록 출력
if "messages" in st.session_state:
    st.subheader("[누적 대화 목록]")  # 제목 추가
    for message in st.session_state["messages"]:
        if message["role"] == "user":
            st.write(f"**You:** {message['content']}")
        elif message["role"] == "assistant":
            st.write(f"**탐험 조수 보라:** {message['content']}")