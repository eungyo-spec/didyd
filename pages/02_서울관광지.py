import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd

# 데이터 준비 (외국인 선호 서울 주요 관광지 TOP 10)
spots = [
    {
        "rank": 1,
        "name": "경복궁",
        "lat": 37.5796,
        "lng": 126.9770,
        "category": "역사/문화",
        "desc": "조선 왕조의 대표적인 법궁으로, 한복을 입고 방문하는 외국인들에게 인기가 매우 높습니다. 수문장 교대식도 주요 볼거리입니다."
    },
    {
        "rank": 2,
        "name": "N서울타워 (남산타워)",
        "lat": 37.5512,
        "lng": 126.9882,
        "category": "랜드마크/전망",
        "desc": "서울 도심 전경을 한눈에 조망할 수 있는 대표 랜드마크입니다. 자물쇠 나무와 케이블카 체험이 유명합니다."
    },
    {
        "rank": 3,
        "name": "명동 쇼핑거리",
        "lat": 37.5636,
        "lng": 126.9822,
        "category": "쇼핑/길거리음식",
        "desc": "K-뷰티 화장품 쇼핑과 다양한 길거리 음식을 즐길 수 있는 필수 방문 코스입니다."
    },
    {
        "rank": 4,
        "name": "북촌한옥마을",
        "lat": 37.5826,
        "lng": 126.9831,
        "category": "전통/골목",
        "desc": "실제 주민들이 거주하는 전통 한옥 주택가로, 한옥과 도심 빌딩이 어우러진 포토존이 인기가 많습니다."
    },
    {
        "rank": 5,
        "name": "인사동 쌈지길",
        "lat": 37.5742,
        "lng": 126.9848,
        "category": "전통공예/문화",
        "desc": "전통 차, 고미술품, 퓨전 공예품 등을 판매하는 거리로 한국적 기념품을 사기에 최적의 장소입니다."
    },
    {
        "rank": 6,
        "name": "동대문디자인플라자 (DDP)",
        "lat": 37.5665,
        "lng": 127.0092,
        "category": "현대건축/야경",
        "desc": "세계적인 건축가 자하 하디드가 설계한 곡선미가 돋보이는 곡면 건축물로, 전시와 야경 명소로 유명합니다."
    },
    {
        "rank": 7,
        "name": "홍대 거리",
        "lat": 37.5563,
        "lng": 126.9226,
        "category": "젊음/버스킹/클럽",
        "desc": "K-POP 버스킹 공연, 독특한 카페, 트렌디한 패션숍, 밤문화 등이 집약된 서교동·동교동 일대입니다."
    },
    {
        "rank": 8,
        "name": "롯데월드 & 롯데월드타워",
        "lat": 37.5111,
        "lng": 127.0982,
        "category": "엔터테인먼트/전망",
        "desc": "실내외 테마파크인 롯데월드와 국내 최고층 건물인 롯데월드타워(서울스카이 전망대)가 위치해 있습니다."
    },
    {
        "rank": 9,
        "name": "국립중앙박물관",
        "lat": 37.5240,
        "lng": 126.9804,
        "category": "역사/박물관",
        "desc": "한국의 선사 시대부터 근대까지의 수많은 문화재와 국보(사유의 방 등)를 관람할 수 있는 국립 박물관입니다."
    },
    {
        "rank": 10,
        "name": "반포한강공원 (무지개분수)",
        "lat": 37.5102,
        "lng": 126.9960,
        "category": "자연/야경/피크닉",
        "desc": "세계 최장 교량 분수인 달빛무지개분수와 한강 라면 피크닉 문화를 즐길 수 있는 명소입니다."
    }
]

df = pd.DataFrame(spots)

# UI 헤더
st.title("🗽 외국인이 좋아하는 서울 주요 관광지 TOP 10")
st.markdown("서울 중심부 지도 위에 외국인 관광객들에게 가장 인기 있는 명소 10곳을 표시했습니다.")
st.write("---")

# 1. Folium 지도 생성
m = folium.Map(location=[37.555, 126.985], zoom_start=12, tiles="OpenStreetMap")

# 마커 추가
for idx, row in df.iterrows():
    popup_text = f"<b>{row['rank']}위. {row['name']}</b><br>분류: {row['category']}"
    folium.Marker(
        location=[row["lat"], row["lng"]],
        popup=folium.Popup(popup_text, max_width=250),
        tooltip=f"{row['rank']}위. {row['name']}",
        icon=folium.Icon(color="red" if row["rank"] <= 3 else "blue", icon="star")
    ).add_to(m)

# 지도를 화면에 출력
st.subheader("📍 서울 관광지 지도")
st_folium(m, width=1100, height=500)

st.write("---")

# 2. 관광지 상세 설명 출력
st.subheader("📑 관광지별 상세 안내")

col1, col2 = st.columns(2)

for idx, row in df.iterrows():
    target_col = col1 if idx % 2 == 0 else col2
    
    with target_col:
        with st.expander(f"**{row['rank']}위. {row['name']}** ({row['category']})", expanded=True):
            st.write(row["desc"])
