class SleepEngine:

    def analyze_day(self, state):
        wbs = state["today"]["wake_windows"]
        naps = state["today"]["naps"]

        if not wbs:
            return None

        avg_wb = sum(wbs) / len(wbs)
        avg_nap = sum(naps) / len(naps) if naps else 0

        return {
            "avg_wb": int(avg_wb),
            "avg_nap": int(avg_nap),
            "count_naps": len(naps)
        }

    def recommend(self, analysis, state):
        target = state["profile"]["target_wb"]

        if not analysis:
            return "Пока мало данных, давай соберем еще один день 🙂"

        avg_wb = analysis["avg_wb"]

        if avg_wb > target + 20:
            return "Есть признаки перегула 😣 Попробуй укладывать раньше."

        if avg_wb < target - 20:
            return "Похоже на недогул 🙂 Можно немного увеличить ВБ."

        return "Режим близок к оптимальному 👍"