import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


# Load data
def load_data():
df = pd.read_csv("countriesMBTI_16types.csv")
return df


df = load_data()


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


tab1, tab2 = st.tabs(["국가별 MBTI", "MBTI 유형별 TOP10 국가"])


with tab1:("🌍 국가별 MBTI 유형 분포 시각화")


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
with tab2:
st.subheader("MBTI 유형별 상위 10개 국가")


mbti_choice = st.selectbox("MBTI 유형을 선택하세요", [c for c in df.columns if c != "Country"], key="mbti_select")


top10 = df[["Country", mbti_choice]].sort_values(by=mbti_choice, ascending=False).head(10)


colors_top10 = ["pink" if c == "South Korea" or c == "Korea" or c == "Republic of Korea" else f"rgba(0,0,255,{1 - i/10})" for i, c in enumerate(top10["Country"]) ]


fig2 = go.Figure(data=[go.Bar(
x=top10["Country"],
y=top10[mbti_choice],
marker_color=colors_top10
)])


fig2.update_layout(
title=f"{mbti_choice} 비율이 높은 국가 TOP10",
xaxis_title="국가",
yaxis_title="비율",
template="plotly_white"
)


st.plotly_chart(fig2, use_container_width=True)
