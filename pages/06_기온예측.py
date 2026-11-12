import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from sklearn.linear_model import LinearRegression
import os

# 1. 페이지 기본 설정
st.set_page_config(page_title="기온 변화 추이 및 선형회귀 예측", page_icon="🌡️", layout="wide")

# 2. Streamlit Cloud 환경에서 한글 폰트 설정 (NanumGothic)
def set_korean_font():
    font_path = "/usr/share/fonts/truetype/nanum/NanumGothic.ttf"
    if os.path.exists(font_path):
        fm.fontManager.addfont(font_path)
        plt.rcParams["font.family"] = "NanumGothic"
    else:
        # 로컬 환경(Windows/Mac) 대비 fallback
        plt.rcParams["font.sans-serif"] = ["Malgun Gothic", "AppleGothic", "NanumGothic", "DejaVu Sans"]
    plt.rcParams["axes.unicode_minus"] = False

set_korean_font()

# 3. 데이터 로드 및 전처리 (1907년 ~ 2026년 연도 변환 포함)
@st.cache_data
def load_data(file_path="temperature.csv"):
    try:
        df = pd.read_csv(file_path, encoding="cp949")
    except UnicodeDecodeError:
        df = pd.read_csv(file_path, encoding="utf-8")

    # '일시' 컬럼(예: 'Oct-07', 'Jan-00')에서 월과 연도 추출
    month_map = {
        "Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "May": 5, "Jun": 6,
        "Jul": 7, "Aug": 8, "Sep": 9, "Oct": 10, "Nov": 11, "Dec": 12
    }
    split_date = df["일시"].str.split("-")
    df["Month_Eng"] = split_date.str[0]
    df["Month"] = df["Month_Eng"].map(month_map)
    yy = split_date.str[1].astype(int)

    # 99 -> 00 으로 넘어갈 때 1900년대에서 2000년대로 전환
    years = []
    century = 1900
    prev_y = -1
    for y in yy:
        if prev_y == 99 and y == 0:
            century = 2000
        years.append(century + y)
        prev_y = y

    df["Year"] = years
    # 결측치(한국전쟁 시기 등) 제거
    df = df.dropna(subset=["평균기온(℃)", "Month", "Year"]).copy()
    return df

df = load_data()

# 4. 사이드바: 사용자 입력 (월 & 예측 연도)
st.title("🌡️ 월별 평균기온 분석 및 선형회귀 예측")
st.sidebar.header("🔍 예측 조건 설정")

selected_month = st.sidebar.selectbox(
    "예측할 월(Month)을 선택하세요",
    options=list(range(1, 13)),
    index=7,  # 기본값: 8월
    format_func=lambda x: f"{x}월"
)

max_data_year = int(df["Year"].max())
target_year = st.sidebar.number_input(
    "예측할 연도(Year)를 입력하세요",
    min_value=max_data_year + 1,
    max_value=2150,
    value=2030,
    step=1
)

# 5. 선택한 월 데이터 필터링 및 선형회귀 모델 학습
month_df = df[df["Month"] == selected_month].sort_values("Year")

X = month_df[["Year"]].values
y = month_df["평균기온(℃)"].values

model = LinearRegression()
model.fit(X, y)

slope = model.coef_[0]          # 기울기 (연간 기온 변화율)
intercept = model.intercept_    # y절편
pred_temp = model.predict([[target_year]])[0]

# 추세선 및 연장선 좌표 생성
x_hist_line = np.linspace(X.min(), X.max(), 100).reshape(-1, 1)
y_hist_line = model.predict(x_hist_line)

x_future_line = np.linspace(X.max(), target_year, 50).reshape(-1, 1)
y_future_line = model.predict(x_future_line)

# 핵심 요약 지표 표시
col1, col2, col3 = st.columns(3)
col1.metric(f"{target_year}년 {selected_month}월 예측 평균기온", f"{pred_temp:.2f} ℃")
col2.metric("과거 데이터 평균기온", f"{y.mean():.2f} ℃", f"{pred_temp - y.mean():+.2f} ℃ (과거 평균 대비)")
col3.metric("연평균 기온 상승률 (기울기)", f"{slope:+.4f} ℃/년", f"10년당 {slope*10:+.2f} ℃")

# 6. 선형회귀 작동 원리가 한눈에 보이는 시각화 그래프
fig, ax = plt.subplots(figsize=(12, 6))

# (1) 과거 실제 기온 관측치 (산점도 + 연도별 연결선)
ax.plot(month_df["Year"], y, color="#95a5a6", alpha=0.45, linewidth=1)
ax.scatter(month_df["Year"], y, color="#3498db", alpha=0.75, s=35, label=f"과거 {selected_month}월 실제 평균기온 ({int(X.min())}~{int(X.max())}년)")

# (2) 데이터와 회귀선 사이의 오차(잔차, Residual) 시각화 — 선형회귀의 핵심 원리!
y_fitted = model.predict(X)
for idx in range(len(X)):
    label_residual = "오차(잔차): 실제값과 추세선의 거리" if idx == 0 else None
    ax.plot(
        [X[idx][0], X[idx][0]], [y[idx], y_fitted[idx]],
        color="#e67e22", linestyle=":", linewidth=0.9, alpha=0.6, label=label_residual
    )

# (3) 선형회귀 학습 추세선 (과거 구간)
ax.plot(
    x_hist_line, y_hist_line, color="#e74c3c", linewidth=2.5,
    label=f"선형회귀 추세선: y = {slope:.4f}x + ({intercept:.2f})"
)

# (4) 미래 예측 연장선 (점선)
ax.plot(
    x_future_line, y_future_line, color="#e74c3c", linestyle="--", linewidth=2.2,
    label="미래 예측 연장선 (외삽)"
)

# (5) 목표 연도 예측 지점 강조 및 수직/수평 보조선
ax.scatter([target_year], [pred_temp], color="#d63031", s=160, zorder=6, edgecolors="black", linewidth=1.5,
           label=f"{target_year}년 예측 기온: {pred_temp:.2f}℃")
ax.axvline(x=target_year, color="#d63031", linestyle=":", alpha=0.5)
ax.axhline(y=pred_temp, color="#d63031", linestyle=":", alpha=0.5)

# 예측 값 텍스트 말풍선 표시
ax.annotate(
    f"📍 {target_year}년 {selected_month}월 예측\n     {pred_temp:.2f} ℃",
    xy=(target_year, pred_temp),
    xytext=(-110, 22 if slope >= 0 else -40),
    textcoords="offset points",
    fontsize=11,
    fontweight="bold",
    color="#b30000",
    bbox=dict(boxstyle="round,pad=0.4", facecolor="#fff5f5", edgecolor="#e74c3c", lw=1.5),
    arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=.2", color="#e74c3c", lw=1.5)
)

ax.set_title(f"[{selected_month}월] 역대 평균기온 추이 및 {target_year}년 선형회귀 기온 예측", fontsize=15, fontweight="bold", pad=15)
ax.set_xlabel("연도 (Year)", fontsize=12)
ax.set_ylabel("평균기온 (℃)", fontsize=12)
ax.grid(True, linestyle="--", alpha=0.35)
ax.legend(loc="upper left", fontsize=9.5, framealpha=0.9)

plt.tight_layout()
st.pyplot(fig)

# 7. 그래프 하단: 선형회귀 알고리즘 작동 원리 설명
st.markdown("---")
st.subheader("📘 그래프 속 선형회귀(Linear Regression) 알고리즘은 어떻게 작동할까?")

st.markdown(f"""
선형회귀는 과거 데이터(연도 $x$와 평균기온 $y$)의 흐름을 가장 잘 관통하는 **하나의 직선(추세선)**을 찾아 미래 값을 예측하는 머신러닝 알고리즘입니다. 위 그래프는 그 작동 과정을 4단계로 보여줍니다.

1. **데이터 분포 확인 (파란색 점):**  
   `temperature.csv`에서 **{selected_month}월** 데이터만 추출하여, 가로축(연도)과 세로축(평균기온) 좌표에 찍습니다.
2. **오차(잔차) 최소화 원리 — 최소제곱법 (주황색 세로 점선):**  
   어떤 직선이 데이터를 가장 잘 대표할까요? 선형회귀는 각 파란색 점(실제 기온)과 빨간색 직선(예측 기온) 사이의 **수직 거리(오차, Residual)의 제곱 합이 최소가 되는 단 하나의 직선**을 수학적으로 계산해 찾습니다.
3. **1차 방정식 도출 (빨간색 실선):**  
   찾아낸 최적의 직선은 중학교 수학에서 배운 직선의 방정식 형태를 가집니다.
   $$y = {slope:.4f}x + ({intercept:.2f})$$
   * **기울기 ($w = {slope:+.4f}$):** 매년 {selected_month}월 평균기온이 평균적으로 **{slope:+.4f}℃**씩 변하고 있음을 뜻합니다. (10년 기준 약 **{slope*10:+.2f}℃** 변화)
   * **절편 ($b = {intercept:.2f}$):** 직선의 기준 위치를 결정하는 상수입니다.
4. **미래 연도 대입 및 예측 (빨간색 점선 및 별표 지점):**  
   학습된 직선을 미래로 그대로 연장(빨간색 점선)한 뒤, 사용자가 입력한 **$x = {target_year}$**을 방정식에 대입하여 예측 기온 **$y = {pred_temp:.2f}\text{{℃}}$**를 산출합니다.
""")
