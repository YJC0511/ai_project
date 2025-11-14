import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Load data
def load_data():
    df = pd.read_csv("countriesMBTI_16types.csv")
    return df

df = load_data()

st.title("🌍 국가별 MBTI 유형 분포 시각화")

# 국가 선택
target_country = st.selectbox("국가를 선택하세요", df['Country'].unique())

# 선택된 국가 데이터 추출
row = df[df['Country'] == target_country].iloc[0]
mbti_cols = [c for c in df.columns if c != "Country"]
values = row[mbti_cols].values

# 데이터프레임 구성
data = pd.DataFrame({"MBTI": mbti_cols, "Value": values})

# 정렬 (높은 비율 순)
data = data.sort_values(by="Value", ascending=False).reset_index(drop=True)

# 색상 지정: 1등은 빨간색, 나머지는 파란색 그라데이션
colors = ["red"] + [f"rgba(0,0,255,{1 - i/len(data)})" for i in range(1, len(data))]

# Plotly 막대그래프
fig = go.Figure(data=[
    go.Bar(
        x=data["MBTI"],
        y=data["Value"],
        marker_color=colors
    )
])

fig.update_layout(
    title=f"{target_country} MBTI 비율",
    xaxis_title="MBTI 유형",
    yaxis_title="비율",
    template="plotly_white"
)

st.plotly_chart(fig, use_container_width=True)

st.markdown("---")
st.subheader("📌 Requirements.txt")
