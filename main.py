import streamlit as st
import hashlib
import random
from datetime import date
from PIL import Image

st.set_page_config(
    page_title="운명의 정원",
    page_icon="🌙",
    layout="wide"
)

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #160e2b, #281744, #120d23);
    color: #f5eaff;
}
h1, h2, h3 {
    color: #e8caff !important;
}
div.stButton > button {
    background: linear-gradient(90deg, #9b72cf, #d2a8ff);
    color: white;
    border-radius: 15px;
    border: none;
    padding: 12px;
    font-weight: bold;
}
.card {
    background: rgba(255,255,255,0.08);
    border: 1px solid rgba(210,170,255,0.3);
    border-radius: 18px;
    padding: 22px;
    margin: 10px 0;
}
.tarot-back {
    text-align:center;
    padding: 1rem .35rem;
    border-radius: 14px;
    border: 1px solid #d6b4e9;
    background: radial-gradient(circle at center,rgba(255,220,150,.14),transparent 55%),
                linear-gradient(145deg,#563078,#241342);
    color: #f8e7b8;
    font-size: 1.8rem;
    min-height: 82px;
}
.tarot-face {
    border: 2px solid #e9c879;
    border-radius: 16px;
    padding: .9rem .5rem;
    text-align: center;
    background: linear-gradient(155deg,#fff2cf,#d8b8e6);
    color: #32164d;
    min-height: 155px;
    box-shadow: 0 8px 20px #10051e66;
}
.tarot-face .symbol { font-size: 2.3rem; margin: .35rem; }
.tarot-face .name { font-weight: bold; font-size: .88rem; }
.tarot-face .keyword { font-size: .7rem; margin-top: .35rem; color: #67447c; }
.tarot-note { color:#d9c8e9; font-size:.88rem; line-height:1.8; }
</style>
""", unsafe_allow_html=True)

st.title("🌙 운명의 정원")
st.caption("두 사람의 사주 · 궁합 연구소")
st.markdown("---")

tab1, tab2, tab3 = st.tabs([
    "💫 생년월일 궁합",
    "🔮 얼굴 관상",
    "🌙 타로 연애 상담"
])

# ---------------------------
# 생년월일 궁합
# ---------------------------
with tab1:
    st.subheader("두 사람의 생년월일을 입력하세요")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 🌷 첫 번째 사람")
        name1 = st.text_input("이름 또는 별명", key="name1")
        birth1 = st.date_input(
            "생년월일",
            value=date(2008, 1, 1),
            key="birth1"
        )

    with col2:
        st.markdown("### 🌙 두 번째 사람")
        name2 = st.text_input("이름 또는 별명", key="name2")
        birth2 = st.date_input(
            "생년월일",
            value=date(2008, 1, 1),
            key="birth2"
        )

    relationship = st.selectbox(
        "두 사람의 관계",
        ["친구", "짝사랑", "연인", "썸", "궁금한 사람"]
    )

    if st.button("✨ 궁합 확인하기", use_container_width=True):

        seed = f"{birth1}-{birth2}-{name1}-{name2}"
        score = int(hashlib.sha256(seed.encode()).hexdigest(), 16) % 101

        st.markdown("---")
        st.markdown("## 💜 두 사람의 궁합 결과")

        st.markdown(
            f"""
            <div class="card">
                <h2 style="text-align:center;">
                    {name1 or "첫 번째 사람"} ✨
                    {name2 or "두 번째 사람"}
                </h2>
                <h1 style="text-align:center;font-size:60px;">
                    {score}점
                </h1>
                <p style="text-align:center;">
                    두 사람의 관계를 재미로 알아보는 궁합 결과
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

        if score >= 80:
            result = "서로의 매력을 발견하기 쉬운 조합"
            description = "함께할 때 즐거운 경험을 쌓고 서로의 차이를 이해한다면 좋은 관계를 만들어갈 수 있어요."
        elif score >= 60:
            result = "천천히 알아갈수록 좋은 조합"
            description = "서로의 성향을 알아가는 과정이 중요해요. 대화를 통해 관계를 발전시켜 보세요."
        elif score >= 40:
            result = "서로 다른 매력을 가진 조합"
            description = "생각이나 표현 방식이 다를 수 있지만, 차이를 존중하면 좋은 관계가 될 수 있어요."
        else:
            result = "새로운 관점을 배우는 조합"
            description = "서로에게 익숙하지 않은 부분이 있을 수 있어요. 충분한 대화와 이해가 중요해요."

        st.markdown(f"### 🌸 {result}")
        st.write(description)

        st.markdown("### 💌 관계 조언")

        advice_list = [
            "상대방의 이야기를 끝까지 들어주기",
            "고마운 마음을 작은 말로 표현하기",
            "서로의 개인적인 시간 존중하기",
            "오해가 생기면 추측보다 대화하기",
            "함께 즐길 수 있는 새로운 활동 찾아보기"
        ]

        st.info(advice_list[score % len(advice_list)])

        st.markdown("### 🌟 추천 데이트·활동")

        activities = [
            "함께 카페에서 이야기 나누기 ☕",
            "산책하며 사진 찍기 📸",
            "보드게임이나 게임 즐기기 🎲",
            "서로 좋아하는 음악 공유하기 🎧",
            "맛있는 음식 먹으러 가기 🍰"
        ]

        st.write(activities[score % len(activities)])

        st.caption(
            "※ 이 궁합은 재미와 자기성찰을 위한 콘텐츠이며, "
            "실제 관계나 미래를 과학적으로 예측하지 않습니다."
        )

# ---------------------------
# 얼굴 관상
# ---------------------------
with tab2:

    st.subheader("🔮 관상 연구소")
    st.write(
        "사진을 업로드하고 특징을 선택하면 "
        "전통 관상 해석을 재미로 확인할 수 있어요."
    )

    uploaded_file = st.file_uploader(
        "사진 업로드",
        type=["jpg", "jpeg", "png"]
    )

    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(
            image,
            caption="업로드한 사진",
            use_container_width=True
        )

    st.markdown("---")
    st.markdown("### 얼굴 특징 선택")

    face_shape = st.selectbox(
        "얼굴형",
        ["둥근형", "계란형", "각진형", "긴형"]
    )

    eyes = st.selectbox(
        "눈의 특징",
        ["큰 눈", "작은 눈", "둥근 눈", "길고 가느다란 눈"]
    )

    eyebrows = st.selectbox(
        "눈썹",
        ["일자형", "아치형", "짙은 눈썹", "얇은 눈썹"]
    )

    nose = st.selectbox(
        "코",
        ["높은 코", "둥근 코끝", "작은 코", "직선형 코"]
    )

    mouth = st.selectbox(
        "입",
        ["작은 입", "큰 입", "도톰한 입술", "얇은 입술"]
    )

    if st.button("🌙 관상 결과 확인하기", use_container_width=True):

        interpretations = {
            "둥근형": "전통 관상에서는 둥근 얼굴형을 부드러운 인상과 연결해 해석하기도 해요.",
            "계란형": "전통적으로 균형과 조화의 이미지로 해석되곤 해요.",
            "각진형": "단단하고 뚜렷한 인상의 상징으로 해석되기도 해요.",
            "긴형": "차분하고 지적인 분위기의 상징으로 풀이하기도 해요."
        }

        eye_interpretations = {
            "큰 눈": "호기심과 표현력의 상징으로 해석하기도 해요.",
            "작은 눈": "세심함과 신중함의 이미지로 풀이하기도 해요.",
            "둥근 눈": "부드럽고 친근한 분위기의 상징으로 보기도 해요.",
            "길고 가느다란 눈": "차분하고 집중력 있는 이미지로 해석하기도 해요."
        }

        eyebrow_interpretations = {
            "일자형": "솔직하고 담백한 이미지의 상징으로 풀이하기도 해요.",
            "아치형": "부드러운 표현과 유연함의 이미지로 해석하기도 해요.",
            "짙은 눈썹": "뚜렷한 인상의 상징으로 보기도 해요.",
            "얇은 눈썹": "섬세하고 정돈된 분위기의 상징으로 풀이하기도 해요."
        }

        nose_interpretations = {
            "높은 코": "전통 해석에서는 자신감의 이미지와 연결하기도 해요.",
            "둥근 코끝": "온화하고 편안한 인상의 상징으로 보기도 해요.",
            "작은 코": "섬세한 분위기의 상징으로 해석하기도 해요.",
            "직선형 코": "깔끔하고 정돈된 이미지로 풀이하기도 해요."
        }

        mouth_interpretations = {
            "작은 입": "차분한 표현의 이미지로 해석하기도 해요.",
            "큰 입": "활발한 소통의 상징으로 풀이하기도 해요.",
            "도톰한 입술": "따뜻한 표현의 이미지로 연결하기도 해요.",
            "얇은 입술": "신중한 표현의 상징으로 보기도 해요."
        }

        st.markdown("---")
        st.markdown("## ✨ 관상 풀이")

        st.markdown(
            f"""
            <div class="card">
                <h3>🌷 얼굴형</h3>
                <p>{face_shape}</p>
                <p>{interpretations[face_shape]}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            f"""
            <div class="card">
                <h3>👁 눈</h3>
                <p>{eyes}</p>
                <p>{eye_interpretations[eyes]}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            f"""
            <div class="card">
                <h3>🌙 눈썹</h3>
                <p>{eyebrows}</p>
                <p>{eyebrow_interpretations[eyebrows]}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            f"""
            <div class="card">
                <h3>✨ 코</h3>
                <p>{nose}</p>
                <p>{nose_interpretations[nose]}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            f"""
            <div class="card">
                <h3>💐 입</h3>
                <p>{mouth}</p>
                <p>{mouth_interpretations[mouth]}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            """
            <div class="card">
                <h3>💜 종합 해석</h3>
                <p>
                전통 관상은 오랜 문화적 해석을 바탕으로 한 재미 콘텐츠예요.
                얼굴 특징만으로 성격, 능력, 운명 또는 미래를
                정확하게 판단할 수는 없어요.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

# ---------------------------
# 타로 카드 데이터 및 해석 함수
# ---------------------------


CARDS = [
    {"name":"바보 (The Fool)","symbol":"🧳","keyword":"새로운 시작 · 자유 · 설렘",
     "meaning":"새로운 가능성을 향해 가볍게 발걸음을 내딛는 카드입니다. 정해진 틀보다 경험과 호기심을 중요하게 여기며, 사랑에서도 계산하기보다 마음이 움직이는 순간을 소중히 여길 수 있습니다. 다만 충분히 생각하지 않고 관계를 시작하거나 상대의 신호를 놓치지 않도록 주의가 필요합니다.",
     "love":"연애에서는 풋풋한 호감과 새로운 출발을 나타냅니다. 서로에게 부담을 주기보다 자연스럽게 알아가는 과정이 잘 어울립니다."},
    {"name":"마법사 (The Magician)","symbol":"✨","keyword":"표현력 · 자신감 · 주도성",
     "meaning":"자신이 가진 능력과 매력을 활용해 상황을 만들어 가는 카드입니다. 생각을 행동으로 옮기는 힘이 있고, 대화와 표현을 통해 관계에 활기를 불어넣을 수 있습니다. 다만 말과 행동이 일치하는지 살피는 태도가 중요합니다.",
     "love":"연애에서는 먼저 다가가거나 마음을 표현하는 능력, 관계를 발전시키려는 적극성을 뜻합니다."},
    {"name":"여사제 (The High Priestess)","symbol":"🌙","keyword":"직감 · 신중함 · 내면",
     "meaning":"겉으로 드러난 말보다 분위기와 감정을 세심하게 읽는 카드입니다. 속마음을 쉽게 공개하지 않고 충분히 관찰한 뒤 마음을 여는 편일 수 있습니다. 혼자 추측하기보다는 필요한 순간 솔직하게 확인하는 것이 좋습니다.",
     "love":"연애에서는 조용한 호감, 깊은 감정, 신중한 관계 형성을 나타냅니다. 서로의 속도를 존중하는 것이 중요합니다."},
    {"name":"여황제 (The Empress)","symbol":"🌷","keyword":"다정함 · 풍요 · 돌봄",
     "meaning":"따뜻함과 배려를 통해 주변을 편안하게 만드는 카드입니다. 상대의 감정을 살피고 애정을 표현하는 데 능숙할 수 있습니다. 다만 상대를 챙기는 데만 집중해 자신의 필요를 뒤로 미루지 않는 것이 좋습니다.",
     "love":"연애에서는 애정 표현, 안정감, 서로를 아끼는 관계를 상징합니다."},
    {"name":"황제 (The Emperor)","symbol":"👑","keyword":"책임감 · 안정 · 원칙",
     "meaning":"관계에서 책임과 약속, 일관성을 중요하게 생각하는 카드입니다. 쉽게 흔들리지 않는 장점이 있지만 자신의 방식만 옳다고 여기면 상대가 답답함을 느낄 수 있습니다.",
     "love":"연애에서는 믿음직함과 안정적인 관계를 뜻합니다. 감정을 말로 표현하는 노력도 함께하면 좋습니다."},
    {"name":"교황 (The Hierophant)","symbol":"🕊️","keyword":"가치관 · 신뢰 · 약속",
     "meaning":"공통된 가치관과 서로 지켜야 할 약속을 중요하게 여기는 카드입니다. 관계를 가볍게 보기보다 진지하게 생각할 수 있습니다. 익숙한 기준에만 얽매이지 않고 서로 다른 생각도 존중하는 것이 중요합니다.",
     "love":"연애에서는 진지한 만남, 신뢰, 관계에 대한 합의와 책임을 나타냅니다."},
    {"name":"연인 (The Lovers)","symbol":"💞","keyword":"끌림 · 선택 · 조화",
     "meaning":"서로에게 끌리는 마음과 관계에서의 선택을 상징합니다. 감정적인 교감이 중요하지만, 좋은 관계는 끌림만으로 완성되지 않습니다. 서로의 가치관과 원하는 관계를 솔직하게 나누는 것이 핵심입니다.",
     "love":"연애에서는 호감과 교감, 관계를 선택하는 순간을 나타냅니다. 서로의 마음을 확인하는 대화가 중요합니다."},
    {"name":"전차 (The Chariot)","symbol":"🏇","keyword":"추진력 · 목표 · 의지",
     "meaning":"원하는 방향을 향해 적극적으로 나아가는 카드입니다. 관계를 발전시키려는 의지가 강할 수 있지만, 속도와 주도권을 두고 부딪힐 수도 있습니다. 함께 목표를 정하고 상대의 속도를 확인해 보세요.",
     "love":"연애에서는 관계 진전과 적극성을 뜻하지만, 한쪽만 앞서가지 않도록 조율해야 합니다."},
    {"name":"힘 (Strength)","symbol":"🦁","keyword":"인내 · 다정한 용기 · 절제",
     "meaning":"강압이 아니라 이해와 인내로 상황을 다루는 힘을 뜻합니다. 상대의 부족한 점을 기다려 주고 차분하게 대화할 수 있습니다. 다만 참는 것만이 배려는 아니므로 불편함도 건강하게 표현해야 합니다.",
     "love":"연애에서는 서로를 이해하려는 노력과 감정 조절, 부드러운 신뢰를 상징합니다."},
    {"name":"은둔자 (The Hermit)","symbol":"🏮","keyword":"성찰 · 독립성 · 거리",
     "meaning":"혼자 생각하고 자신만의 시간을 갖는 것이 중요한 카드입니다. 감정을 정리한 뒤 표현하는 편일 수 있어 상대에게는 다소 조용하게 보일 수 있습니다. 필요한 거리와 관심의 균형을 대화로 맞춰 보세요.",
     "love":"연애에서는 천천히 알아가는 관계와 개인 시간의 존중을 나타냅니다."},
    {"name":"운명의 수레바퀴 (Wheel of Fortune)","symbol":"🎡","keyword":"변화 · 전환점 · 흐름",
     "meaning":"예상하지 못한 변화와 관계의 흐름을 상징합니다. 상황이 빠르게 달라질 수 있으므로 한순간의 분위기만으로 결론을 내리지 않는 것이 좋습니다. 변화가 생겼을 때 함께 대처하는 태도가 중요합니다.",
     "love":"연애에서는 우연한 계기나 관계의 전환점을 뜻합니다. 흐름을 지켜보되 선택과 대화의 역할을 잊지 마세요."},
    {"name":"정의 (Justice)","symbol":"⚖️","keyword":"공정함 · 균형 · 솔직함",
     "meaning":"감정보다 사실과 균형을 살피려는 태도를 나타냅니다. 약속과 책임을 중요하게 여기며 불공평한 상황을 그냥 넘기지 않을 수 있습니다. 옳고 그름을 따지는 것과 상대의 감정을 이해하는 일을 함께 해보세요.",
     "love":"연애에서는 서로에게 공평한 관계, 솔직한 대화, 책임 있는 선택을 뜻합니다."},
    {"name":"매달린 사람 (The Hanged Man)","symbol":"🪢","keyword":"기다림 · 관점 전환 · 양보",
     "meaning":"잠시 멈추어 다른 관점에서 바라볼 필요가 있음을 보여 줍니다. 관계를 서두르기보다 상대의 입장을 이해하는 시간이 도움이 될 수 있습니다. 한쪽만 계속 양보하는 관계가 되지 않도록 주의하세요.",
     "love":"연애에서는 속도 조절과 관점의 변화가 필요함을 나타냅니다."},
    {"name":"죽음 (Death)","symbol":"🦋","keyword":"변화 · 정리 · 재출발",
     "meaning":"끝과 시작이 맞닿아 있는 변화의 카드입니다. 반드시 나쁜 일을 뜻하는 것은 아니며, 오래된 생각이나 관계 방식을 바꾸어야 할 때를 나타냅니다. 과거의 패턴을 반복하지 않는 것이 중요합니다.",
     "love":"연애에서는 관계의 단계 변화, 오래된 오해의 정리, 새로운 방식의 시작을 상징합니다."},
    {"name":"절제 (Temperance)","symbol":"🏺","keyword":"조화 · 조율 · 균형",
     "meaning":"서로 다른 성향을 섞어 균형을 찾는 카드입니다. 빠른 결론보다 대화와 조율을 통해 편안한 관계를 만들어 갈 수 있습니다. 차이를 없애려 하기보다 함께 맞춰 가는 태도가 중요합니다.",
     "love":"연애에서는 서로의 속도와 표현 방식을 조율하며 안정감을 쌓는 관계를 뜻합니다."},
    {"name":"악마 (The Devil)","symbol":"⛓️","keyword":"강한 끌림 · 집착 · 유혹",
     "meaning":"강렬한 끌림이나 쉽게 놓기 어려운 감정을 나타냅니다. 매력적인 관계일 수 있지만 불안, 질투, 의존이 커지지 않는지 살펴야 합니다. 서로의 선택과 경계를 존중하는 것이 중요합니다.",
     "love":"연애에서는 강한 호감과 동시에 관계의 균형을 점검해야 한다는 메시지를 줍니다."},
    {"name":"탑 (The Tower)","symbol":"⚡","keyword":"충격 · 진실 · 재정비",
     "meaning":"기존의 생각이나 기대가 흔들리며 현실을 다시 보게 되는 카드입니다. 불편한 대화가 필요할 수 있지만, 이를 통해 관계의 문제를 분명히 알 수 있습니다. 감정적으로 단정하기보다 사실을 확인해 보세요.",
     "love":"연애에서는 숨겨 둔 문제를 마주하고 관계의 기반을 점검하는 과정을 뜻합니다."},
    {"name":"별 (The Star)","symbol":"⭐","keyword":"희망 · 회복 · 진정성",
     "meaning":"마음의 여유와 희망, 솔직한 모습을 상징합니다. 서로에게 편안함을 주고 좋은 가능성을 발견할 수 있습니다. 다만 기대만 키우기보다 실제 행동과 꾸준함을 함께 살펴보세요.",
     "love":"연애에서는 자연스러운 호감, 신뢰 회복, 함께 성장할 가능성을 나타냅니다."},
    {"name":"달 (The Moon)","symbol":"🌕","keyword":"불확실함 · 상상 · 예민함",
     "meaning":"확실하지 않은 상황에서 걱정이나 상상이 커질 수 있음을 나타냅니다. 상대의 마음을 추측만으로 판단하지 말고 실제 말과 행동을 확인하는 것이 좋습니다.",
     "love":"연애에서는 설렘과 불안이 함께 있을 수 있음을 뜻합니다. 오해를 줄이는 솔직한 소통이 중요합니다."},
    {"name":"태양 (The Sun)","symbol":"☀️","keyword":"기쁨 · 솔직함 · 활력",
     "meaning":"밝고 솔직한 에너지, 함께 있을 때의 즐거움을 상징합니다. 감정을 숨기기보다 자연스럽게 표현할 때 관계가 편안해질 수 있습니다. 좋은 순간을 당연하게 여기지 않고 서로 고마움을 표현해 보세요.",
     "love":"연애에서는 즐거운 교감과 긍정적인 관계 분위기를 나타냅니다."},
    {"name":"심판 (Judgement)","symbol":"📯","keyword":"깨달음 · 재평가 · 결정",
     "meaning":"지나온 일을 돌아보고 중요한 결정을 내리는 카드입니다. 관계를 계속 발전시키려면 무엇이 필요한지 분명히 할 수 있습니다. 과거의 경험을 반복하기보다 배운 점을 활용해 보세요.",
     "love":"연애에서는 관계를 다시 바라보고 서로의 마음을 확인하는 시기를 뜻합니다."},
    {"name":"세계 (The World)","symbol":"🌍","keyword":"완성 · 성숙 · 통합",
     "meaning":"서로 다른 부분을 받아들이며 한 단계 성숙해지는 카드입니다. 관계에서 안정감과 만족감을 추구할 수 있습니다. 완벽함을 기대하기보다 함께 성장하는 과정을 소중히 여기세요.",
     "love":"연애에서는 조화와 성숙, 관계의 한 단계 발전을 상징합니다."}
]

POSITIONS = [
    ("첫 번째 카드 · 본인","현재의 연애 성향","당신이 관계에서 주로 보이는 태도와 첫인상"),
    ("두 번째 카드 · 본인","마음속 바람과 관계의 과제","당신이 연애에서 원하는 것과 주의할 점"),
    ("세 번째 카드 · 상대방","상대방의 연애 성향","상대가 관계에서 보일 수 있는 태도"),
    ("네 번째 카드 · 상대방","상대방의 마음과 관계의 과제","상대가 중요하게 여길 수 있는 것과 조율할 점"),
]

def get_card(name):
    return next(c for c in CARDS if c["name"] == name)

def build_reading(question, picked):
    cards = [get_card(n) for n in picked]
    a, b, c, d = cards
    return f"""
## 🌙 질문에 대한 타로 리딩
**질문:** {question}

### 1. 당신의 카드 — {a['name']}
<small>핵심 상징: {a['keyword']}</small>

{a['meaning']}

**연애에서의 해석:** {a['love']}

이 카드는 당신이 관계를 시작하거나 상대를 알아갈 때 어떤 태도를 보일 수 있는지 보여 줍니다. 특히 {a['keyword']}의 의미를 생각해 보세요. 이것은 고정된 성격 판정이 아니라, 현재 관계를 돌아보기 위한 하나의 관점입니다.

### 2. 당신의 내면 카드 — {b['name']}
<small>핵심 상징: {b['keyword']}</small>

{b['meaning']}

**연애에서의 해석:** {b['love']}

첫 번째 카드가 겉으로 드러나는 태도라면, 두 번째 카드는 당신이 관계에서 진짜로 바라는 것과 신경 써야 할 부분을 나타냅니다. 두 카드가 함께 말하는 핵심은 **{a['keyword']}와 {b['keyword']}의 균형**입니다.

### 3. 상대방의 카드 — {c['name']}
<small>핵심 상징: {c['keyword']}</small>

{c['meaning']}

**연애에서의 해석:** {c['love']}

이 카드는 상대방이 관계에서 보일 수 있는 태도를 상징합니다. 실제 상대의 마음을 확정하는 것은 아니므로, 현실에서의 말과 행동을 함께 살펴보세요.

### 4. 상대방의 내면 카드 — {d['name']}
<small>핵심 상징: {d['keyword']}</small>

{d['meaning']}

**연애에서의 해석:** {d['love']}

세 번째 카드가 상대의 관계 방식이라면, 네 번째 카드는 상대가 중요하게 여기는 감정이나 관계의 과제를 보여 줍니다. 핵심은 **{c['keyword']}와 {d['keyword']}의 조화**입니다.

### 💞 두 사람의 궁합 종합
당신 쪽에는 **{a['keyword']}**, 상대방 쪽에는 **{c['keyword']}**가 나타났습니다. 두 사람은 관계를 대하는 방식에서 서로 닮은 점도, 다르게 느낄 수 있는 점도 있을 수 있습니다.

당신의 내면을 나타내는 **{b['keyword']}**와 상대방의 내면을 나타내는 **{d['keyword']}**를 함께 보면, 관계가 편안해지기 위해서는 서로가 원하는 애정 표현과 개인적인 속도를 알아가는 과정이 중요합니다.

**잘 맞을 수 있는 부분:** 서로의 장점을 인정하고 각자 편안하게 느끼는 방식으로 소통한다면 좋은 시너지를 만들 수 있습니다. 특히 두 카드의 긍정적인 상징을 현실의 행동으로 연결하는 것이 중요합니다.

**주의하면 좋을 부분:** 마음을 추측하거나 한쪽이 일방적으로 맞추기 시작하면 오해가 생길 수 있습니다. 서운한 점은 쌓아 두기보다 차분하게 이야기하고, 서로의 경계를 존중해 보세요.

### 🔮 질문에 대한 결론
**두 사람이 잘 맞을 가능성을 알아보려면, 서로의 차이를 얼마나 편안하게 조율할 수 있는지가 핵심입니다.** 이번 카드 조합은 관계를 바라보는 하나의 상징적인 이야기입니다. 실제로 사귀게 될지, 얼마나 잘 맞을지는 카드가 결정하는 것이 아니라 두 사람이 주고받는 존중과 대화, 행동에 달려 있습니다.

### ✨ 현실에서 확인해 볼 질문
- 함께 있을 때 서로의 모습을 편안하게 드러낼 수 있나요?
- 연락이나 애정 표현의 방식이 다를 때 대화로 조율할 수 있나요?
- 한 사람만 노력하는 것이 아니라 서로 비슷한 정도로 관계에 참여하나요?
"""

def ai_reading(question, picked):
    try:
        api_key = st.secrets.get("OPENAI_API_KEY", "")
    except Exception:
        api_key = ""
    if not api_key:
        return None
    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key)
        card_details = []
        for i, name in enumerate(picked):
            card = get_card(name)
            pos = POSITIONS[i]
            card_details.append(
                f"{pos[0]} / {pos[1]}: {card['name']}, 상징={card['keyword']}, 의미={card['meaning']} 연애 해석={card['love']}"
            )
        prompt = f"""
너는 따뜻하고 섬세한 타로 리더다. 아래 네 장의 메이저 아르카나 카드만을 근거로 사용자의 연애 관계 질문에 한국어로 상세히 답한다.
타로는 오락과 자기성찰을 위한 상징 해석이며 미래, 상대의 실제 속마음, 운명을 사실처럼 단정하지 않는다.
카드별로 그림/상징의 키워드, 본인과 상대방의 성향, 두 사람의 강점, 갈등 가능성, 관계를 발전시키는 대화 방법을 구체적으로 설명한다.
마지막에는 질문에 직접 답하는 결론을 쓴다. 막연한 긍정이나 부정 대신 조건과 이유를 제시한다.
사용자 질문: {question}
카드:
{chr(10).join(card_details)}
"""
        response = client.responses.create(
            model="gpt-4.1-mini",
            input=prompt
        )
        return response.output_text
    except Exception as e:
        st.warning("AI 상세 풀이를 불러오지 못해 기본 카드 해석을 표시합니다.")
        return None



# ---------------------------
# 타로 연애 상담
# ---------------------------
with tab3:
    st.subheader("🌙 나만의 소울카드")
    st.markdown(
        '<p class="tarot-note">별빛 아래 펼쳐지는 네 장의 이야기. '
        '당신과 그 사람의 마음을 타로의 상징으로 들여다보세요.</p>',
        unsafe_allow_html=True
    )

    question = st.text_area(
        "💌 마음속 질문을 적어주세요",
        placeholder="예: 이 사람과 사귀게 된다면 우리는 잘 맞을까? "
                    "서로 어떤 점에서 끌리고, 어떤 점을 조심해야 할까?",
        height=100,
        key="tarot_question"
    )
    st.markdown(
        '<p class="tarot-note">연애 궁합, 썸의 흐름, 서로의 성향, '
        '관계에서 조심할 점 등 궁금한 내용을 자유롭게 적어주세요.</p>',
        unsafe_allow_html=True
    )

    if "tarot_picked" not in st.session_state:
        st.session_state.tarot_picked = []
    if "tarot_order" not in st.session_state:
        order = list(range(len(CARDS)))
        random.shuffle(order)
        st.session_state.tarot_order = order

    picked = st.session_state.tarot_picked
    st.markdown("---")
    st.markdown("### 🃏 네 장의 카드를 선택하세요")
    st.markdown(
        '<p class="tarot-note">카드는 모두 뒷면으로 놓여 있어요. '
        '원하는 카드를 순서대로 네 장 골라주세요. '
        '첫 두 장은 본인, 다음 두 장은 상대방의 카드입니다.</p>',
        unsafe_allow_html=True
    )

    if len(picked) < 4:
        step = len(picked)
        st.info(
            f"현재 선택: {step + 1}/4  ·  "
            f"{POSITIONS[step][0]} — {POSITIONS[step][1]}"
        )
    else:
        st.success("네 장의 카드가 모두 선택되었어요. 이제 두 사람의 이야기를 확인해 보세요.")

    # 22장의 카드를 4열로 배치
    for start in range(0, len(st.session_state.tarot_order), 4):
        row_indices = st.session_state.tarot_order[start:start + 4]
        cols = st.columns(4)
        for col, card_index in zip(cols, row_indices):
            card = CARDS[card_index]
            with col:
                st.markdown(
                    '<div class="tarot-back">✧<br>☾<br>✧</div>',
                    unsafe_allow_html=True
                )
                if card["name"] in picked:
                    st.button(
                        "선택 완료",
                        key=f"tarot_done_{card_index}",
                        disabled=True,
                        use_container_width=True
                    )
                elif len(picked) >= 4:
                    st.button(
                        "선택 마감",
                        key=f"tarot_closed_{card_index}",
                        disabled=True,
                        use_container_width=True
                    )
                else:
                    if st.button(
                        "이 카드 선택",
                        key=f"tarot_pick_{card_index}",
                        use_container_width=True
                    ):
                        st.session_state.tarot_picked.append(card["name"])
                        st.session_state.pop("tarot_show_result", None)
                        st.rerun()

    if picked:
        st.markdown("---")
        st.markdown("### 🌟 선택한 카드")
        chosen_cols = st.columns(4)
        for i, card_name in enumerate(picked):
            card = get_card(card_name)
            with chosen_cols[i]:
                st.markdown(
                    f"""
                    <div class="tarot-face">
                        <div class="symbol">{card['symbol']}</div>
                        <div class="name">{card['name']}</div>
                        <div class="keyword">{card['keyword']}</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                st.caption(POSITIONS[i][0])

    if len(picked) == 4:
        st.markdown("---")
        if st.button(
            "🌙 내 타로 리딩 확인하기",
            type="primary",
            use_container_width=True,
            key="tarot_read_button"
        ):
            if not question.strip():
                st.warning("먼저 궁금한 질문을 적어주세요.")
                st.session_state.tarot_show_result = False
            else:
                st.session_state.tarot_show_result = True

        if st.session_state.get("tarot_show_result", False) and question.strip():
            with st.spinner("네 장의 카드에 담긴 상징을 해석하고 있어요..."):
                reading = ai_reading(question.strip(), picked)

            st.markdown("---")
            st.markdown("## 🔮 두 사람의 타로 리딩")
            if reading:
                st.markdown(reading)
                st.caption(
                    "AI 타로 리딩은 선택한 카드의 상징을 바탕으로 생성한 "
                    "오락·자기성찰용 해석입니다."
                )
            else:
                st.markdown(
                    build_reading(question.strip(), picked),
                    unsafe_allow_html=True
                )
                st.caption(
                    "기본 카드 해석 모드입니다. OpenAI API를 연결하면 "
                    "질문과 카드 조합에 맞춘 더욱 풍부한 풀이를 이용할 수 있습니다."
                )

    st.markdown("---")
    st.markdown(
        '<p class="tarot-note">✦ 타로는 미래나 상대방의 실제 마음을 '
        '확정하는 도구가 아니라, 관계를 다른 시각으로 생각해 보는 '
        '오락·자기성찰 콘텐츠입니다. 실제 관계에서는 서로의 말과 행동, '
        '존중과 대화가 가장 중요해요.</p>',
        unsafe_allow_html=True
    )

    if st.button("↻ 타로 카드 다시 뽑기", use_container_width=True, key="tarot_reset"):
        st.session_state.tarot_picked = []
        new_order = list(range(len(CARDS)))
        random.shuffle(new_order)
        st.session_state.tarot_order = new_order
        st.session_state.pop("tarot_show_result", None)
        st.rerun()
