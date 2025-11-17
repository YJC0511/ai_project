import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# -----------------------------
# 데이터 로드
# -----------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("subway.csv", encoding="cp949")
    df["총이용객수"] = df["승차총승객수"] + df["하차총승객수"]
    return df

df = load_data()

st.title("🚇 서울 지하철 승하차 분석 (2025년 10월)")

# -----------------------------
# 사이드바 선택 UI
# -----------------------------
st.sidebar.header("⚙️ 설정")

# 날짜 선택 (2025년 10월 날짜 자동 추출)
date_list = sorted(df["사용일자"].unique())
selected_date = st.sidebar.selectbox("날짜 선택", date_list)

# 호선 선택
line_list = sorted(df["노선명"].unique())
selected_line = st.sidebar.selectbox("호선 선택", line_list)

# -----------------------------
# 데이터 필터링
# -----------------------------
filtered = df[(df["사용일자"] == selected_date) &
              (df["노선명"] == selected_line)]

# TOP 10 역
top10 = filtered.sort_values("총이용객수", ascending=False).head(10)

st.subheader(f"📊 {selected_date} · {selected_line} TOP 10 역 (승차+하차 기준)")

# -----------------------------
# 그래프 색상 처리
# - 1등: 빨간색
# - 그 외: 파란색 → 점점 밝아지는 형태
# -----------------------------
colors = ["red"]  # 1등

# 파란색 계열 그라데이션 (9개)
blue_gradients = [
    f"rgba(0, 0, 255, {0.1 + 0.09 * i})" for i in range(9)
]
colors.extend(blue_gradients)

# -----------------------------
# Plotly Bar Chart
# -----------------------------
fig = go.Figure()

fig.add_trace(go.Bar(
    x=top10["역명"],
    y=top10["총이용객수"],
    marker_color=colors[:len(top10)],
    text=top10["총이용객수"],
    textposition="auto"
))

fig.update_layout(
    title=f"{selected_date} {selected_line} 승하차 TOP 10",
    xaxis_title="역명",
    yaxis_title="총 승하차 인원",
    template="plotly_white",
)

st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# 데이터 테이블 보기
# -----------------------------
with st.expander("📄 데이터 보기"):
    st.dataframe(top10)
