from config import settings
import random

class TargetManager:
    def __init__(self):
        self.targets = settings.TARGET_SITES

    def get_target(self):
        # For now, just pick a random target
        return random.choice(self.targets)