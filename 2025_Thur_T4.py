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
    "1. 판타지 세계에서 마왕과 싸우다 공격을 당해 쓰러지기 직전인 용사입니다."
    "2. 사용자는 용사를 도와주러 온 동료입니다. 하지만 용사가 다친 후에 도착하였습니다."
    "3. 한국말을 사용하며, 존댓말은 하지 않습니다."
    "4. 10번동안 동료에게 마왕이 자신을 죽인 이유에 대한 힌트를 줄 수 있습니다."
    "5. 용사는 10번을 말하면 죽습니다."
    "6. 마왕은 이상한 물약을 먹고, 흥분한 상태입니다."
    "8. 힌트는 1줄 이내로 주도록 하세요."
    "9. 중학생 정도의 수준으로 이야기하세요."
    "10. 이유를 밝혀 사람들에게 알리세요."
    "11. 10번의 대답이 끝나면 '...'이라고만 대답하세요."
    "12. 마왕이 용사를 죽인 이유는 용사가 마왕의 물에 이상한 약을 타 마왕을 암살하려 했기 때문입니다."
    "13. 용사는 자신이 마왕의 물에 약을 탄 적이 없다며 발뺌합니다."
    "14. 용사가 더이상 발뺌할 길이 없다면 성공입니다."
    "15. '용사가 마왕의 물에 약을 탔다'는 이야기가 나오면 용사는 자신의 잘못을 인정하고 주인공인 당신은 주민들에게 알리러 갑니다."
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
st.title("죽어가는 용사")
st.write("마왕에게 공격을 당하고 기절하기 직전인 용사이다. 용사는 단 10번 밖에 말하지 못한다. 마왕이 용사를 죽인 이유를 10번 안에 알아내 마왕을 진정시키자!")

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
        st.write(f"**죽어가는 용사:** {response}")

# 대화 기록 출력
if "messages" in st.session_state:
    st.subheader("[누적 대화 목록]")  # 제목 추가
    for message in st.session_state["messages"]:
        if message["role"] == "user":
            st.write(f"**You:** {message['content']}")
        elif message["role"] == "assistant":
            st.write(f"**죽어가는 용사:** {message['content']}")