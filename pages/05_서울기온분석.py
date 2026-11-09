import os
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

# 페이지 기본 설정
st.set_page_config(
    page_title="서울 기온 종합 분석 대시보드", page_icon="🌡️", layout="wide"
)

st.title("🌡️ 서울 기온 종합 분석 대시보드")


# 데이터 로드 및 1907년 연도 보정 전처리 함수
@st.cache_data
def load_data():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)

    file_path_parent = os.path.join(parent_dir, "temperature.csv")
    file_path_current = os.path.join(current_dir, "temperature.csv")

    if os.path.exists(file_path_parent):
        target_path = file_path_parent
    elif os.path.exists(file_path_current):
        target_path = file_path_current
    else:
        target_path = "../temperature.csv"

    try:
        df = pd.read_csv(target_path, encoding="utf-8")
    except UnicodeDecodeError:
        df = pd.read_csv(target_path, encoding="cp949")

    # '일시' 파싱 및 1907년부터 시작되도록 연도 보정
    df["날짜"] = pd.to_datetime(df["일시"], format="%b-%y")
    df["연도"] = df["날짜"].dt.year.apply(
        lambda y: y - 100 if y >= 2007 else y
    )
    df["월"] = df["날짜"].dt.month

    return df


# 데이터 불러오기
try:
    df = load_data()
except Exception as e:
    st.error(
        f"데이터 파일을 불러올 수 없습니다. 상위 폴더에 'temperature.csv' 파일이 있는지 확인해 주세요. (오류: {e})"
    )
    st.stop()

# 사이드바 - 분석 메뉴 선택
st.sidebar.header("📊 분석 메뉴 선택")
menu = st.sidebar.radio(
    "원하는 분석 과제를 선택하세요:",
    [
        "1. 서울 월별 평균기온 (1~12월)",
        "2. 연도별 최고/최저기온 추이",
        "3. 특정 2개 연도 비교 분석",
    ],
)

# 공통 연도 목록
min_year = int(df["연도"].min())
max_year = int(df["연도"].max())

# --- [과제 1] 가로축 1월~12월, 서울의 월별 평균기온 그래프 ---
if menu == "1. 서울 월별 평균기온 (1~12월)":
    st.subheader("📈 서울 월별 평균기온 분석 (1월 ~ 12월)")
    st.markdown(
        "전체 연도를 대상으로 각 월별 평균기온의 전체 평균(또는 연도별 추이)을 보여줍니다."
    )

    # 연도 범위 필터 (사이드바)
    selected_years = st.sidebar.slider(
        "조회할 연도 범위", min_year, max_year, (min_year, max_year)
    )
    sub_df = df[
        (df["연도"] >= selected_years[0]) & (df["연도"] <= selected_years[1])
    ]

    # 월별 평균기온 계산
    monthly_avg = (
        sub_df.groupby("월")["평균기온(℃)"].mean().reset_index()
    )

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=monthly_avg["월"],
            y=monthly_avg["평균기온(℃)"],
            mode="lines+markers",
            name="월별 평균기온",
            line=dict(color="#FF8C00", width=3),  # 주황색 계열
            marker=dict(size=8),
        )
    )

    fig.update_layout(
        title=dict(
            text=f"<b>서울 월별 평균기온 ({selected_years[0]}~{selected_years[1]}년)</b>",
            font=dict(size=20),
            x=0.5,
            xanchor="center",
        ),
        xaxis=dict(
            title="월",
            tickmode="array",
            tickvals=list(range(1, 13)),
            ticktext=[f"{m}월" for m in range(1, 13)],
            showgrid=True,
        ),
        yaxis=dict(title="평균기온 (℃)", showgrid=True),
        hovermode="x unified",
        template="plotly_white",
    )

    st.plotly_chart(fig, use_container_width=True)

# --- [과제 2] 연도별 최고기온과 최저기온 그래프 ---
elif menu == "2. 연도별 최고/최저기온 추이":
    st.subheader("🌡️ 연도별 최고 및 최저기온 추이")
    st.markdown(
        "1907년부터 시작되는 연도별 최고기온(찐한 빨강)과 최저기온(찐한 파랑) 변화 추이입니다."
    )

    # 연도별 최고기온의 최댓값, 최저기온의 최솟값 집계
    yearly_temp = (
        df.groupby("연도")
        .agg({"최고기온(℃)": "max", "최저기온(℃)": "min"})
        .reset_index()
    )

    fig = go.Figure()

    # 최고기온 (찐한 빨강)
    fig.add_trace(
        go.Scatter(
            x=yearly_temp["연도"],
            y=yearly_temp["최고기온(℃)"],
            mode="lines+markers",
            name="최고기온",
            line=dict(color="#B22222", width=2.5),  # 찐한 빨강
            marker=dict(size=4),
        )
    )

    # 최저기온 (찐한 파랑)
    fig.add_trace(
        go.Scatter(
            x=yearly_temp["연도"],
            y=yearly_temp["최저기온(℃)"],
            mode="lines+markers",
            name="최저기온",
            line=dict(color="#00008B", width=2.5),  # 찐한 파랑
            marker=dict(size=4),
        )
    )

    fig.update_layout(
        title=dict(
            text="<b>연도별 최고·최저기온 분석</b>",
            font=dict(size=20),
            x=0.5,
            xanchor="center",
        ),
        xaxis=dict(title="연도", showgrid=True, dtick=10),
        yaxis=dict(title="온도 (℃)", showgrid=True),
        legend=dict(
            title="범례",
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
        ),
        hovermode="x unified",
        template="plotly_white",
    )

    st.plotly_chart(fig, use_container_width=True)

# --- [과제 3] 연도 2개를 선택하면 2개 연도의 비교 그래프 ---
elif menu == "3. 특정 2개 연도 비교 분석":
    st.subheader("⚖️ 특정 2개 연도 기온 비교 분석")
    st.markdown(
        "비교하고 싶은 두 개의 연도를 선택하여 월별 기온 변화를 나란히 비교합니다."
    )

    col_y1, col_y2 = st.sidebar.columns(2)
    with col_y1:
        year1 = st.selectbox(
            "비교 연도 1",
            options=sorted(df["연도"].unique(), reverse=True),
            index=0,
        )
    with col_y2:
        year2 = st.selectbox(
            "비교 연도 2",
            options=sorted(df["연도"].unique(), reverse=True),
            index=1 if len(df["연도"].unique()) > 1 else 0,
        )

    df_y1 = df[df["연도"] == year1].sort_values("월")
    df_y2 = df[df["연도"] == year2].sort_values("월")

    fig = go.Figure()

    # 연도 1 평균기온
    fig.add_trace(
        go.Scatter(
            x=df_y1["월"],
            y=df_y1["평균기온(℃)"],
            mode="lines+markers",
            name=f"{year1}년 평균기온",
            line=dict(width=3),
        )
    )
    # 연도 2 평균기온
    fig.add_trace(
        go.Scatter(
            x=df_y2["월"],
            y=df_y2["평균기온(℃)"],
            mode="lines+markers",
            name=f"{year2}년 평균기온",
            line=dict(width=3, dash="dash"),
        )
    )

    fig.update_layout(
        title=dict(
            text=f"<b>{year1}년 vs {year2}년 월별 평균기온 비교 분석</b>",
            font=dict(size=20),
            x=0.5,
            xanchor="center",
        ),
        xaxis=dict(
            title="월",
            tickmode="array",
            tickvals=list(range(1, 13)),
            ticktext=[f"{m}월" for m in range(1, 13)],
            showgrid=True,
        ),
        yaxis=dict(title="평균기온 (℃)", showgrid=True),
        legend=dict(
            title="범례",
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
        ),
        hovermode="x unified",
        template="plotly_white",
    )

    st.plotly_chart(fig, use_container_width=True)

    # 상세 데이터 비교표
    with st.expander("📋 연도별 상세 데이터 비교 표 보기"):
        compare_df = pd.DataFrame(
            {
                "월": [f"{m}월" for m in range(1, 13)],
                f"{year1}년 평균기온": df_y1["평균기온(℃)"].values,
                f"{year2}년 평균기온": df_y2["평균기온(℃)"].values,
            }
        )
        st.dataframe(compare_df, use_container_width=True)
