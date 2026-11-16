import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import streamlit as st

# 페이지 설정
st.set_page_config(
    page_title="Iris 품종 예측 앱", page_icon="🌸", layout="centered"
)

st.title("🌸 붓꽃(Iris) 품종 예측 서비스")
st.markdown(
    "꽃잎의 길이와 너비를 입력하면 **랜덤 포레스트(Random Forest)** 모델이 품종을 예측해 드립니다."
)


@st.cache_resource
def load_data_and_model():
  # 데이터 로드 (cp949 또는 utf-8 인코딩 대응)
  try:
    df = pd.read_csv("Iris.csv", encoding="cp949")
  except:
    df = pd.read_csv("Iris.csv", encoding="utf-8")

  # 모델 학습용 데이터 준비 (꽃잎 길이, 꽃잎 너비 2개 특성만 사용)
  X = df[["꽃잎 길이", "꽃잎 너비"]]
  y = df["품종"]

  model = RandomForestClassifier(random_state=42)
  model.fit(X, y)

  return df, model


df, model = load_data_and_model()

st.divider()

# 사이드바 또는 메인 입력창 설정
st.subheader("🎛️ 꽃잎 제원 입력")
col1, col2 = st.columns(2)

with col1:
  petal_length = st.slider(
      "꽃잎 길이 (cm)",
      min_value=float(df["꽃잎 길이"].min()),
      max_value=float(df["꽃잎 길이"].max()),
      value=4.0,
      step=0.1,
  )

with col2:
  petal_width = st.slider(
      "꽃잎 너비 (cm)",
      min_value=float(df["꽃잎 너비"].min()),
      max_value=float(df["꽃잎 너비"].max()),
      value=1.3,
      step=0.1,
  )

# 예측 수행
input_data = pd.DataFrame(
    [[petal_length, petal_width]], columns=["꽃잎 길이", "꽃잎 너비"]
)
prediction = model.predict(input_data)[0]
prediction_proba = model.predict_proba(input_data)

st.divider()

# 결과 출력
st.subheader("🔍 예측 결과")
st.success(f"입력하신 조건의 예측 품종은 **[{prediction}]** 입니다!")

# 확률 바 차트
proba_df = pd.DataFrame(
    prediction_proba, columns=model.classes_, index=["확률"]
).T
st.bar_chart(proba_df)

st.divider()

# 시각화 (가로축: 꽃잎 길이, 세로축: 꽃잎 너비, 사용자는 연보라별 ★)
st.subheader("📊 데이터 분포 및 사용자 위치")

fig, ax = plt.subplots(figsize=(8, 6))

# 품종별 색상 지정
colors = {
    "Iris-setosa": "#1f77b4",
    "Iris-versicolor": "#ff7f0e",
    "Iris-virginica": "#2ca02c",
}

for species, group in df.groupby("품종"):
  ax.scatter(
      group["꽃잎 길이"],
      group["꽃잎 너비"],
      label=species,
      color=colors.get(species, "gray"),
      alpha=0.7,
      edgecolors="w",
      s=60,
  )

# 사용자가 입력한 위치를 연보라색 별표로 표시
ax.scatter(
    petal_length,
    petal_width,
    color="#9370DB",
    marker="*",
    s=300,
    label="사용자 입력",
    edgecolors="black",
    zorder=5,
)

ax.set_xlabel("Petal Length (꽃잎 길이, cm)", fontsize=12)
ax.set_ylabel("Petal Width (꽃잎 너비, cm)", fontsize=12)
ax.set_title("Iris Petal Length vs Width & User Input", fontsize=14)
ax.legend(loc="upper left")
ax.grid(True, linestyle="--", alpha=0.5)

st.pyplot(fig)
