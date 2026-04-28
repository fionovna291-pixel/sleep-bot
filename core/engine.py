class SleepEngine:

    def analyze_day(self, state):
        wbs = state["today"]["wake_windows"]
        naps = state["today"]["naps"]

        if not wbs:
            return None

        avg_wb = sum(wbs) / len(wbs)
        avg_nap = sum(naps) / len(naps) if naps else 0

        last_wb = wbs[-1] if wbs else avg_wb

        return {
            "avg_wb": int(avg_wb),
            "avg_nap": int(avg_nap),
            "count_naps": len(naps),
            "last_wb": int(last_wb)
        }

    def detect_state(self, analysis, state):
        target = state["profile"]["target_wb"]

        if not target:
            return "unknown"

        last = analysis["last_wb"]

        if last > target + 20:
            return "overtired"

        if last < target - 20:
            return "undertired"

        return "balanced"

    def human_recommendation(self, analysis, state):
        if not analysis:
            return "Пока мало данных, давай понаблюдаем еще день 🙂"

        target = state["profile"]["target_wb"]
        condition = self.detect_state(analysis, state)

        last_wb = analysis["last_wb"]

        if condition == "overtired":
            return (
                f"Сейчас уже есть признаки перегула.\n"
                f"Последнее ВБ было {last_wb} мин, это больше комфортного (~{target}).\n\n"
                f"Я бы попробовала завтра укладывать немного раньше."
            )

        if condition == "undertired":
            return (
                f"Похоже, есть небольшой недогул.\n"
                f"Последнее ВБ было всего {last_wb} мин при норме ~{target}.\n\n"
                f"Можно аккуратно увеличить время бодрствования."
            )

        return (
            f"Пока всё выглядит достаточно стабильно 👍\n"
            f"ВБ близко к норме (~{target} мин)."
        )

    def next_sleep_time(self, state):
        from datetime import timedelta

        last_wake = state["today"]["last_wake"]
        target = state["profile"]["target_wb"]

        if not last_wake or not target:
            return None

        next_time = last_wake + timedelta(minutes=target)

        return next_time

    def human_next_recommendation(self, state):
        next_time = self.next_sleep_time(state)

        if not next_time:
            return None

        return (
            f"Я бы ориентировалась на укладывание примерно в "
            f"{next_time.strftime('%H:%M')} ⏰"
        )