import streamlit as st
from datetime import date, time
import hashlib
from PIL import Image

st.set_page_config(page_title="두 사람의 사주 궁합", page_icon="🔮", layout="wide")

st.title("🔮 두 사람의 사주 · 궁합 연구소")
st.caption("생년월일을 바탕으로 즐기는 전통 명리·별자리 스타일의 엔터테인먼트 앱")

st.info(
    "안내: 이 앱의 점수와 풀이는 재미를 위한 참고 콘텐츠이며 과학적 예측이나 실제 사주 감정이 아닙니다. "
    "양력 기준의 간단한 생년월일 해석으로, 음력 변환·절기·출생지·정밀한 만세력 계산은 반영하지 않습니다. "
    "애착 유형은 생년월일이나 사진으로 판단할 수 없어 간단한 자기보고 응답으로만 참고 표시합니다."
)

def zodiac(d):
    signs = [
        ("염소자리", (1, 1), (1, 19)), ("물병자리", (1, 20), (2, 18)),
        ("물고기자리", (2, 19), (3, 20)), ("양자리", (3, 21), (4, 19)),
        ("황소자리", (4, 20), (5, 20)), ("쌍둥이자리", (5, 21), (6, 20)),
        ("게자리", (6, 21), (7, 22)), ("사자자리", (7, 23), (8, 22)),
        ("처녀자리", (8, 23), (9, 22)), ("천칭자리", (9, 23), (10, 22)),
        ("전갈자리", (10, 23), (11, 21)), ("사수자리", (11, 22), (12, 21)),
        ("염소자리", (12, 22), (12, 31))
    ]
    md = (d.month, d.day)
    for name, start, end in signs:
        if start <= md <= end:
            return name
    return "염소자리"

def chinese_zodiac(year):
    animals = ["쥐", "소", "호랑이", "토끼", "용", "뱀", "말", "양", "원숭이", "닭", "개", "돼지"]
    return animals[(year - 4) % 12] + "띠"

def element(year):
    # 간단한 연도 끝자리 기반 오행 참고표(정밀 사주 계산 아님)
    return {0:"금", 1:"금", 2:"수", 3:"수", 4:"목", 5:"목", 6:"화", 7:"화", 8:"토", 9:"토"}[year % 10]

def stable_score(seed, low=58, high=96):
    n = int(hashlib.sha256(seed.encode("utf-8")).hexdigest()[:8], 16)
    return low + n % (high - low + 1)

def describe_person(label, dob, birth_time):
    return {
        "별자리": zodiac(dob),
        "띠": chinese_zodiac(dob.year),
        "연도 오행 참고": element(dob.year) + " 기운",
        "생일 수비학 숫자": 1 + ((dob.year + dob.month + dob.day - 1) % 9),
        "태어난 시간": birth_time.strftime("%H:%M") if birth_time else "모름 / 입력하지 않음"
    }

def attachment_quiz(label):
    st.markdown(f"**{label}의 관계 성향 자기 점검**")
    st.caption("각 문항에서 평소 자신에게 더 가까운 응답을 골라 주세요. 진단이 아니라 대화를 위한 참고입니다.")
    q1 = st.radio(f"{label} · 상대의 답장이 늦으면?", ["크게 신경 쓰지 않는다", "걱정되거나 확인하고 싶어진다", "부담스럽고 혼자 있고 싶어진다"], key=f"{label}q1")
    q2 = st.radio(f"{label} · 갈등이 생기면?", ["대화로 차분히 풀려고 한다", "상대가 나를 싫어할까 봐 불안해진다", "일단 거리를 두고 싶어진다"], key=f"{label}q2")
    q3 = st.radio(f"{label} · 친밀해질수록?", ["가까움과 개인 시간을 균형 있게 유지한다", "상대의 애정 확인이 더 필요해진다", "독립적인 공간이 더 중요해진다"], key=f"{label}q3")
    anxious = sum(x in [q1, q2, q3] for x in [
        "걱정되거나 확인하고 싶어진다", "상대가 나를 싫어할까 봐 불안해진다", "상대의 애정 확인이 더 필요해진다"
    ])
    avoidant = sum(x in [q1, q2, q3] for x in [
        "부담스럽고 혼자 있고 싶어진다", "일단 거리를 두고 싶어진다", "독립적인 공간이 더 중요해진다"
    ])
    secure = 3 - anxious - avoidant
    if anxious > avoidant and anxious > secure:
        return "불안 성향 응답이 상대적으로 많음"
    if avoidant > anxious and avoidant > secure:
        return "회피 성향 응답이 상대적으로 많음"
    if secure >= anxious and secure >= avoidant:
        return "안정 성향 응답이 상대적으로 많음"
    return "혼합된 응답"

def extra_content(topic, mode, a, b):
    content = {
        "이상형": (
            f"{a}은(는) 자신의 관심사를 존중하고 편안하게 소통하는 사람을 이상형의 기준으로 생각해 볼 수 있어요. "
            f"{b}은(는) 서로의 생활 방식과 속도를 존중하는 관계가 잘 맞는지 대화해 보세요. "
            "실제 이상형은 생년월일보다 각자의 경험과 가치관에 따라 달라집니다."
        ),
        "데이트 방법": "함께 해보고 싶은 활동을 각자 하나씩 고른 뒤 번갈아 계획해 보세요. 조용한 산책·전시 관람·보드게임처럼 대화와 공동 경험이 자연스럽게 생기는 활동이 좋습니다.",
        "서로의 관계에서 주의할 점": "상대의 마음을 추측해서 결론 내리기보다 직접 물어보세요. 연락 빈도, 혼자 보내는 시간, 갈등을 풀 때 필요한 시간을 미리 이야기하면 오해를 줄일 수 있습니다.",
        "인연 정도": "이 항목은 운명이나 미래를 판정하지 않습니다. 서로에게 시간을 쓰고 약속을 지키며 신뢰를 쌓는 정도가 관계의 깊이를 만들어 갑니다.",
        "현재 친밀감 정도": "현재 친밀감은 생년월일만으로 알 수 없습니다. 최근 서로 먼저 연락하는지, 편하게 고민을 나누는지, 함께 있을 때 존중받는지를 기준으로 두 사람이 직접 평가해 보세요.",
        "애정 정도": "애정은 점수로 확정할 수 없습니다. 말과 행동이 일치하는지, 서로의 경계를 존중하는지, 어려울 때 대화할 수 있는지를 살펴보세요.",
        "재회 가능성": "재회 여부를 사주나 점수로 예측할 수는 없습니다. 헤어진 이유가 해결 가능한지, 두 사람 모두 다시 관계를 원하고 있는지, 이전의 문제를 바꿀 구체적인 행동이 있는지가 더 중요합니다."
    }
    st.write(content[topic])

tab1, tab2 = st.tabs(["💞 생년월일 궁합", "🖼️ 사진 기반 관상 콘텐츠"])

with tab1:
    st.subheader("1. 관계 유형 선택")
    mode = st.radio("두 사람의 관계는 어떤 상황인가요?", ["커플", "커플 희망", "친구"], horizontal=True)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("### 나의 정보")
        name1 = st.text_input("이름 또는 별명", "나", key="name1")
        dob1 = st.date_input("생년월일 (양력)", value=date(2008, 1, 1), min_value=date(1900,1,1), max_value=date.today(), key="dob1")
        unknown1 = st.checkbox("태어난 시간 모름", value=True, key="unknown1")
        bt1 = None if unknown1 else st.time_input("태어난 시간", value=time(12,0), key="bt1")
    with c2:
        st.markdown("### 상대방 정보")
        name2 = st.text_input("상대방 이름 또는 별명", "상대방", key="name2")
        dob2 = st.date_input("상대방 생년월일 (양력)", value=date(2008, 1, 1), min_value=date(1900,1,1), max_value=date.today(), key="dob2")
        unknown2 = st.checkbox("상대방 태어난 시간 모름", value=True, key="unknown2")
        bt2 = None if unknown2 else st.time_input("상대방 태어난 시간", value=time(12,0), key="bt2")

    st.markdown("### 2. 관계 성향 자기 점검")
    st.caption("생년월일이나 얼굴 사진으로 불안형·회피형·안정형을 판별할 수 없으므로, 각자 직접 답한 내용만 요약합니다.")
    with st.expander(f"{name1 or '나'}의 문항", expanded=False):
        att1 = attachment_quiz("나")
    with st.expander(f"{name2 or '상대방'}의 문항", expanded=False):
        att2 = attachment_quiz("상대방")

    if st.button("✨ 궁합 풀이 보기", type="primary", use_container_width=True):
        if dob1 == dob2:
            st.caption("두 생년월일이 같습니다. 아래 결과는 오락용 조합 점수입니다.")
        p1 = describe_person(name1, dob1, bt1)
        p2 = describe_person(name2, dob2, bt2)
        seed = f"{dob1.isoformat()}|{dob2.isoformat()}|{mode}"
        score = stable_score(seed)
        st.divider()
        st.subheader("3. 두 사람의 기본 정보")
        left, right = st.columns(2)
        with left:
            st.markdown(f"**{name1 or '나'}**")
            for k,v in p1.items(): st.write(f"- {k}: {v}")
            st.write(f"- 관계 성향 자기 점검: {att1}")
        with right:
            st.markdown(f"**{name2 or '상대방'}**")
            for k,v in p2.items(): st.write(f"- {k}: {v}")
            st.write(f"- 관계 성향 자기 점검: {att2}")

        st.subheader("4. 궁합 요약")
        score_label = "커플 궁합 참고 점수" if mode == "커플" else ("커플 발전 가능성 참고 점수" if mode == "커플 희망" else "우정 궁합 참고 점수")
        st.metric(score_label, f"{score}%")
        st.progress(score / 100)
        st.caption("이 퍼센트는 생년월일을 재료로 만든 임의의 오락용 점수이며, 실제 연애 성사·우정·관계의 미래 확률이 아닙니다.")
        st.markdown("**성향 조합 풀이**")
        st.write(f"{name1 or '나'}은(는) {p1['별자리']} · {p1['띠']}띠, {name2 or '상대방'}은(는) {p2['별자리']} · {p2['띠']}띠로 표시됩니다.")
        st.write("서로의 차이를 단점으로 단정하기보다 의사소통 방식과 개인 시간을 어떻게 맞출지 이야기해 보세요. 생년월일만으로 성격, 애정의 크기, 운명적인 인연을 확정할 수는 없습니다.")
        st.markdown("**관계에서 함께 확인할 질문**")
        st.write("- 연락은 어느 정도 빈도가 서로 편안한가요?")
        st.write("- 서운한 일이 생겼을 때 바로 이야기할까요, 생각할 시간을 가진 뒤 이야기할까요?")
        st.write("- 서로의 취미와 친구 관계, 개인 시간을 어떻게 존중할까요?")
        st.session_state["result_ready"] = True
        st.session_state["last_names"] = (name1 or "나", name2 or "상대방")
        st.session_state["last_mode"] = mode

    if st.session_state.get("result_ready"):
        n1, n2 = st.session_state.get("last_names", ("나","상대방"))
        st.divider()
        st.subheader("5. 더 궁금한 내용")
        topics = ["이상형", "데이트 방법", "서로의 관계에서 주의할 점", "인연 정도", "현재 친밀감 정도", "애정 정도", "재회 가능성"]
        selected = st.multiselect("궁금한 항목을 선택하세요.", topics)
        for topic in selected:
            with st.expander(topic, expanded=True):
                extra_content(topic, st.session_state.get("last_mode","커플"), n1, n2)

with tab2:
    st.subheader("🖼️ 사진으로 보는 관상 콘텐츠")
    st.warning(
        "얼굴 사진만으로 성격, 애착 유형, 연애 성향, 궁합 또는 미래를 알아낼 수 있다는 과학적 근거는 없습니다. "
        "따라서 이 기능은 얼굴을 평가하거나 개인의 성격을 추정하지 않고, 사진을 올려 두 사람이 함께 대화할 수 있는 가벼운 전통문화·자기성찰 콘텐츠를 제공합니다."
    )
    col1, col2 = st.columns(2)
    with col1:
        photo1 = st.file_uploader("나의 사진 업로드", type=["png","jpg","jpeg"], key="photo1")
        if photo1:
            img1 = Image.open(photo1)
            st.image(img1, caption="업로드한 사진", use_container_width=True)
    with col2:
        photo2 = st.file_uploader("상대방 사진 업로드", type=["png","jpg","jpeg"], key="photo2")
        if photo2:
            img2 = Image.open(photo2)
            st.image(img2, caption="업로드한 사진", use_container_width=True)
    if st.button("🌿 관상 문화 콘텐츠 열기", use_container_width=True):
        if not photo1 or not photo2:
            st.error("두 사람의 사진을 모두 업로드해 주세요.")
        else:
            st.success("두 장의 사진이 업로드되었습니다.")
            st.markdown("### 두 사람이 함께 이야기해 볼 주제")
            st.write("전통 관상은 얼굴의 특징과 운명을 연결하던 옛 문화의 한 형태입니다. 현대 과학으로 검증된 성격 분석법은 아니므로, 아래 질문을 대화의 소재로만 활용해 보세요.")
            st.write("1. 서로의 첫인상과 실제 모습은 어떤 점에서 달랐나요?")
            st.write("2. 함께 있을 때 가장 편안하다고 느끼는 순간은 언제인가요?")
            st.write("3. 서로에게 고마웠던 행동 한 가지씩을 이야기해 보세요.")
            st.caption("업로드한 이미지를 분석해 성격이나 운명을 판정하지 않습니다. 사진은 이 앱의 관상 콘텐츠를 위한 입력 예시로만 화면에 표시됩니다.")

st.divider()
st.caption("개인정보 안내: 사진과 생년월일을 공개된 곳에 공유하지 마세요. 이 예제 앱은 외부 AI 분석 API로 사진을 전송하지 않습니다.")

import streamlit as st
import random
from datetime import datetime

st.set_page_config(
    page_title="나만의 소울카드",
    page_icon="🌙",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# -----------------------------
# 카드 데이터: 메이저 아르카나 22장
# -----------------------------
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

# -----------------------------
# 디자인
# -----------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Gowun+Batang:wght@400;700&family=Noto+Sans+KR:wght@300;400;500;700&display=swap');
html, body, [class*="css"] { font-family: 'Noto Sans KR', sans-serif; }
.stApp {
    background:
      radial-gradient(circle at 12% 10%, rgba(255,255,255,.55) 1px, transparent 2px),
      radial-gradient(circle at 83% 16%, rgba(255,220,140,.65) 1px, transparent 2px),
      radial-gradient(circle at 35% 38%, rgba(255,255,255,.45) 1px, transparent 2px),
      radial-gradient(circle at 92% 63%, rgba(255,255,255,.5) 1px, transparent 2px),
      linear-gradient(155deg, #210d3e 0%, #38145d 48%, #17103d 100%);
    background-size: 180px 180px, 220px 220px, 260px 260px, 200px 200px, cover;
    color: #fff7ff;
}
.block-container { max-width: 1120px; padding-top: 2rem; padding-bottom: 4rem; }
h1,h2,h3 { font-family: 'Gowun Batang', serif !important; color: #fff0ca !important; }
.hero { text-align:center; padding: 2.1rem 1rem 1.4rem; }
.hero h1 { font-size: clamp(2rem, 5vw, 3.4rem); letter-spacing: .08em; margin-bottom:.3rem; }
.hero p { color:#ddc9ef; line-height:1.9; font-size:1rem; }
.moon { color:#f6d77c; font-size:2rem; letter-spacing:.8rem; }
.panel {
    background: rgba(30, 13, 58, .78);
    border: 1px solid rgba(231,204,255,.22);
    border-radius: 22px; padding: 1.35rem 1.5rem;
    box-shadow: 0 12px 36px rgba(8,3,25,.25);
    margin: 1rem 0;
}
.small-note { color:#cbb9df; font-size:.88rem; line-height:1.8; }
.role-pill {
    display:inline-block; border:1px solid #b99ad9; color:#f7e9ff;
    padding:.28rem .7rem; border-radius:30px; font-size:.8rem; margin:.15rem;
}
div.stButton > button {
    background: linear-gradient(145deg,#65408e,#3b205f);
    color:#fff5dc; border:1px solid #c8a5e8; border-radius:14px;
    min-height:3rem; width:100%; transition:.2s;
}
div.stButton > button:hover { border-color:#ffe29b; color:#ffe29b; transform:translateY(-2px); }
div.stButton > button:disabled { opacity:.38; }
.stTextArea textarea {
    background:rgba(255,255,255,.94)!important; color:#29133f!important;
    border-radius:13px!important;
}
.tarot-back {
    text-align:center; padding:1.15rem .4rem; border-radius:14px;
    border:1px solid #d6b4e9; background:
      radial-gradient(circle at center,rgba(255,220,150,.14),transparent 55%),
      linear-gradient(145deg,#563078,#241342);
    color:#f8e7b8; font-size:1.8rem; min-height:90px;
}
.tarot-face {
    border:2px solid #e9c879; border-radius:16px; padding:1rem .7rem;
    text-align:center; background:linear-gradient(155deg,#fff2cf,#d8b8e6);
    color:#32164d; min-height:170px; box-shadow:0 8px 20px #10051e66;
}
.tarot-face .symbol { font-size:2.6rem; margin:.45rem; }
.tarot-face .name { font-family:'Gowun Batang',serif; font-weight:bold; font-size:.95rem; }
.tarot-face .keyword { font-size:.72rem; margin-top:.4rem; color:#67447c; }
div[data-testid="stMarkdownContainer"] p { line-height:1.85; }
hr { border-color:rgba(231,204,255,.22); }
footer {visibility:hidden;}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
  <div class="moon">☾ ✧ ☽</div>
  <h1>나만의 소울카드</h1>
  <p>별빛 아래 펼쳐지는 네 장의 이야기<br>
  당신과 그 사람의 마음을 타로의 상징으로 들여다보세요.</p>
</div>
""", unsafe_allow_html=True)

if "picked" not in st.session_state:
    st.session_state.picked = []
if "deck_order" not in st.session_state:
    order = list(range(len(CARDS)))
    random.shuffle(order)
    st.session_state.deck_order = order

st.markdown('<div class="panel">', unsafe_allow_html=True)
st.markdown("### ✍️ 마음속 질문을 적어주세요")
question = st.text_area(
    "질문",
    placeholder="예: 이 사람과 사귀게 된다면 우리는 잘 맞을까? 서로 어떤 점에서 끌리고, 어떤 점을 조심해야 할까?",
    height=95,
    label_visibility="collapsed"
)
st.markdown('<div class="small-note">연애 궁합, 썸의 흐름, 서로의 성향, 관계에서 조심할 점 등 궁금한 내용을 자유롭게 적어주세요.</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

picked = st.session_state.picked
st.markdown("### 🃏 네 장의 카드를 선택하세요")
st.markdown('<div class="small-note">카드는 모두 뒷면으로 놓여 있어요. 원하는 카드를 순서대로 네 장 골라주세요. 첫 두 장은 본인, 다음 두 장은 상대방의 카드입니다.</div>', unsafe_allow_html=True)

step = len(picked)
if step < 4:
    st.markdown(f'<span class="role-pill">선택 {step+1}/4</span> <span class="role-pill">{POSITIONS[step][0]}</span> <span class="role-pill">{POSITIONS[step][1]}</span>', unsafe_allow_html=True)
else:
    st.success("네 장의 카드가 모두 선택되었어요. 이제 두 사람의 이야기를 확인해 보세요.")

cols = st.columns(4)
for display_idx, card_idx in enumerate(st.session_state.deck_order):
    card = CARDS[card_idx]
    with cols[display_idx % 4]:
        already = card["name"] in picked
        st.markdown('<div class="tarot-back">✧<br>☾<br>✧</div>', unsafe_allow_html=True)
        if already:
            st.button("선택 완료", key=f"done_{card_idx}", disabled=True, use_container_width=True)
        elif len(picked) >= 4:
            st.button("선택 마감", key=f"closed_{card_idx}", disabled=True, use_container_width=True)
        else:
            if st.button("이 카드 선택", key=f"pick_{card_idx}", use_container_width=True):
                st.session_state.picked.append(card["name"])
                st.rerun()

if picked:
    st.markdown("### 🌟 선택한 카드")
    chosen_cols = st.columns(4)
    for i, name in enumerate(picked):
        card = get_card(name)
        with chosen_cols[i]:
            st.markdown(f"""
            <div class="tarot-face">
              <div class="symbol">{card['symbol']}</div>
              <div class="name">{card['name']}</div>
              <div class="keyword">{card['keyword']}</div>
            </div>
            <div style="text-align:center;color:#e4d3f1;font-size:.78rem;margin-top:.45rem">{POSITIONS[i][0]}</div>
            """, unsafe_allow_html=True)

if len(picked) == 4:
    st.markdown("---")
    if st.button("🌙 내 타로 리딩 확인하기", type="primary", use_container_width=True):
        if not question.strip():
            st.session_state.need_question = True
        else:
            st.session_state.need_question = False
            st.session_state.show_reading = True
    if st.session_state.get("need_question"):
        st.warning("먼저 궁금한 질문을 적어주세요.")
    if st.session_state.get("show_reading") and question.strip():
        with st.spinner("네 장의 카드에 담긴 상징을 해석하고 있어요..."):
            reading = ai_reading(question.strip(), picked)
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        if reading:
            st.markdown(reading)
            st.caption("AI 타로 리딩은 선택한 카드의 상징을 바탕으로 생성한 오락·자기성찰용 해석입니다.")
        else:
            st.markdown(build_reading(question.strip(), picked), unsafe_allow_html=True)
            st.caption("기본 카드 해석 모드입니다. 더 풍부한 AI 해석을 원하면 Streamlit Secrets에 OPENAI_API_KEY를 설정할 수 있습니다.")
        st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")
left, right = st.columns([3,1])
with left:
    st.markdown('<div class="small-note">✦ 타로는 미래나 상대방의 실제 마음을 확정하는 도구가 아니라, 관계를 다른 시각으로 생각해 보는 오락·자기성찰 콘텐츠입니다. 실제 관계에서는 서로의 말과 행동, 존중과 대화가 가장 중요해요.</div>', unsafe_allow_html=True)
with right:
    if st.button("↻ 처음부터 다시 하기", use_container_width=True):
        for key in ["picked", "show_reading", "need_question", "deck_order"]:
            st.session_state.pop(key, None)
        st.rerun()


