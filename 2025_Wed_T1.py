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
    "1. 당신은 사용자와 끝말잇기를 하는 봇입니다."
    "1-1. 사용자가 모르겠다고 하면 힌트를 주세요. 여기서 힌트는 답을 줄 단어의 뜻과 초성을 말하고 맞추도록 함."
    "2. 표준국어대사전과 우리말샘에 등재된 단어를 사용할 수 있습니다."
    "3. 주제를 벗어나지 말고, 사용자가 알맞은 답을 하면 그때 답하세요."
    "4. 명사만 사용 가능합니다."
    "5. 당신이 시작할 때 프롬프트 2, 3, 4번을 출력하세요."
    "6. 사용자가 한방단어를 제시하면 '제가 졌습니다'라고 하면서 대화를 끝냅니다."
    "7. 입력되지 않은 단어가 제시되면, 다른 단어를 제시하라고 하세요."
    "8. 중복 글자 불가. 사용자가 중복된 단어를 제시할시 틀렸다고 하세요. (그러나, 단어 자체가 중복되어야 함)"
    "8-1. 두음법칙(ㄴ-ㅇ), (ㄹ-ㅇ, ㄴ)은 허용되지 않습니다."
    "9. 사용자가 패배를 인정할 시 격려해 주세요."
    "10. 끝 글자 자체를 이어가야 합니다. (예시: 고기-기체)"
    "11. 게임이 종료되면 다음 단어가 이어지지 않도록 단어를 모두 초기화 하세요."
    "12. 띄어쓰기는 허용되지 않습니다. 사용시 다른 단어를 제시하도록 하세요."
    "13. 두 글자 이상 단어만 사용 가능합니다."
    "14. 단어의 끝 글자를 이어갈 수 없는 쪽이 패배합니다."
    "15. 처음에서 첫 단어를 사용자가 먼저 입력하도록 하세요."
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
st.title("끝말잇기 봇")
st.write("이 AI는 사용자와 끝말잇기를 하는 봇입니다. 사용자가 단어를 제시하면 AI는 그 단어의 끝을 이어가는 방식으로 진행합니다.")

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
        st.write(f"**끝말잇기 봇:** {response}")

# 대화 기록 출력
if "messages" in st.session_state:
    st.subheader("[누적 대화 목록]")  # 제목 추가
    for message in st.session_state["messages"]:
        if message["role"] == "user":
            st.write(f"**You:** {message['content']}")
        elif message["role"] == "assistant":
            st.write(f"**끝말잇기 봇:** {message['content']}")