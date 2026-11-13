import base64
from datetime import datetime
import hashlib
import json
import os
import random
import sqlite3
import time
import streamlit as st

# 페이지 설정
st.set_page_config(
    page_title="아우라 가챠 & 도감", page_icon="✨", layout="wide"
)

# 등급 리스트 정의 (희귀도 높은 순)
items = [
    "𝓓𝓻𝓮𝓪𝓶𝓬𝓪𝓽𝓬𝓱𝓮𝓻",
    "스펙트라플로우",
    "감시자",
    "크로마틱",
    "자장가",
    "헬리오스",
    "황혼",
    "대마법사",
    "아케인",
    "워록",
    "바운디드",
    "재즈",
    "스펙터",
    "태양",
    "달",
    "와트",
    "힘",
    "석영",
    "시데리움",
    "자력",
    "분노",
    "결정화",
    "레어",
    "자연",
    "희귀",
    "일반",
]

# 각 분수 확률에 따른 기본 가중치 설정 (기준: 2,222,222,222)
base_weights = [
    1,
    22,
    49,
    111,
    131,
    247,
    370,
    1258,
    2222,
    3367,
    11111,
    13889,
    15873,
    44444,
    44444,
    67817,
    135634,
    271267,
    542535,
    1085069,
    8680556,
    17361111,
    138888889,
    277777778,
    555555556,
    1111111111,
]

# 각 아우라의 실제 분모 수치 (행운 배율 필터링 기준)
denominators = {
    "𝓓𝓻𝓮𝓪𝓶𝓬𝓪𝓽𝓬𝓱𝓮𝓻": 2222222222,
    "스펙트라플로우": 100000000,
    "감시자": 45000000,
    "크로마틱": 20000000,
    "자장가": 17000000,
    "헬리오스": 9000000,
    "황혼": 6000000,
    "대마법사": 1766000,
    "아케인": 1000000,
    "워록": 660000,
    "바운디드": 200000,
    "재즈": 160000,
    "스펙터": 140000,
    "태양": 50000,
    "달": 50000,
    "와트": 32768,
    "힘": 16384,
    "석영": 8192,
    "시데리움": 4096,
    "자력": 2048,
    "분노": 256,
    "결정화": 128,
    "레어": 16,
    "자연": 8,
    "희귀": 4,
    "일반": 2,
}

# 각 아우라의 분수 표시 문자열
fractions = {
    "𝓓𝓻𝓮𝓪𝓶𝓬𝓪𝓽𝓬𝓱𝓮𝓻": (
        "1 in 2,222,222,222 (밤 버프 시 2배 / 장착 시 밤 행운 100배)"
    ),
    "스펙트라플로우": "1 in 100,000,000",
    "감시자": "1 in 45,000,000",
    "크로마틱": "1 in 20,000,000",
    "자장가": "1 in 17,000,000 (밤 버프 시 1 in 1,700,000)",
    "헬리오스": "1 in 9,000,000",
    "황혼": "1 in 6,000,000 (밤 버프 시 1 in 600,000)",
    "대마법사": "1 in 1,766,000",
    "아케인": "1 in 1,000,000",
    "워록": "1 in 660,000",
    "바운디드": "1 in 200,000",
    "재즈": "1 in 160,000",
    "스펙터": "1 in 140,000",
    "태양": "1 in 50,000 (낮 버프 시 1 in 5,000)",
    "달": "1 in 50,000 (밤 버프 시 1 in 5,000)",
    "와트": "1 in 32,768",
    "힘": "1 in 16,384",
    "석영": "1 in 8,192",
    "시데리움": "1 in 4,096",
    "자력": "1 in 2,048",
    "분노": "1 in 256",
    "결정화": "1 in 128",
    "레어": "1 in 16",
    "자연": "1 in 8",
    "희귀": "1 in 4",
    "일반": "1 in 2",
}

# 컷씬이 존재하는 아우라 목록
cutscene_auras = [
    "𝓓𝓻𝓮𝓪𝓶𝓬𝓪𝓽𝓬𝓱𝓮𝓻",
    "스펙트라플로우",
    "감시자",
    "크로마틱",
    "자장가",
    "헬리오스",
    "황혼",
    "대마법사",
    "아케인",
    "워록",
    "바운디드",
    "재즈",
    "스펙터",
    "태양",
    "달",
    "와트",
    "힘",
    "석영",
    "시데리움",
]

# 등급별 이모티콘 매핑
icons = {
    "𝓓𝓻𝓮𝓪𝓶𝓬𝓪𝓽𝓬𝓱𝓮𝓻": "🕸️🌙✨🦋",
    "스펙트라플로우": "🌌💠💫",
    "감시자": "👁️‍🗨️⚡",
    "크로마틱": "🌈💫",
    "자장가": "🌌🎵💤",
    "헬리오스": "☀️🔥",
    "황혼": "🌆✨💜",
    "대마법사": "🧙‍♂️✨",
    "아케인": "🔮👑",
    "워록": "💀🔥",
    "바운디드": "🌌👑",
    "재즈": "🎶🎷",
    "스펙터": "👻🔮",
    "태양": "☀️✨",
    "달": "🌙✨",
    "와트": "⚡👑⚡",
    "힘": "⚡🔥",
    "석영": "💎✨",
    "시데리움": "🌟🛡️",
    "자력": "🧲💫",
    "분노": "😡💢",
    "결정화": "🔮✨",
    "레어": "💙📦",
    "자연": "🌿🍃",
    "희귀": "💧📘",
    "일반": "⚪📦",
}

# 등급별 테두리 색상
border_colors = {
    "𝓓𝓻𝓮𝓪𝓶𝓬𝓪𝓽𝓬𝓱𝓮𝓻": "#e066ff",
    "스펙트라플로우": "#00ffff",
    "감시자": "#ff0055",
    "크로마틱": "#ff00ff",
    "자장가": "#7a5cff",
    "헬리오스": "#ff9900",
    "황혼": "#b366ff",
    "대마법사": "#9933ff",
    "아케인": "#00ffff",
    "워록": "#ff3300",
    "바운디드": "#9900ff",
    "재즈": "#ff00aa",
    "스펙터": "#00ff88",
    "태양": "#ffcc00",
    "달": "#0099ff",
    "와트": "#00FFFF",
    "힘": "#FF0000",
    "석영": "#FF4500",
    "시데리움": "#FFD700",
    "자력": "#00CED1",
    "분노": "#FF1493",
    "결정화": "#9932CC",
    "레어": "#1E90FF",
    "자연": "#32CD32",
    "희귀": "#87CEEB",
    "일반": "#555555",
}

# 모든 등급 아우라 이미지 경로 매핑
aura_images = {
    "일반": "images/SmartSelect_20261113_115337_NAVER.jpg",
    "희귀": "images/SmartSelect_20261113_115402_NAVER.jpg",
    "자연": "images/SmartSelect_20261113_115446_NAVER.jpg",
    "레어": "images/SmartSelect_20261113_123717_Chrome.jpg",
    "결정화": "images/SmartSelect_20261113_123732_Chrome.jpg",
    "분노": "images/SmartSelect_20261113_123747_Chrome.jpg",
    "자력": "images/SmartSelect_20261113_123943_Chrome.jpg",
    "시데리움": "images/SmartSelect_20261113_123957_Chrome.jpg",
    "석영": "images/SmartSelect_20261113_124024_Chrome.jpg",
    "힘": "images/SmartSelect_20261113_124048_Chrome.jpg",
    "와트": "images/SmartSelect_20261113_125018_NAVER.jpg",
    "스펙터": "images/SmartSelect_20261113_125325_Chrome.jpg",
    "재즈": "images/SmartSelect_20261113_125353_Chrome.jpg",
    "바운디드": "images/SmartSelect_20261113_125424_Chrome.jpg",
    "워록": "images/SmartSelect_20261113_222357_Chrome.jpg",
    "아케인": "images/SmartSelect_20261113_222429_Chrome.jpg",
    "대마법사": "images/SmartSelect_20261113_230233_Chrome.jpg",
    "헬리오스": "images/SmartSelect_20261113_230344_Chrome.jpg",
    "크로마틱": "images/SmartSelect_20261113_230417_Chrome.jpg",
    "감시자": "images/SmartSelect_20261113_233734_Chrome.jpg",
    "스펙트라플로우": "images/SmartSelect_20261113_234508_Chrome.jpg",
    "태양": "images/SmartSelect_20261113_235302_Chrome.jpg",
    "달": "images/SmartSelect_20261113_235408_Chrome.jpg",
    "황혼": "images/SmartSelect_20261113_235637_Chrome.jpg",
    "자장가": "images/SmartSelect_20261113_235654_Chrome.jpg",
    "𝓓𝓻𝓮𝓪𝓶𝓬𝓪𝓽𝓬𝓱𝓮𝓻": "images/SmartSelect_20261113_235729_Chrome.jpg",
}

# 특수 장착 배경 이미지 매핑
equipped_backgrounds = {
    "𝓓𝓻𝓮𝓪𝓶𝓬𝓪𝓽𝓬𝓱𝓮𝓻": "Background/SmartSelect_20261114_000447_Chrome.jpg",
    "스펙트라플로우": "Background/SmartSelect_20261113_234652_NAVER.jpg",
    "감시자": "Background/SmartSelect_20261113_234106_Chrome.jpg",
    "크로마틱": "Background/SmartSelect_20261113_233022_Google.jpg",
    "자장가": "Background/SmartSelect_20261114_000015_Chrome.jpg",
}

# 행운권 상자 아이템 목록 및 메타데이터
potion_items = [
    "100배 행운 포션 (1분)",
    "500배 행운 포션 (30초)",
    "1000배 행운 포션 (15초)",
    "10000배 행운 포션 (10초)",
    "백만배 행운권 (1회)",
]
potion_weights = [900, 70, 20, 9, 1]
potion_config = {
    "100배 행운 포션 (1분)": {"mult": 100, "duration": 60, "type": "potion"},
    "500배 행운 포션 (30초)": {"mult": 500, "duration": 30, "type": "potion"},
    "1000배 행운 포션 (15초)": {"mult": 1000, "duration": 15, "type": "potion"},
    "10000배 행운 포션 (10초)": {"mult": 10000, "duration": 10, "type": "potion"},
    "백만배 행운권 (1회)": {"mult": 1000000, "duration": 0, "type": "ticket"},
}


# ==========================================
# 🗄️ SQLite 데이터베이스 설정 및 관리 함수
# ==========================================
def init_db():
  conn = sqlite3.connect("users.db", check_same_thread=False)
  cursor = conn.cursor()
  cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT,
            data TEXT
        )
    """)
  conn.commit()
  conn.close()


init_db()


def hash_password(password):
  return hashlib.sha256(password.encode()).hexdigest()


def save_user_data_to_db():
  if not st.session_state.get("logged_in", False):
    return
  username = st.session_state.username
  save_data = {
      "history": st.session_state.get("history", []),
      "counts": st.session_state.get("counts", {}),
      "equipped": st.session_state.get("equipped", None),
      "coins": st.session_state.get("coins", 0),
      "inventory_slots": st.session_state.get("inventory_slots", 50),
      "luck_buff_unlocked": st.session_state.get("luck_buff_unlocked", False),
      "triple_roll_unlocked": st.session_state.get(
          "triple_roll_unlocked", False
      ),
      "potions": st.session_state.get("potions", {}),
  }
  conn = sqlite3.connect("users.db", check_same_thread=False)
  cursor = conn.cursor()
  cursor.execute(
      "UPDATE users SET data = ? WHERE username = ?",
      (json.dumps(save_data, ensure_ascii=False), username),
  )
  conn.commit()
  conn.close()


# 세션 기본값 설정
if "logged_in" not in st.session_state:
  st.session_state.logged_in = False
if "username" not in st.session_state:
  st.session_state.username = ""


# ==========================================
# 🔐 로그인 / 회원가입 화면
# ==========================================
if not st.session_state.logged_in:
  st.title("✨ 아우라 가챠 & 도감 — 로그인")
  tab_login, tab_register = st.tabs(["로그인", "회원가입"])

  with tab_login:
    st.subheader("로그인")
    l_user = st.text_input("아이디", key="login_user")
    l_pass = st.text_input("비밀번호", type="password", key="login_pass")
    if st.button("로그인", type="primary", use_container_width=True):
      if l_user.strip() and l_pass.strip():
        conn = sqlite3.connect("users.db", check_same_thread=False)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT password, data FROM users WHERE username = ?", (l_user,)
        )
        row = cursor.fetchone()
        conn.close()

        if row and row[0] == hash_password(l_pass):
          st.session_state.logged_in = True
          st.session_state.username = l_user
          saved_data = json.loads(row[1])
          st.session_state.history = saved_data.get("history", [])
          st.session_state.counts = {
              item: saved_data.get("counts", {}).get(item, 0) for item in items
          }
          st.session_state.equipped = saved_data.get("equipped", None)
          st.session_state.coins = saved_data.get("coins", 0)
          st.session_state.inventory_slots = saved_data.get(
              "inventory_slots", 50
          )
          st.session_state.luck_buff_unlocked = saved_data.get(
              "luck_buff_unlocked", False
          )
          st.session_state.triple_roll_unlocked = saved_data.get(
              "triple_roll_unlocked", False
          )
          st.session_state.potions = {
              p: saved_data.get("potions", {}).get(p, 0) for p in potion_items
          }
          st.session_state.active_potion_mult = 1
          st.session_state.active_potion_end = 0.0
          st.session_state.active_potion_name = None
          st.session_state.million_ticket_active = False
          st.session_state.last_results = []
          st.session_state.last_luck_mult = 1
          st.session_state.selected_codex = items[0]

          st.success(f"환영합니다, {l_user}님! 게임을 시작합니다.")
          time.sleep(0.8)
          st.rerun()
        else:
          st.error("아이디 또는 비밀번호가 올바르지 않습니다.")
      else:
        st.warning("아이디와 비밀번호를 모두 입력해주세요.")

  with tab_register:
    st.subheader("회원가입")
    r_user = st.text_input("사용할 아이디", key="reg_user")
    r_pass = st.text_input("사용할 비밀번호", type="password", key="reg_pass")
    if st.button("가입하기", type="secondary", use_container_width=True):
      if r_user.strip() and r_pass.strip():
        conn = sqlite3.connect("users.db", check_same_thread=False)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT username FROM users WHERE username = ?", (r_user,)
        )
        exist = cursor.fetchone()
        if exist:
          conn.close()
          st.error("이미 존재하는 아이디입니다.")
        else:
          new_user_init_data = {
              "history": [],
              "counts": {item: 0 for item in items},
              "equipped": None,
              "coins": 0,
              "inventory_slots": 50,
              "luck_buff_unlocked": False,
              "triple_roll_unlocked": False,
              "potions": {p: 0 for p in potion_items},
          }
          cursor.execute(
              "INSERT INTO users (username, password, data) VALUES (?, ?, ?)",
              (
                  r_user,
                  hash_password(r_pass),
                  json.dumps(new_user_init_data, ensure_ascii=False),
              ),
          )
          conn.commit()
          conn.close()
          st.success(
              "회원가입이 완료되었습니다! 로그인 탭에서 로그인해 주세요."
          )
      else:
        st.warning("아이디와 비밀번호를 모두 입력해주세요.")

  st.stop()


# ==========================================
# ☀️🌙 [현재 낮/밤 판별 함수: 3분(180초) 주기로 교체]
# ==========================================
def get_world_time_status():
  cycle_time = int(time.time()) % 360
  is_day = cycle_time < 180
  rem_sec = 180 - (cycle_time % 180)
  return is_day, rem_sec


# 🎨 [특수 아우라 장착 배경 적용 함수]
def apply_equipped_background():
  eq = st.session_state.get("equipped")
  bg_path = equipped_backgrounds.get(eq)
  if bg_path and os.path.exists(bg_path):
    with open(bg_path, "rb") as img_file:
      encoded_bg = base64.b64encode(img_file.read()).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: linear-gradient(rgba(10, 10, 18, 0.72), rgba(10, 10, 18, 0.85)), url("data:image/jpeg;base64,{encoded_bg}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


apply_equipped_background()


# 현재 적용 중인 총 행운 배율 계산 함수
def get_current_luck_multiplier(next_pull_number):
  now = time.time()
  if (
      st.session_state.active_potion_mult > 1
      and now >= st.session_state.active_potion_end
  ):
    st.session_state.active_potion_mult = 1
    st.session_state.active_potion_end = 0.0
    st.session_state.active_potion_name = None

  mult = 1

  if st.session_state.million_ticket_active:
    mult *= 1000000
  elif (
      st.session_state.active_potion_mult > 1
      and now < st.session_state.active_potion_end
  ):
    mult *= st.session_state.active_potion_mult

  if st.session_state.luck_buff_unlocked and (next_pull_number % 10 == 0):
    mult *= 2

  is_day, _ = get_world_time_status()
  if not is_day and st.session_state.get("equipped") == "𝓓𝓻𝓮𝓪𝓶𝓬𝓪𝓽𝓬𝓱𝓮𝓻":
    mult *= 100

  return mult


# ✨ [확률별 맞춤형 화려한 풀스크린 컷씬 (최초 1회만 재생)]
def play_fullscreen_star_cutscene(aura_name):
  placeholder = st.empty()

  if aura_name == "𝓓𝓻𝓮𝓪𝓶𝓬𝓪𝓽𝓬𝓱𝓮𝓻":
    star_color = "#e066ff"
    bg_style = "radial-gradient(circle, #2e004d 0%, #05000a 90%)"
    star_symbol = "🕸️🌙✨🦋"
    ment = (
        "🕸️ [DREAMCATCHER] 현실과 환상의 경계가 허물어지며 영원한 꿈의"
        " 수호자가 강림합니다!"
    )
    duration = 4.2
  elif aura_name == "스펙트라플로우":
    star_color = "#00ffff"
    bg_style = "radial-gradient(circle, #00334d 0%, #05000a 90%)"
    star_symbol = "🌌💠⚡💫"
    ment = (
        "🌌 [SPECTRAFLOW] 무한한 차원의 흐름이 공명하며 우주의 근원을"
        " 뒤흔듭니다!"
    )
    duration = 3.8
  elif aura_name == "감시자":
    star_color = "#ff0055"
    bg_style = "radial-gradient(circle, #40001a 0%, #05000a 90%)"
    star_symbol = "👁️‍🗨️⚡🌀"
    ment = (
        "👁️ [OBSERVER] 모든 시공간을 초월하여 영원히 주시하는 절대자의 시선이"
        " 깨어납니다!"
    )
    duration = 3.5
  elif aura_name == "크로마틱":
    star_color = "#ff00ff"
    bg_style = "radial-gradient(circle, #330033 0%, #05000a 90%)"
    star_symbol = "🌟💫🌈"
    ment = (
        "⚠️ [UNIVERSE BREAK] 우주의 모든 스펙트럼이 융합하여 절대적인 빛이"
        " 탄생합니다!"
    )
    duration = 3.2
  elif aura_name == "자장가":
    star_color = "#7a5cff"
    bg_style = "radial-gradient(circle, #1a0d4d 0%, #05000a 90%)"
    star_symbol = "🌌🎵💤✨"
    ment = (
        "🌌 [LULLABY] 깊은 밤의 성좌들이 노래하며 영원한 안식의 선율이 울려"
        " 퍼집니다!"
    )
    duration = 3.2
  elif aura_name == "황혼":
    star_color = "#b366ff"
    bg_style = "radial-gradient(circle, #33114d 0%, #0a050d 90%)"
    star_symbol = "🌆✨💜"
    ment = (
        "🌆 [TWILIGHT] 낮과 밤의 경계가 교차하며 몽환적인 보랏빛 하늘이"
        " 열립니다!"
    )
    duration = 3.0
  elif aura_name == "태양":
    star_color = "#ffcc00"
    bg_style = "radial-gradient(circle, #4d3300 0%, #0a0500 90%)"
    star_symbol = "☀️🔥✨"
    ment = (
        "☀️ [SOLARIS] 찬란한 태양의 권능이 온 세상을 황금빛으로 비춥니다!"
    )
    duration = 2.8
  elif aura_name == "달":
    star_color = "#0099ff"
    bg_style = "radial-gradient(circle, #001a33 0%, #00050a 90%)"
    star_symbol = "🌙✨❄️"
    ment = (
        "🌙 [LUNARIS] 신비로운 달빛의 기운이 어둠 속에서 찬란하게 피어납니다!"
    )
    duration = 2.8
  elif aura_name == "헬리오스":
    star_color = "#ff6600"
    bg_style = "radial-gradient(circle, #4d1a00 0%, #0a0500 90%)"
    star_symbol = "☀️🔥"
    ment = "🔥 [SOLAR FLARE] 태양계의 모든 권능이 폭발하며 차원을 불태웁니다!"
    duration = 3.0
  elif aura_name == "대마법사":
    star_color = "#b84dff"
    bg_style = "radial-gradient(circle, #260033 0%, #05000a 90%)"
    star_symbol = "🧙‍♂️✨🔮"
    ment = "🔮 [ARCHMAGE] 금지된 고대의 아르카나 마력이 온 세상에 해방됩니다!"
    duration = 2.8
  elif aura_name == "아케인":
    star_color = "#00ffff"
    bg_style = "radial-gradient(circle, #003333 0%, #00050a 90%)"
    star_symbol = "🔮👑"
    ment = (
        "태고의 신비로운 아케인 에너지가 온 차원을 뒤덮고 영원히 빛납니다..."
    )
    duration = 2.5
  else:
    star_color = "#ffd700"
    bg_style = "rgba(5, 5, 10, 0.95)"
    star_symbol = "✦"
    ment = "전설적인 에너지가 요동칩니다..."
    duration = 2.2

  fullscreen_html = f"""
    <style>
    @keyframes epicSpinAndGrow {{
        0% {{ transform: rotate(0deg) scale(0.2); opacity: 0.1; filter: brightness(0.5); }}
        50% {{ transform: rotate(540deg) scale(1.8); opacity: 0.9; filter: brightness(1.5); }}
        100% {{ transform: rotate(1080deg) scale(4.0); opacity: 1; filter: brightness(2.0); }}
    }}
    .fullscreen-overlay {{
        position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
        background: {bg_style};
        display: flex; flex-direction: column; justify-content: center; align-items: center;
        z-index: 999999; text-align: center;
    }}
    .fullscreen-star {{
        display: inline-block;
        animation: epicSpinAndGrow {duration}s cubic-bezier(0.25, 1, 0.5, 1) forwards;
        font-size: 110px; color: {star_color}; text-shadow: 0 0 60px {star_color}, 0 0 100px {star_color};
    }}
    </style>
    <div class="fullscreen-overlay">
        <div class="fullscreen-star">{star_symbol}</div>
        <h1 style="color: {star_color}; margin-top: 35px; font-size: 42px; text-shadow: 0 0 25px {star_color}; letter-spacing: 2px;">
            [{aura_name}] 강림 임박!
        </h1>
        <p style="font-size: 24px; color: #ffeb3b; margin-top: 15px; font-weight: bold; max-width: 850px; text-shadow: 0 0 10px rgba(0,0,0,0.8);">
            {ment}
        </p>
    </div>
    """

  with placeholder.container():
    st.markdown(fullscreen_html, unsafe_allow_html=True)

  time.sleep(duration)
  placeholder.empty()


def play_cutscene(aura_name):
  play_fullscreen_star_cutscene(aura_name)


# 1회 또는 다회 뽑기 실행 공통 함수 (버튼 잠금 현상 완전 제거)
def perform_rolls(roll_count=1):
  results = []
  max_luck_applied = 1
  coin_gain_per_roll = (
      10 if st.session_state.get("equipped") == "스펙트라플로우" else 5
  )
  is_day, _ = get_world_time_status()

  prior_counts = {item: st.session_state.counts.get(item, 0) for item in items}

  for _ in range(roll_count):
    next_pull = sum(st.session_state.counts.values()) + 1
    luck_mult = get_current_luck_multiplier(next_pull)
    max_luck_applied = max(max_luck_applied, luck_mult)

    if st.session_state.million_ticket_active:
      st.session_state.million_ticket_active = False

    current_weights = list(base_weights)
    if is_day:
      current_weights[items.index("태양")] *= 10
    else:
      current_weights[items.index("달")] *= 10
      current_weights[items.index("황혼")] *= 10
      current_weights[items.index("자장가")] *= 10
      current_weights[items.index("𝓓𝓻𝓮𝓪𝓶𝓬𝓪𝓽𝓬𝓱𝓮𝓻")] *= 2

    if luck_mult > 1:
      eligible_indices = [
          idx
          for idx, item in enumerate(items)
          if denominators[item] >= luck_mult
      ]
      if eligible_indices:
        for idx in range(len(items)):
          if idx not in eligible_indices:
            current_weights[idx] = 0
          else:
            current_weights[idx] = current_weights[idx] * luck_mult
      else:
        current_weights = [1] + [0] * (len(items) - 1)

    if sum(current_weights) <= 0:
      current_weights = [1] * len(items)

    result = random.choices(items, weights=current_weights, k=1)[0]
    results.append(result)

    st.session_state.counts[result] += 1
    st.session_state.history.insert(0, result)
    st.session_state.coins += coin_gain_per_roll

  new_cutscene_targets = [
      r
      for r in results
      if r in cutscene_auras and prior_counts.get(r, 0) == 0
  ]

  if new_cutscene_targets:
    rarest_aura = min(new_cutscene_targets, key=lambda x: items.index(x))
    play_cutscene(rarest_aura)
    st.balloons()

  st.session_state.last_results = results
  st.session_state.last_luck_mult = max_luck_applied

  save_user_data_to_db()
  return results


# ==========================================
# 🎮 메인 게임 화면
# ==========================================
st.title("✨ 아우라 가챠 & 도감 시스템")

c_u1, c_u2 = st.columns([4, 1])
with c_u1:
  st.markdown(
      f"👤 현재 접속 계정: **`{st.session_state.username}`**님 (자동 영구 저장"
      " 활성화됨)"
  )
with c_u2:
  if st.button("로그아웃", use_container_width=True):
    save_user_data_to_db()
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.rerun()

is_day_now, rem_seconds_now = get_world_time_status()
m_rem = rem_seconds_now // 60
s_rem = rem_seconds_now % 60
is_dc_equipped = st.session_state.get("equipped") == "𝓓𝓻𝓮𝓪𝓶𝓬𝓪𝓽𝓬𝓱𝓮𝓻"

if is_day_now:
  st.markdown(
      f"""
        <div style="background: linear-gradient(90deg, #ff9900, #ffcc00); padding: 12px; border-radius: 8px; text-align: center; color: black; font-weight: bold; font-size: 18px; margin-bottom: 15px; box-shadow: 0 0 15px rgba(255,204,0,0.5);">
            🌞 [현재 낮 시간대] 태양(☀️) 확률 10배 폭증 중! (남은 시간: {m_rem}분 {s_rem}초 후 밤으로 전환)
        </div>
        """,
      unsafe_allow_html=True,
  )
else:
  dc_bonus_text = (
      " | 🕸️ 𝓓𝓻𝓮𝓪𝓶𝓬𝓪𝓽𝓬𝓱𝓮𝓻 장착 중: 행운 100배 발동 중!"
      if is_dc_equipped
      else ""
  )
  st.markdown(
      f"""
        <div style="background: linear-gradient(90deg, #003366, #2b1a66); padding: 12px; border-radius: 8px; text-align: center; color: white; font-weight: bold; font-size: 16px; margin-bottom: 15px; box-shadow: 0 0 15px rgba(153,102,255,0.5);">
            🌙 [현재 밤 시간대] 달·황혼·자장가 10배 / 𝓓𝓻𝓮𝓪𝓶𝓬𝓪𝓽𝓬𝓱𝓮𝓻 2배 폭증 중! (남은 시간: {m_rem}분 {s_rem}초 후 낮으로 전환){dc_bonus_text}
        </div>
        """,
      unsafe_allow_html=True,
  )

with st.container(border=True):
  st.markdown("### 👤 현재 장착 중인 아우라")
  equipped_aura = st.session_state.get("equipped")

  if equipped_aura and equipped_aura in items:
    col_img, col_info = st.columns([1, 4])
    img_path = aura_images.get(equipped_aura)

    with col_img:
      if img_path and os.path.exists(img_path):
        st.image(img_path, use_container_width=True)
      else:
        st.markdown(
            f"<div style='font-size: 50px; text-align: center;'>{icons.get(equipped_aura, '✨')}</div>",
            unsafe_allow_html=True,
        )

    with col_info:
      st.markdown(
          f"#### {icons.get(equipped_aura, '✨')} **[{equipped_aura}]** 장착"
          " 중"
      )
      st.write(
          f"보유 수량: **{st.session_state.counts.get(equipped_aura, 0)}개**"
      )
      if equipped_aura == "스펙트라플로우":
        st.caption(
            "💠 **[특수 능력]** 코인 획득량 2배 (뽑기당 10 G) & 전용 배경"
            " 적용 중!"
        )
      elif equipped_aura == "𝓓𝓻𝓮𝓪𝓶𝓬𝓪𝓽𝓬𝓱𝓮𝓻":
        st.caption(
            "🕸️ **[특수 능력]** 밤 시간대 행운 100배 버프 적용 중! & 전용"
            " 배경 적용 중!"
        )
      elif equipped_aura in equipped_backgrounds:
        st.caption("🌌 전용 배경 테마가 적용되어 있습니다.")
      if st.button("❌ 장착 해제", key="top_unequip_btn"):
        st.session_state.equipped = None
        save_user_data_to_db()
        st.rerun()
  else:
    st.session_state.equipped = None
    st.info(
        "현재 장착된 아우라가 없습니다. 뽑기를 통해 아우라를 획득하고"
        " 장착해보세요!"
    )

col_c1, col_c2 = st.columns(2)
with col_c1:
  st.metric(label="💰 보유 코인", value=f"{st.session_state.coins} G")
with col_c2:
  total_pulls = sum(st.session_state.counts.values())
  st.metric(label="🎲 총 뽑기 횟수", value=f"{total_pulls}회")

st.divider()

tab_gacha, tab_inventory, tab_potions, tab_codex, tab_shop = st.tabs(
    ["🎲 아우라 뽑기", "🎒 스토리지", "🧪 포션 인벤토리", "📖 도감 (Codex)", "🛒 상점"]
)

with tab_gacha:
  roll_coin_label = (
      "1회당 +10 G (스펙트라플로우 효과)"
      if st.session_state.get("equipped") == "스펙트라플로우"
      else "1회당 +5 G"
  )
  st.subheader(f"🎲 행운의 아우라 소환 ({roll_coin_label})")

  now = time.time()
  if (
      st.session_state.active_potion_mult > 1
      and now < st.session_state.active_potion_end
  ):
    rem_sec = int(st.session_state.active_potion_end - now)
    st.warning(
        f"🧪 **[포션 버프 적용 중]** {st.session_state.active_potion_name} —"
        f" 남은 시간: **{rem_sec}초** (최소 1/{st.session_state.active_potion_mult:,}"
        " 이상 확정!)"
    )
  elif (
      st.session_state.active_potion_mult > 1
      and now >= st.session_state.active_potion_end
  ):
    st.session_state.active_potion_mult = 1
    st.session_state.active_potion_end = 0.0
    st.session_state.active_potion_name = None

  if st.session_state.million_ticket_active:
    st.error(
        "🎟️ **[백만배 행운권 장전 완료!]** 다음 뽑기 1회에 최소 **1/1,000,000"
        " (아케인 이상)** 아우라가 100% 확정 등장합니다!"
    )

  if st.session_state.luck_buff_unlocked:
    st.success("🍀 [영구 버프 활성화됨] 매 10번째 뽑기마다 행운 2배 적용 중!")

  with st.expander("📋 등급별 기본 확률표 보기"):
    weights_sum = sum(base_weights)
    for item, weight in zip(items, base_weights):
      prob = (weight / weights_sum) * 100
      if prob < 0.01:
        prob_str = f"{prob:.8f}%"
      else:
        prob_str = f"{prob:.4f}%"
      st.markdown(
          f"- **{icons.get(item, '✨')} {item}** : `{prob_str}`"
          f" ({fractions.get(item, 'N/A')})"
      )

  st.write("")

  if st.session_state.triple_roll_unlocked:
    col_b1, col_b2 = st.columns(2)
    with col_b1:
      if st.button("🎲 1회 무료 뽑기", type="secondary", use_container_width=True):
        perform_rolls(1)
        st.rerun()
    with col_b2:
      triple_bonus_coins = (
          30 if st.session_state.get("equipped") == "스펙트라플로우" else 15
      )
      if st.button(
          f"🔥 3회 연속 뽑기 (+{triple_bonus_coins} G)",
          type="primary",
          use_container_width=True,
      ):
        perform_rolls(3)
        st.rerun()
  else:
    if st.button("🎲 1회 무료 뽑기", type="primary", use_container_width=True):
      perform_rolls(1)
      st.rerun()

  if st.session_state.last_luck_mult > 1:
    st.markdown(
        f"""
        <div style="text-align: center; padding: 12px; background-color: #004d40; color: #66ffcc; border-radius: 8px; margin-top: 10px; border: 1px solid #00b0ff; font-weight: bold; font-size: 18px;">
            🍀 [행운 {st.session_state.last_luck_mult:,}배 활성화!] 최소 1/{st.session_state.last_luck_mult:,} 이상 등급이 보장되었습니다! 🍀
        </div>
        """,
        unsafe_allow_html=True,
    )

  if st.session_state.last_results:
    res_list = st.session_state.last_results
    per_coin = (
        10 if st.session_state.get("equipped") == "스펙트라플로우" else 5
    )
    earned_coins = len(res_list) * per_coin
    result_badges = " &nbsp;|&nbsp; ".join(
        [f"{icons.get(r, '✨')} [{r}]" for r in res_list]
    )
    st.markdown(
        f"""
        <div style="text-align: center; padding: 20px; background-color: #1e1e1e; color: white; border-radius: 10px; margin-top: 15px;">
            <span style="font-size: 28px; font-weight: bold;">
                {result_badges} 획득!
            </span>
            <p style="color: #ffd700; margin-top: 8px;">(+ {earned_coins} 코인 획득)</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

  st.divider()
  st.subheader("📜 최근 뽑기 기록")
  if st.session_state.history:
    recent = st.session_state.history[:8]
    for i, res in enumerate(recent):
      st.text(
          f"{len(st.session_state.history) - i}번째: {icons.get(res, '✨')} [{res}]"
      )
  else:
    st.text("아직 뽑기 기록이 없습니다.")

with tab_inventory:
  owned_items = [
      item
      for item in items
      if st.session_state.counts.get(item, 0) > 0
  ]
  st.subheader(
      f"📦 아우라 스토리지 [보유 종류: {len(owned_items)} / {len(items)}]"
  )

  if owned_items:
    st.write("획득한 아우라를 확인하고 장착할 수 있습니다.")
    cols_per_row = 4
    rows = [
        owned_items[i : i + cols_per_row]
        for i in range(0, len(owned_items), cols_per_row)
    ]

    for row in rows:
      cols = st.columns(cols_per_row)
      for idx, item in enumerate(row):
        with cols[idx]:
          count = st.session_state.counts.get(item, 0)
          is_equipped = st.session_state.get("equipped") == item
          b_color = border_colors.get(item, "#ffffff")
          icon = icons.get(item, "✨")

          bg_color = "#1b3a4b" if is_equipped else "#222222"

          st.markdown(
              f"""
              <div style="background-color: {bg_color}; border: 2px solid {b_color}; border-radius: 8px; padding: 12px; text-align: center; margin-bottom: 10px; min-height: 110px;">
                  <div style="font-size: 24px;">{icon}</div>
                  <div style="font-weight: bold; color: white; font-size: 14px; margin-top: 4px;">{item}</div>
                  <div style="color: #aaa; font-size: 11px; margin-top: 2px;">보유: {count}개</div>
                  {"<div style='color: #4da6ff; font-size: 11px; font-weight: bold; margin-top: 2px;'>[장착 중]</div>" if is_equipped else ""}
              </div>
              """,
              unsafe_allow_html=True,
          )

          if is_equipped:
            st.button(
                "장착중",
                key=f"inv_eq_{item}",
                disabled=True,
                use_container_width=True,
            )
          else:
            if st.button(
                "장착", key=f"inv_btn_{item}", use_container_width=True
            ):
              st.session_state.equipped = item
              save_user_data_to_db()
              st.rerun()
      st.write("")
  else:
    st.markdown(
        """
        <div style="text-align: center; padding: 50px; color: #777;">
            <h3>🎒 스토리지가 비어 있습니다!</h3>
            <p>뽑기를 통해 첫 아우라를 획득해보세요.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with tab_potions:
  st.subheader("🧪 포션 인벤토리")
  st.write("상점에서 구매한 행운 포션과 백만배 행운권을 확인하고 사용할 수 있습니다.")

  all_potions_count = sum(st.session_state.potions.values())
  if all_potions_count > 0:
    p_cols_per_row = 3
    p_rows = [
        potion_items[i : i + p_cols_per_row]
        for i in range(0, len(potion_items), p_cols_per_row)
    ]

    for row in p_rows:
      cols = st.columns(p_cols_per_row)
      for idx, p_name in enumerate(row):
        count = st.session_state.potions.get(p_name, 0)
        with cols[idx]:
          st.markdown(
              f"""
              <div style="background-color: #222222; border: 2px solid #00b0ff; border-radius: 8px; padding: 15px; text-align: center; margin-bottom: 10px; min-height: 120px;">
                  <div style="font-size: 28px;">🧪</div>
                  <div style="font-weight: bold; color: white; font-size: 14px; margin-top: 6px;">{p_name}</div>
                  <div style="color: #66ffcc; font-size: 12px; margin-top: 4px;">보유: {count}개</div>
              </div>
              """,
              unsafe_allow_html=True,
          )
          if count > 0:
            if st.button(
                "사용하기", key=f"tab_use_pot_{p_name}", use_container_width=True
            ):
              st.session_state.potions[p_name] -= 1
              cfg = potion_config[p_name]
              if cfg["type"] == "potion":
                st.session_state.active_potion_mult = cfg["mult"]
                st.session_state.active_potion_end = (
                    time.time() + cfg["duration"]
                )
                st.session_state.active_potion_name = p_name
              elif cfg["type"] == "ticket":
                st.session_state.million_ticket_active = True
              save_user_data_to_db()
              st.rerun()
          else:
            st.button(
                "보유 없음",
                key=f"tab_none_pot_{p_name}",
                disabled=True,
                use_container_width=True,
            )
      st.write("")
  else:
    st.markdown(
        """
        <div style="text-align: center; padding: 50px; color: #777;">
            <h3>🧪 포션 인벤토리가 비어 있습니다!</h3>
            <p>상점에서 행운권 상자를 구매하여 포션을 획득해보세요.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with tab_codex:
  st.subheader("📖 아우라 도감 (Aura Codex)")
  st.write(
      "왼쪽 목록에서 아우라를 선택하여 상세 정보와 컷씬을 확인할 수"
      " 있습니다."
  )

  col_left, col_right = st.columns([1, 1.5])

  with col_left:
    st.markdown("#### 📜 등급 목록")
    for item in items:
      is_owned = st.session_state.counts.get(item, 0) > 0
      display_name = (
          f"{icons.get(item, '✨')} {item}" if is_owned else "🔒 [LOCKED] ???"
      )

      if st.button(
          display_name,
          key=f"codex_select_{item}",
          use_container_width=True,
      ):
        st.session_state.selected_codex = item

  with col_right:
    sel = st.session_state.selected_codex
    if sel not in items:
      sel = items[0]
    is_owned = st.session_state.counts.get(sel, 0) > 0
    st.markdown(f"#### 상세 정보: `{sel if is_owned else '???'}`")

    with st.container(border=True):
      if is_owned:
        img_path = aura_images.get(sel)
        if img_path and os.path.exists(img_path):
          st.image(img_path, width=150)
        else:
          st.markdown(
              f"<div style='font-size: 40px;'>{icons.get(sel, '✨')}</div>",
              unsafe_allow_html=True,
          )

        st.markdown(f"### [{sel}]")
        st.write(f"**희귀도 확률:** {fractions.get(sel, 'N/A')}")
        st.write(f"**보유 수량:** {st.session_state.counts.get(sel, 0)}개")
        st.markdown("---")

        if sel in cutscene_auras:
          st.info("이 아우라는 전용 연출 컷씬이 존재합니다!")
          if st.button("🎬 컷씬 다시 보기", use_container_width=True):
            play_cutscene(sel)
        else:
          st.caption("이 아우라에는 별도의 컷씬 연출이 없습니다.")
      else:
        st.markdown(
            """
            <div style="text-align: center; padding: 40px; color: #777;">
                <h2>🔒</h2>
                <h3>아직 획득하지 못한 아우라입니다.</h3>
                <p>뽑기를 통해 도감을 해금해보세요!</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

with tab_shop:
  st.subheader("🛒 상점 & 데이터 관리")

  with st.container(border=True):
    col_box1, col_box2 = st.columns([2, 1])
    with col_box1:
      st.markdown("### 🎁 행운권 상자 (즉시 개봉)")
      st.write(
          "초고배율 행운 포션이나 백만배 행운권을 획득할 수 있는 미스터리"
          " 상자입니다."
      )
      with st.expander("📋 상자 구성품 확률 보기"):
        st.markdown("- **90%**: 100배 행운 포션 (1분) — 최소 1/128 이상 보장")
        st.markdown("- **7%**: 500배 행운 포션 (30초) — 최소 1/2,048 이상 보장")
        st.markdown("- **2%**: 1000배 행운 포션 (15초) — 최소 1/2,048 이상 보장")
        st.markdown("- **0.9%**: 10000배 행운 포션 (10초) — 최소 1/16,384 이상 보장")
        st.markdown("- **0.1%**: 백만배 행운권 (1회) — 최소 1/1,000,000 (아케인 이상) 확정!")
    with col_box2:
      st.write("")
      if st.button(
          "상자 구매 및 열기 (300 G)",
          type="primary",
          key="buy_luck_box",
          use_container_width=True,
      ):
        if st.session_state.coins >= 300:
          st.session_state.coins -= 300
          won_item = random.choices(
              potion_items, weights=potion_weights, k=1
          )[0]
          st.session_state.potions[won_item] += 1
          save_user_data_to_db()
          st.success(f"🎉 행운권 상자에서 **[{won_item}]**을(를) 획득했습니다!")
          st.balloons()
          time.sleep(1.2)
          st.rerun()
        else:
          st.error("코인이 부족합니다! (300 G 필요)")

  with st.container(border=True):
    col_t1, col_t2 = st.columns([2, 1])
    with col_t1:
      st.markdown("### 🔥 3회씩 연속 뽑기 (영구)")
      st.write(
          "한 번에 3회씩 아우라를 빠르게 소환할 수 있는 기능을 해금합니다."
      )
    with col_t2:
      st.write("")
      if st.session_state.triple_roll_unlocked:
        st.button(
            "보유 완료",
            disabled=True,
            key="buy_triple_done",
            use_container_width=True,
        )
      else:
        if st.button(
            "구매 (500 G)", key="buy_triple_roll", use_container_width=True
        ):
          if st.session_state.coins >= 500:
            st.session_state.coins -= 500
            st.session_state.triple_roll_unlocked = True
            save_user_data_to_db()
            st.success("3회 연속 뽑기 기능이 해금되었습니다!")
            st.rerun()
          else:
            st.error("코인이 부족합니다! (500 G 필요)")

  with st.container(border=True):
    col_l1, col_l2 = st.columns([2, 1])
    with col_l1:
      st.markdown("### 🍀 10뽑마다 행운 2배 버프 (영구)")
      st.write("매 10번째 뽑기마다 상위 아우라를 얻을 확률이 2배로 증가합니다!")
    with col_l2:
      st.write("")
      if st.session_state.luck_buff_unlocked:
        st.button(
            "구매 완료",
            disabled=True,
            key="buy_luck_done",
            use_container_width=True,
        )
      else:
        if st.button(
            "구매 (200 G)", key="buy_luck_buff", use_container_width=True
        ):
          if st.session_state.coins >= 200:
            st.session_state.coins -= 200
            st.session_state.luck_buff_unlocked = True
            save_user_data_to_db()
            st.success("10뽑마다 행운 2배 버프가 해금되었습니다!")
            st.rerun()
          else:
            st.error("코인이 부족합니다!")

  with st.container(border=True):
    col_s1, col_s2 = st.columns([2, 1])
    with col_s1:
      st.markdown("### 🎒 아우라 가방 확장권")
      st.write(
          f"현재 가방 최대 수용 칸수: **{st.session_state.inventory_slots}칸**"
      )
    with col_s2:
      st.write("")
      if st.button("구매 (50 G)", key="buy_bag", use_container_width=True):
        if st.session_state.coins >= 50:
          st.session_state.coins -= 50
          st.session_state.inventory_slots += 20
          save_user_data_to_db()
          st.success("가방 칸수가 확장되었습니다!")
          st.rerun()
        else:
          st.error("코인이 부족합니다!")

  with st.container(border=True):
    st.markdown("### 💻 개발자 인증 패널")
    st.write("비밀번호를 입력하고 개발자 권한을 활성화하세요.")

    dev_password = st.text_input(
        "개발자 비밀번호", type="password", key="dev_pw_input"
    )
    if st.button("🔐 권한 인증 및 모든 도감 해금", type="primary"):
      if dev_password == "0925":
        for item in items:
          st.session_state.counts[item] = max(
              1, st.session_state.counts.get(item, 1)
          )
        save_user_data_to_db()
        st.success(
            "개발자 인증 성공! 모든 아우라 도감과 스토리지에 해금되었습니다!"
        )
        st.rerun()
      else:
        st.error("비밀번호가 틀렸습니다!")

  st.write("")
  if st.button(
      "🔄 현재 계정 데이터 초기화",
      type="secondary",
      use_container_width=True,
  ):
    st.session_state.history = []
    st.session_state.counts = {item: 0 for item in items}
    st.session_state.equipped = None
    st.session_state.coins = 0
    st.session_state.inventory_slots = 50
    st.session_state.luck_buff_unlocked = False
    st.session_state.triple_roll_unlocked = False
    st.session_state.potions = {p: 0 for p in potion_items}
    st.session_state.active_potion_mult = 1
    st.session_state.active_potion_end = 0.0
    st.session_state.active_potion_name = None
    st.session_state.million_ticket_active = False
    st.session_state.last_results = []
    st.session_state.last_luck_mult = 1
    st.session_state.selected_codex = items[0]
    save_user_data_to_db()
    st.rerun()
