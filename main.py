import os
import random
import time
import streamlit as st

# 페이지 설정
st.set_page_config(
    page_title="아우라 가챠 & 도감", page_icon="✨", layout="wide"
)

# 등급 리스트 정의 (희귀도 높은 순)
items = [
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

# 각 분수 확률에 따른 가중치 설정 (기준: 200,000)
weights = [1, 1, 1, 6, 12, 24, 48, 97, 781, 1562, 12500, 25000, 50000, 100000]

# 각 아우라의 분수 표시 문자열
fractions = {
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
cutscene_auras = ["바운디드", "재즈", "스펙터", "와트", "힘", "석영", "시데리움"]

# 등급별 이모티콘 매핑
icons = {
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
}

# 세션 상태 초기화
if "history" not in st.session_state:
  st.session_state.history = []
if "counts" not in st.session_state:
  st.session_state.counts = {item: 0 for item in items}
if "equipped" not in st.session_state:
  st.session_state.equipped = None
if "coins" not in st.session_state:
  st.session_state.coins = 0
if "inventory_slots" not in st.session_state:
  st.session_state.inventory_slots = 50
if "auto_roll_unlocked" not in st.session_state:
  st.session_state.auto_roll_unlocked = False
if "auto_roll_active" not in st.session_state:
  st.session_state.auto_roll_active = False
if "last_result" not in st.session_state:
  st.session_state.last_result = None
if "is_cutscene" not in st.session_state:
  st.session_state.is_cutscene = False
if "selected_codex" not in st.session_state:
  st.session_state.selected_codex = items[0]


# ✨ [Sol's RNG 스타일 원작 연출] 화면 중앙에서 별이 회전하며 커지는 CSS 애니메이션 컷씬
def play_sols_rng_cutscene(aura_name):
  placeholder = st.empty()

  if aura_name == "바운디드":
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
    ment = "현실의 벽을 부수는 압도적인 힘이 폭발합니다..."
  else:
    star_color = "#ffd700"
    ment = "전설적인 에너지가 요동칩니다..."

  # CSS 애니메이션 주입 (별이 회전하며 커지는 효과)
  animation_html = f"""
    <style>
    @keyframes spinAndGrow {{
        0% {{ transform: rotate(0deg) scale(0.5); opacity: 0.3; }}
        50% {{ transform: rotate(360deg) scale(1.2); opacity: 0.8; }}
        100% {{ transform: rotate(720deg) scale(2.0); opacity: 1; }}
    }}
    .spinning-star {{
        display: inline-block;
        animation: spinAndGrow 2.5s ease-in-out forwards;
        font-size: 70px;
        color: {star_color};
        text-shadow: 0 0 30px {star_color};
    }}
    </style>
    <div style="
        text-align: center;
        padding: 50px 20px;
        background: #0d0d14;
        border: 3px solid {star_color};
        border-radius: 15px;
        margin-top: 15px;
        margin-bottom: 15px;
        box-shadow: 0 0 30px {star_color};
    ">
        <div style="margin-bottom: 20px;">
            <div class="spinning-star">✦</div>
        </div>
        <h2 style="color: {star_color}; margin: 10px 0; font-size: 26px; text-shadow: 0 0 10px {star_color};">
            [{aura_name}] 강림 임박!
        </h2>
        <p style="font-size: 18px; color: #ffeb3b; margin-top: 10px; font-weight: bold;">
            {ment}
        </p>
    </div>
    """

  with placeholder.container():
    st.markdown(animation_html, unsafe_allow_html=True)

  # 애니메이션 재생 시간 동안 대기
  time.sleep(2.5)
  placeholder.empty()


# 기타 상위 등급 일반 컷씬
def play_cutscene(aura_name):
  play_sols_rng_cutscene(aura_name)


# 1회 뽑기 실행 공통 함수
def perform_roll():
  result = random.choices(items, weights=weights, k=1)[0]

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

  if equipped_aura:
    col_img, col_info = st.columns([1, 4])
    img_path = aura_images.get(equipped_aura)

    with col_img:
      if img_path and os.path.exists(img_path):
        st.image(img_path, use_container_width=True)
      else:
        st.markdown(
            f"<div style='font-size: 50px; text-align: center;'>{icons[equipped_aura]}</div>",
            unsafe_allow_html=True,
        )

    with col_info:
      st.markdown(f"#### {icons[equipped_aura]} **[{equipped_aura}]** 장착 중")
      st.write(f"보유 수량: **{st.session_state.counts[equipped_aura]}개**")
      if st.button("❌ 장착 해제", key="top_unequip_btn"):
        st.session_state.equipped = None
        st.rerun()
  else:
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

  with st.expander("📋 등급별 확률표 보기"):
    weights_sum = sum(weights)
    for item, weight in zip(items, weights):
      prob = (weight / weights_sum) * 100
      st.markdown(f"- **{icons[item]} {item}** : `{prob:.4f}%` ({fractions[item]})")

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

  if st.session_state.last_result:
    res = st.session_state.last_result
    icon = icons[res]
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
          f"{len(st.session_state.history) - i}번째: {icons[res]} [{res}]"
      )
  else:
    st.text("아직 뽑기 기록이 없습니다.")

# ------------------------------------------
# [탭 2] 스토리지 (인벤토리)
# ------------------------------------------
with tab_inventory:
  owned_items = [
      item for item in items if st.session_state.counts[item] > 0
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
          count = st.session_state.counts[item]
          is_equipped = st.session_state.equipped == item
          b_color = border_colors[item]
          icon = icons[item]

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
      is_owned = st.session_state.counts[item] > 0
      display_name = (
          f"{icons[item]} {item}" if is_owned else "🔒 [LOCKED] ???"
      )

      if st.button(
          display_name,
          key=f"codex_select_{item}",
          use_container_width=True,
      ):
        st.session_state.selected_codex = item

  with col_right:
    sel = st.session_state.selected_codex
    is_owned = st.session_state.counts[sel] > 0
    st.markdown(f"#### 상세 정보: `{sel if is_owned else '???'}`")

    with st.container(border=True):
      if is_owned:
        img_path = aura_images.get(sel)
        if img_path and os.path.exists(img_path):
          st.image(img_path, width=150)
        else:
          st.markdown(
              f"<div style='font-size: 40px;'>{icons[sel]}</div>",
              unsafe_allow_html=True,
          )

        st.markdown(f"### [{sel}]")
        st.write(f"**희귀도 확률:** {fractions[sel]}")
        st.write(f"**보유 수량:** {st.session_state.counts[sel]}개")
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
# [탭 4] 상점 (개발자 비번 인증)
# ------------------------------------------
with tab_shop:
  st.subheader("🛒 상점")

  with st.container(border=True):
    st.markdown("### 💻 개발자 인증 패널")
    st.write("비밀번호를 입력하고 개발자 권한을 활성화하세요.")

    dev_password = st.text_input(
        "개발자 비밀번호", type="password", key="dev_pw_input"
    )
    if st.button("🔐 권한 인증 및 모든 도감 해금", type="primary"):
      if dev_password == "0925":
        for item in items:
          if st.session_state.counts[item] == 0:
            st.session_state.counts[item] = 1
        st.success(
            "개발자 인증 성공! 모든 아우라 도감과 스토리지에 해금되었습니다!"
        )
        st.rerun()
      else:
        st.error("비밀번호가 틀렸습니다!")

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
