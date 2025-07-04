import random
from fake_useragent import UserAgent
import numpy as np

class FingerprintGenerator:
    def __init__(self):
        self.ua = UserAgent(browsers=['chrome', 'firefox', 'safari'])
        self.viewports = self._generate_viewport_matrix()
        self.timezones = self._get_timezone_hierarchy()
        self.locales = ['en-US', 'en-GB', 'fr-FR', 'de-DE', 'ja-JP', 'es-ES']

    def generate(self):
        return {
            "user_agent": self.ua.random,
            "viewport": self._get_weighted_viewport(),
            "timezone": self._get_weighted_timezone(),
            "locale": random.choice(self.locales),
            "platform": self._get_platform_from_ua()
        }

    def _generate_viewport_matrix(self):
        # Device, viewport, probability weight
        return [
            # Desktop
            {"width": 1920, "height": 1080, "weight": 35},
            {"width": 1366, "height": 768, "weight": 25},
            {"width": 1440, "height": 900, "weight": 15},
            # Tablet
            {"width": 1024, "height": 768, "weight": 10},
            {"width": 768, "height": 1024, "weight": 5},
            # Mobile
            {"width": 414, "height": 896, "weight": 5},
            {"width": 375, "height": 812, "weight": 5}
        ]

    def _get_weighted_viewport(self):
        weights = [v['weight'] for v in self.viewports]
        chosen = random.choices(self.viewports, weights=weights, k=1)[0]
        return {"width": chosen['width'], "height": chosen['height']}

    def _get_timezone_hierarchy(self):
        # Timezone, population percentage
        return {
            'America/New_York': 15,
            'America/Los_Angeles': 12,
            'Europe/London': 10,
            'Europe/Paris': 8,
            'Asia/Tokyo': 7,
            'Australia/Sydney': 5,
            # Other timezones share remaining 43%
            'other': 43
        }

    def _get_weighted_timezone(self):
        tz_list = []
        weights = []
        for tz, weight in self.timezones.items():
            if tz != 'other':
                tz_list.append(tz)
                weights.append(weight)
        
        # Add random timezone for "other"
        if random.random() < (self.timezones['other'] / 100):
            return random.choice([
                'America/Chicago', 'America/Denver', 'Europe/Berlin', 
                'Asia/Shanghai', 'Asia/Dubai', 'Asia/Kolkata'
            ])
        return random.choices(tz_list, weights=weights, k=1)[0]

    def _get_platform_from_ua(self):
        # Not used directly but helps with consistency
        return "Win32" if "Windows" in self.ua.random else "MacIntel"