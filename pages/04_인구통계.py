import os
from pathlib import Path
import pandas as pd
import plotly.express as px
import streamlit as st

# 1. 페이지 레이아웃 및 제목 설정
st.set_page_config(page_title="서울시 연령별 인구 분석", layout="wide")
st.title("📊 서울특별시 자치구별 연령별 인구 분포")


# 2. 상위 폴더의 population.csv 경로 추적 및 한글 깨짐 방지 로드 함수
@st.cache_data
def load_data():
    # 현재 py 파일 위치를 기준으로 상위 폴더의 population.csv 파일 경로 설정
    current_dir = Path(__file__).parent
    file_path = current_dir.parent / "population.csv"

    # 상위 폴더 경로 시도 실패 시 일반 상대 경로('../population.csv') 대체
    if not file_path.exists():
        file_path = "../population.csv"

    encodings = ["cp949", "euc-kr", "utf-8", "utf-8-sig"]
    df = None

    for enc in encodings:
        try:
            df = pd.read_csv(file_path, encoding=enc)
            break
        except (UnicodeDecodeError, Exception):
            continue

    if df is None:
        st.error(
            "상위 폴더에서 population.csv 파일을 찾을 수 없거나 인코딩 오류가 발생했습니다."
        )
        return None

    # 행정구역 명칭 정제 (예: "서울특별시 종로구 (1111000000)" -> "서울특별시 종로구")
    df["행정구역_정제"] = df["행정구역"].apply(
        lambda x: str(x).split("(")[0].strip()
    )

    # 쉼표 제거 및 숫자형 변환
    num_cols = [c for c in df.columns if c not in ["행정구역", "행정구역_정제"]]
    for c in num_cols:
        if df[c].dtype == "object":
            df[c] = (
                df[c].astype(str).str.replace(",", "").str.strip().astype(int)
            )

    return df


df = load_data()

if df is not None:
    # 3. 사이드바 필터 (행정구, 성별, 연도)
    st.sidebar.header("⚙️ 검색 옵션")

    # 연도 선택
    years = [2025]
    selected_year = st.sidebar.selectbox("연도 선택", years)

    # 행정구 선택
    region_list = df["행정구역_정제"].unique().tolist()
    selected_region = st.sidebar.selectbox("행정구 선택", region_list, index=0)

    # 성별 선택
    gender_option = st.sidebar.radio("성별 선택", ["전체", "남성", "여성"])

    # 선택된 행 추출
    row = df[df["행정구역_정제"] == selected_region].iloc[0]

    # 연령대 컬럼 정의
    age_groups = [
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

    # 성별에 따른 컬럼 매핑
    if gender_option == "전체":
        cols = [f"{selected_year}년_거주자_{g}" for g in age_groups]
    elif gender_option == "남성":
        cols = [f"{selected_year}년_남_거주자_{g}" for g in age_groups]
    else:
        cols = [f"{selected_year}년_여_거주자_{g}" for g in age_groups]

    population_values = [row[c] for c in cols]

    # 시각화용 데이터프레임 구축
    chart_df = pd.DataFrame({"나이": age_groups, "인구수": population_values})

    # 4. 꺾은선 그래프 생성 (Plotly)
    # - 연한 초록색 계열 (#90EE90)
    # - 가로축 10살 단위, 세로축 100 단위 구분선(grid) 반영
    fig = px.line(
        chart_df,
        x="나이",
        y="인구수",
        markers=True,
        title=f"<b>[{selected_region}] {selected_year}년 {gender_option} 연령별 인구 분포</b>",
    )

    fig.update_traces(
        line_color="#90EE90",
        line_width=3,
        marker=dict(size=8, color="#2E8B57"),
    )

    fig.update_layout(
        xaxis=dict(
            title="나이 (10세 단위)",
            showgrid=True,
            gridcolor="lightgrey",
            gridwidth=1,
        ),
        yaxis=dict(
            title="인구수 (명)",
            showgrid=True,
            gridcolor="lightgrey",
            gridwidth=1,
            dtick=100,  # 세로축 100 단위 구분선
        ),
        plot_bgcolor="white",
        height=550,
    )

    # 그래프 출력
    st.plotly_chart(fig, use_container_width=True)

    # 요약 정보 및 데이터표
    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("📌 요약 정보")
        st.write(f"- **선택 지역**: {selected_region}")
        st.write(f"- **선택 연도**: {selected_year}년")
        st.write(f"- **선택 성별**: {gender_option}")
        st.write(f"- **해당 조건 총 인구**: {sum(population_values):,} 명")
    with col2:
        st.subheader("📋 세부 데이터")
        st.dataframe(chart_df, use_container_width=True)
