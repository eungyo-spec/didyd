import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.ensemble import RandomForestRegressor
import os

# 1. 페이지 기본 설정
st.set_page_config(page_title="월별 기온 변화 및 다중 회귀 모델 예측", page_icon="🌡️", layout="wide")

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

# 3. 데이터 로드 및 전처리 (pages 폴더 기준 상위 폴더의 temperature.csv 경로 반영)
@st.cache_data
def load_data():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, "..", "temperature.csv")
    
    try:
        df = pd.read_csv(file_path, encoding="cp949")
    except UnicodeDecodeError:
        df = pd.read_csv(file_path, encoding="utf-8")

    month_map = {
        "Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "May": 5, "Jun": 6,
        "Jul": 7, "Aug": 8, "Sep": 9, "Oct": 10, "Nov": 11, "Dec": 12
    }
    split_date = df["일시"].str.split("-")
    df["Month_Eng"] = split_date.str[0]
    df["Month"] = df["Month_Eng"].map(month_map)
    yy = split_date.str[1].astype(int)

    years = []
    century = 1900
    prev_y = -1
    for y in yy:
        if prev_y == 99 and y == 0:
            century = 2000
        years.append(century + y)
        prev_y = y

    df["Year"] = years
    df = df.dropna(subset=["평균기온(℃)", "Month", "Year"]).copy()
    return df

df = load_data()

# 4. 사이드바: 사용자 입력 (월, 예측 연도, 회귀 알고리즘 선택)
st.title("🌡️ 월별 평균기온 분석 및 다중 회귀 모델 예측")
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

# 회귀 알고리즘 선택selectbox 추가
model_type = st.sidebar.selectbox(
    "회귀 알고리즘을 선택하세요",
    options=["선형회귀 (Linear Regression)", "랜덤 포레스트 (Random Forest)", "릿지 회귀 (Ridge Regression)"],
    index=0
)

# 5. 데이터 필터링 및 선택된 모델 학습
month_df = df[df["Month"] == selected_month].sort_values("Year")

X = month_df[["Year"]].values
y = month_df["평균기온(℃)"].values

# 모델 객체 생성 및 학습
if model_type == "선형회귀 (Linear Regression)":
    model = LinearRegression()
    model.fit(X, y)
    pred_temp = model.predict([[target_year]])[0]
    y_fitted = model.predict(X)
    
    # 시각화용 트렌드 라인
    x_hist_line = np.linspace(X.min(), X.max(), 100).reshape(-1, 1)
    y_hist_line = model.predict(x_hist_line)
    x_future_line = np.linspace(X.max(), target_year, 50).reshape(-1, 1)
    y_future_line = model.predict(x_future_line)
    
    slope = model.coef_[0]
    intercept = model.intercept_

elif model_type == "랜덤 포레스트 (Random Forest)":
    # random_state 고정으로 결과 재현성 확보
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X, y)
    pred_temp = model.predict([[target_year]])[0]
    y_fitted = model.predict(X)
    
    x_hist_line = np.linspace(X.min(), X.max(), 100).reshape(-1, 1)
    y_hist_line = model.predict(x_hist_line)
    x_future_line = np.linspace(X.max(), target_year, 50).reshape(-1, 1)
    y_future_line = model.predict(x_future_line)

else:  # 릿지 회귀 (Ridge Regression)
    model = Ridge(alpha=1.0)
    model.fit(X, y)
    pred_temp = model.predict([[target_year]])[0]
    y_fitted = model.predict(X)
    
    x_hist_line = np.linspace(X.min(), X.max(), 100).reshape(-1, 1)
    y_hist_line = model.predict(x_hist_line)
    x_future_line = np.linspace(X.max(), target_year, 50).reshape(-1, 1)
    y_future_line = model.predict(x_future_line)
    
    slope = model.coef_[0]
    intercept = model.intercept_

# 핵심 요약 지표 표시
col1, col2, col3 = st.columns(3)
col1.metric(f"{target_year}년 {selected_month}월 예측 평균기온", f"{pred_temp:.2f} ℃")
col2.metric("과거 데이터 평균기온", f"{y.mean():.2f} ℃", f"{pred_temp - y.mean():+.2f} ℃ (과거 평균 대비)")
if model_type != "랜덤 포레스트 (Random Forest)":
    col3.metric("연평균 기온 상승률 (기울기)", f"{slope:+.4f} ℃/년", f"10년당 {slope*10:+.2f} ℃")
else:
    col3.metric("모델 유형", "앙상블 비선형", "Decision Tree 100개")

# 6. 알고리즘 작동 원리가 보이는 시각화 그래프
fig, ax = plt.subplots(figsize=(12, 6))

# (1) 과거 실제 기온 관측치
ax.plot(month_df["Year"], y, color="#95a5a6", alpha=0.45, linewidth=1)
ax.scatter(month_df["Year"], y, color="#3498db", alpha=0.75, s=35, label=f"과거 {selected_month}월 실제 평균기온")

# (2) 오차(잔차) 시각화
for idx in range(len(X)):
    label_residual = "오차(잔차): 실제값과 모델 추정치 거리" if idx == 0 else None
    ax.plot(
        [X[idx][0], X[idx][0]], [y[idx], y_fitted[idx]],
        color="#e67e22", linestyle=":", linewidth=0.9, alpha=0.6, label=label_residual
    )

# (3) 모델 추세선
line_color = "#e74c3c" if "Linear" in model_type or "Ridge" in model_type else "#8e44ad"
line_label = f"모델 학습 추세선 ({model_type.split(' ')[0]})"
ax.plot(x_hist_line, y_hist_line, color=line_color, linewidth=2.5, label=line_label)

# (4) 미래 예측 연장선
ax.plot(x_future_line, y_future_line, color=line_color, linestyle="--", linewidth=2.2, label="미래 예측 연장선")

# (5) 목표 연도 예측 지점 강조
ax.scatter([target_year], [pred_temp], color="#d63031", s=160, zorder=6, edgecolors="black", linewidth=1.5,
           label=f"{target_year}년 예측 기온: {pred_temp:.2f}℃")
ax.axvline(x=target_year, color="#d63031", linestyle=":", alpha=0.5)
ax.axhline(y=pred_temp, color="#d63031", linestyle=":", alpha=0.5)

ax.annotate(
    f"📍 {target_year}년 {selected_month}월 예측\n     {pred_temp:.2f} ℃",
    xy=(target_year, pred_temp),
    xytext=(-110, 22),
    textcoords="offset points",
    fontsize=11,
    fontweight="bold",
    color="#b30000",
    bbox=dict(boxstyle="round,pad=0.4", facecolor="#fff5f5", edgecolor=line_color, lw=1.5),
    arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=.2", color=line_color, lw=1.5)
)

ax.set_title(f"[{selected_month}월] 역대 평균기온 추이 및 {target_year}년 {model_type} 기온 예측", fontsize=15, fontweight="bold", pad=15)
ax.set_xlabel("연도 (Year)", fontsize=12)
ax.set_ylabel("평균기온 (℃)", fontsize=12)
ax.grid(True, linestyle="--", alpha=0.35)
ax.legend(loc="upper left", fontsize=9.5, framealpha=0.9)

plt.tight_layout()
st.pyplot(fig)

# 7. 그래프 하단: 선택된 알고리즘 작동 원리 설명
st.markdown("---")
st.subheader(f"📘 선택한 '{model_type}' 알고리즘은 어떻게 작동할까?")

if "Linear" in model_type:
    st.markdown(f"""
    **선형회귀 (Linear Regression)** 작동 원리:
    1. **최소제곱법 (주황색 세로 점선):** 각 연도별 실제 기온(파란색 점)과 직선(추세선) 사이의 **오차(잔차)의 제곱 합을 최소화**하는 최적의 단일 직선 방정식을 찾습니다.
    2. **방정식 도출:** $y = {slope:.4f}x + ({intercept:.2f})$ 형태로 표현되며, 연간 기온 변화 추세($slope$)를 가장 직관적으로 보여줍니다.
    3. **미래 예측:** 연도 $x = {target_year}$를 대입하여 미래 기온(${pred_temp:.2f}℃$)을 산출합니다.
    """)
elif "Random Forest" in model_type:
    st.markdown(f"""
    **랜덤 포레스트 회귀 (Random Forest Regressor)** 작동 원리:
    1. **앙상블(Ensemble)과 다수의 나무:** 데이터에서 무작위로 샘플링을 여러 번 진행하여 **100개의 독립된 의사결정 나무(Decision Tree)**를 생성합니다.
    2. **비선형 패턴 학습:** 단순한 일직선이 아니라, 데이터 구간별로 분기점을 나누어 기온의 미세한 굴곡과 비선형적 변화 패턴을 유연하게 학습합니다.
    3. **최종 예측:** 100개의 나무가 각각 예측한 값들을 모아 **평균(Average)**을 내어 최종 예측값(${pred_temp:.2f}℃$)을 결정합니다. 이상치나 급격한 변동에 강한 장점이 있습니다.
    """)
else:
    st.markdown(f"""
    **릿지 회귀 (Ridge Regression)** 작동 원리:
    1. **L2 규제(Regularization) 추가:** 기본 선형회귀와 유사하게 직선을 찾지만, 계수(기울기)가 너무 커지지 않도록 **페널티(규제 항)**를 부여합니다.
    2. **과적합 방지 및 안정성:** 기온 데이터에 연도별 이상치나 불규칙한 노이즈가 많을 때, 모델이 지나치게 요동치는 것을 막고 **안정적이고 일반화된 추세선**을 유지하도록 도와줍니다.
    3. **미래 예측:** 규제가 적용된 최적의 회귀선 방정식에 $x = {target_year}$를 대입하여 ${pred_temp:.2f}℃$를 예측합니다.
    """)
