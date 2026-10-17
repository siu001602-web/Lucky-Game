import random
import time
import streamlit as st

# 1. 페이지 기본 설정
st.set_page_config(
    page_title="두근두근 뽑기 & 상점 시뮬레이터",
    page_icon="🎲",
    layout="centered",
)

# 비밀 연출용 커스텀 CSS (암전 이펙트)
st.markdown(
    """
    <style>
    @keyframes fadeDark {
        0% { background-color: rgba(0, 0, 0, 0); }
        30% { background-color: rgba(0, 0, 0, 0.95); }
        80% { background-color: rgba(0, 0, 0, 0.95); }
        100% { background-color: rgba(0, 0, 0, 0); }
    }
    .secret-effect {
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        z-index: 999999;
        pointer-events: none;
        animation: fadeDark 1.5s ease-in-out forwards;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# 2. 확률 설정 (총합 100%)
# 비밀: 0.01% (0.0001), 전설: 0.09% (0.0009), 영웅: 2.9% (0.029), 희귀: 7.0% (0.070), 일반: 90.0% (0.900)
TIERS = [
    ("비밀", 0.0001, "#FF1493"),  # 핫핑크
    ("전설", 0.0009, "#FFD700"),  # 골드
    ("영웅", 0.0290, "#9400D3"),  # 퍼플
    ("희귀", 0.0700, "#1E90FF"),  # 블루
    ("일반", 0.9000, "#A9A9A9"),  # 그레이
]

# 아이템 판매 가격 (코인)
SELL_PRICES = {
    "일반": 0.01,
    "희귀": 0.05,
    "영웅": 0.1,
    "전설": 100.0,
    "비밀": 0.0,
}


def gacha_roll():
    """가중치 확률에 따라 등급 하나 추첨"""
    rand_val = random.random()
    cumulative = 0.0
    for name, prob, color in TIERS:
        cumulative += prob
        if rand_val <= cumulative:
            return name, color
    return "일반", "#A9A9A9"


def lucky_dice_roll():
    """행운의 주사위: 전설 70%, 비밀 30%"""
    rand_val = random.random()
    if rand_val <= 0.30:
        return "비밀", "#FF1493"
    else:
        return "전설", "#FFD700"


# 3. 데이터(세션) 초기화
if "coins" not in st.session_state:
    st.session_state.coins = 0.0
if "history" not in st.session_state:
    st.session_state.history = []
if "stats" not in st.session_state:
    st.session_state.stats = {
        "비밀": 0,
        "전설": 0,
        "영웅": 0,
        "희귀": 0,
        "일반": 0,
    }
if "inventory" not in st.session_state:
    st.session_state.inventory = {
        "비밀": 0,
        "전설": 0,
        "영웅": 0,
        "희귀": 0,
        "일반": 0,
    }
if "trigger_secret_effect" not in st.session_state:
    st.session_state.trigger_secret_effect = False

# 비밀 등급 연출 실행
if st.session_state.trigger_secret_effect:
    st.markdown(
        '<div class="secret-effect"></div>', unsafe_allow_html=True
    )
    st.session_state.trigger_secret_effect = False

# 4. 앱 상단 레이아웃 (타이틀 & 코인 보유량)
st.title("🎲 뽑기 & 상점 시뮬레이터")
st.metric(label="💰 보유 코인", value=f"{st.session_state.coins:.2f} 코인")

st.divider()

# 탭 구성
tab1, tab2, tab3 = st.tabs(
    ["🎰 아이템 뽑기", "🏪 상점 & 판매소", "📊 통계 & 기록"]
)

# ================= TAB 1: 아이템 뽑기 =================
with tab1:
    st.subheader("아이템 뽑기")
    col1, col2 = st.columns(2)

    with col1:
        if st.button("🎰 1회 뽑기", use_container_width=True):
            name, color = gacha_roll()
            st.session_state.history.append(name)
            st.session_state.stats[name] += 1
            st.session_state.inventory[name] += 1

            if name == "비밀":
                st.session_state.trigger_secret_effect = True
                st.rerun()

            st.success(f"🎉 **[1회 결과]** 당첨: **:{color}[{name}]**")

    with col2:
        if st.button("🚀 10연차!", use_container_width=True):
            results = []
            has_secret = False
            for _ in range(10):
                name, color = gacha_roll()
                st.session_state.history.append(name)
                st.session_state.stats[name] += 1
                st.session_state.inventory[name] += 1
                results.append(f":{color}[{name}]")
                if name == "비밀":
                    has_secret = True

            if has_secret:
                st.session_state.trigger_secret_effect = True
                st.rerun()

            st.info("✨ **[10연차 결과]** ✨")
            st.write(" | ".join(results[:5]))
            st.write(" | ".join(results[5:]))

# ================= TAB 2: 상점 & 판매소 =================
with tab2:
    st.subheader("💵 아이템 판매소")
    st.caption("보유한 아이템을 판매하여 코인을 획득하세요.")

    c1, c2, c3, c4 = st.columns(4)
    c1.write(f"⚪ 일반 ({st.session_state.inventory['일반']}개)\n개당 0.01코인")
    c2.write(f"🔵 희귀 ({st.session_state.inventory['희귀']}개)\n개당 0.05코인")
    c3.write(f"🟣 영웅 ({st.session_state.inventory['영웅']}개)\n개당 0.10코인")
    c4.write(
        f"🟡 전설 ({st.session_state.inventory['전설']}개)\n개당 100.0코인"
    )

    if st.button("💰 일반/희귀/영웅/전설 일괄 판매하기", type="primary"):
        earned = (
            (st.session_state.inventory["일반"] * SELL_PRICES["일반"])
            + (st.session_state.inventory["희귀"] * SELL_PRICES["희귀"])
            + (st.session_state.inventory["영웅"] * SELL_PRICES["영웅"])
            + (st.session_state.inventory["전설"] * SELL_PRICES["전설"])
        )
        if earned > 0:
            st.session_state.coins += earned
            for tier in ["일반", "희귀", "영웅", "전설"]:
                st.session_state.inventory[tier] = 0
            st.success(f"🎉 아이템을 모두 판매하여 {earned:.2f} 코인을 얻었습니다!")
            st.rerun()
        else:
            st.warning("판매할 수 있는 아이템이 없습니다.")

    st.divider()

    st.subheader("🛒 Special 상점")

    s_col1, s_col2 = st.columns(2)

    with s_col1:
        st.markdown("### 🎲 행운의 주사위")
        st.write("가격: **300 코인**")
        st.write("확률: **전설 70% | 비밀 30%**")
        if st.button("🎲 행운의 주사위 구매"):
            if st.session_state.coins >= 300:
                st.session_state.coins -= 300
                name, color = lucky_dice_roll()
                st.session_state.history.append(f"주사위:{name}")
                st.session_state.stats[name] += 1
                st.session_state.inventory[name] += 1

                if name == "비밀":
                    st.session_state.trigger_secret_effect = True
                    st.rerun()

                st.success(f"🎲 주사위 결과: **:{color}[{name}]** 당첨!")
                st.rerun()
            else:
                st.error("코인이 부족합니다! (300 코인 필요)")

    with s_col2:
        st.markdown("### 💖 비밀 등급 확정 구슬")
        st.write("가격: **2000 코인**")
        st.write("효과: **비밀 등급 100% 획득**")
        if st.button("🔮 비밀 구슬 구매"):
            if st.session_state.coins >= 2000:
                st.session_state.coins -= 2000
                name = "비밀"
                st.session_state.history.append("상점구매:비밀")
                st.session_state.stats[name] += 1
                st.session_state.inventory[name] += 1
                st.session_state.trigger_secret_effect = True
                st.rerun()
            else:
                st.error("코인이 부족합니다! (2000 코인 필요)")

# ================= TAB 3: 통계 & 기록 =================
with tab3:
    st.subheader("📊 누적 뽑기 통계")
    total_count = len(st.session_state.history)

    if total_count > 0:
        m1, m2, m3, m4, m5 = st.columns(5)
        m1.metric("💖 비밀", f"{st.session_state.stats['비밀']}회")
        m2.metric("🟡 전설", f"{st.session_state.stats['전설']}회")
        m3.metric("🟣 영웅", f"{st.session_state.stats['영웅']}회")
        m4.metric("🔵 희귀", f"{st.session_state.stats['희귀']}회")
        m5.metric("⚪ 일반", f"{st.session_state.stats['일반']}회")

        st.caption(f"총 획득 횟수: {total_count}회")

        with st.expander("📜 최근 뽑기 기록 보기"):
            for idx, item in enumerate(
                reversed(st.session_state.history[-20:]), 1
            ):
                st.write(f"{idx}. {item}")

        st.divider()

        if st.button("🗑️ 전체 데이터 초기화", type="secondary"):
            st.session_state.coins = 0.0
            st.session_state.history = []
            st.session_state.stats = {
                "비밀": 0,
                "전설": 0,
                "영웅": 0,
                "희귀": 0,
                "일반": 0,
            }
            st.session_state.inventory = {
                "비밀": 0,
                "전설": 0,
                "영웅": 0,
                "희귀": 0,
                "일반": 0,
            }
            st.rerun()
    else:
        st.write("아직 기록이 없습니다.")
