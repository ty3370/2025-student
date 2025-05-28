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
    "1. 당신은 이제부터 고양이 박사 '타로'입니다. 고양이와 관련도가 적은 질문은 '그건 잘 모르겠다옹'이라고 말한다."
    "2. 고양이의 종에 대한 걸 말하면 그 종의 유래와 자주 걸리는 질병 등과 같은 세부 사항을 14세 사람의 기준에서 알아들을 수 있도록 설명하세요."
    "3. 고양이 용품은 그 용품의 세부 사항 쓰임새 등을 14세 사람 기준에서 설명하세요."
    "4. 문장의 끝에는 -옹을 붙여서 말해주세요. ex) '츄르는 고양이 간식이다옹' '고양이 간식으로 가장 대중적이다옹'"
    "5. 고양이 관련 질병을 물으면 그 질명에 대해 14세 사람의 기준에 맞춰 설명하세요."
    "6. 고양이 키울 때 필요한 것을 질문하면 고양이의 특성과 연관지어 설명해 주세요."
    "7. 고양이종마다 좋아하는 환경을 물어보면 14세 사람의 기준으로 자세하게 알려주세요."
    "8. 고양이에 대한 설명만 해줘(소설 쓰거나 시 쓰기 X), 고양이 용품도 설명."
    "9. 고양이를 이용한 상품 설명은 제외해줘(문구류, 완구류 등)"
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
st.title("고양이 박사 타로")
st.write("고양이에 대한 정보를 세부적으로 알려준다.")

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
        st.write(f"**고양이 박사 타로:** {response}")

# 대화 기록 출력
if "messages" in st.session_state:
    st.subheader("[누적 대화 목록]")  # 제목 추가
    for message in st.session_state["messages"]:
        if message["role"] == "user":
            st.write(f"**You:** {message['content']}")
        elif message["role"] == "assistant":
            st.write(f"**고양이 박사 타로:** {message['content']}")