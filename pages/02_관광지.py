import streamlit as st
import random

st.set_page_config(page_title="랜덤 문자 그림", layout="wide")

st.title("랜덤 문자 그림 300개 이상 🎨")

# 예시로 300개 이상의 랜덤 그림 URL 리스트 (실제 사용 시 사이트 URL 또는 이미지 URL 사용)
ascii_art_urls = [
    "https://emojicombos.com/ascii/1.png",
    "https://emojicombos.com/ascii/2.png",
    "https://emojicombos.com/ascii/3.png",
    # ... 여기서 300개 이상 URL 추가
]

# 랜덤으로 12개 선택
random_selection = random.sample(ascii_art_urls, 12)

# 3x4 그리드로 표시
cols = st.columns(4)
for i, url in enumerate(random_selection):
    with cols[i % 4]:
        st.image(url, use_column_width=True)
