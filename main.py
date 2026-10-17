import random
import tkinter as tk
from tkinter import messagebox

# 확률 설정 (총합 100%)
# 일반: 90%, 희귀: 7%, 영웅: 2.9%, 전설: 0.1%
TIERS = [
    ("전설", 0.001, "#FFD700"),  # (이름, 확률, 색상)
    ("영웅", 0.029, "#9400D3"),
    ("희귀", 0.070, "#1E90FF"),
    ("일반", 0.900, "#A9A9A9"),
]


def gacha_roll():
    """가중치 확률에 따라 등급을 하나 뽑습니다."""
    rand_val = random.random()
    cumulative = 0.0
    for name, prob, color in TIERS:
        cumulative += prob
        if rand_val <= cumulative:
            return name, color
    return "일반", "#A9A9A9"


class GachaApp:

    def __init__(self, root):
        self.root = root
        self.root.title("두근두근 뽑기 시뮬레이터")
        self.root.geometry("450x520")
        self.root.resizable(False, False)

        # 뽑기 기록 저장 변수
        self.history = []  # 뽑은 아이템 이름 목록
        self.stats = {"전설": 0, "영웅": 0, "희귀": 0, "일반": 0}

        # 타이틀 레이블
        self.title_label = tk.Label(
            root, text="🎲 아이템 뽑기 시뮬레이터 🎲", font=("Helvetica", 16, "bold")
        )
        self.title_label.pack(pady=15)

        # 결과 출력 박스 (화면)
        self.result_frame = tk.Frame(
            root, width=380, height=140, bg="#F0F0F0", relief="solid", bd=2
        )
        self.result_frame.pack_propagate(False)
        self.result_frame.pack(pady=5)

        self.result_label = tk.Label(
            self.result_frame,
            text="버튼을 눌러 뽑기를 시작하세요!",
            font=("Helvetica", 13),
            bg="#F0F0F0",
            justify="center",
        )
        self.result_label.pack(expand=True)

        # 버튼 프레임 (1회 뽑기 & 10연차)
        self.btn_frame = tk.Frame(root)
        self.btn_frame.pack(pady=15)

        self.roll_button = tk.Button(
            self.btn_frame,
            text="1회 뽑기",
            font=("Helvetica", 12, "bold"),
            bg="#4CAF50",
            fg="white",
            width=12,
            command=lambda: self.start_animation(1),
        )
        self.roll_button.grid(row=0, column=0, padx=10)

        self.roll10_button = tk.Button(
            self.btn_frame,
            text="10연차!",
            font=("Helvetica", 12, "bold"),
            bg="#FF9800",
            fg="white",
            width=12,
            command=lambda: self.start_animation(10),
        )
        self.roll10_button.grid(row=0, column=1, padx=10)

        # 아이템 목록 및 통계 확인 버튼
        self.history_button = tk.Button(
            root,
            text="📜 뽑기 목록 및 통계 보기",
            font=("Helvetica", 11),
            bg="#2196F3",
            fg="white",
            width=28,
            command=self.show_history,
        )
        self.history_button.pack(pady=5)

        self.is_rolling = False

    def start_animation(self, count):
        """뽑기 버튼을 누르면 실행 (1회 또는 10회)"""
        if self.is_rolling:
            return

        self.is_rolling = True
        self.roll_button.config(state=tk.DISABLED, bg="#9E9E9E")
        self.roll10_button.config(state=tk.DISABLED, bg="#9E9E9E")
        self.history_button.config(state=tk.DISABLED)

        # 애니메이션용 리스트
        names = ["일반", "희귀", "영웅", "전설"]
        colors = ["#A9A9A9", "#1E90FF", "#9400D3", "#FFD700"]

        # 연출을 위해 12번 깜빡인 후 결과 출력
        self._animate_steps(12, count, names, colors)

    def _animate_steps(self, step_count, total_rolls, names, colors):
        if step_count > 0:
            idx = random.randint(0, 3)
            self.result_label.config(
                text=f"추첨 중... ({names[idx]})",
                fg=colors[idx],
                font=("Helvetica", 14, "bold"),
            )
            self.root.after(
                40,
                lambda: self._animate_steps(
                    step_count - 1, total_rolls, names, colors
                ),
            )
        else:
            # 최종 결과 계산
            results = []
            for _ in range(total_rolls):
                name, color = gacha_roll()
                results.append((name, color))
                self.history.append(name)
                self.stats[name] += 1

            # 결과 화면 출력
            if total_rolls == 1:
                name, color = results[0]
                self.result_label.config(
                    text=f"🎉 [1회 결과] 당첨: {name} 🎉",
                    fg=color,
                    font=("Helvetica", 15, "bold"),
                )
            else:
                # 10연차 결과 포맷팅
                result_text = "✨ [10연차 결과] ✨\n"
                result_str_list = [res[0] for res in results]
                # 보기 좋게 5개씩 줄바꿈
                result_text += (
                    ", ".join(result_str_list[:5])
                    + "\n"
                    + ", ".join(result_str_list[5:])
                )
                self.result_label.config(
                    text=result_text,
                    fg="#333333",
                    font=("Helvetica", 12, "bold"),
                )

            # 버튼 잠금 해제
            self.is_rolling = False
            self.roll_button.config(state=tk.NORMAL, bg="#4CAF50")
            self.roll10_button.config(state=tk.NORMAL, bg="#FF9800")
            self.history_button.config(state=tk.NORMAL)

    def show_history(self):
        """새 창을 띄워 지금까지 뽑은 전체 목록과 통계를 보여줍니다."""
        history_win = tk.Toplevel(self.root)
        history_win.title("뽑기 목록 및 통계")
        history_win.geometry("350x400")
        history_win.resizable(False, False)

        tk.Label(
            history_win, text="📊 누적 뽑기 통계", font=("Helvetica", 14, "bold")
        ).pack(pady=10)

        total_count = len(self.history)
        stat_text = (
            f"총 뽑기 횟수: {total_count}회\n\n"
            f"🟡 전설: {self.stats['전설']}회 ({self._get_percent('전설', total_count)}%)\n"
            f"🟣 영웅: {self.stats['영웅']}회 ({self._get_percent('영웅', total_count)}%)\n"
            f"🔵 희귀: {self.stats['희귀']}회 ({self._get_percent('희귀', total_count)}%)\n"
            f"⚪ 일반: {self.stats['일반']}회 ({self._get_percent('일반', total_count)}%)"
        )

        tk.Label(
            history_win,
            text=stat_text,
            font=("Helvetica", 11),
            justify="left",
            bg="#FAFAFA",
            relief="groove",
            padx=15,
            pady=10,
        ).pack(fill="x", padx=20)

        tk.Label(
            history_win,
            text="📜 최근 뽑기 기록 (최신 15개)",
            font=("Helvetica", 12, "bold"),
        ).pack(pady=10)

        # 최근 기록 15개만 리스트박스로 표시
        list_frame = tk.Frame(history_win)
        list_frame.pack(fill="both", expand=True, padx=20, pady=5)

        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        listbox = tk.Listbox(
            list_frame, yscrollcommand=scrollbar.set, font=("Helvetica", 10)
        )
        # 역순으로 최근 것이 위로 오게
        for item in reversed(self.history[-30:]):
            listbox.insert(tk.END, f"• {item}")

        listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=listbox.yview)

    def _get_percent(self, tier, total):
        if total == 0:
            return 0.0
        return round((self.stats[tier] / total) * 100, 2)


if __name__ == "__main__":
    root = tk.Tk()
    app = GachaApp(root)
    root.mainloop()
