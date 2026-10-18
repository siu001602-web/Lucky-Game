import json
import random
import time
import streamlit as st

st.set_page_config(
    page_title="두근두근 뽑기 & 상점 시뮬레이터",
    page_icon="🎲",
    layout="centered",
)

st.markdown(
    """
    <style>
    @keyframes fadeDark { 0% { background-color: rgba(0,0,0,0); } 25%, 75% { background-color: rgba(0,0,0,0.98); } 100% { background-color: rgba(0,0,0,0); } }
    @keyframes monsterJump { 0% { transform: scale(0.2); opacity: 0; } 50% { transform: scale(1.2); opacity: 1; } 100% { transform: scale(1.0); opacity: 1; } }
    @keyframes holyFlash { 0% { background-color: rgba(0,0,0,0); } 40%, 80% { background-color: rgba(255,255,255,1); } 100% { background-color: rgba(0,0,0,0); } }
    @keyframes abyssWhirlpool { 0% { opacity: 0; transform: scale(0.8); } 50% { opacity: 1; transform: rotate(180deg) scale(1); } 100% { opacity: 0; transform: scale(1.2); } }
    @keyframes cometMeteor { 0% { opacity: 0; } 30%, 70% { opacity: 1; } 100% { opacity: 0; } }
    @keyframes earthquake { 0%, 100% { transform: translate(0, 0); } 50% { transform: translate(10px, -10px); } }
    @keyframes blackholeSuck { 0% { opacity: 0; } 50% { opacity: 1; transform: scale(1.1); } 100% { opacity: 0; } }
    @keyframes sunsetGravity { 0%, 100% { opacity: 0; } 50% { opacity: 1; } }
    @keyframes appleFall { 0% { transform: translateY(-300px); opacity: 0; } 100% { transform: translateY(150px); opacity: 1; } }
    @keyframes endingFade { 0%, 100% { opacity: 0; background-color: rgba(0,0,0,0); } 50% { opacity: 1; background-color: #000; } }

    .effect-overlay { position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; z-index: 9999999; display: flex; justify-content: center; align-items: center; pointer-events: none; }
    .dark-fade { animation: fadeDark 2.5s ease-in-out forwards; }
    .holy-fade { animation: holyFlash 2.5s ease-in-out forwards; }
    .abyss-fade { animation: abyssWhirlpool 8.0s ease-in-out forwards; }
    .comet-fade { animation: cometMeteor 6.0s ease-in-out forwards; }
    .rift-fade { animation: earthquake 5.0s ease-in-out forwards; }
    .blackhole-fade { animation: blackholeSuck 6.0s ease-in-out forwards; }
    .gravity-fade { animation: sunsetGravity 6.0s ease-in-out forwards; }
    .ending-fade { animation: endingFade 8.0s ease-in-out forwards; background-color: #000; }

    .monster-popup, .holy-popup, .abyss-popup, .comet-popup, .rift-popup, .blackhole-popup, .gravity-text, .ending-text {
        font-size: 45px; font-weight: bold; text-align: center; text-shadow: 0px 0px 20px #000; color: #FFF; animation: monsterJump 0.8s ease-out forwards;
    }
    .falling-apple { font-size: 100px; animation: appleFall 2.0s ease-in forwards; }
    </style>
""",
    unsafe_allow_html=True,
)

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

HIGH_TIERS = [
    "비밀",
    "도깨비",
    "신성한",
    "어비스",
    "혜성",
    "균열자",
    "시간의 지배자",
    "블랙홀",
    "중력",
]
TICKET_DEFS = [
    ("만배 행운권", 10000.0, 100),
    ("십만배 행운권", 100000.0, 1000),
    ("백만배 행운권", 1000000.0, 10000),
    ("천만배 행운권", 10000000.0, 30000),
]


def gacha_roll(multiplier=1.0):
    base_dict = {name: prob for name, prob, color in TIERS}
    color_dict = {name: color for name, prob, color in TIERS}

    if multiplier > 1.0:
        total_inc = 0.0
        for name in HIGH_TIERS:
            orig = base_dict[name]
            new_p = orig * multiplier
            total_inc += new_p - orig
            base_dict[name] = new_p

        c_sum = base_dict["일반"] + base_dict["희귀"]
        if c_sum > 0:
            ratio = max(0.0, (c_sum - total_inc) / c_sum)
            base_dict["일반"] *= ratio
            base_dict["희귀"] *= ratio

    adjusted = [(n, base_dict[n], color_dict[n]) for n, _, _ in TIERS]
    total_p = sum(t[1] for t in adjusted)
    rand_v = random.random() * total_p
    cum = 0.0
    for name, prob, color in adjusted:
        cum += prob
        if rand_v <= cum:
            return name, color
    return adjusted[-1][0], adjusted[-1][2]


# 세션 상태 초기화
defaults = {
    "coins": 0.0,
    "history": [],
    "stats": {t[0]: 0 for t in TIERS},
    "inventory": {t: 0 for t, _, _ in TIERS},
    "special_inventory": {
        "행운의 주사위": 0,
        "만배 행운권": 0,
        "십만배 행운권": 0,
        "백만배 행운권": 0,
        "천만배 행운권": 0,
        "100연차 기능권": 0,
        "500연차 기능권": 0,
        "1000연차 기능권": 0,
        "3000연차 기능권": 0,
        "10000연차 기능권": 0,
    },
    "unlocked": {
        t[0]: t[0] in ["일반", "희귀", "영웅", "전설"] for t in TIERS
    },
    "has_100_roll": False,
    "has_500_roll": False,
    "has_1000_roll": False,
    "has_3000_roll": False,
    "has_10000_roll": False,
    "active_multiplier": 1.0,
    "active_multiplier_count": 0,
    "balloons_shown": False,
    "effect_type": None,
    "skip_cutscenes_map": {t: False for t in HIGH_TIERS},
}

for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# 기존 세션에 inventory 키가 누락된 경우 안전하게 보정
for t, _, _ in TIERS:
    if t not in st.session_state.inventory:
        st.session_state.inventory[t] = 0

# 컷씬 처리
eff = st.session_state.effect_type
if eff:
    st.session_state.effect_type = None
    effects_html = {
        "ending": '<div class="effect-overlay ending-fade"><div class="ending-text">✨ 플레이해주셔서 감사합니다! ✨</div></div>',
        "gravity": '<div class="effect-overlay gravity-fade"><div class="gravity-text"><div class="falling-apple">🍎</div>[중력] 등급 발견!!</div></div>',
        "blackhole": '<div class="effect-overlay blackhole-fade"><div class="blackhole-popup">🕳️ [블랙홀] 시공간 붕괴!</div></div>',
        "rift": '<div class="effect-overlay rift-fade"><div class="rift-popup">⚡ [균열자] 차원 균열 발생!</div></div>',
        "comet": '<div class="effect-overlay comet-fade"><div class="comet-popup">☄️ [혜성] 우주 강림!</div></div>',
        "abyss": '<div class="effect-overlay abyss-fade"><div class="abyss-popup">🌊 [어비스] 심해 소용돌이!</div></div>',
        "holy": '<div class="effect-overlay holy-fade"><div class="holy-popup">✨ [신성한] 등급 강림!</div></div>',
        "secret": '<div class="effect-overlay dark-fade"><div class="monster-popup">💖 [비밀] 등급 획득!</div></div>',
        "dokebi": '<div class="effect-overlay dark-fade"><div class="monster-popup">👹 [도깨비] 출현!</div></div>',
    }
    if eff in effects_html:
        st.markdown(effects_html[eff], unsafe_allow_html=True)
        time.sleep(2.0 if eff not in ["gravity", "abyss", "rift"] else 6.0)
        st.rerun()


def get_display_name(name):
    if not st.session_state.unlocked.get(name, False):
        return "❓ ??"
    mapping = {
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
    return mapping.get(name, name)


def execute_rolls(count):
    highest = None
    for _ in range(count):
        mult = 1.0
        if st.session_state.active_multiplier_count > 0:
            mult = st.session_state.active_multiplier
            st.session_state.active_multiplier_count -= 1
            if st.session_state.active_multiplier_count == 0:
                st.session_state.active_multiplier = 1.0

        name, _ = gacha_roll(mult)
        st.session_state.history.append(name)
        st.session_state.stats[name] += 1
        st.session_state.inventory[name] += 1
        st.session_state.unlocked[name] = True

        if (
            name in HIGH_TIERS
            and not st.session_state.skip_cutscenes_map.get(name, False)
        ):
            if highest is None or HIGH_TIERS.index(name) < HIGH_TIERS.index(
                highest
            ):
                highest = name
    return highest


def check_all():
    return all(st.session_state.unlocked.get(t[0], False) for t in TIERS)


# 상단 UI
st.title("🎲 뽑기 & 상점 시뮬레이터")
st.metric(label="💰 보유 코인", value=f"{st.session_state.coins:.2f} 코인")

if check_all():
    if not st.session_state.balloons_shown:
        st.balloons()
        st.session_state.balloons_shown = True
    if st.button(
        "🏆 [엔딩 보기] 플레이해주셔서 감사합니다",
        type="primary",
        use_container_width=True,
    ):
        st.session_state.effect_type = "ending"
        st.rerun()

if st.session_state.active_multiplier_count > 0:
    m_val = st.session_state.active_multiplier
    st.info(
        f"🎟️ **[{int(m_val):,}배 행운 버프] 활성화 중!** (남은 횟수: **{st.session_state.active_multiplier_count}회**)"
    )

with st.expander("⚙️ 설정 (컷씬 스킵)"):
    for t in HIGH_TIERS:
        st.session_state.skip_cutscenes_map[t] = st.checkbox(
            f"{get_display_name(t)} 스킵",
            value=st.session_state.skip_cutscenes_map[t],
            key=f"skip_setting_{t}",
        )

st.divider()

tabs = st.tabs(
    ["🎰 뽑기", "🏪 상점", "🎒 배낭", "📕 도감", "📊 통계", "💾 세이브"]
)

# 1. 뽑기 탭
with tabs[0]:
    st.subheader("아이템 뽑기")
    c1, c2 = st.columns(2)
    with c1:
        if st.button("🎰 1회 뽑기", use_container_width=True):
            mult = (
                st.session_state.active_multiplier
                if st.session_state.active_multiplier_count > 0
                else 1.0
            )
            if mult > 1.0:
                st.session_state.active_multiplier_count -= 1
                if st.session_state.active_multiplier_count == 0:
                    st.session_state.active_multiplier = 1.0
            name, color = gacha_roll(mult)
            st.session_state.history.append(name)
            st.session_state.stats[name] += 1
            st.session_state.inventory[name] += 1
            st.session_state.unlocked[name] = True

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
            if (
                name in mapping
                and not st.session_state.skip_cutscenes_map.get(name, False)
            ):
                st.session_state.effect_type = mapping[name]
                st.rerun()
            st.success(f"🎉 **[1회]** 당첨: **:{color}[{get_display_name(name)}]**")

    with c2:
        if st.button("🚀 10연차!", use_container_width=True):
            hit = execute_rolls(10)
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
            if hit and not st.session_state.skip_cutscenes_map.get(hit, False):
                st.session_state.effect_type = mapping[hit]
                st.rerun()
            st.success("✨ 10연차 완료!")

    rolls_map = [
        ("has_100_roll", "💥 100연차", 100),
        ("has_500_roll", "🔥 500연차", 500),
        ("has_1000_roll", "⚡ 1000연차", 1000),
        ("has_3000_roll", "🌟 3000연차", 3000),
        ("has_10000_roll", "🌌 10000연차", 10000),
    ]
    active_rolls = [(lbl, cnt) for flag, lbl, cnt in rolls_map if st.session_state[flag]]
    if active_rolls:
        st.write("---")
        cols = st.columns(len(active_rolls))
        for idx, (lbl, cnt) in enumerate(active_rolls):
            with cols[idx]:
                if st.button(lbl, use_container_width=True, type="primary"):
                    execute_rolls(cnt)
                    st.success(f"🎉 {cnt}연차 완료!")

# 2. 상점 탭
with tabs[1]:
    st.subheader("💵 등급별 판매소")
    sell_sel = {}
    cols = st.columns(3)
    for i, (t_name, _, _) in enumerate(TIERS):
        with cols[i % 3]:
            sell_sel[t_name] = st.checkbox(
                f"{get_display_name(t_name)} ({st.session_state.inventory.get(t_name, 0)}개)",
                key=f"sell_{t_name}",
            )

    if st.button("💰 선택 아이템 판매", type="primary"):
        earned = sum(
            st.session_state.inventory.get(t, 0) * SELL_PRICES[t]
            for t, sel in sell_sel.items()
            if sel
        )
        for t, sel in sell_sel.items():
            if sel:
                st.session_state.inventory[t] = 0
        if earned > 0:
            st.session_state.coins += earned
            st.success(f"🎉 {earned:.2f} 코인 획득!")
            st.rerun()

    st.divider()
    st.subheader("🛒 Special 상점")
    buy_qty = st.number_input("행운권 일괄 구매 수량", 1, 1000, 1)

    t_cols = st.columns(2)
    with t_cols[0]:
        if st.button("🎲 주사위 구매 (800코인)"):
            if st.session_state.coins >= 800:
                st.session_state.coins -= 800
                st.session_state.special_inventory["행운의 주사위"] += 1
                st.success("구매 완료!")
            else:
                st.error("코인 부족!")

    for name, _, price in TICKET_DEFS:
        cost = price * buy_qty
        if st.button(f"🎟️ {name} {buy_qty}장 ({cost:,}코인)", key=f"buy_{name}"):
            if st.session_state.coins >= cost:
                st.session_state.coins -= cost
                st.session_state.special_inventory[name] += buy_qty
                st.success("구매 완료!")
            else:
                st.error("코인 부족!")

    # 연차 상점
    st.markdown("### 🎫 연차 해금 상점")
    t_shop = [
        ("has_100_roll", "💥 100연차", 500, "100연차 기능권"),
        ("has_500_roll", "🔥 500연차", 50000, "500연차 기능권"),
        ("has_1000_roll", "⚡ 1000연차", 150000, "1000연차 기능권"),
        ("has_3000_roll", "🌟 3000연차", 300000, "3000연차 기능권"),
        ("has_10000_roll", "🌌 10000연차", 2000000, "10000연차 기능권"),
    ]
    s_cols = st.columns(5)
    for idx, (flag, title, price, key_name) in enumerate(t_shop):
        with s_cols[idx]:
            st.markdown(f"#### {title}")
            if st.session_state[flag]:
                st.button("품절", disabled=True, key=f"s_{idx}")
            else:
                if st.button(f"{price:,}코인", key=f"b_{idx}"):
                    if st.session_state.coins >= price:
                        st.session_state.coins -= price
                        st.session_state.special_inventory[key_name] += 1
                        st.session_state[flag] = True
                        st.success("해금완료!")
                        st.rerun()
                    else:
                        st.error("부족")

# 3. 배낭 탭
with tabs[2]:
    st.subheader("🎒 배낭")
    dice_c = st.session_state.special_inventory["행운의 주사위"]
    if st.button(f"🎲 주사위 사용 (보유: {dice_c}개)", disabled=(dice_c == 0)):
        st.session_state.special_inventory["행운의 주사위"] -= 1
        name, color = lucky_dice_roll()
        st.session_state.history.append(f"주사위:{name}")
        st.session_state.stats[name] += 1
        st.session_state.inventory[name] += 1
        st.session_state.unlocked[name] = True
        st.success(f"당첨: {get_display_name(name)}")
        st.rerun()

    st.markdown("---")
    use_qty = st.number_input("행운권 일괄 사용 수량", 1, 10000, 1, key="u_qty")
    for name, mult, _ in TICKET_DEFS:
        cnt = st.session_state.special_inventory[name]
        if st.button(
            f"🎟️ {name} {use_qty}장 사용 (보유: {cnt}개)",
            disabled=(cnt < use_qty),
            key=f"use_{name}",
        ):
            st.session_state.special_inventory[name] -= use_qty
            if st.session_state.active_multiplier == mult:
                st.session_state.active_multiplier_count += use_qty
            else:
                st.session_state.active_multiplier = mult
                st.session_state.active_multiplier_count = use_qty
            st.success(f"{name} {use_qty}장 적용!")
            st.rerun()

# 4. 도감 탭
with tabs[3]:
    st.subheader("📕 도감")
    for t_name, prob, color in TIERS:
        unlocked = st.session_state.unlocked[t_name]
        disp = get_display_name(t_name)
        price = SELL_PRICES[t_name] if unlocked else "???"
        st.markdown(
            f"### :{color}[{disp}] | 확률: `{prob*100:.11f}%` | 가격: `{price}`"
        )

# 5. 통계 탭
with tabs[4]:
    st.subheader("📊 통계")
    if st.session_state.history:
        cols = st.columns(4)
        for idx, t in enumerate(HIGH_TIERS + ["전설", "영웅", "희귀", "일반"]):
            cols[idx % 4].metric(
                get_display_name(t), f"{st.session_state.stats.get(t, 0)}회"
            )
        if st.button("🗑️ 초기화"):
            for k in list(st.session_state.keys()):
                del st.session_state[k]
            st.rerun()
    else:
        st.write("기록 없음")

# 6. 세이브 탭
with tabs[5]:
    st.subheader("💾 세이브 / 로드")
    data = json.dumps(
        {
            k: st.session_state[k]
            for k in [
                "coins",
                "history",
                "stats",
                "inventory",
                "special_inventory",
                "unlocked",
                "has_100_roll",
                "has_500_roll",
                "has_1000_roll",
                "has_3000_roll",
                "has_10000_roll",
                "active_multiplier",
                "active_multiplier_count",
            ]
        },
        ensure_ascii=False,
    )
    st.download_button("📥 다운로드", data, "gacha_save.json", "application/json")
    st.text_area("텍스트 백업", data, height=100)

    up = st.file_uploader("로드", type=["json"])
    if up and st.button("🔄 불러오기 실행"):
        for k, v in json.load(up).items():
            st.session_state[k] = v
        st.success("완료!")
        st.rerun()
