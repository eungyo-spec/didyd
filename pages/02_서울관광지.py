import os, zipfile

base = "/mnt/data/seoul_tourism_map"
os.makedirs(base, exist_ok=True)

app_py = """import streamlit as st
import streamlit.components.v1 as components
import json

st.set_page_config(page_title="서울 인기 관광지 TOP 10", page_icon="🗺️", layout="wide")

spots = [
 {"rank":1,"name":"경복궁","en":"Gyeongbokgung Palace","lat":37.5796,"lon":126.9770,"category":"역사·문화","desc":"조선 왕조의 대표 궁궐이에요. 한복을 입고 고궁을 거닐며 한국의 전통 건축과 역사를 만날 수 있어요."},
 {"rank":2,"name":"N서울타워","en":"N Seoul Tower","lat":37.5512,"lon":126.9882,"category":"전망·야경","desc":"남산에 있는 서울의 대표 전망 명소예요. 도시 전경과 야경을 감상하기 좋아요."},
 {"rank":3,"name":"명동","en":"Myeong-dong","lat":37.5636,"lon":126.9850,"category":"쇼핑·먹거리","desc":"화장품 매장과 길거리 음식, 쇼핑 공간이 모여 있어 활기찬 서울의 분위기를 느낄 수 있어요."},
 {"rank":4,"name":"북촌 한옥마을","en":"Bukchon Hanok Village","lat":37.5826,"lon":126.9830,"category":"전통·산책","desc":"전통 한옥이 이어지는 동네예요. 주민들이 생활하는 곳이므로 조용히 둘러보고 사생활을 존중해 주세요."},
 {"rank":5,"name":"인사동","en":"Insadong","lat":37.5740,"lon":126.9857,"category":"공예·문화","desc":"전통 공예품과 기념품 가게, 찻집을 만날 수 있어 한국의 멋을 경험하기 좋은 거리예요."},
 {"rank":6,"name":"홍대 거리","en":"Hongdae","lat":37.5563,"lon":126.9236,"category":"음악·문화","desc":"개성 있는 카페와 상점, 공연과 거리 문화로 유명해 젊고 자유로운 분위기를 즐길 수 있어요."},
 {"rank":7,"name":"동대문디자인플라자(DDP)","en":"Dongdaemun Design Plaza","lat":37.5671,"lon":127.0095,"category":"건축·전시","desc":"독특한 곡선형 건축물과 디자인 전시, 행사로 잘 알려진 복합 문화 공간이에요."},
 {"rank":8,"name":"창덕궁","en":"Changdeokgung Palace","lat":37.5794,"lon":126.9910,"category":"역사·자연","desc":"자연 지형과 조화를 이루는 궁궐이에요. 아름다운 정원과 한국 전통 궁궐 문화를 함께 감상할 수 있어요."},
 {"rank":9,"name":"광장시장","en":"Gwangjang Market","lat":37.5700,"lon":126.9997,"category":"시장·음식","desc":"빈대떡, 김밥 등 다양한 한국 음식을 맛볼 수 있는 전통시장으로, 현지 먹거리 탐방에 좋아요."},
 {"rank":10,"name":"청계천","en":"Cheonggyecheon Stream","lat":37.5692,"lon":126.9780,"category":"산책·휴식","desc":"도심 한가운데를 흐르는 산책 공간이에요. 잠시 쉬어 가거나 도심 풍경을 즐기기 좋아요."}
]

st.title("🗺️ 외국인 여행자를 위한 서울 인기 관광지 TOP 10")
st.caption("서울 여행 계획을 세울 때 참고할 수 있는 대표 명소 모음이에요. 순위는 공식 실시간 집계가 아닌 안내용 추천 목록입니다.")
st.info("📍 지도에서 번호가 붙은 마커를 누르면 관광지 이름과 간단한 설명을 볼 수 있어요. 지도 타일을 불러오려면 인터넷 연결이 필요합니다.")

map_html = '''
<!DOCTYPE html><html><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"/>
<style>
html,body{margin:0;padding:0;font-family:Arial,sans-serif}
#map{height:590px;width:100%;border-radius:12px}
.pin{background:#1769aa;color:white;border:2px solid white;border-radius:50%;width:30px;height:30px;line-height:26px;text-align:center;font-weight:bold;box-shadow:0 1px 5px #777}
.popup-title{font-size:15px;font-weight:bold;margin-bottom:4px}
.popup-en{color:#555;font-size:12px;margin-bottom:6px}
.popup-desc{line-height:1.45;max-width:230px}
</style></head><body><div id="map"></div>
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<script>
const spots = __SPOTS__;
const map = L.map('map').setView([37.5665,126.9780],12);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',{
 maxZoom:19, attribution:'&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map);
const safe = v => String(v).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const bounds=[];
spots.forEach(s=>{
 const icon=L.divIcon({className:'',html:`<div class="pin">${s.rank}</div>`,iconSize:[30,30],iconAnchor:[15,15]});
 const popup=`<div class="popup-title">${s.rank}. ${safe(s.name)}</div><div class="popup-en">${safe(s.en)} · ${safe(s.category)}</div><div class="popup-desc">${safe(s.desc)}</div>`;
 L.marker([s.lat,s.lon],{icon}).addTo(map).bindPopup(popup);
 bounds.push([s.lat,s.lon]);
});
map.fitBounds(bounds,{padding:[28,28]});
</script></body></html>
'''
components.html(map_html.replace("__SPOTS__", json.dumps(spots, ensure_ascii=False)), height=610, scrolling=False)

st.subheader("✨ 관광지 한눈에 보기")
for i in range(0, len(spots), 2):
    cols = st.columns(2)
    for col, spot in zip(cols, spots[i:i+2]):
        with col:
            st.markdown(f"### {spot['rank']}. {spot['name']}")
            st.caption(f"{spot['en']} · {spot['category']}")
            st.write(spot["desc"])

st.divider()
st.caption("참고: 관광지 선호도는 방문객 국적·여행 시기·조사 기관에 따라 달라질 수 있습니다. 이 목록은 외국인 여행자에게 잘 알려진 대표 명소를 모은 추천 목록이며, 공식 선호도 순위를 의미하지 않습니다.")
"""

requirements = "streamlit>=1.30.0\\n"
readme = """# 서울 인기 관광지 TOP 10 지도 (Streamlit)

## 파일
- `app.py`: Streamlit 앱 코드
- `requirements.txt`: Streamlit 설치 설정

## Streamlit Community Cloud 배포
1. 두 파일을 GitHub 저장소 최상위 폴더에 업로드합니다.
2. Streamlit Community Cloud에서 해당 저장소를 선택합니다.
3. Main file path에 `app.py`를 지정하고 배포합니다.

지도는 브라우저에서 Leaflet과 OpenStreetMap 타일을 불러옵니다. 지도 타일을 보려면 인터넷 연결이 필요합니다. 별도의 지도 라이브러리는 설치하지 않습니다.

TOP 10은 공식 실시간 순위가 아니라 외국인 여행자에게 잘 알려진 대표 관광지를 모은 안내용 추천 목록입니다.
"""

for name, content in [("app.py", app_py), ("requirements.txt", requirements), ("README.md", readme)]:
    with open(os.path.join(base, name), "w", encoding="utf-8") as f:
        f.write(content)

zip_path = "/mnt/data/seoul_tourism_map_streamlit.zip"
with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
    for name in ["app.py", "requirements.txt", "README.md"]:
        z.write(os.path.join(base, name), arcname=name)

print("완료: app.py, requirements.txt, README.md를 만들고 ZIP으로 묶었습니다.")
