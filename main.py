import json
import random
import time
import streamlit as st

# 1. 페이지 기본 설정
st.set_page_config(
    page_title="두근두근 뽑기 & 상점 시뮬레이터",
    page_icon="🎲",
    layout="centered",
)

# 커스텀 연출 CSS (컷씬 애니메이션 및 클릭 방지 처리)
st.markdown(
    """
    <style>
    @keyframes fadeDark {
        0% { background-color: rgba(0, 0, 0, 0); }
        25% { background-color: rgba(0, 0, 0, 0.98); }
        75% { background-color: rgba(0, 0, 0, 0.98); }
        100% { background-color: rgba(0, 0, 0, 0); }
    }
    @keyframes monsterJump {
        0% { transform: scale(0.2); opacity: 0; }
        50% { transform: scale(1.2); opacity: 1; }
        100% { transform: scale(1.0); opacity: 1; }
    }
    @keyframes holyFlash {
        0% { background-color: rgba(0, 0, 0, 0); }
        20% { background-color: rgba(0, 0, 0, 0.98); }
        40% { background-color: rgba(255, 255, 255, 1); }
        80% { background-color: rgba(255, 255, 255, 1); }
        100% { background-color: rgba(0, 0, 0, 0); }
    }
    @keyframes abyssWhirlpool {
        0% { background: radial-gradient(circle, #001133 0%, #000511 100%); opacity: 0; transform: scale(0.8); }
        20% { opacity: 1; transform: scale(1); }
        50% { background: radial-gradient(circle, #003366 0%, #000511 100%); transform: rotate(180deg); }
        80% { opacity: 1; transform: scale(1); }
        100% { opacity: 0; transform: scale(1.2); }
    }
    @keyframes cometMeteor {
        0% { background: #020208; opacity: 0; }
        15% { opacity: 1; }
        30% { background: radial-gradient(circle at 80% 20%, #ffaa00 0%, #020208 60%); }
        60% { background: radial-gradient(circle at 20% 80%, #ff4400 0%, #020208 70%); }
        85% { opacity: 1; }
        100% { opacity: 0; }
    }

    /* 컷씬 진행 중 클릭 방지 레이어 */
    .effect-overlay {
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        z-index: 9999999;
        pointer-events: auto; /* 화면 터치/클릭 방지 */
        display: flex;
        justify-content: center;
        align-items: center;
    }
    .dark-fade { animation: fadeDark 2.5s ease-in-out forwards; }
    .holy-fade { animation: holyFlash 2.5s ease-in-out forwards; }
    .abyss-fade { animation: abyssWhirlpool 10.0s ease-in-out forwards; }
    .comet-fade { animation: cometMeteor 8.0s ease-in-out forwards; }

    .monster-popup {
        font-size: 50px;
        font-weight: bold;
        color: #FF4500;
        text-shadow: 0px 0px 20px #000000;
        animation: monsterJump 0.8s ease-out forwards;
        text-align: center;
    }
    .holy-popup {
        font-size: 50px;
        font-weight: bold;
        color: #00BFFF;
        text-shadow: 0px 0px 30px #FFFFFF;
        animation: monsterJump 0.8s ease-out forwards;
        text-align: center;
    }
    .abyss-popup {
        font-size: 50px;
        font-weight: bold;
        color: #00ffff;
        text-shadow: 0px 0px 30px #0055ff;
        animation: monsterJump 1.2s ease-out forwards;
        text-align: center;
    }
    .comet-popup {
        font-size: 55px;
        font-weight: bold;
        color: #ffcc00;
        text-shadow: 0px 0px 40px #ff3300;
        animation: monsterJump 1.5s ease-out forwards;
        text-align: center;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# 2. 확률 설정 (총합 100%)
# 혜성: 0.00001% (0.00000010)
# 어비스: 0.00009% (0.00000090)
# 신성한: 0.0009% (0.00000900)
# 도깨비: 0.001% (0.00001000)
# 비밀: 0.009% (0.00009000)
# 전설: 0.09% (0.00090000)
# 영웅: 2.9% (0.02900000)
# 희귀: 7.0% (0.07000000)
# 일반: 89.99899% (0.89998990)
TIERS = [
    ("혜성", 0.00000010, "#FF4500"),  # 우주 오렌지
    ("어비스", 0.00000090, "#00FFFF"),  # 심해 시안
    ("신성한", 0.00000900, "#00BFFF"),  # 딥 스카이 블루
    ("도깨비", 0.00001000, "#FF0055"),  # 네온 붉은색
    ("비밀", 0.00009000, "#FF1493"),  # 핫핑크
    ("전설", 0.00090000, "#FFD700"),  # 골드
    ("영웅", 0.02900000, "#9400D3"),  # 퍼플
    ("희귀", 0.07000000, "#1E90FF"),  # 블루
    ("일반", 0.89998990, "#A9A9A9"),  # 그레이
]

# 아이템 판매 가격 (코인)
SELL_PRICES = {
    "일반": 0.01,
    "희귀": 0.05,
    "영웅": 5.0,
    "전설": 100.0,
    "비밀": 1000.0,
    "도깨비": 5000.0,
    "신성한": 20000.0,
    "어비스": 100000.0,
    "혜성": 500000.0,
}


def gacha_roll():
    rand_val = random.random()
    cumulative = 0.0
    for name, prob, color in TIERS:
        cumulative += prob
        if rand_val <= cumulative:
            return name, color
    return "일반", "#A9A9A9"


def lucky_dice_roll():
    """행운의 주사위: 전설 70%, 비밀 20%, 도깨비 10%"""
    rand_val = random.random()
    if rand_val <= 0.10:
        return "도깨비", "#FF0055"
    elif rand_val <= 0.30:
        return "비밀", "#FF1493"
    else:
        return "전설", "#FFD700"


# 3. 데이터(세션) 초기화
if "coins" not in st.session_state:
    st.session_state.coins = 0.0
if "history" not in st.session_state:
    st.session_state.history = []
if "stats" not in st.session_state:
    st.session_state.stats = {t[0]: 0 for t in TIERS}
if "inventory" not in st.session_state:
    st.session_state.inventory = {t[0]: 0 for t in TIERS}
if "special_inventory" not in st.session_state:
    st.session_state.special_inventory = {
        "행운의 주사위": 0,
        "비밀 등급 확정 구슬": 0,
        "100연차 기능권": 0,
    }
if "unlocked" not in st.session_state:
    st.session_state.unlocked = {
        "혜성": False,
        "어비스": False,
        "신성한": False,
        "도깨비": False,
        "비밀": False,
        "전설": True,
        "영웅": True,
        "희귀": True,
        "일반": True,
    }
if "has_100_roll" not in st.session_state:
    st.session_state.has_100_roll = False

if "effect_type" not in st.session_state:
    st.session_state.effect_type = None

# 연출 실행 처리 (컷씬 동안 입력 차단)
if st.session_state.effect_type == "comet":
    st.markdown(
        '<div class="effect-overlay comet-fade"><div class="comet-popup">☄️ [혜성] 등급 우주에서 강림!! ☄️<br>거대한 메테오가 충돌합니다!</div></div>',
        unsafe_allow_html=True,
    )
    time.sleep(7.5)
    st.session_state.effect_type = None
    st.rerun()
elif st.session_state.effect_type == "abyss":
    st.markdown(
        '<div class="effect-overlay abyss-fade"><div class="abyss-popup">🌊 [어비스] 심해 소용돌이 발생!! 🌊<br>심연의 수평선이 휘감아칩니다!</div></div>',
        unsafe_allow_html=True,
    )
    time.sleep(9.5)
    st.session_state.effect_type = None
    st.rerun()
elif st.session_state.effect_type == "holy":
    st.markdown(
        '<div class="effect-overlay holy-fade"><div class="holy-popup">✨ [신성한] 등급 강림!! ✨<br>거룩한 빛이 사방을 비춥니다!</div></div>',
        unsafe_allow_html=True,
    )
    time.sleep(2.3)
    st.session_state.effect_type = None
    st.rerun()
elif st.session_state.effect_type == "secret":
    st.markdown(
        '<div class="effect-overlay dark-fade"><h1 style="color: #FF1493; font-size: 50px;">✨ 비밀 등급 획득! ✨</h1></div>',
        unsafe_allow_html=True,
    )
    time.sleep(2.0)
    st.session_state.effect_type = None
    st.rerun()
elif st.session_state.effect_type == "dokebi":
    st.markdown(
        '<div class="effect-overlay dark-fade"><div class="monster-popup">👹 도깨비 튀어나옴!!<br>도깨비 등급 획득!! 👹</div></div>',
        unsafe_allow_html=True,
    )
    time.sleep(2.0)
    st.session_state.effect_type = None
    st.rerun()


def get_display_name(tier_name):
    if not st.session_state.unlocked.get(tier_name, False):
        return "❓ ??"
    names = {
        "혜성": "☄️ 혜성",
        "어비스": "🌊 어비스",
        "신성한": "👼 신성한",
        "도깨비": "👹 도깨비",
        "비밀": "💖 비밀",
        "전설": "🟡 전설",
        "영웅": "🟣 영웅",
        "희귀": "🔵 희귀",
        "일반": "⚪ 일반",
    }
    return names.get(tier_name, tier_name)


# 4. 앱 상단 레이아웃
st.title("🎲 뽑기 & 상점 시뮬레이터")
st.metric(label="💰 보유 코인", value=f"{st.session_state.coins:.2f} 코인")

st.divider()

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(
    [
        "🎰 아이템 뽑기",
        "🏪 상점 & 판매소",
        "🎒 배낭",
        "📕 아이템 도감",
        "📊 통계 & 기록",
        "💾 세이브/로드",
    ]
)

# ================= TAB 1: 아이템 뽑기 =================
with tab1:
    st.subheader("아이템 뽑기")
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("🎰 1회 뽑기", use_container_width=True):
            name, color = gacha_roll()
            st.session_state.history.append(name)
            st.session_state.stats[name] += 1
            st.session_state.inventory[name] += 1

            if name in ["혜성", "어비스", "신성한", "도깨비", "비밀"]:
                st.session_state.unlocked[name] = True
                st.session_state.effect_type = (
                    "comet"
                    if name == "혜성"
                    else (
                        "abyss"
                        if name == "어비스"
                        else (
                            "holy"
                            if name == "신성한"
                            else "dokebi" if name == "도깨비" else "secret"
                        )
                    )
                )
                st.rerun()

            display_name = get_display_name(name)
            st.success(f"🎉 **[1회 결과]** 당첨: **:{color}[{display_name}]**")

    with col2:
        if st.button("🚀 10연차!", use_container_width=True):
            results = []
            special_hit = None
            priority = ["혜성", "어비스", "신성한", "도깨비", "비밀"]

            for _ in range(10):
                name, color = gacha_roll()
                st.session_state.history.append(name)
                st.session_state.stats[name] += 1
                st.session_state.inventory[name] += 1

                if name in priority:
                    st.session_state.unlocked[name] = True
                    if (
                        special_hit is None
                        or priority.index(name) < priority.index(special_hit)
                    ):
                        special_hit = name

                display_name = get_display_name(name)
                results.append(f":{color}[{display_name}]")

            if special_hit:
                st.session_state.effect_type = (
                    "comet"
                    if special_hit == "혜성"
                    else (
                        "abyss"
                        if special_hit == "어비스"
                        else (
                            "holy"
                            if special_hit == "신성한"
                            else (
                                "dokebi"
                                if special_hit == "도깨비"
                                else "secret"
                            )
                        )
                    )
                )
                st.rerun()

            st.info("✨ **[10연차 결과]** ✨")
            st.write(" | ".join(results[:5]))
            st.write(" | ".join(results[5:]))

    with col3:
        if st.session_state.has_100_roll:
            if st.button("💥 100연차!", use_container_width=True, type="primary"):
                special_hit = None
                priority = ["혜성", "어비스", "신성한", "도깨비", "비밀"]

                for _ in range(100):
                    name, color = gacha_roll()
                    st.session_state.history.append(name)
                    st.session_state.stats[name] += 1
                    st.session_state.inventory[name] += 1

                    if name in priority:
                        st.session_state.unlocked[name] = True
                        if (
                            special_hit is None
                            or priority.index(name) < priority.index(special_hit)
                        ):
                            special_hit = name

                if special_hit:
                    st.session_state.effect_type = (
                        "comet"
                        if special_hit == "혜성"
                        else (
                            "abyss"
                            if special_hit == "어비스"
                            else (
                                "holy"
                                if special_hit == "신성한"
                                else (
                                    "dokebi"
                                    if special_hit == "도깨비"
                                    else "secret"
                                )
                            )
                        )
                    )
                    st.rerun()

                st.success("💥 100연차 완료! 통계 및 인벤토리를 확인해보세요.")
                st.rerun()
        else:
            st.button(
                "🔒 100연차 (상점 해금)",
                use_container_width=True,
                disabled=True,
            )

# ================= TAB 2: 상점 & 판매소 =================
with tab2:
    st.subheader("💵 원하는 등급 선택 판매소")
    st.caption("판매하고 싶은 등급을 체크하고 판매 버튼을 누르세요.")

    sell_selection = {}
    c1, c2, c3 = st.columns(3)
    with c1:
        sell_selection["일반"] = st.checkbox(
            f"⚪ 일반 ({st.session_state.inventory['일반']}개)",
            key="chk_normal",
        )
        sell_selection["희귀"] = st.checkbox(
            f"🔵 희귀 ({st.session_state.inventory['희귀']}개)", key="chk_rare"
        )
        sell_selection["영웅"] = st.checkbox(
            f"🟣 영웅 ({st.session_state.inventory['영웅']}개)", key="chk_epic"
        )
    with c2:
        sell_selection["전설"] = st.checkbox(
            f"🟡 전설 ({st.session_state.inventory['전설']}개)",
            key="chk_legend",
        )
        b_name = get_display_name("비밀")
        sell_selection["비밀"] = st.checkbox(
            f"{b_name} ({st.session_state.inventory['비밀']}개)", key="chk_secret"
        )
        d_name = get_display_name("도깨비")
        sell_selection["도깨비"] = st.checkbox(
            f"{d_name} ({st.session_state.inventory['도깨비']}개)",
            key="chk_dokebi",
        )
    with c3:
        h_name = get_display_name("신성한")
        sell_selection["신성한"] = st.checkbox(
            f"{h_name} ({st.session_state.inventory['신성한']}개)", key="chk_holy"
        )
        a_name = get_display_name("어비스")
        sell_selection["어비스"] = st.checkbox(
            f"{a_name} ({st.session_state.inventory['어비스']}개)",
            key="chk_abyss",
        )
        cm_name = get_display_name("혜성")
        sell_selection["혜성"] = st.checkbox(
            f"{cm_name} ({st.session_state.inventory['혜성']}개)", key="chk_comet"
        )

    if st.button("💰 선택한 아이템 판매하기", type="primary"):
        earned = 0.0
        sold_any = False
        for tier, checked in sell_selection.items():
            if checked and st.session_state.inventory[tier] > 0:
                count = st.session_state.inventory[tier]
                earned += count * SELL_PRICES[tier]
                st.session_state.inventory[tier] = 0
                sold_any = True

        if sold_any and earned > 0:
            st.session_state.coins += earned
            st.success(f"🎉 선택한 아이템을 판매하여 {earned:.2f} 코인을 획득했습니다!")
            st.rerun()
        else:
            st.warning("판매할 아이템을 선택하지 않았거나 개수가 0개입니다.")

    st.divider()

    st.subheader("🛒 Special 상점")
    s_col1, s_col2, s_col3 = st.columns(3)

    with s_col1:
        st.markdown("### 🎲 행운의 주사위")
        st.write("가격: **800 코인**")

        secret_prob_str = (
            "비밀 20%" if st.session_state.unlocked.get("비밀") else "❓ ??"
        )
        dokebi_prob_str = (
            "도깨비 10%" if st.session_state.unlocked.get("도깨비") else "❓ ??"
        )
        st.write(f"확률: **전설 70% | {secret_prob_str} | {dokebi_prob_str}**")

        if st.button("🎲 주사위 구매"):
            if st.session_state.coins >= 800:
                st.session_state.coins -= 800
                st.session_state.special_inventory["행운의 주사위"] += 1
                st.success("✨ '행운의 주사위'를 배낭에 넣었습니다!")
            else:
                st.error("코인이 부족합니다! (800 코인 필요)")

    with s_col2:
        st.markdown("### 💖 비밀 확정 구슬")
        st.write("가격: **1500 코인**")
        if st.button("🔮 비밀 구슬 구매"):
            if st.session_state.coins >= 1500:
                st.session_state.coins -= 1500
                st.session_state.special_inventory["비밀 등급 확정 구슬"] += 1
                st.success("✨ '비밀 등급 확정 구슬'을 배낭에 넣었습니다!")
            else:
                st.error("코인이 부족합니다! (1500 코인 필요)")

    with s_col3:
        st.markdown("### 💥 100연차 기능")
        st.write("가격: **500 코인**")
        st.write("효과: **100연차 기능 영구 해금**")

        is_sold_out = st.session_state.has_100_roll or (
            st.session_state.special_inventory.get("100연차 기능권", 0) > 0
        )

        if is_sold_out:
            st.button("🚫 [품절]", disabled=True, key="btn_soldout_100")
        else:
            if st.button("💥 100연차 구매"):
                if st.session_state.coins >= 500:
                    st.session_state.coins -= 500
                    st.session_state.special_inventory["100연차 기능권"] += 1
                    st.success("✨ '100연차 기능권'을 배낭에 넣었습니다!")
                    st.rerun()
                else:
                    st.error("코인이 부족합니다! (500 코인 필요)")

# ================= TAB 3: 배낭 =================
with tab3:
    st.subheader("🎒 특수 아이템 배낭")

    b_col1, b_col2, b_col3 = st.columns(3)

    with b_col1:
        st.markdown("### 🎲 행운의 주사위")
        dice_count = st.session_state.special_inventory["행운의 주사위"]
        st.write(f"보유: **{dice_count}개**")
        if st.button("주사위 사용", disabled=(dice_count == 0)):
            st.session_state.special_inventory["행운의 주사위"] -= 1
            name, color = lucky_dice_roll()
            st.session_state.history.append(f"주사위사용:{name}")
            st.session_state.stats[name] += 1
            st.session_state.inventory[name] += 1

            if name in ["도깨비", "비밀"]:
                st.session_state.unlocked[name] = True
                st.session_state.effect_type = (
                    "dokebi" if name == "도깨비" else "secret"
                )
                st.rerun()

            display_name = get_display_name(name)
            st.success(f"🎲 결과: **:{color}[{display_name}]** 당첨!")
            st.rerun()

    with b_col2:
        st.markdown("### 🔮 비밀 확정 구슬")
        marble_count = st.session_state.special_inventory[
            "비밀 등급 확정 구슬"
        ]
        st.write(f"보유: **{marble_count}개**")
        if st.button("구슬 사용", disabled=(marble_count == 0)):
            st.session_state.special_inventory["비밀 등급 확정 구슬"] -= 1
            name = "비밀"
            st.session_state.unlocked["비밀"] = True
            st.session_state.history.append("구슬사용:비밀")
            st.session_state.stats[name] += 1
            st.session_state.inventory[name] += 1
            st.session_state.effect_type = "secret"
            st.rerun()

    with b_col3:
        st.markdown("### 💥 100연차 기능권")
        ticket_count = st.session_state.special_inventory.get(
            "100연차 기능권", 0
        )
        if st.session_state.has_100_roll:
            st.write("상태: **영구 해금 완료**")
            st.button("사용 완료", disabled=True, key="btn_already_unlocked")
        else:
            st.write(f"보유: **{ticket_count}개**")
            if st.button("기능권 사용", disabled=(ticket_count == 0)):
                st.session_state.special_inventory["100연차 기능권"] -= 1
                st.session_state.has_100_roll = True
                st.success("🎉 '100연차' 기능이 영구 해금되었습니다!")
                st.rerun()

# ================= TAB 4: 아이템 도감 =================
with tab4:
    st.subheader("📕 등급 도감")
    st.caption(
        "각 등급을 뽑으면 도감에 정식 등록되어 이름과 상세 정보가 해금됩니다."
    )

    for tier_name, prob, color in TIERS:
        is_unlocked = st.session_state.unlocked.get(tier_name, False)
        prob_percent = prob * 100

        with st.container():
            if is_unlocked:
                disp_name = get_display_name(tier_name)
                price = SELL_PRICES[tier_name]
                st.markdown(
                    f"### :{color}[{disp_name}]  \n"
                    f"* **등장 확률**: `{prob_percent:.8f}%`  \n"
                    f"* **판매 가격**: `{price:.2f} 코인`  \n"
                    f"* **상태**: `🔓 도감 해금 완료`"
                )
            else:
                st.markdown(
                    f"### ❓ 미해금 등급  \n"
                    f"* **등장 확률**: `{prob_percent:.8f}%`  \n"
                    f"* **판매 가격**: `??? 코인`  \n"
                    f"* **상태**: `🔒 뽑아서 해금 필요`"
                )
            st.divider()

# ================= TAB 5: 통계 & 기록 =================
with tab5:
    st.subheader("📊 누적 뽑기 통계")
    total_count = len(st.session_state.history)

    if total_count > 0:
        cols1 = st.columns(5)
        for idx, t in enumerate(["혜성", "어비스", "신성한", "도깨비", "비밀"]):
            disp = get_display_name(t)
            cols1[idx].metric(disp, f"{st.session_state.stats[t]}회")

        cols2 = st.columns(4)
        for idx, t in enumerate(["전설", "영웅", "희귀", "일반"]):
            disp = get_display_name(t)
            cols2[idx].metric(disp, f"{st.session_state.stats[t]}회")

        st.caption(f"총 획득 횟수: {total_count}회")

        with st.expander("📜 최근 뽑기 기록 보기"):
            for idx, item in enumerate(
                reversed(st.session_state.history[-20:]), 1
            ):
                disp = get_display_name(item.replace("주사위사용:", ""))
                st.write(f"{idx}. {disp}")

        st.divider()

        if st.button("🗑️ 전체 데이터 초기화", type="secondary"):
            st.session_state.coins = 0.0
            st.session_state.history = []
            st.session_state.stats = {t[0]: 0 for t in TIERS}
            st.session_state.inventory = {t[0]: 0 for t in TIERS}
            st.session_state.special_inventory = {
                "행운의 주사위": 0,
                "비밀 등급 확정 구슬": 0,
                "100연차 기능권": 0,
            }
            st.session_state.unlocked = {
                "혜성": False,
                "어비스": False,
                "신성한": False,
                "도깨비": False,
                "비밀": False,
                "전설": True,
                "영웅": True,
                "희귀": True,
                "일반": True,
            }
            st.session_state.has_100_roll = False
            st.rerun()
    else:
        st.write("아직 기록이 없습니다.")

# ================= TAB 6: 세이브 / 로드 =================
with tab6:
    st.subheader("💾 세이브 파일 관리")

    game_data = {
        "coins": st.session_state.coins,
        "history": st.session_state.history,
        "stats": st.session_state.stats,
        "inventory": st.session_state.inventory,
        "special_inventory": st.session_state.special_inventory,
        "unlocked": st.session_state.unlocked,
        "has_100_roll": st.session_state.has_100_roll,
    }
    json_data = json.dumps(game_data, ensure_ascii=False, indent=4)

    st.download_button(
        label="📥 세이브 파일 다운로드",
        data=json_data,
        file_name="gacha_save.json",
        mime="application/json",
    )

    st.divider()

    st.markdown("### 📤 세이브 파일 불러오기")
    uploaded_file = st.file_uploader(
        "저장해 둔 세이브 파일(gacha_save.json)을 업로드하세요.",
        type=["json"],
    )

    if uploaded_file is not None:
        try:
            loaded_data = json.load(uploaded_file)
            if st.button("🔄 이 데이터로 게임 시작하기"):
                st.session_state.coins = loaded_data.get("coins", 0.0)
                st.session_state.history = loaded_data.get("history", [])

                default_stats = {t[0]: 0 for t in TIERS}
                st.session_state.stats = {
                    **default_stats,
                    **loaded_data.get("stats", {}),
                }

                default_inventory = {t[0]: 0 for t in TIERS}
                st.session_state.inventory = {
                    **default_inventory,
                    **loaded_data.get("inventory", {}),
                }

                default_special = {
                    "행운의 주사위": 0,
                    "비밀 등급 확정 구슬": 0,
                    "100연차 기능권": 0,
                }
                st.session_state.special_inventory = {
                    **default_special,
                    **loaded_data.get("special_inventory", {}),
                }

                default_unlocked = {
                    "혜성": False,
                    "어비스": False,
                    "신성한": False,
                    "도깨비": False,
                    "비밀": False,
                    "전설": True,
                    "영웅": True,
                    "희귀": True,
                    "일반": True,
                }
                st.session_state.unlocked = {
                    **default_unlocked,
                    **loaded_data.get("unlocked", {}),
                }

                st.session_state.has_100_roll = loaded_data.get(
                    "has_100_roll", False
                )

                st.success("🎉 세이브 파일을 성공적으로 불러왔습니다!")
                st.rerun()
        except Exception as e:
            st.error(f"세이브 파일 형식이 잘못되었습니다: {e}")
