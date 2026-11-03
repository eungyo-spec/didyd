import pandas as pd
import plotly.graph_objects as go
import streamlit as st

# 1. 페이지 설정
st.set_page_config(
    page_title="MBTI별 국가 순위 분석", page_icon="🏆", layout="wide"
)


# 2. 데이터 로드 (캐싱 적용)
@st.cache_data
def load_data():
  df = pd.read_csv("countriesMBTI_16types (1).csv")
  return df


df = load_data()
mbti_cols = [c for c in df.columns if c != "Country"]

# 메인 타이틀
st.title("🏆 MBTI별 국가 순위 및 비율 시각화")
st.markdown(
    "원하는 **MBTI 유형**을 선택하면, 해당 비율이 높은 국가부터 순서대로 막대그래프로"
    " 나타납니다. (1위: 노란색, 2위~: 초록색 그라데이션)"
)

# 3. 사이드바 - MBTI 선택
selected_mbti = st.sidebar.selectbox(
    "🔍 분석할 MBTI 유형을 선택하세요:", options=mbti_cols
)

# 4. 데이터 정렬 (선택한 MBTI 기준으로 내림차순 정렬)
rank_df = df[["Country", selected_mbti]].copy()
rank_df["Percentage"] = rank_df[selected_mbti] * 100
rank_df = rank_df.sort_values(by="Percentage", ascending=False).reset_index(
    drop=True
)

# 5. 국가 수에 맞춘 동적 초록색 그라데이션 생성 (matplotlib 없이 구현)
num_countries = len(rank_df)


# 간단한 보간법으로 초록색 계열 색상 리스트 생성 (진한 초록 -> 연한 초록)
def get_green_gradient(n):
  colors = []
  for i in range(n):
    # 진한 초록(#145A32)에서 연한 초록(#EAFAF1) 사이의 RGB 값 계산
    r = int(20 + (234 - 20) * (i / max(1, n - 1)))
    g = int(90 + (250 - 90) * (i / max(1, n - 1)))
    b = int(50 + (241 - 50) * (i / max(1, n - 1)))
    colors.append(f"rgb({r},{g},{b})")
  return colors


green_colors = get_green_gradient(num_countries - 1)

# 1등은 노란색(#FFD700), 나머지는 초록색 그라데이션 적용
bar_colors = ["#FFD700"] + green_colors

# 6. Plotly 막대그래프 생성
fig = go.Figure(
    data=[
        go.Bar(
            x=rank_df["Country"],
            y=rank_df["Percentage"],
            text=[f"{val:.2f}%" for val in rank_df["Percentage"]],
            textposition="auto",
            marker=dict(color=bar_colors),
        )
    ]
)

fig.update_layout(
    title=dict(
        text=(
            f"<b>전세계 국가별 '{selected_mbti}' 비율 순위 (높은 순)</b>"
        ),
        font=dict(size=20),
    ),
    xaxis_title="국가",
    yaxis_title="비율 (%)",
    template="plotly_white",
    height=600,
    xaxis=dict(tickangle=-45),
)

# 7. 화면 출력 (왼쪽: 요약 및 표, 오른쪽: 그래프)
col1, col2 = st.columns([1, 3])

with col1:
  st.subheader(f"🥇 {selected_mbti} 1위 국가")
  top_1 = rank_df.iloc[0]
  st.metric(
      label=f"{top_1['Country']}",
      value=f"{top_1['Percentage']:.2f}%",
      delta="1위",
  )

  st.write("---")
  st.markdown("### 📋 전체 국가 순위 표")
  st.dataframe(
      rank_df[["Country", "Percentage"]].style.format(
          {"Percentage": "{:.2f}%"}
      ),
      use_container_width=True,
      height=400,
  )

with col2:
  st.plotly_chart(fig, use_container_width=True)
