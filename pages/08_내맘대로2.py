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
    "Aether", "Lumine",
    "Albedo", "Alhaitham", "Aloy", "Amber",
    "Arlecchino", "Ayaka", "Ayato",
    "Baizhu", "Barbara", "Beidou", "Bennett",
    "Candace", "Charlotte", "Chevreuse", "Chiori",
    "Chongyun", "Collei", "Cyno",
    "Dehya", "Diluc", "Diona", "Dori",
    "Eula",
    "Faruzan", "Fischl", "Freminet", "Furina",
    "Gaming", "Ganyu", "Gorou",
    "Heizou", "Hu Tao",
    "Itto",
    "Jean", "Jiao", "Kachina",
    "Kaeya", "Kaveh", "Keqing", "Kirara",
    "Klee", "Kujou Sara", "Kuki Shinobu",
    "Layla", "Lisa", "Lynette", "Lyney",
    "Mika", "Mona",
    "Nahida", "Navia", "Neuvillette", "Nilou", "Ningguang",
    "Noelle",
    "Qiqi",
    "Raiden Shogun", "Razor", "Rosaria",
    "Sangonomiya Kokomi", "Sayu", "Sethos",
    "Shenhe", "Sucrose",
    "Tartaglia", "Thoma", "Tighnari", "Traveler",
    "Venti",
    "Wanderer",
    "Wriothesley",
    "Xiangling", "Xianyun", "Xiao", "Xingqiu", "Xinyan",
    "Yae Miko", "Yanfei", "Yaoyao", "Yelan", "Yoimiya",
    "Yun Jin",
    "Zhongli"
]

# 보유 캐릭터 기본값을 전체 캐릭터로 자동 입력
char_input = st.sidebar.text_area(
    "캐릭터 이름을 줄바꿈으로 입력하세요 (기본: 전체 원신 캐릭터)",
    value="
".join(ALL_CHARACTERS)
)

characters = [c.strip() for c in char_input.split("
") if c.strip()] [c.strip() for c in char_input.split("\n") if c.strip()]

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
