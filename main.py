import random
import streamlit as st

# 페이지 설정
st.set_page_config(page_title="뽑기 시뮬레이터", page_icon="🎁", layout="centered")

st.title("🎁 뽑기 시뮬레이터")

# 세션 상태 초기화
if "history" not in st.session_state:
  st.session_state.history = []
if "counts" not in st.session_state:
  st.session_state.counts = {
      "신성": 0,
      "토큰": 0,
      "전설": 0,
      "에픽": 0,
      "희귀": 0,
      "일반": 0,
  }

# 등급 및 가중치 설정 (총합 1,000,000 기준)
items = ["신성", "토큰", "전설", "에픽", "희귀", "일반"]
weights = [
    20,  # 신성: 0.002% (1/50,000)
    1000,  # 토큰: 0.1% (1/1,000)
    10000,  # 전설: 1%
    190000,  # 에픽: 19%
    300000,  # 희귀: 30%
    498980,  # 일반: 49.898%
]

# 등급별 색상 설정
colors = {
    "신성": "#FF1493",  # 진분홍
    "토큰": "#00CED1",  # 청록
    "전설": "#FFA500",  # 주황/금색
    "에픽": "#9932CC",  # 보라
    "희귀": "#1E90FF",  # 파랑
    "일반": "#808080",  # 회색
}

# 뽑기 버튼
if st.button("🎲 1회 뽑기", type="primary", use_container_width=True):
  result = random.choices(items, weights=weights, k=1)[0]

  # 횟수 및 기록 업데이트
  st.session_state.counts[result] += 1
  st.session_state.history.insert(0, result)

  # 희귀 등급 풍선 효과 (원치 않으시면 이 두 줄은 지우셔도 됩니다)
  if result in ["신성", "토큰"]:
    st.balloons()

  # 화면 중앙에 깔끔하게 [등급]만 표시
  color = colors[result]
  st.markdown(
      f"""
        <div style="text-align: center; padding: 30px 0;">
            <span style="font-size: 42px; font-weight: bold; color: {color};">
                [{result}]
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

  for item, count in st.session_state.counts.items():
    rate = (count / total_pulls * 100) if total_pulls > 0 else 0
    st.text(f"{item}: {count}회 ({rate:.3f}%)")

with col2:
  st.subheader("📜 최근 뽑기 기록")
  if st.session_state.history:
    recent = st.session_state.history[:5]
    for i, res in enumerate(recent):
      st.text(f"{len(st.session_state.history) - i}번째: [{res}]")
  else:
    st.text("아직 뽑기 기록이 없습니다.")

# 초기화 버튼
if st.button("🔄 기록 초기화"):
  st.session_state.history = []
  st.session_state.counts = {
      "신성": 0,
      "토큰": 0,
      "전설": 0,
      "에픽": 0,
      "희귀": 0,
      "일반": 0,
  }
  st.rerun()
