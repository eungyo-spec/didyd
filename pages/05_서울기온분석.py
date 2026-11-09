import os
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

# 페이지 기본 설정
st.set_page_config(
    page_title="서울 기온 종합 분석 대시보드", page_icon="🌡️", layout="wide"
)

st.title("🌡️ 서울 기온 종합 분석 대시보드 (1907 ~ 2026)")


# 데이터 로드 및 1907년~2026년 연도 보정 전처리 함수
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

    # '일시' 파싱 (예: Oct-07 -> 2007년, Oct-26 -> 2026년)
    df["날짜"] = pd.to_datetime(df["일시"], format="%b-%y")

    # 연도 보정: 2007년 이상으로 파싱된 데이터 중 2006년 이하 데이터는 1900년대로 매핑 (1907 ~ 2006)
    # 2007년 이후의 실제 최신 데이터(2007~2026)는 그대로 유지
    df["연도"] = df["날짜"].dt.year.apply(
        lambda y: y - 100 if (y >= 2007 and y <= 2026) else y
    )
    # 데이터셋의 실제 첫 시작(Oct-07 -> 1907년 10월)에 맞게 2000년대 초반부 정밀 보정
    df["연도"] = df["날짜"].apply(
        lambda d: (
            d.year - 100
            if (
                d.year >= 2007
                and d.year <= 2026
                and not (d.year == 2026 and d.month > 10)
            )
            else d.year
        )
    )

    # 안전하게 다시 명시적 매핑 (Oct-07부터 Oct-26까지 1907~2026 순차 반영)
    # 위 식에서 2007~2026년 데이터를 1907~2026으로 정확히 인식하도록 래핑
    def correct_year(row_date):
        y = row_date.year
        m = row_date.month
        # 데이터가 Oct-07(2007년 10월)부터 시작해 Oct-26(2026년 10월)까지 이어짐
        if 2007 <= y <= 2026:
            # 만약 2007~2016년 사이라면 1900년대로 변환 (1907~1916)
            # 단, 실제 2007~2026년 데이터를 구분하기 위해 인덱스나 순서 기반으로 처리하는 것이 안전함
            pass
        return y

    # 간결하고 확실한 연도 보정 (2000년대 초반으로 잘못 파싱된 1900년대 데이터를 -100년)
    # 원본 데이터의 구조(1907년 10월 ~ 2026년 10월)에 맞춤
    temp_years = []
    base_year = 1907
    for idx, row in df.iterrows():
        # 데이터 순서가 1907년 10월부터 1개월씩 증가하므로 순차 할당
        computed_year = 1907 + idx // 12
        computed_month = (idx % 12) + 1
        temp_years.append(computed_year)

    df["연도"] = [1907 + i // 12 for i in range(len(df))]
    df["월"] = [(i % 12) + 9 if i < 3 else (i % 12) + 1 for i in range(len(df))]
    # 위보다 안전하게 원래 날짜 기반 파싱 결과에서 오프셋 적용
    df["날짜"] = pd.to_datetime(df["일시"], format="%b-%y")

    # 정교한 연도 보정 로직
    actual_years = []
    start_y = 1907
    start_m = 10
    for i in range(len(df)):
        m = ((start_m - 1 + i) % 12) + 1
        y = start_y + (start_m - 1 + i) // 12
        actual_years.append(y)

    df["연도"] = actual_years
    df["월"] = [((10 - 1 + i) % 12) + 1 for i in range(len(df))]

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
        "2. 연도별 최고/최저기온 추이 (1907~2026)",
        "3. 특정 2개 연도 비교 분석",
    ],
)

min_year = int(df["연도"].min())
max_year = int(df["연도"].max())

# --- [과제 1] 가로축 1월~12월, 서울의 월별 평균기온 그래프 ---
if menu == "1. 서울 월별 평균기온 (1~12월)":
    st.subheader("📈 서울 월별 평균기온 분석 (1월 ~ 12월)")
    st.markdown(
        "1907년부터 2026년까지 전체 기간 동안 각 월별 평균기온의 추이를 보여줍니다."
    )

    selected_years = st.sidebar.slider(
        "조회할 연도 범위", min_year, max_year, (min_year, max_year)
    )
    sub_df = df[
        (df["연도"] >= selected_years[0]) & (df["연도"] <= selected_years[1])
    ]

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
            line=dict(color="#FF8C00", width=3),
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

# --- [과제 2] 연도별 최고기온과 최저기온 그래프 (1907~2026) ---
elif menu == "2. 연도별 최고/최저기온 추이 (1907~2026)":
    st.subheader("🌡️ 연도별 최고 및 최저기온 추이 (1907 ~ 2026)")
    st.markdown(
        "1907년부터 2026년까지의 연도별 최고기온(찐한 빨강)과 최저기온(찐한 파랑) 변화 추이입니다."
    )

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
            line=dict(color="#B22222", width=2.5),
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
            line=dict(color="#00008B", width=2.5),
            marker=dict(size=4),
        )
    )

    fig.update_layout(
        title=dict(
            text="<b>연도별 최고·최저기온 분석 (1907~2026)</b>",
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

# --- [과제 3] 특정 2개 연도 비교 분석 ---
elif menu == "3. 특정 2개 연도 비교 분석":
    st.subheader("⚖️ 특정 2개 연도 기온 비교 분석")
    st.markdown(
        "1907년~2026년 사이 비교하고 싶은 두 개의 연도를 선택하여 월별 기온 변화를 비교합니다."
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

    fig.add_trace(
        go.Scatter(
            x=df_y1["월"],
            y=df_y1["평균기온(℃)"],
            mode="lines+markers",
            name=f"{year1}년 평균기온",
            line=dict(width=3),
        )
    )
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

    with st.expander("📋 연도별 상세 데이터 비교 표 보기"):
        compare_df = pd.DataFrame(
            {
                "월": [f"{m}월" for m in range(1, 13)],
                f"{year1}년 평균기온": (
                    df_y1["평균기온(℃)"].values
                    if len(df_y1) == 12
                    else [None] * 12
                ),
                f"{year2}년 평균기온": (
                    df_y2["평균기온(℃)"].values
                    if len(df_y2) == 12
                    else [None] * 12
                ),
            }
        )
        st.dataframe(compare_df, use_container_width=True)
