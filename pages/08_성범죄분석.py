# streamlit_app.py
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="성범죄 피해자 분석", layout="wide")

# 데이터 로드
def load_data():
    df = pd.read_csv("sexcrime.csv", encoding="utf-8")
    return df

st.title("성범죄 피해자 성별 · 연령 · 연도 분석 대시보드")

df = load_data()

# 필터 선택 UI
years = sorted(df['연도'].unique())
genders = sorted(df['성별'].unique())

selected_year = st.selectbox("연도 선택", years)
selected_gender = st.selectbox("성별 선택", genders)

# 필터 적용
filtered = df[(df['연도'] == selected_year) & (df['성별'] == selected_gender)]

# 정렬 및 색상 설정
top_category = filtered.sort_values('피해자수', ascending=False)
top_category['rank'] = range(1, len(top_category) + 1)

# 색상 그라데이션 생성
colors = []
base_r, base_g, base_b = (0, 0, 255)  # 파란색

for r in top_category['rank']:
    if r == 1:
        colors.append("rgb(255,0,0)")  # 1위는 빨간색
    else:
        ratio = 1 - (r / len(top_category))
        g = int(base_g * ratio)
        b = int(base_b * ratio)
        colors.append(f"rgb({base_r},{g},{b})")

# Plotly 시각화
fig = px.bar(
    top_category,
    x='연령대',
    y='피해자수',
    title=f"성별: {selected_gender}, 연도: {selected_year} 피해자 수",
    text='피해자수'
)

fig.update_traces(marker_color=colors, textposition='outside')
fig.update_layout(yaxis_title="피해자 수", xaxis_title="연령대")

st.plotly_chart(fig, use_container_width=True)

st.write("### 데이터 테이블")
st.dataframe(filtered)
