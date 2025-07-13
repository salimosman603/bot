import logging
import time
import random
import os
from .browser import BrowserWrapper
from .proxy import ProxyManager
from .fingerprint import FingerprintGenerator
from .targets import TargetManager
from config import settings

class BotRunner:
    def __init__(self):
        self.proxy_manager = ProxyManager()
        self.fingerprint_generator = FingerprintGenerator()
        self.target_manager = TargetManager()
        self.browser_wrapper = BrowserWrapper(self.proxy_manager, self.fingerprint_generator)
        self.setup_logging()
        self.session_counter = 0

    def setup_logging(self):
        log_dir = os.path.dirname(settings.TRAFFIC_LOG)
        if log_dir:
            os.makedirs(log_dir, exist_ok=True)

        logging.basicConfig(
            filename=settings.TRAFFIC_LOG,
            level=logging.INFO,
            format='%(asctime)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        # Add console logging for better debugging
        console = logging.StreamHandler()
        console.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(message)s')
        console.setFormatter(formatter)
        logging.getLogger('').addHandler(console)
        
        self.logger = logging.getLogger('traffic')

    def run(self):
        self.logger.info("Starting bot runner")
        while True:
            try:
                self.logger.info(f"Starting session {self.session_counter + 1}")
                target = self.target_manager.get_target()
                self.browser_wrapper.simulate_session(target)
                self.session_counter += 1
                self.logger.info(f"Completed session {self.session_counter}")
                
                # Adaptive cooldown based on session count
                min_wait, max_wait = settings.SESSION_COOLDOWN
                cooldown = max_wait - (max_wait - min_wait) * (self.session_counter / settings.MAX_SESSIONS)
                wait_time = random.uniform(min_wait, cooldown)
                self.logger.info(f"Waiting {wait_time:.1f} seconds before next session")
                time.sleep(wait_time)
                
            except Exception as e:
                self.logger.error(f"Runner error: {str(e)}")
                time.sleep(30)  # Recover after error