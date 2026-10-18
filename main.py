import json
import random
import time
import streamlit as st

st.set_page_config(page_title="두근두근 뽑기 & 상점", page_icon="🎲", layout="centered")

st.markdown("""
<style>
@keyframes fadeDark { 0% { background-color: rgba(0,0,0,0); } 25%, 75% { background-color: rgba(0,0,0,0.98); } 100% { background-color: rgba(0,0,0,0); } }
@keyframes monsterJump { 0% { transform: scale(0.2); opacity: 0; } 50% { transform: scale(1.2); opacity: 1; } 100% { transform: scale(1.0); opacity: 1; } }
@keyframes purpleHold { 0%, 100% { background-color: rgba(75, 0, 130, 0.95); } }
@keyframes zombieAnim { 0% { transform: translateY(50px) scale(0.5); opacity: 0; } 50% { transform: translateY(0) scale(1.1) rotate(-3deg); opacity: 1; } 100% { transform: translateY(0) scale(1) rotate(0deg); opacity: 1; } }
@keyframes thunderAnim { 0% { background-color: #fff; transform: scale(1.2); } 20% { background-color: #220033; transform: scale(0.9); } 40% { background-color: #fff; transform: scale(1.1); } 100% { background-color: rgba(75,0,130,0.95); transform: scale(1); } }
@keyframes potionAnim { 0% { transform: translateY(-300px); opacity: 0; } 60% { transform: translateY(0); opacity: 1; background-color: rgba(0, 255, 0, 0.8); } 100% { opacity: 1; background-color: rgba(75,0,130,0.95); } }
@keyframes vampireAnim { 0% { transform: translateX(300px); background-color: rgba(255,0,0,0.9); opacity: 0; } 50% { transform: translateX(0); opacity: 1; } 100% { transform: translateX(0); opacity: 1; } }
@keyframes jiangshiAnim { 0% { transform: scale(0.8) translateX(-50px); opacity: 0; } 40% { transform: scale(1.2) translateX(40px); opacity: 1; } 100% { transform: scale(1) translateX(0); opacity: 1; } }
@keyframes frankAnim { 0% { transform: rotate(0deg) scale(0.8); opacity: 0; } 50% { transform: rotate(15deg) scale(1.1); opacity: 1; } 100% { transform: rotate(0deg) scale(1); opacity: 1; } }
@keyframes moonDrop { 0% { transform: translateY(-150px); opacity: 0; } 100% { transform: translateY(0); opacity: 1; } }
@keyframes pumpkinPop { 0% { transform: scale(0); opacity: 0; } 100% { transform: scale(1); opacity: 1; } }
@keyframes ghostPop { 0% { transform: scale(0); opacity: 0; } 100% { transform: scale(1); opacity: 1; } }
@keyframes appleRain { 0% { transform: translateY(-400px); opacity: 0; } 100% { transform: translateY(300px); opacity: 0.9; } }
@keyframes endingFade { 0%, 100% { opacity: 0; background-color: rgba(0,0,0,0); } 50% { opacity: 1; background-color: #000; } }

.effect-overlay { position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; z-index: 9999999; display: flex; flex-direction: column; justify-content: center; align-items: center; pointer-events: auto; user-select: none; }
.purple-hold-fade { animation: purpleHold 3.0s ease-in-out forwards; background-color: rgba(75, 0, 130, 0.95); }
.zombie-fade { animation: zombieAnim 1.5s ease-in-out forwards; }
.thunder-fade { animation: thunderAnim 1.5s ease-in-out forwards; }
.potion-fade { animation: potionAnim 1.5s ease-in-out forwards; }
.vampire-fade { animation: vampireAnim 1.5s ease-in-out forwards; }
.jiangshi-fade { animation: jiangshiAnim 1.5s ease-in-out forwards; }
.frank-fade { animation: frankAnim 2.0s ease-in-out forwards; }
.pumpkin-king-fade { animation: fadeDark 3s ease-in-out forwards; }
.ghost-fade { animation: fadeDark 3s ease-in-out forwards; }
.ending-fade { animation: endingFade 6.0s ease-in-out forwards; background-color: #000; }

.popup-text { font-size: 38px; font-weight: bold; text-align: center; text-shadow: 0px 0px 20px #000; color: #FFF; animation: monsterJump 0.8s ease-out forwards; }
.moon-icon { font-size: 90px; animation: moonDrop 1.5s ease-out forwards; margin-bottom: 15px; }
.pumpkin-icon { font-size: 120px; animation: pumpkinPop 1.5s ease-out forwards; margin-bottom: 15px; }
.ghost-icon { font-size: 130px; animation: ghostPop 1.5s ease-out forwards; margin-bottom: 15px; }
.pokedex-title { font-size: 16px; font-weight: bold; }
.pokedex-sub { font-size: 12px; color: #888; }
</style>
""", unsafe_allow_html=True)

TIERS_DATA = [
    ("은하", 0.00000000000005, "#8A2BE2", 70000000.0),
    ("대천사", 0.0, "#FFFFFF", 40000000.0),
    ("수호천사", 0.0, "#FFF8DC", 20000000.0),
    ("헤파이스토스", 0.0, "#FF8C00", 1000000.0),
    ("중력", 0.0000000000005, "#FF4500", 30000000.0),
    ("블랙홀", 0.0000000000015, "#AA00FF", 10000000.0),
    ("시간의 지배자", 0.0000000000080, "#FFD700", 5000000.0),
    ("균열자", 0.0000000000900, "#FF0000", 2000000.0),
    ("혜성", 0.0000000009000, "#FF8C00", 500000.0),
    ("어비스", 0.0000009000000, "#00FFFF", 100000.0),
    ("신성한", 0.0000090000000, "#00BFFF", 20000.0),
    ("도깨비", 0.0000100000000, "#FF0055", 5000.0),
    ("비밀", 0.0000900000000, "#FF1493", 1000.0),
    ("전설", 0.0009000000000, "#FFD700", 100.0),
    ("영웅", 0.0290000000000, "#9400D3", 5.0),
    ("희귀", 0.0700000000000, "#1E90FF", 0.05),
    ("일반", 0.8999899890845, "#A9A9A9", 0.01),
]

HALLOWEEN_DATA = [
    ("호박왕", 0.000001, "#FF8C00", 5000000.0),
    ("유령", 0.0001, "#E0FFFF", 10000.0),
    ("사탕", 0.1, "#FF69B4", 100.0),
    ("박쥐", 99.899899, "#8A2BE2", 1.0),
]

HALLOWEEN_BOX_DATA = [
    ("프랑켄슈타인", 0.05, "#32CD32", 0.0),
    ("강시", 0.25, "#FF4500", 0.0),
    ("뱀파이어", 0.7, "#DC143C", 0.0),
    ("마녀", 4.0, "#8A2BE2", 0.0),
    ("잭오랜턴", 15.0, "#FF8C00", 0.0),
    ("스켈레톤", 30.0, "#F5F5F5", 0.0),
    ("좀비", 50.0, "#556B2F", 0.0),
]

ALL_TIERS = TIERS_DATA + HALLOWEEN_DATA + HALLOWEEN_BOX_DATA
SELL_PRICES = {t[0]: t[3] for t in ALL_TIERS}
HIGH_TIERS = ["은하", "대천사", "수호천사", "헤파이스토스", "중력", "블랙홀", "시간의 지배자", "균열자", "혜성", "어비스", "신성한", "도깨비", "비밀", "호박왕", "유령", "프랑켄슈타인", "강시", "뱀파이어", "마녀", "잭오랜턴", "스켈레톤", "좀비"]

def format_currency(val):
    if val >= 100000000:
        return f"{int(val//100000000)}억" if val%100000000==0 else f"{int(val//100000000)}억 {int((val%100000000)//10000)}만"
    elif val >= 10000:
        return f"{int(val//10000)}만" if val%10000==0 else f"{int(val//10000)}만 {int(val%10000)}"
    return f"{val:,.2f}" if isinstance(val, float) and not val.is_integer() else f"{int(val):,}"

def get_base_name(name):
    if not st.session_state.unlocked.get(name, False):
        return "❓ ??"
    mapping = {
        "은하": "🌌 은하", "대천사": "👼✨ 대천사", "수호천사": "🕊️ 수호천사", "헤파이스토스": "🔥 헤파이스토스",
        "중력": "🍎 중력", "블랙홀": "🕳️ 블랙홀", "시간의 지배자": "⏳ 시간의 지배자", "균열자": "🌀 균열자",
        "혜성": "☄️ 혜성", "어비스": "🌊 어비스", "신성한": "👼 신성한", "도깨비": "👹 도깨비",
        "비밀": "💖 비밀", "전설": "🟡 전설", "영웅": "🟣 영웅", "희귀": "🔵 희귀", "일반": "⚪ 일반",
        "호박왕": "🎃 호박왕", "유령": "👻 유령", "사탕": "🍬 사탕", "박쥐": "🦇 박쥐",
        "프랑켄슈타인": "⚡ 프랑켄슈타인", "강시": "🧟‍♂️ 강시", "뱀파이어": "🧛 뱀파이어",
        "마녀": "🧙 마녀", "잭오랜턴": "🎃 잭오랜턴", "스켈레톤": "💀 스켈레톤", "좀비": "🧟 좀비"
    }
    return mapping.get(name, name)

def get_display_name(name, mutation=None):
    if not st.session_state.unlocked.get(name, False): return "❓ ??"
    base = get_base_name(name)
    return f"{base}({mutation})" if mutation else base

defaults = {
    "coins": 0.0, "total_donated": 0.0, "history": [],
    "stats": {t[0]: 0 for t in ALL_TIERS}, "inventory": {t[0]: 0 for t in ALL_TIERS},
    "mutation_stats": {"골드": 0, "다이아": 0, "오염": 0},
    "unlocked": {t[0]: t[0] in ["일반", "희귀", "영웅", "전설", "사탕", "박쥐"] for t in ALL_TIERS},
    "mutation_unlocked": {t[0]: {"골드": False, "다이아": False, "오염": False} for t in ALL_TIERS},
    "special_inventory": {"행운의 주사위": 0, "할로윈 뽑기권": 0, "만배 행운권": 0, "십만배 행운권": 0, "백만배 행운권": 0, "천만배 행운권": 0, "100연차 기능권": 0, "500연차 기능권": 0, "1000연차 기능권": 0, "3000연차 기능권": 0, "10000연차 기능권": 0},
    "has_100_roll": False, "has_500_roll": False, "has_1000_roll": False, "has_3000_roll": False, "has_10000_roll": False,
    "active_multiplier": 1.0, "active_multiplier_count": 0, "balloons_shown": False, "effect_type": None,
    "skip_cutscenes_map": {t: False for t in HIGH_TIERS if t not in ["수호천사", "대천사"]}
}
for k, v in defaults.items():
    if k not in st.session_state: st.session_state[k] = v

eff = st.session_state.effect_type
if eff:
    st.session_state.effect_type = None
    effects_map = {
        "ending": ('ending-fade', '<div class="popup-text">✨ 플레이해주셔서 감사합니다! ✨</div>'),
        "archangel_phase1": ('purple-hold-fade', '<div class="popup-text">🕊️ 하늘의 문이 열립니다!<br>[수호천사] 강림!!</div>'),
        "archangel_phase2": ('purple-hold-fade', '<div class="popup-text">🕊️✨ 천상의 문이 열리고...<br>[대천사] 강림!!</div>'),
        "galaxy_phase1": ('purple-hold-fade', '<div class="popup-text">🕳️ 사건의 지평선 붕괴<br>✨ 공허가 태동합니다... ✨</div>'),
        "galaxy_phase2": ('purple-hold-fade', '<div class="popup-text">🌌 시공간 맥동 및 방출<br>[은하] 강림!!</div>'),
        "pumpkin_king": ('pumpkin-king-fade', '<div class="moon-icon">🌕</div><div class="pumpkin-icon">🎃</div><div class="popup-text">🎃 어두운 밤하늘, 집 위로 달이 내려앉고... 🎃<br>🌕 거대한 호박왕 강림!! 🌕</div>'),
        "ghost": ('ghost-fade', '<div class="ghost-icon">👻</div><div class="popup-text">👻 ...스스스 ...👻<br>💥 기괴한 유령 출현!! 💥</div>'),
        "zombie": ('zombie-fade', '<div class="purple-hold-fade effect-overlay"><div class="popup-text">🧟 무덤이 갈라지며 화면이 흔들린다!<br>[좀비] 출현!!</div></div>'),
        "skeleton": ('thunder-fade', '<div class="purple-hold-fade effect-overlay"><div class="popup-text">⚡ 하늘에서 벼락이 치며 해골이 강림한다!<br>[스켈레톤] 등장!!</div></div>'),
        "jackolantern": ('pumpkin-king-fade', '<div class="purple-hold-fade effect-overlay"><div class="pumpkin-icon">🎃</div><div class="popup-text">✨ 호박이 튀어나와 반짝인다!<br>[잭오랜턴] 등장!!</div></div>'),
        "witch": ('potion-fade', '<div class="purple-hold-fade effect-overlay"><div class="popup-text">🧪 초록색 포션이 위에서부터 뿌려진다!<br>[마녀] 등장!!</div></div>'),
        "vampire": ('vampire-fade', '<div class="purple-hold-fade effect-overlay"><div class="popup-text">🧛 붉은 피의 물결과 날카로운 이빨!<br>[뱀파이어] 강림!!</div></div>'),
        "jiangshi": ('jiangshi-fade', '<div class="purple-hold-fade effect-overlay"><div class="popup-text">🧟‍♂️ 쿵쿵! 화면이 밀려났다 돌아온다!<br>[강시] 출현!!</div></div>'),
        "frankestein": ('frank-fade', '<div class="purple-hold-fade effect-overlay"><div class="popup-text">⚡ 번개와 유령들이 뒤덮는 공포!<br>[프랑켄슈타인] 강림!!</div></div>'),
        "angel": ('purple-hold-fade', '<div class="popup-text">🕊️ [수호천사] 강림!!</div>'),
        "hephaestus": ('purple-hold-fade', '<div class="popup-text">🔥 대장간의 신 강림!<br>[헤파이스토스] 득템!!</div>'),
        "gravity": ('purple-hold-fade', '<div class="popup-text">🍎 중력장 붕괴!<br>[중력] 등급 획득!!</div>'),
        "blackhole": ('purple-hold-fade', '<div class="popup-text">🕳️ [블랙홀] 강림!!</div>'),
        "time_ruler": ('purple-hold-fade', '<div class="popup-text">⏳ [시간의 지배자] 일그러짐!</div>'),
        "rift": ('purple-hold-fade', '<div class="popup-text">⚡ [균열자] 강림!!</div>'),
        "comet": ('purple-hold-fade', '<div class="popup-text">☄️ [혜성] 우주 강림!</div>'),
        "abyss": ('purple-hold-fade', '<div class="popup-text">🌊 [어비스] 소용돌이!</div>'),
        "holy": ('purple-hold-fade', '<div class="popup-text">✨ [신성한] 등급 강림!</div>'),
        "secret": ('purple-hold-fade', '<div class="popup-text">💖 [비밀] 등급 획득!</div>'),
        "dokebi": ('purple-hold-fade', '<div class="popup-text">👹 [도깨비] 출현!</div>'),
        "pollution": ('purple-hold-fade', '<div class="popup-text">☣️ [오염 돌연변이] 발현!!</div>'),
        "gold": ('purple-hold-fade', '<div class="popup-text">🪙 [골드 돌연변이] 발현!!</div>'),
        "diamond": ('purple-hold-fade', '<div class="popup-text">💎 [다이아 돌연변이] 발현!!</div>'),
    }
    if eff in effects_map:
        cls, html = effects_map[eff]
        st.markdown(f'<div class="effect-overlay {cls}">{html}</div>', unsafe_allow_html=True)
        time.sleep(3.0)
        st.rerun()

def check_mutation():
    r = random.random()
    return "오염" if r < 0.001 else ("다이아" if r < 0.01 else ("골드" if r < 0.1 else None))

def gacha_roll(multiplier=1.0):
    normal = [t for t in TIERS_DATA if t[0] not in ["헤파이스토스", "수호천사", "대천사"]]
    b_dict = {t[0]: t[1] for t in normal}
    if multiplier > 1.0:
        for name in HIGH_TIERS:
            if name in ["헤파이스토스", "수호천사", "대천사", "호박왕", "유령"]: continue
            if name in b_dict: b_dict[name] = min(b_dict[name]*multiplier, 0.2)
    total_p = sum(b_dict.values())
    rand_v = random.random() * total_p
    cum = 0.0
    for name, prob, color in normal:
        cum += b_dict[name]
        if rand_v <= cum: return name, color, check_mutation()
    return normal[-1][0], normal[-1][2], check_mutation()

def halloween_roll():
    rand_v = random.random() * 100.0
    cum = 0.0
    for name, prob, color in HALLOWEEN_DATA:
        cum += prob
        if rand_v <= cum: return name, color
    return HALLOWEEN_DATA[-1][0], HALLOWEEN_DATA[-1][2]

def halloween_box_roll():
    rand_v = random.random() * 100.0
    cum = 0.0
    for name, prob, color in HALLOWEEN_BOX_DATA:
        cum += prob
        if rand_v <= cum: return name, color
    return HALLOWEEN_BOX_DATA[-1][0], HALLOWEEN_BOX_DATA[-1][2]

st.title("🎲 뽑기 & 상점 시뮬레이터")
st.metric("💰 보유 코인", f"{format_currency(st.session_state.coins)} 코인")

if all(st.session_state.unlocked.get(t[0], False) for t in TIERS_DATA):
    if not st.session_state.balloons_shown: st.balloons(); st.session_state.balloons_shown = True
    if st.button("🏆 [엔딩 보기]", type="primary", use_container_width=True):
        st.session_state.effect_type = "ending"; st.rerun()

if st.session_state.active_multiplier_count > 0:
    st.info(f"🎟️ **[{int(st.session_state.active_multiplier):,}배 행운 버프] 활성화 중!** (남은 횟수: {st.session_state.active_multiplier_count}회)")

with st.expander("⚙️ 설정 (컷씬 스킵)"):
    for idx, t in enumerate(HIGH_TIERS):
        if t in ["수호천사", "대천사"]: continue
        st.session_state.skip_cutscenes_map[t] = st.checkbox(
            f"{get_base_name(t)} 스킵", 
            value=st.session_state.skip_cutscenes_map[t],
            key=f"skip_setting_{t}_{idx}"
        )

st.divider()
tabs = st.tabs(["🎰 뽑기", "🎃 할로윈", "🏪 상점", "🛠️ 대장간", "🎁 기부", "🎒 배낭", "📕 도감", "📊 통계", "💾 세이브", "🔑 개발자"])

# 1. 뽑기 탭
with tabs[0]:
    st.subheader("아이템 뽑기")
    c1, c2 = st.columns(2)
    with c1:
        if st.button("🎰 1회 뽑기", use_container_width=True):
            mult = st.session_state.active_multiplier if st.session_state.active_multiplier_count > 0 else 1.0
            if mult > 1.0:
                st.session_state.active_multiplier_count -= 1
                if st.session_state.active_multiplier_count == 0: st.session_state.active_multiplier = 1.0
            name, color, mut = gacha_roll(mult)
            st.session_state.history.append((name, mut))
            st.session_state.stats[name] += 1; st.session_state.inventory[name] += 1; st.session_state.unlocked[name] = True
            if mut: st.session_state.mutation_stats[mut] += 1; st.session_state.mutation_unlocked[name][mut] = True
            
            mapping = {"은하": "galaxy_phase1", "중력": "gravity", "블랙홀": "blackhole", "시간의 지배자": "time_ruler", "균열자": "rift", "혜성": "comet", "어비스": "abyss", "신성한": "holy", "도깨비": "dokebi", "비밀": "secret"}
            if name in mapping and not st.session_state.skip_cutscenes_map.get(name, False):
                st.session_state.effect_type = mapping[name]; st.rerun()
            elif mut and name in HIGH_TIERS:
                st.session_state.effect_type = {"골드": "gold", "다이아": "diamond", "오염": "pollution"}[mut]; st.rerun()
            st.success(f"🎉 당첨: **:{color}[{get_display_name(name, mut)}]**")
    with c2:
        if st.button("🚀 10연차!", use_container_width=True):
            highest, mut_hit = None, None
            for _ in range(10):
                name, _, mut = gacha_roll(1.0)
                st.session_state.history.append((name, mut))
                st.session_state.stats[name] += 1; st.session_state.inventory[name] += 1; st.session_state.unlocked[name] = True
                if mut: st.session_state.mutation_stats[mut] += 1; st.session_state.mutation_unlocked[name][mut] = True; mut_hit = mut
                if name in HIGH_TIERS: highest = name
            mapping = {"은하": "galaxy_phase1", "중력": "gravity", "블랙홀": "blackhole", "시간의 지배자": "time_ruler", "균열자": "rift", "혜성": "comet", "어비스": "abyss", "신성한": "holy", "도깨비": "dokebi", "비밀": "secret"}
            if highest and not st.session_state.skip_cutscenes_map.get(highest, False):
                st.session_state.effect_type = mapping[highest]; st.rerun()
            elif mut_hit:
                st.session_state.effect_type = {"골드": "gold", "다이아": "diamond", "오염": "pollution"}[mut_hit]; st.rerun()
            st.success("✨ 10연차 완료!")

# 2. 할로윈 탭
with tabs[1]:
    st.subheader("🎃 할로윈 한정 뽑기 & 합성")
    
    st.markdown("""
        <audio autoplay loop>
          <source src="https://actions.google.com/sounds/v1/ambiences/creepy_wind.ogg" type="audio/ogg">
        </audio>
    """, unsafe_allow_html=True)

    h_tickets = st.session_state.special_inventory.get("할로윈 뽑기권", 0)
    st.info(f"🎟️ 보유 할로윈 뽑기권: **{format_currency(h_tickets)}장**")
    if st.button("🎃 할로윈 1회 뽑기", disabled=(h_tickets < 1), use_container_width=True):
        st.session_state.special_inventory["할로윈 뽑기권"] -= 1
        name, _ = halloween_roll()
        
        is_first_time = not st.session_state.unlocked.get(name, False)
        st.session_state.stats[name] += 1
        st.session_state.inventory[name] += 1
        st.session_state.unlocked[name] = True

        if is_first_time and not st.session_state.skip_cutscenes_map.get(name, False):
            if name == "호박왕":
                st.session_state.effect_type = "pumpkin_king"; st.rerun()
            elif name == "유령":
                st.session_state.effect_type = "ghost"; st.rerun()

        st.success(f"🎉 할로윈 당첨: [{get_base_name(name)}]")

    st.divider()
    st.markdown("### 📦 할로윈 상자 전용 합성 시스템")
    st.info("재료: **유령 1개 + 사탕 1개 + 박쥐 1개**를 소모하여 할로윈 상자를 엽니다! (상점 판매 불가 등급 획득 가능)")

    g_cnt = st.session_state.inventory.get("유령", 0)
    c_cnt = st.session_state.inventory.get("사탕", 0)
    b_cnt = st.session_state.inventory.get("박쥐", 0)
    can_box_craft = (g_cnt >= 1 and c_cnt >= 1 and b_cnt >= 1)

    st.write(f"현재 재료 보유량 - 유령: {format_currency(g_cnt)}개 | 사탕: {format_currency(c_cnt)}개 | 박쥐: {format_currency(b_cnt)}개")

    if st.button("🎁 할로윈 상자 열기 (합성)", type="primary", disabled=not can_box_craft, use_container_width=True):
        st.session_state.inventory["유령"] -= 1
        st.session_state.inventory["사탕"] -= 1
        st.session_state.inventory["박쥐"] -= 1

        box_name, _ = halloween_box_roll()
        is_first = not st.session_state.unlocked.get(box_name, False)
        st.session_state.stats[box_name] += 1
        st.session_state.inventory[box_name] += 1
        st.session_state.unlocked[box_name] = True

        box_cutscene_map = {
            "좀비": "zombie", "스켈레톤": "skeleton", "잭오랜턴": "jackolantern",
            "마녀": "witch", "뱀파이어": "vampire", "강시": "jiangshi", "프랑켄슈타인": "frankestein"
        }

        if is_first and box_name in box_cutscene_map and not st.session_state.skip_cutscenes_map.get(box_name, False):
            st.session_state.effect_type = box_cutscene_map[box_name]
            st.rerun()
        else:
            st.success(f"📦 할로윈 상자 개봉 결과: **[{get_base_name(box_name)}]** 획득!")

# 3. 상점 탭
with tabs[2]:
    st.subheader("💵 판매소 및 Special 상점")
    sellable_items = [t for t in ALL_TIERS if t[0] not in [hb[0] for hb in HALLOWEEN_BOX_DATA]]
    sell_sel = {t[0]: st.checkbox(f"{get_base_name(t[0])} ({format_currency(st.session_state.inventory.get(t[0], 0))}개)", key=f"sell_check_{t[0]}") for t in sellable_items}
    if st.button("💰 선택 아이템 판매", type="primary"):
        earned = sum(st.session_state.inventory[t] * SELL_PRICES[t] for t, sel in sell_sel.items() if sel)
        for t, sel in sell_sel.items():
            if sel: st.session_state.inventory[t] = 0
        if earned > 0:
            st.session_state.coins += earned; st.success(f"🎉 {format_currency(earned)} 코인 획득!"); st.rerun()
    
    st.divider()
    h_buy_qty = st.number_input("할로윈 뽑기권 구매 (장당 100코인, 최대 1백만)", 1, 1000000, 1)
    if st.button("🎟️ 할로윈 뽑기권 구매", type="primary"):
        cost = h_buy_qty * 100.0
        if st.session_state.coins >= cost:
            st.session_state.coins -= cost; st.session_state.special_inventory["할로윈 뽑기권"] += h_buy_qty
            st.success("구매 완료!"); st.rerun()
        else: st.error("코인 부족!")

# 4. 대장간 탭
with tabs[3]:
    st.subheader("🛠️ 불꽃의 대장간")
    st.info("비밀 등급 이상 3개를 소모하여 상위 등급이나 헤파이스토스를 영접하세요! (승급 19.9%, 소멸 50%, 무효 30%, 신 0.1%)")
    secret_items = [t[0] for t in TIERS_DATA if t[0] in HIGH_TIERS and HIGH_TIERS.index(t[0]) >= HIGH_TIERS.index("비밀")]
    sel_forge = st.selectbox("합성 재료 선택", secret_items, format_func=lambda x: get_base_name(x))
    owned = st.session_state.inventory.get(sel_forge, 0)
    if st.button("🔥 대장간 재련 시작", type="primary", disabled=(owned < 3)):
        st.session_state.inventory[sel_forge] -= 3
        r = random.random() * 100
        if r < 0.1:
            st.session_state.inventory["헤파이스토스"] += 1; st.session_state.unlocked["헤파이스토스"] = True
            st.session_state.effect_type = "hephaestus"; st.rerun()
        elif r < 20.0:
            idx = secret_items.index(sel_forge)
            if idx > 0:
                upper = secret_items[idx-1]
                st.session_state.inventory[upper] += 1; st.session_state.unlocked[upper] = True
                mapping = {"은하": "galaxy_phase1", "중력": "gravity", "블랙홀": "blackhole", "시간의 지배자": "time_ruler", "균열자": "rift", "혜성": "comet", "어비스": "abyss", "신성한": "holy", "도깨비": "dokebi", "비밀": "secret"}
                if upper in mapping: st.session_state.effect_type = mapping[upper]; st.rerun()
                st.success(f"🌟 승급 성공: {get_base_name(upper)} 획득!")
        else:
            st.warning("재련 실패 또는 무효화되었습니다.")

# 5. 기부 탭 (최대 100회 일괄 기부 적용)
with tabs[4]:
    st.subheader("🎁 개발자 기부 시스템")
    total_d = st.session_state.get("total_donated", 0.0)
    
    if total_d >= 30000000.0:
        p_angel, p_arch = 1.0, 0.01
        str_angel = "1.0% (3천만 코인 달성 보너스!)"
        str_arch = "0.01% (3천만 코인 달성 보너스!)"
    elif total_d >= 5000000.0:
        p_angel, p_arch = 0.1, 0.001
        str_angel = "0.1% (5백만 코인 달성 보너스!)"
        str_arch = "0.001% (5백만 코인 달성 보너스!)"
    else:
        p_angel, p_arch = 0.01, 0.0001
        str_angel = "0.01% (기본 확률)"
        str_arch = "0.0001% (기본 확률)"

    st.info(f"""
    💡 **개발자 기부 안내**
    - 1회 기부 금액: **10,000 코인**
    - 현재 누적 기부금: **{format_currency(total_d)} 코인**
    
    📊 **현재 적용 중인 획득 확률표 (1회당)**
    - [{get_base_name('수호천사')}]: **{str_angel}**
    - [{get_base_name('대천사')}]: **{str_arch}**
    """)

    donation_counts = [1, 10, 100]
    d_cols = st.columns(len(donation_counts))
    
    for idx, d_cnt in enumerate(donation_counts):
        cost_total = d_cnt * 10000.0
        with d_cols[idx]:
            if st.button(f"💖 {d_cnt}회 기부\n({format_currency(cost_total)}코인)", use_container_width=True, type="primary", key=f"donate_btn_{d_cnt}"):
                if st.session_state.coins >= cost_total:
                    st.session_state.coins -= cost_total
                    st.session_state.total_donated += cost_total
                    
                    hit_archangel = False
                    hit_angel = False
                    angel_count = 0
                    archangel_count = 0

                    for _ in range(d_cnt):
                        if random.random() * 100 < p_arch:
                            st.session_state.inventory["대천사"] += 1
                            st.session_state.unlocked["대천사"] = True
                            hit_archangel = True
                            archangel_count += 1
                        elif random.random() * 100 < p_angel:
                            st.session_state.inventory["수호천사"] += 1
                            st.session_state.unlocked["수호천사"] = True
                            hit_angel = True
                            angel_count += 1

                    if hit_archangel:
                        st.session_state.effect_type = "archangel_phase1"
                        st.rerun()
                    elif hit_angel and angel_count == 1 and not st.session_state.unlocked.get("수호천사", False):
                        st.session_state.effect_type = "angel"
                        st.rerun()
                    else:
                        msg = f"💸 {d_cnt}회 기부 완료! ({format_currency(cost_total)}코인 소모)\n"
                        if archangel_count > 0 or angel_count > 0:
                            msg += f"- [{get_base_name('대천사')}]: {archangel_count}회 획득!\n"
                            msg += f"- [{get_base_name('수호천사')}]: {angel_count}회 획득!\n"
                            st.success(msg)
                        else:
                            st.warning(f"💸 총 {d_cnt}회 기부 완료! (아쉽게도 이번엔 천사가 응답하지 않았습니다.)")
                else:
                    st.error("❌ 보유 코인이 부족합니다!")

# 6. 배낭 탭
with tabs[5]:
    st.subheader("🎒 배낭")
    dice = st.session_state.special_inventory.get("행운의 주사위", 0)
    if st.button(f"🎲 주사위 사용 (보유: {dice}개)", disabled=(dice == 0)):
        st.session_state.special_inventory["행운의 주사위"] -= 1
        name, color, mut = gacha_roll(1.0)
        st.session_state.inventory[name] += 1; st.session_state.unlocked[name] = True
        st.success(f"당첨: {get_display_name(name, mut)}"); st.rerun()

# 7. 도감 탭
with tabs[6]:
    st.subheader("📕 도감")
    st.markdown("### 🎃 할로윈 전용 도감")
    halloween_all_list = HALLOWEEN_DATA + HALLOWEEN_BOX_DATA
    for t_name, prob, color, _ in halloween_all_list:
        unlocked = st.session_state.unlocked.get(t_name, False)
        disp = get_base_name(t_name)
        st.markdown(f"<div class='pokedex-title'>:<span style='color:{color}'>{disp}</span> (확률: {prob}%)</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='pokedex-sub'>상태: {'해금됨' if unlocked else '🔒 미해금 (??)'}</div>", unsafe_allow_html=True)
        st.markdown("<hr style='margin: 4px 0px; border-color: rgba(255,255,255,0.08);'>", unsafe_allow_html=True)

    st.markdown("### 🎲 일반 / 특수 도감")
    for t_name, prob, color, _ in TIERS_DATA:
        unlocked = st.session_state.unlocked.get(t_name, False)
        disp = get_base_name(t_name)
        st.markdown(f"<div class='pokedex-title'>:<span style='color:{color}'>{disp}</span></div>", unsafe_allow_html=True)
        st.markdown(f"<div class='pokedex-sub'>상태: {'해금됨' if unlocked else '미해금'}</div>", unsafe_allow_html=True)
        st.markdown("<hr style='margin: 4px 0px; border-color: rgba(255,255,255,0.08);'>", unsafe_allow_html=True)

# 8. 통계 탭
with tabs[7]:
    st.subheader("📊 통계")
    for t in HIGH_TIERS:
        st.metric(get_base_name(t), f"{format_currency(st.session_state.stats.get(t, 0))}회")

# 9. 세이브 탭
with tabs[8]:
    st.subheader("💾 세이브 / 로드")
    data = json.dumps({k: st.session_state[k] for k in ["coins", "total_donated", "inventory", "unlocked", "special_inventory"]}, ensure_ascii=False)
    st.download_button("📥 다운로드", data, "save.json", "application/json")
    up = st.file_uploader("로드", type=["json"])
    if up and st.button("🔄 불러오기"):
        for k, v in json.load(up).items(): st.session_state[k] = v
        st.success("완료!"); st.rerun()

# 10. 개발자 탭
with tabs[9]:
    st.subheader("🔑 개발자 전용")
    if st.text_input("비밀번호", type="password") == "090925":
        add = st.number_input("지급 코인", value=10000.0, step=1000.0)
        if st.button("💰 지급 받기", type="primary"):
            st.session_state.coins += add; st.success("지급 완료!"); st.rerun()
