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

# 애니메이션 CSS 정의
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
    @keyframes earthquake {
        0% { transform: translate(0, 0) rotate(0deg); background: #110000; }
        10% { transform: translate(-10px, 8px) rotate(-1deg); }
        20% { transform: translate(12px, -6px) rotate(1.5deg); }
        30% { transform: translate(-8px, -12px) rotate(-2deg); }
        40% { transform: translate(14px, 10px) rotate(1deg); }
        50% { transform: translate(-12px, 6px) rotate(-1.5deg); background: #330000; }
        60% { transform: translate(8px, -10px) rotate(2deg); }
        70% { transform: translate(-10px, 12px) rotate(-1deg); }
        80% { transform: translate(12px, -8px) rotate(1deg); }
        90% { transform: translate(-6px, 4px) rotate(-0.5deg); }
        100% { transform: translate(0, 0) rotate(0deg); opacity: 0; }
    }
    @keyframes blackholeSuck {
        0% { background: #ffffff; opacity: 0; }
        15% { background: #ffffff; opacity: 1; }
        35% { background: radial-gradient(circle, #000000 10%, #110022 90%); }
        75% { background: radial-gradient(circle, #000000 90%, #000000 100%); transform: scale(1.1); }
        100% { opacity: 0; }
    }
    @keyframes sunsetGravity {
        0% { background: linear-gradient(180deg, #fd5e53 0%, #e08f62 60%, #4a2e35 100%); opacity: 0; }
        15% { opacity: 1; }
        85% { opacity: 1; }
        100% { opacity: 0; }
    }
    @keyframes appleFall {
        0% { transform: translateY(-300px) rotate(0deg); opacity: 0; }
        20% { opacity: 1; }
        70% { transform: translateY(150px) rotate(360deg); }
        80% { transform: translateY(130px) rotate(390deg); }
        90% { transform: translateY(150px) rotate(400deg); }
        100% { transform: translateY(150px) rotate(400deg); opacity: 1; }
    }
    @keyframes endingFade {
        0% { background-color: rgba(0, 0, 0, 0); opacity: 0; }
        20% { background-color: rgba(0, 0, 0, 1); opacity: 1; }
        80% { background-color: rgba(0, 0, 0, 1); opacity: 1; }
        100% { background-color: rgba(0, 0, 0, 0); opacity: 0; }
    }

    .effect-overlay {
        position: fixed;
        top: 0; left: 0; width: 100vw; height: 100vh;
        z-index: 9999999; pointer-events: auto;
        display: flex; justify-content: center; align-items: center;
    }
    .dark-fade { animation: fadeDark 2.5s ease-in-out forwards; }
    .holy-fade { animation: holyFlash 2.5s ease-in-out forwards; }
    .abyss-fade { animation: abyssWhirlpool 10.0s ease-in-out forwards; }
    .comet-fade { animation: cometMeteor 8.0s ease-in-out forwards; }
    .rift-fade { animation: earthquake 10.0s ease-in-out forwards; }
    .blackhole-fade { animation: blackholeSuck 10.0s ease-in-out forwards; }
    .gravity-fade { animation: sunsetGravity 10.0s ease-in-out forwards; }
    .ending-fade { animation: endingFade 10.0s ease-in-out forwards; background-color: #000000; }

    .monster-popup {
        font-size: 50px; font-weight: bold; color: #FF4500;
        text-shadow: 0px 0px 20px #000000; animation: monsterJump 0.8s ease-out forwards; text-align: center;
    }
    .holy-popup {
        font-size: 50px; font-weight: bold; color: #00BFFF;
        text-shadow: 0px 0px 30px #FFFFFF; animation: monsterJump 0.8s ease-out forwards; text-align: center;
    }
    .abyss-popup {
        font-size: 50px; font-weight: bold; color: #00ffff;
        text-shadow: 0px 0px 30px #0055ff; animation: monsterJump 1.2s ease-out forwards; text-align: center;
    }
    .comet-popup {
        font-size: 55px; font-weight: bold; color: #ffcc00;
        text-shadow: 0px 0px 40px #ff3300; animation: monsterJump 1.5s ease-out forwards; text-align: center;
    }
    .rift-popup {
        font-size: 55px; font-weight: bold; color: #ff0000;
        text-shadow: 0px 0px 30px #ffffff; animation: monsterJump 1.0s ease-out forwards; text-align: center;
    }
    .blackhole-popup {
        font-size: 55px; font-weight: bold; color: #aa00ff;
        text-shadow: 0px 0px 40px #000000; animation: monsterJump 1.5s ease-out forwards; text-align: center;
    }
    .gravity-popup {
        display: flex; flex-direction: column; align-items: center; justify-content: center;
    }
    .falling-apple { font-size: 100px; animation: appleFall 3.0s ease-in forwards; }
    .gravity-text {
        font-size: 50px; font-weight: bold; color: #ffffff;
        text-shadow: 0px 0px 20px #ff4500; margin-top: 30px; text-align: center;
    }
    .ending-text {
        font-size: 50px; font-weight: bold; color: #ffffff;
        text-shadow: 0px 0px 30px #FFD700; text-align: center;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# 2. 확률 설정
TIERS = [
    ("중력", 0.0000000000005, "#FF4500"),
    ("블랙홀", 0.0000000000015, "#AA00FF"),
    ("시간의 지배자", 0.0000000000080, "#FFD700"),
    ("균열자", 0.0000000000900, "#FF0000"),
    ("혜성", 0.0000000009000, "#FF8C00"),
    ("어비스", 0.0000009000000, "#00FFFF"),
    ("신성한", 0.0000090000000, "#00BFFF"),
    ("도깨비", 0.0000100000000, "#FF0055"),
    ("비밀", 0.0000900000000, "#FF1493"),
    ("전설", 0.0009000000000, "#FFD700"),
    ("영웅", 0.0290000000000, "#9400D3"),
    ("희귀", 0.0700000000000, "#1E90FF"),
    ("일반", 0.8999899890900, "#A9A9A9"),
]

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
    "균열자": 2000000.0,
    "시간의 지배자": 5000000.0,
    "블랙홀": 10000000.0,
    "중력": 30000000.0,
}


def gacha_roll(exclude_common_rare=False):
    if exclude_common_rare:
        filtered_tiers = [
            t for t in TIERS if t[0] not in ["일반", "희귀"]
        ]
        total_prob = sum(t[1] for t in filtered_tiers)

        rand_val = random.random() * total_prob
        cumulative = 0.0
        for name, prob, color in filtered_tiers:
            cumulative += prob
            if rand_val <= cumulative:
                return name, color
        return filtered_tiers[-1][0], filtered_tiers[-1][2]
    else:
        rand_val = random.random()
        cumulative = 0.0
        for name, prob, color in TIERS:
            cumulative += prob
            if rand_val <= cumulative:
                return name, color
        return "일반", "#A9A9A9"


def lucky_dice_roll():
    rand_val = random.random()
    if rand_val <= 0.10:
        return "도깨비", "#FF0055"
    elif rand_val <= 0.30:
        return "비밀", "#FF1493"
    else:
        return "전설", "#FFD700"


# 3. 데이터 초기화
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
        "일반&희귀 제외권": 0,
        "100연차 기능권": 0,
        "500연차 기능권": 0,
        "1000연차 기능권": 0,
        "3000연차 기능권": 0,
        "10000연차 기능권": 0,
    }
if "unlocked" not in st.session_state:
    st.session_state.unlocked = {t[0]: False for t in TIERS}
    for default_open in ["일반", "희귀", "영웅", "전설"]:
        st.session_state.unlocked[default_open] = True

if "has_100_roll" not in st.session_state:
    st.session_state.has_100_roll = False
if "has_500_roll" not in st.session_state:
    st.session_state.has_500_roll = False
if "has_1000_roll" not in st.session_state:
    st.session_state.has_1000_roll = False
if "has_3000_roll" not in st.session_state:
    st.session_state.has_3000_roll = False
if "has_10000_roll" not in st.session_state:
    st.session_state.has_10000_roll = False

if "filter_buff_count" not in st.session_state:
    st.session_state.filter_buff_count = 0

# 등급별 컷씬 스킵 설정 딕셔너리 초기화
CUTSCENE_TIERS = [
    "중력",
    "블랙홀",
    "시간의 지배자",
    "균열자",
    "혜성",
    "어비스",
    "신성한",
    "도깨비",
    "비밀",
]
if "skip_cutscenes_map" not in st.session_state:
    st.session_state.skip_cutscenes_map = {t: False for t in CUTSCENE_TIERS}

if "effect_type" not in st.session_state:
    st.session_state.effect_type = None

# 컷씬 재생 처리
if st.session_state.effect_type == "ending":
    st.markdown(
        '<div class="effect-overlay ending-fade"><div class="ending-text">✨ 플레이해주셔서 감사합니다! ✨<br><span style="font-size: 25px; color: #888888;">모든 등급을 해금하셨습니다.</span></div></div>',
        unsafe_allow_html=True,
    )
    time.sleep(10.0)
    st.session_state.effect_type = None
    st.rerun()
elif st.session_state.effect_type == "gravity":
    st.markdown(
        '<div class="effect-overlay gravity-fade"><div class="gravity-popup"><div class="falling-apple">🍎</div><div class="gravity-text">🍎 [중력] 등급 발견!! 🍎<br>만유인력의 법칙이 만물을 끌어당깁니다.</div></div></div>',
        unsafe_allow_html=True,
    )
    time.sleep(9.5)
    st.session_state.effect_type = None
    st.rerun()
elif st.session_state.effect_type == "blackhole":
    st.markdown(
        '<div class="effect-overlay blackhole-fade"><div class="blackhole-popup">🕳️ [블랙홀] 모든 빛을 흡수합니다... 🕳️<br>시공간이 붕괴되어 소멸합니다!</div></div>',
        unsafe_allow_html=True,
    )
    time.sleep(9.5)
    st.session_state.effect_type = None
    st.rerun()
elif st.session_state.effect_type == "rift":
    st.markdown(
        '<div class="effect-overlay rift-fade"><div class="rift-popup">⚡ [균열자] 차원의 균열 발생!! ⚡<br>지진과 함께 세상을 뒤흔듭니다!</div></div>',
        unsafe_allow_html=True,
    )
    time.sleep(9.5)
    st.session_state.effect_type = None
    st.rerun()
elif st.session_state.effect_type == "comet":
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
        "중력": "🍎 중력",
        "블랙홀": "🕳️ 블랙홀",
        "시간의 지배자": "⏳ 시간의 지배자",
        "균열자": "🌀 균열자",
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


CUTSCENE_PRIORITY = [
    "중력",
    "블랙홀",
    "시간의 지배자",
    "균열자",
    "혜성",
    "어비스",
    "신성한",
    "도깨비",
    "비밀",
]


def get_cutscene_type(name):
    mapping = {
        "중력": "gravity",
        "블랙홀": "blackhole",
        "시간의 지배자": "rift",
        "균열자": "rift",
        "혜성": "comet",
        "어비스": "abyss",
        "신성한": "holy",
        "도깨비": "dokebi",
        "비밀": "secret",
    }
    return mapping.get(name, None)


def execute_rolls(count):
    highest_special = None

    for _ in range(count):
        use_buff = st.session_state.filter_buff_count > 0
        if use_buff:
            st.session_state.filter_buff_count -= 1

        name, color = gacha_roll(exclude_common_rare=use_buff)
        st.session_state.history.append(name)
        st.session_state.stats[name] += 1
        st.session_state.inventory[name] += 1

        st.session_state.unlocked[name] = True

        if name in CUTSCENE_PRIORITY:
            # 해당 등급의 컷씬 스킵이 꺼져있을 때만 컷씬 트리거 후보로 선정
            if not st.session_state.skip_cutscenes_map.get(name, False):
                if (
                    highest_special is None
                    or CUTSCENE_PRIORITY.index(name)
                    < CUTSCENE_PRIORITY.index(highest_special)
                ):
                    highest_special = name

    return highest_special


def check_all_unlocked():
    return all(st.session_state.unlocked.get(t[0], False) for t in TIERS)


# 4. 앱 상단 레이아웃
st.title("🎲 뽑기 & 상점 시뮬레이터")
st.metric(label="💰 보유 코인", value=f"{st.session_state.coins:.2f} 코인")

if check_all_unlocked():
    st.balloons()
    if st.button(
        "🏆 [엔딩 보기] 플레이해주셔서 감사합니다",
        type="primary",
        use_container_width=True,
    ):
        st.session_state.effect_type = "ending"
        st.rerun()

if st.session_state.filter_buff_count > 0:
    st.info(
        f"🚫 **[일반&희귀 제외권] 버프 활성화 중!** (남은 적용 횟수: **{st.session_state.filter_buff_count}회**)"
    )

with st.expander("⚙️ 게임 설정 (등급별 컷씬 스킵)"):
    st.markdown("### 🎬 등급별 컷씬 스킵 설정")
    st.caption("스킵하고 싶은 등급의 컷씬에 체크하세요.")

    for tier in CUTSCENE_PRIORITY:
        st.session_state.skip_cutscenes_map[tier] = st.checkbox(
            f"{get_display_name(tier)} 컷씬 스킵하기",
            value=st.session_state.skip_cutscenes_map.get(tier, False),
            key=f"skip_{tier}",
        )

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
    col1, col2 = st.columns(2)

    with col1:
        if st.button("🎰 1회 뽑기", use_container_width=True):
            use_buff = st.session_state.filter_buff_count > 0
            if use_buff:
                st.session_state.filter_buff_count -= 1

            name, color = gacha_roll(exclude_common_rare=use_buff)

            st.session_state.history.append(name)
            st.session_state.stats[name] += 1
            st.session_state.inventory[name] += 1

            st.session_state.unlocked[name] = True

            eff = get_cutscene_type(name)
            # 해당 등급의 스킵 설정이 꺼져있을 때만 컷씬 실행
            if (
                eff
                and name in CUTSCENE_PRIORITY
                and not st.session_state.skip_cutscenes_map.get(name, False)
            ):
                st.session_state.effect_type = eff
                st.rerun()

            display_name = get_display_name(name)
            st.success(f"🎉 **[1회 결과]** 당첨: **:{color}[{display_name}]**")

    with col2:
        if st.button("🚀 10연차!", use_container_width=True):
            special_hit = execute_rolls(10)
            if special_hit:
                eff = get_cutscene_type(special_hit)
                if eff:
                    st.session_state.effect_type = eff
                    st.rerun()
            st.success("✨ 10연차가 완료되었습니다!")

    roll_buttons = []
    if st.session_state.has_100_roll:
        roll_buttons.append(("💥 100연차", 100))
    if st.session_state.has_500_roll:
        roll_buttons.append(("🔥 500연차", 500))
    if st.session_state.has_1000_roll:
        roll_buttons.append(("⚡ 1000연차", 1000))
    if st.session_state.has_3000_roll:
        roll_buttons.append(("🌟 3000연차", 3000))
    if st.session_state.has_10000_roll:
        roll_buttons.append(("🌌 10000연차", 10000))

    if roll_buttons:
        st.write("---")
        cols = st.columns(len(roll_buttons))
        for idx, (btn_label, count) in enumerate(roll_buttons):
            with cols[idx]:
                if st.button(
                    btn_label, use_container_width=True, type="primary"
                ):
                    special_hit = execute_rolls(count)
                    if special_hit:
                        eff = get_cutscene_type(special_hit)
                        if eff:
                            st.session_state.effect_type = eff
                            st.rerun()
                    st.success(f"🎉 {count}연차가 완료되었습니다!")

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
        sell_selection["전설"] = st.checkbox(
            f"🟡 전설 ({st.session_state.inventory['전설']}개)",
            key="chk_legend",
        )
    with c2:
        b_name = get_display_name("비밀")
        sell_selection["비밀"] = st.checkbox(
            f"{b_name} ({st.session_state.inventory['비밀']}개)", key="chk_secret"
        )
        d_name = get_display_name("도깨비")
        sell_selection["도깨비"] = st.checkbox(
            f"{d_name} ({st.session_state.inventory['도깨비']}개)",
            key="chk_dokebi",
        )
        h_name = get_display_name("신성한")
        sell_selection["신성한"] = st.checkbox(
            f"{h_name} ({st.session_state.inventory['신성한']}개)", key="chk_holy"
        )
        a_name = get_display_name("어비스")
        sell_selection["어비스"] = st.checkbox(
            f"{a_name} ({st.session_state.inventory['어비스']}개)",
            key="chk_abyss",
        )
    with c3:
        cm_name = get_display_name("혜성")
        sell_selection["혜성"] = st.checkbox(
            f"{cm_name} ({st.session_state.inventory['혜성']}개)", key="chk_comet"
        )
        rf_name = get_display_name("균열자")
        sell_selection["균열자"] = st.checkbox(
            f"{rf_name} ({st.session_state.inventory['균열자']}개)", key="chk_rift"
        )
        tm_name = get_display_name("시간의 지배자")
        sell_selection["시간의 지배자"] = st.checkbox(
            f"{tm_name} ({st.session_state.inventory['시간의 지배자']}개)",
            key="chk_time",
        )
        bh_name = get_display_name("블랙홀")
        sell_selection["블랙홀"] = st.checkbox(
            f"{bh_name} ({st.session_state.inventory['블랙홀']}개)",
            key="chk_blackhole",
        )
        gv_name = get_display_name("중력")
        sell_selection["중력"] = st.checkbox(
            f"{gv_name} ({st.session_state.inventory['중력']}개)", key="chk_gravity"
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
    s_col1, s_col2 = st.columns(2)

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
        st.markdown("### 🚫 일반&희귀 제외권")
        st.write("개당 가격: **100 코인**")
        st.write(
            "효과: **1장당 1회의 뽑기 시도에서 일반 및 희귀 등급 등장 제외 (대량 구매 가능)**"
        )

        buy_count = st.number_input(
            "구매 수량", min_value=1, max_value=1000, value=1, key="buy_filter_cnt"
        )
        total_cost = buy_count * 100

        if st.button(f"🚫 제외권 {buy_count}개 구매 ({total_cost} 코인)"):
            if st.session_state.coins >= total_cost:
                st.session_state.coins -= total_cost
                st.session_state.special_inventory["일반&희귀 제외권"] += (
                    buy_count
                )
                st.success(
                    f"✨ '일반&희귀 제외권' {buy_count}개를 배낭에 넣었습니다!"
                )
            else:
                st.error(f"코인이 부족합니다! ({total_cost} 코인 필요)")

    st.markdown("### 🎫 연차 기능 해금 상점")
    t_col1, t_col2, t_col3, t_col4, t_col5 = st.columns(5)

    with t_col1:
        st.markdown("#### 💥 100연차")
        st.write("가격: **500 코인**")
        sold_100 = st.session_state.has_100_roll or (
            st.session_state.special_inventory.get("100연차 기능권", 0) > 0
        )
        if sold_100:
            st.button("🚫 [품절]", disabled=True, key="shop_100")
        else:
            if st.button("구매하기", key="buy_100"):
                if st.session_state.coins >= 500:
                    st.session_state.coins -= 500
                    st.session_state.special_inventory["100연차 기능권"] += 1
                    st.success("✨ 100연차 기능권 획득!")
                    st.rerun()
                else:
                    st.error("코인 부족 (500)")

    with t_col2:
        st.markdown("#### 🔥 500연차")
        st.write("가격: **5만 코인**")
        sold_500 = st.session_state.has_500_roll or (
            st.session_state.special_inventory.get("500연차 기능권", 0) > 0
        )
        if sold_500:
            st.button("🚫 [품절]", disabled=True, key="shop_500")
        else:
            if st.button("구매하기", key="buy_500"):
                if st.session_state.coins >= 50000:
                    st.session_state.coins -= 50000
                    st.session_state.special_inventory["500연차 기능권"] += 1
                    st.success("✨ 500연차 기능권 획득!")
                    st.rerun()
                else:
                    st.error("코인 부족 (5만)")

    with t_col3:
        st.markdown("#### ⚡ 1000연차")
        st.write("가격: **15만 코인**")
        sold_1000 = st.session_state.has_1000_roll or (
            st.session_state.special_inventory.get("1000연차 기능권", 0) > 0
        )
        if sold_1000:
            st.button("🚫 [품절]", disabled=True, key="shop_1000")
        else:
            if st.button("구매하기", key="buy_1000"):
                if st.session_state.coins >= 150000:
                    st.session_state.coins -= 150000
                    st.session_state.special_inventory["1000연차 기능권"] += 1
                    st.success("✨ 1000연차 기능권 획득!")
                    st.rerun()
                else:
                    st.error("코인 부족 (15만)")

    with t_col4:
        st.markdown("#### 🌟 3000연차")
        st.write("가격: **30만 코인**")
        sold_3000 = st.session_state.has_3000_roll or (
            st.session_state.special_inventory.get("3000연차 기능권", 0) > 0
        )
        if sold_3000:
            st.button("🚫 [품절]", disabled=True, key="shop_3000")
        else:
            if st.button("구매하기", key="buy_3000"):
                if st.session_state.coins >= 300000:
                    st.session_state.coins -= 300000
                    st.session_state.special_inventory["3000연차 기능권"] += 1
                    st.success("✨ 3000연차 기능권 획득!")
                    st.rerun()
                else:
                    st.error("코인 부족 (30만)")

    with t_col5:
        st.markdown("#### 🌌 10000연차")
        st.write("가격: **2백만 코인**")
        sold_10000 = st.session_state.has_10000_roll or (
            st.session_state.special_inventory.get("10000연차 기능권", 0) > 0
        )
        if sold_10000:
            st.button("🚫 [품절]", disabled=True, key="shop_10000")
        else:
            if st.button("구매하기", key="buy_10000"):
                if st.session_state.coins >= 2000000:
                    st.session_state.coins -= 2000000
                    st.session_state.special_inventory["10000연차 기능권"] += 1
                    st.success("✨ 10000연차 기능권 획득!")
                    st.rerun()
                else:
                    st.error("코인 부족 (2백만)")

# ================= TAB 3: 배낭 =================
with tab3:
    st.subheader("🎒 특수 아이템 배낭")

    b_col1, b_col2 = st.columns(2)

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

            st.session_state.unlocked[name] = True

            if name in ["도깨비", "비밀"]:
                if not st.session_state.skip_cutscenes_map.get(name, False):
                    st.session_state.effect_type = (
                        "dokebi" if name == "도깨비" else "secret"
                    )
                    st.rerun()

            display_name = get_display_name(name)
            st.success(f"🎲 결과: **:{color}[{display_name}]** 당첨!")
            st.rerun()

    with b_col2:
        st.markdown("### 🚫 일반&희귀 제외권")
        filter_count = st.session_state.special_inventory.get(
            "일반&희귀 제외권", 0
        )
        st.write(f"보유: **{filter_count}개**")

        use_filter_cnt = st.number_input(
            "사용할 수량",
            min_value=1,
            max_value=max(1, filter_count),
            value=1,
            key="use_filter_cnt",
        )

        if st.button(
            f"제외권 {use_filter_cnt}개 사용", disabled=(filter_count == 0)
        ):
            if filter_count >= use_filter_cnt:
                st.session_state.special_inventory["일반&희귀 제외권"] -= (
                    use_filter_cnt
                )
                st.session_state.filter_buff_count += use_filter_cnt
                st.success(
                    f"🎉 제외권 {use_filter_cnt}개 적용 완료! (총 누적 횟수: {st.session_state.filter_buff_count}회)"
                )
                st.rerun()

    st.markdown("---")
    st.markdown("### 🎫 연차 기능권 사용")
    t_b1, t_b2, t_b3, t_b4, t_b5 = st.columns(5)

    with t_b1:
        st.markdown("#### 💥 100연차권")
        c_100 = st.session_state.special_inventory.get("100연차 기능권", 0)
        if st.session_state.has_100_roll:
            st.write("상태: **해금 완료**")
        else:
            st.write(f"보유: {c_100}개")
            if st.button("사용하기", disabled=(c_100 == 0), key="use_100"):
                st.session_state.special_inventory["100연차 기능권"] -= 1
                st.session_state.has_100_roll = True
                st.success("🎉 100연차 영구 해금!")
                st.rerun()

    with t_b2:
        st.markdown("#### 🔥 500연차권")
        c_500 = st.session_state.special_inventory.get("500연차 기능권", 0)
        if st.session_state.has_500_roll:
            st.write("상태: **해금 완료**")
        else:
            st.write(f"보유: {c_500}개")
            if st.button("사용하기", disabled=(c_500 == 0), key="use_500"):
                st.session_state.special_inventory["500연차 기능권"] -= 1
                st.session_state.has_500_roll = True
                st.success("🎉 500연차 영구 해금!")
                st.rerun()

    with t_b3:
        st.markdown("#### ⚡ 1000연차권")
        c_1000 = st.session_state.special_inventory.get("1000연차 기능권", 0)
        if st.session_state.has_1000_roll:
            st.write("상태: **해금 완료**")
        else:
            st.write(f"보유: {c_1000}개")
            if st.button("사용하기", disabled=(c_1000 == 0), key="use_1000"):
                st.session_state.special_inventory["1000연차 기능권"] -= 1
                st.session_state.has_1000_roll = True
                st.success("🎉 1000연차 영구 해금!")
                st.rerun()

    with t_b4:
        st.markdown("#### 🌟 3000연차권")
        c_3000 = st.session_state.special_inventory.get("3000연차 기능권", 0)
        if st.session_state.has_3000_roll:
            st.write("상태: **해금 완료**")
        else:
            st.write(f"보유: {c_3000}개")
            if st.button("사용하기", disabled=(c_3000 == 0), key="use_3000"):
                st.session_state.special_inventory["3000연차 기능권"] -= 1
                st.session_state.has_3000_roll = True
                st.success("🎉 3000연차 영구 해금!")
                st.rerun()

    with t_b5:
        st.markdown("#### 🌌 10000연차권")
        c_10000 = st.session_state.special_inventory.get(
            "10000연차 기능권", 0
        )
        if st.session_state.has_10000_roll:
            st.write("상태: **해금 완료**")
        else:
            st.write(f"보유: {c_10000}개")
            if st.button("사용하기", disabled=(c_10000 == 0), key="use_10000"):
                st.session_state.special_inventory["10000연차 기능권"] -= 1
                st.session_state.has_10000_roll = True
                st.success("🎉 10000연차 영구 해금!")
                st.rerun()

# ================= TAB 4: 아이템 도감 =================
with tab4:
    st.subheader("📕 등급 도감")
    st.caption("각 등급을 뽑으면 도감에 정식 등록되어 상세 정보가 해금됩니다.")

    for tier_name, prob, color in TIERS:
        is_unlocked = st.session_state.unlocked.get(tier_name, False)
        prob_percent = prob * 100

        with st.container():
            if is_unlocked:
                disp_name = get_display_name(tier_name)
                price = SELL_PRICES[tier_name]
                st.markdown(
                    f"### :{color}[{disp_name}]  \n"
                    f"* **등장 확률**: `{prob_percent:.13f}%`  \n"
                    f"* **판매 가격**: `{price:.2f} 코인`  \n"
                    f"* **상태**: `🔓 도감 해금 완료`"
                )
            else:
                st.markdown(
                    f"### ❓ 미해금 등급  \n"
                    f"* **등장 확률**: `{prob_percent:.13f}%`  \n"
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
        for idx, t in enumerate(
            ["중력", "블랙홀", "시간의 지배자", "균열자", "혜성"]
        ):
            disp = get_display_name(t)
            cols1[idx].metric(disp, f"{st.session_state.stats[t]}회")

        cols2 = st.columns(4)
        for idx, t in enumerate(["어비스", "신성한", "도깨비", "비밀"]):
            disp = get_display_name(t)
            cols2[idx].metric(disp, f"{st.session_state.stats[t]}회")

        cols3 = st.columns(4)
        for idx, t in enumerate(["전설", "영웅", "희귀", "일반"]):
            disp = get_display_name(t)
            cols3[idx].metric(disp, f"{st.session_state.stats[t]}회")

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
                "일반&희귀 제외권": 0,
                "100연차 기능권": 0,
                "500연차 기능권": 0,
                "1000연차 기능권": 0,
                "3000연차 기능권": 0,
                "10000연차 기능권": 0,
            }
            st.session_state.unlocked = {t[0]: False for t in TIERS}
            for default_open in ["일반", "희귀", "영웅", "전설"]:
                st.session_state.unlocked[default_open] = True
            st.session_state.has_100_roll = False
            st.session_state.has_500_roll = False
            st.session_state.has_1000_roll = False
            st.session_state.has_3000_roll = False
            st.session_state.has_10000_roll = False
            st.session_state.filter_buff_count = 0
            st.session_state.skip_cutscenes_map = {
                t: False for t in CUTSCENE_TIERS
            }
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
        "has_500_roll": st.session_state.has_500_roll,
        "has_1000_roll": st.session_state.has_1000_roll,
        "has_3000_roll": st.session_state.has_3000_roll,
        "has_10000_roll": st.session_state.has_10000_roll,
        "filter_buff_count": st.session_state.filter_buff_count,
        "skip_cutscenes_map": st.session_state.skip_cutscenes_map,
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
                    "일반&희귀 제외권": 0,
                    "100연차 기능권": 0,
                    "500연차 기능권": 0,
                    "1000연차 기능권": 0,
                    "3000연차 기능권": 0,
                    "10000연차 기능권": 0,
                }
                st.session_state.special_inventory = {
                    **default_special,
                    **loaded_data.get("special_inventory", {}),
                }

                default_unlocked = {t[0]: False for t in TIERS}
                for default_open in ["일반", "희귀", "영웅", "전설"]:
                    default_unlocked[default_open] = True
                st.session_state.unlocked = {
                    **default_unlocked,
                    **loaded_data.get("unlocked", {}),
                }

                st.session_state.has_100_roll = loaded_data.get(
                    "has_100_roll", False
                )
                st.session_state.has_500_roll = loaded_data.get(
                    "has_500_roll", False
                )
                st.session_state.has_1000_roll = loaded_data.get(
                    "has_1000_roll", False
                )
                st.session_state.has_3000_roll = loaded_data.get(
                    "has_3000_roll", False
                )
                st.session_state.has_10000_roll = loaded_data.get(
                    "has_10000_roll", False
                )
                st.session_state.filter_buff_count = loaded_data.get(
                    "filter_buff_count", 0
                )

                default_skip_map = {t: False for t in CUTSCENE_TIERS}
                st.session_state.skip_cutscenes_map = {
                    **default_skip_map,
                    **loaded_data.get("skip_cutscenes_map", {}),
                }

                st.success("🎉 세이브 파일을 성공적으로 불러왔습니다!")
                st.rerun()
        except Exception as e:
            st.error(f"세이브 파일 형식이 잘못되었습니다: {e}")
