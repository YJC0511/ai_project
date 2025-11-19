import streamlit as st
import random
import pandas as pd

st.set_page_config(page_title="원신 나선비경 랜덤 파티", layout="wide", page_icon="🎮")
st.title("🎮 원신 나선비경 랜덤 파티 생성기")
st.markdown("선택한 캐릭터로 랜덤 파티 1·2 생성")

# 공식 한글 캐릭터 전체 목록
characters = [
    "엠버", "리사", "카야", "바바라", "레이저", "앤티", "설탕", "노엘", "피슬", "베넷",
    "향릉", "행추", "응광", "중운", "신염", "디오나", "로자리아", "연비", "북두", "토마",
    "구라라", "시노부", "미카", "레이라", "패루잔", "린네", "린타", "쿠쿠", "알하이탐",
    "데히야", "타이나리", "니루", "나히다", "야오야오", "카베", "시토리", "요이미야",
    "코코미", "신학", "야에 미코", "아야카", "아야토", "호두", "유라", "소", "각청",
    "진", "설윤", "감우", "치치", "중운", "응광", "종려", "타르탈리아", "푸리나",
    "클레", "모나", "알베도", "라이덴", "카즈하", "야란", "휴톤", "방랑자", "선인",
]

# 사이드바 설정
st.sidebar.header("파티 설정")
party_size = st.sidebar.slider("캐릭터 수 (파티별)", 1, 4, 4)

st.sidebar.markdown("---")
st.sidebar.write("총 캐릭터 수: {}명".format(len(characters)))

# 랜덤 파티 생성 버튼
if st.button("✨ 랜덤 파티 생성 ✨"):
    if len(characters) < party_size * 2:
        st.error("캐릭터 수가 부족합니다!")
    else:
        selected = random.sample(characters, party_size * 2)
        team1 = selected[:party_size]
        team2 = selected[party_size:]

        st.success("🎉 파티 생성 완료! 🎉")

        col1, col2 = st.columns(2)
        with col1:
            st.subheader("1파티")
            st.info(", ".join(team1))
        with col2:
            st.subheader("2파티")
            st.info(", ".join(team2))

        # CSV 다운로드
        df = pd.DataFrame({
            "파티": ["1파티"]*party_size + ["2파티"]*party_size,
            "캐릭터": team1 + team2
        })
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button("💾 CSV 다운로드", csv, "genshin_random_teams.csv", "text/csv")

# Footer
st.markdown("---")
st.caption("앱 제작: Streamlit | 랜덤 파티 생성기 🎮")

# requirements.txt 내용
# streamlit>=1.20
# pandas
# numpy
