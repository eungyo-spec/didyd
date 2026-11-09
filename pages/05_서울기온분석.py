import os
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

# 페이지 기본 설정
st.set_page_config(
    page_title="월별 기온 분석 대시보드", page_icon="🌡️", layout="wide"
)

st.title("🌡️ 월별 기온 분석 대시보드")


# 데이터 로드 및 1907년 연도 보정 전처리 함수
@st.cache_data
def load_data():
    # 현재 파일 기준 상위 폴더 경로 탐색
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

    # 인코딩 대응 (utf-8 실패 시 cp949)
    try:
        df = pd.read_csv(target_path, encoding="utf-8")
    except UnicodeDecodeError:
        df = pd.read_csv(target_path, encoding="cp949")

    # '일시' 컬럼 파싱 (예: Oct-07 -> 2007년으로 기본 파싱됨)
    df["날짜"] = pd.to_datetime(df["일시"], format="%b-%y")

    # 1907년부터 시작되도록 연도 보정 (2000년 이상으로 인식된 경우 100년을 빼줌)
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

# 사이드바 - 월 선택 필터
st.sidebar.header("🔍 조회 옵션")
selected_month = st.sidebar.selectbox(
    "조회할 월을 선택하세요",
    options=list(range(1, 13)),
    format_func=lambda x: f"{x}월",
    index=0,  # 기본값: 1월
)

# 선택한 월의 데이터 필터링 및 연도순 정렬
filtered_df = (
    df[df["월"] == selected_month].sort_values("연도").reset_index(drop=True)
)

# 꺾은선 그래프 생성 (Plotly go.Figure)
fig = go.Figure()

# 1. 최고기온 (찐한 빨강)
fig.add_trace(
    go.Scatter(
        x=filtered_df["연도"],
        y=filtered_df["최고기온(℃)"],
        mode="lines+markers",
        name="최고기온",
        line=dict(color="#B22222", width=3),  # 찐한 빨강 (Firebrick)
        marker=dict(size=5),
    )
)

# 2. 최저기온 (찐한 파랑)
fig.add_trace(
    go.Scatter(
        x=filtered_df["연도"],
        y=filtered_df["최저기온(℃)"],
        mode="lines+markers",
        name="최저기온",
        line=dict(color="#00008B", width=3),  # 찐한 파랑 (DarkBlue)
        marker=dict(size=5),
    )
)

# 그래프 레이아웃 설정 (제목, 축, 범례)
fig.update_layout(
    title=dict(
        text=f"<b>{selected_month}월 기온분석</b>",
        font=dict(size=22),
        x=0.5,
        xanchor="center",
    ),
    xaxis=dict(
        title="연도",
        showgrid=True,
        dtick=10,  # 10년 단위 격자 표시 (1907, 1917, 1927...)
    ),
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

# Streamlit 화면에 그래프 출력
st.plotly_chart(fig, use_container_width=True)

# 데이터 테이블 확인
with st.expander(f"📋 {selected_month}월 상세 데이터 보기"):
    st.dataframe(
        filtered_df[["연도", "일시", "최고기온(℃)", "최저기온(℃)", "평균기온(℃)"]],
        use_container_width=True,
    )
