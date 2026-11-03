import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import matplotlib.colors as mcolors

# 1. 페이지 설정
st.set_page_config(
    page_title="세계 국가별 MBTI 분포",
    page_icon="🌍",
    layout="wide"
)


# 2. 데이터 로드 (캐싱을 통해 속도 최적화)
@st.cache_data
def load_data():
    df = pd.read_csv("countriesMBTI_16types (1).csv")
    return df


df = load_data()
mbti_cols = [c for c in df.columns if c != "Country"]

# 메인 타이틀
st.title("🌍 국가별 MBTI 비율 시각화")
st.markdown(
    "국가를 선택하면 16가지 MBTI 비율을 확인하실 수 있습니다. (1위: 노란색, 2위~16위: 초록색 그라데이션)"
)

# 3. 사이드바 - 국가 선택
selected_country = st.sidebar.selectbox(
    "국가를 선택하세요:", options=df["Country"].unique()
)

# 4. 선택된 국가 데이터 추출 및 정렬
country_row = df[df["Country"] == selected_country].iloc[0]

mbti_df = (
    pd.DataFrame(
        {
            "MBTI": mbti_cols,
            "Ratio": [country_row[col] for col in mbti_cols],
            "Percentage": [country_row[col] * 100 for col in mbti_cols],
        }
    )
    .sort_values(by="Ratio", ascending=False)
    .reset_index(drop=True)
)

# 5. 색상 그라데이션 생성 (1등: 노란색, 2등~16등: 초록색 -> 점점 어두워짐)
# 밝은 연두/초록(#76D7C4)부터 딥 그린/어두운 초록(#145A32)까지 15단계 생성
green_cmap = mcolors.LinearSegmentedColorMap.from_list(
    "green_grad", ["#76D7C4", "#145A32"], N=15
)
green_colors = [
    mcolors.to_hex(green_cmap(i / 14)) for i in range(15)
]

# 1등은 노란색(#FFD700), 나머지는 그라데이션 색상 배치
bar_colors = ["#FFD700"] + green_colors

# 6. Plotly 막대그래프 생성
fig = go.Figure(
    data=[
        go.Bar(
            x=mbti_df["MBTI"],
            y=mbti_df["Percentage"],
            text=[f"{val:.2f}%" for val in mbti_df["Percentage"]],
            textposition="auto",
            marker=dict(color=bar_colors),
        )
    ]
)

fig.update_layout(
    title=dict(
        text=f"<b>{selected_country}의 MBTI 유형별 비율 (%)</b>", font=dict(size=20)
    ),
    xaxis_title="MBTI 유형",
    yaxis_title="비율 (%)",
    template="plotly_white",
    height=550,
)

# 7. 화면 출력
col1, col2 = st.columns([1, 3])

with col1:
    st.subheader(f"📌 {selected_country} 요약")
    top_1 = mbti_df.iloc[0]
    st.metric(
        label="🥇 가장 높은 비율 (1위)",
        value=top_1["MBTI"],
        delta=f"{top_1['Percentage']:.2f}%",
    )

    st.write("---")
    st.dataframe(
        mbti_df[["MBTI", "Percentage"]].style.format(
            {"Percentage": "{:.2f}%"}
        ),
        use_container_width=True,
        height=350,
    )

with col2:
    st.plotly_chart(fig, use_container_width=True)
