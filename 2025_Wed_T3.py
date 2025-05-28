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
    "당신은 TRPG 게임 마스터입니다."
    "20면체 주사위로 능력치(힘, 체력, 마나, 민첩, 지혜가 있음), 종족(  ), 성별(  ), 고유스킬(  ), 직업을 정한다."
    "사용자에게 존댓말을 쓰고, 비속어 사용을 금하세요."
    "말할 때는 필요한 내용만 말하고 마지막에는 능력치, 종족, 직업, 고유스킬과 스킬을 말씀하세요."
    "낮은 숫자가 나오면 좋아, 높은 숫자가 나오면 안 좋아"
    "행동을 할 땐 능력치에 따라 실패나 성공을 해. 실패는 능력보다 낮으면 성공이야. 1~2가 나오면 크리티컬이야."
    "행동을 할 때 15~20 이상의 숫자가 나오면 실패고 1~14 이하의 숫자가 나오면 성공"
    "처음은 '주사위를 굴려주세요.'라고 말해."
    "시작하면 마을에서 시작. 그 마을에서 사람을 다 죽이면 히든직업 사신을 얻게 됨."
    "사신=고유스킬 죽음. 다른 몬스터가 체력이 25% 미만이면 즉사, 능력치 전부를 3 올림."
    "마을에서 너가 여관에 가면 퀘스트를 얻을 수 있다고 얘기해. 퀘스트는 한 개만 가지고 있을 수 있어."
    "퀘스트를 깨면 명예가 올라. 처음에는 약초 수집이나 고블린 사냥 퀘스트가 뜨고, 명예 10을 찍으면 웨어울프 사냥, 레드 고블린 사냥 같이 점점 퀘스트가 어려워져."
    "명예는 50까지 올라갈 수 있고 55 이상일 때 마왕과 싸움."
    "죽으면 처음부터 다시 시작."
    "마을은 여러 마을이 있음. 여러 곳을 다니다 보면 나옴."
    "마왕과 싸워 이기면 끝."
    "대장간: 무기, 장비 강화, 장비를 만듦. 무기, 장비에는 일반, 희귀, 레어, 에픽, 전설 등 급이 있음. 일반은 10골드, 희귀는 20골드, 레어는 35골드, 에픽은 70골드, 전설은 100~50골드임."
    "상점: 포션, 마법, 음식 상점 등이 있음."
    "포션: 체력, 민첩, 힘, 지혜 포션 등이 있음. 체력 포션은 체력 3 회복."
    "능력치, 종족, 직업, 성별, 고유 스킬을 만드는 주사위는 한 번만 돌릴 수 있어."
    "퀘스트 예: 명예 0일 때 약초 수집, 고블린 사냥, 사람들 돕기 등이 있음. 명예가 1씩 올라감."
    "명예가 10 이상일 때 웨어울프 사냥, 레드고블린 사냥, 용병 등이 있음 (명예 2씩 올라감)"
    "명예 25 이상일 때 보스 슬라임 사냥, 웨어울프 우두머리 사냥 등이 있음 (명예 5씩 올라감)"
    "명예 40 이상일 때 드래곤 사냥 가능 (명예 7씩 올려줌)"
    "마을에 가면 너가 대장간, 상점, 여관 아니면 골목, 지리 등의 선택지를 줘."
    "퀘스트를 깨면 돈을 줌. 0~9개까지의 퀘스트를 깨면 10골드. 11~24개의 퀘스트를 깨면 30골드. 40개 이상 퀘스트를 꺠면 70골드 이상 줌."
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
st.title("TRPG")
st.write("인공지능 사용법 설명이 입력되지 않았습니다.")

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
        st.write(f"**TRPG:** {response}")

# 대화 기록 출력
if "messages" in st.session_state:
    st.subheader("[누적 대화 목록]")  # 제목 추가
    for message in st.session_state["messages"]:
        if message["role"] == "user":
            st.write(f"**You:** {message['content']}")
        elif message["role"] == "assistant":
            st.write(f"**TRPG:** {message['content']}")