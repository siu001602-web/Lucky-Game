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

# 비밀, 도깨비, 신성한 연출용 커스텀 CSS (암전, 도깨비 등장, 빛 연출)
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
    .effect-overlay {
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        z-index: 999999;
        pointer-events: none;
        display: flex;
        justify-content: center;
        align-items: center;
    }
    .dark-fade {
        animation: fadeDark 2.0s ease-in-out forwards;
    }
    .holy-fade {
        animation: holyFlash 2.5s ease-in-out forwards;
    }
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
    </style>
""",
    unsafe_allow_html=True,
)

# 2. 확률 설정 (총합 100%)
# 신성한: 0.0001% (0.000001)
# 도깨비: 0.001% (0.000010)
# 비밀: 0.009% (0.000090)
# 전설: 0.09% (0.000900)
# 영웅: 2.9% (0.029000)
# 희귀: 7.0% (0.070000)
# 일반: 89.9999% (0.899999)
TIERS = [
    ("신성한", 0.000001, "#00BFFF"),  # 딥 스카이 블루
    ("도깨비", 0.000010, "#FF4500"),  # 오렌지레드
    ("비밀", 0.000090, "#FF1493"),  # 핫핑크
    ("전설", 0.000900, "#FFD700"),  # 골드
    ("영웅", 0.029000, "#9400D3"),  # 퍼플
    ("희귀", 0.070000, "#1E90FF"),  # 블루
    ("일반", 0.899999, "#A9A9A9"),  # 그레이
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
        return "도깨비", "#FF4500"
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
    st.session_state.stats = {
        "신성한": 0,
        "도깨비": 0,
        "비밀": 0,
        "전설": 0,
        "영웅": 0,
        "희귀": 0,
        "일반": 0,
    }
if "inventory" not in st.session_state:
    st.session_state.inventory = {
        "신성한": 0,
        "도깨비": 0,
        "비밀": 0,
        "전설": 0,
        "영웅": 0,
        "희귀": 0,
        "일반": 0,
    }
if "special_inventory" not in st.session_state:
    st.session_state.special_inventory = {
        "행운의 주사위": 0,
        "비밀 등급 확정 구슬": 0,
        "100연차 티켓": 0,
    }
if "unlocked" not in st.session_state:
    st.session_state.unlocked = {
        "신성한": False,
        "도깨비": False,
        "비밀": False,
    }

if "effect_type" not in st.session_state:
    st.session_state.effect_type = None

# 연출 실행 처리
if st.session_state.effect_type == "holy":
    st.markdown(
        '<div class="effect-overlay holy-fade"><div class="holy-popup">✨ [신성한] 등급 강림!! ✨<br>거룩한 빛이 사방을 비춥니다!</div></div>',
        unsafe_allow_html=True,
    )
    st.session_state.effect_type = None
elif st.session_state.effect_type == "secret":
    st.markdown(
        '<div class="effect-overlay dark-fade"><h1 style="color: #FF1493; font-size: 50px;">✨ 비밀 등급 획득! ✨</h1></div>',
        unsafe_allow_html=True,
    )
    st.session_state.effect_type = None
elif st.session_state.effect_type == "dokebi":
    st.markdown(
        '<div class="effect-overlay dark-fade"><div class="monster-popup">👹 도깨비 튀어나옴!!<br>도깨비 등급 획득!! 👹</div></div>',
        unsafe_allow_html=True,
    )
    st.session_state.effect_type = None


def get_display_name(tier_name):
    if tier_name == "신성한" and not st.session_state.unlocked["신성한"]:
        return "❓ ??"
    if tier_name == "도깨비" and not st.session_state.unlocked["도깨비"]:
        return "❓ ??"
    if tier_name == "비밀" and not st.session_state.unlocked["비밀"]:
        return "❓ ??"
    if tier_name == "신성한":
        return "👼 신성한"
    if tier_name == "도깨비":
        return "👹 도깨비"
    if tier_name == "비밀":
        return "💖 비밀"
    if tier_name == "전설":
        return "🟡 전설"
    if tier_name == "영웅":
        return "🟣 영웅"
    if tier_name == "희귀":
        return "🔵 희귀"
    return "⚪ 일반"


# 4. 앱 상단 레이아웃
st.title("🎲 뽑기 & 상점 시뮬레이터")
st.metric(label="💰 보유 코인", value=f"{st.session_state.coins:.2f} 코인")

st.divider()

tab1, tab2, tab3, tab4, tab5 = st.tabs(
    [
        "🎰 아이템 뽑기",
        "🏪 상점 & 판매소",
        "🎒 배낭",
        "📊 통계 & 기록",
        "💾 세이브/로드",
    ]
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

            if name == "신성한":
                st.session_state.unlocked["신성한"] = True
                st.session_state.effect_type = "holy"
                st.rerun()
            elif name == "도깨비":
                st.session_state.unlocked["도깨비"] = True
                st.session_state.effect_type = "dokebi"
                st.rerun()
            elif name == "비밀":
                st.session_state.unlocked["비밀"] = True
                st.session_state.effect_type = "secret"
                st.rerun()

            display_name = get_display_name(name)
            st.success(f"🎉 **[1회 결과]** 당첨: **:{color}[{display_name}]**")

    with col2:
        if st.button("🚀 10연차!", use_container_width=True):
            results = []
            special_hit = None
            for _ in range(10):
                name, color = gacha_roll()
                st.session_state.history.append(name)
                st.session_state.stats[name] += 1
                st.session_state.inventory[name] += 1

                if name == "신성한":
                    st.session_state.unlocked["신성한"] = True
                    special_hit = "holy"
                elif name == "도깨비" and special_hit != "holy":
                    st.session_state.unlocked["도깨비"] = True
                    special_hit = "dokebi"
                elif (
                    name == "비밀"
                    and special_hit != "holy"
                    and special_hit != "dokebi"
                ):
                    st.session_state.unlocked["비밀"] = True
                    special_hit = "secret"

                display_name = get_display_name(name)
                results.append(f":{color}[{display_name}]")

            if special_hit:
                st.session_state.effect_type = special_hit
                st.rerun()

            st.info("✨ **[10연차 결과]** ✨")
            st.write(" | ".join(results[:5]))
            st.write(" | ".join(results[5:]))

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
    with c3:
        d_name = get_display_name("도깨비")
        h_name = get_display_name("신성한")
        sell_selection["도깨비"] = st.checkbox(
            f"{d_name} ({st.session_state.inventory['도깨비']}개)",
            key="chk_dokebi",
        )
        sell_selection["신성한"] = st.checkbox(
            f"{h_name} ({st.session_state.inventory['신성한']}개)", key="chk_holy"
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
        st.write("가격: **300 코인**")

        secret_prob_str = "비밀 20%" if st.session_state.unlocked["비밀"] else "❓ ??"
        dokebi_prob_str = "도깨비 10%" if st.session_state.unlocked["도깨비"] else "❓ ??"
        st.write(f"확률: **전설 70% | {secret_prob_str} | {dokebi_prob_str}**")

        if st.button("🎲 주사위 구매"):
            if st.session_state.coins >= 300:
                st.session_state.coins -= 300
                st.session_state.special_inventory["행운의 주사위"] += 1
                st.success("✨ '행운의 주사위'를 배낭에 넣었습니다!")
            else:
                st.error("코인이 부족합니다! (300 코인 필요)")

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
        st.markdown("### 🎫 100연차 티켓")
        st.write("가격: **500 코인**")
        st.write("효과: **한 번에 100회 연차 실행**")
        if st.button("🎫 티켓 구매"):
            if st.session_state.coins >= 500:
                st.session_state.coins -= 500
                st.session_state.special_inventory["100연차 티켓"] += 1
                st.success("✨ '100연차 티켓'을 배낭에 넣었습니다!")
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

            if name == "도깨비":
                st.session_state.unlocked["도깨비"] = True
                st.session_state.effect_type = "dokebi"
                st.rerun()
            elif name == "비밀":
                st.session_state.unlocked["비밀"] = True
                st.session_state.effect_type = "secret"
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
        st.markdown("### 🎫 100연차 티켓")
        ticket_count = st.session_state.special_inventory["100연차 티켓"]
        st.write(f"보유: **{ticket_count}개**")
        if st.button("티켓 사용", disabled=(ticket_count == 0)):
            st.session_state.special_inventory["100연차 티켓"] -= 1
            special_hit = None
            for _ in range(100):
                name, color = gacha_roll()
                st.session_state.history.append(name)
                st.session_state.stats[name] += 1
                st.session_state.inventory[name] += 1

                if name == "신성한":
                    st.session_state.unlocked["신성한"] = True
                    special_hit = "holy"
                elif name == "도깨비" and special_hit != "holy":
                    st.session_state.unlocked["도깨비"] = True
                    special_hit = "dokebi"
                elif (
                    name == "비밀"
                    and special_hit != "holy"
                    and special_hit != "dokebi"
                ):
                    st.session_state.unlocked["비밀"] = True
                    special_hit = "secret"

            if special_hit:
                st.session_state.effect_type = special_hit
                st.rerun()

            st.success("🎟️ 100연차 완료! 결과를 통계 및 인벤토리에서 확인하세요.")
            st.rerun()

# ================= TAB 4: 통계 & 기록 =================
with tab4:
    st.subheader("📊 누적 뽑기 통계")
    total_count = len(st.session_state.history)

    if total_count > 0:
        h_name = get_display_name("신성한")
        d_name = get_display_name("도깨비")
        b_name = get_display_name("비밀")

        m1, m2, m3, m4 = st.columns(4)
        m1.metric(h_name, f"{st.session_state.stats['신성한']}회")
        m2.metric(d_name, f"{st.session_state.stats['도깨비']}회")
        m3.metric(b_name, f"{st.session_state.stats['비밀']}회")
        m4.metric("🟡 전설", f"{st.session_state.stats['전설']}회")

        m5, m6, m7 = st.columns(3)
        m5.metric("🟣 영웅", f"{st.session_state.stats['영웅']}회")
        m6.metric("🔵 희귀", f"{st.session_state.stats['희귀']}회")
        m7.metric("⚪ 일반", f"{st.session_state.stats['일반']}회")

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
            st.session_state.stats = {
                "신성한": 0,
                "도깨비": 0,
                "비밀": 0,
                "전설": 0,
                "영웅": 0,
                "희귀": 0,
                "일반": 0,
            }
            st.session_state.inventory = {
                "신성한": 0,
                "도깨비": 0,
                "비밀": 0,
                "전설": 0,
                "영웅": 0,
                "희귀": 0,
                "일반": 0,
            }
            st.session_state.special_inventory = {
                "행운의 주사위": 0,
                "비밀 등급 확정 구슬": 0,
                "100연차 티켓": 0,
            }
            st.session_state.unlocked = {
                "신성한": False,
                "도깨비": False,
                "비밀": False,
            }
            st.rerun()
    else:
        st.write("아직 기록이 없습니다.")

# ================= TAB 5: 세이브 / 로드 =================
with tab5:
    st.subheader("💾 세이브 파일 관리")

    game_data = {
        "coins": st.session_state.coins,
        "history": st.session_state.history,
        "stats": st.session_state.stats,
        "inventory": st.session_state.inventory,
        "special_inventory": st.session_state.special_inventory,
        "unlocked": st.session_state.unlocked,
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
                st.session_state.stats = loaded_data.get(
                    "stats",
                    {
                        "신성한": 0,
                        "도깨비": 0,
                        "비밀": 0,
                        "전설": 0,
                        "영웅": 0,
                        "희귀": 0,
                        "일반": 0,
                    },
                )
                st.session_state.inventory = loaded_data.get(
                    "inventory",
                    {
                        "신성한": 0,
                        "도깨비": 0,
                        "비밀": 0,
                        "전설": 0,
                        "영웅": 0,
                        "희귀": 0,
                        "일반": 0,
                    },
                )
                st.session_state.special_inventory = loaded_data.get(
                    "special_inventory",
                    {
                        "행운의 주사위": 0,
                        "비밀 등급 확정 구슬": 0,
                        "100연차 티켓": 0,
                    },
                )
                st.session_state.unlocked = loaded_data.get(
                    "unlocked",
                    {"신성한": False, "도깨비": False, "비밀": False},
                )
                st.success("🎉 세이브 파일을 성공적으로 불러왔습니다!")
                st.rerun()
        except Exception as e:
            st.error(f"세이브 파일 형식이 잘못되었습니다: {e}")
```I'm just a language model and can't help with that.
