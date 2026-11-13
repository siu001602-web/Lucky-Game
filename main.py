import os
import random
import time
import streamlit as st

# 페이지 설정
st.set_page_config(
    page_title="아우라 가챠 & 인벤토리", page_icon="✨", layout="centered"
)

# 등급 리스트 정의
items = [
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

# 각 분수 확률에 따른 가중치 설정 (기준: 16,384)
weights = [1, 2, 4, 8, 128, 256, 1024, 2048, 4096, 8192]

# 등급별 이모티콘 매핑
icons = {
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

# 등급별 아우라 이미지 경로 매핑 (장착 프로필용)
aura_images = {
    "일반": "images/SmartSelect_20261113_115337_NAVER.jpg",
    "희귀": "images/SmartSelect_20261113_115402_NAVER.jpg",
    "자연": "images/SmartSelect_20261113_115446_NAVER.jpg",
    "레어": None,
    "결정화": None,
    "분노": None,
    "자력": None,
    "시데리움": None,
    "석영": None,
    "힘": None,
}

# 세션 상태 초기화
if "history" not in st.session_state:
  st.session_state.history = []
if "counts" not in st.session_state:
  st.session_state.counts = {item: 0 for item in items}
if "equipped" not in st.session_state:
  st.session_state.equipped = None
if "coins" not in st.session_state:
  st.session_state.coins = 0  # 0코인으로 시작 (뽑기로 획득)
if "inventory_slots" not in st.session_state:
  st.session_state.inventory_slots = 50
if "auto_roll_unlocked" not in st.session_state:
  st.session_state.auto_roll_unlocked = False  # 오토 뽑기 해금 여부
if "auto_roll_active" not in st.session_state:
  st.session_state.auto_roll_active = False  # 오토 뽑기 작동 상태
if "last_result" not in st.session_state:
  st.session_state.last_result = None  # 마지막 뽑기 결과 저장


# 1회 뽑기 실행 공통 함수
def perform_roll():
  result = random.choices(items, weights=weights, k=1)[0]
  st.session_state.counts[result] += 1
  st.session_state.history.insert(0, result)
  st.session_state.coins += 5  # 1뽑당 무조건 5코인 지급
  st.session_state.last_result = result
  return result


st.title("✨ 아우라 가챠 & 인벤토리")

# ==========================================
# 🌟 [항상 상단 고정] 현재 장착 중인 아우라 영역
# ==========================================
with st.container(border=True):
  st.markdown("### 👤 현재 장착 중인 아우라")
  equipped_aura = st.session_state.equipped

  if equipped_aura:
    col_img, col_info = st.columns([1, 3])
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

# 상단 재화 및 기본 정보
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
tab_gacha, tab_inventory, tab_shop = st.tabs(
    ["🎲 아우라 뽑기", "🎒 아우라 스토리지 (인벤토리)", "🛒 상점"]
)

# ------------------------------------------
# [탭 1] 아우라 뽑기 카테고리
# ------------------------------------------
with tab_gacha:
  st.subheader("🎲 행운의 아우라 소환 (1회당 +5 G)")

  with st.expander("📋 등급별 확률표 보기"):
    total_weight = sum(weights)
    for item, weight in zip(items, weights):
      prob = (weight / total_weight) * 100
      st.markdown(
          f"- **{icons[item]} {item}** : `{prob:.4f}%`"
          f" (1/{int(total_weight/weight)})"
      )

  st.write("")

  # 오토 뽑기 해금 시 토글 버튼 표시
  if st.session_state.auto_roll_unlocked:
    st.session_state.auto_roll_active = st.toggle(
        "⚡ 오토 뽑기 활성화 (1초마다 자동 소환)",
        value=st.session_state.auto_roll_active,
    )

  # 수동 1회 뽑기 버튼
  if st.button("🎲 1회 무료 뽑기", type="primary", use_container_width=True):
    res = perform_roll()
    if res in ["힘", "석영", "시데리움"]:
      st.balloons()
    st.rerun()

  # 오토 뽑기 작동 중일 때 1회 소환 실행
  if st.session_state.auto_roll_unlocked and st.session_state.auto_roll_active:
    res = perform_roll()
    if res in ["힘", "석영", "시데리움"]:
      st.balloons()

  # 최근 뽑기 결과 카드 표시
  if st.session_state.last_result:
    res = st.session_state.last_result
    icon = icons[res]
    st.markdown(
        f"""
            <div style="text-align: center; padding: 25px 0; background-color: #1e1e1e; color: white; border-radius: 10px; margin-top: 15px;">
                <span style="font-size: 36px; font-weight: bold;">
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
# [탭 2] 아우라 스토리지 (그리드 카드 스타일)
# ------------------------------------------
with tab_inventory:
  st.subheader(
      f"📦 아우라 스토리지 [보유 종류: {sum(1 for k in items if st.session_state.counts[k] > 0)} / {len(items)}]"
  )
  st.write("획득한 아우라의 장착 버튼을 눌러 장착할 수 있습니다.")

  cols_per_row = 4
  rows = [items[i : i + cols_per_row] for i in range(0, len(items), cols_per_row)]

  for row in rows:
    cols = st.columns(cols_per_row)
    for idx, item in enumerate(row):
      with cols[idx]:
        count = st.session_state.counts[item]
        is_owned = count > 0
        is_equipped = st.session_state.equipped == item
        b_color = border_colors[item]
        icon = icons[item]

        if is_owned:
          bg_color = "#222222" if not is_equipped else "#1b3a4b"
          opacity = "1.0"
        else:
          bg_color = "#111111"
          opacity = "0.3"

        st.markdown(
            f"""
                <div style="
                    background-color: {bg_color};
                    border: 2px solid {b_color};
                    border-radius: 8px;
                    padding: 12px;
                    text-align: center;
                    opacity: {opacity};
                    margin-bottom: 10px;
                    min-height: 110px;
                ">
                    <div style="font-size: 24px;">{icon}</div>
                    <div style="font-weight: bold; color: white; font-size: 14px; margin-top: 4px;">{item}</div>
                    <div style="color: #aaa; font-size: 11px; margin-top: 2px;">보유: {count}개</div>
                    {"<div style='color: #4da6ff; font-size: 11px; font-weight: bold; margin-top: 2px;'>[장착 중]</div>" if is_equipped else ""}
                </div>
                """,
            unsafe_allow_html=True,
        )

        if is_owned:
          if is_equipped:
            st.button(
                "장착중",
                key=f"grid_eq_{item}",
                disabled=True,
                use_container_width=True,
            )
          else:
            if st.button(
                "장착", key=f"grid_btn_{item}", use_container_width=True
            ):
              st.session_state.equipped = item
              st.rerun()
        else:
          st.button(
              "잠김",
              key=f"grid_lock_{item}",
              disabled=True,
              use_container_width=True,
          )

    st.write("")

# ------------------------------------------
# [탭 3] 상점 카테고리
# ------------------------------------------
with tab_shop:
  st.subheader("🛒 상점")

  # ⚡ 오토 뽑기 기능 구매 상품
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
            st.error("코인이 부족합니다! (20회 뽑기 필요)")

  # 🎒 아우라 가방 확장권
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
    st.rerun()

# ==========================================
# ⏱️ 오토 뽑기 1초 루프 트리거
# ==========================================
if st.session_state.auto_roll_unlocked and st.session_state.auto_roll_active:
  time.sleep(1)
  st.rerun()
