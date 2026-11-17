import streamlit as st
from datetime import date, datetime, timedelta

try:
    from korean_lunar_calendar import KoreanLunarCalendar
    LUNAR_AVAILABLE = True
except ImportError:
    LUNAR_AVAILABLE = False

st.set_page_config(
    page_title="우리 사이 | 사주 궁합",
    page_icon="💗",
    layout="centered",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
    .stApp { background: linear-gradient(180deg, #fff8fb 0%, #fbf8ff 100%); }
    .main .block-container { max-width: 900px; padding-top: 2rem; padding-bottom: 3rem; }
    h1, h2, h3 { color: #49334f; }
    div[data-testid="stMetric"] {
        background: white; border: 1px solid #f0dfeb; padding: 16px;
        border-radius: 16px;
    }
    .hero {
        padding: 28px 24px; border-radius: 22px; text-align: center;
        color: white; background: linear-gradient(120deg, #563d67, #a45c83);
        margin-bottom: 20px;
    }
    .hero h1 { color: white; margin-bottom: 8px; }
    .hero p { color: #fff0f7; margin-bottom: 0; }
    .note {
        background: #fff; border-left: 4px solid #bd7b9d; padding: 12px 16px;
        border-radius: 8px; color: #55485a; margin: 10px 0 18px 0;
    }
    .result-card {
        background: white; border: 1px solid #f0dfeb; border-radius: 16px;
        padding: 18px; margin: 8px 0;
    }
    .small-muted { color: #776d7b; font-size: 0.88rem; }
</style>
""", unsafe_allow_html=True)

# 천간·지지의 오행은 전통 명리학의 기본 대응표를 단순화해 사용합니다.
STEMS = ["갑", "을", "병", "정", "무", "기", "경", "신", "임", "계"]
BRANCHES = ["자", "축", "인", "묘", "진", "사", "오", "미", "신", "유", "술", "해"]
STEM_ELEMENT = {
    "갑": "목", "을": "목", "병": "화", "정": "화", "무": "토",
    "기": "토", "경": "금", "신": "금", "임": "수", "계": "수"
}
BRANCH_ELEMENT = {
    "자": "수", "축": "토", "인": "목", "묘": "목", "진": "토",
    "사": "화", "오": "화", "미": "토", "신": "금", "유": "금",
    "술": "토", "해": "수"
}
ELEMENTS = ["목", "화", "토", "금", "수"]
ELEMENT_DESC = {
    "목": "성장과 시작을 상징해요. 새로운 시도와 발전을 중요하게 여기는 이미지입니다.",
    "화": "표현과 열정을 상징해요. 활기와 감정 표현을 중요하게 여기는 이미지입니다.",
    "토": "균형과 안정감을 상징해요. 꾸준함과 신뢰를 중요하게 여기는 이미지입니다.",
    "금": "원칙과 정돈을 상징해요. 기준과 책임감을 중요하게 여기는 이미지입니다.",
    "수": "유연함과 지혜를 상징해요. 생각과 관찰, 적응을 중요하게 여기는 이미지입니다."
}

def sexagenary(index):
    return STEMS[index % 10] + BRANCHES[index % 12]

def to_solar_date(birth_date, calendar_type, is_leap):
    if calendar_type == "양력":
        return birth_date
    if not LUNAR_AVAILABLE:
        raise ValueError("음력 변환 기능을 사용하려면 korean-lunar-calendar 라이브러리가 필요합니다.")
    cal = KoreanLunarCalendar()
    ok = cal.setLunarDate(birth_date.year, birth_date.month, birth_date.day, is_leap)
    if not ok:
        raise ValueError("입력한 음력 날짜를 변환할 수 없습니다. 날짜와 윤달 여부를 확인해 주세요.")
    return date(cal.solarYear, cal.solarMonth, cal.solarDay)

def get_pillars(solar_date, birth_time):
    # 연주는 입춘 전후를 단순 보정합니다. 절기 시각을 계산하는 정밀 만세력은 아닙니다.
    year_for_pillar = solar_date.year if (solar_date.month, solar_date.day) >= (2, 4) else solar_date.year - 1
    year_index = (year_for_pillar - 1984) % 60
    year_pillar = sexagenary(year_index)

    # 월주는 절입일의 실제 시각 대신 양력 날짜 구간을 근사해 계산합니다.
    # 2월 초를 인월로 보고 월지를 순환시킵니다.
    month = solar_date.month
    if solar_date.day < 5:
        month -= 1
    if month <= 0:
        month = 12
    month_branch_index = (month - 2) % 12
    month_branch = BRANCHES[(2 + month_branch_index) % 12]
    year_stem_index = year_index % 10
    # 오호둔 월간법의 간략 적용
    first_month_stem = ((year_stem_index % 5) * 2 + 2) % 10
    month_stem = STEMS[(first_month_stem + month_branch_index) % 10]
    month_pillar = month_stem + month_branch

    # 2000-01-07을 갑자일 기준일로 삼아 60갑자를 계산합니다.
    anchor = date(2000, 1, 7)
    day_index = (solar_date - anchor).days % 60
    day_pillar = sexagenary(day_index)

    if birth_time is None:
        hour_pillar = None
    else:
        hour = birth_time.hour
        branch_index = ((hour + 1) // 2) % 12
        hour_branch = BRANCHES[branch_index]
        day_stem_index = day_index % 10
        first_hour_stem = (day_stem_index % 5) * 2
        hour_stem = STEMS[(first_hour_stem + branch_index) % 10]
        hour_pillar = hour_stem + hour_branch

    pillars = {"년주": year_pillar, "월주": month_pillar, "일주": day_pillar}
    if hour_pillar:
        pillars["시주"] = hour_pillar
    return pillars

def analyze_person(name, birth_date, calendar_type, is_leap, birth_time):
    solar = to_solar_date(birth_date, calendar_type, is_leap)
    pillars = get_pillars(solar, birth_time)
    counts = {e: 0 for e in ELEMENTS}
    for pillar in pillars.values():
        counts[STEM_ELEMENT[pillar[0]]] += 1
        counts[BRANCH_ELEMENT[pillar[1]]] += 1
    if birth_time is None:
        # 시주를 모르는 경우 실제 오행 개수와 혼동하지 않도록 별도 표시
        pass
    dominant = max(counts, key=counts.get)
    missing = [e for e, n in counts.items() if n == 0]
    return {
        "name": name, "birth": birth_date, "solar": solar, "calendar": calendar_type,
        "pillars": pillars, "counts": counts, "dominant": dominant, "missing": missing,
        "time_known": birth_time is not None
    }

def compatibility_score(a, b):
    # 교육·오락용으로 만든 간단한 규칙 점수이며 전통 명리학의 정식 궁합 점수가 아닙니다.
    score = 68
    if a["pillars"]["일주"][1] == b["pillars"]["일주"][1]:
        score += 9
    if a["dominant"] == b["dominant"]:
        score += 4
    else:
        score += 6
    common = sum(1 for e in ELEMENTS if a["counts"][e] > 0 and b["counts"][e] > 0)
    score += (common - 3) * 2
    if a["pillars"]["년주"][1] == b["pillars"]["년주"][1]:
        score += 3
    return max(45, min(95, score))

def relationship_copy(kind, score):
    if kind == "커플 희망":
        title = "연애 가능성 참고 점수"
        if score >= 80:
            msg = "서로의 차이를 알아가며 친밀감을 쌓아볼 만한 조합으로 풀이할 수 있어요. 다만 실제 관계는 대화와 상호 존중이 더 중요해요."
        elif score >= 65:
            msg = "서로 알아갈 여지가 있는 조합이에요. 서두르기보다 공통 관심사와 편안한 대화를 통해 관계를 만들어 가는 것이 좋아요."
        else:
            msg = "관계의 속도나 표현 방식이 다를 수 있다는 관점으로 살펴보세요. 점수와 관계의 가능성은 같지 않으며, 서로를 알아가는 과정이 중요해요."
    elif kind == "커플":
        title = "커플 궁합 참고 점수"
        msg = "점수는 두 사람의 사주 요소를 단순 비교한 오락용 지표예요. 실제 관계의 만족도는 서로의 대화, 신뢰, 배려와 함께 만들어집니다."
    else:
        title = "우정 궁합 참고 점수"
        msg = "서로 다른 성향이 좋은 보완점이 될 수도 있어요. 편안한 우정을 위해서는 차이를 존중하고 솔직하게 소통하는 것이 중요합니다."
    return title, msg

def attachment_result(anxiety, avoidance):
    # 자기보고 문항에 따른 비진단적 참고 분류
    if anxiety <= 2.5 and avoidance <= 2.5:
        return "안정형 경향", "관계에서 신뢰를 표현하고, 친밀함과 개인 시간을 비교적 편안하게 조율하는 편일 수 있어요."
    if anxiety >= 3.5 and avoidance < 3.5:
        return "불안형 경향", "상대의 반응이나 관계의 변화에 민감할 수 있어요. 마음이 불편할 때 추측하기보다 필요한 것을 차분히 말해보세요."
    if avoidance >= 3.5 and anxiety < 3.5:
        return "회피형 경향", "혼자 생각할 시간이 중요하고 감정을 표현하기까지 시간이 걸릴 수 있어요. 필요한 거리와 소통 방식을 미리 공유해보세요."
    if anxiety >= 3.5 and avoidance >= 3.5:
        return "불안·회피 혼합 경향", "가까워지고 싶은 마음과 거리를 두고 싶은 마음이 함께 나타날 수 있어요. 상황에 따라 반응이 달라질 수 있습니다."
    return "뚜렷한 한 유형으로 분류하기 어려움", "애착은 상황과 관계에 따라 달라질 수 있어요. 몇 가지 응답만으로 유형을 단정하지 않는 것이 좋습니다."

def person_form(label, key):
    st.subheader(label)
    name = st.text_input("이름 또는 별명", value=("나" if key == "me" else "상대방"), key=f"{key}_name")
    calendar_type = st.radio("달력", ["양력", "음력"], horizontal=True, key=f"{key}_calendar")
    birth_date = st.date_input("생년월일", value=date(2000, 1, 1), min_value=date(1900, 1, 1),
                               max_value=date.today(), key=f"{key}_date")
    is_leap = False
    if calendar_type == "음력":
        is_leap = st.checkbox("윤달", key=f"{key}_leap")
    time_choice = st.radio("태어난 시간", ["시간 선택", "모름"], horizontal=True, key=f"{key}_time_choice")
    birth_time = None
    if time_choice == "시간 선택":
        birth_time = st.time_input("태어난 시간 입력", value=datetime.strptime("12:00", "%H:%M").time(), key=f"{key}_time")
    return name.strip() or label, birth_date, calendar_type, is_leap, birth_time

def attachment_questions(person_label, key):
    st.markdown(f"**{person_label}의 관계 성향 질문**")
    st.caption("각 문항에서 평소 자신과 가까운 정도를 선택해 주세요. 1점은 전혀 그렇지 않음, 5점은 매우 그러함입니다.")
    q1 = st.slider(f"{person_label}: 답장이 늦거나 반응이 달라지면 관계가 불안해진다", 1, 5, 3, key=f"{key}_q1")
    q2 = st.slider(f"{person_label}: 속상한 일이 있어도 혼자 해결하고 싶고 감정을 말하기 어렵다", 1, 5, 3, key=f"{key}_q2")
    q3 = st.slider(f"{person_label}: 갈등이 생기면 상대와 대화하며 해결하는 편이다", 1, 5, 3, key=f"{key}_q3")
    anxiety = (q1 + (6 - q3)) / 2
    avoidance = (q2 + (6 - q3)) / 2
    return anxiety, avoidance

st.markdown("""
<div class="hero">
  <h1>💗 우리 사이</h1>
  <p>두 사람의 사주와 관계 성향으로 살펴보는 궁합</p>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="note">이 앱은 전통 사주 요소를 단순화한 오락·자기성찰용 서비스입니다. 실제 미래, 연애 성공 여부, 성격 또는 심리 상태를 과학적으로 예측하거나 진단하지 않습니다.</div>', unsafe_allow_html=True)

with st.form("couple_form"):
    st.subheader("1. 어떤 관계인가요?")
    relation = st.radio("관계 유형", ["커플", "커플 희망", "친구"], horizontal=True)
    st.divider()
    st.subheader("2. 두 사람의 출생 정보")
    left, right = st.columns(2)
    with left:
        me_data = person_form("나의 정보", "me")
    with right:
        other_data = person_form("상대방 정보", "other")
    st.divider()
    st.subheader("3. 관계 성향 알아보기")
    st.caption("애착 유형은 출생 정보나 사주로 판단할 수 없으므로, 아래 자기응답을 별도로 반영합니다.")
    with st.expander("나의 관계 성향 질문", expanded=False):
        me_attach = attachment_questions("나", "me_attach")
    with st.expander("상대방의 관계 성향 질문", expanded=False):
        other_attach = attachment_questions("상대방", "other_attach")
    submitted = st.form_submit_button("💞 우리 궁합 알아보기", use_container_width=True)

if submitted:
    try:
        me = analyze_person(*me_data)
        other = analyze_person(*other_data)
        score = compatibility_score(me, other)
        st.session_state["result"] = {
            "relation": relation, "me": me, "other": other, "score": score,
            "me_attach": me_attach, "other_attach": other_attach
        }
    except Exception as e:
        st.error(f"입력 정보를 처리하지 못했습니다: {e}")

if "result" in st.session_state:
    r = st.session_state["result"]
    me, other, score, relation = r["me"], r["other"], r["score"], r["relation"]
    st.divider()
    st.markdown("## ✨ 두 사람의 궁합 결과")
    title, desc = relationship_copy(relation, score)
    st.markdown(f'<div class="result-card"><div class="small-muted">{title}</div><h1 style="text-align:center;color:#9b527b;font-size:3rem;margin:8px 0;">{score}%</h1><p style="text-align:center;">{desc}</p></div>', unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    for col, person in [(c1, me), (c2, other)]:
        with col:
            st.markdown(f"### {person['name']}")
            st.write(f"**양력 환산일:** {person['solar'].isoformat()}")
            st.write(f"**오행에서 두드러진 요소:** {person['dominant']}")
            for label, pillar in person["pillars"].items():
                st.write(f"- {label}: **{pillar}**")
            if not person["time_known"]:
                st.caption("태어난 시간을 몰라 시주는 제외했습니다.")

    st.markdown("### 🌿 오행 구성 비교")
    cols = st.columns(5)
    for col, element in zip(cols, ELEMENTS):
        with col:
            st.metric(element, f"{me['counts'][element]} : {other['counts'][element]}")
    st.caption("각 숫자는 계산에 포함된 천간·지지에서 해당 오행이 나온 횟수입니다. 태어난 시간을 모르면 6개 요소만 집계합니다.")
    common = [e for e in ELEMENTS if me["counts"][e] > 0 and other["counts"][e] > 0]
    st.markdown("### 💞 오행 궁합 풀이")
    st.write(f"두 사람 모두에게 나타나는 오행은 **{', '.join(common) if common else '없음'}**입니다.")
    st.write(f"{me['name']}에게 두드러지는 오행은 **{me['dominant']}**, {other['name']}에게 두드러지는 오행은 **{other['dominant']}**입니다.")
    st.write(f"- {me['name']}: {ELEMENT_DESC[me['dominant']]}")
    st.write(f"- {other['name']}: {ELEMENT_DESC[other['dominant']]}")
    if me["dominant"] == other["dominant"]:
        st.write("비슷한 관심사나 반응 방식을 공유한다고 해석해 볼 수 있지만, 비슷함이 항상 잘 맞는다는 뜻은 아닙니다.")
    else:
        st.write("서로 다른 강점이 보완점이 될 수 있습니다. 다만 차이를 이해하고 조율하는 대화가 필요합니다.")

    st.markdown("### 🌙 관계에서 살펴볼 점")
    day_a, day_b = me["pillars"]["일주"], other["pillars"]["일주"]
    if day_a[1] == day_b[1]:
        st.write("두 사람의 일지 지지가 같습니다. 전통적인 상징 풀이에서는 비슷한 정서적 리듬이나 익숙함으로 해석하기도 합니다.")
    else:
        st.write("두 사람의 일지 지지가 다릅니다. 서로 다른 생활 리듬이나 표현 방식을 알아가는 것이 관계에 도움이 될 수 있습니다.")
    if me["dominant"] != other["dominant"]:
        st.write("오행의 중심 요소가 다르므로, 한쪽의 방식만 정답으로 여기지 않고 서로의 차이를 조율하는 태도가 중요합니다.")
    else:
        st.write("오행의 중심 요소가 같으므로 공통점이 친밀감을 만드는 데 도움이 될 수 있습니다. 반대로 비슷한 약점이 반복되지 않도록 살펴보세요.")

    st.markdown("### 🫶 관계 성향 참고 결과")
    a1, d1 = r["me_attach"]
    a2, d2 = r["other_attach"]
    type1, explain1 = attachment_result(a1, d1)
    type2, explain2 = attachment_result(a2, d2)
    ca, cb = st.columns(2)
    with ca:
        st.markdown(f"**{me['name']}**")
        st.subheader(type1)
        st.write(explain1)
    with cb:
        st.markdown(f"**{other['name']}**")
        st.subheader(type2)
        st.write(explain2)
    st.caption("이 결과는 앱 안의 짧은 자기응답을 바탕으로 한 비진단적 참고 분류입니다. 심리검사나 전문가의 평가를 대신하지 않습니다.")

    st.markdown("### 💌 두 사람에게 전하는 조언")
    st.write("궁합 점수는 관계의 성패를 정해 주지 않습니다. 서로의 감정과 경계를 존중하고, 불편한 점은 비난보다 구체적인 요청으로 표현해 보세요. 좋은 관계는 사주 점수보다 두 사람이 함께 만들어 가는 행동에 달려 있습니다.")

    with st.expander("📌 계산 방식과 정확도 안내"):
        st.write("현재 버전은 양력·음력 날짜 변환과 간단한 간지·오행 계산을 바탕으로 구성한 프로토타입입니다.")
        st.write("월주와 연주 경계는 절기 시각을 정밀하게 계산하지 않고 양력 날짜로 근사합니다. 따라서 전문 만세력과 결과가 다를 수 있습니다.")
        st.write("궁합 퍼센트는 앱 내부 규칙으로 산출한 재미용 점수이며, 실제 연애 성사 확률이나 우정의 질을 의미하지 않습니다.")
        st.write("이름과 생년월일 등 입력 정보는 별도 데이터베이스에 저장하지 않습니다. 단, Streamlit 호스팅 환경의 기본 로그·세션 처리 정책은 별도로 적용될 수 있습니다.")

st.markdown("---")
st.caption("우리 사이 · 사주 궁합 프로토타입 | 중요한 관계의 결정은 점수나 운세보다 서로의 의사와 경험을 우선해 주세요.")
