import random
import streamlit as st

# 페이지 설정
st.set_page_config(page_title="뽑기 시뮬레이터", page_icon="🎁", layout="centered")

st.title("🎁 뽑기 시뮬레이터")

# 등급 리스트 정의 (상위 등급부터 하위 등급 순)
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

# 세션 상태 초기화
if "history" not in st.session_state:
  st.session_state.history = []
if "counts" not in st.session_state:
  st.session_state.counts = {item: 0 for item in items}

# 각 분수 확률에 따른 가중치 설정 (기준: 16,384)
weights = [
    1,  # 힘: 1/16384
    2,  # 석영: 1/8192
    4,  # 시데리움: 1/4096
    8,  # 자력: 1/2048
    128,  # 분노: 1/128
    256,  # 결정화: 1/64
    1024,  # 레어: 1/16
    2048,  # 자연: 1/8
    4096,  # 희귀: 1/4
    8192,  # 일반: 1/2
]

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

# 확률표 안내 (접이식)
with st.expander("📋 등급별 확률표 보기"):
  total_weight = sum(weights)
  for item, weight in zip(items, weights):
    prob = (weight / total_weight) * 100
    st.markdown(
        f"- **{icons[item]} {item}** : `{prob:.4f}%` (1/{int(total_weight/weight)})"
    )

# 뽑기 버튼
if st.button("🎲 1회 뽑기", type="primary", use_container_width=True):
  result = random.choices(items, weights=weights, k=1)[0]

  # 횟수 및 기록 업데이트
  st.session_state.counts[result] += 1
  st.session_state.history.insert(0, result)

  # 상위 등급 당첨 시 풍선 효과
  if result in ["힘", "석영", "시데리움", "자력", "분노"]:
    st.balloons()

  # 화면 중앙에 이모티콘과 함께 [등급] 표시
  icon = icons[result]
  st.markdown(
      f"""
        <div style="text-align: center; padding: 30px 0;">
            <span style="font-size: 42px; font-weight: bold;">
                {icon} [{result}] {icon}
            </span>
        </div>
        """,
      unsafe_allow_html=True,
  )

st.divider()

# 통계 및 기록 영역
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
if st.button("🔄 기록 초기화", use_container_width=True):
  st.session_state.history = []
  st.session_state.counts = {item: 0 for item in items}
  st.rerun()
