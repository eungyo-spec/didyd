import pandas as pd
import plotly.graph_objects as go
import streamlit as st

# 1. 페이지 설정
st.set_page_config(
    page_title="MBTI별 국가 Top 10 순위", page_icon="🏆", layout="wide"
)


# 2. 데이터 로드 (캐싱 적용)
@st.cache_data
def load_data():
  df = pd.read_csv("countriesMBTI_16types (1).csv")

  # 영문 국가명을 한국어 국가명으로 변환하기 위한 딕셔너리
  country_map = {
      "Afghanistan": "아프가니스탄",
      "Albania": "알바니아",
      "Algeria": "알제리",
      "Andorra": "안도라",
      "Angola": "앙골라",
      "Antigua and Barbuda": "앤티가 바부다",
      "Argentina": "아르헨티나",
      "Armenia": "아르메니아",
      "Australia": "호주",
      "Austria": "오스트리아",
      "Azerbaijan": "아제르바이잔",
      "Bahamas": "바하마",
      "Bahrain": "바레인",
      "Bangladesh": "방글라데시",
      "Barbados": "바베이도스",
      "Belarus": "벨라루스",
      "Belgium": "벨기에",
      "Belize": "벨리즈",
      "Bhutan": "부탄",
      "Bosnia and Herzegovina": "보스니아 헤르체고비나",
      "Botswana": "보츠와나",
      "Brazil": "브라질",
      "Brunei": "브루나이",
      "Bulgaria": "불가리아",
      "Burkina Faso": "부르키나파소",
      "Burundi": "부룬디",
      "Cambodia": "캄보디아",
      "Cameroon": "카메룬",
      "Canada": "캐나다",
      "Cape Verde": "카보베르데",
      "Central African Republic": "중앙아프리카 공화국",
      "Chad": "차드",
      "Chile": "칠레",
      "China": "중국",
      "Colombia": "콜롬비아",
      "Comoros": "코모로",
      "Congo": "콩고공화국",
      "Costa Rica": "코스타리카",
      "Croatia": "크로아티아",
      "Cuba": "쿠바",
      "Cyprus": "키프로스",
      "Czech Republic": "체코",
      "Denmark": "덴마크",
      "Djibouti": "지부티",
      "Dominica": "도미니카",
      "Dominican Republic": "도미니카 공화국",
      "Ecuador": "에콰도르",
      "Egypt": "이집트",
      "El Salvador": "엘살바도르",
      "Equatorial Guinea": "적도 기니",
      "Eritrea": "에리트레아",
      "Estonia": "에스토니아",
      "Eswatini": "에스와티니",
      "Ethiopia": "에티오피아",
      "Fiji": "피지",
      "Finland": "핀란드",
      "France": "프랑스",
      "Gabon": "가봉",
      "Gambia": "감비아",
      "Georgia": "조지아",
      "Germany": "독일",
      "Ghana": "가나",
      "Greece": "그리스",
      "Grenada": "그레나다",
      "Guatemala": "과테말라",
      "Guinea": "기니",
      "Guinea-Bissau": "기니비사우",
      "Guyana": "가이아나",
      "Haiti": "아이티",
      "Honduras": "온두라스",
      "Hungary": "헝가리",
      "Iceland": "아이슬란드",
      "India": "인도",
      "Indonesia": "인도네시아",
      "Iran": "이란",
      "Iraq": "이라크",
      "Ireland": "아일랜드",
      "Israel": "이스라엘",
      "Italy": "이탈리아",
      "Jamaica": "자메이카",
      "Japan": "일본",
      "Jordan": "요르단",
      "Kazakhstan": "카자흐스탄",
      "Kenya": "케냐",
      "Kiribati": "키리바시",
      "Kuwait": "쿠웨이트",
      "Kyrgyzstan": "키르기스스탄",
      "Laos": "라오스",
      "Latvia": "라트비아",
      "Lebanon": "레바논",
      "Lesotho": "레소토",
      "Liberia": "라이베리아",
      "Libya": "리비아",
      "Liechtenstein": "리히텐슈타인",
      "Lithuania": "리투아니아",
      "Luxembourg": "룩셈부르크",
      "Madagascar": "마다가스카르",
      "Malawi": "말라위",
      "Malaysia": "말레이시아",
      "Maldives": "몰디브",
      "Mali": "말리",
      "Malta": "몰타",
      "Mauritania": "모리타니",
      "Mauritius": "모리셔스",
      "Mexico": "멕시코",
      "Micronesia": "미크로네시아",
      "Moldova": "몰도바",
      "Monaco": "모나코",
      "Mongolia": "몽골",
      "Montenegro": "몬테네그로",
      "Morocco": "모로코",
      "Mozambique": "모잠비크",
      "Myanmar": "미얀마",
      "Namibia": "나미비아",
      "Nauru": "나우루",
      "Nepal": "네팔",
      "Netherlands": "네덜란드",
      "New Zealand": "뉴질랜드",
      "Nicaragua": "니카라과",
      "Niger": "니제르",
      "Nigeria": "나이지리아",
      "North Korea": "북한",
      "North Macedonia": "북마케도니아",
      "Norway": "노르웨이",
      "Oman": "오만",
      "Pakistan": "파키스탄",
      "Palau": "팔라우",
      "Panama": "파나마",
      "Papua New Guinea": "파푸아뉴기니",
      "Paraguay": "파라과이",
      "Peru": "페루",
      "Philippines": "필리핀",
      "Poland": "폴란드",
      "Portugal": "포르투갈",
      "Qatar": "카타르",
      "Romania": "루마니아",
      "Russia": "러시아",
      "Rwanda": "르완다",
      "Saint Kitts and Nevis": "세인트키츠 네비스",
      "Saint Lucia": "세인트루시아",
      "Saint Vincent and the Grenadines": "세인트빈센트 그레나딘",
      "Samoa": "사모아",
      "San Marino": "산마리노",
      "Sao Tome and Principe": "상투메 프린시페",
      "Saudi Arabia": "사우디아라비아",
      "Senegal": "세네갈",
      "Serbia": "세르비아",
      "Seychelles": "세이셸",
      "Sierra Leone": "시에라리온",
      "Singapore": "싱가포르",
      "Slovakia": "슬로바키아",
      "Slovenia": "슬로베니아",
      "Solomon Islands": "솔로몬 제도",
      "Somalia": "소말리아",
      "South Africa": "남아프리카 공화국",
      "South Korea": "대한민국",
      "Spain": "스페인",
      "Sri Lanka": "스리랑카",
      "Sudan": "수단",
      "Suriname": "수리남",
      "Sweden": "스웨덴",
      "Switzerland": "스위스",
      "Syria": "시리아",
      "Taiwan": "대만",
      "Tajikistan": "타지키스탄",
      "Tanzania": "탄자니아",
      "Thailand": "태국",
      "Timor-Leste": "동티모르",
      "Togo": "토고",
      "Tonga": "통가",
      "Trinidad and Tobago": "트리니다드 토바고",
      "Tunisia": "튀니지",
      "Turkey": "튀르키예",
      "Turkmenistan": "투르크메니스탄",
      "Tuvalu": "투발루",
      "Uganda": "우간다",
      "Ukraine": "우크라이나",
      "United Arab Emirates": "아랍에미리트",
      "United Kingdom": "영국",
      "United States": "미국",
      "Uruguay": "우루과이",
      "Uzbekistan": "우즈베키스탄",
      "Vanuatu": "바누아투",
      "Vatican City": "바티칸 시국",
      "Venezuela": "베네수엘라",
      "Vietnam": "베트남",
      "Yemen": "예멘",
      "Zambia": "잠비아",
      "Zimbabwe": "짐바브웨",
  }

  # 매핑 목록에 있는 경우 한글로 변경, 없으면 원본 유지
  df["Country"] = df["Country"].map(country_map).fillna(df["Country"])
  return df


df = load_data()
mbti_cols = [c for c in df.columns if c != "Country"]

# 메인 타이틀
st.title("🏆 MBTI별 국가 Top 10 순위 및 비율 시각화")
st.markdown(
    "원하는 **MBTI 유형**을 선택하면, 해당 비율이 가장 높은 **상위 10개 국가(한글"
    " 명칭)**를 막대그래프로 보여줍니다. (1위: 노란색, 2위~10위: 초록색 그라데이션)"
)

# 3. 사이드바 - MBTI 선택
selected_mbti = st.sidebar.selectbox(
    "🔍 분석할 MBTI 유형을 선택하세요:", options=mbti_cols
)

# 4. 데이터 정렬 및 Top 10 추출
rank_df = df[["Country", selected_mbti]].copy()
rank_df["Percentage"] = rank_df[selected_mbti] * 100
rank_df = (
    rank_df.sort_values(by="Percentage", ascending=False)
    .head(10)
    .reset_index(drop=True)
)

# 5. Top 10에 맞춘 초록색 그라데이션 색상 생성 (1등 제외 9개 색상)
num_bars = len(rank_df)


def get_green_gradient(n):
  colors = []
  for i in range(n):
    r = int(20 + (234 - 20) * (i / max(1, n - 1)))
    g = int(90 + (250 - 90) * (i / max(1, n - 1)))
    b = int(50 + (241 - 50) * (i / max(1, n - 1)))
    colors.append(f"rgb({r},{g},{b})")
  return colors


green_colors = get_green_gradient(num_bars - 1)

# 1등은 노란색(#FFD700), 2위~10위는 초록색 그라데이션 적용
bar_colors = ["#FFD700"] + green_colors

# 6. Plotly 막대그래프 생성
fig = go.Figure(
    data=[
        go.Bar(
            x=rank_df["Country"],
            y=rank_df["Percentage"],
            text=[f"{val:.2f}%" for val in rank_df["Percentage"]],
            textposition="auto",
            marker=dict(color=bar_colors),
        )
    ]
)

fig.update_layout(
    title=dict(
        text=f"<b>'{selected_mbti}' 비율 Top 10 국가 순위</b>",
        font=dict(size=20),
    ),
    xaxis_title="국가",
    yaxis_title="비율 (%)",
    template="plotly_white",
    height=550,
)

# 7. 화면 출력
