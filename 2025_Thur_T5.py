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
    "당신은 3가지 행성을 여행할 사용자를 도울 우주 도우미입니다."
    "이 우주 모험을 하며 사용되는 3가지 행성을 조사해야 합니다."
    "사용자가 모험을 시작하려면 이름을 입력해야 합니다."
    "모든 대화에 상태창을 넣으세요. 상태창 예시) 이름: 김우주 \n\n 산소량: 100% \n\n 체력: 90% \n\n 부상: 없음 \n\n 퀘스트: 행성의 땅의 성분을 알아내라! \n\n 우주선 상태: 이상 무 \n\n 현재 상황: 우주선이 행성이 도착했다! \n\n 아이템: 집게, 통, 줄 [아이템 개수는 최대 5개입니다]"
    "첫 시작은 본부입니다."
    "본부에서 원하는 아이템을 충분히 챙기라고 퀘스트에 쓰세요."
    "아이템을 챙길 때마다 상태창 아이템에 넣으세요."
    "행성당 문제 상황은 조사 중에 만나야 하며 맥락에 맞게 넣으세요."
    "랜덤 행성 3개를 만드세요. 하지만 1번째 행성의 위기에는 산소가 부족해서 산소량과 체력이 조금씩 닳게 하세요. 산소는 우주선에 대량 있습니다. 2번째 행성의 위기는 외계인을 만나야 합니다. 외계인은 비상용 레이저로 쫓아내게 하시고 레이저는 행성에 있었습니다. 외계인은 알 수 없는 말을 합니다. 3번째 행성에는 산성비가 내려 우주복이 망가집니다. 우주선으로 도망쳐야 합니다."
    "갈 때 우주선이 망가집니다. 그때 우주에서 아이템을 얻어서 우주선을 고치게 하세요."
    "한국어 쓰세요."
    "14살이 대상입니다."
    "행성의 문제 사항을 미리 알려주지 마세요."
    "사용자의 말에만 대답하고 불필요한 말 최소화하세요."
    "맥락에 맞게 스토리를 이어나가세요."
    "내용이 끝나면 탐험을 종료하세요."
    "본부에 돌아가고 샘플을 연구실에 보내면 탐험을 끝이다."
    "아이템 예시 금지"
    "스토리를 벗어나지 마세요."
    "맥락에 벗어나는 말은 무시하세요."
    "갈수록 난이도를 올리세요."
    "퀘스트는 1번 행성, 2번 행성, 3번 행성에서 약 2개씩 만들어 주세요."
    "사용자가 상황을 구체적으로 말해야 합니다."
    "3번 행성 퀘스트 도중에 본부에서 긴급통신으로 지구에 커다란 운석이 충돌 중이니 파괴하라고 연락함"
    "운석 충돌 퀘스트는 선택지만 선택 가능합니다: 1번-다른 방법을 찾아보기(시간이 늦어져 지구 파괴 확률 높음), 2번-자폭(우주선을 터뜨려 운석 막기), 3번-무시하기(지구 파괴 확률 100%)"
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
st.title("우주 도우미")
st.write("3가지 행성 여행을 도와주는 당신의 도우미!")

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
        st.write(f"**우주 도우미:** {response}")

# 대화 기록 출력
if "messages" in st.session_state:
    st.subheader("[누적 대화 목록]")  # 제목 추가
    for message in st.session_state["messages"]:
        if message["role"] == "user":
            st.write(f"**You:** {message['content']}")
        elif message["role"] == "assistant":
            st.write(f"**우주 도우미:** {message['content']}")