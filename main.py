import os
import random
import streamlit as st

# 페이지 설정
st.set_page_config(
    page_title="아우라 뽑기 & 장착 시뮬레이터", page_icon="✨", layout="centered"
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

# 등급별 아우라 이미지 경로 매핑 (나머지 등급도 이미지 추가 시 여기에 경로 입력)
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
  st.session_state.equipped = None  # 현재 장착 중인 아우라

st.title("✨ 아우라 뽑기 & 장착 시뮬레이터")

# ==========================================
# 1. 현재 장착 중인 아우라 표시 영역
# ==========================================
st.subheader("👤 현재 장착 중인 아우라")
equipped_aura = st.session_state.equipped

with st.container(border=True):
  if equipped_aura:
    col_img, col_info = st.columns([1, 2])
    img_path = aura_images.get(equipped_aura)

    with col_img:
      if img_path and os.path.exists(img_path):
        st.image(img_path, use_container_width=True)
      else:
        # 이미지가 아직 없는 등급일 경우 이모티콘 크게 표시
        st.markdown(
            f"<div style='font-size: 64px; text-align: center;'>{icons[equipped_aura]}</div>",
            unsafe_allow_html=True,
        )

    with col_info:
      st.markdown(f"### {icons[equipped_aura]} **[{equipped_aura}]** 장착됨")
      st.write(f"보유 수량: **{st.session_state.counts[equipped_aura]}개**")
      if st.button("❌ 장착 해제", key="unequip_btn"):
        st.session_state.equipped = None
        st.rerun()
  else:
    st.info(
        "현재 장착된 아우라가 없습니다. 아래에서 아우라를 뽑은 뒤 장착해보세요!"
    )

st.divider()

# ==========================================
# 2. 아우라 뽑기 영역
# ==========================================
if st.button("🎲 1회 뽑기", type="primary", use_container_width=True):
  result = random.choices(items, weights=weights, k=1)[0]

  # 횟수 및 기록 업데이트
  st.session_state.counts[result] += 1
  st.session_state.history.insert(0, result)

  if result in ["힘", "석영", "시데리움", "자력", "분노"]:
    st.balloons()

  # 뽑기 결과 표시
  icon = icons[result]
  st.markdown(
      f"""
        <div style="text-align: center; padding: 20px 0;">
            <span style="font-size: 38px; font-weight: bold;">
                {icon} [{result}] 획득! {icon}
            </span>
        </div>
        """,
      unsafe_allow_html=True,
  )

  # 뽑은 아우라에 이미지가 등록되어 있다면 결과창에도 살짝 보여주기
  res_img = aura_images.get(result)
  if res_img and os.path.exists(res_img):
    _, mid_col, _ = st.columns([1, 1, 1])
    with mid_col:
      st.image(res_img, caption=f"[{result}] 아우라", use_container_width=True)

st.divider()

# ==========================================
# 3. 인벤토리 (보유 아우라 선택 및 장착)
# ==========================================
st.subheader("🎒 보유 아우라 장착하기")

# 1개 이상 보유한 아우라만 필터링
owned_auras = [item for item in items if st.session_state.counts[item] > 0]

if owned_auras:
  col_sel, col_btn = st.columns([3, 1])
  with col_sel:
    selected_aura = st.selectbox(
        "장착할 아우라를 선택하세요:",
        options=owned_auras,
        format_func=lambda x: (
            f"{icons[x]} {x} (보유: {st.session_state.counts[x]}개)"
        ),
        label_visibility="collapsed",
    )
  with col_btn:
    if st.button("⚔️ 장착하기", use_container_width=True):
      st.session_state.equipped = selected_aura
      st.rerun()
else:
  st.caption("아직 보유한 아우라가 없습니다. 먼저 뽑기를 진행해주세요.")

st.divider()

# ==========================================
# 4. 통계 및 최근 기록 영역
# ==========================================
col1, col2 = st.columns(2)

with col1:
  st.subheader("📊 누적 통계")
  total_pulls = sum(st.session_state.counts.values())
  st.write(f"총 뽑기 횟수: **{total_pulls}회**")

  for item in items:
    count = st.session_state.counts[item]
    rate = (count / total_pulls * 100) if total_pulls > 0 else 0
    st.text(f"{icons[item]} {item}: {count}회 ({rate:.2f}%)")

with col2:
  st.subheader("📜 최근 뽑기 기록")
  if st.session_state.history:
    recent = st.session_state.history[:5]
    for i, res in enumerate(recent):
      st.text(
          f"{len(st.session_state.history) - i}번째: {icons[res]} [{res}]"
      )
  else:
    st.text("아직 뽑기 기록이 없습니다.")

st.write("")

# 초기화 버튼
if st.button("🔄 모든 데이터 초기화", use_container_width=True):
  st.session_state.history = []
  st.session_state.counts = {item: 0 for item in items}
  st.session_state.equipped = None
  st.rerun()
