class SleepEngine:

    def analyze(self, state):
        avg = state["profile"]["avg_wb"]
        windows = state["today"]["wake_windows"]

        if not windows:
            return {"status": "no_data"}

        last = windows[-1]

        if last > avg + 20:
            return {"status": "overtired"}

        if last < avg - 20:
            return {"status": "undertired"}

        return {"status": "balanced"}

    def recommend(self, state, analysis):
        avg = state["profile"]["avg_wb"]

        if analysis["status"] == "overtired":
            return avg - 15

        if analysis["status"] == "undertired":
            return avg + 10

        return avg