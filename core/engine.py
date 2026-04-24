class SleepEngine:

    def analyze(self, state):

        avg = state["profile"]["avg_wb"]

        last_wb = state["today"]["wake_windows"][-1] if state["today"]["wake_windows"] else avg

        overtired = 0
        undertired = 0

        # перегул
        if last_wb > avg + 20:
            overtired += 0.6

        if state["today"]["naps"]:
            if state["today"]["naps"][-1] < 40:
                overtired += 0.3

        # недогул
        if last_wb < avg - 20:
            undertired += 0.6

        return {
            "overtired": min(overtired, 1),
            "undertired": min(undertired, 1)
        }

    def decide(self, analysis, state):

        avg = state["profile"]["avg_wb"]

        if analysis["overtired"] > 0.6:
            return {"wb": avg - 15, "mode": "overtired"}

        if analysis["undertired"] > 0.6:
            return {"wb": avg + 10, "mode": "undertired"}

        return {"wb": avg, "mode": "balanced"}




