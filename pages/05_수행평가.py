import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import plotly.colors as pcolors

# --- 1. 데이터 로딩 및 전처리 함수 ---
@st.cache_data
def load_and_preprocess_data():
    """
    CSV 파일을 로드하고 시각화에 적합한 형태로 전처리합니다.
    (기존 코드와 동일)
    """
    try:
        df = pd.read_csv('sexcrime.csv')
    except FileNotFoundError:
        st.error("🚨 'sexcrime.csv' 파일을 찾을 수 없습니다. Streamlit Cloud에 app.py와 함께 파일을 업로드했는지 확인해주세요.")
        return pd.DataFrame(), pd.DataFrame()

    # 1-1. 연령대별 분포 분석용 데이터 (df_long)
    df_long = df.melt(id_vars='연도', var_name='구분', value_name='피해자_수')
    df_long = df_long[~df_long['구분'].str.contains('불상|미상')]
    df_long['성별'] = df_long['구분'].apply(lambda x: x.split('_')[0])
    df_long['연령대'] = df_long['구분'].apply(lambda x: x.split('_')[1])
    
    age_order = ['6세이하', '12세이하', '15세이하', '20세이하', '30세이하', '40세이하', '50세이하', '60세이하', '60세초과']
    df_long['연령대'] = pd.Categorical(df_long['연령대'], categories=age_order, ordered=True)
    
    # 1-2. 성별/연도별 총합 분석용 데이터 (df_summary)
    # '불상' 및 '미상' 제외하고 성별로 총합 계산
    
    # '연도' 컬럼을 제외한 모든 컬럼을 대상으로 함
    cols_to_sum = [col for col in df.columns if col not in ['연도', '불상', '남자_미상', '여자_미상']]
    df_sum = df[['연도']].copy()
    
    # 남성 피해자 총합
    male_cols = [col for col in cols_to_sum if col.startswith('남자')]
    df_sum['남자_총합'] = df[male_cols].sum(axis=1)
    
    # 여성 피해자 총합
    female_cols = [col for col in cols_to_sum if col.startswith('여자')]
    df_sum['여자_총합'] = df[female_cols].sum(axis=1)
    
    # 전체 피해자 총합
    df_sum['전체_총합'] = df_sum['남자_총합'] + df_sum['여자_총합']
    
    return df_long, df_sum

# --- 2. 시각화 함수: 연령대별 분포 (기존 기능) ---
def create_age_distribution_chart(df_filtered, selected_gender, selected_year):
    """Plotly 막대 그래프를 생성하고 1등을 빨간색으로 표시합니다."""
    
    if df_filtered.empty:
        st.warning(f"⚠️ {selected_year}년 {selected_gender} 데이터가 존재하지 않습니다.")
        return None
        
    df_plot = df_filtered.sort_values('피해자_수', ascending=False)
    
    values = df_plot['피해자_수'].tolist()
    age_groups = df_plot['연령대'].tolist()
    max_val = df_plot['피해자_수'].max()

    # 색상 지정 로직: 1등은 빨간색, 나머지는 파란색 계열 그라데이션
    N = len(df_plot)
    sequential_colors = pcolors.sample_colorscale('Blues', [i/(N-1) for i in range(N)], low=0.2, high=0.8)
    colors_map = []
    
    for i, val in enumerate(values):
        if val == max_val:
            colors_map.append('rgb(255, 0, 0)') 
        else:
            colors_map.append(sequential_colors[i])

    fig = go.Figure(data=[
        go.Bar(
            x=age_groups, 
            y=values, 
            marker_color=colors_map,
            hovertemplate='<b>%{x}</b><br>피해자 수: %{y:,.0f}<extra></extra>'
        )
    ])

    fig.update_layout(
        title={
            'text': f"<b>{selected_year}년 {selected_gender}</b> 연령대별 피해자 분포 (1등: 빨간색)",
            'y':0.9, 'x':0.5, 'xanchor': 'center', 'yanchor': 'top'
        },
        xaxis_title="연령대",
        yaxis_title="피해자 수",
        margin=dict(l=20, r=20, t=80, b=20),
        plot_bgcolor='#f0f2f6'
    )
    
    fig.update_xaxes(categoryorder='array', categoryarray=age_groups) 

    return fig

# --- 3. 시각화 함수: 연도별 총 피해자 추이 (신규 기능) ---
def create_time_series_chart(df_summary):
    """연도별 전체 피해자 수 추이를 Plotly Line Chart로 생성합니다."""
    
    fig = px.line(
        df_summary, 
        x='연도', 
        y='전체_총합', 
        markers=True, # 데이터 포인트 마커 표시
        title='연도별 전체 성범죄 피해자 수 추이',
        labels={'연도': '연도', '전체_총합': '총 피해자 수'}
    )
    
    fig.update_traces(line_color='darkred', line_width=3, marker=dict(size=8))
    
    # 툴팁 형식 설정
    fig.update_traces(hovertemplate='<b>연도: %{x}</b><br>총 피해자 수: %{y:,.0f}<extra></extra>')
    
    fig.update_layout(
        xaxis_title='연도',
        yaxis_title='피해자 수 (명)',
        plot_bgcolor='#f0f2f6'
    )
    
    return fig

# --- 4. 시각화 함수: 성별 총합 비교 (신규 기능) ---
def create_gender_summary_chart(df_summary, selected_year):
    """선택된 연도의 남성/여성 피해자 총합을 Plotly Stacked Bar Chart로 생성합니다."""
    
    df_year = df_summary[df_summary['연도'] == selected_year].iloc[0]
    
    # 데이터프레임 구조 변경 (Plotly Express가 잘 처리할 수 있도록)
    data = {
        '성별': ['남성', '여성'],
        '총합': [df_year['남자_총합'], df_year['여자_총합']]
    }
    df_plot = pd.DataFrame(data)
    
    # 색상: 남성은 파란색, 여성은 (상대적으로 피해가 높으므로) 주황색 계열
    colors = ['#1f77b4', '#ff7f0e'] # 남성: Blue, 여성: Orange
    
    fig = px.bar(
        df_plot, 
        x='성별', 
        y='총합', 
        color='성별', 
        color_discrete_sequence=colors,
        title=f'{selected_year}년 성별 피해자 총합 비교',
        labels={'성별': '성별', '총합': '피해자 수'}
    )
    
    # 툴팁 및 막대 위에 값 표시
    fig.update_traces(
        texttemplate='%{y:,.0f}', 
        textposition='outside',
        hovertemplate='<b>성별: %{x}</b><br>총 피해자 수: %{y:,.0f}<extra></extra>'
    )
    
    fig.update_layout(
        xaxis_title='', # 성별은 축 제목 필요 없음
        yaxis_title='피해자 수 (명)',
        plot_bgcolor='#f0f2f6'
    )
    
    return fig

# --- 5. Streamlit 앱 실행 ---
def main():
    st.set_page_config(layout="wide", page_title="연도/성별 성범죄 피해자 분석", initial_sidebar_state="expanded")
    
    st.title("📊 성범죄 피해자 인터랙티브 분석 대시보드")
    st.markdown("## 성별/연령대/시간 흐름에 따른 피해 규모 분석")
    st.markdown("---")
    
    df_long, df_summary = load_and_preprocess_data()

    if df_long.empty:
        return 

    # --- 사이드바 필터 ---
    st.sidebar.header("🔍 데이터 선택")
    
    all_years = sorted(df_long['연도'].unique().tolist(), reverse=True)
    selected_year = st.sidebar.selectbox(
        "기준 연도 선택",
        options=all_years,
        index=0 
    )

    # Streamlit Tabs 기능 사용
    tab1, tab2, tab3 = st.tabs(["피해 연령대 분포 분석 (기존)", "연도별 피해 추이", "성별 총합 비교"])

    # --- 탭 1: 피해 연령대 분포 분석 (기존 기능) ---
    with tab1:
        st.subheader(f"📌 {selected_year}년 성별 피해 연령대 분포")
        
        all_genders = df_long['성별'].unique().tolist()
        default_index = all_genders.index('여자') if '여자' in all_genders else 0 
        selected_gender = st.radio(
            "분석 대상 성별을 선택하세요.",
            options=all_genders,
            index=default_index,
            key='gender_select'
        )

        df_filtered = df_long[
            (df_long['연도'] == selected_year) & 
            (df_long['성별'] == selected_gender)
        ]
        
        fig = create_age_distribution_chart(df_filtered, selected_gender, selected_year)
        
        if fig:
            st.plotly_chart(fig, use_container_width=True)
            
            st.markdown("#### 📋 데이터 테이블")
            df_display = df_filtered[['연령대', '피해자_수']].sort_values('피해자_수', ascending=False)
            df_display.columns = ['연령대', '피해자 수']
            st.dataframe(df_display.reset_index(drop=True), use_container_width=True)

    # --- 탭 2: 연도별 피해 추이 (신규 기능) ---
    with tab2:
        st.subheader("📌 전체 성범죄 피해자 수의 연도별 추이")
        
        fig_time = create_time_series_chart(df_summary)
        st.plotly_chart(fig_time, use_container_width=True)
        
        st.markdown("#### 📋 연도별 총 피해자 수")
        st.dataframe(df_summary.sort_values('연도', ascending=False).set_index('연도'), use_container_width=True)


    # --- 탭 3: 성별 총합 비교 (신규 기능) ---
    with tab3:
        st.subheader(f"📌 {selected_year}년 남성 vs 여성 피해자 총합 비교")
        
        fig_gender_summary = create_gender_summary_chart(df_summary, selected_year)
        st.plotly_chart(fig_gender_summary, use_container_width=True)
        
        st.markdown(f"#### 📋 {selected_year}년 성별 총합 데이터")
        df_gender_data = df_summary[df_summary['연도'] == selected_year][['남자_총합', '여자_총합']]
        df_gender_data.columns = ['남성 피해자 수', '여성 피해자 수']
        st.dataframe(df_gender_data.T.rename_axis('성별'), use_container_width=True)

if __name__ == '__main__':
    main()
