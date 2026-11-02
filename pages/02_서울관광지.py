import os, zipfile, textwrap

project_dir = "/mnt/data/seoul_tourism_map"
os.makedirs(project_dir, exist_ok=True)

app_code = r'''import streamlit as st
import folium
from streamlit_folium import st_folium

st.set_page_config(
    page_title="서울 인기 관광지 TOP 10",
    page_icon="🗺️",
    layout="wide"
)

# 대표 관광지 10곳입니다. 공식 통계 순위가 아닌, 해외 방문객에게 잘 알려진 명소를
# 바탕으로 구성한 추천 목록입니다.
PLACES = [
    {
        "rank": 1, "name": "경복궁", "category": "역사 · 전통문화",
        "lat": 37.5796, "lon": 126.9770,
        "description": "조선 왕조의 대표 궁궐이에요. 한복을 입고 궁궐을 둘러보며 한국의 전통 건축과 역사를 느낄 수 있어요.",
        "tip": "관람 시간과 휴궁일을 방문 전에 확인하세요."
    },
    {
        "rank": 2, "name": "명동", "category": "쇼핑 · 먹거리",
        "lat": 37.5636, "lon": 126.9869,
        "description": "화장품 매장과 쇼핑 거리, 길거리 음식으로 유명해요. 쇼핑과 한국 간식을 한 번에 즐기기 좋아요.",
        "tip": "저녁 시간에는 길거리 음식 노점이 활기를 띠어요."
    },
    {
        "rank": 3, "name": "N서울타워", "category": "전망 · 야경",
        "lat": 37.5512, "lon": 126.9882,
        "description": "남산 위에서 서울의 전경을 감상할 수 있는 전망 명소예요. 특히 해 질 무렵과 밤 풍경이 아름다워요.",
        "tip": "날씨가 맑은 날 방문하면 전망을 더 잘 즐길 수 있어요."
    },
    {
        "rank": 4, "name": "북촌한옥마을", "category": "전통문화 · 산책",
        "lat": 37.5826, "lon": 126.9830,
        "description": "한옥이 모여 있는 골목에서 서울의 전통적인 분위기를 만날 수 있어요. 사진 촬영과 조용한 산책으로 인기예요.",
        "tip": "실제 주민들이 사는 곳이니 조용히 둘러봐 주세요."
    },
    {
        "rank": 5, "name": "홍대거리", "category": "문화 · 쇼핑 · 밤문화",
        "lat": 37.5563, "lon": 126.9236,
        "description": "젊은 감성의 카페와 패션 매장, 거리 공연이 어우러진 곳이에요. 개성 있는 문화를 경험하기 좋아요.",
        "tip": "주말에는 거리 공연과 다양한 팝업을 만날 수 있어요."
    },
    {
        "rank": 6, "name": "동대문디자인플라자(DDP)", "category": "건축 · 전시",
        "lat": 37.5670, "lon": 127.0095,
        "description": "독특한 곡선 형태의 건축물로 유명해요. 전시와 디자인 행사, 야간 조명을 즐길 수 있어요.",
        "tip": "방문일에 열리는 전시와 행사를 미리 확인해 보세요."
    },
    {
        "rank": 7, "name": "창덕궁", "category": "역사 · 정원",
        "lat": 37.5794, "lon": 126.9910,
        "description": "자연 지형을 살린 아름다운 궁궐이에요. 고즈넉한 분위기와 전통 정원을 감상할 수 있어요.",
        "tip": "후원 관람은 별도 예약이나 운영 조건이 있을 수 있어요."
    },
    {
        "rank": 8, "name": "광장시장", "category": "전통시장 · 음식",
        "lat": 37.5701, "lon": 126.9997,
        "description": "빈대떡, 김밥 등 다양한 한국 음식을 맛볼 수 있는 전통시장이에요. 현지 먹거리를 경험하기 좋아요.",
        "tip": "혼잡할 수 있으니 소지품을 잘 챙기고 천천히 둘러보세요."
    },
    {
        "rank": 9, "name": "롯데월드타워 서울스카이", "category": "전망 · 랜드마크",
        "lat": 37.5125, "lon": 127.1025,
        "description": "높은 전망대에서 서울과 한강 주변 풍경을 넓게 볼 수 있어요. 쇼핑과 식사를 함께 즐기기에도 편리해요.",
        "tip": "전망대 입장권과 운영 시간을 사전에 확인하세요."
    },
    {
        "rank": 10, "name": "청계천", "category": "도심 산책 · 휴식",
        "lat": 37.5692, "lon": 126.ile if False else 126.9788,
        "description": "도심 한가운데 흐르는 산책 공간이에요. 주변 명소와 함께 걸으며 서울의 색다른 모습을 느낄 수 있어요.",
        "tip": "주변 일정과 연결해 가볍게 산책하기 좋아요."
    },
]

st.title("🗺️ 서울 인기 관광지 TOP 10")
st.write("지도에서 번호가 표시된 마커를 눌러 관광지 이름과 간단한 정보를 확인해 보세요.")
st.caption("※ 공식 방문객 수 순위가 아니라, 해외 여행객에게 잘 알려진 서울의 대표 명소를 모은 추천 목록입니다. 운영 시간·입장 정보는 방문 전에 공식 안내를 확인하세요.")

with st.sidebar:
    st.header("🔎 관광지 찾기")
    selected_categories = st.multiselect(
        "관광 유형 선택",
        options=sorted({p["category"] for p in PLACES}),
        default=sorted({p["category"] for p in PLACES})
    )
    st.info("마커를 클릭하면 지도에서 관광지 정보를 볼 수 있어요.")

filtered_places = [p for p in PLACES if p["category"] in selected_categories]

m = folium.Map(
    location=[37.5665, 126.9780],
    zoom_start=12,
    tiles="OpenStreetMap",
    control_scale=True
)

for place in filtered_places:
    popup_html = f"""
    <div style="font-family: sans-serif; width: 220px;">
      <h4 style="margin-bottom: 6px;">{place['rank']}. {place['name']}</h4>
      <p style="margin: 0 0 6px 0;"><b>{place['category']}</b></p>
      <p style="margin: 0;">{place['description']}</p>
    </div>
    """
    folium.Marker(
        location=[place["lat"], place["lon"]],
        tooltip=f"{place['rank']}. {place['name']}",
        popup=folium.Popup(popup_html, max_width=300),
        icon=folium.DivIcon(
            html=f"""
            <div style="
                background:#e63946; color:white; border:2px solid white;
                border-radius:50%; width:30px; height:30px;
                display:flex; align-items:center; justify-content:center;
                font-weight:bold; font-size:13px; box-shadow:0 1px 5px #555;">
                {place['rank']}
            </div>""",
            icon_size=(30, 30),
            icon_anchor=(15, 15)
        )
    ).add_to(m)

if not filtered_places:
    st.warning("선택한 유형의 관광지가 없어요. 왼쪽에서 유형을 하나 이상 선택해 주세요.")
else:
    st_folium(m, use_container_width=True, height=560, returned_objects=[])

st.subheader("📍 관광지 한눈에 보기")
st.write("지도 아래에서 각 장소의 매력과 방문 팁을 확인해 보세요.")

for place in filtered_places:
    with st.container(border=True):
        left, right = st.columns([1, 4])
        with left:
            st.markdown(f"### {place['rank']}.")
            st.markdown(f"**{place['category']}**")
        with right:
            st.markdown(f"### {place['name']}")
            st.write(place["description"])
            st.caption(f"💡 방문 팁: {place['tip']}")

st.divider()
st.caption("서울 여행 아이디어를 위한 안내 앱입니다. 위치는 지도 표시용 대략적인 좌표이며, 순위는 공식 통계 순위를 의미하지 않습니다.")
'''
# Fix a deliberately awkward coordinate expression into a normal numeric literal.
app_code = app_code.replace("126.ile if False else 126.9788", "126.9788")

requirements = """streamlit
folium
streamlit-folium
"""

readme = """# 서울 인기 관광지 TOP 10 지도 (Streamlit)

## 포함 파일
- `app.py`: 서울 관광지 지도와 장소별 설명
- `requirements.txt`: Streamlit Cloud에서 설치할 패키지 목록

## Streamlit Community Cloud에 배포하기
1. 이 ZIP 파일을 풀어 GitHub 저장소에 `app.py`, `requirements.txt`를 올립니다.
2. Streamlit Community Cloud에서 **Create app**을 선택합니다.
3. 저장소, 브랜치, 메인 파일 경로 `app.py`를 지정하고 배포합니다.
4. 앱은 `requirements.txt`를 읽어 필요한 패키지를 설치합니다.

## 참고
지도 타일을 표시하려면 앱 이용자의 인터넷 연결이 필요합니다. 관광지 목록은 해외 여행객에게 잘 알려진 대표 명소를 선정한 것이며, 공식 방문객 통계에 따른 순위는 아닙니다.
"""

with open(os.path.join(project_dir, "app.py"), "w", encoding="utf-8") as f:
    f.write(app_code)
with open(os.path.join(project_dir, "requirements.txt"), "w", encoding="utf-8") as f:
    f.write(requirements)
with open(os.path.join(project_dir, "README.md"), "w", encoding="utf-8") as f:
    f.write(readme)

zip_path = "/mnt/data/seoul_tourism_map_streamlit.zip"
with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
    for name in ["app.py", "requirements.txt", "README.md"]:
        z.write(os.path.join(project_dir, name), arcname=name)

print("Created:", zip_path)
print("Files:", os.listdir(project_dir))
