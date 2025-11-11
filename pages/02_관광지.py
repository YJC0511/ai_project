import streamlit as st
import folium
from streamlit_folium import st_folium

# --- 서울 관광지 데이터 (위도, 경도 포함) ---
tourist_spots = [
    {"name": "경복궁", "lat": 37.579617, "lon": 126.977041, "desc": "조선시대의 대표 궁궐로, 외국인들이 가장 많이 방문하는 명소입니다."},
    {"name": "N서울타워", "lat": 37.551169, "lon": 126.988227, "desc": "서울의 상징적인 랜드마크로, 야경이 특히 아름답습니다."},
    {"name": "북촌한옥마을", "lat": 37.582604, "lon": 126.983998, "desc": "전통 한옥이 잘 보존된 마을로, 한국의 옛 정취를 느낄 수 있습니다."},
    {"name": "창덕궁", "lat": 37.579414, "lon": 126.991011, "desc": "유네스코 세계문화유산에 등재된 고궁입니다."},
    {"name": "동대문디자인플라자(DDP)", "lat": 37.566479, "lon": 127.009488, "desc": "현대적인 건축미와 패션, 디자인이 어우러진 명소입니다."},
    {"name": "한강공원", "lat": 37.5285, "lon": 126.9346, "desc": "서울 시민과 관광객 모두가 즐기는 한강변 공원입니다."},
    {"name": "서울숲", "lat": 37.544579, "lon": 127.037038, "desc": "도심 속 자연을 느낄 수 있는 휴식 공간입니다."},
    {"name": "국립중앙박물관", "lat": 37.523984, "lon": 126.980355, "desc": "한국의 대표적인 박물관으로, 다양한 전시가 열립니다."},
    {"name": "광화문", "lat": 37.575928, "lon": 126.976849, "desc": "서울의 중심이자 역사적 상징이 된 장소입니다."},
    {"name": "여의도 한강공원", "lat": 37.5283, "lon": 126.9326, "desc": "야경이 아름답고 피크닉 장소로 인기 있는 공원입니다."}
]

# --- Streamlit 설정 ---
st.set_page_config(page_title="서울 주요 관광지 Top 10", layout="centered")

st.title("🗺️ 서울 주요 관광지 Top 10")
st.write("외국인 관광객들이 가장 좋아하는 서울의 주요 관광지들을 지도에서 확인해보세요!")

# --- 지도 생성 (80% 크기 조정) ---
m = folium.Map(location=[37.5665, 126.9780], zoom_start=12, width="80%", height="80%")

# --- 관광지 마커 추가 ---
for spot in tourist_spots:
    folium.Marker(
        location=[spot["lat"], spot["lon"]],
        popup=f"<b>{spot['name']}</b><br>{spot['desc']}",
        tooltip=spot["name"],
        icon=folium.Icon(color="blue", icon="info-sign")
    ).add_to(m)

# --- 지도 표시 ---
st_folium(m, width=800, height=500)

# --- 관광지 간단 소개글 ---
st.markdown("---")
st.subheader("📍 관광지 간단 소개")
for i, spot in enumerate(tourist_spots, start=1):
    st.markdown(f"**{i}. {spot['name']}** — {spot['desc']}")

st.markdown("""
서울은 역사와 현대가 조화를 이루는 도시입니다.  
이 10곳은 한국의 문화를 경험하고 서울의 매력을 느끼기에 가장 좋은 장소로 꼽힙니다. 🇰🇷
""")
