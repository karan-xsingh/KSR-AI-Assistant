# ╔══════════════════════════════╗
# ║  KSR MODULE — vision.py      ║
# ║  Screen reading + OCR        ║
# ╚══════════════════════════════╝

import os, re, base64, io, subprocess
import pyautogui

try:
    import mss
    from PIL import Image
    MSS_OK = True
except ImportError:
    MSS_OK = False

try:
    import pytesseract
    # Set tesseract path
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    OCR_OK = True
except ImportError:
    OCR_OK = False

# ── TAKE SCREENSHOT ───────────────────────────────────────────
def take_screenshot(region=None):
    """Take full screenshot or a region. Returns PIL Image."""
    if not MSS_OK:
        return None
    with mss.mss() as sct:
        if region:
            shot = sct.grab(region)
        else:
            shot = sct.grab(sct.monitors[1])
        img = Image.frombytes('RGB', shot.size, shot.bgra, 'raw', 'BGRX')
        return img

def screenshot_to_base64(img=None):
    """Convert screenshot to base64 for AI APIs."""
    if img is None:
        img = take_screenshot()
    if img is None:
        return None
    img.thumbnail((1280, 720))
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    return base64.b64encode(buf.getvalue()).decode()

def save_screenshot(path="screenshot.png"):
    img = take_screenshot()
    if img:
        img.save(path)
        return path
    return None

# ── READ TEXT FROM SCREEN (OCR) ───────────────────────────────
def read_screen_text(region=None):
    """Read ALL text visible on screen using OCR."""
    if not OCR_OK:
        return "pytesseract not installed. Run: pip install pytesseract"
    img = take_screenshot(region)
    if img is None:
        return ""
    try:
        text = pytesseract.image_to_string(img)
        return text.strip()
    except Exception as e:
        print(f"OCR error: {e}")
        return ""

def read_selected_region(x, y, width, height):
    """Read text from a specific region of screen."""
    region = {"top": y, "left": x, "width": width, "height": height}
    return read_screen_text(region)

# ── READ CODING QUESTION FROM SCREEN ─────────────────────────
def read_coding_question():
    """
    Reads the current screen and extracts a coding question/problem.
    Works with LeetCode, HackerRank, competitive programming sites,
    VS Code problem descriptions, etc.
    """
    text = read_screen_text()
    if not text:
        return None

    # Clean up OCR artifacts
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = text.strip()

    # Try to find problem title + description pattern
    lines = text.split('\n')
    problem_lines = []
    capturing = False

    for line in lines:
        line = line.strip()
        if not line:
            continue
        # Start capturing at common problem indicators
        if any(kw in line.lower() for kw in [
            'problem', 'question', 'given', 'write a', 'implement',
            'find', 'return', 'input:', 'output:', 'example',
            'description', 'constraints', 'note:'
        ]):
            capturing = True
        if capturing and line:
            problem_lines.append(line)

    if problem_lines:
        return '\n'.join(problem_lines[:50])  # First 50 lines max
    return text[:2000]  # Fallback: first 2000 chars

# ── GET ACTIVE WINDOW INFO ────────────────────────────────────
def get_active_windows():
    """Get titles of all open windows."""
    try:
        result = subprocess.check_output(
            'powershell -command "Get-Process | Where-Object {$_.MainWindowTitle -ne \'\'} | Select-Object -ExpandProperty MainWindowTitle"',
            shell=True, text=True, timeout=5
        ).strip()
        return [w.strip() for w in result.split('\n') if w.strip()]
    except:
        return []

def get_focused_window():
    """Get the title of the currently focused window."""
    try:
        result = subprocess.check_output(
            'powershell -command "Add-Type -AssemblyName Microsoft.VisualBasic; [Microsoft.VisualBasic.Interaction]::AppActivate((Get-Process | Where-Object {$_.MainWindowTitle -ne \'\'} | Select-Object -First 1).Id)"',
            shell=True, text=True, timeout=3
        )
        windows = get_active_windows()
        return windows[0] if windows else ""
    except:
        windows = get_active_windows()
        return windows[0] if windows else ""

# ── FIND TEXT ON SCREEN ───────────────────────────────────────
def find_text_on_screen(search_text):
    """Find if specific text is visible on screen. Returns True/False."""
    screen_text = read_screen_text().lower()
    return search_text.lower() in screen_text

def get_screen_summary():
    """Get a quick summary of what's on screen."""
    windows = get_active_windows()
    text_preview = read_screen_text()[:500] if OCR_OK else ""

    summary = []
    if windows:
        summary.append(f"Open windows: {', '.join(windows[:5])}")
    if text_preview:
        # Extract first few meaningful lines
        lines = [l.strip() for l in text_preview.split('\n') if len(l.strip()) > 5][:5]
        if lines:
            summary.append(f"Visible text: {' | '.join(lines)}")
    return '\n'.join(summary) if summary else "Nothing detected on screen."

if __name__ == "__main__":
    print("Testing vision module...")
    print(get_screen_summary())