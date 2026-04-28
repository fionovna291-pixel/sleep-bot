from datetime import datetime

users = {}

async def init_db():
    pass

def get_user(user_id):
    if user_id not in users:
        users[user_id] = {
            "profile": {
                "age": None,
                "avg_wb": None
            },
            "today": {
                "sleep_start": None,
                "wake_windows": [],
                "naps": []
            }
        }
    return users[user_id]

def save_sleep_start(user_id):
    user = get_user(user_id)
    user["today"]["sleep_start"] = datetime.now()

def save_wakeup(user_id):
    user = get_user(user_id)

    start = user["today"]["sleep_start"]
    if not start:
        return None

    now = datetime.now()
    duration = (now - start).seconds // 60

    user["today"]["naps"].append(duration)
    user["today"]["sleep_start"] = None

    return duration

def save_wake_window(user_id, minutes):
    user = get_user(user_id)
    user["today"]["wake_windows"].append(minutes)