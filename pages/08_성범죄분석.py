import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="성범죄 피해자 통계", layout="wide")

# -----------------------------
# 데이터 불러오기
# -----------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("경찰청_성범죄 피해자 성별 연령별 현황_20241231.csv", encoding="utf-8")
    return df

df = load_data()

st.title("📊 성범죄 피해자 성별 · 연령 · 연도 분석 대시보드")

# -----------------------------
# 사이드바 필터
# -----------------------------
st.sidebar.header("🔎 필터 선택")

years = sorted(df["연도"].unique())
sexes = sorted(df["성별"].unique())

selected_year = st.sidebar.selectbox("연도 선택", years)
selected_sex = st.sidebar.selectbox("성별 선택", sexes)

filtered = df[(df["연도"] == selected_year) & (df["성별"] == selected_sex)]

# -----------------------------
# Plotly 색상 스타일 — 1등(최대값)은 빨강, 나머지는 파랑~밝은 파랑 그라데이션
# -----------------------------
def generate_colors(values):
    max_val = max(values)
    colors = []

    for v in values:
        if v == max_val:
            colors.append("red")
        else:
            # 파란색 계열 그라데이션
            # 값이 클수록 색을 진하게
            intensity = 1 - (v / max_val) * 0.7
            colors.append(f"rgba(0, 0, 255, {intensity})")
    return colors

values = filtered["피해자수"].tolist()
colors = generate_colors(values)

# -----------------------------
# Plotly 그래프 생성
# -----------------------------
fig = px.bar(
    filtered,
    x="연령대",
    y="피해자수",
    title=f"{selected_year}년 {selected_sex} 성범죄 피해자 현황",
)

fig.update_traces(marker_color=colors)
fig.update_layout(
    xaxis_title="연령대",
    yaxis_title="피해자 수",
    title_x=0.5,
    template="plotly_white",
    font=dict(size=15),
)

st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# 데이터 테이블 보기
# -----------------------------
st.subheader("📄 필터링된 데이터")
st.dataframe(filtered)
