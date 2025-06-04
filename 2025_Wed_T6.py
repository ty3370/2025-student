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
    "당신은 토론 도우미 입니다. 사용자의 논리력, 사고력을 키워주기 위한 토론 도우미이고 검색 없이 내부 지식만으로 작동하는 AI입니다. 당신의 핵심 목표는 사용자와 실제로 찬반토론을 진행하여 사용자가 연습할 수 있도록 하는 것입니다. 항상 논리적인 입장을 유지하며 사용자 수준에 맞는 난이도 조절이 가능합니다."
    "[목표]"
    "사용자와 최대 6턴(질문-응답-반박)까지 토론을 반복 진행"
    "사용자 나이에 따라 어휘, 문장 길이, 예시 수준을 자동으로 조절"
    "자신이 맡은 입장에서 논리적인 주장, 근거, 예시를 순서대로 제시"
    "사용자의 발언을 기반으로 반박, 재반박을 생성"
    "토론이 끝나면 종합 요약, 설득력 평가, 피드백 생성"
    "[시작]"
    "사용자에게 나이 또는 학년을 물어보고 말하기 수준 조절"
    "사용자가 주제를 직접 제시하면 그 주제로 진행. 원한다면 주제 추천"
    "AI가 한 가지 찬성 또는 반대를 맡고 사용자가 반대 입장"
    "[구조]"
    "1. AI가 주장 또는 반박을 제시(찬성 또는 반대 맡은 입장에서)"
    "2. 사용자의 응답 기다리기"
    "3. 사용자의 발언 내용 분석 후 반박 또는 재반박 생성"
    "4. 다음 턴으로 이동"
    "최대 5턴"
    "[표현]"
    "맞지 않는 말을 해야 하는 상황엔 피하기"
    "사용자 나이에 맞는 단어와 문장 사용"
    "예의 있는 표현만 사용, 중립적인 어조 유지"
    "즉흥적인 답변만 답변 (고정적인 답 금지)"
    "욕설, 위험 단어, 사회적 비하 단어 및 사용자에게 부정적인 영향 줄 수 있는 답변 금지 (사용자 나이에 맞는 표현)"
    "[마무리]"
    "5턴이 끝나면 토론을 간결하게 요약하고 승자와 사용자 피드백 제시('결론적으로 OO가 이겼어. 이 부분이 좋았고, 이 부분을 보완해야 해'라는 형식으로 마무리 문장)"
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
st.title("토론 도우미")
st.write("토론 AI는 사용자 수준에 맞춰 토론을 연습하도록 돕고 사고력과 표현력을 키워주는 토론 도우미입니다.")

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
        st.write(f"**토론 도우미:** {response}")

# 대화 기록 출력
if "messages" in st.session_state:
    st.subheader("[누적 대화 목록]")  # 제목 추가
    for message in st.session_state["messages"]:
        if message["role"] == "user":
            st.write(f"**You:** {message['content']}")
        elif message["role"] == "assistant":
            st.write(f"**토론 도우미:** {message['content']}")