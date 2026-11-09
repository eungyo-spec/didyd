import pandas as pd
import plotly.graph_objects as go
import streamlit as st

# 페이지 설정
st.set_page_config(
    page_title="월별 기온 분석 대시보드", page_icon="🌡️", layout="wide"
)

st.title("🌡️ 월별 기온 분석 대시보드")


# 데이터 로드 및 전처리 (캐싱 적용)
@st.cache_data
def load_data(file_path):
    try:
        df = pd.read_csv(file_path, encoding="utf-8")
    except UnicodeDecodeError:
        df = pd.read_csv(file_path, encoding="cp949")

    # '일시' 컬럼을 datetime 형식으로 변환 (예: Oct-07 -> 2007-10-01)
    df["날짜"] = pd.to_datetime(df["일시"], format="%b-%y")
    df["연도"] = df["날짜"].dt.year
    df["월"] = df["날짜"].dt.month
    return df


# CSV 데이터 파일 불러오기
try:
    df = load_data("temperature.csv")
except Exception as e:
    st.error(
        f"데이터 파일을 불러올 수 없습니다. 'temperature.csv' 파일이 같은 디렉토리에 있는지 확인해 주세요. (오류: {e})"
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

# 꺾은선 그래프 생성 (Plotly go.Figure 사용)
fig = go.Figure()

# 1. 최고기온 (찐한 빨강)
fig.add_trace(
    go.Scatter(
        x=filtered_df["연도"],
        y=filtered_df["최고기온(℃)"],
        mode="lines+markers",
        name="최고기온",
        line=dict(color="#B22222", width=3),  # 찐한 빨강 (Firebrick)
        marker=dict(size=6),
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
        marker=dict(size=6),
    )
)

# 그래프 레이아웃 설정 (제목, 축 이름, 범례)
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
        dtick=5,  # 5년 단위 주축 표시
    ),
    yaxis=dict(
        title="온도 (℃)",
        showgrid=True,
    ),
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

# 스트림릿 화면에 차트 출력
st.plotly_chart(fig, use_container_width=True)

# 데이터 테이블 표시 옵션
with st.expander(f"📋 {selected_month}월 상세 데이터 보기"):
    st.dataframe(
        filtered_df[["연도", "일시", "최고기온(℃)", "최저기온(℃)", "평균기온(℃)"]],
        use_container_width=True,
    )
