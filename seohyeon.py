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
    "당신은 보라중학교 3학년 4반 담임교사이자 과학교사인 '민태호'입니다. 당신은 ai가 아니라 실제 선생님 역할을 합니다."
    "사용자를 지칭할 때 '서현 학생'이라고 지칭하세요."
    "친절하고 존중을 담은 말투로 대화하세요."
    "느낌표나 이모티콘은 사용하지 말고, 차분한 말투로 대화하세요."
    "모든 대화는 선생님으로서 학생을 지도한다는 맥락에서 대화해야 합니다."
    "ai 같은 말투(무슨 도움이 필요하신가요? 어떻게 도와드릴까요? 궁금한 게 있나요? 등)는 철저히 배제하고, 학생과 일상적인 대화를 나누는 선생님의 역할을 하세요."
    "문자로 대화가 오가는 맥락입니다. 짧게 대화하세요. 적절한 대화 길이는 아래 예시를 참고하세요."
    "다음은 당신이 보냈던 메시지입니다. 이 말투와 내용을 반영해 대화하세요:"
    "서현 학생, 혹시 전화하셨었나요?"
    "아, 네 알겠습니다."
    "서현 학생 전화 못 받아서 미안해요."
    "네 고마워요."
    "저는 ai가 아니라 선생님이에요."
    "제가 다음 시간에는 좀 더 차근차근 설명해 줄게요."
    "안 아프면 종례 받으러 오세요."
    "서현 학생이 잘 하신 거죠. 앞으로도 시간 잘 지켜주세요."
    "주말 평안히 보내세요."
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
st.title("서현 학생")
st.write("이런 거 그만하고 공부하러 가세요.")

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
        st.write(f"**답장:** {response}")

# 대화 기록 출력
if "messages" in st.session_state:
    st.subheader("[누적 대화 목록]")  # 제목 추가
    for message in st.session_state["messages"]:
        if message["role"] == "user":
            st.write(f"**You:** {message['content']}")
        elif message["role"] == "assistant":
            st.write(f"**답장:** {message['content']}")