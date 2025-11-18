import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.colors as pcolors

# --- 1. 데이터 로딩 및 전처리 함수 ---
@st.cache_data
def load_data():
    """CSV 파일을 로드하고 시각화에 적합한 형태로 전처리합니다."""
    try:
        # Streamlit Cloud에 업로드된 'sexcrime.csv' 파일을 읽어옵니다.
        df = pd.read_csv('sexcrime.csv')
    except FileNotFoundError:
        st.error("🚨 'sexcrime.csv' 파일을 찾을 수 없습니다. Streamlit Cloud에 app.py와 함께 파일을 업로드했는지 확인해주세요.")
        return pd.DataFrame()

    # '연도'를 제외한 모든 컬럼을 Long-format으로 변환합니다.
    df_long = df.melt(id_vars='연도', var_name='구분', value_name='피해자_수')
    
    # '불상' 및 '미상' 데이터를 제외하고 '성별' 및 '연령대'로 분리합니다.
    df_long = df_long[~df_long['구분'].str.contains('불상|미상')]

    # '구분' 컬럼에서 '성별'과 '연령대' 분리
    df_long['성별'] = df_long['구분'].apply(lambda x: x.split('_')[0])
    df_long['연령대'] = df_long['구분'].apply(lambda x: x.split('_')[1])
    
    # '연령대'의 순서를 정의하여 그래프에서 논리적으로 정렬되도록 합니다.
    age_order = ['6세이하', '12세이하', '15세이하', '20세이하', '30세이하', '40세이하', '50세이하', '60세이하', '60세초과']
    df_long['연령대'] = pd.Categorical(df_long['연령대'], categories=age_order, ordered=True)
    
    return df_long

# --- 2. 시각화 함수 ---
def create_chart(df_filtered, selected_gender, selected_year):
    """Plotly 막대 그래프를 생성하고 1등을 빨간색으로 표시합니다."""
    
    if df_filtered.empty:
        st.warning(f"⚠️ {selected_year}년 {selected_gender} 데이터가 존재하지 않습니다.")
        return None
        
    # 피해자 수 기준 내림차순 정렬
    df_plot = df_filtered.sort_values('피해자_수', ascending=False)
    
    values = df_plot['피해자_수'].tolist()
    age_groups = df_plot['연령대'].tolist()
    max_val = df_plot['피해자_수'].max()

    # 색상 지정 로직: 1등은 빨간색, 나머지는 파란색 계열 그라데이션
    N = len(df_plot)
    # 파란색 계열의 순차적 색상 팔레트 생성
    sequential_colors = pcolors.sample_colorscale('Blues', [i/(N-1) for i in range(N)], low=0.2, high=0.8)
    
    colors_map = []
    
    for i, val in enumerate(values):
        if val == max_val:
            # 1등 (최댓값)은 빨간색
            colors_map.append('rgb(255, 0, 0)') 
        else:
            # 나머지는 생성된 파란색 그라데이션을 순서대로 할당 (내림차순 정렬된 순서대로)
            colors_map.append(sequential_colors[i])

    
    # Plotly Graph Object를 사용하여 막대 그래프 생성
    fig = go.Figure(data=[
        go.Bar(
            x=age_groups, 
            y=values, 
            marker_color=colors_map,
            hovertemplate='<b>%{x}</b><br>피해자 수: %{y:,.0f}<extra></extra>'
        )
    ])

    # 그래프 레이아웃 설정
    fig.update_layout(
        title={
            'text': f"<b>{selected_year}년 {selected_gender}</b> 연령대별 성범죄 피해자 수",
            'y':0.9, 'x':0.5, 'xanchor': 'center', 'yanchor': 'top'
        },
        xaxis_title="연령대",
        yaxis_title="피해자 수",
        margin=dict(l=20, r=20, t=80, b=20),
        plot_bgcolor='#f0f2f6' # Streamlit 배경색과 유사하게 설정
    )
    
    # x축의 연령대 순서를 정렬된 순서로 유지
    fig.update_xaxes(categoryorder='array', categoryarray=age_groups) 

    return fig

# --- 3. Streamlit 앱 실행 ---
def main():
    st.set_page_config(layout="wide", page_title="연도/성별 성범죄 피해자 분석", initial_sidebar_state="expanded")
    
    st.title("📊 성별 및 연도별 성범죄 피해자 인터랙티브 분석")
    st.markdown("---")
    
    df_long = load_data()

    if df_long.empty:
        return 

    # --- 사이드바 필터 ---
    st.sidebar.header("🔍 데이터 선택")
    
    # 연도 선택
    all_years = sorted(df_long['연도'].unique().tolist(), reverse=True)
    selected_year = st.sidebar.selectbox(
        "연도 선택",
        options=all_years,
        index=0 
    )

    # 성별 선택
    all_genders = df_long['성별'].unique().tolist()
    # '여자'가 있다면 기본값으로 설정
    default_index = all_genders.index('여자') if '여자' in all_genders else 0 
    selected_gender = st.sidebar.radio(
        "성별 선택",
        options=all_genders,
        index=default_index
    )

    # --- 데이터 필터링 ---
    df_filtered = df_long[
        (df_long['연도'] == selected_year) & 
        (df_long['성별'] == selected_gender)
    ]
    
    # --- 그래프 그리기 ---
    fig = create_chart(df_filtered, selected_gender, selected_year)
    
    if fig:
        # Plotly 그래프를 Streamlit에 표시 (전체 너비 사용)
        st.plotly_chart(fig, use_container_width=True)
        
        # --- 데이터 테이블 표시 ---
        st.markdown("## 📋 데이터 테이블")
        df_display = df_filtered[['연령대', '피해자_수']].sort_values('피해자_수', ascending=False)
        df_display.columns = ['연령대', '피해자 수']
        st.dataframe(df_display.reset_index(drop=True), use_container_width=True)

if __name__ == '__main__':
    main()
