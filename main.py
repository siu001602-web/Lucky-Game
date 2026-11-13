import os
import random
import streamlit as st

# 페이지 설정
st.set_page_config(
    page_title="아우라 가챠 & 상점 시뮬레이터", page_icon="✨", layout="centered"
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
  st.session_state.coins = 100  # 보너스용 코인
if "inventory_slots" not in st.session_state:
  st.session_state.inventory_slots = 50

st.title("✨ 아우라 가챠 & 상점 시뮬레이터")

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
    ["🎲 아우라 뽑기", "🎒 인벤토리 & 장착", "🛒 아우라 가방 상점"]
)

# ------------------------------------------
# [탭 1] 아우라 뽑기 카테고리 (비용 제거)
# ------------------------------------------
with tab_gacha:
  st.subheader("🎲 행운의 아우라 소환 (무료)")

  # 확률표 안내 (접이식)
  with st.expander("📋 등급별 확률표 보기"):
    total_weight = sum(weights)
    for item, weight in zip(items, weights):
      prob = (weight / total_weight) * 100
      st.markdown(
          f"- **{icons[item]} {item}** : `{prob:.4f}%`"
          f" (1/{int(total_weight/weight)})"
      )

  st.write("")

  # 무료 뽑기 버튼
  if st.button("🎲 1회 무료 뽑기", type="primary", use_container_width=True):
    result = random.choices(items, weights=weights, k=1)[0]

    # 횟수 및 기록 업데이트
    st.session_state.counts[result] += 1
    st.session_state.history.insert(0, result)

    # 보상 코인 지급
    reward_coin = 5
    if result in ["힘", "석영", "시데리움"]:
      reward_coin = 100
      st.balloons()
    elif result in ["자력", "분노", "결정화"]:
      reward_coin = 30
    st.session_state.coins += reward_coin

    # 뽑기 결과 표시
    icon = icons[result]
    st.markdown(
        f"""
            <div style="text-align: center; padding: 25px 0; background-color: #f0f2f6; border-radius: 10px; margin-top: 15px;">
                <span style="font-size: 36px; font-weight: bold;">
                    {icon} [{result}] 획득! {icon}
                </span>
                <p style="color: gray; margin-top: 5px;">(+ 보너스 코인 {reward_coin}G 획득)</p>
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
# [탭 2] 인벤토리 & 장착 카테고리 (나열식)
# ------------------------------------------
with tab_inventory:
  st.subheader("🎒 아우라 도감 및 나열식 장착")
  st.write("보유 중인 아우라를 확인하고 원하는 아우라를 장착하세요.")

  # 모든 아우라를 쭉 나열하여 표시
  for item in items:
    count = st.session_state.counts[item]
    is_owned = count > 0
    is_equipped = st.session_state.equipped == item

    with st.container(border=True):
      col_icon, col_name, col_status, col_btn = st.columns([1, 2, 2, 1])

      with col_icon:
        st.markdown(
            f"<div style='font-size: 30px; text-align: center;'>{icons[item]}</div>",
            unsafe_allow_html=True,
        )

      with col_name:
        st.markdown(f"**[{item}]**")
        if is_equipped:
          st.caption("✨ 장착 중")

      with col_status:
        st.write(f"보유: **{count}개**")

      with col_btn:
        if is_owned:
          if is_equipped:
            st.button("장착중", key=f"eq_{item}", disabled=True, use_container_width=True)
          else:
            if st.button("장착하기", key=f"btn_{item}", use_container_width=True):
              st.session_state.equipped = item
              st.rerun()
        else:
          st.caption("미보유")

# ------------------------------------------
# [탭 3] 아우라 가방 상점 카테고리
# ------------------------------------------
with tab_shop:
  st.subheader("🛒 아우라 가방 & 상점")
  st.write("뽑기로 얻은 코인으로 가방 슬롯을 확장하거나 코인을 충전하세요.")

  with st.container(border=True):
    col_s1, col_s2 = st.columns([2, 1])
    with col_s1:
      st.markdown("### 🎒 아우라 가방 확장권")
      st.write(
          f"현재 가방 최대 수용 칸수: **{st.session_state.inventory_slots}칸**"
      )
    with col_s2:
      st.write("")
      if st.button("구매 (50 G)", use_container_width=True):
        if st.session_state.coins >= 50:
          st.session_state.coins -= 50
          st.session_state.inventory_slots += 20
          st.success("가방 칸수가 20칸 확장되었습니다!")
          st.rerun()
        else:
          st.error("코인이 부족합니다!")

  with st.container(border=True):
    col_s3, col_s4 = st.columns([2, 1])
    with col_s3:
      st.markdown("### 💰 긴급 코인 충전")
      st.write("무료로 코인 100G를 즉시 충전합니다.")
    with col_s4:
      st.write("")
      if st.button("충전 받기", use_container_width=True):
        st.session_state.coins += 100
        st.success("코인 100G가 충전되었습니다!")
        st.rerun()

  st.write("")
  if st.button(
      "🔄 모든 게임 데이터 초기화",
      type="secondary",
      use_container_width=True,
  ):
    st.session_state.history = []
    st.session_state.counts = {item: 0 for item in items}
    st.session_state.equipped = None
    st.session_state.coins = 100
    st.session_state.inventory_slots = 50
    st.rerun()
