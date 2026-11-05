import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# 페이지 레이아웃 설정
st.set_page_config(
    page_title="서울시 연령별 인구수 분석", page_icon="📈", layout="wide"
)

st.title("📈 연령대별 인구수 추이 및 구별 비교 분석")
st.caption("2025년 서울특별시 및 자치구별 연령/성별 인구 데이터")


# 1. 데이터 로드 (EUC-KR 인코딩 & 천 단위 쉼표 자동 처리)
@st.cache_data
def load_data():
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

# 2. 사이드바 - 조건 선택
st.sidebar.header("⚙️ 데이터 조회 및 분석 조건")

# 분석 유형 선택
analysis_type = st.sidebar.radio(
    "분석 유형 선택",
    ["1. 특정 행정구 연령별 꺾은선 그래프", "2. 특정 연령대 최고 인구 구별 막대 그래프"],
)

selected_year = st.sidebar.selectbox("연도 선택", ["2025년"])
gender_option = st.sidebar.selectbox("성별 선택", ["전체", "남성", "여성"])

# 성별 매핑 prefix
if gender_option == "전체":
    prefix = f"{selected_year}_거주자_"
elif gender_option == "남성":
    prefix = f"{selected_year}_남_거주자_"
else:
    prefix = f"{selected_year}_여_거주자_"

# --- 기능 1: 행정구 선택 -> 연령별 꺾은선 그래프 ---
if analysis_type == "1. 특정 행정구 연령별 꺾은선 그래프":
    district_list = df["행정구"].tolist()
    selected_district = st.sidebar.selectbox(
        "행정구 선택", district_list, index=1 if len(district_list) > 1 else 0
    )

    target_row = df[df["행정구"] == selected_district].iloc[0]
    population_values = [target_row[f"{prefix}{age}"] for age in age_categories]

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=age_categories,
            y=population_values,
            mode="lines+markers",
            name=f"{selected_district} ({gender_option})",
            line=dict(color="#90EE90", width=3),  # 연한 초록색
            marker=dict(size=8, color="#2E8B57"),
            hovertemplate="연령대: %{x}<br>인구수: %{y:,.0f}명<extra></extra>",
        )
    )

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
            dtick=1,  # 10살 단위 구분선
        ),
        yaxis=dict(
            title="인구수 (명)",
            showgrid=True,
            gridcolor="#E5E5E5",
            gridwidth=1,
            dtick=10000,  # 1만 단위 구분선
            tickformat=",.0f",
        ),
        hovermode="x unified",
        plot_bgcolor="white",
        height=550,
    )
    st.plotly_chart(fig, use_container_width=True)

    with st.expander("📊 상세 데이터 확인하기"):
        data_df = pd.DataFrame(
            {"연령대": age_categories, "인구수(명)": population_values}
        )
        st.dataframe(data_df.T, use_container_width=True)

# --- 기능 2: 연령대 선택 -> 인구수 많은 구 막대 그래프 ---
else:
    selected_age = st.sidebar.selectbox(
        "10살 단위 연령대 선택", age_categories, index=2  # 기본값: 20~29세
    )

    # 서울특별시 전체를 제외한 각 자치구 데이터만 추출
    df_districts = df[df["행정구"] != "서울특별시 전체"].copy()
    target_col = f"{prefix}{selected_age}"

    # 인구수가 많은 순서로 정렬
    df_sorted = df_districts.sort_values(
        by=target_col, ascending=False
    ).reset_index(drop=True)

    # 막대 그래프 생성 (연한 초록색 적용)
    fig_bar = px.bar(
        df_sorted,
        x="행정구",
        y=target_col,
        title=f"<b>[{selected_year}] {selected_age} ({gender_option}) 인구가 가장 많은 행정구 순위</b>",
        labels={"행정구": "행정구역", target_col: "인구수 (명)"},
        text_auto=",.0f",
    )

    fig_bar.update_traces(
        marker_color="#90EE90",
        marker_line_color="#2E8B57",
        marker_line_width=1.5,
        textposition="outside",
    )

    fig_bar.update_layout(
        xaxis=dict(title="행정구", tickangle=-45),
        yaxis=dict(
            title="인구수 (명)",
            showgrid=True,
            gridcolor="#E5E5E5",
            gridwidth=1,
            dtick=10000,  # 1만 단위 구분선
            tickformat=",.0f",
        ),
        plot_bgcolor="white",
        height=550,
    )

    st.plotly_chart(fig_bar, use_container_width=True)

    # 상위 TOP 3 지표 카드 표시
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(
            "🥇 1위",
            f"{df_sorted.iloc[0]['행정구']}",
            f"{df_sorted.iloc[0][target_col]:,} 명",
        )
    with col2:
        st.metric(
            "🥈 2위",
            f"{df_sorted.iloc[1]['행정구']}",
            f"{df_sorted.iloc[1][target_col]:,} 명",
        )
    with col3:
        st.metric(
            "🥉 3위",
            f"{df_sorted.iloc[2]['행정구']}",
            f"{df_sorted.iloc[2][target_col]:,} 명",
        )

    with st.expander("📊 순위별 전체 데이터 보기"):
        st.dataframe(
            df_sorted[["행정구", target_col]].rename(
                columns={target_col: "인구수(명)"}
            ),
            use_container_width=True,
        )
