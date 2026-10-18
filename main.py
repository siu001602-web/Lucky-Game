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
    @keyframes greenFlash { 0% { background-color: rgba(0,0,0,0); } 40%, 80% { background-color: rgba(0,255,0,0.9); } 100% { background-color: rgba(0,0,0,0); } }
    @keyframes goldFlash { 0% { background-color: rgba(0,0,0,0); } 40%, 80% { background-color: rgba(255,215,0,0.95); } 100% { background-color: rgba(0,0,0,0); } }
    @keyframes diamondFlash { 0% { background-color: rgba(0,0,0,0); } 40%, 80% { background-color: rgba(30,144,255,0.95); } 100% { background-color: rgba(0,0,0,0); } }
    @keyframes smithSpark { 0% { background-color: rgba(255,69,0,0); transform: scale(0.9); } 20% { background-color: rgba(255,140,0,0.9); transform: scale(1.1); } 40% { background-color: rgba(255,215,0,1); transform: scale(1.0); } 70% { background-color: rgba(255,69,0,0.8); } 100% { background-color: rgba(0,0,0,0.95); transform: scale(1.0); } }
    @keyframes angelOpen { 0% { background-color: rgba(255,255,255,0); transform: scale(0.9); } 30% { background-color: rgba(255,255,250,0.95); transform: scale(1.05); } 70% { background-color: rgba(255,223,0,0.85); } 100% { background-color: rgba(0,0,0,0.95); transform: scale(1.0); } }
    @keyframes archangelRing { 0% { background-color: rgba(255,255,255,0); transform: scale(0.8); } 40% { background-color: rgba(255,255,255,0.9); transform: scale(1.2) rotate(180deg); } 70% { background-color: rgba(255,215,0,0.8); transform: scale(1.0) rotate(360deg); filter: drop-shadow(0 0 30px #FFD700); } 100% { background-color: rgba(0,0,0,0.95); transform: scale(1.0) rotate(360deg); } }
    @keyframes timeDistortion { 0% { background-color: rgba(0,0,0,0); transform: perspective(500px) rotateY(0deg) scale(1); filter: blur(0px); } 25% { background-color: rgba(75,0,130,0.9); transform: perspective(500px) rotateY(15deg) skewX(20deg) scale(1.1); filter: blur(2px); } 50% { background-color: rgba(255,215,0,0.85); transform: perspective(500px) rotateY(-15deg) skewX(-20deg) scale(0.95); filter: blur(4px); } 75% { background-color: rgba(75,0,130,0.9); transform: perspective(500px) rotateY(10deg) skewX(10deg) scale(1.05); filter: blur(1px); } 100% { background-color: rgba(0,0,0,0.98); transform: perspective(500px) rotateY(0deg) scale(1); filter: blur(0px); } }
    @keyframes gravityCollapse { 0% { background-color: rgba(139,0,0,0); transform: scale(1) rotate(0deg); } 20% { background-color: rgba(139,0,0,0.85); transform: scale(1.1) rotate(5deg); } 40% { background-color: rgba(255,69,0,0.9); transform: scale(0.95) rotate(-5deg) skewX(10deg); } 70% { background-color: rgba(75,0,130,0.95); transform: scale(1.05) rotate(3deg) skewX(-10deg); } 100% { background-color: rgba(0,0,0,0.98); transform: scale(1) rotate(0deg); } }
    @keyframes blackholeUniverse { 0% { background-color: rgba(255,255,255,1); transform: scale(0.2); border-radius: 50%; } 30% { background-color: rgba(0,0,0,1); transform: scale(1.0); border-radius: 0%; } 60% { background: radial-gradient(circle, #110033 0%, #000000 100%); transform: scale(1.0); box-shadow: inset 0 0 100px #9400D3; } 100% { background: radial-gradient(circle, #220044 0%, #000000 100%); transform: scale(1.0); } }
    @keyframes galaxyAbsorbPulse { 0% { background: radial-gradient(circle, #000000 0%, #0a001a 100%); transform: scale(1); } 25% { background: radial-gradient(circle, #4b0082 10%, #000000 90%); transform: scale(0.3); } 50% { background: radial-gradient(circle, #8a2be2 80%, #000000 100%); transform: scale(1.4); } 75% { background: radial-gradient(circle, #000000 5%, #191970 95%); transform: scale(0.4); } 100% { background: radial-gradient(circle, #050014 0%, #000000 100%); transform: scale(1); } }
    @keyframes riftSpinGreen { 0% { transform: translate(0, 0) rotate(0deg) scale(1); background-color: rgba(0,0,0,0); } 20% { transform: translate(-12px, 12px) rotate(90deg) scale(1.05); background-color: rgba(0,100,0,0.4); } 40% { transform: translate(12px, -12px) rotate(270deg) scale(0.95); background-color: rgba(0,200,0,0.7); } 70% { transform: translate(-8px, 8px) rotate(540deg) scale(1.1); background-color: rgba(0,255,0,0.95); border-radius: 0%; } 100% { transform: translate(0, 0) rotate(720deg) scale(1); background-color: rgba(0,255,0,1); border-radius: 0%; } }
    @keyframes abyssWhirlpool { 0% { opacity: 0; transform: scale(0.8); } 50% { opacity: 1; transform: rotate(180deg) scale(1); } 100% { opacity: 0; transform: scale(1.2); } }
    @keyframes cometMeteor { 0% { opacity: 0; } 30%, 70% { opacity: 1; } 100% { opacity: 0; } }
    @keyframes appleRain { 0% { transform: translateY(-400px) scale(0.5); opacity: 0; } 50% { opacity: 1; } 100% { transform: translateY(300px) scale(1.2); opacity: 0.9; } }
    @keyframes endingFade { 0%, 100% { opacity: 0; background-color: rgba(0,0,0,0); } 50% { opacity: 1; background-color: #000; } }

    .effect-overlay { position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; z-index: 9999999; display: flex; justify-content: center; align-items: center; pointer-events: auto; user-select: none; }
    .dark-fade { animation: fadeDark 2.5s ease-in-out forwards; }
    .holy-fade { animation: holyFlash 2.5s ease-in-out forwards; }
    .green-fade { animation: greenFlash 2.5s ease-in-out forwards; }
    .gold-fade { animation: goldFlash 2.5s ease-in-out forwards; }
    .diamond-fade { animation: diamondFlash 2.5s ease-in-out forwards; }
    .smith-fade { animation: smithSpark 10.0s ease-in-out forwards; }
    .angel-fade { animation: angelOpen 5.0s ease-in-out forwards; }
    .archangel-fade { animation: archangelRing 5.0s ease-in-out forwards; }
    .time-fade { animation: timeDistortion 10.0s ease-in-out forwards; }
    .gravity-collapse-fade { animation: gravityCollapse 10.0s ease-in-out forwards; }
    .blackhole-universe-fade { animation: blackholeUniverse 10.0s ease-in-out forwards; }
    .galaxy-pulse-fade { animation: galaxyAbsorbPulse 6.0s ease-in-out infinite; }
    .rift-spin-green-fade { animation: riftSpinGreen 5.0s cubic-bezier(0.4, 0, 0.2, 1) forwards; }
    .abyss-fade { animation: abyssWhirlpool 8.0s ease-in-out forwards; }
    .comet-fade { animation: cometMeteor 6.0s ease-in-out forwards; }
    .ending-fade { animation: endingFade 8.0s ease-in-out forwards; background-color: #000; }

    .monster-popup, .holy-popup, .green-popup, .gold-popup, .diamond-popup, .smith-popup, .angel-popup, .archangel-popup, .time-popup, .gravity-collapse-popup, .blackhole-universe-popup, .galaxy-popup, .rift-spin-green-popup, .abyss-popup, .comet-popup, .ending-text {
        font-size: 40px; font-weight: bold; text-align: center; text-shadow: 0px 0px 20px #000; color: #FFF; animation: monsterJump 0.8s ease-out forwards;
    }
    .green-popup { color: #00FF00; text-shadow: 0px 0px 30px #000; }
    .gold-popup { color: #FFF700; text-shadow: 0px 0px 30px #8B6508; }
    .diamond-popup { color: #E0FFFF; text-shadow: 0px 0px 30px #00008B; }
    .smith-popup { color: #FFD700; text-shadow: 0px 0px 30px #FF4500; font-size: 38px; }
    .angel-popup { color: #FFFACD; text-shadow: 0px 0px 40px #FFD700; font-size: 38px; }
    .archangel-popup { color: #FFFFFF; text-shadow: 0px 0px 50px #FFD700; font-size: 40px; }
    .time-popup { color: #00FFFF; text-shadow: 0px 0px 40px #FFD700; font-size: 38px; }
    .gravity-collapse-popup { color: #FF4500; text-shadow: 0px 0px 40px #FF0000; font-size: 42px; }
    .blackhole-universe-popup { color: #DA70D6; text-shadow: 0px 0px 50px #9400D3; font-size: 42px; }
    .galaxy-popup { color: #8A2BE2; text-shadow: 0px 0px 60px #4B0082; font-size: 44px; }
    .rift-spin-green-popup { color: #FFFFFF; text-shadow: 0px 0px 40px #00FF00; font-size: 42px; }
    
    .rain-apple-1 { position: absolute; left: 15%; font-size: 90px; animation: appleRain 1.5s ease-in infinite; }
    .rain-apple-2 { position: absolute; left: 35%; font-size: 110px; animation: appleRain 1.2s ease-in infinite 0.3s; }
    .rain-apple-3 { position: absolute; left: 55%; font-size: 80px; animation: appleRain 1.8s ease-in infinite 0.6s; }
    .rain-apple-4 { position: absolute; left: 75%; font-size: 100px; animation: appleRain 1.4s ease-in infinite 0.2s; }

    .galaxy-star { position: absolute; background: #FFF; border-radius: 50%; animation: starTwinkle 2s infinite ease-in-out; }
    @keyframes starTwinkle { 0%, 100% { opacity: 0.2; transform: scale(0.8); } 50% { opacity: 1; transform: scale(1.2); } }
    
    .pokedex-title { font-size: 16px; font-weight: bold; }
    .pokedex-sub { font-size: 12px; color: #888; }
    </style>
""",
    unsafe_allow_html=True,
)


def format_currency(val):
    if val >= 100000000:
        억 = val // 100000000
        나머지 = val % 100000000
        if 나머지 == 0:
            return f"{int(억)}억"
        else:
            return f"{int(억)}억 {int(나머지 // 10000)}만"
    elif val >= 10000:
        만 = val // 10000
        나머지 = val % 10000
        if 나머지 == 0:
            return f"{int(만)}만"
        else:
            return f"{int(만)}만 {int(나머지)}"
    else:
        return f"{val:,.2f}" if isinstance(val, float) and not val.is_integer() else f"{int(val):,}"


TIERS = [
    ("은하", 0.00000000001, "#8A2BE2"),
    ("대천사", 0.0, "#FFFFFF"),
    ("수호천사", 0.0, "#FFF8DC"),
    ("헤파이스토스", 0.0, "#FF8C00"),
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
    ("일반", 0.89998998908, "#A9A9A9"),
]

SELL_PRICES = {
    "은하": 70000000.0,
    "대천사": 40000000.0,
    "수호천사": 20000000.0,
    "헤파이스토스": 1000000.0,
    "중력": 30000000.0,
    "블랙홀": 10000000.0,
    "시간의 지배자": 5000000.0,
    "균열자": 2000000.0,
    "혜성": 500000.0,
    "어비스": 100000.0,
    "신성한": 20000.0,
    "도깨비": 5000.0,
    "비밀": 1000.0,
    "전설": 100.0,
    "영웅": 5.0,
    "희귀": 0.05,
    "일반": 0.01,
}

HIGH_TIERS = [
    "은하",
    "대천사",
    "수호천사",
    "헤파이스토스",
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
TICKET_DEFS = [
    ("만배 행운권", 10000.0, 100),
    ("십만배 행운권", 100000.0, 1000),
    ("백만배 행운권", 100000.0, 10000),
    ("천만배 행운권", 10000000.0, 30000),
]

TIER_CAPS = {
    "비밀": 0.20,
    "도깨비": 0.18,
    "신성한": 0.15,
    "어비스": 0.12,
    "혜성": 0.08,
    "균열자": 0.05,
    "시간의 지배자": 0.02,
    "블랙홀": 0.005,
    "중력": 0.001,
    "은하": 0.0001,
}


def check_mutation():
    r = random.random()
    if r < 0.001:
        return "오염"
    elif r < 0.01:
        return "다이아"
    elif r < 0.1:
        return "골드"
    return None


def gacha_roll(multiplier=1.0):
    normal_tiers = [t for t in TIERS if t[0] not in ["헤파이스토스", "수호천사", "대천사"]]
    base_dict = {name: prob for name, prob, color in normal_tiers}
    color_dict = {name: color for name, prob, color in normal_tiers}

    if multiplier > 1.0:
        total_high_prob = 0.0
        for name in HIGH_TIERS:
            if name in ["헤파이스토스", "수호천사", "대천사"]:
                continue
            orig = base_dict.get(name, 0.0)
            boosted = orig * multiplier
            cap = TIER_CAPS.get(name, 1.0)
            final_p = min(boosted, cap)
            base_dict[name] = final_p
            total_high_prob += final_p

        remaining_prob = max(0.10, 1.0 - total_high_prob)
        low_tiers = ["일반", "희귀", "영웅", "전설"]
        low_sum = sum(base_dict[k] for k in low_tiers)
        if low_sum > 0:
            for k in low_tiers:
                base_dict[k] = (base_dict[k] / low_sum) * remaining_prob

    adjusted = [(n, base_dict[n], color_dict[n]) for n, _, _ in normal_tiers]
    total_p = sum(t[1] for t in adjusted)
    rand_v = random.random() * total_p
    cum = 0.0
    for name, prob, color in adjusted:
        cum += prob
        if rand_v <= cum:
            return name, color, check_mutation()
    return adjusted[-1][0], adjusted[-1][2], check_mutation()


defaults = {
    "coins": 0.0,
    "total_donated": 0.0,
    "history": [],
    "stats": {t[0]: 0 for t in TIERS},
    "inventory": {t: 0 for t, _, _ in TIERS},
    "mutation_stats": {"골드": 0, "다이아": 0, "오염": 0},
    "unlocked": {
        t[0]: t[0] in ["일반", "희귀", "영웅", "전설"] for t in TIERS
    },
    "mutation_unlocked": {
        t[0]: {"골드": False, "다이아": False, "오염": False} for t, _, _ in TIERS
    },
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
    "has_100_roll": False,
    "has_500_roll": False,
    "has_1000_roll": False,
    "has_3000_roll": False,
    "has_10000_roll": False,
    "active_multiplier": 1.0,
    "active_multiplier_count": 0,
    "balloons_shown": False,
    "effect_type": None,
    "pending_mutation_effect": None,
    "skip_cutscenes_map": {t: False for t in HIGH_TIERS if t not in ["수호천사", "대천사"]},
}

for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

for t, _, _ in TIERS:
    if t not in st.session_state.inventory:
        st.session_state.inventory[t] = 0
    if t not in st.session_state.mutation_unlocked:
        st.session_state.mutation_unlocked[t] = {
            "골드": False,
            "다이아": False,
            "오염": False,
        }

for sp_key, sp_val in defaults["special_inventory"].items():
    if sp_key not in st.session_state.special_inventory:
        st.session_state.special_inventory[sp_key] = sp_val

if len(st.session_state.history) > 1000:
    st.session_state.history = st.session_state.history[-1000:]

# 컷씬 오버레이 제어 (은하 2단계 흡수/방출 컷씬 포함)
eff = st.session_state.effect_type
if eff:
    st.session_state.effect_type = None
    effects_html = {
        "ending": '<div class="effect-overlay ending-fade"><div class="ending-text">✨ 플레이해주셔서 감사합니다! ✨</div></div>',
        "archangel_phase1": '<div class="effect-overlay angel-fade"><div class="angel-popup">🕊️ 하늘의 문이 열립니다! 🕊️<br>✨ 천사들이 반겨줍니다 ✨<br>[수호천사] 강림!!</div></div>',
        "archangel_phase2": '<div class="effect-overlay archangel-fade"><div class="archangel-popup">🕊️✨ 천상의 문이 열리고... ✨🕊️<br>🌀 찬란한 천사링 전개 🌀<br>[대천사] 강림!!</div></div>',
        "galaxy_phase1": '<div class="effect-overlay blackhole-universe-fade"><div class="blackhole-universe-popup">🕳️ 사건의 지평선 붕괴 🕳️<br>✨ 차원 너머의 공허가 태동합니다... ✨</div></div>',
        "galaxy_phase2": '<div class="effect-overlay galaxy-pulse-fade"><div class="galaxy-popup">🌌 공허의 시공간 맥동! 🌌<br>✨ 차원 흡수 및 폭발적 방출 ✨<br>[은하] 강림!!</div></div>',
        "angel": '<div class="effect-overlay angel-fade"><div class="angel-popup">🕊️ 하늘의 문이 열립니다! 🕊️<br>✨ 천사들이 반겨줍니다 ✨<br>[수호천사] 강림!!</div></div>',
        "hephaestus": '<div class="effect-overlay smith-fade"><div class="smith-popup">🔥 대장간의 신 스파크 폭발! 🔥<br>🏛️ 그리스 아테네 신전 강림 🏛️<br>[헤파이스토스] 득템!!</div></div>',
        "gravity": '<div class="effect-overlay gravity-collapse-fade"><div class="gravity-collapse-popup">🍎 중력장 붕괴! 🍎<br>사과 폭풍우 강림!!<br>[중력] 등급 획득!!</div><div class="rain-apple-1">🍎</div><div class="rain-apple-2">🍎</div><div class="rain-apple-3">🍎</div><div class="rain-apple-4">🍎</div></div>',
        "blackhole": '<div class="effect-overlay blackhole-universe-fade"><div class="blackhole-universe-popup">🕳️ 사건의 지평선 붕괴 🕳️<br>✨ 무한한 은하수의 확장 ✨<br>[블랙홀] 강림!!</div><div class="galaxy-star" style="top:20%; left:30%; width:4px; height:4px;"></div><div class="galaxy-star" style="top:40%; left:70%; width:6px; height:6px;"></div><div class="galaxy-star" style="top:70%; left:25%; width:5px; height:5px;"></div><div class="galaxy-star" style="top:80%; left:80%; width:4px; height:4px;"></div><div class="galaxy-star" style="top:15%; left:85%; width:7px; height:7px;"></div></div>',
        "time_ruler": '<div class="effect-overlay time-fade"><div class="time-popup">⏳ 째깍... 째깍... ⏳<br>🌀 [시간의 지배자] 시공간 일그러짐!</div></div>',
        "rift": '<div class="effect-overlay rift-spin-green-fade"><div class="rift-spin-green-popup">⚡ 차원 대균열 발생! ⚡<br>그린 에너지 확장중...<br>[균열자] 강림!!</div></div>',
        "comet": '<div class="effect-overlay comet-fade"><div class="comet-popup">☄️ [혜성] 우주 강림!</div></div>',
        "abyss": '<div class="effect-overlay abyss-fade"><div class="abyss-popup">🌊 [어비스] 심해 소용돌이!</div></div>',
        "holy": '<div class="effect-overlay holy-fade"><div class="holy-popup">✨ [신성한] 등급 강림!</div></div>',
        "secret": '<div class="effect-overlay dark-fade"><div class="monster-popup">💖 [비밀] 등급 획득!</div></div>',
        "dokebi": '<div class="effect-overlay dark-fade"><div class="monster-popup">👹 [도깨비] 출현!</div></div>',
        "pollution": '<div class="effect-overlay green-fade"><div class="green-popup">☣️ [오염 돌연변이] 발현!! ☣️</div></div>',
        "gold": '<div class="effect-overlay gold-fade"><div class="gold-popup">🪙 [골드 돌연변이] 발현!! 🪙</div></div>',
        "diamond": '<div class="effect-overlay diamond-fade"><div class="diamond-popup">💎 [다이아 돌연변이] 발현!! 💎</div></div>',
    }
    if eff in effects_html:
        st.markdown(effects_html[eff], unsafe_allow_html=True)
        if eff == "archangel_phase1":
            time.sleep(4.0)
            st.session_state.effect_type = "archangel_phase2"
        elif eff == "galaxy_phase1":
            time.sleep(4.0)
            st.session_state.effect_type = "galaxy_phase2"
        else:
            time.sleep(5.0 if eff in ["hephaestus", "angel", "archangel_phase2", "galaxy_phase2", "time_ruler", "gravity", "blackhole"] else (5.0 if eff == "rift" else (2.0 if eff != "abyss" else 6.0)))
        st.rerun()


def get_base_name(name):
    if not st.session_state.unlocked.get(name, False):
        return "❓ ??"
    mapping = {
        "은하": "🌌 은하",
        "대천사": "👼✨ 대천사",
        "수호천사": "🕊️ 수호천사",
        "헤파이스토스": "🔥 헤파이스토스",
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


def get_display_name(name, mutation=None):
    if not st.session_state.unlocked.get(name, False):
        return "❓ ??"
    base = get_base_name(name)
    if mutation == "골드":
        return f"{base}(골드)"
    elif mutation == "다이아":
        return f"{base}(다이아)"
    elif mutation == "오염":
        return f"{base}(오염)"
    return base


def execute_rolls(count):
    highest = None
    mutation_hit = None

    for _ in range(count):
        mult = (
            st.session_state.active_multiplier
            if st.session_state.active_multiplier_count > 0
            else 1.0
        )
        if mult > 1.0:
            st.session_state.active_multiplier_count -= 1
            if st.session_state.active_multiplier_count == 0:
                st.session_state.active_multiplier = 1.0

        name, _, mutation = gacha_roll(mult)
        st.session_state.history.append((name, mutation))
        st.session_state.stats[name] += 1
        st.session_state.inventory[name] += 1
        st.session_state.unlocked[name] = True

        if mutation:
            st.session_state.mutation_stats[mutation] += 1
            st.session_state.mutation_unlocked[name][mutation] = True
            if name in HIGH_TIERS:
                mutation_hit = mutation

        if (
            name in HIGH_TIERS
            and not st.session_state.skip_cutscenes_map.get(name, False)
        ):
            if highest is None or HIGH_TIERS.index(name) < HIGH_TIERS.index(
                highest
            ):
                highest = name

    return highest, mutation_hit


def check_all():
    return all(st.session_state.unlocked.get(t[0], False) for t in TIERS)


# 상단 UI
st.title("🎲 뽑기 & 상점 시뮬레이터")
st.metric(label="💰 보유 코인", value=f"{format_currency(st.session_state.coins)} 코인")

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
        if t in ["수호천사", "대천사"]:
            continue
        st.session_state.skip_cutscenes_map[t] = st.checkbox(
            f"{get_base_name(t)} 스킵",
            value=st.session_state.skip_cutscenes_map[t],
            key=f"skip_setting_{t}",
        )

st.divider()

tabs = st.tabs(
    ["🎰 뽑기", "🏪 상점", "🛠️ 대장간", "🎁 개발자 기부", "🎒 배낭", "📕 도감", "📊 통계", "💾 세이브", "🔑 개발자"]
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
            name, color, mutation = gacha_roll(mult)
            st.session_state.history.append((name, mutation))
            st.session_state.stats[name] += 1
            st.session_state.inventory[name] += 1
            st.session_state.unlocked[name] = True

            if mutation:
                st.session_state.mutation_stats[mutation] += 1
                st.session_state.mutation_unlocked[name][mutation] = True

            mapping = {
                "은하": "galaxy_phase1",
                "중력": "gravity",
                "블랙홀": "blackhole",
                "시간의 지배자": "time_ruler",
                "균열자": "rift",
                "혜성": "comet",
                "어비스": "abyss",
                "신성한": "holy",
                "도깨비": "dokebi",
                "비밀": "secret",
            }
            mutation_map = {
                "골드": "gold",
                "다이아": "diamond",
                "오염": "pollution",
            }

            if (
                name in mapping
                and not st.session_state.skip_cutscenes_map.get(name, False)
            ):
                st.session_state.effect_type = mapping[name]
                if mutation in mutation_map:
                    st.session_state.pending_mutation_effect = mutation_map[mutation]
                st.rerun()
            elif mutation in mutation_map and name in HIGH_TIERS:
                st.session_state.effect_type = mutation_map[mutation]
                st.rerun()

            st.success(
                f"🎉 **[1회]** 당첨: **:{color}[{get_display_name(name, mutation)}]**"
            )

    with c2:
        if st.button("🚀 10연차!", use_container_width=True):
            hit, mutation_hit = execute_rolls(10)
            mapping = {
                "은하": "galaxy_phase1",
                "중력": "gravity",
                "블랙홀": "blackhole",
                "시간의 지배자": "time_ruler",
                "균열자": "rift",
                "혜성": "comet",
                "어비스": "abyss",
                "신성한": "holy",
                "도깨비": "dokebi",
                "비밀": "secret",
            }
            mutation_map = {
                "골드": "gold",
                "다이아": "diamond",
                "오염": "pollution",
            }
            if hit and not st.session_state.skip_cutscenes_map.get(hit, False):
                st.session_state.effect_type = mapping[hit]
                if mutation_hit in mutation_map:
                    st.session_state.pending_mutation_effect = mutation_map[mutation_hit]
                st.rerun()
            elif mutation_hit in mutation_map:
                st.session_state.effect_type = mutation_map[mutation_hit]
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
                    hit, mutation_hit = execute_rolls(cnt)
                    mapping = {
                        "은하": "galaxy_phase1",
                        "중력": "gravity",
                        "블랙홀": "blackhole",
                        "시간의 지배자": "time_ruler",
                        "균열자": "rift",
                        "혜성": "comet",
                        "어비스": "abyss",
                        "신성한": "holy",
                        "도깨비": "dokebi",
                        "비밀": "secret",
                    }
                    mutation_map = {
                        "골드": "gold",
                        "다이아": "diamond",
                        "오염": "pollution",
                    }
                    if hit and not st.session_state.skip_cutscenes_map.get(
                        hit, False
                    ):
                        st.session_state.effect_type = mapping[hit]
                        if mutation_hit in mutation_map:
                            st.session_state.pending_mutation_effect = mutation_map[mutation_hit]
                        st.rerun()
                    elif mutation_hit in mutation_map:
                        st.session_state.effect_type = mutation_map[mutation_hit]
                        st.rerun()
                    st.success(f"🎉 {cnt}연차 완료!")

# 2. 상점 탭
with tabs[1]:
    st.subheader("💵 등급별 판매소")
    sell_sel = {}
    cols = st.columns(3)
    for i, (t_name, _, _) in enumerate(TIERS):
        with cols[i % 3]:
            sell_sel[t_name] = st.checkbox(
                f"{get_base_name(t_name)} ({format_currency(st.session_state.inventory.get(t_name, 0))}개)",
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
            st.success(f"🎉 {format_currency(earned)} 코인 획득!")
            st.rerun()

    st.divider()
    st.subheader("🛒 Special 상점")
    buy_qty = st.number_input("행운권 일괄 구매 수량", 1, 100000, 1)

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
        if st.button(f"🎟️ {name} {format_currency(buy_qty)}장 ({format_currency(cost)}코인)", key=f"buy_{name}"):
            if st.session_state.coins >= cost:
                st.session_state.coins -= cost
                st.session_state.special_inventory[name] += buy_qty
                st.success("구매 완료!")
            else:
                st.error("코인 부족!")

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
                if st.button(f"{format_currency(price)}코인", key=f"b_{idx}"):
                    if st.session_state.coins >= price:
                        st.session_state.coins -= price
                        st.session_state.special_inventory[key_name] += 1
                        st.session_state[flag] = True
                        st.success("해금완료!")
                        st.rerun()
                    else:
                        st.error("부족")

# 3. 대장간 탭
with tabs[2]:
    st.subheader("🛠️ 불꽃의 대장간 (일괄 합성 시스템)")
    hephaestus_name = get_base_name("헤파이스토스")
    st.info(f"비밀 등급 이상 아이템 3개를 소모하여 상위 등급이나 대장간 신을 영접하세요!\n- 승급: 19.9% | 실패(소멸): 50% | 무효(유지): 30% | {hephaestus_name}: 0.1%")

    secret_and_above = [t[0] for t in TIERS if t[0] not in ["헤파이스토스", "수호천사", "대천사"]]
    secret_idx = secret_and_above.index("비밀")
    forge_targets = secret_and_above[: secret_idx + 1]

    selected_forge_item = st.selectbox(
        "합성할 재료 선택 (동일 등급 3개 소모)",
        forge_targets,
        format_func=lambda x: get_base_name(x),
    )

    owned_count = st.session_state.inventory.get(selected_forge_item, 0)
    max_forge_sets = owned_count // 3

    st.write(f"현재 보유량: **{format_currency(owned_count)}개** (최대 합성 가능 횟수: **{format_currency(max_forge_sets)}회**)")

    max_key = f"max_forge_{selected_forge_item}"
    if max_key not in st.session_state:
        st.session_state[max_key] = False

    c_btn1, c_btn2 = st.columns([1.5, 8.5])
    with c_btn1:
        if st.button("⚡ 최대치 선택", use_container_width=True, disabled=(max_forge_sets == 0)):
            st.session_state[f"val_{selected_forge_item}"] = max_forge_sets

    current_val = st.session_state.get(f"val_{selected_forge_item}", 1)
    if current_val > max_forge_sets:
        current_val = max(1, max_forge_sets)

    if max_forge_sets > 0:
        forge_count = st.number_input("합성 진행 횟수 선택", min_value=1, max_value=max_forge_sets, value=current_val, key=f"val_{selected_forge_item}")
    else:
        forge_count = 0
        st.warning("합성 재료(동일 등급 3개 이상)가 부족합니다!")

    if st.button("🔥 대장간 일괄 재련 시작", type="primary", disabled=(max_forge_sets == 0)):
        total_materials_needed = forge_count * 3
        st.session_state.inventory[selected_forge_item] -= total_materials_needed

        success_count = 0
        fail_count = 0
        refund_count = 0
        hephaestus_hit = False
        last_success_item = None

        for _ in range(forge_count):
            roll_val = random.random() * 100
            if roll_val < 0.1:
                st.session_state.inventory["헤파이스토스"] += 1
                st.session_state.unlocked["헤파이스토스"] = True
                hephaestus_hit = True
            elif roll_val < 19.9 + 0.1:
                current_idx = secret_and_above.index(selected_forge_item)
                if current_idx > 0:
                    upper_item = secret_and_above[current_idx - 1]
                    st.session_state.inventory[upper_item] += 1
                    st.session_state.unlocked[upper_item] = True
                    success_count += 1
                    last_success_item = upper_item
                else:
                    st.session_state.inventory["헤파이스토스"] += 1
                    st.session_state.unlocked["헤파이스토스"] = True
                    hephaestus_hit = True
            elif roll_val < 50.0 + 19.9 + 0.1:
                fail_count += 1
            else:
                refund_count += 1
                st.session_state.inventory[selected_forge_item] += 3

        mapping = {
            "은하": "galaxy_phase1",
            "중력": "gravity",
            "블랙홀": "blackhole",
            "시간의 지배자": "time_ruler",
            "균열자": "rift",
            "혜성": "comet",
            "어비스": "abyss",
            "신성한": "holy",
            "도깨비": "dokebi",
            "비밀": "secret",
        }

        if hephaestus_hit:
            st.session_state.effect_type = "hephaestus"
            st.rerun()
        elif last_success_item and last_success_item in mapping:
            st.session_state.effect_type = mapping[last_success_item]
            st.rerun()
        else:
            result_msg = f"✨ **[일괄 합성 결과 ({format_currency(forge_count)}회 진행)]**\n"
            if success_count > 0:
                current_idx = secret_and_above.index(selected_forge_item)
                upper_item = secret_and_above[current_idx - 1] if current_idx > 0 else "헤파이스토스"
                result_msg += f"- 🌟 승급 성공: **{format_currency(success_count)}회** ({get_base_name(upper_item)} 획득)\n"
            if fail_count > 0:
                result_msg += f"- 💥 소멸 실패: **{format_currency(fail_count)}회**\n"
            if refund_count > 0:
                result_msg += f"- 🛡️ 무효(재료반환): **{format_currency(refund_count)}회**\n"
            st.success(result_msg)

# 4. 개발자 기부 탭
with tabs[3]:
    st.subheader("🎁 개발자 기부 시스템")
    total_d = st.session_state.get("total_donated", 0.0)
    
    if total_d >= 30000000.0:
        curr_angel_p = 1.0
        curr_arch_p = 0.01
        angel_p_str = "1.0% (3천만 코인 달성 보너스!)"
        arch_p_str = "0.01% (3천만 코인 달성 보너스!)"
    elif total_d >= 5000000.0:
        curr_angel_p = 0.1
        curr_arch_p = 0.001
        angel_p_str = "0.1% (5백만 코인 달성 보너스!)"
        arch_p_str = "0.001% (5백만 코인 달성 보너스!)"
    else:
        curr_angel_p = 0.01
        curr_arch_p = 0.0001
        angel_p_str = "0.01% (기본 확률)"
        arch_p_str = "0.0001% (기본 확률)"

    display_angel_name = get_base_name("수호천사")
    display_archangel_name = get_base_name("대천사")

    st.info(f"💡 개발자에게 1회 **1만 코인**을 기부합니다.\n- 현재 누적 기부금: **{format_currency(total_d)} 코인**\n- [{display_angel_name}] 획득 확률: **{angel_p_str}**\n- [{display_archangel_name}] 획득 확률: **{arch_p_str}**")

    donation_counts = [1, 10, 100]
    d_cols = st.columns(len(donation_counts))
    
    for idx, d_cnt in enumerate(donation_counts):
        cost_total = d_cnt * 10000.0
        with d_cols[idx]:
            if st.button(f"💖 {format_currency(d_cnt)}회 기부 ({format_currency(cost_total)}코인)", use_container_width=True, type="primary"):
                if st.session_state.coins >= cost_total:
                    st.session_state.coins -= cost_total
                    st.session_state.total_donated += cost_total
                    
                    hit_type = None
                    for _ in range(d_cnt):
                        r_arch = random.random() * 100
                        r_ang = random.random() * 100
                        if r_arch < curr_arch_p:
                            hit_type = "archangel"
                            break
                        elif r_ang < curr_angel_p:
                            hit_type = "angel"
                            break
                    
                    if hit_type == "archangel":
                        st.session_state.inventory["대천사"] += 1
                        st.session_state.unlocked["대천사"] = True
                        st.session_state.effect_type = "archangel_phase1"
                        st.rerun()
                    elif hit_type == "angel":
                        st.session_state.inventory["수호천사"] += 1
                        first_time = not st.session_state.unlocked.get("수호천사", False)
                        st.session_state.unlocked["수호천사"] = True
                        if first_time:
                            st.session_state.effect_type = "angel"
                            st.rerun()
                        else:
                            st.success(f"🎉 [{get_base_name('수호천사')}] 획득 완료!")
                    else:
                        st.warning(f"💸 총 {format_currency(d_cnt)}회({format_currency(cost_total)}코인) 기부 완료! (아쉽게도 이번엔 천사가 나오지 않았습니다!)")
                else:
                    st.error("❌ 보유 코인이 부족합니다!")

# 5. 배낭 탭
with tabs[4]:
    st.subheader("🎒 배낭")
    dice_c = st.session_state.special_inventory.get("행운의 주사위", 0)
    if st.button(f"🎲 주사위 사용 (보유: {format_currency(dice_c)}개)", disabled=(dice_c == 0)):
        st.session_state.special_inventory["행운의 주사위"] -= 1
        name, color, mutation = gacha_roll(1.0)
        st.session_state.history.append((name, mutation))
        st.session_state.stats[name] += 1
        st.session_state.inventory[name] += 1
        st.session_state.unlocked[name] = True
        if mutation:
            st.session_state.mutation_stats[mutation] += 1
            st.session_state.mutation_unlocked[name][mutation] = True
        st.success(f"당첨: {get_display_name(name, mutation)}")
        st.rerun()

    st.markdown("---")
    use_qty = st.number_input("행운권 일괄 사용 수량", 1, 100000, 1, key="u_qty")
    for name, mult, _ in TICKET_DEFS:
        cnt = st.session_state.special_inventory.get(name, 0)
        if st.button(
            f"🎟️ {name} {format_currency(use_qty)}장 사용 (보유: {format_currency(cnt)}개)",
            disabled=(cnt < use_qty),
            key=f"use_{name}",
        ):
            st.session_state.special_inventory[name] -= use_qty
            if st.session_state.active_multiplier == mult:
                st.session_state.active_multiplier_count += use_qty
            else:
                st.session_state.active_multiplier = mult
                st.session_state.active_multiplier_count = use_qty
            st.success(f"{name} {format_currency(use_qty)}장 적용!")
            st.rerun()

# 6. 도감 탭
with tabs[5]:
    st.subheader("📕 도감")
    mapping_cutscene = {
        "은하": "galaxy_phase1",
        "대천사": "archangel_phase1",
        "수호천사": "angel",
        "헤파이스토스": "hephaestus",
        "중력": "gravity",
        "블랙홀": "blackhole",
        "시간의 지배자": "time_ruler",
        "균열자": "rift",
        "혜성": "comet",
        "어비스": "abyss",
        "신성한": "holy",
        "도깨비": "dokebi",
        "비밀": "secret",
    }

    for t_name, prob, color in TIERS:
        unlocked = st.session_state.unlocked[t_name]
        disp = get_base_name(t_name)
        price = format_currency(SELL_PRICES[t_name]) if unlocked else "???"
        
        if t_name in ["수호천사", "대천사"]:
            prob_str = "기부 전용 (누적 기부금 연동)"
        elif prob > 0:
            prob_str = f"{prob*100:.11f}%"
        else:
            prob_str = "대장간 전용"

        c1, c2 = st.columns([3.2, 1.0])
        with c1:
            st.markdown(
                f"<div class='pokedex-title'>:<span style='color:{color}'>{disp}</span> | 확률: <code>{prob_str}</code> | 가격: <code>{price}</code></div>",
                unsafe_allow_html=True,
            )
            if unlocked:
                m_dict = st.session_state.mutation_unlocked.get(t_name, {})
                g_u = "🪙골드(O)" if m_dict.get("골드") else "🪙골드(X)"
                d_u = "💎다이아(O)" if m_dict.get("다이아") else "💎다이아(X)"
                p_u = "☣️오염(O)" if m_dict.get("오염") else "☣️오염(X)"
                st.markdown(
                    f"<div class='pokedex-sub'>돌연변이: {g_u} | {d_u} | {p_u}</div>",
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    "<div class='pokedex-sub'>돌연변이: 🔒 미해금</div>",
                    unsafe_allow_html=True,
                )

        with c2:
            if unlocked and t_name in mapping_cutscene:
                if st.button("▶ 다시보기", key=f"preview_{t_name}", use_container_width=True):
                    st.session_state.effect_type = mapping_cutscene[t_name]
                    st.rerun()

        st.markdown("<hr style='margin: 4px 0px; border-color: rgba(255,255,255,0.08);'>", unsafe_allow_html=True)

# 7. 통계 탭
with tabs[6]:
    st.subheader("📊 통계")
    if st.session_state.history:
        cols = st.columns(4)
        for idx, t in enumerate(HIGH_TIERS + ["전설", "영웅", "희귀", "일반"]):
            cols[idx % 4].metric(
                get_base_name(t), f"{format_currency(st.session_state.stats.get(t, 0))}회"
            )

        st.markdown("### 🧪 돌연변이 발견 통계")
        m_cols = st.columns(3)
        m_cols[0].metric(
            "🪙 골드 돌연변이",
            f"{format_currency(st.session_state.get('mutation_stats', {}).get('골드', 0))}회",
        )
        m_cols[1].metric(
            "💎 다이아 돌연변이",
            f"{format_currency(st.session_state.get('mutation_stats', {}).get('다이아', 0))}회",
        )
        m_cols[2].metric(
            "☣️ 오염 돌연변이",
            f"{format_currency(st.session_state.get('mutation_stats', {}).get('오염', 0))}회",
        )

        if st.button("🗑️ 초기화"):
            for k in list(st.session_state.keys()):
                del st.session_state[k]
            st.rerun()
    else:
        st.write("기록 없음")

# 8. 세이브 탭
with tabs[7]:
    st.subheader("💾 세이브 / 로드")
    data = json.dumps(
        {
            k: st.session_state[k]
            for k in [
                "coins",
                "total_donated",
                "history",
                "stats",
                "inventory",
                "mutation_stats",
                "mutation_unlocked",
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

# 9. 개발자 전용 탭 (비밀번호: 090925)
with tabs[8]:
    st.subheader("🔑 개발자 전용 코인 지급 메뉴")
    pw_input = st.text_input("개발자 비밀번호를 입력하세요", type="password")
    
    if pw_input == "090925":
        st.success("🔓 개발자 권한 인증 완료!")
        add_coins = st.number_input("지급할 코인 수량을 입력하세요", min_value=0.0, step=1000.0, value=10000.0)
        if st.button("💰 코인 지급 받기", type="primary"):
            st.session_state.coins += add_coins
            st.success(f"🎉 성공적으로 {format_currency(add_coins)} 코인이 지급되었습니다!")
            st.rerun()
    elif pw_input != "":
        st.error("❌ 비밀번호가 틀렸습니다!")
    else:
        st.info("🔒 접근하려면 올바른 비밀번호를 입력하세요.")
