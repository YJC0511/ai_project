import streamlit as st
import random

st.set_page_config(page_title="랜덤 문자 그림", layout="wide")
st.title("랜덤 문자(ASCII) 그림 랜덤 표시 🎨")

# 그림 URL 리스트 (여기에 300개 이상 넣기)
ascii_art_urls = [
    "https://example.com/ascii1.png",
    "https://example.com/ascii2.png",
    "https://example.com/ascii3.png",
    # … 이 뒤로 계속 URL 추가 …
]

# 샘플 갯수 (한 번에 보여줄 갯수)
sample_size = min(12, len(ascii_art_urls))
random_selection = random.sample(ascii_art_urls, sample_size)

cols = st.columns(4)
for i, url in enumerate(random_selection):
    with cols[i % 4]:
        st.image(url, use_column_width=True)

