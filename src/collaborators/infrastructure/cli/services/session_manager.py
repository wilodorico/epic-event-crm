import json
import os

SESSION_FILE = ".crm_session"


class SessionManager:
    @staticmethod
    def save_session(user_data: dict):
        with open(SESSION_FILE, "w") as f:
            json.dump(user_data, f)

    @staticmethod
    def load_session() -> dict | None:
        if not os.path.exists(SESSION_FILE):
            return None
        with open(SESSION_FILE, "r") as f:
            return json.load(f)

    @staticmethod
    def clear_session():
        if os.path.exists(SESSION_FILE):
            os.remove(SESSION_FILE)
