import random
import time
import logging
import json
import os
from playwright.sync_api import sync_playwright
from urllib.parse import urljoin
from .fingerprint import FingerprintGenerator
from .proxy import ProxyManager
from .gpu_mouse import human_click
from .behavior import simulate_reading, random_mouse_movement
from .adstxt_parser import parse_ads_txt
from config import settings

class BrowserWrapper:
    def __init__(self, proxy_manager, fingerprint_generator):
        self.proxy_manager = proxy_manager
        self.fingerprint_generator = fingerprint_generator
        self.logger = logging.getLogger('traffic')
        self.playwright = None

    def _load_device_profile(self):
        """Load a random device profile for enhanced stealth"""
        profiles_dir = os.path.join(settings.BASE_DIR, 'config', 'device_profiles')
        if not os.path.exists(profiles_dir):
            return None
            
        profiles = [f for f in os.listdir(profiles_dir) if f.endswith('.json')]
        if not profiles:
            return None
            
        profile_file = os.path.join(profiles_dir, random.choice(profiles))
        try:
            with open(profile_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            self.logger.error(f"Failed to load device profile: {str(e)}")
            return None

    def create_context(self):
        proxy = self.proxy_manager.get_verified_proxy()
        device_profile = self._load_device_profile()
        
        # Enhanced device profile handling with validation
        fingerprint = {}
        if device_profile:
            # Use correct key names from device profiles
            fingerprint = {
                "user_agent": device_profile.get('userAgent', self.fingerprint_generator.generate()['user_agent']),
                "viewport": device_profile.get('viewport', {'width': 1920, 'height': 1080}),
                "timezone": device_profile.get('timezone', 'America/New_York'),
                "locale": device_profile.get('locale', 'en-US'),
                "platform": device_profile.get('platform', 'Win32')
            }
            self.logger.info(f"Using device profile: {list(device_profile.keys())}")
        else:
            fingerprint = self.fingerprint_generator.generate()
            self.logger.info("Using generated fingerprint")
        
        # Validate critical fields
        if not fingerprint.get("user_agent"):
            fingerprint["user_agent"] = self.fingerprint_generator.generate()['user_agent']
            self.logger.warning("Falling back to generated user agent")
        
        # Log fingerprint for debugging
        self.logger.debug(f"Fingerprint: UA={fingerprint['user_agent'][:30]}... | Viewport={fingerprint['viewport']}")
        

        self.playwright = sync_playwright().start()
        
        browser = self.playwright.chromium.launch(
            headless=True,
            proxy={"server": proxy['server']} if proxy else None,
            args=[
                f'--user-agent={fingerprint["user_agent"]}',
                f'--timezone={fingerprint["timezone"]}',
                f'--lang={fingerprint["locale"]}',
                '--disable-blink-features=AutomationControlled',
                '--disable-dev-shm-usage',
                '--no-sandbox',
                '--single-process'
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
        
        # Apply enhanced stealth with device profile
        from .stealth_engine import apply_stealth
        apply_stealth(context, device_profile)
        
        return browser, context

    def simulate_session(self, target_config):
        browser, context = None, None
        try:
            browser, context = self.create_context()
            page = context.new_page()
            
            # Start session at random entry point
            entry_url = urljoin(target_config['base_url'], random.choice(target_config['entry_paths']))
            
            # Parse ads.txt for legitimate ad networks
            ad_networks = parse_ads_txt(target_config['base_url'])
            if ad_networks:
                self.logger.info(f"Found {len(ad_networks)} authorized ad networks")
            
            # Bypass anti-bot measures
            page.goto("https://google.com", timeout=60000)
            time.sleep(3)
            page.goto(entry_url, timeout=120000)
            self.logger.info(f"Loaded {entry_url}")
            
            # Wait for ads to load
            time.sleep(target_config['ad_wait_time'])
            
            # Verify ad elements exist
            ad_count = self.count_ads(page, target_config['ad_selectors'])
            self.logger.info(f"Found {ad_count} ads on page")
            
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
                        # Wait for ads on new page
                        time.sleep(target_config['ad_wait_time'])
            
            # Final ad click before closing
            if random.random() < 0.7 and ad_count > 0:
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
            try:
                # Count all matching elements
                elements = page.query_selector_all(selector)
                for element in elements:
                    # Check if element is visible
                    if element.is_visible():
                        ad_count += 1
            except Exception as e:
                self.logger.warning(f"Selector error: {selector} - {str(e)}")
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
            try:
                elements = page.query_selector_all(selector)
                for element in elements:
                    if element.is_visible():
                        visible_ads.append(element)
            except Exception as e:
                self.logger.warning(f"Ad selector error: {selector} - {str(e)}")
        
        if not visible_ads:
            self.logger.warning("No visible ads to click")
            return False
            
        # Select random ad
        ad = random.choice(visible_ads)
        
        try:
            # Get tag name using evaluate
            tag_name = ad.evaluate("element => element.tagName.toLowerCase()")
            box = ad.bounding_box()
            
            # Calculate click position
            click_x = box['x'] + box['width']/2 + random.uniform(-5, 5)
            click_y = box['y'] + box['height']/2 + random.uniform(-5, 5)
            
            # Click with human-like precision
            human_click(page, click_x, click_y)
            
            self.logger.info(f"Clicked {tag_name} ad at position ({box['x']}, {box['y']})")
            
            # Stay on ad page
            time.sleep(random.uniform(8, 25))
            return True
        except Exception as e:
            self.logger.error(f"Ad click failed: {str(e)}")
            return False

    def find_internal_link(self, page, target_config, visited_pages):
        # Find internal links not yet visited
        internal_links = []
        for selector in target_config['internal_link_selectors']:
            try:
                links = page.query_selector_all(selector)
                for link in links:
                    href = link.get_attribute('href')
                    if href:
                        # Normalize URL
                        if href.startswith('/'):
                            full_url = urljoin(target_config['base_url'], href)
                        elif href.startswith(target_config['base_url']):
                            full_url = href
                        else:
                            continue
                            
                        if full_url not in visited_pages:
                            internal_links.append(full_url)
            except:
                continue
        
        return random.choice(internal_links) if internal_links else None