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
    "𝓘𝓬𝓮𝓐𝓰𝓮",
    "𝓜𝓪𝓶𝓶𝓸𝓽𝓱",
    "𝓓𝓻𝓮𝓪𝓶𝓬𝓪𝓽𝓬𝓱𝓮𝓻",
    "𝓢𝓹𝓮𝓬𝓽𝓻𝓪𝓕𝓵𝓸𝔀 𖤐",
    "감시자",
    "크로마틱",
    "자장가",
    "블리자드",
    "헬리오스",
    "황혼",
    "대마법사",
    "아케인",
    "워록",
    "바운디드",
    "재즈",
    "스펙터",
    "만년서리",
    "태양",
    "달",
    "와트",
    "힘",
    "빙하",
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

# 각 아우라의 실제 분모 수치 (행운 배율 필터링 및 확률 기준)
denominators = {
    "𝓘𝓬𝓮𝓐𝓰𝓮": 1500000000,
    "𝓜𝓪𝓶𝓶𝓸𝓽𝓱": 300000000,
    "𝓓𝓻𝓮𝓪𝓶𝓬𝓪𝓽𝓬𝓱𝓮𝓻": 2222222222,
    "𝓢𝓹𝓮𝓬𝓽𝓻𝓪𝓕𝓵𝓸𝔀 𖤐": 100000000,
    "감시자": 45000000,
    "크로마틱": 20000000,
    "자장가": 17000000,
    "블리자드": 27315000,
    "헬리오스": 9000000,
    "황혼": 6000000,
    "대마법사": 1766000,
    "아케인": 1000000,
    "워록": 660000,
    "바운디드": 200000,
    "재즈": 160000,
    "스펙터": 140000,
    "만년서리": 73500,
    "태양": 50000,
    "달": 50000,
    "와트": 32768,
    "힘": 16384,
    "빙하": 2304,
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

# 분모를 기반으로 정확한 가중치 자동 생성
base_weights = [int(1000000000000 / denominators[item]) for item in items]

# 각 아우라의 분수 표시 문자열
fractions = {
    "𝓘𝓬𝓮𝓐𝓰𝓮": "1 in 1,500,000,000 (눈올 때 행운 10배)",
    "𝓜𝓪𝓶𝓶𝓸𝓽𝓱": "1 in 300,000,000 (눈 확률 10% 증가)",
    "𝓓𝓻𝓮𝓪𝓶𝓬𝓪𝓽𝓬𝓱𝓮𝓻": (
        "1 in 2,222,222,222 (밤 버프 시 2배 / 장착 시 밤 행운 10배)"
    ),
    "𝓢𝓹𝓮𝓬𝓽𝓻𝓪𝓕𝓵𝓸𝔀 𖤐": "1 in 100,000,000",
    "감시자": "1 in 45,000,000",
    "크로마틱": "1 in 20,000,000",
    "자장가": "1 in 17,000,000 (밤 버프 시 1 in 1,700,000)",
    "블리자드": "1 in 27,315,000 (눈올 때 확률 3배)",
    "헬리오스": "1 in 9,000,000",
    "황혼": "1 in 6,000,000 (밤 버프 시 1 in 600,000)",
    "대마법사": "1 in 1,766,000",
    "아케인": "1 in 1,000,000",
    "워록": "1 in 660,000",
    "바운디드": "1 in 200,000",
    "재즈": "1 in 160,000",
    "스펙터": "1 in 140,000",
    "만년서리": "1 in 73,500 (눈올 때 확률 3배)",
    "태양": "1 in 50,000 (낮 버프 시 1 in 5,000)",
    "달": "1 in 50,000 (밤 버프 시 1 in 5,000)",
    "와트": "1 in 32,768",
    "힘": "1 in 16,384",
    "빙하": "1 in 2,304 (눈올 때 확률 3배)",
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
    "𝓘𝓬𝓮𝓐𝓰𝓮",
    "𝓜𝓪𝓶𝓶𝓸𝓽𝓱",
    "𝓓𝓻𝓮𝓪𝓶𝓬𝓪𝓽𝓬𝓱𝓮𝓻",
    "𝓢𝓹𝓮𝓬𝓽𝓻𝓪𝓕𝓵𝓸𝔀 𖤐",
    "감시자",
    "크로마틱",
    "자장가",
    "블리자드",
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
    "𝓘𝓬𝓮𝓐𝓰𝓮": "❄️🧊👑",
    "𝓜𝓪𝓶𝓶𝓸𝓽𝓱": "🦣❄️🧊",
    "𝓓𝓻𝓮𝓪𝓶𝓬𝓪𝓽𝓬𝓱𝓮𝓻": "🕸️🌙✨🦋",
    "𝓢𝓹𝓮𝓬𝓽𝓻𝓪𝓕𝓵𝓸𝔀 𖤐": "🌌💠💫",
    "감시자": "👁️‍🗨️⚡",
    "크로마틱": "🌈💫",
    "자장가": "🌌🎵💤",
    "블리자드": "❄️🌨️🌀",
    "헬리오스": "☀️🔥",
    "황혼": "🌆✨💜",
    "대마법사": "🧙‍♂️✨",
    "아케인": "🔮👑",
    "워록": "💀🔥",
    "바운디드": "🌌👑",
    "재즈": "🎶🎷",
    "스펙터": "👻🔮",
    "만년서리": "❄️💎",
    "태양": "☀️✨",
    "달": "🌙✨",
    "와트": "⚡👑⚡",
    "힘": "⚡🔥",
    "빙하": "🧊❄️",
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
    "빙하": "images/SmartSelect_20261114_102325_NAVER.jpg",
    "힘": "images/SmartSelect_20261113_124048_Chrome.jpg",
    "만년서리": "images/SmartSelect_20261114_102346_NAVER.jpg",
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
    "블리자드": "images/SmartSelect_20261114_102513_NAVER.jpg",
    "𝓢𝓹𝓮𝓬𝓽𝓻𝓪𝓕𝓵𝓸𝔀 𖤐": "images/SmartSelect_20261113_234508_Chrome.jpg",
    "태양": "images/SmartSelect_20261113_235302_Chrome.jpg",
    "달": "images/SmartSelect_20261113_235408_Chrome.jpg",
    "황혼": "images/SmartSelect_20261113_235637_Chrome.jpg",
    "자장가": "images/SmartSelect_20261113_235654_Chrome.jpg",
    "𝓓𝓻𝓮𝓪𝓶𝓬𝓪𝓽𝓬𝓱𝓮𝓻": "images/SmartSelect_20261113_235729_Chrome.jpg",
    "𝓜𝓪𝓶𝓶𝓸𝓽𝓱": "images/file_00000000485082099074341e8735beff.png",
    "𝓘𝓬𝓮𝓐𝓰𝓮": "images/file_000000009c888209b0b962261732b998.png",
}

# 특수 장착 배경 이미지 매핑
equipped_backgrounds = {
    "𝓘𝓬𝓮𝓐𝓰𝓮": "Background/SmartSelect_20261114_105008_NAVER.jpg",
    "𝓜𝓪𝓶𝓶𝓸𝓽𝓱": "Background/SmartSelect_20261114_104343_NAVER.jpg",
    "블리자드": "Background/SmartSelect_20261114_104034_NAVER.jpg",
    "𝓓𝓻𝓮𝓪𝓶𝓬𝓪𝓽𝓬𝓱𝓮𝓻": "Background/SmartSelect_20261114_000447_Chrome.jpg",
    "𝓢𝓹𝓮𝓬𝓽𝓻𝓪𝓕𝓵𝓸𝔀 𖤐": "Background/SmartSelect_20261113_234652_NAVER.jpg",
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


def get_current_save_dict():
  return {
      "counts": st.session_state.get("counts", {}),
      "levels": st.session_state.get("levels", {}),
      "titles": st.session_state.get("titles", []),
      "equipped_title": st.session_state.get("equipped_title", None),
      "equipped": st.session_state.get("equipped", None),
      "coins": st.session_state.get("coins", 0),
      "inventory_slots": st.session_state.get("inventory_slots", 50),
      "luck_buff_unlocked": st.session_state.get("luck_buff_unlocked", False),
      "triple_roll_unlocked": st.session_state.get(
          "triple_roll_unlocked", False
      ),
      "five_roll_unlocked": st.session_state.get("five_roll_unlocked", False),
      "potions": st.session_state.get("potions", {}),
  }


def save_user_data_to_db():
  if not st.session_state.get("logged_in", False):
    return
  username = st.session_state.username
  save_data = get_current_save_dict()
  conn = sqlite3.connect("users.db", check_same_thread=False)
  cursor = conn.cursor()
  cursor.execute(
      "UPDATE users SET data = ? WHERE username = ?",
      (json.dumps(save_data, ensure_ascii=False), username),
  )
  conn.commit()
  conn.close()


def apply_loaded_data_to_session(saved_data):
  st.session_state.counts = {
      item: saved_data.get("counts", {}).get(item, 0) for item in items
  }
  st.session_state.levels = {
      item: saved_data.get("levels", {}).get(item, 1) for item in items
  }
  st.session_state.titles = saved_data.get("titles", [])
  st.session_state.equipped_title = saved_data.get("equipped_title", None)
  st.session_state.equipped = saved_data.get("equipped", None)
  st.session_state.coins = saved_data.get("coins", 0)
  st.session_state.inventory_slots = saved_data.get("inventory_slots", 50)
  st.session_state.luck_buff_unlocked = saved_data.get(
      "luck_buff_unlocked", False
  )
  st.session_state.triple_roll_unlocked = saved_data.get(
      "triple_roll_unlocked", False
  )
  st.session_state.five_roll_unlocked = saved_data.get(
      "five_roll_unlocked", False
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
          apply_loaded_data_to_session(saved_data)

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
              "counts": {item: 0 for item in items},
              "levels": {item: 1 for item in items},
              "titles": [],
              "equipped_title": None,
              "equipped": None,
              "coins": 0,
              "inventory_slots": 50,
              "luck_buff_unlocked": False,
              "triple_roll_unlocked": False,
              "five_roll_unlocked": False,
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
# ☀️🌙 [낮/밤 시스템: 3분(180초) 주기]
# ==========================================
def get_world_time_status():
  current_time = int(time.time())
  cycle_time = current_time % 360
  is_day = cycle_time < 180
  rem_sec = 180 - (cycle_time % 180)
  return is_day, rem_sec


# ==========================================
# ❄️ [계절 및 날씨 시스템: 1분(60초) 독립 주기, 30% 눈 확률 (맘모스 장착 시 +10%)]
# ==========================================
def get_world_weather_status():
  current_time = int(time.time())
  cycle_time = current_time % 60
  rem_sec = 60 - cycle_time

  minute_seed = current_time // 60
  random.seed(minute_seed)

  snow_chance = 0.30
  if st.session_state.get("equipped") == "𝓜𝓪𝓶𝓶𝓸𝓽𝓱":
    snow_chance = 0.40

  is_snow = random.random() < snow_chance
  random.seed()

  return is_snow, rem_sec, int(snow_chance * 100)


# 🎨 [특수 아우라 장착 배경 및 가독성 향상 CSS 적용 함수]
def apply_equipped_background():
  eq = st.session_state.get("equipped")
  bg_path = equipped_backgrounds.get(eq)

  base_style = """
    <style>
    [data-testid="stMetricValue"], [data-testid="stMetricLabel"] {
        color: #ffffff !important;
        text-shadow: 0 0 4px rgba(0,0,0,0.9), 0 0 10px rgba(0,0,0,0.8);
    }
    .stTabs [data-baseweb="tab"] {
        color: #ffffff !important;
        font-weight: bold;
        text-shadow: 0 0 4px rgba(0,0,0,0.9);
    }
    .stTabs [data-baseweb="tab"] p {
        color: #ffffff !important;
    }
    </style>
    """

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
        {base_style}
        """,
        unsafe_allow_html=True,
    )
  else:
    st.markdown(base_style, unsafe_allow_html=True)


apply_equipped_background()


# 🎖️ [칭호 희귀도별 화려하고 예쁜 스타일 적용 HTML 생성 함수]
def get_styled_title_html(title_name):
  if not title_name:
    return ""

  if "GOD OF ICE" in title_name or "ANCIENT KING" in title_name or "𝓑𝓵𝓲𝔃𝔃𝓪𝓻𝓭" in title_name:
    style = (
        "background: linear-gradient(90deg, #00ffff, #00bfff, #ffffff, #1e90ff);"
        " -webkit-background-clip: text; -webkit-text-fill-color: transparent;"
        " font-weight: 900; text-shadow: 0 0 12px rgba(0,255,255,0.7),"
        " 0 0 20px rgba(0,191,255,0.6); font-size: 1.05em; padding: 0 4px;"
    )
  elif "ICE MONARCH" in title_name or "FROST EMPEROR" in title_name:
    style = (
        "background: linear-gradient(90deg, #e0ffff, #00bfff);"
        " -webkit-background-clip: text; -webkit-text-fill-color: transparent;"
        " font-weight: 800; text-shadow: 0 0 10px rgba(0,191,255,0.7);"
        " font-size: 1.05em; padding: 0 4px;"
    )
  elif "초월자" in title_name or "몽상가" in title_name or "환상" in title_name or "𝓟𝓻𝓲𝓼𝓶" in title_name:
    style = (
        "background: linear-gradient(90deg, #ff007f, #7928ca, #0070f3, #00dfd8);"
        " -webkit-background-clip: text; -webkit-text-fill-color: transparent;"
        " font-weight: 900; text-shadow: 0 0 10px rgba(255,0,127,0.6),"
        " 0 0 20px rgba(0,223,216,0.5); font-size: 1.05em; padding: 0 4px;"
    )
  elif "𝓦𝓪𝓽𝓬𝓱𝓮𝓻" in title_name or "𝓛𝓾𝓵𝓵𝓪𝓫𝔂" in title_name or "𝓣𝔀𝓲𝓵𝓲𝓰𝓱𝓽" in title_name:
    style = (
        "background: linear-gradient(90deg, #b366ff, #ff3399, #66ccff);"
        " -webkit-background-clip: text; -webkit-text-fill-color: transparent;"
        " font-weight: 800; text-shadow: 0 0 12px rgba(179,102,255,0.7);"
        " font-size: 1.05em; padding: 0 4px;"
    )
  elif "𝓗𝓮𝓵𝓲𝓸𝓼" in title_name or "𝓐𝓻𝓬𝓪𝓷𝓮" in title_name or "𝓐𝓻𝓬𝓱𝓶𝓪𝓰𝓮" in title_name:
    style = (
        "background: linear-gradient(90deg, #ffd700, #ff6600, #ff0055);"
        " -webkit-background-clip: text; -webkit-text-fill-color: transparent;"
        " font-weight: 800; text-shadow: 0 0 12px rgba(255,153,0,0.7);"
        " font-size: 1.05em; padding: 0 4px;"
    )
  elif "잔광" in title_name:
    style = (
        "background: linear-gradient(90deg, #00ffff, #0077ff);"
        " -webkit-background-clip: text; -webkit-text-fill-color: transparent;"
        " font-weight: 800; text-shadow: 0 0 12px rgba(0,255,255,0.7);"
        " font-size: 1.05em; padding: 0 4px;"
    )
  elif "달인" in title_name:
    style = (
        "background: linear-gradient(90deg, #ffe600, #ff8c00);"
        " -webkit-background-clip: text; -webkit-text-fill-color: transparent;"
        " font-weight: 800; text-shadow: 0 0 10px rgba(255,215,0,0.7);"
        " font-size: 1.05em; padding: 0 4px;"
    )
  else:
    style = (
        "color: #ffeb3b; font-weight: bold; text-shadow: 0 0 6px rgba(0,0,0,0.9),"
        " 0 0 12px rgba(255,235,59,0.5); font-size: 1.02em; padding: 0 4px;"
    )

  return f'<span style="{style}">🎖️ [{title_name}]</span>'


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

  is_snow, _, _ = get_world_weather_status()
  if is_snow and st.session_state.get("equipped") == "𝓘𝓬𝓮𝓐𝓰𝓮":
    mult *= 10

  is_day, _ = get_world_time_status()
  if not is_day and st.session_state.get("equipped") == "𝓓𝓻𝓮𝓪𝓶𝓬𝓪𝓽𝓬𝓱𝓮𝓻":
    mult *= 10

  return mult


# ✨ [확률별 맞춤형 화려한 풀스크린 컷씬 (최초 1회만 재생)]
def play_fullscreen_star_cutscene(aura_name):
  placeholder = st.empty()

  if aura_name == "𝓘𝓬𝓮𝓐𝓰𝓮":
    star_color = "#00ffff"
    bg_style = "radial-gradient(circle, #001a33 0%, #00050f 90%)"
    star_symbol = "❄️🧊👑"
    ment = "❄️ [ICE AGE] 빙하기의 절대적인 한기가 온 세상을 영원의 빙하로 뒤덮습니다!"
    duration = 4.5
  elif aura_name == "𝓜𝓪𝓶𝓶𝓸𝓽𝓱":
    star_color = "#add8e6"
    bg_style = "radial-gradient(circle, #102030 0%, #050a10 90%)"
    star_symbol = "🦣❄️"
    ment = (
        "🦣 [MAMMOTH] 고대 빙하의 수호자 맘모스가 거대한 눈보라와 함께 포효합니다!"
    )
    duration = 4.0
  elif aura_name == "블리자드":
    star_color = "#87ceeb"
    bg_style = "radial-gradient(circle, #002244 0%, #050a15 90%)"
    star_symbol = "❄️🌨️"
    ment = "🌨️ [BLIZZARD] 모든 것을 얼어붙게 만드는 거대한 눈폭풍이 몰아칩니다!"
    duration = 3.5
  elif aura_name == "𝓓𝓻𝓮𝓪𝓶𝓬𝓪𝓽𝓬𝓱𝓮𝓻":
    star_color = "#e066ff"
    bg_style = "radial-gradient(circle, #2e004d 0%, #05000a 90%)"
    star_symbol = "🕸️🌙✨🦋"
    ment = (
        "🕸️ [DREAMCATCHER] 현실과 환상의 경계가 허물어지며 영원한 꿈의"
        " 수호자가 강림합니다!"
    )
    duration = 4.2
  elif aura_name == "𝓢𝓹𝓮𝓬𝓽𝓻𝓪𝓕𝓵𝓸𝔀 𖤐":
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
  else:
    star_color = "#ffd700"
    bg_style = "rgba(5, 5, 10, 0.95)"
    star_symbol = "✦"
    ment = "전설적인 에너지가 요동칩니다..."
    duration = 2.5

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


# 아우라 레벨업 요구치 계산 함수 (분모 기준)
def get_level_requirements(denom):
  if denom > 100000000:  # 1억 초과
    return {1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 10, 7: 100}
  elif denom >= 1000000:  # 100만 이상 ~ 1억 이하
    return {1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 10, 7: 100}
  elif denom > 100000:  # 10만 초과 ~ 100만 미만
    return {1: 1, 2: 30, 3: 50, 4: 100, 5: 500, 6: 1000, 7: 1500}
  else:  # 10만 이하
    return {1: 1, 2: 10, 3: 20, 4: 30, 5: 50, 6: 100, 7: 300}


def get_max_requirement(denom):
  return get_level_requirements(denom)[7]


# 1회 또는 다회 뽑기 실행 공통 함수
def perform_rolls(roll_count=1):
  results = []
  max_luck_applied = 1
  coin_gain_per_roll = (
      10 if st.session_state.get("equipped") == "𝓢𝓹𝓮𝓬𝓽𝓻𝓪𝓕𝓵𝓸𝔀 𖤐" else 5
  )
  is_snow, _, _ = get_world_weather_status()
  is_day, _ = get_world_time_status()

  prior_counts = {item: st.session_state.counts.get(item, 0) for item in items}

  for _ in range(roll_count):
    next_pull = sum(st.session_state.counts.values()) + 1
    luck_mult = get_current_luck_multiplier(next_pull)
    max_luck_applied = max(max_luck_applied, luck_mult)

    if st.session_state.million_ticket_active:
      st.session_state.million_ticket_active = False

    current_weights = list(base_weights)

    # 낮/밤 버프 적용
    if is_day:
      current_weights[items.index("태양")] *= 10
    else:
      current_weights[items.index("달")] *= 10
      current_weights[items.index("황혼")] *= 10
      current_weights[items.index("자장가")] *= 10
      current_weights[items.index("𝓓𝓻𝓮𝓪𝓶𝓬𝓪𝓽𝓬𝓱𝓮𝓻")] *= 2

    # 눈 날씨 버프 적용 (빙하·만년서리·블리자드 3배 / 맘모스·아이스에이지 2배)
    if is_snow:
      current_weights[items.index("빙하")] *= 3
      current_weights[items.index("만년서리")] *= 3
      current_weights[items.index("블리자드")] *= 3
      current_weights[items.index("𝓜𝓪𝓶𝓶𝓸𝓽𝓱")] *= 2
      current_weights[items.index("𝓘𝓬𝓮𝓐𝓰𝓮")] *= 2

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

    # 최초 획득 칭호 지급
    if (
        prior_counts.get(result, 0) == 0
        and st.session_state.counts.get(result, 0) == 0
    ):
      if result == "𝓢𝓹𝓮𝓬𝓽𝓻𝓪𝓕𝓵𝓸𝔀 𖤐":
        t_name = "영광의 잔광"
        if t_name not in st.session_state.titles:
          st.session_state.titles.append(t_name)
      elif result == "𝓓𝓻𝓮𝓪𝓶𝓬𝓪𝓽𝓬𝓱𝓮𝓻":
        t_name = "• ⋆༺무한의 환상༻⋆"
        if t_name not in st.session_state.titles:
          st.session_state.titles.append(t_name)
      elif result == "𝓜𝓪𝓶𝓶𝓸𝓽𝓱":
        t_name = "❄ 𝐈𝐂𝐄 𝐌𝐎𝐍𝐀𝐑𝐂𝐇 ❄"
        if t_name not in st.session_state.titles:
          st.session_state.titles.append(t_name)
      elif result == "𝓘𝓬𝓮𝓐𝓰𝓮":
        t_name = "♛ 𝐅𝐑𝐎𝐒𝐓 𝐄𝐌𝐏𝐄𝐑𝐎𝐑 ♛"
        if t_name not in st.session_state.titles:
          st.session_state.titles.append(t_name)

    # MAX 레벨이 아닐 때만 수량 증가 (MAX 달성 후 추가 안 됨)
    curr_lvl = st.session_state.levels.get(result, 1)
    if curr_lvl < 7:
      st.session_state.counts[result] += 1

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
  eq_title = st.session_state.get("equipped_title")
  styled_title_html = (
      f" &nbsp; {get_styled_title_html(eq_title)}" if eq_title else ""
  )
  st.markdown(
      f"👤 현재 접속 계정: **`{st.session_state.username}`**님{styled_title_html}"
      " (자동 영구 저장 활성화됨)",
      unsafe_allow_html=True,
  )
with c_u2:
  if st.button("로그아웃", use_container_width=True):
    save_user_data_to_db()
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.rerun()

# 낮/밤 및 날씨 상태바 표시
is_day_now, time_rem_sec = get_world_time_status()
t_min = time_rem_sec // 60
t_sec = time_rem_sec % 60

is_snow_now, weather_rem_sec, current_snow_pct = get_world_weather_status()
w_sec = weather_rem_sec

is_mammoth_equipped = st.session_state.get("equipped") == "𝓜𝓪𝓶𝓶𝓸𝓽𝓱"
is_ia_equipped = st.session_state.get("equipped") == "𝓘𝓬𝓮𝓐𝓰𝓮"
is_dc_equipped = st.session_state.get("equipped") == "𝓓𝓻𝓮𝓪𝓶𝓬𝓪𝓽𝓬𝓱𝓮𝓻"

# 1. 낮/밤 상태 표시 배너
if is_day_now:
  st.markdown(
      f"""
        <div style="background: linear-gradient(90deg, #ff9900, #ffcc00); padding: 10px; border-radius: 8px; text-align: center; color: black; font-weight: bold; font-size: 16px; margin-bottom: 8px; box-shadow: 0 0 10px rgba(255,204,0,0.4);">
            🌞 [현재 낮 시간대] 태양(☀️) 확률 10배 폭증 중! (남은 시간: {t_min}분 {t_sec}초 후 밤으로 전환)
        </div>
        """,
      unsafe_allow_html=True,
  )
else:
  dc_text = " | 🕸️ 𝓓𝓻𝓮𝓪𝓶𝓬𝓪𝓽𝓬𝓱𝓮𝓻 장착 중: 밤 행운 10배!" if is_dc_equipped else ""
  st.markdown(
      f"""
        <div style="background: linear-gradient(90deg, #003366, #2b1a66); padding: 10px; border-radius: 8px; text-align: center; color: white; font-weight: bold; font-size: 16px; margin-bottom: 8px; box-shadow: 0 0 10px rgba(153,102,255,0.4);">
            🌙 [현재 밤 시간대] 달·황혼·자장가 10배 / 𝓓𝓻𝓮𝓪𝓶𝓬𝓪𝓽𝓬𝓱𝓮𝓻 2배! (남은 시간: {t_min}분 {t_sec}초 후 낮으로 전환){dc_text}
        </div>
        """,
      unsafe_allow_html=True,
  )

# 2. 날씨(눈/정상) 상태 표시 배너
if is_snow_now:
  ia_text = " | ❄️ 𝓘𝓬𝓮𝓐𝓰𝓮 장착 중: 행운 10배!" if is_ia_equipped else ""
  st.markdown(
      f"""
        <div style="background: linear-gradient(90deg, #004080, #0080ff); padding: 10px; border-radius: 8px; text-align: center; color: white; font-weight: bold; font-size: 16px; margin-bottom: 15px; box-shadow: 0 0 10px rgba(0,191,255,0.4);">
            🌨️ [현재 날씨: 눈 내리는 중] 눈 확률 {current_snow_pct}% (빙하·만년서리·블리자드 3배 / 맘모스·아이스에이지 2배) (남은 시간: {w_sec}초){ia_text}
        </div>
        """,
      unsafe_allow_html=True,
  )
else:
  m_text = " | 🦣 𝓜𝓪𝓶𝓶𝓸𝓽𝓱 장착 중: 눈 확률 +10%!" if is_mammoth_equipped else ""
  st.markdown(
      f"""
        <div style="background: linear-gradient(90deg, #333333, #555555); padding: 10px; border-radius: 8px; text-align: center; color: white; font-weight: bold; font-size: 16px; margin-bottom: 15px; box-shadow: 0 0 10px rgba(100,100,100,0.4);">
            ⛅ [현재 날씨: 정상 (맑음)] 눈 내릴 확률 {current_snow_pct}% (남은 시간: {w_sec}초){m_text}
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
      if equipped_aura == "𝓜𝓪𝓶𝓶𝓸𝓽𝓱":
        st.caption("🦣 **[능력 활성화]** 눈이 내릴 확률이 10% 증가합니다!")
      elif equipped_aura == "𝓘𝓬𝓮𝓐𝓰𝓮":
        st.caption("❄️ **[능력 활성화]** 눈이 올 때 행운 10배가 적용됩니다!")
      elif equipped_aura == "𝓓𝓻𝓮𝓪𝓶𝓬𝓪𝓽𝓬𝓱𝓮𝓻":
        st.caption("🕸️ **[능력 활성화]** 밤 시간대 행운 10배 버프 적용 중!")
      elif equipped_aura == "𝓢𝓹𝓮𝓬𝓽𝓻𝓪𝓕𝓵𝓸𝔀 𖤐":
        st.caption(
            "💠 **[특수 능력]** 코인 획득량 2배 (뽑기당 10 G) & 전용 배경"
            " 적용 중!"
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

tab_gacha, tab_inventory, tab_potions, tab_codex, tab_titles, tab_shop = st.tabs(
    ["🎲 아우라 뽑기", "🎒 스토리지", "🧪 포션 인벤토리", "📖 도감 (Codex)", "🎖️ 칭호 칸", "🛒 상점"]
)

with tab_gacha:
  roll_coin_label = (
      "1회당 +10 G (𝓢𝓹𝓮𝓬𝓽𝓻𝓪𝓕𝓵𝓸𝔀 𖤐 효과)"
      if st.session_state.get("equipped") == "𝓢𝓹𝓮𝓬𝓽𝓻𝓪𝓕𝓵𝓸𝔀 𖤐"
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
    total_w = sum(base_weights)
    for item, w in zip(items, base_weights):
      prob = (w / total_w) * 100
      if prob < 0.000001:
        prob_str = f"{prob:.10f}%"
      elif prob < 0.01:
        prob_str = f"{prob:.8f}%"
      else:
        prob_str = f"{prob:.4f}%"
      st.markdown(
          f"- **{icons.get(item, '✨')} {item}** : `{prob_str}`"
          f" ({fractions.get(item, 'N/A')})"
      )

  st.write("")

  has_triple = st.session_state.get("triple_roll_unlocked", False)
  has_five = st.session_state.get("five_roll_unlocked", False)

  if has_five:
    col_b1, col_b2 = st.columns(2)
    with col_b1:
      if st.button("🎲 1회 무료 뽑기", type="secondary", use_container_width=True):
        perform_rolls(1)
        st.rerun()
    with col_b2:
      five_bonus_coins = (
          50 if st.session_state.get("equipped") == "𝓢𝓹𝓮𝓬𝓽𝓻𝓪𝓕𝓵𝓸𝔀 𖤐" else 25
      )
      if st.button(
          f"⚡ 5회 연속 뽑기 (+{five_bonus_coins} G)",
          type="primary",
          use_container_width=True,
      ):
        perform_rolls(5)
        st.rerun()
  elif has_triple:
    col_b1, col_b2 = st.columns(2)
    with col_b1:
      if st.button("🎲 1회 무료 뽑기", type="secondary", use_container_width=True):
        perform_rolls(1)
        st.rerun()
    with col_b2:
      triple_bonus_coins = (
          30 if st.session_state.get("equipped") == "𝓢𝓹𝓮𝓬𝓽𝓻𝓪𝓕𝓵𝓸𝔀 𖤐" else 15
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
        10 if st.session_state.get("equipped") == "𝓢𝓹𝓮𝓬𝓽𝓻𝓪𝓕𝓵𝓸𝔀 𖤐" else 5
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

with tab_inventory:
  owned_items = [
      item
      for item in items
      if st.session_state.counts.get(item, 0) > 0
      or st.session_state.levels.get(item, 1) > 1
  ]
  st.subheader(
      f"📦 아우라 스토리지 & 레벨업 [보유 종류: {len(owned_items)} / {len(items)}]"
  )

  if owned_items:
    st.write(
        "획득한 아우라를 확인하고 레벨업 및 장착을 진행할 수 있습니다. (Max"
        " 달성 시 추가 수량이 쌓이지 않습니다)"
    )

    if "levels" not in st.session_state:
      st.session_state.levels = {item: 1 for item in items}

    for item in owned_items:
      count = st.session_state.counts.get(item, 0)
      lvl = st.session_state.levels.get(item, 1)
      denom = denominators.get(item, 2)
      reqs = get_level_requirements(denom)
      max_req = reqs[7]

      with st.container(border=True):
        col_i1, col_i2, col_i3 = st.columns([1, 2, 1])
        with col_i1:
          icon = icons.get(item, "✨")
          st.markdown(
              f"<div style='font-size: 36px; text-align: center;'>{icon}</div>",
              unsafe_allow_html=True,
          )
        with col_i2:
          st.markdown(f"#### [{item}] — Lv. {lvl} / 6 (Max)")
          if lvl < 7:
            next_req = reqs[lvl + 1] if lvl + 1 <= 7 else max_req
            st.write(
                f"현재 보유: **{count}개** / 다음 레벨업 필요: **{next_req}개**"
            )
          else:
            st.markdown(
                "⭐ <span style='color: #ffd700; font-weight: bold;'>MAX"
                " LEVEL 달성 완료!</span>",
                unsafe_allow_html=True,
            )
        with col_i3:
          is_equipped = st.session_state.get("equipped") == item
          if is_equipped:
            st.button(
                "장착중", key=f"inv_eq_btn_{item}", disabled=True, use_container_width=True
            )
          else:
            if st.button(
                "장착", key=f"inv_use_btn_{item}", use_container_width=True
            ):
              st.session_state.equipped = item
              save_user_data_to_db()
              st.rerun()

          if lvl < 7:
            next_req = reqs[lvl + 1]
            if count >= next_req:
              if st.button(
                  "레벨업!", key=f"lvl_up_{item}", use_container_width=True, type="primary"
              ):
                st.session_state.counts[item] -= next_req
                st.session_state.levels[item] += 1
                new_lvl = st.session_state.levels[item]

                if new_lvl == 7:
                  custom_max_titles = {
                      "𝓢𝓹𝓮𝓬𝓽𝓻𝓪𝓕𝓵𝓸𝔀 𖤐": "𓆩 𝓟𝓻𝓲𝓼𝓶 𓆪",
                      "감시자": "𓆩 𝓦𝓪𝓽𝓬𝓱𝓮𝓻 𓆪",
                      "자장가": "𓆩 𝓛𝓾𝓵𝓵𝓪𝓫𝔂 𓆪",
                      "블리자드": "𓆩 𝓑𝓵𝓲𝔃𝔃𝓪𝓻𝓭 𓆪",
                      "헬리오스": "◇𝓗𝓮𝓵𝓲𝓸𝓼 ◇",
                      "아케인": "◇ 𝓐𝓻𝓬𝓪𝓷𝓮 ◇",
                      "대마법사": "◇ 𝓐𝓻𝓬𝓱𝓶𝓪𝓰𝓮 ◇",
                      "황혼": "◇𝓣𝔀𝓲𝓵𝓲𝓰𝓱𝓽 ◇",
                      "𝓓𝓻𝓮𝓪𝓶𝓬𝓪𝓽𝓬𝓱𝓮𝓻": "• ⋆༺무한의 환상༻⋆",
                      "𝓜𝓪𝓶𝓶𝓸𝓽𝓱": "꧁༺ 𝐀𝐍𝐂𝐈𝐄𝐍𝐓 𝙆𝐈𝐍𝙶 ༻꧂",
                      "𝓘𝓬𝓮𝓐𝓰𝓮": "꧁༺ 𝐆𝐎𝐃 𝐎𝐅 𝐈𝗖𝐄 ༻꧂",
                  }
                  t_name = custom_max_titles.get(item, f"{item}의 달인")

                  if "titles" not in st.session_state:
                    st.session_state.titles = []
                  if t_name not in st.session_state.titles:
                    st.session_state.titles.append(t_name)
                    st.success(f"🎉 만렙 달성! 새 칭호 [{t_name}] 획득!")

                save_user_data_to_db()
                st.rerun()
          else:
            st.button(
                "MAX", key=f"max_btn_{item}", disabled=True, use_container_width=True
            )
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
  st.write(
      "상점에서 구매한 행운 포션과 백만배 행운권을 원하는 수량만큼 선택해서"
      " 사용할 수 있습니다. (사용 수량만큼 시간이 누적됩니다)"
  )

  all_potions_count = sum(st.session_state.potions.values())
  if all_potions_count > 0:
    for p_name in potion_items:
      count = st.session_state.potions.get(p_name, 0)
      if count > 0:
        with st.container(border=True):
          col_p1, col_p2, col_p3 = st.columns([1, 2, 1])
          with col_p1:
            st.markdown(
                f"<div style='font-size: 38px; text-align: center;'>🧪</div>",
                unsafe_allow_html=True,
            )
          with col_p2:
            st.markdown(f"#### {p_name}")
            st.write(f"보유 수량: **{count}개**")
            if count == 1:
              st.caption("사용할 수량: 1개")
              use_qty = 1
            else:
              use_qty = st.slider(
                  "사용할 수량",
                  min_value=1,
                  max_value=count,
                  value=1,
                  key=f"slider_qty_{p_name}",
              )
          with col_p3:
            st.write("")
            st.write("")
            if st.button(
                f"선택 사용 ({use_qty}개)",
                key=f"btn_use_qty_{p_name}",
                type="primary",
                use_container_width=True,
            ):
              st.session_state.potions[p_name] -= use_qty
              cfg = potion_config[p_name]

              if cfg["type"] == "potion":
                now = time.time()
                add_duration = cfg["duration"] * use_qty
                if (
                    st.session_state.active_potion_name == p_name
                    and now < st.session_state.active_potion_end
                ):
                  st.session_state.active_potion_end += add_duration
                else:
                  base_time = (
                      max(now, st.session_state.active_potion_end)
                      if st.session_state.active_potion_mult > 1
                      else now
                  )
                  st.session_state.active_potion_end = base_time + add_duration
                  st.session_state.active_potion_mult = cfg["mult"]
                  st.session_state.active_potion_name = p_name
              elif cfg["type"] == "ticket":
                if "million_ticket_count" not in st.session_state:
                  st.session_state.million_ticket_count = 0
                st.session_state.million_ticket_count += use_qty
                st.session_state.million_ticket_active = True

              save_user_data_to_db()
              st.success(
                  f"🎉 [{p_name}] {use_qty}개가 성공적으로 사용되었습니다!"
              )
              time.sleep(0.8)
              st.rerun()
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
      is_owned = (
          st.session_state.counts.get(item, 0) > 0
          or st.session_state.levels.get(item, 1) > 1
      )
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
    is_owned = (
        st.session_state.counts.get(sel, 0) > 0
        or st.session_state.levels.get(sel, 1) > 1
    )
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
        st.write(f"**현재 레벨:** Lv. {st.session_state.levels.get(sel, 1)} / 6")
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

with tab_titles:
  st.subheader("🎖️ 칭호 도감 칸 (Titles Codex)")
  st.write(
      "획득한 칭호를 장착하거나 해제할 수 있습니다. (칭호는 1개만 장착"
      " 가능합니다)"
  )

  if "titles" not in st.session_state:
    st.session_state.titles = []
  if "equipped_title" not in st.session_state:
    st.session_state.equipped_title = None

  user_titles = st.session_state.titles
  if user_titles:
    st.markdown(f"#### 🏅 보유 중인 칭호 목록 ({len(user_titles)}개 획득)")
    for t in user_titles:
      is_t_equipped = st.session_state.get("equipped_title") == t
      with st.container(border=True):
        col_t1, col_t2 = st.columns([3, 1])
        with col_t1:
          badge_text = " ⭐ [장착중]" if is_t_equipped else ""
          styled_t_html = get_styled_title_html(t)
          st.markdown(
              f"{styled_t_html}{badge_text}", unsafe_allow_html=True
          )
        with col_t2:
          if is_t_equipped:
            if st.button(
                "장착 해제", key=f"unequip_title_{t}", use_container_width=True
            ):
              st.session_state.equipped_title = None
              save_user_data_to_db()
              st.rerun()
          else:
            if st.button(
                "장착하기",
                key=f"equip_title_{t}",
                use_container_width=True,
                type="primary",
            ):
              st.session_state.equipped_title = t
              save_user_data_to_db()
              st.rerun()
  else:
    st.markdown(
        """
        <div style="text-align: center; padding: 50px; color: #777;">
            <h3>🎖️ 아직 획득한 칭호가 없습니다!</h3>
            <p>아우라를 뽑거나 레벨업(MAX)을 달성하여 칭호를 수집해보세요.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with tab_shop:
  st.subheader("🛒 상점 & 데이터 관리")

  with st.container(border=True):
    col_box1, col_box2 = st.columns([2, 1])
    with col_box1:
      st.markdown("### 🎁 행운권 상자 (원하는 수량 구매)")
      st.write(
          "초고배율 행운 포션이나 백만배 행운권을 획득할 수 있는 미스터리"
          " 상자입니다. (개당 300 G)"
      )
      with st.expander("📋 상자 구성품 확률 보기"):
        st.markdown("- **90%**: 100배 행운 포션 (1분) — 최소 1/128 이상 보장")
        st.markdown("- **7%**: 500배 행운 포션 (30초) — 최소 1/2,048 이상 보장")
        st.markdown("- **2%**: 1000배 행운 포션 (15초) — 최소 1/2,048 이상 보장")
        st.markdown("- **0.9%**: 10000배 행운 포션 (10초) — 최소 1/16,384 이상 보장")
        st.markdown("- **0.1%**: 백만배 행운권 (1회) — 최소 1/1,000,000 (아케인 이상) 확정!")

      affordable_boxes = st.session_state.coins // 300
      if affordable_boxes < 1:
        st.warning("코인이 부족합니다! (상자 1개당 300 G 필요)")
        buy_box_qty = 1
      elif affordable_boxes == 1:
        st.caption("구매 가능한 수량: 1개")
        buy_box_qty = 1
      else:
        buy_box_qty = st.slider(
            "구매할 상자 수량",
            min_value=1,
            max_value=affordable_boxes,
            value=1,
            key="slider_buy_boxes",
        )
      total_box_price = buy_box_qty * 300
      st.write(f"총 필요 코인: **{total_box_price:,} G**")

    with col_box2:
      st.write("")
      st.write("")
      can_buy = affordable_boxes >= 1
      if st.button(
          f"상자 {buy_box_qty}개 구매 & 개봉",
          type="primary",
          key="buy_luck_box_qty",
          use_container_width=True,
          disabled=not can_buy,
      ):
        if st.session_state.coins >= total_box_price:
          st.session_state.coins -= total_box_price
          won_summary = {}
          for _ in range(buy_box_qty):
            won_item = random.choices(
                potion_items, weights=potion_weights, k=1
            )[0]
            st.session_state.potions[won_item] += 1
            won_summary[won_item] = won_summary.get(won_item, 0) + 1

          save_user_data_to_db()
          summary_str = ", ".join(
              [f"**{k}** {v}개" for k, v in won_summary.items()]
          )
          st.success(
              f"🎉 행운권 상자 {buy_box_qty}개 개봉 결과: {summary_str} 획득!"
          )
          st.balloons()
          time.sleep(1.2)
          st.rerun()
        else:
          st.error(f"코인이 부족합니다! ({total_box_price:,} G 필요)")

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
    col_f1, col_f2 = st.columns([2, 1])
    with col_f1:
      st.markdown("### ⚡ 5회씩 연속 뽑기 (영구)")
      st.write(
          "3회 연속 뽑기를 보유한 상태에서, 한 번에 5회씩 아우라를 소환할 수"
          " 있는 강력한 기능을 해금합니다."
      )
    with col_f2:
      st.write("")
      if st.session_state.five_roll_unlocked:
        st.button(
            "보유 완료",
            disabled=True,
            key="buy_five_done",
            use_container_width=True,
        )
      elif not st.session_state.triple_roll_unlocked:
        st.button(
            "3회 뽑기 선행 구매 필요",
            disabled=True,
            key="buy_five_locked",
            use_container_width=True,
        )
      else:
        if st.button(
            "구매 (1000 G)", key="buy_five_roll", use_container_width=True
        ):
          if st.session_state.coins >= 1000:
            st.session_state.coins -= 1000
            st.session_state.five_roll_unlocked = True
            save_user_data_to_db()
            st.success("5회 연속 뽑기 기능이 해금되었습니다!")
            st.rerun()
          else:
            st.error("코인이 부족합니다! (1000 G 필요)")

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

  # ==========================================
  # 💾 데이터 백업 및 파일 불러오기 (복구) 패널
  # ==========================================
  with st.container(border=True):
    st.markdown("### 💾 데이터 백업 및 파일 불러오기")
    st.write(
        "서버가 재시작되어도 데이터가 날아가지 않도록 현재 계정 상태를"
        " JSON 파일로 저장하거나, 백업 파일을 불러와 즉시 복구할 수 있습니다."
    )

    col_bk1, col_bk2 = st.columns(2)
    with col_bk1:
      current_json_str = json.dumps(
          get_current_save_dict(), ensure_ascii=False, indent=2
      )
      st.download_button(
          label="📥 내 데이터 백업 파일 저장 (.json)",
          data=current_json_str,
          file_name=f"{st.session_state.username}_backup.json",
          mime="application/json",
          use_container_width=True,
      )

    with col_bk2:
      uploaded_backup = st.file_uploader(
          "📤 백업 파일(.json) 선택",
          type=["json"],
          key="backup_file_uploader",
          label_visibility="collapsed",
      )
      if uploaded_backup is not None:
        if st.button(
            "🔄 선택한 백업 파일로 데이터 복구 실행",
            type="primary",
            use_container_width=True,
        ):
          try:
            loaded_json = json.load(uploaded_backup)
            apply_loaded_data_to_session(loaded_json)
            save_user_data_to_db()
            st.success("✅ 백업 파일에서 데이터 복구가 완료되었습니다!")
            time.sleep(0.8)
            st.rerun()
          except Exception as e:
            st.error(f"파일을 불러오는 중 오류가 발생했습니다: {e}")

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
    st.session_state.counts = {item: 0 for item in items}
    st.session_state.levels = {item: 1 for item in items}
    st.session_state.titles = []
    st.session_state.equipped_title = None
    st.session_state.equipped = None
    st.session_state.coins = 0
    st.session_state.inventory_slots = 50
    st.session_state.luck_buff_unlocked = False
    st.session_state.triple_roll_unlocked = False
    st.session_state.five_roll_unlocked = False
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
