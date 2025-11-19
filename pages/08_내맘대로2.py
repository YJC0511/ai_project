# Streamlit App: Genshin Impact Spiral Abyss Random Team Generator
# File: app.py

import streamlit as st
import random
import pandas as pd

st.set_page_config(page_title="Genshin Spiral Abyss Random Team Generator", layout="wide")
st.title("원신 나선비경 랜덤 덱 생성기")

st.markdown("""
### 🔥 기능
- 보유 캐릭터 목록 입력
- 나선비경 **1파티 / 2파티** 자동 랜덤 생성
- 중복 없이 캐릭터 배치
- CSV 다운로드 기능
""")

# --------------------
# Sidebar
# --------------------
st.sidebar.header("보유 캐릭터 목록 입력")
# 전체 원신 캐릭터 목록 (2025 기준 최신)
ALL_CHARACTERS = [
    "여행자(바람)", "여행자(바위)", "여행자(번개)", "여행자(풀)",

    "엠버", "가아라(고로우)", "사라(쿠죠 사라)", "신학(셴허)", "이토", "클레", "모나", "바바라", "베넷",
    "향릉", "행추", "북두", "설탕(슈크로스)", "연비", "요이미야", "야에 미코",

    "알베도", "다이루크", "감우", "유라", "디오나", "케이아", "리사", "노엘", "응광",

    "치치", "진", "벤티", "레이저", "샹링", "신염", "토마", "쿠키 신obu", "사유",

    "라이덴 쇼군", "야란", "푸리나", "느비예트(느비예뜨)", "나히다", "닐루", "데히야", "알하이탐", "카베",

    "타르탈리아", "아이아토", "카미사토 아야카", "코코미(코코미 사농미야)", "원더러(방랑자)",

    "콜레이", "타이나리", "도리", "사이노", "세토스",

    "프레미네", "리니", "리넷", "샬롯",

    "나비아", "클로린데", "치오리", "시토리(혹은 신규 표기 반영 가능)",

    "종려", "호두", "중운", "루미네/에테르(여행자)",

    "미카", "로자리아", "피슬", "파루잔", "헤이조", "야오야오",

    "치치", "각청", "카즈하(카에데하라 카즈하)", "카키나? (신규 캐릭터면 추가 가능)",

    "아를레키노", "체브레즈(슈브르즈)", "카산드라(추후 업데이트 시 반영)"
]ip()]

team_size = st.sidebar.number_input("각 파티 인원", min_value=1, max_value=4, value=4)

st.sidebar.write(f"총 보유 캐릭터 수: **{len(characters)}명**")

# --------------------
# Team Generation
# --------------------
def generate_two_teams(chars, size):
    if len(chars) < size * 2:
        return None, None, "⚠️ 캐릭터 수가 부족합니다. 최소 " + str(size * 2) + "명 필요합니다."

    pool = chars.copy()
    random.shuffle(pool)

    team1 = pool[:size]
    team2 = pool[size:size*2]
    return team1, team2, None

if st.button("랜덤 덱 생성하기"):
    team1, team2, err = generate_two_teams(characters, team_size)

    if err:
        st.error(err)
    else:
        st.success("랜덤 파티 생성 완료!")

        col1, col2 = st.columns(2)
        with col1:
            st.subheader("1파티")
            st.write(team1)
        with col2:
            st.subheader("2파티")
            st.write(team2)

        df = pd.DataFrame({
            "Party": ["1st Team"] * len(team1) + ["2nd Team"] * len(team2),
            "Character": team1 + team2
        })

        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button("CSV 다운로드", csv, "genshin_random_teams.csv", "text/csv")

st.markdown("---")
st.info("원한다면 속성 균형(원소 조합), 힐러 필수 포함, 방깍/증폭 조합 등 고급 규칙도 추가해드릴 수 있습니다!")

# --------------------
# requirements.txt 내용 (Streamlit Cloud 업로드용)
# --------------------
# streamlit>=1.20
# pandas
# numpy
# matplotlib
