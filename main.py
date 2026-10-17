import random
import streamlit as st

# 1. 페이지 기본 설정
st.set_page_config(
    page_title="두근두근 뽑기 시뮬레이터", page_icon="🎲", layout="centered"
)

# 2. 확률 설정 (총합 100%)
TIERS = [
    ("전설", 0.001, "#FFD700"),  # (이름, 확률, 색상)
    ("영웅", 0.029, "#9400D3"),
    ("희귀", 0.070, "#1E90FF"),
    ("일반", 0.900, "#A9A9A9"),
]


def gacha_roll():
    """가중치 확률에 따라 등급 하나 추첨"""
    rand_val = random.random()
    cumulative = 0.0
    for name, prob, color in TIERS:
        cumulative += prob
        if rand_val <= cumulative:
            return name, color
    return "일반", "#A9A9A9"


# 3. 데이터(세션) 초기화 - 새로고침해도 뽑기 기록 유지
if "history" not in st.session_state:
    st.session_state.history = []
if "stats" not in st.session_state:
    st.session_state.stats = {"전설": 0, "영웅": 0, "희귀": 0, "일반": 0}

# 4. 앱 타이틀
st.title("🎲 아이템 뽑기 시뮬레이터")
st.write("버튼을 눌러 아이템을 뽑아보세요!")

st.divider()

# 5. 뽑기 버튼 레이아웃
col1, col2 = st.columns(2)

with col1:
    if st.button("🎰 1회 뽑기", use_container_width=True):
        name, color = gacha_roll()
        st.session_state.history.append(name)
        st.session_state.stats[name] += 1
        st.success(f"🎉 **[1회 결과]** 당첨: **:{color}[{name}]**")

with col2:
    if st.button("🚀 10연차!", use_container_width=True):
        results = []
        for _ in range(10):
            name, color = gacha_roll()
            st.session_state.history.append(name)
            st.session_state.stats[name] += 1
            results.append(f":{color}[{name}]")

        st.info("✨ **[10연차 결과]** ✨")
        st.write(" | ".join(results[:5]))
        st.write(" | ".join(results[5:]))

st.divider()

# 6. 통계 및 누적 기록 표시
st.subheader("📊 누적 뽑기 통계")
total_count = len(st.session_state.history)

if total_count > 0:
    # 4개 칼럼으로 지표 출력
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("🟡 전설", f"{st.session_state.stats['전설']}회")
    m2.metric("🟣 영웅", f"{st.session_state.stats['영웅']}회")
    m3.metric("🔵 희귀", f"{st.session_state.stats['희귀']}회")
    m4.metric("⚪ 일반", f"{st.session_state.stats['일반']}회")

    st.caption(f"총 뽑기 횟수: {total_count}회")

    # 최근 기록 접이식 메뉴
    with st.expander("📜 최근 뽑기 기록 보기"):
        for idx, item in enumerate(
            reversed(st.session_state.history[-20:]), 1
        ):
            st.write(f"{idx}. {item}")
else:
    st.write("아직 뽑기 기록이 없습니다.")
