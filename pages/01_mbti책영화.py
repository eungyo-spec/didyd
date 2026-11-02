import streamlit as st
import random

# 🍋 페이지 설정
st.set_page_config(
    page_title="MBTI 취향 탐험소",
    page_icon="🍋",
    layout="wide"
)

# 🎨 디자인
st.markdown("""
<style>
    .stApp {
        background-color: #FFFDF5;
    }

    h1 {
        color: #FF8C42;
        text-align: center;
    }

    h2, h3 {
        color: #5A9E6F;
    }

    .intro {
        text-align: center;
        font-size: 18px;
        color: #666666;
    }

    .recommend-card {
        background-color: #FFFFFF;
        padding: 20px;
        border-radius: 15px;
        border: 2px solid #FFE0A3;
        margin-bottom: 12px;
    }

    .tag {
        color: #E98232;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)


# 📚 MBTI별 도서 및 영화 추천 데이터
# 형식: 국내 도서, 해외 도서, 국내 영화, 해외 영화

recommendations = {
    "ISTJ": {
        "books": [
            ("불편한 편의점", "김호연", "국내"),
            ("모모", "미하엘 엔데", "해외")
        ],
        "movies": [
            ("리틀 포레스트", "임순례 감독", "국내"),
            ("쇼생크 탈출", "프랭크 다라본트 감독", "해외")
        ]
    },

    "ISFJ": {
        "books": [
            ("아몬드", "손원평", "국내"),
            ("어린 왕자", "앙투안 드 생텍쥐페리", "해외")
        ],
        "movies": [
            ("집으로...", "이정향 감독", "국내"),
            ("패딩턴", "폴 킹 감독", "해외")
        ]
    },

    "INFJ": {
        "books": [
            ("소년이 온다", "한강", "국내"),
            ("데미안", "헤르만 헤세", "해외")
        ],
        "movies": [
            ("벌새", "김보라 감독", "국내"),
            ("죽은 시인의 사회", "피터 위어 감독", "해외")
        ]
    },

    "INTJ": {
        "books": [
            ("천 개의 파랑", "천선란", "국내"),
            ("1984", "조지 오웰", "해외")
        ],
        "movies": [
            ("설국열차", "봉준호 감독", "국내"),
            ("인터스텔라", "크리스토퍼 놀란 감독", "해외")
        ]
    },

    "ISTP": {
        "books": [
            ("달러구트 꿈 백화점", "이미예", "국내"),
            ("노인과 바다", "어니스트 헤밍웨이", "해외")
        ],
        "movies": [
            ("베테랑", "류승완 감독", "국내"),
            ("마션", "리들리 스콧 감독", "해외")
        ]
    },

    "ISFP": {
        "books": [
            ("어서 오세요, 휴남동 서점입니다", "황보름", "국내"),
            ("키친", "요시모토 바나나", "해외")
        ],
        "movies": [
            ("리틀 포레스트", "임순례 감독", "국내"),
            ("비긴 어게인", "존 카니 감독", "해외")
        ]
    },

    "INFP": {
        "books": [
            ("아몬드", "손원평", "국내"),
            ("어린 왕자", "앙투안 드 생텍쥐페리", "해외")
        ],
        "movies": [
            ("너의 결혼식", "이석근 감독", "국내"),
            ("월터의 상상은 현실이 된다", "벤 스틸러 감독", "해외")
        ]
    },

    "INTP": {
        "books": [
            ("지구 끝의 온실", "김초엽", "국내"),
            ("프랑켄슈타인", "메리 셸리", "해외")
        ],
        "movies": [
            ("잠", "유재선 감독", "국내"),
            ("인셉션", "크리스토퍼 놀란 감독", "해외")
        ]
    },

    "ESTP": {
        "books": [
            ("완득이", "김려령", "국내"),
            ("톰 소여의 모험", "마크 트웨인", "해외")
        ],
        "movies": [
            ("극한직업", "이병헌 감독", "국내"),
            ("스파이더맨: 뉴 유니버스", "밥 퍼시케티 외", "해외")
        ]
    },

    "ESFP": {
        "books": [
            ("불편한 편의점", "김호연", "국내"),
            ("찰리와 초콜릿 공장", "로알드 달", "해외")
        ],
        "movies": [
            ("써니", "강형철 감독", "국내"),
            ("맘마미아!", "필리다 로이드 감독", "해외")
        ]
    },

    "ENFP": {
        "books": [
            ("달러구트 꿈 백화점", "이미예", "국내"),
            ("해리 포터와 마법사의 돌", "J. K. 롤링", "해외")
        ],
        "movies": [
            ("엑시트", "이상근 감독", "국내"),
            ("업", "피트 닥터 감독", "해외")
        ]
    },

    "ENTP": {
        "books": [
            ("천 개의 파랑", "천선란", "국내"),
            ("이상한 나라의 앨리스", "루이스 캐럴", "해외")
        ],
        "movies": [
            ("극한직업", "이병헌 감독", "국내"),
            ("트루먼 쇼", "피터 위어 감독", "해외")
        ]
    },

    "ESTJ": {
        "books": [
            ("역사의 쓸모", "최태성", "국내"),
            ("어린 왕자", "앙투안 드 생텍쥐페리", "해외")
        ],
        "movies": [
            ("국가대표", "김용화 감독", "국내"),
            ("히든 피겨스", "시어도어 멜피 감독", "해외")
        ]
    },

    "ESFJ": {
        "books": [
            ("어서 오세요, 휴남동 서점입니다", "황보름", "국내"),
            ("작은 아씨들", "루이자 메이 올컷", "해외")
        ],
        "movies": [
            ("7번방의 선물", "이환경 감독", "국내"),
            ("패딩턴", "폴 킹 감독", "해외")
        ]
    },

    "ENFJ": {
        "books": [
            ("페인트", "이희영", "국내"),
            ("연금술사", "파울로 코엘료", "해외")
        ],
        "movies": [
            ("완득이", "이한 감독", "국내"),
            ("죽은 시인의 사회", "피터 위어 감독", "해외")
        ]
    },

    "ENTJ": {
        "books": [
            ("불편한 편의점", "김호연", "국내"),
            ("1984", "조지 오웰", "해외")
        ],
        "movies": [
            ("변호인", "양우석 감독", "국내"),
            ("머니볼", "베넷 밀러 감독", "해외")
        ]
    }
}


# 🌟 앱 제목
st.title("🍋 MBTI 취향 탐험소")
st.markdown(
    '<p class="intro">'
    '내 MBTI와 잘 어울리는 책과 영화를 찾아 떠나 볼까요? 📚🎬'
    '</p>',
    unsafe_allow_html=True
)

st.write("")
st.info("💡 MBTI를 선택하면 책 2권과 영화 2편을 추천해 드려요!")

# 🧩 MBTI 선택
mbti_list = [
    "ISTJ", "ISFJ", "INFJ", "INTJ",
    "ISTP", "ISFP", "INFP", "INTP",
    "ESTP", "ESFP", "ENFP", "ENTP",
    "ESTJ", "ESFJ", "ENFJ", "ENTJ"
]

selected_mbti = st.selectbox(
    "🧩 나의 MBTI를 선택해 주세요!",
    mbti_list
)

# 🔍 추천 버튼
if st.button("✨ 나만의 추천 확인하기!", use_container_width=True):

    data = recommendations[selected_mbti]

    st.success(
        f"🎉 {selected_mbti} 유형을 위한 추천 결과가 도착했어요!"
    )

    # 📚 책 추천
    st.header("📚 오늘의 책 추천")

    col1, col2 = st.columns(2)

    for i, book in enumerate(data["books"]):
        title, author, category = book

        with (col1 if i == 0 else col2):
            st.markdown(
                f"""
                <div class="recommend-card">
                    <h3>📖 {title}</h3>
                    <p><b>작가</b> : {author}</p>
                    <p class="tag">🌏 {category} 도서</p>
                </div>
                """,
                unsafe_allow_html=True
            )

    st.write("")

    # 🎬 영화 추천
    st.header("🎬 오늘의 영화 추천")

    col3, col4 = st.columns(2)

    for i, movie in enumerate(data["movies"]):
        title, director, category = movie

        with (col3 if i == 0 else col4):
            st.markdown(
                f"""
                <div class="recommend-card">
                    <h3>🍿 {title}</h3>
                    <p><b>감독</b> : {director}</p>
                    <p class="tag">🌏 {category} 영화</p>
                </div>
                """,
                unsafe_allow_html=True
            )

    st.divider()

    st.markdown(
        """
        <h3 style="text-align:center;">
            🍀 오늘의 추천이 마음에 들었나요?
        </h3>
        <p style="text-align:center;">
            책과 영화 속에서 새로운 취향을 발견해 봐요! 💚
        </p>
        """,
        unsafe_allow_html=True
    )

    if st.button("🎲 다른 MBTI도 구경하기"):
        st.rerun()

else:
    st.markdown("---")
    st.markdown(
        """
        <div style="text-align:center;">
            <h3>🍊 어떤 작품을 만나게 될까요?</h3>
            <p>MBTI를 선택하고 버튼을 눌러 보세요!</p>
            <p>📚 국내 도서 1권 + 해외 도서 1권</p>
            <p>🎬 국내 영화 1편 + 해외 영화 1편</p>
        </div>
        """,
        unsafe_allow_html=True
    )
