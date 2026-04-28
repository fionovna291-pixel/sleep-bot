class SleepEngine:

    def analyze(self, state):
        avg = state["profile"]["avg_wb"]

        wake_windows = state["today"]["wake_windows"]
        naps = state["today"]["naps"]

        last_wb = wake_windows[-1] if wake_windows else avg

        overtired = 0
        undertired = 0

        if last_wb > avg + 20:
            overtired += 0.6

        if naps:
            if naps[-1] < 40:
                overtired += 0.3

        if last_wb < avg - 20:
            undertired += 0.6

        return {
            "overtired": min(overtired, 1),
            "undertired": min(undertired, 1),
            "last_wb": last_wb
        }

    def decide(self, analysis, state):
        avg = state["profile"]["avg_wb"]

        if analysis["overtired"] > 0.6:
            return {"wb": avg - 15, "mode": "overtired"}

        if analysis["undertired"] > 0.6:
            return {"wb": avg + 10, "mode": "undertired"}

        return {"wb": avg, "mode": "balanced"}