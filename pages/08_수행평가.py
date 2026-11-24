import io
from pathlib import Path
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="🍰 디저트·간식 영양 & 달리기 계산기",
    page_icon="🏃",
    layout="centered",
)

CSV_FILENAME = "한국식품산업클러스터진흥원_영양정보_20261019 (2).csv"

# 기본 내장 백업 데이터 (CSV 파일이 없을 경우를 대비)
FALLBACK_DATA = [
    ("과자, 건빵", 419, 16.84),
    ("과자, 만주, 밤", 330, 42.45),
    ("과자, 모나카", 346, 36.58),
    ("과자, 비스킷, 하드", 534, 9.21),
    ("과자, 비스킷, 소프트", 489, 23.46),
    ("과자, 사과파이", 471, 22.83),
    ("과자, 전병", 398, 48.10),
    ("과자, 스넥, 새우", 494, 4.00),
    ("과자, 스넥, 감자", 536, 0.00),
    ("과자, 스넥, 옥수수", 520, 2.01),
    ("과자, 잼 와플", 287, 36.40),
    ("과자, 커스터드 크림 와플", 252, 15.10),
    ("과자, 초코파이", 428, 31.18),
    ("과자, 쿠키, 통밀", 471, 17.18),
    ("과자, 쿠키, 땅콩버터", 493, 22.42),
    ("과자, 쿠키, 초코칩", 494, 23.18),
    ("과자, 쿠키, 버터", 512, 16.45),
    ("과자, 크랙커, 땅콩샌드", 524, 14.64),
    ("과자, 크랙커, 치즈샌드", 497, 14.69),
    ("과자, 크랙커, 채소샌드", 506, 12.12),
    ("과자, 뻥튀기, 원반 모양, 팽화", 383, 1.74),
    ("과자, 마카로니 과자, 튀긴것", 457, 1.34),
    ("빵, 곰보빵", 415, 17.01),
    ("빵, 하드 롤빵", 293, 1.77),
    ("빵, 소프트 롤빵", 316, 6.40),
    ("빵, 모닝빵", 316, 11.33),
    ("빵, 모카빵", 354, 15.43),
    ("빵, 바게트빵", 279, 1.80),
    ("빵, 식빵", 279, 4.12),
    ("빵, 식빵, 구운것", 266, 4.15),
    ("빵, 잼빵", 297, 35.40),
    ("빵, 찐빵, 팥", 213, 10.42),
    ("빵, 카스텔라", 299, 24.85),
    ("빵, 버터 크로와상", 406, 11.26),
    ("빵, 팥빵", 253, 16.37),
    ("빵, 치즈 페이스트리", 374, 6.95),
    ("빵, 과일 페이스트리", 371, 27.53),
    ("빵, 붕어빵, 팥", 254, 11.98),
    ("빵, 소시지빵", 323, 5.05),
    ("케이크, 과일(후르츠)", 324, 27.42),
    ("케이크, 롤케이크", 369, 17.41),
    ("케이크, 생크림 블루베리", 280, 22.87),
    ("케이크, 쇼튼드 케이크", 327, 24.80),
    ("케이크, 초콜릿 케이크", 417, 38.19),
    ("케이크, 치즈 케이크", 331, 17.61),
    ("케이크, 파운드 케이크", 408, 17.43),
    ("케이크, 팬케이크", 227, None),
]


def parse_lines_to_df(lines: list[str]) -> pd.DataFrame:
    cleaned = [line.rstrip("\r\n").strip('"') for line in lines if line.strip()]
    df = pd.read_csv(io.StringIO("\n".join(cleaned)), sep="\t")
    df.columns = [c.strip() for c in df.columns]
    df["일반성분에너지"] = pd.to_numeric(df["일반성분에너지"], errors="coerce")
    df["일반성분총당류"] = pd.to_numeric(df["일반성분총당류"], errors="coerce")
    df = df.dropna(subset=["식품명한글", "일반성분에너지"]).reset_index(drop=True)
    return df


@st.cache_data
def load_data() -> tuple[pd.DataFrame, str]:
    local_path = Path(__file__).parent / CSV_FILENAME
    if local_path.exists():
        raw_bytes = local_path.read_bytes()
        for enc in ("cp949", "utf-8-sig", "utf-8"):
            try:
                text = raw_bytes.decode(enc)
                return parse_lines_to_df(text.splitlines()), f"로컬 CSV ({enc})"
            except UnicodeDecodeError:
                continue

    fallback_df = pd.DataFrame(
        FALLBACK_DATA, columns=["식품명한글", "일반성분에너지", "일반성분총당류"]
    )
    fallback_df["일반성분에너지"] = pd.to_numeric(fallback_df["일반성분에너지"])
    fallback_df["일반성분총당류"] = pd.to_numeric(fallback_df["일반성분총당류"])
    return fallback_df, "기본 내장 데이터"


df, data_source = load_data()

st.title("🍰 내가 고른 디저트·간식 영양 & 달리기 계산기 🏃")
st.caption(f"데이터 출처: 한국식품산업클러스터진흥원 영양정보 ({data_source})")

# 사이드바에서 체중 설정 (기본값 60kg)
with st.sidebar:
    st.header("⚙️ 내 신체 설정")
    weight_kg = st.slider("체중 (kg)", min_value=35, max_value=120, value=60, step=1)
    speed_kmh = st.slider("달리기 속도 (km/h)", min_value=6.0, max_value=14.0, value=8.0, step=0.5)
    st.info("💡 보통 조깅 속도는 약 8.0 km/h (1km당 약 7.5분)입니다.")

# 1. 식품 선택
selected_food = st.selectbox(
    "🍽️ 칼로리와 당류를 확인할 식품을 선택하세요",
    options=df["식품명한글"].tolist(),
)

row = df[df["식품명한글"] == selected_food].iloc[0]
kcal = float(row["일반성분에너지"])
sugar = float(row["일반성분총당류"]) if pd.notna(row["일반성분총당류"]) else None

st.markdown("---")
st.subheader(f"📊 '{selected_food}' 영양 정보")

col1, col2 = st.columns(2)
with col1:
    avg_kcal = df["일반성분에너지"].mean()
    st.metric(
        label="🔥 칼로리 (일반성분에너지)",
        value=f"{kcal:.0f} kcal",
        delta=f"전체 평균({avg_kcal:.0f} kcal) 대비 {kcal - avg_kcal:+.0f} kcal",
        delta_color="inverse",
    )

with col2:
    if sugar is not None:
        avg_sugar = df["일반성분총당류"].mean()
        who_pct = (sugar / 50.0) * 100
        st.metric(
            label="🍬 총당류 (일반성분총당류)",
            value=f"{sugar:.2f} g",
            delta=f"WHO 권장 50g의 {who_pct:.1f}% (평균 {avg_sugar:.1f}g)",
            delta_color="inverse",
        )
    else:
        st.metric(
            label="🍬 총당류 (일반성분총당류)",
            value="데이터 없음 (NaN)",
            delta="해당 식품의 총당류 기록이 비어 있어요",
        )

st.markdown("---")

# 2. 달리기 모양 이모지 버튼
# 달리기 MET 8.3 기준: kcal/min = (8.3 * 3.5 * weight_kg) / 200
# 1km 이동 시간(분) = (1 / speed_kmh) * 60 -> 1km당 소모 열량 = kcal/min * (60 / speed_kmh)
kcal_per_min = (8.3 * 3.5 * weight_kg) / 200.0
kcal_per_km = kcal_per_min * (60.0 / speed_kmh)
km_needed = kcal / kcal_per_km
est_minutes = (km_needed / speed_kmh) * 60.0

if st.button("🏃‍♂️", help="이 식품을 먹었을 때 뛰어야 할 거리(km) 계산하기"):
    st.session_state["show_run_result"] = True

if st.session_state.get("show_run_result", False):
    st.success(f"🏃‍♂️ **{selected_food}** ({kcal:.0f} kcal)를 소모하려면 약 **{km_needed:.2f} km**를 뛰어야 해요!")
    st.write(
        f"- **계산 기준:** 체중 **{weight_kg} kg**, 시속 **{speed_kmh:.1f} km/h** 달리기 (1km당 약 **{kcal_per_km:.1f} kcal** 소모, 예상 소요 시간 약 **{est_minutes:.0f}분**)"
    )

    # 체감하기 쉬운 예시 (400m 트랙 기준)
    track_laps = km_needed / 0.4
    st.info(
        f"🏟️ **체감 예시:** 학교 운동장 **400m 트랙 약 {track_laps:.1f}바퀴**를 돌아야 하는 거리예요! "
        f"(편의점~학교 왕복이나 동네 공원 한 바퀴를 떠올려 보세요 🌳)"
    )
