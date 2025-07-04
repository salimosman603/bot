import random
import time
import requests
from config import settings

class ProxyManager:
    def __init__(self):
        self.proxies = self._load_proxies()
        self.tor_proxies = ["socks5://localhost:9050"]
        self.verified_proxies = []
        self.last_verification = 0
        self.verify_proxies()

    def _load_proxies(self):
        try:
            with open(settings.PROXIES_FILE, 'r') as f:
                return [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            return []

    def verify_proxies(self):
        """Test all proxies and keep only working ones"""
        self.verified_proxies = []
        test_url = "https://api.ipify.org?format=json"
        
        # Verify Tor first
        try:
            response = requests.get(test_url, proxies={"http": self.tor_proxies[0], "https": self.tor_proxies[0]}, timeout=10)
            if response.status_code == 200:
                self.verified_proxies.append({
                    'server': self.tor_proxies[0],
                    'type': 'tor',
                    'ip': response.json()['ip']
                })
                print(f"✅ Tor proxy working: {response.json()['ip']}")
        except Exception as e:
            print(f"❌ Tor proxy failed: {str(e)}")
        
        # Verify other proxies
        for proxy in self.proxies:
            try:
                start = time.time()
                response = requests.get(test_url, proxies={"http": proxy, "https": proxy}, timeout=15)
                latency = time.time() - start
                
                if response.status_code == 200:
                    self.verified_proxies.append({
                        'server': proxy,
                        'type': 'residential',
                        'ip': response.json()['ip'],
                        'latency': latency
                    })
                    print(f"✅ Proxy working: {proxy} | IP: {response.json()['ip']} | Latency: {latency:.2f}s")
            except Exception as e:
                print(f"❌ Proxy failed: {proxy} | {str(e)}")
        
        self.last_verification = time.time()
        print(f"Verified {len(self.verified_proxies)} proxies")

    def get_verified_proxy(self):
        # Re-verify every 30 minutes
        if time.time() - self.last_verification > 1800 or not self.verified_proxies:
            self.verify_proxies()
            
        if not self.verified_proxies:
            return None  # No working proxies
            
        # Prefer Tor proxies 30% of the time
        tor_proxies = [p for p in self.verified_proxies if p['type'] == 'tor']
        other_proxies = [p for p in self.verified_proxies if p['type'] != 'tor']
        
        if tor_proxies and random.random() < 0.3:
            return random.choice(tor_proxies)
        elif other_proxies:
            # Select fastest proxies
            other_proxies.sort(key=lambda x: x.get('latency', 1))
            return random.choice(other_proxies[:5])
        else:
            return random.choice(self.verified_proxies)