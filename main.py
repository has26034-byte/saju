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
