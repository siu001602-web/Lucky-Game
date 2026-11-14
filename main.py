import base64
from datetime import datetime
import hashlib
json = __import__("json")
os = __import__("os")
random = __import__("random")
sqlite3 = __import__("sqlite3")
time = __import__("time")
colorsys = __import__("colorsys")
import streamlit as st

# 페이지 설정
st.set_page_config(
    page_title="아우라 가챠 & 도감", page_icon="✨", layout="wide"
)

# 등급 리스트 정의 (희귀도 높은 순)
items = [
    "𝓣𝓱𝓮 𝓞𝓻𝓲𝓰𝓲𝓷 𝓗𝓪𝓷𝓭", "𝓓𝓻𝓮𝓪𝓶𝓬𝓪𝓽𝓬𝓱𝓮𝓻", "사도:베일", "수확가", "악몽의 하늘", "𝓘𝓬𝓮𝓐𝓰𝓮", "𝓜𝓪𝓶𝓶𝓸𝓽𝓱",
    "✧ 𝓗𝔂𝓹𝓮𝓻 𝓟𝓻𝓲𝓼𝓶 ✧", "𝓢𝔂𝓶𝓹𝓱𝓸𝓷𝔂♤", "𝓢𝓹𝓮𝓬𝓽𝓻𝓪𝓕𝓵𝓸𝔀 𖤐", "༒ 𝕷𝕰𝕁𝕴𝕬𝕿𝕳𝕬𝕹 ༒", "감시자",
    "아쿠아리움", "선원", "샤킨", "포세이돈", "에바네샌트",
    "기원", "망령", "듀라한", "영혼 사냥꾼", "묘화", "밤나팔꽃", "바이탈", "룬(나이트)", "펌프",
    "블리자드", "이상", "크로마틱", "자장가",
    "그래피티", "헬리오스", "속력", "황혼",
    "아파타이트", "대마법사", "아케인", "워록",
    "테러", "바운디드", "재즈", "스펙터",
    "이색", "노틸러스", "아쿠아틱",
    "만년서리", "태양", "달", "와트",
    "힘", "카와이", "석영", "출혈",
    "시데리움", "콜라", "빙하", "재",
    "자력", "글록", "아쿠아마린", "사파이어", "잉크",
    "에메랄드", "루비", "분노", "토파즈",
    "결정화", "현기증", "원자", "수소", "레어", "자연",
    "굿", "희귀", "일반",
]

denominators = {
    "𝓣𝓱𝓮 𝓞𝓻𝓲𝓰𝓲𝓷 𝓗𝓪𝓷𝓭": 7500000000, "𝓓𝓻𝓮𝓪𝓶𝓬𝓪𝓽𝓬𝓱𝓮𝓻": 2222222222,
    "사도:베일": 800000000, "수확가": 666000000, "악몽의 하늘": 190000000,
    "𝓘𝓬𝓮𝓐𝓰𝓮": 1500000000, "𝓜𝓪𝓶𝓶𝓸𝓽𝓱": 300000000,
    "✧ 𝓗𝔂𝓹𝓮𝓻 𝓟𝓻𝓲𝓼𝓶 ✧": 200000000, "𝓢𝔂𝓶𝓹𝓱𝓸𝓷𝔂♤": 175000000, "𝓢𝓹𝓮𝓬𝓽𝓻𝓪𝓕𝓵𝓸𝔀 𖤐": 100000000,
    "༒ 𝕷𝕰𝕁𝕴𝕬𝕿𝕳𝕬𝕹 ༒": 1730400000, "감시자": 45000000,
    "아쿠아리움": 80000000, "선원": 12000000, "샤킨": 10000000, "포세이돈": 4000000, "에바네샌트": 3360000,
    "기원": 6500000, "망령": 4100000,
    "듀라한": 72000000, "영혼 사냥꾼": 40000000, "묘화": 21000000, "밤나팔꽃": 10000000, "바이탈": 6000000, "룬(나이트)": 1000000, "펌프": 200000,
    "블리자드": 27315000, "이상": 24691356, "크로마틱": 20000000, "자장가": 17000000,
    "그래피티": 12000000, "헬리오스": 9000000, "속력": 7630000, "황혼": 6000000,
    "아파타이트": 3133133, "대마법사": 1766000, "아케인": 1000000, "워록": 660000,
    "테러": 400000, "바운디드": 200000, "재즈": 160000, "스펙터": 140000,
    "이색": 99999, "노틸러스": 70000, "아쿠아틱": 40000,
    "만년서리": 73500, "태양": 50000, "달": 50000, "와트": 32768,
    "힘": 16384, "카와이": 12300, "석영": 8192, "출혈": 4444,
    "시데리움": 4096, "콜라": 3999, "빙하": 2304, "재": 2300,
    "자력": 2048, "글록": 1700, "아쿠아마린": 900, "사파이어": 800, "잉크": 700,
    "에메랄드": 500, "루비": 350, "분노": 256, "토파즈": 150,
    "결정화": 128, "현기증": 123, "원자": 1180, "수소": 1111, "레어": 16, "자연": 8,
    "굿": 5, "희귀": 4, "일반": 2,
}

halloween_auras = [
    "펌프", "룬(나이트)", "바이탈", "밤나팔꽃", "묘화", "영혼 사냥꾼", "듀라한",
    "악몽의 하늘", "수확가", "사도:베일"
]

aura_colors = {
    "𝓣𝓱𝓮 𝓞𝓻𝓲𝓰𝓲𝓷 𝓗𝓪𝓷𝓭": "#ffd700",
    "𝓓𝓻𝓮𝓪𝓶𝓬𝓪𝓽𝓬𝓱𝓮𝓻": "#b366ff",
    "사도:베일": "#ff3366",
    "수확가": "#ff6600",
    "악몽의 하늘": "#9900cc",
    "𝓘𝓬𝓮𝓐𝓰𝓮": "#00bfff",
    "𝓜𝓪𝓶𝓶𝓸𝓽𝓱": "#add8e6",
    "✧ 𝓗𝔂𝓹𝓮𝓻 𝓟𝓻𝓲𝓼𝓶 ✧": "#ff77ff",
    "𝓢𝔂𝓶𝓹𝓱𝓸𝓷𝔂♤": "#ffaa33",
    "𝓢𝓹𝓮𝓬𝓽𝓻𝓪𝓕𝓵𝓸𝔀 𖤐": "#00ffff",
    "༒ 𝕷𝕰𝕁𝕴𝕬𝕿𝕳𝕬𝕹 ༒": "#00aaee",
}

base_weights = [max(1, int(7500000000000 / denominators[item])) for item in items]

fractions = {
    "𝓣𝓱𝓮 𝓞𝓻𝓲𝓰𝓲𝓷 𝓗𝓪𝓷𝓭": "1 in 7,500,000,000 (운명조작: 장착 시 1회당 10뽑 가능)",
    "𝓓𝓻𝓮𝓪𝓶𝓬𝓪𝓽𝓬𝓱𝓮𝓻": "1 in 2,222,222,222 (밤 버프 시 2배 / 장착 시 밤 행운 10배)",
    "사도:베일": "1 in 800,000,000 (할로윈 전용 / 장착 시 뽑기마다 0.1% 확률로 500배 행운 포션 드랍)",
    "수확가": "1 in 666,000,000 (할로윈 전용 / 장착 시 100뽑마다 행운 2배 증가)",
    "악몽의 하늘": "1 in 190,000,000 (할로윈 전용 / 장착 시 3턴 내 1% 확률로 10배~1000배 행운 발현)",
    "𝓘𝓬𝓮𝓐𝓰𝓮": "1 in 1,500,000,000 (눈올 때 행운 10배)",
    "𝓜𝓪𝓶𝓶𝓸𝓽𝓱": "1 in 300,000,000 (눈 확률 10% 증가)",
    "✧ 𝓗𝔂𝓹𝓮𝓻 𝓟𝓻𝓲𝓼𝓶 ✧": "1 in 200,000,000 (장착 시 크로마틱 확률 2배 증가)",
    "𝓢𝔂𝓶𝓹𝓱𝓸𝓷𝔂♤": "1 in 175,000,000 (황금선율: 장착 시 1분마다 5% 확률로 3분간 행운 10배, 중첩 가능)",
    "𝓢𝓹𝓮𝓬𝓽𝓻𝓪𝓕𝓵𝓸𝔀 𖤐": "1 in 100,000,000 (장착 시 코인 획득량 2배)",
    "༒ 𝕷𝕰𝕁𝕴𝕬𝕿𝕳𝕬𝕹 ༒": "1 in 1,730,400,000 (절대포식: 뽑기 시 0.5% 확률로 해당 칸 아우라를 삼키고 백만배 행운 적용)",
    "감시자": "1 in 45,000,000",
    "아쿠아리움": "1 in 80,000,000 (비올 때 확률 4배)",
    "선원": "1 in 12,000,000 (비올 때 확률 4배)",
    "샤킨": "1 in 10,000,000 (비올 때 확률 4배)",
    "포세이돈": "1 in 4,000,000 (비올 때 확률 4배)",
    "에바네샌트": "1 in 3,360,000 (비올 때 확률 4배)",
    "기원": "1 in 6,500,000",
    "망령": "1 in 4,100,000",
    "듀라한": "1 in 72,000,000 (할로윈 2024 바이옴 전용)",
    "영혼 사냥꾼": "1 in 40,000,000 (할로윈 2024 바이옴 전용)",
    "묘화": "1 in 21,000,000 (할로윈 2024 바이옴 전용)",
    "밤나팔꽃": "1 in 10,000,000 (할로윈 2024 바이옴 전용)",
    "바이탈": "1 in 6,000,000 (할로윈 2024 바이옴 전용)",
    "룬(나이트)": "1 in 1,000,000 (할로윈 2024 바이옴 전용)",
    "펌프": "1 in 200,000 (할로윈 2024 바이옴 전용)",
    "블리자드": "1 in 27,315,000 (눈올 때 확률 3배)",
    "이상": "1 in 24,691,356",
    "크로마틱": "1 in 20,000,000",
    "자장가": "1 in 17,000,000 (밤 버프 시 1 in 1,700,000)",
    "그래피티": "1 in 12,000,000",
    "헬리오스": "1 in 9,000,000",
    "속력": "1 in 7,630,000",
    "황혼": "1 in 6,000,000 (밤 버프 시 1 in 600,000)",
    "아파타이트": "1 in 3,133,133",
    "대마법사": "1 in 1,766,000",
    "아케인": "1 in 1,000,000",
    "워록": "1 in 660,000",
    "테러": "1 in 400,000",
    "바운디드": "1 in 200,000",
    "재즈": "1 in 160,000",
    "스펙터": "1 in 140,000",
    "이색": "1 in 99,999",
    "노틸러스": "1 in 70,000",
    "아쿠아틱": "1 in 40,000",
    "만년서리": "1 in 73,500 (눈올 때 확률 3배)",
    "태양": "1 in 50,000 (낮 버프 시 1 in 5,000)",
    "달": "1 in 50,000 (밤 버프 시 1 in 5,000)",
    "와트": "1 in 32,768",
    "힘": "1 in 16,384",
    "카와이": "1 in 12,300",
    "석영": "1 in 8,192",
    "출혈": "1 in 4,444",
    "시데리움": "1 in 4096",
    "콜라": "1 in 3999",
    "빙하": "1 in 2304 (눈올 때 확률 3배)",
    "재": "1 in 2300",
    "자력": "1 in 2048",
    "글록": "1 in 1700",
    "아쿠아마린": "1 in 900",
    "사파이어": "1 in 800",
    "잉크": "1 in 700",
    "에메랄드": "1 in 500",
    "루비": "1 in 350",
    "분노": "1 in 256",
    "토파즈": "1 in 150",
    "결정화": "1 in 128",
    "현기증": "1 in 123",
    "원자": "1 in 1180",
    "수소": "1 in 1111",
    "레어": "1 in 16",
    "자연": "1 in 8",
    "굿": "1 in 5",
    "희귀": "1 in 4",
    "일반": "1 in 2",
}

cutscene_auras = [
    "𝓣𝓱𝓮 𝓞𝓻𝓲𝓰𝓲𝓷 𝓗𝓪𝓷𝓭", "𝓓𝓻𝓮𝓪𝓶𝓬𝓪𝓽𝓬𝓱𝓮𝓻", "사도:베일", "수확가", "악몽의 하늘", "𝓘𝓬𝓮𝓐𝓰𝓮", "𝓜𝓪𝓶𝓶𝓸𝓽𝓱",
    "✧ 𝓗𝔂𝓹𝓮𝓻 𝓟𝓻𝓲𝓼𝓶 ✧", "𝓢𝔂𝓶𝓹𝓱𝓸𝓷𝔂♤", "𝓢𝓹𝓮𝓬𝓽𝓻𝓪𝓕𝓵𝓸𝔀 𖤐", "༒ 𝕷𝕰𝕁𝕴𝕬𝕿𝕳𝕬𝕹 ༒", "감시자",
    "아쿠아리움", "선원", "샤킨", "포세이돈", "에바네샌트",
    "기원", "망령", "듀라한", "영혼 사냥꾼", "묘화", "밤나팔꽃", "바이탈", "룬(나이트)", "펌프",
    "블리자드", "이상", "크로마틱", "자장가",
    "그래피티", "헬리오스", "속력", "황혼",
    "아파타이트", "대마법사", "아케인", "워록",
    "테러", "바운디드", "재즈", "스펙터",
    "태양", "달", "와트", "힘",
    "카와이", "석영", "시데리움",
]

icons = {
    "𝓣𝓱𝓮 𝓞𝓻𝓲𝓰𝓲𝓷 𝓗𝓪𝓷𝓭": "🖐️✨🌌👑", "𝓓𝓻𝓮𝓪𝓶𝓬𝓪𝓽𝓬𝓱𝓮𝓻": "🕸️🌙✨🦋",
    "사도:베일": "🎃👁️", "수확가": "🎃🗡️", "악몽의 하늘": "🎃🌌",
    "𝓘𝓬𝓮𝓐𝓰𝓮": "❄️🧊👑", "𝓜𝓪𝓶𝓶𝓸𝓽𝓱": "🦣❄️🧊",
    "✧ 𝓗𝔂𝓹𝓮𝓻 𝓟𝓻𝓲𝓼𝓶 ✧": "🌈💎✨", "𝓢𝔂𝓶𝓹𝓱𝓸𝓷𝔂♤": "🎼🎻✨♠️", "𝓢𝓹𝓮𝓬𝓽𝓻𝓪𝓕𝓵𝓸𝔀 𖤐": "🌌💠💫",
    "༒ 𝕷𝕰𝕁𝕴𝕬𝕿𝕳𝕬𝕹 ༒": "🌊🐉🌀", "감시자": "👁️‍🗨️⚡",
    "아쿠아리움": "🐠🌊🏛️", "선원": "⚓⛵🌊", "샤킨": "🦈🌊⚡", "포세이돈": "🔱🌊🌊", "에바네샌트": "🌀✨🌌",
    "기원": "🌌✨", "망령": "👻⚡",
    "듀라한": "🎃🗡️", "영혼 사냥꾼": "🎃👻", "묘화": "🎃🔥", "밤나팔꽃": "🎃🌸", "바이탈": "🎃💉", "룬(나이트)": "🎃🛡️", "펌프": "🎃✨",
    "블리자드": "❄️🌨️🌀", "이상": "🌀❓🌌", "크로마틱": "🌈💫", "자장가": "🌌🎵💤",
    "그래피티": "🎨✨", "헬리오스": "☀️🔥", "속력": "⚡💨", "황혼": "🌆✨💜",
    "아파타이트": "💠💎", "대마법사": "🧙‍♂️✨", "아케인": "🔮👑", "워록": "💀🔥",
    "테러": "💣💥", "바운디드": "🌌👑", "재즈": "🎶🎷", "스펙터": "👻🔮",
    "이색": "🌈✨", "노틸러스": "🐚🌊", "아쿠아틱": "💧✨",
    "만년서리": "❄️💎", "태양": "☀️✨", "달": "🌙✨", "와트": "⚡👑⚡",
    "힘": "⚡🔥", "카와이": "🎀💖✨", "석영": "💎✨", "출혈": "🩸⚔️",
    "시데리움": "🌟🛡️", "콜라": "🥤🫧", "빙하": "🧊❄️", "재": "🌫️🔥",
    "자력": "🧲💫", "글록": "🔫💥", "아쿠아마린": "🌊💎", "사파이어": "💙💎", "잉크": "🖋️🖤",
    "에메랄드": "💚💎", "루비": "❤️💎", "분노": "😡💢", "토파즈": "💛💎",
    "결정화": "🔮✨", "현기증": "😵‍💫🌀", "원자": "⚛️✨", "수소": "🧪✨", "레어": "💙📦", "자연": "🌿🍃",
    "굿": "👍✨", "희귀": "💧📘", "일반": "⚪📦",
}

aura_images = {
    "일반": "images/SmartSelect_20261113_115337_NAVER.jpg",
    "희귀": "images/SmartSelect_20261113_115402_NAVER.jpg",
    "굿": "images/SmartSelect_20261114_222408_NAVER.jpg",
    "자연": "images/SmartSelect_20261113_115446_NAVER.jpg",
    "레어": "images/SmartSelect_20261113_123717_Chrome.jpg",
    "수소": "images/SmartSelect_20261115_020236_Chrome.jpg",
    "원자": "images/SmartSelect_20261115_020252_Chrome.jpg",
    "현기증": "images/SmartSelect_20261114_222110_NAVER.jpg",
    "결정화": "images/SmartSelect_20261113_123732_Chrome.jpg",
    "토파즈": "images/SmartSelect_20261114_222131_NAVER.jpg",
    "분노": "images/SmartSelect_20261113_123747_Chrome.jpg",
    "루비": "images/SmartSelect_20261114_222150_NAVER.jpg",
    "에메랄드": "images/SmartSelect_20261114_222223_NAVER.jpg",
    "잉크": "images/SmartSelect_20261114_222257_NAVER.jpg",
    "사파이어": "images/SmartSelect_20261114_222318_NAVER.jpg",
    "아쿠아마린": "images/SmartSelect_20261114_222350_NAVER.jpg",
    "글록": "images/SmartSelect_20261115_020312_Chrome.jpg",
    "자력": "images/SmartSelect_20261113_123943_Chrome.jpg",
    "재": "images/SmartSelect_20261114_165430_Chrome.jpg",
    "빙하": "images/SmartSelect_20261114_102325_NAVER.jpg",
    "콜라": "images/SmartSelect_20261114_165408_Chrome.jpg",
    "시데리움": "images/SmartSelect_20261113_123957_Chrome.jpg",
    "출혈": "images/SmartSelect_20261114_165351_Chrome.jpg",
    "석영": "images/SmartSelect_20261113_124024_Chrome.jpg",
    "카와이": "images/SmartSelect_20261114_170711_Chrome.jpg",
    "힘": "images/SmartSelect_20261113_124048_Chrome.jpg",
    "와트": "images/SmartSelect_20261113_125018_NAVER.jpg",
    "달": "images/SmartSelect_20261113_235408_Chrome.jpg",
    "태양": "images/SmartSelect_20261113_235302_Chrome.jpg",
    "만년서리": "images/SmartSelect_20261114_102346_NAVER.jpg",
    "아쿠아틱": "images/SmartSelect_20261115_024126_NAVER.jpg",
    "노틸러스": "images/SmartSelect_20261115_024039_NAVER.jpg",
    "이색": "images/SmartSelect_20261115_024102_NAVER.jpg",
    "스펙터": "images/SmartSelect_20261113_125325_Chrome.jpg",
    "재즈": "images/SmartSelect_20261113_125353_Chrome.jpg",
    "바운디드": "images/SmartSelect_20261113_125424_Chrome.jpg",
    "테러": "images/SmartSelect_20261114_170620_Chrome.jpg",
    "워록": "images/SmartSelect_20261113_222357_Chrome.jpg",
    "아케인": "images/SmartSelect_20261113_222429_Chrome.jpg",
    "대마법사": "images/SmartSelect_20261113_230233_Chrome.jpg",
    "아파타이트": "images/SmartSelect_20261114_165512_Chrome.jpg",
    "황혼": "images/SmartSelect_20261113_235637_Chrome.jpg",
    "속력": "images/SmartSelect_20261114_165543_Chrome.jpg",
    "헬리오스": "images/SmartSelect_20261113_230344_Chrome.jpg",
    "그래피티": "images/SmartSelect_20261114_170754_Chrome.jpg",
    "자장가": "images/SmartSelect_20261113_235654_Chrome.jpg",
    "크로마틱": "images/SmartSelect_20261113_230417_Chrome.jpg",
    "이상": "images/SmartSelect_20261114_223653_Chrome.jpg",
    "블리자드": "images/SmartSelect_20261114_102513_NAVER.jpg",
    "펌프": "Halloween/SmartSelect_20261115_025739_Chrome.jpg",
    "룬(나이트)": "Halloween/SmartSelect_20261115_025805_Chrome.jpg",
    "바이탈": "Halloween/SmartSelect_20261115_025830_Chrome.jpg",
    "밤나팔꽃": "Halloween/SmartSelect_20261115_025911_Chrome.jpg",
    "묘화": "Halloween/SmartSelect_20261115_025927_Chrome.jpg",
    "영혼 사냥꾼": "Halloween/SmartSelect_20261115_025943_Chrome.jpg",
    "듀라한": "Halloween/SmartSelect_20261115_030001_Chrome.jpg",
    "악몽의 하늘": "Halloween/SmartSelect_20261115_032306_Chrome.jpg",
    "수확가": "Halloween/SmartSelect_20261115_032331_Chrome.jpg",
    "사도:베일": "Halloween/SmartSelect_20261115_032347_Chrome.jpg",
    "기원": "images/SmartSelect_20261115_024250_NAVER.jpg",
    "망령": "images/SmartSelect_20261115_024226_NAVER.jpg",
    "에바네샌트": "images/SmartSelect_20261115_020409_Chrome.jpg",
    "포세이돈": "images/SmartSelect_20261115_020426_Chrome.jpg",
    "샤킨": "images/SmartSelect_20261115_020446_Chrome.jpg",
    "선원": "images/SmartSelect_20261115_020503_Chrome.jpg",
    "아쿠아리움": "images/SmartSelect_20261115_020523_Chrome.jpg",
    "감시자": "images/SmartSelect_20261113_233734_Chrome.jpg",
    "༒ 𝕷𝕰𝕁𝕴𝕬𝕿𝕳𝕬𝕹 ༒": "images/SmartSelect_20261115_020543_Chrome.jpg",
    "𝓢𝓹𝓮𝓬𝓽𝓻𝓪𝓕𝓵𝓸𝔀 𖤐": "images/SmartSelect_20261113_234508_Chrome.jpg",
    "𝓢𝔂𝓶𝓹𝓱𝓸𝓷𝔂♤": "images/SmartSelect_20261114_224237_Chrome.jpg",
    "✧ 𝓗𝔂𝓹𝓮𝓻 𝓟𝓻𝓲𝓼𝓶 ✧": "images/SmartSelect_20261114_172102_NAVER.jpg",
    "𝓜𝓪𝓶𝓶𝓸𝓽𝓱": "images/file_00000000485082099074341e8735beff.png",
    "𝓘𝓬𝓮𝓐𝓰𝓮": "images/file_000000009c888209b0b962261732b998.png",
    "𝓓𝓻𝓮𝓪𝓶𝓬𝓪𝓽𝓬𝓱𝓮𝓻": "images/SmartSelect_20261113_235729_Chrome.jpg",
    "𝓣𝓱𝓮 𝓞𝓻𝓲𝓰𝓲𝓷 𝓗𝓪𝓷𝓭": "images/SmartSelect_20261114_223837_Chrome.jpg",
}

equipped_backgrounds = {
    "𝓣𝓱𝓮 𝓞𝓻𝓲𝓰𝓲𝓷 𝓗𝓪𝓷𝓭": "Background/SmartSelect_20261114_230443_Chrome.jpg",
    "𝓘𝓬𝓮𝓐𝓰𝓮": "Background/SmartSelect_20261114_105008_NAVER.jpg",
    "𝓜𝓪𝓶𝓶𝓸𝓽𝓱": "Background/SmartSelect_20261114_104343_NAVER.jpg",
    "✧ 𝓗𝔂𝓹𝓮𝓻 𝓟𝓻𝓲𝓼𝓶 ✧": "Background/file_00000000b07c82069ec3c3f543da2f45.png",
    "𝓢𝔂𝓶𝓹𝓱𝓸𝓷𝔂♤": "Background/SmartSelect_20261114_225405_Chrome.jpg",
    "블리자드": "Background/SmartSelect_20261114_104034_NAVER.jpg",
    "이상": "Background/images.jpeg",
    "𝓓𝓻𝓮𝓪𝓶𝓬𝓪𝓽𝓬𝓱𝓮𝓻": "Background/SmartSelect_20261114_000447_Chrome.jpg",
    "𝓢𝓹𝓮𝓬𝓽𝓻𝓪𝓕𝓵𝓸𝔀 𖤐": "Background/SmartSelect_20261113_234652_NAVER.jpg",
    "감시자": "Background/SmartSelect_20261113_234106_Chrome.jpg",
    "༒ 𝕷𝕰𝕁𝕴𝕬𝕿𝕳𝕬𝕹 ༒": "Background/SmartSelect_20261115_022224_Google.jpg",
    "아쿠아리움": "Background/SmartSelect_20261115_022254_Google.jpg",
    "선원": "Background/SmartSelect_20261115_022157_Google.jpg",
    "샤킨": "Background/SmartSelect_20261115_021602_Google.jpg",
    "밤나팔꽃": "Background/SmartSelect_20261115_030923_Google.jpg",
    "묘화": "Background/SmartSelect_20261115_031435_Google.jpg",
    "영혼 사냥꾼": "Background/SmartSelect_20261115_031528_Google.jpg",
    "듀라한": "Background/SmartSelect_20261115_031612_Google.jpg",
    "악몽의 하늘": "Background/SmartSelect_20261115_033218_Google.jpg",
    "수확가": "Background/SmartSelect_20261115_033608_Google.jpg",
    "사도:베일": "Background/SmartSelect_20261115_033436_Google.jpg",
    "크로마틱": "images/SmartSelect_20261113_233022_Google.jpg",
    "자장가": "Background/SmartSelect_20261114_000015_Chrome.jpg",
    "그래피티": "Background/SmartSelect_20261114_171237_Google.jpg",
}

skin_items = [
    "빼빼로데이 2026 (대마법사)",
    "빼빼로데이 2026 (감시자)",
    "빼빼로데이 2026 (카와이)",
]
skin_theme_names = {
    "빼빼로데이 2026 (대마법사)": "빼빼로데이 2026",
    "빼빼로데이 2026 (감시자)": "빼빼로데이 2026",
    "빼빼로데이 2026 (카와이)": "빼빼로데이 2026",
}
skin_images = {
    "빼빼로데이 2026 (대마법사)": "Skin/SmartSelect_20261114_234213_Gallery.jpg",
    "빼빼로데이 2026 (감시자)": "Skin/SmartSelect_20261114_234230_Gallery.jpg",
    "빼빼로데이 2026 (카와이)": "Skin/file_00000000568c8206bd1c2f53ae66e8ca.png",
}
skin_required_aura = {
    "빼빼로데이 2026 (대마법사)": "대마법사",
    "빼빼로데이 2026 (감시자)": "감시자",
    "빼빼로데이 2026 (카와이)": "카와이",
}

aura_to_skins = {
    "대마법사": ["빼빼로데이 2026 (대마법사)"],
    "감시자": ["빼빼로데이 2026 (감시자)"],
    "카와이": ["빼빼로데이 2026 (카와이)"],
}

potion_items = [
    "100배 행운 포션 (1분)", "500배 행운 포션 (30초)",
    "1000배 행운 포션 (15초)", "10000배 행운 포션 (10초)",
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
  normalized_skins = {
      s: min(1, int(st.session_state.get("skins", {}).get(s, 0)))
      for s in skin_items
  }
  return {
      "counts": st.session_state.get("counts", {}),
      "levels": st.session_state.get("levels", {}),
      "titles": st.session_state.get("titles", []),
      "equipped_title": st.session_state.get("equipped_title", None),
      "equipped": st.session_state.get("equipped", None),
      "equipped_skin": st.session_state.get("equipped_skin", None),
      "coins": st.session_state.get("coins", 0),
      "inventory_slots": st.session_state.get("inventory_slots", 50),
      "luck_buff_unlocked": st.session_state.get(
          "luck_buff_unlocked", False
      ),
      "triple_roll_unlocked": st.session_state.get(
          "triple_roll_unlocked", False
      ),
      "five_roll_unlocked": st.session_state.get("five_roll_unlocked", False),
      "potions": st.session_state.get("potions", {}),
      "cases": st.session_state.get("cases", 0),
      "skins": normalized_skins,
      "weather_tickets": st.session_state.get("weather_tickets", 0),
      "weather_offset": st.session_state.get("weather_offset", 0),
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
  st.session_state.equipped_skin = saved_data.get("equipped_skin", None)
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
  st.session_state.cases = saved_data.get("cases", 0)
  st.session_state.skins = {
      s: min(1, int(saved_data.get("skins", {}).get(s, 0))) for s in skin_items
  }
  st.session_state.weather_tickets = saved_data.get("weather_tickets", 0)
  st.session_state.weather_offset = saved_data.get("weather_offset", 0)

  st.session_state.active_potion_mult = 1
  st.session_state.active_potion_end = 0.0
  st.session_state.active_potion_name = None
  st.session_state.million_ticket_active = False
  st.session_state.symphony_buff_ends = []
  st.session_state.symphony_last_minute = None
  st.session_state.last_results = []
  st.session_state.last_luck_mult = 1
  st.session_state.selected_codex = items[0]


if "logged_in" not in st.session_state:
  st.session_state.logged_in = False
if "username" not in st.session_state:
  st.session_state.username = ""
if "symphony_buff_ends" not in st.session_state:
  st.session_state.symphony_buff_ends = []
if "symphony_last_minute" not in st.session_state:
  st.session_state.symphony_last_minute = None
if "weather_tickets" not in st.session_state:
  st.session_state.weather_tickets = 0
if "weather_offset" not in st.session_state:
  st.session_state.weather_offset = 0


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
          time.sleep(0.5)
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
              "equipped_skin": None,
              "coins": 0,
              "inventory_slots": 50,
              "luck_buff_unlocked": False,
              "triple_roll_unlocked": False,
              "five_roll_unlocked": False,
              "potions": {p: 0 for p in potion_items},
              "cases": 0,
              "skins": {s: 0 for s in skin_items},
              "weather_tickets": 0,
              "weather_offset": 0,
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


def update_symphony_golden_melody():
  now = time.time()
  st.session_state.symphony_buff_ends = [
      end_t for end_t in st.session_state.get("symphony_buff_ends", []) if end_t > now
  ]

  if st.session_state.get("equipped") == "𝓢𝔂𝓶𝓹𝓱𝓸𝓷𝔂♤":
    curr_min = int(now // 60)
    last_min = st.session_state.get("symphony_last_minute")

    if last_min is None:
      st.session_state.symphony_last_minute = curr_min
    elif curr_min > last_min:
      elapsed_mins = min(curr_min - last_min, 10)
      for idx in range(elapsed_mins):
        if random.random() < 0.05:
          trigger_time = (last_min + idx + 1) * 60
          end_time = max(now, trigger_time) + 180
          if end_time > now:
            st.session_state.symphony_buff_ends.append(end_time)
            st.toast("🎼 [황금선율 발동!] 3분간 행운 10배 중첩!", icon="🎻")
      st.session_state.symphony_last_minute = curr_min
  else:
    st.session_state.symphony_last_minute = None

  active_stacks = len(st.session_state.symphony_buff_ends)
  symphony_mult = (10 ** active_stacks) if active_stacks > 0 else 1
  max_rem_sec = (
      int(max(st.session_state.symphony_buff_ends) - now)
      if active_stacks > 0
      else 0
  )
  return active_stacks, symphony_mult, max_rem_sec


def get_world_time_status():
  current_time = int(time.time())
  cycle_time = current_time % 360
  is_day = cycle_time < 180
  rem_sec = 180 - (cycle_time % 180)
  return is_day, rem_sec


def get_world_weather_status():
  current_time = int(time.time()) + st.session_state.get("weather_offset", 0)
  
  big_cycle_idx = current_time // 300
  big_rem_sec = 300 - (current_time % 300)
  
  random.seed(big_cycle_idx * 999)
  halloween_chance = 0.002
  eq_now = st.session_state.get("equipped")
  if eq_now in halloween_auras:
    halloween_chance += 0.003

  is_halloween_macro = random.random() < halloween_chance
  random.seed()

  if is_halloween_macro:
    return "halloween_2024", big_rem_sec
  else:
    small_cycle_idx = current_time // 60
    small_rem_sec = 60 - (current_time % 60)

    random.seed(small_cycle_idx)
    sub_roll = random.random()
    if sub_roll < 0.5:
      w_type = "normal"
    elif sub_roll < 0.75:
      w_type = "rain"
    else:
      w_type = "snow"
    random.seed()

    return w_type, small_rem_sec


def apply_equipped_background():
  eq = st.session_state.get("equipped")
  eq_skin = st.session_state.get("equipped_skin")
  bg_path = equipped_backgrounds.get(eq)
  if eq_skin and eq_skin in skin_images:
    bg_path = skin_images[eq_skin]

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


def hex_to_pastel_neon_css(hex_color: str) -> str:
  hex_color = hex_color.lstrip('#')
  if len(hex_color) != 6:
    hex_color = "a855f7"

  r = int(hex_color[0:2], 16) / 255.0
  g = int(hex_color[2:4], 16) / 255.0
  b = int(hex_color[4:6], 16) / 255.0
  h, l, s = colorsys.rgb_to_hls(r, g, b)

  c1 = colorsys.hls_to_rgb((h - 0.12) % 1.0, 0.78, 0.88)
  c2 = colorsys.hls_to_rgb(h, 0.76, 0.92)
  c3 = colorsys.hls_to_rgb((h + 0.12) % 1.0, 0.78, 0.88)

  def to_hex(rgb):
    return "#{:02x}{:02x}{:02x}".format(
        int(rgb[0] * 255), int(rgb[1] * 255), int(rgb[2] * 255)
    )

  hex1, hex2, hex3 = to_hex(c1), to_hex(c2), to_hex(c3)

  return (
      f"background: linear-gradient(90deg, {hex1}, {hex2}, {hex3}); "
      f"-webkit-background-clip: text; "
      f"-webkit-text-fill-color: transparent; "
      f"font-weight: 900; "
      f"filter: drop-shadow(0 0 9px {hex2}aa); "
      f"font-size: 1.06em; padding: 0 4px;"
  )


def get_styled_title_html(title_name):
  if not title_name:
    return ""

  halloween_titles = [
      "𓆩 𝓟𝓾𝓶𝓹 𓆪", "𓆩 𝕽𝖚𝓷𝖊 𝕶𝓷𝓲𝓰𝓱𝓽 𓆪", "𓆩 𝓥𝓲𝓽𝓪𝓵 𓆪",
      "𓆩 𝓜𝓸𝓸𝓷𝓯𝓵𝓸𝔀𝓮𝓻 𓆪", "𓆩 𝓜𝔂𝓸𝓱𝔀𝓪 𓆪", "𓆩 𝕾𝖔𝖚𝖑 𝕳𝓾𝓷𝖙𝖊𝓻 𓆪", "𓆩 𝓓𝓾𝓵𝓵𝓪𝓱𝓪𝓷 𓆪",
      "𓆩 𝕯𝖗𝖊𝖆𝓶 𝕺𝓕 𝕹𝖎𝖌𝖍𝖙𝖒𝖆𝓻𝓮 𓆪", "𓆩 𝕾𝖔𝖚𝖑 𝕳𝖆𝖗𝖛𝖊𝖘𝓽𝖊𝖗 𓆪", "𓆩 𝕳𝖊𝖗𝖆𝖑𝕯 𝕺𝓯 𝕿𝕍𝖊𝖎𝖑 𓆪",
      "꧁༺ 🎃𝕾𝖔𝓿𝖊𝓻𝖊𝖎𝓰𝓷 𝕺𝓋 𝕰𝖙𝖊𝓻𝓷𝖆𝖑 𝕯𝖆𝖗𝖐𝓷𝖊𝖘𝖘🎃 ༻꧂",
      "꧁༺ 🎃𝕿𝖍𝖊 𝕱𝖎𝖓𝖆𝖑 𝕽𝖊𝖆𝓟𝖊𝖗🎃 ༻꧂",
      "꧁༺ 🎃𝕯𝖎𝖛𝖎𝖓𝖊 𝕬𝖗𝖇𝖎𝖙𝖊𝖗 𝕺𝓋 𝕿𝖍𝖊 𝕁𝖔𝖎𝓭🎃 ༻꧂"
  ]
  if title_name in halloween_titles:
    return f'<span style="background: linear-gradient(90deg, #ff6600, #ff9900, #ffcc00); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 900; text-shadow: 0 0 12px rgba(255,102,0,0.7); font-size: 1.08em; padding: 0 4px;">{title_name}</span>'

  rainbow_max_titles = [
      "𓆩 𝓣𝓱𝓮 𝓞𝓶𝓷𝓲𝓹𝓸𝓽𝓮𝓷𝓽 𓆪",
      "𓆩 𝓔𝓽𝓮𝓻𝓷𝓪𝓵 𝓞𝓶𝓷𝓲𝓬𝓱𝓻𝓸𝓶𝓪 𓆪",
      "𓆩 𝓔𝓽𝓮𝓻𝓷𝓪𝓵 𝓢𝔂𝓶𝓹𝓱𝓸𝓷𝔂 𓆪",
      "𓆩 𝓟𝓻𝓲𝓼𝓶 𓆪",
      "꧁༺ 𝐀𝐍𝐂𝐈𝐄𝐍𝐓 𝙆𝐈𝐍𝙶 ༻꧂",
      "꧁༺ 𝐆𝐎𝐃 𝐎𝐅 𝐈𝗖𝐄 ༻꧂",
      "꧁༺ 𝐋𝐎𝐑𝐃 𝐎𝐅 𝐃𝐑𝐄𝐀𝐌𝐒 ༻꧂",
      "🌊🔱 𝐋𝐎𝐑𝐃 𝐎𝐅 𝐓𝐇𝐄 𝐀𝐁𝐘𝐒𝐒 🔱🌊",
      "🌊✨ 𝐏𝐑𝐈𝐌𝐎𝐑𝐃𝐈𝐀𝐋 𝐀𝐁𝐘𝐒𝐒 ✨🌊",
      "𓆩 𝕺𝖗𝓲g𝓲𝓷 𝕾𝓹𝖆𝓻𝚔 𓆪",
      "𓆩 𝕬𝓹𝓱𝓪𝓷𝓽 𓆪",
  ]
  if title_name in rainbow_max_titles:
    return f'<span style="background: linear-gradient(90deg, #ff0000, #ff7f00, #ffff00, #00ff00, #00ffff, #0077ff, #9b00ff); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 900; text-shadow: 0 0 12px rgba(255,255,255,0.65), 0 0 22px rgba(255,0,255,0.5); font-size: 1.08em; padding: 0 4px;">{title_name}</span>'

  if "𝓓𝓲𝓿𝓲𝓷𝓮 𝓒𝓻𝓮𝓪𝓽𝓸𝓻" in title_name:
    style = hex_to_pastel_neon_css(aura_colors["𝓣𝓱𝓮 𝓞𝓻𝓲𝓰𝓲𝓷 𝓗𝓪𝓷𝓭"])
  elif "𝓞𝓻𝓬𝓱𝓮𝓼𝓽𝓻𝓪𝓵 𝓜𝓪𝓮𝓼𝓽𝓻𝓸" in title_name:
    style = hex_to_pastel_neon_css(aura_colors["𝓢𝔂𝓶𝓹𝓱𝓸𝓷𝔂♤"])
  elif "𝓟𝓻𝓲𝓼𝓶𝓪𝓽𝓲𝓬 𝓓𝓮𝓲𝓽𝔂" in title_name:
    style = hex_to_pastel_neon_css(aura_colors["✧ 𝓗𝔂𝓹𝓮𝓻 𝓟𝓻𝓲𝓼𝓶 ✧"])
  elif "LEVIATHAN" in title_name or "𝐀𝐁𝐘𝐒𝐒" in title_name or "PRIMORDIAL" in title_name:
    style = hex_to_pastel_neon_css(aura_colors["༒ 𝕷𝕰𝕁𝕴𝕬𝕿𝕳𝕬𝕹 ༒"])
  elif "ICE MONARCH" in title_name or "𝐀𝐍𝐂𝐈𝐄𝐍𝐓" in title_name:
    style = hex_to_pastel_neon_css(aura_colors["𝓜𝓪𝓶𝓶𝓸𝓽𝓱"])
  elif "FROST EMPEROR" in title_name or "𝐆𝐎𝐃" in title_name:
    style = hex_to_pastel_neon_css(aura_colors["𝓘𝓬𝓮𝓐𝓰𝓮"])
  elif "무한의 환상" in title_name:
    style = hex_to_pastel_neon_css(aura_colors["𝓓𝓻𝓮𝓪𝓶𝓬𝓪𝓽𝓬𝓱𝓮𝓻"])
  elif "영광의 잔광" in title_name:
    style = hex_to_pastel_neon_css(aura_colors["𝓢𝓹𝓮𝓬𝓽𝓻𝓪𝓕𝓵𝓸𝔀 𖤐"])
  else:
    style = "color: #ffeb3b; font-weight: bold; text-shadow: 0 0 6px rgba(0,0,0,0.9), 0 0 12px rgba(255,235,59,0.5); font-size: 1.02em; padding: 0 4px;"

  return f'<span style="{style}">{title_name}</span>'


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

  _, sym_mult, _ = update_symphony_golden_melody()
  mult *= sym_mult

  if st.session_state.luck_buff_unlocked and (next_pull_number % 10 == 0):
    mult *= 2

  equipped_now = st.session_state.get("equipped")

  if equipped_now == "수확가":
    harvest_stacks = next_pull_number // 100
    if harvest_stacks > 0:
      mult *= (2 ** harvest_stacks)

  if equipped_now == "악몽의 하늘":
    if "nightmare_turn" not in st.session_state:
      st.session_state.nightmare_turn = 1
    
    turn = st.session_state.nightmare_turn
    triggered = False
    if turn >= 3:
      triggered = True
    else:
      if random.random() < 0.01 or random.random() < 0.5:
        triggered = True

    if triggered:
      if turn == 1:
        mult *= 10
        st.toast("🎃 [악몽의 하늘 발동!] 1턴 성공! 행운 10배 폭증!", icon="🌌")
      elif turn == 2:
        mult *= 100
        st.toast("🎃 [악몽의 하늘 발동!] 2턴 성공! 행운 100배 폭증!", icon="🌌")
      else:
        mult *= 1000
        st.toast("🎃 [악몽의 하늘 발동!] 3턴 성공! 행운 1000배 폭증!", icon="🌌")
      st.session_state.nightmare_turn = 1
    else:
      st.session_state.nightmare_turn += 1

  biome_type, _ = get_world_weather_status()
  if biome_type == "snow" and equipped_now == "𝓘𝓬𝓮𝓐𝓰𝓮":
    mult *= 10

  is_day, _ = get_world_time_status()
  if not is_day and equipped_now == "𝓓𝓻𝓮𝓪𝓶𝓬𝓪𝓽𝓬𝓱𝓮𝓻":
    mult *= 10

  return mult


def play_fullscreen_star_cutscene(aura_name):
  placeholder = st.empty()

  if aura_name == "𝓣𝓱𝓮 𝓞𝓻𝓲𝓰𝓲𝓷 𝓗𝓪𝓷𝓭":
    star_color = "#ffd700"
    bg_style = "radial-gradient(circle, #3d2b00 0%, #080500 90%)"
    star_symbol = "🖐️✨🌌👑"
    ment = "🖐️ [THE ORIGIN HAND] 태초의 창조주가 손을 뻗어 우주의 모든 법칙과 운명을 새롭게 빚어냅니다!"
    duration = 5.0
  elif aura_name == "사도:베일":
    star_color = "#ff3366"
    bg_style = "radial-gradient(circle, #33001a 0%, #080005 90%)"
    star_symbol = "🎃👁️"
    ment = "🎃 [사도:베일] 공허의 베일 속에서 찬란한 심판의 눈동자가 떠오릅니다!"
    duration = 4.8
  elif aura_name == "수확가":
    star_color = "#ff6600"
    bg_style = "radial-gradient(circle, #331100 0%, #080200 90%)"
    star_symbol = "🎃🗡️"
    ment = "🎃 [수확가] 종말의 낫이 휘둘러지며 영혼의 거대한 수확이 시작됩니다!"
    duration = 4.8
  elif aura_name == "악몽의 하늘":
    star_color = "#9900cc"
    bg_style = "radial-gradient(circle, #220033 0%, #05000a 90%)"
    star_symbol = "🎃🌌"
    ment = "🎃 [악몽의 하늘] 뒤틀린 밤하늘의 공포가 온 세상의 시공간을 잠식합니다!"
    duration = 4.8
  elif aura_name == "༒ 𝕷𝕰𝕁𝕴𝕬𝕿𝕳𝕬𝕹 ༒":
    star_color = "#00ffff"
    bg_style = "radial-gradient(circle, #001a33 0%, #000308 90%)"
    star_symbol = "🌊🐉🌀"
    ment = "🌊 [LEVIATHAN] 심해의 절대 군주가 깨어나 세상 모든 것을 포식할 파도를 일으킵니다!"
    duration = 4.8
  else:
    star_color = "#ff6600"
    bg_style = "radial-gradient(circle, #331100 0%, #080200 90%)"
    star_symbol = "🎃"
    ment = f"🎃 [{aura_name}] 할로윈 2024의 어둠과 마법이 깨어납니다!"
    duration = 3.5

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


def get_level_requirements(item_name, denom):
  if item_name in halloween_auras:
    return {1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 7, 7: 10}

  if denom > 100000000:
    return {1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 10, 7: 100}
  elif denom >= 1000000:
    return {1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 10, 7: 100}
  elif denom > 100000:
    return {1: 1, 2: 30, 3: 50, 4: 100, 5: 500, 6: 1000, 7: 1500}
  else:
    return {1: 1, 2: 10, 3: 20, 4: 30, 5: 50, 6: 100, 7: 300}


def perform_rolls(roll_count=1):
  results = []
  max_luck_applied = 1
  equipped_now = st.session_state.get("equipped")
  coin_gain_per_roll = 10 if equipped_now == "𝓢𝓹𝓮𝓬𝓽𝓻𝓪𝓕𝓵𝓸𝔀 𖤐" else 5
  biome_type, _ = get_world_weather_status()
  is_day, _ = get_world_time_status()

  prior_counts = {item: st.session_state.counts.get(item, 0) for item in items}

  for _ in range(roll_count):
    next_pull = sum(st.session_state.counts.values()) + 1
    luck_mult = get_current_luck_multiplier(next_pull)
    max_luck_applied = max(max_luck_applied, luck_mult)

    if st.session_state.million_ticket_active:
      st.session_state.million_ticket_active = False

    if equipped_now == "사도:베일" and random.random() < 0.001:
      p500_name = "500배 행운 포션 (30초)"
      st.session_state.potions[p500_name] = st.session_state.potions.get(p500_name, 0) + 1
      st.toast("🎃 [사도:베일 능력 발동!] 뽑기 중 500배 행운 포션 (30초)을 획득했습니다!", icon="🧪")

    current_weights = list(base_weights)

    if equipped_now == "✧ 𝓗𝔂𝓹𝓮𝓻 𝓟𝓻𝓲𝓼𝓶 ✧":
      current_weights[items.index("크로마틱")] *= 2

    if is_day:
      current_weights[items.index("태양")] *= 10
    else:
      current_weights[items.index("달")] *= 10
      current_weights[items.index("황혼")] *= 10
      current_weights[items.index("자장가")] *= 10
      current_weights[items.index("𝓓𝓻𝓮𝓪𝓶𝓬𝓪𝓽𝓬𝓱𝓮𝓻")] *= 2

    if biome_type == "snow":
      current_weights[items.index("빙하")] *= 3
      current_weights[items.index("만년서리")] *= 3
      current_weights[items.index("블리자드")] *= 3
      current_weights[items.index("𝓜𝓪𝓶𝓶𝓸𝓽𝓱")] *= 2
      current_weights[items.index("𝓘𝓬𝓮𝓐𝓰𝓮")] *= 2
    elif biome_type == "rain":
      current_weights[items.index("에바네샌트")] *= 4
      current_weights[items.index("포세이돈")] *= 4
      current_weights[items.index("샤킨")] *= 4
      current_weights[items.index("선원")] *= 4
      current_weights[items.index("아쿠아리움")] *= 4
      current_weights[items.index("༒ 𝕷𝕰𝕁𝕴𝕬𝕿𝕳𝕬𝕹 ༒")] *= 2
    
    if biome_type != "halloween_2024":
      for h_aura in halloween_auras:
        current_weights[items.index(h_aura)] = 0

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

    if equipped_now == "༒ 𝕷𝕰𝕁𝕴𝕬𝕿𝕳𝕬𝕹 ༒" and random.random() < 0.005:
      eligible_predators = [it for it in items if denominators[it] >= 1000000]
      if eligible_predators:
        result = random.choice(eligible_predators)
      st.toast("🌊 [절대포식 발동!] 리바이어던이 뽑기 결과를 집어삼키고 백만배 행운을 발동시켰습니다!", icon="🐉")

    results.append(result)

    if (
        prior_counts.get(result, 0) == 0
        and st.session_state.counts.get(result, 0) == 0
    ):
      first_get_titles = {
          "사도:베일": "𓆩 𝕳𝖊𝖗𝖆𝖑𝕯 𝕺𝓯 𝕿𝕍𝖊𝖎𝖑 𓆪",
          "수확가": "𓆩 𝕾𝖔𝖚𝖑 𝕳𝖆𝖗𝖛𝖊𝖘𝓽𝖊𝖗 𓆪",
          "악몽의 하늘": "𓆩 𝕯𝖗𝓮𝖆𝓶 𝕺𝓕 𝕹𝖎𝖌𝖍𝖙𝖒𝖆𝓻𝓮 𓆪",
          "𝓢𝓹𝓮𝓬𝓽𝓻𝓪𝓕𝓵𝓸𝔀 𖤐": "영광의 잔광",
          "𝓢𝔂𝓶𝓹𝓱𝓸𝓷𝔂♤": "◇𝓞𝓻𝓬h𝓮𝓼𝓽𝓻𝓪𝓵 𝓜𝓪𝓮𝓼𝓽𝓻𝓸 ◇",
          "✧ 𝓗𝔂𝓹𝓮𝓻 𝓟𝓻𝓲𝓼𝓶 ✧": "𓆩 𝓟𝓻𝓲𝓼𝓶𝓪𝓽𝓲𝓬 𝓓𝓮𝓲𝓽𝔂 𓆪",
          "༒ 𝕷𝕰𝕁𝕴𝕬𝕿𝕳𝕬𝕹 ༒": "🌊✨ 𝐏𝐑𝐈𝐌𝐎𝐑𝐃𝐈𝐀𝐋 𝐀𝐁𝐘𝐒𝐒 ✨🌊",
          "𝓓𝓻𝓮𝓪𝓶𝓬𝓪𝓽𝓬𝓱𝓮𝓻": "• ⋆༺무한의 환상༻⋆",
          "𝓜𝓪𝓶𝓶𝓸𝓽𝓱": "❄ 𝐈𝐂𝐄 𝐌𝐎𝐍𝐀𝐑𝐂𝐇 ❄",
          "𝓘𝓬𝓮𝓐𝓰𝓮": "♛ 𝐅𝐑𝐎𝐒𝐓 𝐄𝐌𝐏𝐄𝐑𝐎𝐑 ♛",
          "𝓣𝓱𝓮 𝓞𝓻𝓲𝓰𝓲𝓷 𝓗𝓪𝓷𝓭": "◇𝓓𝓲𝓿𝓲𝓷𝓮 𝓒𝓻𝓮𝓪𝓽𝓸𝓻 ◇",
      }
      if result in first_get_titles:
        t_name = first_get_titles[result]
        if t_name not in st.session_state.titles:
          st.session_state.titles.append(t_name)

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


st.title("✨ 아우라 가챠 & 도감 시스템")

c_u1, c_u2 = st.columns([4, 1])
with c_u1:
  eq_title = st.session_state.get("equipped_title")
  styled_title_html = (
      f" &nbsp; [{get_styled_title_html(eq_title)}]" if eq_title else ""
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

sym_stacks, sym_mult, sym_rem_sec = update_symphony_golden_melody()

is_day_now, time_rem_sec = get_world_time_status()
t_min = time_rem_sec // 60
t_sec = time_rem_sec % 60

biome_type, biome_rem_sec = get_world_weather_status()
b_min = biome_rem_sec // 60
b_sec = biome_rem_sec % 60

is_mammoth_equipped = st.session_state.get("equipped") == "𝓜𝓪𝓶𝓶𝓸𝓽𝓱"
is_ia_equipped = st.session_state.get("equipped") == "𝓘𝓬𝓮𝓐𝓰𝓮"
is_dc_equipped = st.session_state.get("equipped") == "𝓓𝓻𝓮𝓪𝓶𝓬𝓪𝓽𝓬𝓱𝓮𝓻"
is_hween_equipped = st.session_state.get("equipped") in halloween_auras

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

if biome_type == "halloween_2024":
  h_boost = " | 🎃 할로윈 아우라 장착 중: 바이옴 확률 +0.3% 적용!" if is_hween_equipped else ""
  st.markdown(
      f"""
        <div style="background: linear-gradient(90deg, #ff6600, #331100); padding: 10px; border-radius: 8px; text-align: center; color: white; font-weight: bold; font-size: 16px; margin-bottom: 15px; box-shadow: 0 0 14px rgba(255,102,0,0.7);">
            🎃 [현재 바이옴: 할로윈 2024] (5분 유지 / 할로윈 전용 아우라 10종 출현 가능!) (남은 시간: {b_min}분 {b_sec}초){h_boost}
        </div>
        """,
      unsafe_allow_html=True,
  )
elif biome_type == "snow":
  ia_text = " | ❄️ 𝓘𝓬𝓮𝓐𝓰𝓮 장착 중: 행운 10배!" if is_ia_equipped else ""
  st.markdown(
      f"""
        <div style="background: linear-gradient(90deg, #004080, #0080ff); padding: 10px; border-radius: 8px; text-align: center; color: white; font-weight: bold; font-size: 16px; margin-bottom: 15px; box-shadow: 0 0 10px rgba(0,191,255,0.4);">
            🌨️ [현재 날씨: 눈] (1분마다 랜덤 전환 / 할로윈 아우라 출현 불가) (남은 시간: {b_sec}초){ia_text}
        </div>
        """,
      unsafe_allow_html=True,
  )
elif biome_type == "rain":
  st.markdown(
      f"""
        <div style="background: linear-gradient(90deg, #00334d, #006699); padding: 10px; border-radius: 8px; text-align: center; color: white; font-weight: bold; font-size: 16px; margin-bottom: 15px; box-shadow: 0 0 10px rgba(0,153,255,0.4);">
            🌧️ [현재 날씨: 비] (1분마다 랜덤 전환 / 할로윈 아우라 출현 불가) (남은 시간: {b_sec}초)
        </div>
        """,
      unsafe_allow_html=True,
  )
else:
  m_text = " | 🦣 𝓜𝓪𝓶𝓶𝓸𝓽𝓱 장착 중: 눈 확률 +15%!" if is_mammoth_equipped else ""
  h_boost = " | 🎃 할로윈 아우라 장착 중: 바이옴 확률 +0.3% 적용!" if is_hween_equipped else ""
  st.markdown(
      f"""
        <div style="background: linear-gradient(90deg, #333333, #555555); padding: 10px; border-radius: 8px; text-align: center; color: white; font-weight: bold; font-size: 16px; margin-bottom: 15px; box-shadow: 0 0 10px rgba(100,100,100,0.4);">
            ⛅ [현재 날씨: 일반] (1분마다 랜덤 전환 / 할로윈 아우라 출현 불가) (남은 시간: {b_sec}초){m_text}{h_boost}
        </div>
        """,
      unsafe_allow_html=True,
  )

if sym_stacks > 0:
  s_min = sym_rem_sec // 60
  s_sec = sym_rem_sec % 60
  st.markdown(
      f"""
        <div style="background: linear-gradient(90deg, #b8860b, #ffd700); padding: 10px; border-radius: 8px; text-align: center; color: black; font-weight: bold; font-size: 16px; margin-bottom: 15px; box-shadow: 0 0 14px rgba(255,215,0,0.6);">
            🎼 [황금선율 {sym_stacks}중첩 활성화!] 현재 행운 {sym_mult:,}배 적용 중! (최대 남은 시간: {s_min}분 {s_sec}초)
        </div>
        """,
      unsafe_allow_html=True,
  )

with st.container(border=True):
  st.markdown("### 👤 현재 장착 중인 아우라 / 스킨")
  equipped_aura = st.session_state.get("equipped")
  equipped_skin = st.session_state.get("equipped_skin")

  c_eq1, c_eq2 = st.columns(2)
  with c_eq1:
    st.write("**[아우라]**")
    if equipped_aura and equipped_aura in items:
      st.markdown(f"✨ **{equipped_aura}**")
      if st.button("❌ 아우라 장착 해제", key="top_unequip_btn"):
        st.session_state.equipped = None
        save_user_data_to_db()
        st.rerun()
    else:
      st.caption("장착된 아우라 없음")

  with c_eq2:
    st.write("**[스킨]**")
    if equipped_skin and equipped_skin in skin_images:
      st.markdown(f"🎨 **{equipped_skin}**")
      if st.button("❌ 스킨 장착 해제", key="top_unequip_skin_btn"):
        st.session_state.equipped_skin = None
        save_user_data_to_db()
        st.rerun()
    else:
      st.caption("장착된 스킨 없음")

col_c1, col_c2 = st.columns(2)
with col_c1:
  st.metric(label="💰 보유 코인", value=f"{st.session_state.coins} G")
with col_c2:
  total_pulls = sum(st.session_state.counts.values())
  st.metric(label="🎲 총 뽑기 횟수", value=f"{total_pulls}회")

st.divider()

tab_gacha, tab_cases, tab_inventory, tab_potions, tab_codex, tab_titles, tab_shop = st.tabs(
    ["🎲 아우라 뽑기", "🎁 케이스", "🎒 스토리지", "🧪 포션 인벤토리", "📖 도감 (Codex)", "🎖️ 칭호 칸", "🛒 상점"]
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

  has_origin_hand = st.session_state.get("equipped") == "𝓣𝓱𝓮 𝓞𝓻𝓲𝓰𝓲𝓷 𝓗𝓪𝓷𝓭"
  has_triple = st.session_state.get("triple_roll_unlocked", False)
  has_five = st.session_state.get("five_roll_unlocked", False)

  if has_origin_hand:
    col_b1, col_b2 = st.columns(2)
    with col_b1:
      if st.button("🎲 1회 무료 뽑기", type="secondary", use_container_width=True):
        perform_rolls(1)
        st.rerun()
    with col_b2:
      if st.button(
          "🖐️ [운명조작] 10회 연속 뽑기 (+50 G)",
          type="primary",
          use_container_width=True,
      ):
        perform_rolls(10)
        st.rerun()
  elif has_five:
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
            <span style="font-size: 24px; font-weight: bold;">
                {result_badges} 획득!
            </span>
            <p style="color: #ffd700; margin-top: 8px;">(+ {earned_coins} 코인 획득)</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with tab_cases:
  st.subheader("🎁 케이스 오픈 시스템")
  st.write("100배 행운 포션 10개로 **케이스 1개**를 구매할 수 있으며, 케이스를 열어 한정 스킨이나 500배 포션을 획득할 수 있습니다!")

  if "cases" not in st.session_state:
    st.session_state.cases = 0
  if "skins" not in st.session_state:
    st.session_state.skins = {s: 0 for s in skin_items}

  current_p100_count = st.session_state.potions.get("100배 행운 포션 (1분)", 0)
  current_cases = st.session_state.cases

  col_cc1, col_cc2 = st.columns(2)
  with col_cc1:
    st.metric(label="🧪 보유 중인 100배 포션", value=f"{current_p100_count}개")
  with col_cc2:
    st.metric(label="🎁 보유 중인 케이스", value=f"{current_cases}개")

  st.divider()

  col_buy_case, col_open_case = st.columns(2)

  with col_buy_case:
    st.markdown("### 🛒 케이스 구매")
    st.write("• 재료: **100배 행운 포션 10개** = 케이스 1개")
    can_buy_case = current_p100_count >= 10
    if st.button("🎁 케이스 1개 구매하기", type="primary", use_container_width=True, disabled=not can_buy_case):
      st.session_state.potions["100배 행운 포션 (1분)"] -= 10
      st.session_state.cases += 1
      save_user_data_to_db()
      st.success("🎉 케이스 1개를 성공적으로 구매했습니다!")
      st.rerun()

  with col_open_case:
    st.markdown("### 🔓 케이스 오픈")
    st.write("• 확률: **꽝 70%** / **500배 포션 20%** / **스킨 10%**")
    can_open_case = current_cases >= 1
    if st.button("🔓 케이스 1개 열기", type="secondary", use_container_width=True, disabled=not can_open_case):
      st.session_state.cases -= 1
      
      roll_val = random.random()
      if roll_val < 0.70:
        st.session_state.last_case_result = ("꽝", "❌ 꽝입니다! 아무것도 나오지 않았습니다.")
      elif roll_val < 0.90:
        p500_name = "500배 행운 포션 (30초)"
        st.session_state.potions[p500_name] = st.session_state.potions.get(p500_name, 0) + 1
        st.session_state.last_case_result = ("포션", f"🧪 [500배 행운 포션 (30초)] 1개를 획득했습니다!")
      else:
        won_skin = random.choice(skin_items)
        already_owned = st.session_state.skins.get(won_skin, 0) >= 1
        st.session_state.skins[won_skin] = 1
        if already_owned:
          st.session_state.last_case_result = ("스킨", f"🎨 스킨 [{won_skin}]이(가) 등장했습니다! (이미 보유 중)")
        else:
          st.session_state.last_case_result = ("스킨", f"🎨 스킨 [{won_skin}]을(를) 획득했습니다!")
          st.balloons()

      save_user_data_to_db()
      st.rerun()

  if "last_case_result" in st.session_state:
    res_type, res_msg = st.session_state.last_case_result
    bg_col = "#2a2a2a" if res_type == "꽝" else ("#004d40" if res_type == "포션" else "#4a148c")
    st.markdown(
        f"""
        <div style="text-align: center; padding: 18px; background-color: {bg_col}; color: white; border-radius: 10px; margin-top: 20px; font-size: 20px; font-weight: bold;">
            {res_msg}
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
      f"📦 아우라 스토리지 [보유 종류: {len(owned_items)} / {len(items)}]"
  )
  st.write(
      "아우라 카드를 확인하고 장착, 레벨업 또는 **전용 스킨 장착**을 진행하세요."
  )

  if owned_items:
    if "levels" not in st.session_state:
      st.session_state.levels = {item: 1 for item in items}

    cols_per_row = 5
    for i in range(0, len(owned_items), cols_per_row):
      row_items = owned_items[i : i + cols_per_row]
      grid_cols = st.columns(cols_per_row)

      for idx, item in enumerate(row_items):
        count = st.session_state.counts.get(item, 0)
        lvl = st.session_state.levels.get(item, 1)
        is_equipped = st.session_state.get("equipped") == item

        denom = denominators.get(item, 2)
        reqs = get_level_requirements(item, denom)
        next_req = reqs[lvl + 1] if lvl + 1 <= 7 else reqs[7]

        with grid_cols[idx]:
          with st.container(border=True):
            st.markdown(
                f"<div style='text-align:center; font-size:30px;'>{icons.get(item, '✨')}</div>",
                unsafe_allow_html=True,
            )
            st.markdown(
                f"<div style='text-align:center; font-size:13px; font-weight:bold; word-break:keep-all; min-height:38px;'>[{item}]</div>",
                unsafe_allow_html=True,
            )
            
            if lvl < 7:
              st.markdown(
                  f"<div style='text-align:center; font-size:11px; color:#aaa; margin-bottom:5px;'>Lv.{lvl} ({count}/{next_req})</div>",
                  unsafe_allow_html=True,
              )
            else:
              st.markdown(
                  f"<div style='text-align:center; font-size:11px; color:#ffd700; margin-bottom:5px;'>⭐ MAX Lv.6</div>",
                  unsafe_allow_html=True,
              )

            if is_equipped:
              st.markdown(
                  "<div"
                  " style='text-align:center; font-size:12px; color:#00ffcc;"
                  " margin-bottom:5px;'><b>[장착중]</b></div>",
                  unsafe_allow_html=True,
              )
            else:
              if st.button("장착", key=f"grid_eq_{item}", use_container_width=True):
                st.session_state.equipped = item
                save_user_data_to_db()
                st.rerun()

            if lvl < 7:
              can_upgrade = count >= next_req
              if st.button(
                  f"업그레이드" if can_upgrade else f"재료 부족",
                  key=f"grid_lvl_{item}",
                  use_container_width=True,
                  type="primary" if can_upgrade else "secondary",
                  disabled=not can_upgrade
              ):
                st.session_state.counts[item] -= next_req
                st.session_state.levels[item] += 1
                new_lvl = st.session_state.levels[item]
                if new_lvl == 7:
                  custom_max_titles = {
                      "𝓣𝓱𝓮 𝓞𝓻𝓲𝓰𝓲𝓷 𝓗𝓪𝓷𝓭": "𓆩 𝓣𝓱𝓮 𝓞𝓶𝓷𝓲𝓹𝓸𝓽𝓮𝓷𝓽 𓆪",
                      "𝓓𝓻𝓮𝓪𝓶𝓬𝓪𝓽𝓬𝓱𝓮𝓻": "꧁༺ 𝐋𝐎𝐑𝐃 𝐎𝐅 𝐃𝐑𝐄𝐀𝐌𝐒 ༻꧂",
                      "사도:베일": "꧁༺ 🎃𝕯𝖎𝖛𝖎𝖓𝖊 𝕬𝖗𝖇𝖎𝖙𝖊𝖗 𝕺𝓋 𝕿𝖍𝖊 𝕁𝖔𝖎𝓭🎃 ༻꧂",
                      "수확가": "꧁༺ 🎃𝕿𝖍𝖊 𝕱𝖎𝖓𝖆𝖑 𝕽𝖊𝖆𝓟𝖊𝖗🎃 ༻꧂",
                      "악몽의 하늘": "꧁༺ 🎃𝕾𝖔𝓿𝖊𝓻𝖊𝖎𝓰𝓷 𝕺𝓋 𝕰𝖙𝖊𝓻𝓷𝖆𝖑 𝕯𝖆𝖗𝖐𝓷𝖊𝖘𝖘🎃 ༻꧂",
                      "༒ 𝕷𝕰𝕁𝕴𝕬𝕿𝕳𝕬𝕹 ༒": "🌊🔱 𝐋𝐎𝐑𝐃 𝐎𝐅 𝐓𝐇𝐄 𝐀𝐁𝐘𝐒𝐒 🔱🌊",
                      "✧ 𝓗𝔂𝓹𝓮𝓻 𝓟𝓻𝓲𝓼𝓶 ✧": "𓆩 𝓔𝓽𝓮𝓻𝓷𝓪𝓵 𝓞𝓶𝓷𝓲𝓬𝓱𝓻𝓸𝓶𝓪 𓆪",
                      "𝓢𝔂𝓶𝓹𝓱𝓸𝓷𝔂♤": "𓆩 𝓔𝓽𝓮𝓻𝓷𝓪𝓵 𝓢𝔂𝓶𝓹𝓱𝓸𝓷𝔂 𓆪",
                      "𝓢𝓹𝓮𝓬𝓽𝓻𝓪𝓕𝓵𝓸𝔀 𖤐": "𓆩 𝓟𝓻𝓲𝓼𝓶 𓆪",
                      "감시자": "𓆩 𝓦𝓪𝓽𝓬𝓱𝓮𝓻 𓆩",
                      "아쿠아리움": "𓆩 𝓐𝓺𝓾𝓪𝓻𝓲𝓾𝓶 𓆪",
                      "선원": "𓆩 𝓢𝓪𝓲𝓵𝓸𝓻 𓆩",
                      "샤킨": "𓆩 𝕾𝖍𝖆𝖗𝖐𝖎𝓷 𓆩",
                      "포세이돈": "𓆩 𝕻𝖔𝖘𝖊𝖎𝕉𝖔𝓷 𓆪",
                      "에바네샌트": "𓆩 𝓔𝓿𝓪𝓷𝓮𝓼𝓬𝓮𝓷𝓽 𓆩",
                      "기원": "𓆩 𝕺𝖗𝓲g𝓲𝓷 𝕾𝓹𝖆𝓻𝚔 𓆪",
                      "망령": "𓆩 𝕬𝓹𝓱𝓪𝓷𝓽 𓆪",
                      "듀라한": "𓆩 𝓓𝓾𝓵𝓵𝓪𝓱𝓪𝓷 𓆪",
                      "영혼 사냥꾼": "𓆩 𝕾𝖔𝖚𝖑 𝕳𝖚𝓷ⵜ𝖊𝓻 𓆪",
                      "묘화": "𓆩 𝓜𝔂𝓸𝓱𝔀𝓪 𓆪",
                      "밤나팔꽃": "𓆩 𝓜𝓸𝓸𝓷𝓯𝓵𝓸𝔀𝓮𝓻 𓆪",
                      "바이탈": "𓆩 𝓥𝓲𝓽𝓪𝓵 𓆪",
                      "룬(나이트)": "𓆩 𝕽𝖚𝓷𝖊 𝕶𝓷𝓲𝓰𝓱𝓽 𓆪",
                      "펌프": "𓆩 𝓟𝓾𝓶𝓹 𓆪",
                      "크로마틱": "𓆩 𝓒𝓱𝓻𝓸𝓶𝓪𝓽𝓲𝓬 𓆪",
                      "자장가": "𓆩 𝓛𝓾𝓵𝓵𝓪𝓫𝔂 𓆩",
                      "그래피티": "𓆩 𝓖𝓻𝓪𝓯𝓯𝓲𝓽𝓲 𓆩",
                      "블리자드": "𓆩 𝓑𝓵𝓲𝔃𝔃𝓪𝓻𝓭 𓆩",
                      "이상": "◇𝓑𝓮𝔂𝓸𝓷𝓭 𝓡𝓮𝓪𝓵𝓲𝓽𝔂 ◇",
                      "헬리오스": "◇𝓗𝓮𝓵𝓲𝓸𝓼 ◇",
                      "속력": "◇𝓥𝓮𝓵𝓸𝓬𝓲𝓽𝔂◇",
                      "황혼": "◇𝓣𝔀𝓲𝓵𝓲𝓰𝓱𝓽 ◇",
                      "아파타이트": "◇𝓐𝓹𝓪𝓽𝓲𝓽𝓮 ◇",
                      "𝓜𝓪𝓶𝓶𝓸𝓽𝓱": "꧁༺ 𝐀𝐍𝐂𝐈𝐄𝐍𝐓 𝙆𝐈𝐍𝙶 ༻꧂",
                      "𝓘𝓬𝓮𝓐𝓰𝓮": "꧁༺ 𝐆𝐎𝐃 𝐎𝐅 𝐈𝗖𝐄 ༻꧂",
                  }
                  t_name = custom_max_titles.get(item, f"{item}의 달인")
                  if "titles" not in st.session_state:
                    st.session_state.titles = []
                  if t_name not in st.session_state.titles:
                    st.session_state.titles.append(t_name)
                    st.success(f"🎉 만렙 달성! [{t_name}] 획득!")
                save_user_data_to_db()
                st.rerun()
            else:
              st.button("MAX 완료", key=f"max_btn_{item}", disabled=True, use_container_width=True)
  else:
    st.markdown(
        """
        <div style="text-align: center; padding: 50px; color: #777;">
            <h3>🎒 스토리지가 비어 있습니다!</h3>
        </div>
        """,
        unsafe_allow_html=True,
    )

with tab_potions:
  st.subheader("🧪 포션 인벤토리")
  
  weather_ticket_count = st.session_state.get("weather_tickets", 0)
  if weather_ticket_count > 0:
    with st.container(border=True):
      col_wt1, col_wt2, col_wt3 = st.columns([1, 2, 1])
      with col_wt1:
        st.markdown("<div style='font-size: 38px; text-align: center;'>🌦️</div>", unsafe_allow_html=True)
      with col_wt2:
        st.markdown("#### 🌦️ 날씨 변경권")
        st.write(f"보유 수량: **{weather_ticket_count}개**")
        use_wt_qty = 1 if weather_ticket_count == 1 else st.slider("사용할 수량", min_value=1, max_value=weather_ticket_count, value=1, key="slider_qty_weather_ticket")
      with col_wt3:
        st.write("")
        st.write("")
        if st.button(f"날씨 변경권 사용 ({use_wt_qty}개)", key="btn_use_weather_ticket", type="primary", use_container_width=True):
          st.session_state.weather_tickets -= use_wt_qty
          
          # [핵심 수정] 즉시 날씨 오프셋을 재계산하여 새 날씨와 타이머(1분 또는 할로윈 5분)로 전환되도록 강제 고정
          current_real_time = int(time.time())
          
          # 다음 날씨가 할로윈일 확률 테스트
          test_offset_seed = current_real_time + random.randint(10000, 999999)
          test_big_cycle = test_offset_seed // 300
          random.seed(test_big_cycle * 999)
          is_hween = random.random() < 0.002
          random.seed()
          
          target_duration = 300 if is_hween else 60
          new_offset = target_duration - (current_real_time % target_duration) + (random.randint(1, 100) * target_duration)
          st.session_state.weather_offset = new_offset

          save_user_data_to_db()
          st.success(f"🎉 날씨 변경권 {use_wt_qty}장을 사용하여 날씨와 타이머를 즉시 초기화했습니다!")
          st.rerun()

  all_potions_count = sum(st.session_state.potions.values())
  if all_potions_count > 0 or weather_ticket_count > 0:
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
            use_qty = 1 if count == 1 else st.slider("사용할 수량", min_value=1, max_value=count, value=1, key=f"slider_qty_{p_name}")
          with col_p3:
            st.write("")
            st.write("")
            if st.button(f"선택 사용 ({use_qty}개)", key=f"btn_use_qty_{p_name}", type="primary", use_container_width=True):
              st.session_state.potions[p_name] -= use_qty
              cfg = potion_config[p_name]
              if cfg["type"] == "potion":
                now = time.time()
                add_duration = cfg["duration"] * use_qty
                if st.session_state.active_potion_name == p_name and now < st.session_state.active_potion_end:
                  st.session_state.active_potion_end += add_duration
                else:
                  st.session_state.active_potion_end = now + add_duration
                  st.session_state.active_potion_mult = cfg["mult"]
                  st.session_state.active_potion_name = p_name
              elif cfg["type"] == "ticket":
                if "million_ticket_count" not in st.session_state:
                  st.session_state.million_ticket_count = 0
                st.session_state.million_ticket_count += use_qty
                st.session_state.million_ticket_active = True
              save_user_data_to_db()
              st.success(f"🎉 [{p_name}] {use_qty}개가 성공적으로 사용되었습니다!")
              st.rerun()
  if all_potions_count == 0 and weather_ticket_count == 0:
    st.markdown("<div style='text-align: center; padding: 50px; color: #777;'><h3>🧪 포션 인벤토리가 비어 있습니다!</h3></div>", unsafe_allow_html=True)

with tab_codex:
  st.subheader("📖 아우라 도감 (Aura Codex)")
  col_left, col_right = st.columns([1, 1.5])
  with col_left:
    st.markdown("#### 📜 등급 목록")
    for item in items:
      is_owned = st.session_state.counts.get(item, 0) > 0 or st.session_state.levels.get(item, 1) > 1
      display_name = f"{icons.get(item, '✨')} {item}" if is_owned else "🔒 [LOCKED] ???"
      if st.button(display_name, key=f"codex_select_{item}", use_container_width=True):
        st.session_state.selected_codex = item

  with col_right:
    sel = st.session_state.get("selected_codex", items[0])
    if sel not in items:
      sel = items[0]
    is_owned = st.session_state.counts.get(sel, 0) > 0 or st.session_state.levels.get(sel, 1) > 1
    st.markdown(f"#### 상세 정보: `{sel if is_owned else '???'}`")
    with st.container(border=True):
      if is_owned:
        img_path = aura_images.get(sel)
        if img_path and os.path.exists(img_path):
          st.image(img_path, width=150)
        else:
          st.markdown(f"<div style='font-size: 40px;'>{icons.get(sel, '✨')}</div>", unsafe_allow_html=True)
        st.markdown(f"### [{sel}]")
        st.write(f"**희귀도 확률:** {fractions.get(sel, 'N/A')}")
        st.write(f"**보유 수량:** {st.session_state.counts.get(sel, 0)}개")
        st.write(f"**현재 레벨:** Lv. {st.session_state.levels.get(sel, 1)} / 6")
        
        matching_skins = aura_to_skins.get(sel, [])
        if matching_skins:
          st.markdown("---")
          st.markdown("##### 🎨 전용 스킨 관리")
          if "skins" not in st.session_state:
            st.session_state.skins = {s: 0 for s in skin_items}

          for skin_name in matching_skins:
            is_skin_owned = st.session_state.skins.get(skin_name, 0) >= 1
            is_skin_equipped = st.session_state.get("equipped_skin") == skin_name

            if is_skin_owned:
              st.success(f"🎨 보유 중인 스킨: **{skin_name}**")
              if is_skin_equipped:
                if st.button("❌ 스킨 장착 해제", key=f"codex_unequip_{skin_name}", use_container_width=True):
                  st.session_state.equipped_skin = None
                  save_user_data_to_db()
                  st.rerun()
              else:
                if st.button("🎨 이 스킨 장착하기", key=f"codex_equip_{skin_name}", type="primary", use_container_width=True):
                  st.session_state.equipped_skin = skin_name
                  save_user_data_to_db()
                  st.success(f"[{skin_name}] 스킨을 장착했습니다!")
                  st.rerun()
            else:
              st.caption(f"🔒 미보유 스킨: {skin_name} (케이스 오픈으로 획득 가능)")

        st.markdown("---")
        if sel in cutscene_auras:
          if st.button("🎬 컷씬 다시 보기", use_container_width=True):
            play_cutscene(sel)
      else:
        st.markdown("<div style='text-align: center; padding: 40px; color: #777;'><h2>🔒</h2><h3>아직 획득하지 못한 아우라입니다.</h3></div>", unsafe_allow_html=True)

with tab_titles:
  st.subheader("🎖️ 칭호 도감 칸 (Titles Codex)")
  user_titles = st.session_state.titles
  if user_titles:
    cols_per_row = 5
    for i in range(0, len(user_titles), cols_per_row):
      row_titles = user_titles[i : i + cols_per_row]
      grid_cols = st.columns(cols_per_row)
      for idx, t in enumerate(row_titles):
        is_t_equipped = st.session_state.get("equipped_title") == t
        with grid_cols[idx]:
          with st.container(border=True):
            st.markdown("<div style='text-align:center; font-size:26px;'>🎖️</div>", unsafe_allow_html=True)
            styled_t_html = get_styled_title_html(t)
            st.markdown(f"<div style='text-align:center; font-size:12px; font-weight:bold; word-break:keep-all; min-height:35px;'>{styled_t_html}</div>", unsafe_allow_html=True)
            if is_t_equipped:
              if st.button("해제", key=f"grid_unequip_t_{t}", use_container_width=True):
                st.session_state.equipped_title = None
                save_user_data_to_db()
                st.rerun()
            else:
              if st.button("장착", key=f"grid_equip_t_{t}", use_container_width=True, type="primary"):
                st.session_state.equipped_title = t
                save_user_data_to_db()
                st.rerun()
  else:
    st.markdown("<div style='text-align: center; padding: 50px; color: #777;'><h3>🎖️ 아직 획득한 칭호가 없습니다!</h3></div>", unsafe_allow_html=True)

with tab_shop:
  st.subheader("🛒 상점 & 데이터 백업/복구")
  
  with st.container(border=True):
    st.markdown("### 🌦️ 날씨 변경권 구매 (1개당 400 G)")
    st.write("구매 후 [포션 인벤토리] 탭에서 사용할 수 있으며, 사용 즉시 현재 날씨 확률 그대로 새로운 날씨로 바뀝니다!")
    max_weather_buy = st.session_state.coins // 400
    buy_weather_qty = 1 if max_weather_buy <= 1 else st.slider("구매할 날씨 변경권 수량", min_value=1, max_value=max_weather_buy, value=1, key="slider_buy_weather_tickets")
    total_weather_price = buy_weather_qty * 400
    st.write(f"총 필요 코인: **{total_weather_price:,} G**")
    if st.button(f"날씨 변경권 {buy_weather_qty}개 구매", type="primary", use_container_width=True, disabled=max_weather_buy < 1):
      if st.session_state.coins >= total_weather_price:
        st.session_state.coins -= total_weather_price
        st.session_state.weather_tickets = st.session_state.get("weather_tickets", 0) + buy_weather_qty
        save_user_data_to_db()
        st.success(f"🎉 날씨 변경권 {buy_weather_qty}개를 성공적으로 구매했습니다!")
        st.rerun()

  with st.container(border=True):
    col_box1, col_box2 = st.columns([2, 1])
    with col_box1:
      st.markdown("### 🎁 행운권 상자 구매 (300 G)")
      affordable_boxes = st.session_state.coins // 300
      buy_box_qty = 1 if affordable_boxes <= 1 else st.slider("구매할 상자 수량", min_value=1, max_value=affordable_boxes, value=1, key="slider_buy_boxes")
      total_box_price = buy_box_qty * 300
      st.write(f"총 필요 코인: **{total_box_price:,} G**")
    with col_box2:
      st.write("")
      if st.button(f"상자 {buy_box_qty}개 구매 & 개봉", type="primary", use_container_width=True, disabled=affordable_boxes < 1):
        if st.session_state.coins >= total_box_price:
          st.session_state.coins -= total_box_price
          won_summary = {}
          for _ in range(buy_box_qty):
            won_item = random.choices(potion_items, weights=potion_weights, k=1)[0]
            st.session_state.potions[won_item] += 1
            won_summary[won_item] = won_summary.get(won_item, 0) + 1
          save_user_data_to_db()
          st.success("🎉 행운권 상자 개봉 완료!")
          st.rerun()

  st.divider()

  st.markdown("### 💾 세이브 데이터 백업 및 복구")
  st.write("현재 계정의 모든 진행 상황(아우라, 레벨, 코인, 포션, 칭호 등)을 파일로 백업하거나 불러올 수 있습니다.")

  current_save_json = json.dumps(get_current_save_dict(), ensure_ascii=False, indent=2)
  
  col_dl, col_ul = st.columns(2)
  with col_dl:
    st.download_button(
        label="📥 내 세이브 데이터 백업 (JSON 다운로드)",
        data=current_save_json,
        file_name=f"aura_save_{st.session_state.username}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
        mime="application/json",
        use_container_width=True
    )

  with col_ul:
    uploaded_file = st.file_uploader("📤 세이브 파일 업로드 (복구)", type=["json"], key="save_uploader")
    if uploaded_file is not None:
      try:
        loaded_data = json.loads(uploaded_file.read().decode("utf-8"))
        apply_loaded_data_to_session(loaded_data)
        save_user_data_to_db()
        st.success("🎉 세이브 데이터가 성공적으로 복구되었습니다!")
        st.rerun()
      except Exception as e:
        st.error(f"❌ 파일 읽기 실패: 올바른 세이브 JSON 파일이 아닙니다. ({e})")

  with st.container(border=True):
    st.markdown("### 💻 개발자 인증 패널")
    dev_password = st.text_input("개발자 비밀번호", type="password", key="dev_pw_input")
    if st.button("🔐 권한 인증 및 모든 도감 해금", type="primary"):
      if dev_password == "0925":
        for item in items:
          st.session_state.counts[item] = max(1, st.session_state.counts.get(item, 1))
        for s in skin_items:
          st.session_state.skins[s] = 1
        save_user_data_to_db()
        st.success("개발자 인증 성공! 모든 도감이 해금되었습니다!")
        st.rerun()
      else:
        st.error("비밀번호가 틀렸습니다!")
