import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Proxies file
PROXIES_FILE = os.path.join(BASE_DIR, 'config', 'proxies.txt')

# Logs directory
LOGS_DIR = os.path.join(BASE_DIR, 'logs')
TRAFFIC_LOG = os.path.join(LOGS_DIR, 'traffic.log')

MAX_SESSIONS = 500  # Increased sessions for revenue goals

# Bot settings
MAX_SESSIONS_PER_PROXY = int(os.getenv('MAX_SESSIONS_PER_PROXY', 2))  # Lower to avoid detection
USER_AGENT_ROTATION_INTERVAL = int(os.getenv('USER_AGENT_ROTATION_INTERVAL', 3))  # More frequent rotation
SESSION_COOLDOWN = (5, 30)  # Seconds between sessions

# Target settings - enhanced with multiple pages
TARGET_SITES = [
    {
        'base_url': 'https://mtoken.info',
        'entry_paths': ['/', '/tools/identity-generator', '/tools/temp-mail', '/tools/credit-card-generator', '/tools'],
        'internal_link_selectors': ['.nav-link', 'a.more-link', 'a.read-more'],
        'ad_selectors': ['.ad-banner', '#ad-sidebar', '.ad-box'],
        'min_time_on_page': 15,
        'max_time_on_page': 90,
        'probability_click_ad': 0.4,  # More realistic click rate
        'pages_per_session': (2, 5),  # Min/max pages per session
    }
]