import json
import os
import random
import time
import streamlit as st

# 페이지 설정
st.set_page_config(
    page_title="아우라 가챠 & 도감", page_icon="✨", layout="wide"
)

# 등급 리스트 정의 (희귀도 높은 순 - 신규 등급 포함)
items = [
    "아케인",
    "워록",
    "바운디드",
    "재즈",
    "스펙터",
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

# 각 분수 확률에 따른 가중치 설정 (기준: 1,000,000)
base_weights = [
    1,
    1,
    5,
    6,
    7,
    30,
    61,
    122,
    244,
    488,
    3906,
    7812,
    62500,
    125000,
    250000,
    500000,
]

# 각 아우라의 분수 표시 문자열
fractions = {
    "아케인": "1 in 1,000,000",
    "워록": "1 in 660,000",
    "바운디드": "1 in 200,000",
    "재즈": "1 in 160,000",
    "스펙터": "1 in 140,000",
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
    "아케인",
    "워록",
    "바운디드",
    "재즈",
    "스펙터",
    "와트",
    "힘",
    "석영",
    "시데리움",
]

# 등급별 이모티콘 매핑
icons = {
    "아케인": "🔮👑",
    "워록": "💀🔥",
    "바운디드": "🌌👑",
    "재즈": "🎶🎷",
    "스펙터": "👻🔮",
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
    "아케인": "#00ffff",
    "워록": "#ff3300",
    "바운디드": "#9900ff",
    "재즈": "#ff00aa",
    "스펙터": "#00ff88",
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
}


# ==========================================
# 🛡️ [업데이트 안전 호환] 세션 초기화 및 데이터 보정
# ==========================================
def init_session_state():
  defaults = {
      "history": [],
      "counts": {item: 0 for item in items},
      "equipped": None,
      "coins": 0,
      "inventory_slots": 50,
      "auto_roll_unlocked": False,
      "auto_roll_active": False,
      "luck_buff_unlocked": False,
      "last_result": None,
      "luck_active_flag": False,
      "is_cutscene": False,
      "selected_codex": items[0],
  }

  for key, val in defaults.items():
    if key not in st.session_state:
      st.session_state[key] = val

  # 신규 등급이 추가되어도 기존 데이터에 키가 없으면 0으로 자동 채움
  for item in items:
    if item not in st.session_state.counts:
      st.session_state.counts[item] = 0


init_session_state()


# ✨ [풀스크린 컷씬] 화면 전체에서 별이 회전하며 커지는 연출
def play_fullscreen_star_cutscene(aura_name):
  placeholder = st.empty()

  if aura_name == "아케인":
    star_color = "#00ffff"
    ment = (
        "태고의 신비로운 아케인 에너지가 온 차원을 뒤덮고 영원히 빛납니다..."
    )
  elif aura_name == "워록":
    star_color = "#ff3300"
    ment = "어둠의 파괴자가 깨어나며 전장을 지배할 저주가 쏟아집니다..."
  elif aura_name == "바운디드":
    star_color = "#bf00ff"
    ment = "시공간의 경계가 무너지고 영원한 심판이 시작됩니다..."
  elif aura_name == "재즈":
    star_color = "#ff007f"
    ment = "화려한 선율과 함께 온 우주를 매료시킬 리듬이 깨어납니다..."
  elif aura_name == "스펙터":
    star_color = "#00ffcc"
    ment = "차가운 영혼의 안개가 걷히고 전설의 유령이 눈을 뜹니다..."
  elif aura_name == "와트":
    star_color = "#00ffff"
    ment = "초전설 에너지 과부하! 강력한 전류가 몰아칩니다..."
  elif aura_name == "힘":
    star_color = "#ff0055"
    ment = "현실의 벽을 부주는 압도적인 힘이 폭발합니다..."
  else:
    star_color = "#ffd700"
    ment = "전설적인 에너지가 요동칩니다..."

  fullscreen_html = f"""
    <style>
    @keyframes fullSpinAndGrow {{
        0% {{ transform: rotate(0deg) scale(0.3); opacity: 0.2; }}
        50% {{ transform: rotate(360deg) scale(1.5); opacity: 0.8; }}
        100% {{ transform: rotate(720deg) scale(3.5); opacity: 1; }}
    }}
    .fullscreen-overlay {{
        position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
        background: rgba(5, 5, 10, 0.95);
        display: flex; flex-direction: column; justify-content: center; align-items: center;
        z-index: 999999; text-align: center;
    }}
    .fullscreen-star {{
        display: inline-block;
        animation: fullSpinAndGrow 2.5s ease-in-out forwards;
        font-size: 100px; color: {star_color}; text-shadow: 0 0 50px {star_color};
    }}
    </style>
    <div class="fullscreen-overlay">
        <div class="fullscreen-star">✦</div>
        <h1 style="color: {star_color}; margin-top: 30px; font-size: 38px; text-shadow: 0 0 20px {star_color};">
            [{aura_name}] 강림 임박!
        </h1>
        <p style="font-size: 22px; color: #ffeb3b; margin-top: 15px; font-weight: bold; max-width: 800px;">
            {ment}
        </p>
    </div>
    """

  with placeholder.container():
    st.markdown(fullscreen_html, unsafe_allow_html=True)

  time.sleep(2.5)
  placeholder.empty()


def play_cutscene(aura_name):
  play_fullscreen_star_cutscene(aura_name)


# 1회 뽑기 실행 공통 함수
def perform_roll():
  total_pulls = sum(st.session_state.counts.values()) + 1

  current_weights = list(base_weights)
  st.session_state.luck_active_flag = False

  if st.session_state.luck_buff_unlocked and (total_pulls % 10 == 0):
    current_weights[:5] = [w * 2 for w in current_weights[:5]]
    st.session_state.luck_active_flag = True

  result = random.choices(items, weights=current_weights, k=1)[0]

  if result in cutscene_auras:
    st.session_state.is_cutscene = True
    play_cutscene(result)
    st.session_state.is_cutscene = False
    st.balloons()

  st.session_state.counts[result] += 1
  st.session_state.history.insert(0, result)
  st.session_state.coins += 5
  st.session_state.last_result = result
  return result


st.title("✨ 아우라 가챠 & 도감 시스템")

# ==========================================
# 🌟 [항상 상단 고정] 현재 장착 중인 아우라 영역
# ==========================================
with st.container(border=True):
  st.markdown("### 👤 현재 장착 중인 아우라")
  equipped_aura = st.session_state.equipped

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
      if st.button("❌ 장착 해제", key="top_unequip_btn"):
        st.session_state.equipped = None
        st.rerun()
  else:
    st.session_state.equipped = None
    st.info(
        "현재 장착된 아우라가 없습니다. 뽑기를 통해 아우라를 획득하고"
        " 장착해보세요!"
    )

# 상단 재화 정보
col_c1, col_c2 = st.columns(2)
with col_c1:
  st.metric(label="💰 보유 코인", value=f"{st.session_state.coins} G")
with col_c2:
  total_pulls = sum(st.session_state.counts.values())
  st.metric(label="🎲 총 뽑기 횟수", value=f"{total_pulls}회")

st.divider()

# ==========================================
# 🗂️ 카테고리 탭 구성
# ==========================================
tab_gacha, tab_inventory, tab_codex, tab_shop = st.tabs(
    ["🎲 아우라 뽑기", "🎒 스토리지", "📖 도감 (Codex)", "🛒 상점"]
)

# ------------------------------------------
# [탭 1] 아우라 뽑기
# ------------------------------------------
with tab_gacha:
  st.subheader("🎲 행운의 아우라 소환 (1회당 +5 G)")
  if st.session_state.luck_buff_unlocked:
    st.success("🍀 [행운 버프 활성화됨] 매 10번째 뽑기마다 행운 2배 적용 중!")

  with st.expander("📋 등급별 확률표 보기"):
    weights_sum = sum(base_weights)
    for item, weight in zip(items, base_weights):
      prob = (weight / weights_sum) * 100
      if prob < 0.01:
        prob_str = f"{prob:.6f}%"
      else:
        prob_str = f"{prob:.4f}%"
      st.markdown(
          f"- **{icons.get(item, '✨')} {item}** : `{prob_str}`"
          f" ({fractions.get(item, 'N/A')})"
      )

  st.write("")

  if st.session_state.auto_roll_unlocked:
    st.session_state.auto_roll_active = st.toggle(
        "⚡ 오토 뽑기 활성화 (1초마다 자동 소환)",
        value=st.session_state.auto_roll_active,
        disabled=st.session_state.is_cutscene,
    )

  if st.button(
      "🎲 1회 무료 뽑기",
      type="primary",
      use_container_width=True,
      disabled=st.session_state.is_cutscene,
  ):
    perform_roll()
    st.rerun()

  if (
      st.session_state.auto_roll_unlocked
      and st.session_state.auto_roll_active
      and not st.session_state.is_cutscene
  ):
    perform_roll()
    time.sleep(1)
    st.rerun()

  if st.session_state.luck_active_flag:
    st.markdown(
        """
        <div style="text-align: center; padding: 12px; background-color: #004d40; color: #66ffcc; border-radius: 8px; margin-top: 10px; border: 1px solid #00b0ff; font-weight: bold; font-size: 18px;">
            🍀 [행운 2배 활성화!] 이번 10번째 뽑기 행운이 2배로 적용되었습니다! 🍀
        </div>
        """,
        unsafe_allow_html=True,
    )

  if st.session_state.last_result:
    res = st.session_state.last_result
    icon = icons.get(res, "✨")
    st.markdown(
        f"""
        <div style="text-align: center; padding: 20px; background-color: #1e1e1e; color: white; border-radius: 10px; margin-top: 15px;">
            <span style="font-size: 32px; font-weight: bold;">
                {icon} [{res}] 획득! {icon}
            </span>
            <p style="color: #ffd700; margin-top: 5px;">(+ 5 코인 획득)</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

  st.divider()
  st.subheader("📜 최근 뽑기 기록")
  if st.session_state.history:
    recent = st.session_state.history[:5]
    for i, res in enumerate(recent):
      st.text(
          f"{len(st.session_state.history) - i}번째: {icons.get(res, '✨')} [{res}]"
      )
  else:
    st.text("아직 뽑기 기록이 없습니다.")

# ------------------------------------------
# [탭 2] 스토리지 (인벤토리)
# ------------------------------------------
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
          is_equipped = st.session_state.equipped == item
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

# ------------------------------------------
# [탭 3] 도감 (Codex)
# ------------------------------------------
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

# ------------------------------------------
# [탭 4] 상점 (개발자 비번 인증 및 세이브/로드 시스템)
# ------------------------------------------
with tab_shop:
  st.subheader("🛒 상점 & 데이터 관리")

  # 💾 [신규 기능] 세이브 데이터 백업 및 복구 패널
  with st.container(border=True):
    st.markdown("### 💾 게임 데이터 저장 및 불러오기")
    st.write(
        "플레이 데이터를 파일로 저장하거나, 저장된 파일을 업로드하여"
        " 언제든 이어서 할 수 있습니다."
    )

    # 1. 저장 데이터 JSON 생성
    save_data = {
        "history": st.session_state.history,
        "counts": st.session_state.counts,
        "equipped": st.session_state.equipped,
        "coins": st.session_state.coins,
        "inventory_slots": st.session_state.inventory_slots,
        "auto_roll_unlocked": st.session_state.auto_roll_unlocked,
        "luck_buff_unlocked": st.session_state.luck_buff_unlocked,
    }
    json_str = json.dumps(save_data, ensure_ascii=False, indent=4)

    st.download_button(
        label="📥 게임 데이터 저장하기 (파일 다운로드)",
        data=json_str,
        file_name="sols_rng_save.json",
        mime="application/json",
        use_container_width=True,
    )

    st.write("")
    uploaded_file = st.file_uploader(
        "📤 저장한 데이터 불러오기 (JSON 파일 업로드)", type=["json"]
    )
    if uploaded_file is not None:
      try:
        loaded_data = json.load(uploaded_file)
        # 안전하게 세션에 반영 (새로운 항목이 추가되었어도 에러 안 나게 방어)
        st.session_state.history = loaded_data.get("history", [])
        saved_counts = loaded_data.get("counts", {})
        for item in items:
          st.session_state.counts[item] = saved_counts.get(item, 0)
        st.session_state.equipped = loaded_data.get("equipped", None)
        st.session_state.coins = loaded_data.get("coins", 0)
        st.session_state.inventory_slots = loaded_data.get(
            "inventory_slots", 50
        )
        st.session_state.auto_roll_unlocked = loaded_data.get(
            "auto_roll_unlocked", False
        )
        st.session_state.luck_buff_unlocked = loaded_data.get(
            "luck_buff_unlocked", False
        )
        st.success(
            "성공적으로 게임 데이터를 불러왔습니다! 화면이 갱신됩니다."
        )
        time.sleep(1)
        st.rerun()
      except Exception as e:
        st.error(f"데이터를 불러오는 중 오류가 발생했습니다: {e}")

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
        st.success(
            "개발자 인증 성공! 모든 아우라 도감과 스토리지에 해금되었습니다!"
        )
        st.rerun()
      else:
        st.error("비밀번호가 틀렸습니다!")

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
            st.success("10뽑마다 행운 2배 버프가 해금되었습니다!")
            st.rerun()
          else:
            st.error("코인이 부족합니다!")

  with st.container(border=True):
    col_a1, col_a2 = st.columns([2, 1])
    with col_a1:
      st.markdown("### ⚡ 오토 뽑기 기능 (영구)")
      st.write("1초마다 자동으로 아우라를 뽑아주는 편리한 기능입니다.")
    with col_a2:
      st.write("")
      if st.session_state.auto_roll_unlocked:
        st.button("보유 완료", disabled=True, use_container_width=True)
      else:
        if st.button("구매 (100 G)", key="buy_autoroll", use_container_width=True):
          if st.session_state.coins >= 100:
            st.session_state.coins -= 100
            st.session_state.auto_roll_unlocked = True
            st.session_state.auto_roll_active = True
            st.success("오토 뽑기 기능이 해금되었습니다!")
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
          st.success("가방 칸수가 확장되었습니다!")
          st.rerun()
        else:
          st.error("코인이 부족합니다!")

  st.write("")
  if st.button(
      "🔄 모든 게임 데이터 초기화",
      type="secondary",
      use_container_width=True,
  ):
    st.session_state.history = []
    st.session_state.counts = {item: 0 for item in items}
    st.session_state.equipped = None
    st.session_state.coins = 0
    st.session_state.inventory_slots = 50
    st.session_state.auto_roll_unlocked = False
    st.session_state.auto_roll_active = False
    st.session_state.luck_buff_unlocked = False
    st.session_state.luck_active_flag = False
    st.session_state.last_result = None
    st.session_state.is_cutscene = False
    st.session_state.selected_codex = items[0]
    st.rerun()

# ==========================================
# ⏱️ 오토 뽑기 1초 루프 트리거
# ==========================================
if st.session_state.auto_roll_unlocked and st.session_state.auto_roll_active:
  time.sleep(1)
  st.rerun()
