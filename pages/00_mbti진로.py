import streamlit as st

# ==========================================
# 🌈 페이지 설정
# ==========================================
st.set_page_config(
    page_title="MBTI 진로 탐험소",
    page_icon="🌈",
    layout="wide"
)

# ==========================================
# 🎨 디자인
# ==========================================
st.markdown("""
<style>
.stApp {
    background: linear-gradient(180deg, #F5F0FF, #FFFFFF);
}

.main-title {
    text-align: center;
    color: #7548B8;
    font-size: 38px;
    font-weight: 800;
    padding: 15px 0 5px 0;
}

.subtitle {
    text-align: center;
    color: #6B6078;
    font-size: 17px;
    line-height: 1.8;
    margin-bottom: 25px;
}

.career-card {
    background: white;
    border: 2px solid #E5D7FA;
    border-radius: 20px;
    padding: 22px;
    margin: 10px 0;
    min-height: 310px;
    box-shadow: 0 5px 15px rgba(90, 60, 140, 0.08);
}

.career-title {
    color: #7548B8;
    font-size: 23px;
    font-weight: 800;
    margin-bottom: 15px;
}

.career-label {
    color: #8055AD;
    font-weight: 700;
    margin-top: 15px;
}

.career-text {
    color: #51485D;
    line-height: 1.8;
    font-size: 15px;
}

.salary {
    background: #F0E9FF;
    color: #603AA1;
    border-radius: 12px;
    padding: 12px;
    font-weight: bold;
    margin-top: 15px;
}

.notice {
    background: #FFF5DC;
    padding: 18px;
    border-radius: 15px;
    line-height: 1.9;
    color: #6A5126;
}

.footer {
    text-align: center;
    color: #8A8294;
    font-size: 13px;
    padding: 20px 0;
}

@media (max-width: 600px) {
    .main-title {
        font-size: 29px;
    }

    .career-card {
        padding: 16px;
        min-height: auto;
    }
}
</style>
""", unsafe_allow_html=True)


# ==========================================
# 💼 MBTI별 진로 데이터
# 형식: 직업명, 이모지, 설명, 관련 학과,
#       도움이 되는 강점, 참고용 연봉 범위
# ==========================================
career_data = {
    "ISTJ": {
        "title": "📋 꼼꼼하고 책임감 있는 현실주의자",
        "desc": "체계적으로 계획하고 정확하게 일을 처리하는 걸 좋아한다면!",
        "jobs": [
            {
                "name": "회계사",
                "emoji": "🧮",
                "work": "기업의 재무 상태를 분석하고 회계 자료와 세금 관련 업무를 검토해.",
                "major": "회계학과, 경영학과, 세무학과",
                "personality": "꼼꼼함, 책임감, 논리적인 판단력",
                "salary": "약 4,000만~8,000만 원 이상",
            },
            {
                "name": "데이터 분석가",
                "emoji": "📊",
                "work": "데이터를 분석해 문제의 원인을 찾고 더 나은 의사결정을 도와.",
                "major": "통계학과, 데이터사이언스학과, 컴퓨터공학과",
                "personality": "분석력, 집중력, 논리적 사고",
                "salary": "약 3,500만~7,000만 원 이상",
            },
        ],
    },

    "ISFJ": {
        "title": "💗 세심하고 따뜻한 수호자",
        "desc": "주변 사람을 돕고 세심하게 챙기는 일에 관심이 있다면!",
        "jobs": [
            {
                "name": "간호사",
                "emoji": "🩺",
                "work": "환자의 건강 상태를 살피고 치료와 회복을 돕는 의료 전문가야.",
                "major": "간호학과",
                "personality": "세심함, 책임감, 협력하는 태도",
                "salary": "약 3,000만~6,000만 원 이상",
            },
            {
                "name": "초등학교 교사",
                "emoji": "🍎",
                "work": "학생들이 기초 지식을 배우고 건강하게 성장하도록 지도해.",
                "major": "교육대학교, 초등교육과",
                "personality": "인내심, 배려, 의사소통 능력",
                "salary": "약 3,000만~6,000만 원 이상",
            },
        ],
    },

    "INFJ": {
        "title": "🌌 의미와 가치를 생각하는 통찰가",
        "desc": "사람의 마음을 이해하거나 깊이 있는 이야기를 만드는 걸 좋아한다면!",
        "jobs": [
            {
                "name": "상담 전문가",
                "emoji": "💬",
                "work": "사람들이 고민을 이해하고 스스로 해결 방향을 찾도록 도와.",
                "major": "심리학과, 상담학과, 교육학과",
                "personality": "공감 능력, 경청, 윤리 의식",
                "salary": "약 2,800만~5,000만 원 이상",
            },
            {
                "name": "작가",
                "emoji": "✍️",
                "work": "소설, 에세이, 웹소설 등 다양한 글을 통해 생각과 이야기를 전달해.",
                "major": "국어국문학과, 문예창작학과, 콘텐츠학과",
                "personality": "상상력, 관찰력, 꾸준함",
                "salary": "약 2,500만~5,000만 원 이상",
            },
        ],
    },

    "INTJ": {
        "title": "♟️ 전략적으로 생각하는 설계자",
        "desc": "복잡한 문제를 분석하고 장기적인 계획을 세우는 걸 좋아한다면!",
        "jobs": [
            {
                "name": "소프트웨어 개발자",
                "emoji": "💻",
                "work": "컴퓨터 프로그램과 서비스를 설계하고 개발해.",
                "major": "컴퓨터공학과, 소프트웨어학과, AI학과",
                "personality": "논리력, 문제 해결력, 끈기",
                "salary": "약 3,500만~8,000만 원 이상",
            },
            {
                "name": "건축가",
                "emoji": "🏛️",
                "work": "건축물의 기능과 디자인, 안전 등을 고려해 공간을 계획해.",
                "major": "건축학과, 건축공학과",
                "personality": "공간 감각, 계획성, 창의력",
                "salary": "약 3,000만~6,000만 원 이상",
            },
        ],
    },

    "ISTP": {
        "title": "🔧 직접 탐구하고 해결하는 장인",
        "desc": "기계나 도구를 직접 다루면서 문제를 해결하는 게 재미있다면!",
        "jobs": [
            {
                "name": "기계 엔지니어",
                "emoji": "⚙️",
                "work": "기계와 장비를 설계하고 작동 원리를 분석해 개선해.",
                "major": "기계공학과, 메카트로닉스공학과",
                "personality": "분석력, 실용적인 사고, 문제 해결력",
                "salary": "약 3,500만~7,000만 원 이상",
            },
            {
                "name": "자동차 정비사",
                "emoji": "🚗",
                "work": "자동차의 상태를 점검하고 고장 원인을 찾아 수리해.",
                "major": "자동차공학과, 자동차과, 기계공학과",
                "personality": "관찰력, 손재주, 꼼꼼함",
                "salary": "약 2,800만~5,000만 원 이상",
            },
        ],
    },

    "ISFP": {
        "title": "🎨 감각적이고 자유로운 예술가",
        "desc": "색깔과 디자인, 아름다운 것들을 표현하는 데 관심이 있다면!",
        "jobs": [
            {
                "name": "일러스트레이터",
                "emoji": "🖌️",
                "work": "그림으로 책, 광고, 게임 등 다양한 콘텐츠를 표현해.",
                "major": "회화과, 일러스트레이션학과, 시각디자인학과",
                "personality": "관찰력, 표현력, 창의력",
                "salary": "약 2,500만~5,000만 원 이상",
            },
            {
                "name": "제품 디자이너",
                "emoji": "🪑",
                "work": "사람들이 편리하게 사용할 수 있는 제품을 디자인해.",
                "major": "산업디자인학과, 제품디자인학과",
                "personality": "미적 감각, 관찰력, 사용자에 대한 이해",
                "salary": "약 3,000만~6,000만 원 이상",
            },
        ],
    },

    "INFP": {
        "title": "🌷 가치와 상상력을 소중히 여기는 중재자",
        "desc": "상상력이 풍부하고 자신의 생각을 표현하는 걸 좋아한다면!",
        "jobs": [
            {
                "name": "시나리오 작가",
                "emoji": "🎬",
                "work": "영화와 드라마, 영상 콘텐츠의 인물과 이야기를 만들어.",
                "major": "문예창작학과, 영화학과, 방송영상학과",
                "personality": "상상력, 표현력, 관찰력",
                "salary": "약 2,500만~5,000만 원 이상",
            },
            {
                "name": "심리학 연구원",
                "emoji": "🧠",
                "work": "사람의 생각과 행동을 과학적인 방법으로 연구해.",
                "major": "심리학과, 인지과학과, 통계학과",
                "personality": "호기심, 분석력, 인내심",
                "salary": "약 3,000만~6,000만 원 이상",
            },
        ],
    },

    "INTP": {
        "title": "🔬 호기심 가득한 논리 탐구자",
        "desc": "왜 그런지 질문하고 새로운 원리를 알아내는 게 즐겁다면!",
        "jobs": [
            {
                "name": "과학 연구원",
                "emoji": "🔍",
                "work": "실험과 관찰을 통해 새로운 지식을 발견하고 연구 결과를 분석해.",
                "major": "물리학과, 화학과, 생명과학과 등 관련 전공",
                "personality": "호기심, 분석력, 탐구심",
                "salary": "약 3,000만~7,000만 원 이상",
            },
            {
                "name": "AI 개발자",
                "emoji": "🤖",
                "work": "인공지능 모델과 프로그램을 개발하고 성능을 개선해.",
                "major": "컴퓨터공학과, 인공지능학과, 수학과",
                "personality": "논리력, 수학적 사고, 실험 정신",
                "salary": "약 4,000만~9,000만 원 이상",
            },
        ],
    },

    "ESTP": {
        "title": "⚡ 행동력 넘치는 모험가",
        "desc": "직접 행동하고 빠르게 상황을 파악하는 걸 좋아한다면!",
        "jobs": [
            {
                "name": "응급구조사",
                "emoji": "🚑",
                "work": "응급 상황에서 환자를 평가하고 필요한 응급처치를 제공해.",
                "major": "응급구조학과",
                "personality": "침착함, 신속한 판단력, 책임감",
                "salary": "약 3,000만~5,000만 원 이상",
            },
            {
                "name": "스포츠 지도자",
                "emoji": "🏅",
                "work": "운동 기술을 가르치고 훈련과 경기 준비를 지도해.",
                "major": "체육학과, 스포츠과학과, 스포츠지도학과",
                "personality": "활동성, 소통 능력, 지도력",
                "salary": "약 2,800만~5,000만 원 이상",
            },
        ],
    },

    "ESFP": {
        "title": "🎉 즐거움과 에너지를 나누는 엔터테이너",
        "desc": "사람들과 어울리고 새로운 경험을 만드는 걸 좋아한다면!",
        "jobs": [
            {
                "name": "방송인",
                "emoji": "🎤",
                "work": "방송과 영상 콘텐츠를 통해 정보와 재미를 전달해.",
                "major": "신문방송학과, 미디어학과, 연극영화과",
                "personality": "표현력, 소통 능력, 순발력",
                "salary": "약 2,500만~6,000만 원 이상",
            },
            {
                "name": "이벤트 기획자",
                "emoji": "🎪",
                "work": "축제와 행사, 공연 등을 기획하고 현장을 운영해.",
                "major": "광고홍보학과, 문화콘텐츠학과, 관광학과",
                "personality": "활동성, 협업 능력, 순발력",
                "salary": "약 2,800만~5,000만 원 이상",
            },
        ],
    },

    "ENFP": {
        "title": "🌈 가능성을 발견하는 활동가",
        "desc": "새로운 아이디어를 떠올리고 다양한 분야에 도전하는 걸 좋아한다면!",
        "jobs": [
            {
                "name": "광고 기획자",
                "emoji": "💡",
                "work": "사람들의 관심을 끌 수 있는 광고 아이디어와 마케팅 전략을 기획해.",
                "major": "광고홍보학과, 경영학과, 미디어학과",
                "personality": "창의력, 소통 능력, 호기심",
                "salary": "약 3,000만~6,000만 원 이상",
            },
            {
                "name": "콘텐츠 크리에이터",
                "emoji": "📹",
                "work": "영상과 글, 이미지 등을 활용해 사람들에게 콘텐츠를 전달해.",
                "major": "미디어학과, 영상학과, 콘텐츠학과",
                "personality": "창의력, 표현력, 꾸준함",
                "salary": "약 2,500만~6,000만 원 이상",
            },
        ],
    },

    "ENTP": {
        "title": "💥 새로운 아이디어를 만드는 변론가",
        "desc": "기존의 방법에 질문을 던지고 새로운 가능성을 찾는 걸 좋아한다면!",
        "jobs": [
            {
                "name": "창업가",
                "emoji": "🚀",
                "work": "새로운 사업 아이디어를 구체화하고 제품이나 서비스를 만들어.",
                "major": "경영학과, 창업학과, 산업공학과 등",
                "personality": "도전 정신, 창의력, 문제 해결력",
                "salary": "개인별 편차가 커서 일률적인 연봉 산정이 어려워",
            },
            {
                "name": "브랜드 전략 기획자",
                "emoji": "📣",
                "work": "고객과 시장을 분석하고 브랜드의 성장 전략을 세워.",
                "major": "경영학과, 광고홍보학과, 마케팅학과",
                "personality": "기획력, 분석력, 설득력",
                "salary": "약 3,500만~7,000만 원 이상",
            },
        ],
    },

    "ESTJ": {
        "title": "📋 체계적으로 목표를 이루는 경영자",
        "desc": "계획을 세우고 사람들과 협력해 목표를 이루는 걸 좋아한다면!",
        "jobs": [
            {
                "name": "프로젝트 매니저",
                "emoji": "🗓️",
                "work": "프로젝트의 일정과 예산, 업무를 관리하고 목표 달성을 이끌어.",
                "major": "경영학과, 산업공학과, 정보시스템학과",
                "personality": "조직력, 책임감, 의사소통 능력",
                "salary": "약 4,000만~8,000만 원 이상",
            },
            {
                "name": "물류 관리자",
                "emoji": "📦",
                "work": "상품의 보관과 운송, 재고를 효율적으로 관리해.",
                "major": "물류학과, 산업공학과, 유통학과",
                "personality": "계획성, 분석력, 문제 해결력",
                "salary": "약 3,000만~6,000만 원 이상",
            },
        ],
    },

    "ESFJ": {
        "title": "🤝 사람들과 협력하는 외교관",
        "desc": "다른 사람을 돕고 함께 목표를 이루는 걸 좋아한다면!",
        "jobs": [
            {
                "name": "인사 담당자",
                "emoji": "👥",
                "work": "직원 채용과 교육, 조직문화 개선 등 사람과 관련된 업무를 담당해.",
                "major": "경영학과, 심리학과, 행정학과",
                "personality": "소통 능력, 배려, 조직력",
                "salary": "약 3,000만~6,000만 원 이상",
            },
            {
                "name": "호텔 서비스 매니저",
                "emoji": "🏨",
                "work": "고객에게 좋은 서비스를 제공하고 호텔 운영을 관리해.",
                "major": "호텔경영학과, 관광학과, 서비스경영학과",
                "personality": "친절함, 소통 능력, 문제 해결력",
                "salary": "약 3,000만~6,000만 원 이상",
            },
        ],
    },

    "ENFJ": {
        "title": "🌟 사람들의 성장을 돕는 선도자",
        "desc": "다른 사람의 장점을 발견하고 성장을 돕는 일이 즐겁다면!",
        "jobs": [
            {
                "name": "진로 상담 전문가",
                "emoji": "🧭",
                "work": "학생과 구직자가 관심사와 강점을 발견하고 진로를 탐색하도록 도와.",
                "major": "교육학과, 상담학과, 심리학과",
                "personality": "공감 능력, 경청, 소통 능력",
                "salary": "약 2,800만~5,000만 원 이상",
            },
            {
                "name": "교육 프로그램 기획자",
                "emoji": "📚",
                "work": "사람들이 효과적으로 배우도록 교육 콘텐츠와 프로그램을 설계해.",
                "major": "교육학과, 교육공학과, 평생교육학과",
                "personality": "기획력, 공감 능력, 협업 능력",
                "salary": "약 3,000만~5,500만 원 이상",
            },
        ],
    },

    "ENTJ": {
        "title": "🏆 목표를 향해 나아가는 지휘관",
        "desc": "큰 목표를 세우고 전략적으로 실행하는 걸 좋아한다면!",
        "jobs": [
            {
                "name": "경영 컨설턴트",
                "emoji": "📈",
                "work": "기업의 문제를 분석하고 성과를 높일 수 있는 전략을 제안해.",
                "major": "경영학과, 경제학과, 산업공학과",
                "personality": "분석력, 리더십, 전략적 사고",
                "salary": "약 4,000만~9,000만 원 이상",
            },
            {
                "name": "사업 기획자",
                "emoji": "🎯",
                "work": "사업 목표와 실행 계획을 세우고 새로운 성장 기회를 찾아.",
                "major": "경영학과, 경제학과, 산업공학과",
                "personality": "기획력, 추진력, 의사결정 능력",
                "salary": "약 3,500만~7,000만 원 이상",
            },
        ],
    },
}


# ==========================================
# 🏠 메인 화면
# ==========================================
st.markdown(
    '<div class="main-title">🌈 MBTI 진로 탐험소 🚀</div>',
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="subtitle">
        내 MBTI로 발견하는 새로운 직업의 세계! ✨<br>
        나에게 맞는 진로 아이디어를 재미있게 찾아보자.
    </div>
    """,
    unsafe_allow_html=True
)

st.info(
    "💜 MBTI 유형을 선택하면 추천 직업 2개와 "
    "관련 학과, 도움이 되는 성격, 참고용 연봉을 알려 줄게!"
)

# ==========================================
# 🧩 MBTI 선택
# ==========================================
mbti_list = [
    "ISTJ", "ISFJ", "INFJ", "INTJ",
    "ISTP", "ISFP", "INFP", "INTP",
    "ESTP", "ESFP", "ENFP", "ENTP",
    "ESTJ", "ESFJ", "ENFJ", "ENTJ"
]

selected_mbti = st.selectbox(
    "🧩 나의 MBTI를 선택해 줘!",
    mbti_list,
    format_func=lambda x: f"{x} | {career_data[x]['title']}"
)

st.markdown("---")

# ==========================================
# 🚀 진로 추천 결과
# ==========================================
if st.button("🚀 내 진로 알아보기!", use_container_width=True):

    result = career_data[selected_mbti]

    st.balloons()

    st.markdown(f"# 🎉 {selected_mbti} 진로 탐험 결과")

    st.markdown(f"### {result['title']}")

    st.write(result["desc"])

    st.markdown("## 💼 너를 위한 추천 직업 TOP 2")

    columns = st.columns(2)

    for index, job in enumerate(result["jobs"]):

        with columns[index]:

            st.markdown(
                f"""
                <div class="career-card">
                    <div class="career-title">
                        {job['emoji']} {job['name']}
                    </div>

                    <div class="career-text">
                        {job['work']}
                    </div>

                    <div class="career-label">
                        🎓 관련 학과
                    </div>

                    <div class="career-text">
                        {job['major']}
                    </div>

                    <div class="career-label">
                        💖 도움이 되는 성격과 강점
                    </div>

                    <div class="career-text">
                        {job['personality']}
                    </div>

                    <div class="salary">
                        💰 참고용 연봉<br>
                        {job['salary']}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

    st.markdown("## 🌟 나만의 진로 미션")

    st.success(
        """
        **미션 1. 🔎 직업 탐색하기**  
        두 직업 중 더 궁금한 직업을 하나 골라 봐!

        **미션 2. 📚 학과 알아보기**  
        관련 학과에서 어떤 과목을 배우는지 찾아봐.

        **미션 3. 🎯 직접 경험하기**  
        관련 책을 읽거나 체험 활동에 참여해 보자!
        """
    )

    st.markdown(
        """
        <div class="notice">
            💛 <b>꼭 기억해!</b><br><br>
            MBTI는 진로를 결정하는 정답이 아니야.<br>
            같은 MBTI라도 좋아하는 활동과 잘하는 일은 다를 수 있어.<br>
            추천 직업은 여러 가능성 중 일부일 뿐이야! 🌱<br><br>
            💰 연봉은 직업별 공식 통계를 실시간 조회한 값이 아니라
            대략적인 참고 범위야. 경력, 기업 규모, 지역, 자격 등에 따라
            실제 연봉은 달라질 수 있어.
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("### 🔍 더 자세히 알아보기")

    st.markdown(
        "- [한국고용정보원 직업정보](https://www.work.go.kr/consltJobCarpa/srch/jobInfoSrch/srchJobInfo.do)"
    )

    st.markdown(
        "- [커리어넷 진로·직업 정보](https://www.career.go.kr/)"
    )

else:

    st.markdown("## 💜 진로 탐험을 시작해 볼까?")

    st.write(
        "위에서 MBTI를 선택하고 버튼을 눌러 봐! "
        "너에게 새로운 진로 아이디어를 소개해 줄게. 🎁"
    )

    st.markdown(
        """
        🌱 **이런 걸 알아볼 수 있어!**

        - 🎓 어떤 학과를 공부하면 좋을까?
        - 💖 어떤 성격과 강점이 도움이 될까?
        - 💰 연봉은 어느 정도일까?
        """
    )

# ==========================================
# 📌 하단 안내
# ==========================================
st.markdown("---")

st.markdown(
    """
    <div class="footer">
        🌈 MBTI 진로 탐험소 | 나의 가능성을 발견하는 시간 ✨<br>
        진로 탐색을 위한 참고용 콘텐츠입니다.
    </div>
    """,
    unsafe_allow_html=True
)
