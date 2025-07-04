import random
import time
import logging
from playwright.sync_api import sync_playwright
from urllib.parse import urljoin
from .fingerprint import FingerprintGenerator
from .proxy import ProxyManager
from .gpu_mouse import human_click
from .behavior import simulate_reading, random_mouse_movement
from config import settings

class BrowserWrapper:
    def __init__(self, proxy_manager, fingerprint_generator):
        self.proxy_manager = proxy_manager
        self.fingerprint_generator = fingerprint_generator
        self.logger = logging.getLogger('traffic')
        self.playwright = None

    def create_context(self):
        proxy = self.proxy_manager.get_verified_proxy()  # Get verified proxy
        fingerprint = self.fingerprint_generator.generate()
        
        self.playwright = sync_playwright().start()
        
        # Use Google Chrome for better stealth
        browser = self.playwright.chromium.launch(
            headless=False,  # Critical for detection avoidance
            executable_path="/usr/bin/google-chrome-stable",
            proxy={"server": proxy['server']} if proxy else None,
            args=[
                f'--user-agent={fingerprint["user_agent"]}',
                f'--timezone={fingerprint["timezone"]}',
                f'--lang={fingerprint["locale"]}',
                '--disable-blink-features=AutomationControlled',
                '--disable-dev-shm-usage',
                '--no-sandbox'
            ]
        )
        context = browser.new_context(
            viewport=fingerprint["viewport"],
            locale=fingerprint["locale"],
            timezone_id=fingerprint["timezone"],
            user_agent=fingerprint["user_agent"],
            java_script_enabled=True,
            ignore_https_errors=True
        )
        
        # Apply stealth enhancements
        from .stealth_engine import apply_stealth
        apply_stealth(context)
        
        return browser, context

    def simulate_session(self, target_config):
        browser, context = None, None
        try:
            browser, context = self.create_context()
            page = context.new_page()
            
            # Start session at random entry point
            entry_url = urljoin(target_config['base_url'], random.choice(target_config['entry_paths']))
            
            # Bypass anti-bot measures with indirect navigation
            page.goto("https://google.com", timeout=60000)
            time.sleep(3)
            page.goto(entry_url, timeout=120000)
            self.logger.info(f"Loaded {entry_url}")
            
            # Verify ad elements exist
            ad_count = self.count_ads(page, target_config['ad_selectors'])
            if ad_count == 0:
                self.logger.error("NO ADS FOUND! Check ad selectors")
                return
            
            # Visit multiple pages
            pages_to_visit = random.randint(*target_config['pages_per_session'])
            visited_pages = [entry_url]
            
            for i in range(pages_to_visit):
                # Simulate page interaction
                self.interact_with_page(page, target_config)
                
                # Random mouse movements between actions
                random_mouse_movement(page)
                
                # Navigate to next page if not last
                if i < pages_to_visit - 1:
                    next_page = self.find_internal_link(page, target_config, visited_pages)
                    if next_page:
                        page.goto(next_page, timeout=60000)
                        visited_pages.append(next_page)
                        self.logger.info(f"Navigated to {next_page}")
            
            # Final ad click before closing
            if random.random() < 0.7:  # 70% chance to click ad at session end
                self.click_random_ad(page, target_config)
                
        except Exception as e:
            self.logger.error(f"Session failed: {str(e)}")
        finally:
            if browser:
                browser.close()
            if self.playwright:
                self.playwright.stop()

    def count_ads(self, page, selectors):
        ad_count = 0
        for selector in selectors:
            ad_count += page.locator(selector).count()
        self.logger.info(f"Found {ad_count} ads on page")
        return ad_count

    def interact_with_page(self, page, target_config):
        # Human-like behavior
        self.scroll_page(page)
        simulate_reading(page)
        random_mouse_movement(page)
        
        # Random ad click during session
        if random.random() < target_config['probability_click_ad']:
            self.click_random_ad(page, target_config)
            
        # Time on page
        time_on_page = random.uniform(
            target_config['min_time_on_page'], 
            target_config['max_time_on_page']
        )
        time.sleep(time_on_page)

    def scroll_page(self, page):
        # Human-like scrolling with variable speed
        scroll_height = page.evaluate("document.body.scrollHeight")
        viewport_height = page.evaluate("window.innerHeight")
        position = 0
        scrolls = random.randint(3, 8)
        
        for _ in range(scrolls):
            scroll_distance = min(
                random.randint(viewport_height // 2, viewport_height * 2),
                scroll_height - position
            )
            if scroll_distance <= 0:
                break
                
            page.mouse.wheel(0, scroll_distance)
            position += scroll_distance
            time.sleep(random.uniform(0.2, 1.5))

    def click_random_ad(self, page, target_config):
        # Get all visible ads
        visible_ads = []
        for selector in target_config['ad_selectors']:
            ads = page.locator(selector).all()
            for ad in ads:
                if ad.is_visible():
                    visible_ads.append(ad)
        
        if not visible_ads:
            self.logger.warning("No visible ads to click")
            return False
            
        # Select random ad
        ad = random.choice(visible_ads)
        box = ad.bounding_box()
        
        # Click with human-like precision
        human_click(
            page, 
            box['x'] + box['width']/2 + random.uniform(-5, 5),
            box['y'] + box['height']/2 + random.uniform(-5, 5)
        )
        
        self.logger.info(f"Clicked ad at position ({box['x']}, {box['y']})")
        
        # Stay on ad page
        time.sleep(random.uniform(8, 25))
        return True

    def find_internal_link(self, page, target_config, visited_pages):
        # Find internal links not yet visited
        internal_links = []
        for selector in target_config['internal_link_selectors']:
            links = page.locator(selector).all()
            for link in links:
                href = link.get_attribute('href')
                if href and (href.startswith('/') or href.startswith(target_config['base_url'])):
                    full_url = urljoin(target_config['base_url'], href)
                    if full_url not in visited_pages:
                        internal_links.append(full_url)
        
        return random.choice(internal_links) if internal_links else None