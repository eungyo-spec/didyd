import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
import streamlit as st

# 페이지 설정
st.set_page_config(
    page_title="Iris 다중 모델 품종 예측 앱", page_icon="🌸", layout="centered"
)

st.title("🌸 붓꽃(Iris) 품종 예측 및 비교 분석 서비스")
st.markdown(
    "특성 조합과 머신러닝 알고리즘을 선택하여 품종 예측 결과를 비교해 보세요."
)


@st.cache_resource
def load_data():
  try:
    df = pd.read_csv("Iris.csv", encoding="cp949")
  except:
    df = pd.read_csv("Iris.csv", encoding="utf-8")
  return df


df = load_data()

st.sidebar.header("⚙️ 모델 설정")

# 알고리즘 선택
algorithm_name = st.sidebar.selectbox(
    "분류 알고리즘 선택",
    ["Random Forest", "Support Vector Machine (SVM)", "K-Nearest Neighbors (KNN)"],
)

# 알고리즘별 작동 원리 설명 딕셔너리
algorithm_descriptions = {
    "Random Forest": (
        "**랜덤 포레스트 (Random Forest) 작동 원리**:\n"
        "수많은 의사결정 나무(Decision Tree)를 숲처럼 여러 개 만들어, 각 나무가 내린 예측 결과를 "
        "다수결(Ensemble) 방식으로 종합하여 최종 품종을 결정하는 앙상블 알고리즘입니다. "
        "과적합을 방지하고 일반화 성능이 매우 뛰어납니다."
    ),
    "Support Vector Machine (SVM)": (
        "**서포트 벡터 머신 (SVM) 작동 원리**:\n"
        "데이터들이 속한 공간에서 각 품종 간의 경계(초평면, Hyperplane)를 정의하여, "
        "데이터들과의 거리(마진)가 최대가 되는 최적의 경계선을 찾아 분류를 수행하는 알고리즘입니다. "
        "선형 및 비선형 경계 구분에 모두 강력합니다."
    ),
    "K-Nearest Neighbors (KNN)": (
        "**K-최근접 이웃 (KNN) 작동 원리**:\n"
        "새로운 데이터가 들어왔을 때, 공간상에서 가장 가까운 거리에 있는 K개의 기존 데이터를 찾고, "
        "그중 다수의 데이터가 속한 품종으로 분류하는 비모수적·직관적인 알고리즘입니다."
    ),
}


def get_trained_model(algo_choice, X, y):
  if algo_choice == "Random Forest":
    model = RandomForestClassifier(random_state=42)
  elif algo_choice == "Support Vector Machine (SVM)":
    model = SVC(probability=True, random_state=42)
  else:
    model = KNeighborsClassifier(n_neighbors=5)

  model.fit(X, y)
  return model


# 탭 생성 (탭1: 꽃잎 특성, 탭2: 꽃받침 특성)
tab1, tab2 = st.tabs(
    ["🌿 꽃잎 특성 (Petal Length & Width)", "🌱 꽃받침 특성 (Sepal Length & Width)"]
)

# 품종별 색상 지정
colors = {
    "Iris-setosa": "#1f77b4",
    "Iris-versicolor": "#ff7f0e",
    "Iris-virginica": "#2ca02c",
}

# --- [Tab 1] 꽃잎 길이 & 꽃잎 너비 ---
with tab1:
  st.subheader("🌿 꽃잎(Petal) 제원을 이용한 예측")

  X1 = df[["꽃잎 길이", "꽃잎 너비"]]
  y1 = df["품종"]
  model1 = get_trained_model(algorithm_name, X1, y1)

  col1, col2 = st.columns(2)
  with col1:
    p_len = st.slider(
        "꽃잎 길이 (cm)",
        float(X1["꽃잎 길이"].min()),
        float(X1["꽃잎 길이"].max()),
        4.0,
        0.1,
        key="p_len",
    )
  with col2:
    p_wid = st.slider(
        "꽃잎 너비 (cm)",
        float(X1["꽃잎 너비"].min()),
        float(X1["꽃잎 너비"].max()),
        1.3,
        0.1,
        key="p_wid",
    )

  input_data1 = pd.DataFrame([[p_len, p_wid]], columns=["꽃잎 길이", "꽃잎 너비"])
  pred1 = model1.predict(input_data1)[0]

  st.success(f"**[{algorithm_name}]** 예측 품종: **{pred1}**")

  # 시각화
  fig1, ax1 = plt.subplots(figsize=(7, 5))
  for species, group in df.groupby("품종"):
    ax1.scatter(
        group["꽃잎 길이"],
        group["꽃잎 너비"],
        label=species,
        color=colors.get(species),
        alpha=0.7,
        edgecolors="w",
        s=60,
    )
  ax1.scatter(
      p_len,
      p_wid,
      color="#9370DB",
      marker="*",
      s=300,
      label="사용자 입력",
      edgecolors="black",
      zorder=5,
  )
  ax1.set_xlabel("Petal Length (cm)")
  ax1.set_ylabel("Petal Width (cm)")
  ax1.set_title("Petal Length vs Width")
  ax1.legend(loc="upper left")
  ax1.grid(True, linestyle="--", alpha=0.5)
  st.pyplot(fig1)

  # 알고리즘 작동 원리 출력
  st.info(algorithm_descriptions[algorithm_name])

# --- [Tab 2] 꽃받침 길이 & 꽃받침 너비 ---
with tab2:
  st.subheader("🌱 꽃받침(Sepal) 제원을 이용한 예측")
  st.markdown(
      "*(추천 이유: 꽃받침 특성은 품종 간 일부 겹치는 구간이 존재하여, 선택한 알고리즘이 공간을 어떻게 분할하고 판별하는지 비교하기 좋습니다.)*"
  )

  X2 = df[["꽃받침 길이", "꽃받침 너비"]]
  y2 = df["품종"]
  model2 = get_trained_model(algorithm_name, X2, y2)

  col3, col4 = st.columns(2)
  with col3:
    s_len = st.slider(
        "꽃받침 길이 (cm)",
        float(X2["꽃받침 길이"].min()),
        float(X2["꽃받침 길이"].max()),
        5.8,
        0.1,
        key="s_len",
    )
  with col4:
    s_wid = st.slider(
        "꽃받침 너비 (cm)",
        float(X2["꽃받침 너비"].min()),
        float(X2["꽃받침 너비"].max()),
        3.0,
        0.1,
        key="s_wid",
    )

  input_data2 = pd.DataFrame(
      [[s_len, s_wid]], columns=["꽃받침 길이", "꽃받침 너비"]
  )
  pred2 = model2.predict(input_data2)[0]

  st.success(f"**[{algorithm_name}]** 예측 품종: **{pred2}**")

  # 시각화
  fig2, ax2 = plt.subplots(figsize=(7, 5))
  for species, group in df.groupby("품종"):
    ax2.scatter(
        group["꽃받침 길이"],
        group["꽃받침 너비"],
        label=species,
        color=colors.get(species),
        alpha=0.7,
        edgecolors="w",
        s=60,
    )
  ax2.scatter(
      s_len,
      s_wid,
      color="#9370DB",
      marker="*",
      s=300,
      label="사용자 입력",
      edgecolors="black",
      zorder=5,
  )
  ax2.set_xlabel("Sepal Length (cm)")
  ax2.set_ylabel("Sepal Width (cm)")
  ax2.set_title("Sepal Length vs Width")
  ax2.legend(loc="upper left")
  ax2.grid(True, linestyle="--", alpha=0.5)
  st.pyplot(fig2)

  # 알고리즘 작동 원리 출력
  st.info(algorithm_descriptions[algorithm_name])
