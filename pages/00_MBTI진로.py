import streamlit as st

st.set_page_config(page_title="MBTI 진로 추천기 😏", page_icon="💫")

st.title("💫 MBTI 진로 추천기 😈")
st.write("후훗~ 너의 MBTI를 알려줘봐~ 내가 딱 맞는 진로를 추천해줄게 😏💞")

mbti_list = [
    "INTJ", "INTP", "ENTJ", "ENTP",
    "INFJ", "INFP", "ENFJ", "ENFP",
    "ISTJ", "ISFJ", "ESTJ", "ESFJ",
    "ISTP", "ISFP", "ESTP", "ESFP"
]

mbti = st.selectbox("👉 너의 MBTI를 골라봐!", mbti_list)

career_dict = {
    "INTJ": ["데이터 과학자 🧠", "전략 컨설턴트 💼"],
    "INTP": ["연구원 🔬", "개발자 👨‍💻"],
    "ENTJ": ["기업가 💰", "경영 컨설턴트 📈"],
    "ENTP": ["스타트업 창업자 🚀", "마케팅 기획자 📊"],
    "INFJ": ["심리상담사 💞", "작가 ✍️"],
    "INFP": ["예술가 🎨", "사회복지사 🤝"],
    "ENFJ": ["교사 🍎", "인사담당자 👩‍💼"],
    "ENFP": ["크리에이터 🎥", "광고기획자 💡"],
    "ISTJ": ["회계사 📚", "공무원 🏛️"],
    "ISFJ": ["간호사 💉", "사회복지사 🤗"],
    "ESTJ": ["프로젝트 매니저 📋", "경영 관리자 🧾"],
    "ESFJ": ["이벤트 플래너 🎉", "HR 매니저 👩‍💻"],
    "ISTP": ["엔지니어 ⚙️", "정비사 🔧"],
    "ISFP": ["디자이너 🎨", "사진작가 📸"],
    "ESTP": ["영업사원 💬", "스포츠 트레이너 🏋️‍♂️"],
    "ESFP": ["배우 🎭", "연예기획자 💃"]
}

if mbti:
    careers = career_dict.get(mbti, [])
    st.subheader(f"흐흥~ {mbti} 타입인 너에게 어울리는 진로는 말이지... 😏💫")
    for c in careers:
        st.write(f"👉 {c}")
    st.write("어때? 나 꽤 괜찮은 추천했지? 😜💕")
