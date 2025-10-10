import json
import os

from collaborators.infrastructure.security.jwt_service import JWTService

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
            data = json.load(f)

        token = data.get("token")
        if not token:
            return None

        jwt_service = JWTService()
        try:
            decoded = jwt_service.decode(token)
            return decoded
        except ValueError as e:
            print(f"❌ Invalid session token: {str(e)}")
            return None

    @staticmethod
    def clear_session():
        if os.path.exists(SESSION_FILE):
            os.remove(SESSION_FILE)
