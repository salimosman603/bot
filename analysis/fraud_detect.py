import requests
from config import settings

def test_fraud_score(ip: str, user_agent: str):
    # Use external fraud detection API to test our own traffic
    resp = requests.post(
        "https://api.fraudscore.io/v2/check",
        json={
            "ip": ip,
            "ua": user_agent,
            "js": True,
            "flash": False,
            "iframe": True
        },
        headers={"Authorization": f"Bearer {settings.FRAUDSCORE_API_KEY}"}
    )
    return resp.json()["risk_score"]  # Target < 0.25 to avoid detection