# ╔══════════════════════════════╗
# ║  KSR MODULE — web_agent.py   ║
# ║  Full web automation agent   ║
# ╚══════════════════════════════╝

import time, re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException, NoSuchElementException, WebDriverException
)
try:
    from webdriver_manager.chrome import ChromeDriverManager
    WDM_OK = True
except ImportError:
    WDM_OK = False

# ── BROWSER SETUP ─────────────────────────────────────────────
driver = None

def get_driver(headless=False):
    """Get or create Chrome WebDriver."""
    global driver
    if driver:
        try:
            driver.current_url  # Test if still alive
            return driver
        except:
            driver = None

    opts = Options()
    if headless:
        opts.add_argument("--headless=new")
    opts.add_argument("--start-maximized")
    opts.add_argument("--disable-notifications")
    opts.add_argument("--disable-popup-blocking")
    opts.add_argument(f"--profile-directory=Default")
    opts.add_experimental_option("excludeSwitches", ["enable-automation"])
    opts.add_experimental_option('useAutomationExtension', False)

    try:
        if WDM_OK:
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=opts)
        else:
            driver = webdriver.Chrome(options=opts)
        return driver
    except Exception as e:
        print(f"WebDriver error: {e}")
        return None

def close_browser():
    global driver
    if driver:
        try: driver.quit()
        except: pass
        driver = None

# ── NAVIGATION ────────────────────────────────────────────────
def go_to(url):
    """Open a URL in browser."""
    d = get_driver()
    if not d: return False
    try:
        d.get(url)
        time.sleep(2)
        return True
    except Exception as e:
        print(f"Navigation error: {e}")
        return False

def new_tab(url):
    """Open URL in a new tab."""
    d = get_driver()
    if not d: return False
    try:
        d.execute_script(f"window.open('{url}', '_blank');")
        d.switch_to.window(d.window_handles[-1])
        time.sleep(2)
        return True
    except Exception as e:
        print(f"New tab error: {e}")
        return False

def go_back():
    d = get_driver()
    if d: d.back()

def go_forward():
    d = get_driver()
    if d: d.forward()

def refresh():
    d = get_driver()
    if d: d.refresh()

def get_current_url():
    d = get_driver()
    return d.current_url if d else ""

def get_page_title():
    d = get_driver()
    return d.title if d else ""

# ── CLICKING ──────────────────────────────────────────────────
def click_by_text(text, timeout=8):
    """Click any element containing specific text."""
    d = get_driver()
    if not d: return False
    try:
        # Try multiple strategies
        strategies = [
            f"//*[contains(text(), '{text}')]",
            f"//button[contains(text(), '{text}')]",
            f"//a[contains(text(), '{text}')]",
            f"//input[@value='{text}']",
            f"//*[@aria-label='{text}']",
            f"//*[contains(@placeholder, '{text}')]",
        ]
        for xpath in strategies:
            try:
                el = WebDriverWait(d, 2).until(EC.element_to_be_clickable((By.XPATH, xpath)))
                el.click()
                time.sleep(1)
                return True
            except: continue
        return False
    except Exception as e:
        print(f"Click error: {e}")
        return False

def click_by_css(selector, timeout=8):
    """Click element by CSS selector."""
    d = get_driver()
    if not d: return False
    try:
        el = WebDriverWait(d, timeout).until(EC.element_to_be_clickable((By.CSS_SELECTOR, selector)))
        el.click()
        time.sleep(0.8)
        return True
    except Exception as e:
        print(f"CSS click error: {e}")
        return False

def click_by_xpath(xpath, timeout=8):
    """Click element by XPath."""
    d = get_driver()
    if not d: return False
    try:
        el = WebDriverWait(d, timeout).until(EC.element_to_be_clickable((By.XPATH, xpath)))
        el.click()
        time.sleep(0.8)
        return True
    except Exception as e:
        print(f"XPath click error: {e}")
        return False

# ── TYPING ────────────────────────────────────────────────────
def type_in_field(selector_or_text, value, by_text=False, clear_first=True, press_enter=False):
    """Type text into an input field."""
    d = get_driver()
    if not d: return False
    try:
        if by_text:
            el = WebDriverWait(d, 8).until(
                EC.presence_of_element_located((By.XPATH, f"//*[contains(@placeholder, '{selector_or_text}')] | //input[@name='{selector_or_text}'] | //textarea[contains(@placeholder, '{selector_or_text}')]"))
            )
        else:
            el = WebDriverWait(d, 8).until(EC.presence_of_element_located((By.CSS_SELECTOR, selector_or_text)))

        if clear_first:
            el.clear()
        el.send_keys(value)
        time.sleep(0.3)
        if press_enter:
            el.send_keys(Keys.ENTER)
        return True
    except Exception as e:
        print(f"Type error: {e}")
        return False

def type_in_search(query, press_enter=True):
    """Type in any search box on current page."""
    d = get_driver()
    if not d: return False
    search_selectors = [
        'input[type="search"]',
        'input[name="q"]',
        'input[name="search"]',
        'input[placeholder*="search" i]',
        'input[placeholder*="Search" i]',
        '[role="searchbox"]',
        'input[type="text"]:first-of-type',
    ]
    for sel in search_selectors:
        try:
            el = WebDriverWait(d, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, sel)))
            el.clear()
            el.send_keys(query)
            if press_enter: el.send_keys(Keys.ENTER)
            time.sleep(1.5)
            return True
        except: continue
    return False

# ── SCROLLING ─────────────────────────────────────────────────
def scroll_down(amount=500):
    d = get_driver()
    if d: d.execute_script(f"window.scrollBy(0, {amount});")

def scroll_up(amount=500):
    d = get_driver()
    if d: d.execute_script(f"window.scrollBy(0, -{amount});")

def scroll_to_top():
    d = get_driver()
    if d: d.execute_script("window.scrollTo(0, 0);")

def scroll_to_bottom():
    d = get_driver()
    if d: d.execute_script("window.scrollTo(0, document.body.scrollHeight);")

# ── PAGE CONTENT ──────────────────────────────────────────────
def get_page_text():
    """Get all visible text from current page."""
    d = get_driver()
    if not d: return ""
    try:
        return d.find_element(By.TAG_NAME, 'body').text[:5000]
    except: return ""

def get_element_text(selector):
    """Get text of a specific element."""
    d = get_driver()
    if not d: return ""
    try:
        el = WebDriverWait(d, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
        return el.text
    except: return ""

def get_links():
    """Get all links on current page."""
    d = get_driver()
    if not d: return []
    try:
        els = d.find_elements(By.TAG_NAME, 'a')
        return [(el.text.strip(), el.get_attribute('href')) for el in els if el.text.strip() and el.get_attribute('href')]
    except: return []

def find_element_text(search_text):
    """Find if specific text exists on page."""
    return search_text.lower() in get_page_text().lower()

# ── SMART ACTIONS ─────────────────────────────────────────────
def google_search(query):
    """Search Google and return."""
    go_to(f"https://www.google.com/search?q={query.replace(' ', '+')}")
    time.sleep(2)

def youtube_search(query):
    """Search YouTube."""
    go_to(f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}")
    time.sleep(2)

def youtube_play(query):
    """Search YouTube and play first video."""
    youtube_search(query)
    time.sleep(2)
    # Click first video thumbnail
    selectors = ['a#video-title', '.ytd-video-renderer a', 'ytd-video-renderer h3 a']
    for sel in selectors:
        if click_by_css(sel): return True
    return False

def fill_form(fields_dict):
    """
    Fill a web form with dict of {placeholder_or_name: value}.
    Example: fill_form({'email': 'test@gmail.com', 'password': '123'})
    """
    d = get_driver()
    if not d: return False
    success = True
    for field_name, value in fields_dict.items():
        selectors = [
            f'input[name="{field_name}"]',
            f'input[placeholder*="{field_name}" i]',
            f'input[id="{field_name}"]',
            f'textarea[name="{field_name}"]',
        ]
        filled = False
        for sel in selectors:
            try:
                el = WebDriverWait(d, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, sel)))
                el.clear()
                el.send_keys(value)
                filled = True
                break
            except: continue
        if not filled:
            print(f"Couldn't fill field: {field_name}")
            success = False
    return success

def take_screenshot_browser(path="browser_screenshot.png"):
    """Take screenshot of current browser state."""
    d = get_driver()
    if d:
        d.save_screenshot(path)
        return path
    return None

# ── LINKEDIN AGENT ────────────────────────────────────────────
def linkedin_search_jobs(query, location="India"):
    """Search jobs on LinkedIn."""
    url = f"https://www.linkedin.com/jobs/search/?keywords={query.replace(' ', '%20')}&location={location}"
    go_to(url)
    time.sleep(3)
    return get_page_text()[:2000]

# ── LEETCODE AGENT ────────────────────────────────────────────
def leetcode_get_problem():
    """Get current LeetCode problem text."""
    d = get_driver()
    if not d: return ""
    try:
        # LeetCode problem description
        el = WebDriverWait(d, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '[data-track-load="description_content"]'))
        )
        return el.text
    except:
        return get_page_text()[:3000]

def leetcode_submit_code(code):
    """Type code into LeetCode editor and submit."""
    d = get_driver()
    if not d: return False
    try:
        # Click on code editor
        editor = WebDriverWait(d, 5).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '.CodeMirror, .monaco-editor'))
        )
        editor.click()
        time.sleep(0.5)
        # Select all and replace
        from selenium.webdriver.common.action_chains import ActionChains
        ActionChains(d).key_down(Keys.CONTROL).send_keys('a').key_up(Keys.CONTROL).perform()
        time.sleep(0.3)
        editor.send_keys(code)
        return True
    except Exception as e:
        print(f"LeetCode editor error: {e}")
        return False

# ── PROCESS VOICE COMMAND (called from KSR main) ──────────────
def process_web_command(query, speak_fn):
    """
    Handle web agent commands from KSR voice input.
    Returns True if command was handled.
    """
    q = query.lower()

    # YOUTUBE
    if 'play' in q and ('youtube' in q or 'song' in q or 'music' in q):
        term = re.sub(r'play|on youtube|song|music', '', q).strip()
        speak_fn(f"Playing {term} on YouTube.")
        youtube_play(term)
        return True

    elif 'search youtube' in q or 'youtube search' in q:
        term = re.sub(r'search youtube|youtube search|search on youtube', '', q).strip()
        speak_fn(f"Searching {term} on YouTube.")
        youtube_search(term)
        return True

    # GOOGLE
    elif 'google' in q or 'search' in q:
        term = re.sub(r'google|search for|search on google|search', '', q).strip()
        if term:
            speak_fn(f"Searching {term} on Google.")
            google_search(term)
            return True

    # SCROLL
    elif 'scroll down' in q:
        amt = 1000 if any(w in q for w in ['lot','more','big']) else 500
        scroll_down(amt)
        return True
    elif 'scroll up' in q:
        amt = 1000 if any(w in q for w in ['lot','more','big']) else 500
        scroll_up(amt)
        return True
    elif 'go to top' in q: scroll_to_top(); return True
    elif 'go to bottom' in q: scroll_to_bottom(); return True

    # CLICK
    elif 'click on' in q or 'click the' in q:
        target = re.sub(r'click on|click the|click', '', q).strip()
        speak_fn(f"Clicking {target}.")
        if not click_by_text(target):
            speak_fn(f"Couldn't find {target} on the page.")
        return True

    # FILL FORM
    elif 'type' in q or 'fill' in q or 'enter' in q:
        speak_fn("What should I type?")
        return True

    # NAVIGATION
    elif 'go back' in q: go_back(); return True
    elif 'go forward' in q: go_forward(); return True
    elif 'refresh' in q or 'reload' in q: refresh(); return True

    # OPEN URL
    elif 'open' in q and ('http' in q or '.com' in q or '.in' in q):
        # Extract URL
        url_match = re.search(r'https?://\S+|www\.\S+|\S+\.com\S*|\S+\.in\S*', q)
        if url_match:
            url = url_match.group()
            if not url.startswith('http'): url = 'https://' + url
            go_to(url)
            speak_fn(f"Opened {url}.")
            return True

    return False

if __name__ == "__main__":
    print("Testing web agent...")
    google_search("KSR AI assistant")
    time.sleep(3)
    print(get_page_text()[:500])
    close_browser()