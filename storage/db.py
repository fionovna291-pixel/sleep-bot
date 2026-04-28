user_states = {}

async def init_db():
    pass

def get_default_state():
    return {
        "profile": {
            "avg_wb": 120
        },
        "today": {
            "wake_windows": [],
            "naps": [],
            "last_wake": None,
            "sleep_start": None
        }
    }

def load_state(user_id):
    if user_id not in user_states:
        user_states[user_id] = get_default_state()
    return user_states[user_id]

def save_state(user_id, state):
    user_states[user_id] = state