from playwright.sync_api import Page
import random

def apply_stealth(page: Page):
    # Override WebDriver value
    page.add_init_script("""
    delete Object.getPrototypeOf(navigator).webdriver;
    window.chrome = { runtime: {} };
    const originalQuery = window.navigator.permissions.query;
    window.navigator.permissions.query = (parameters) => (
        parameters.name === 'notifications' ? 
            Promise.resolve({ state: Notification.permission }) : 
            originalQuery(parameters)
    );
    """)
    
    # Spoof HTTP headers
    page.set_extra_http_headers({
        "Accept-Language": "en-US,en;q=0.9",
        "Sec-CH-UA": f'"Chromium";v="{random.randint(90,112)}", "Not A;Brand";v="24"'
    })