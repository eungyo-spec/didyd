import pandas as pd
import plotly.graph_objects as go
import streamlit as st

# 페이지 레이아웃 설정
st.set_page_config(
    page_title="서울시 연령별 인구수 분석", page_icon="📈", layout="wide"
)

st.title("📈 연령대별 인구수 추이 분석")
st.caption("2025년 서울특별시 및 자치구별 연령/성별 인구 데이터")


# 1. 데이터 로드 (EUC-KR 인코딩 & 천 단위 쉼표 자동 처리)
@st.cache_data
def load_data():
    # 한글 깨짐 방지를 위한 euc-kr 인코딩 사용
    df = pd.read_csv("population.csv", encoding="euc-kr", thousands=",")

    # 행정구역 명칭 정제 (예: '서울특별시 종로구 (1111000000)' -> '종로구')
    df["행정구"] = (
        df["행정구역"].str.split("(").str[0].str.replace("서울특별시", "").str.strip()
    )
    df["행정구"] = df["행정구"].apply(lambda x: "서울특별시 전체" if x == "" else x)
    return df


try:
    df = load_data()
except Exception as e:
    st.error(
        f"파일을 읽는 중 오류가 발생했습니다. 'population.csv' 파일이 동일한 경로에 있는지 확인해주세요. ({e})"
    )
    st.stop()

# 연령대 컬럼 목록 정의
age_categories = [
    "0~9세",
    "10~19세",
    "20~29세",
    "30~39세",
    "40~49세",
    "50~59세",
    "60~69세",
    "70~79세",
    "80~89세",
    "90~99세",
    "100세 이상",
]

# 2. 사이드바 - 조건 선택 (연도, 행정구, 성별)
st.sidebar.header("⚙️ 조회 조건 선택")

# 연도 선택 (데이터셋 기준 2025년)
selected_year = st.sidebar.selectbox("연도 선택", ["2025년"])

# 행정구 선택
district_list = df["행정구"].tolist()
selected_district = st.sidebar.selectbox(
    "행정구 선택",
    district_list,
    index=1 if len(district_list) > 1 else 0,
)

# 성별 선택
gender_option = st.sidebar.selectbox("성별 선택", ["전체", "남성", "여성"])

# 3. 데이터 추출
target_row = df[df["행정구"] == selected_district].iloc[0]

# 성별 옵션에 따른 컬럼 매핑
if gender_option == "전체":
    prefix = f"{selected_year}_거주자_"
elif gender_option == "남성":
    prefix = f"{selected_year}_남_거주자_"
else:
    prefix = f"{selected_year}_여_거주자_"

population_values = [target_row[f"{prefix}{age}"] for age in age_categories]

# 4. Plotly 꺾은선 그래프 생성
fig = go.Figure()

fig.add_trace(
    go.Scatter(
        x=age_categories,
        y=population_values,
        mode="lines+markers",
        name=f"{selected_district} ({gender_option})",
        # 연한 초록색 선 및 마커 설정 (#90EE90: LightGreen)
        line=dict(color="#90EE90", width=3),
        marker=dict(size=8, color="#2E8B57"),
        hovertemplate="연령대: %{x}<br>인구수: %{y:,.0f}명<extra></extra>",
    )
)

# 5. 그래프 레이아웃 및 눈금/구분선 설정
fig.update_layout(
    title=dict(
        text=f"<b>[{selected_year}] {selected_district} - {gender_option} 연령별 인구수</b>",
        font=dict(size=18),
    ),
    xaxis=dict(
        title="나이 (연령대)",
        showgrid=True,
        gridcolor="#E5E5E5",
        gridwidth=1,
        dtick=1,  # 10살 단위(각 카테고리)마다 구분선 표시
    ),
    yaxis=dict(
        title="인구수 (명)",
        showgrid=True,
        gridcolor="#E5E5E5",
        gridwidth=1,
        dtick=100,  # 세로축 100단위 구분선 표시
        tickformat=",d",
    ),
    hovermode="x unified",
    plot_bgcolor="white",
    height=550,
)

# 6. Streamlit 화면 출력
st.plotly_chart(fig, use_container_width=True)

# 상세 데이터 표 보기
with st.expander("📊 상세 데이터 확인하기"):
    data_df = pd.DataFrame(
        {"연령대": age_categories, "인구수(명)": population_values}
    )
    st.dataframe(data_df.T, use_container_width=True)
