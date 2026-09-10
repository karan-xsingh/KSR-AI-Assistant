# ╔══════════════════════════════╗
# ║  KSR MODULE — scheduler.py   ║
# ║  Repeat tasks & daily routine║
# ╚══════════════════════════════╝

import json, os, re, threading, time, datetime
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

TASKS_FILE = os.path.join(os.path.expanduser("~"), "Desktop", "KSR_Tasks.json")

scheduler = BackgroundScheduler()
scheduler.start()

_speak_fn = None
_process_fn = None

def init(speak_fn, process_fn):
    """Initialize with KSR's speak and process functions."""
    global _speak_fn, _process_fn
    _speak_fn = speak_fn
    _process_fn = process_fn
    load_and_restore_tasks()

def speak(text):
    if _speak_fn: _speak_fn(text)
    else: print(f"[SCHEDULER] {text}")

# ── TASK STORAGE ──────────────────────────────────────────────
def load_tasks():
    try:
        with open(TASKS_FILE, 'r') as f:
            return json.load(f)
    except: return []

def save_tasks(tasks):
    with open(TASKS_FILE, 'w') as f:
        json.dump(tasks, f, indent=2)

def load_and_restore_tasks():
    """Restore all saved tasks on startup."""
    tasks = load_tasks()
    for task in tasks:
        schedule_task(
            task_id=task['id'],
            command=task['command'],
            hour=task.get('hour', 9),
            minute=task.get('minute', 0),
            days=task.get('days', 'mon-sun'),
            save=False
        )
    if tasks:
        print(f"[SCHEDULER] Restored {len(tasks)} scheduled tasks.")

# ── SCHEDULING ────────────────────────────────────────────────
def schedule_task(task_id, command, hour, minute, days='mon-sun', save=True):
    """Schedule a recurring task."""
    def run_task():
        speak(f"Running your scheduled task: {command}")
        if _process_fn:
            _process_fn(command)

    try:
        scheduler.add_job(
            run_task,
            CronTrigger(day_of_week=days, hour=hour, minute=minute),
            id=task_id,
            replace_existing=True
        )
        if save:
            tasks = load_tasks()
            # Remove existing task with same id
            tasks = [t for t in tasks if t['id'] != task_id]
            tasks.append({
                'id': task_id,
                'command': command,
                'hour': hour,
                'minute': minute,
                'days': days
            })
            save_tasks(tasks)
        print(f"[SCHEDULER] Task '{task_id}' scheduled at {hour:02d}:{minute:02d} on {days}")
        return True
    except Exception as e:
        print(f"[SCHEDULER] Error: {e}")
        return False

def remove_task(task_id):
    """Remove a scheduled task."""
    try:
        scheduler.remove_job(task_id)
        tasks = [t for t in load_tasks() if t['id'] != task_id]
        save_tasks(tasks)
        return True
    except: return False

def list_tasks():
    """Get all scheduled tasks."""
    return load_tasks()

def clear_all_tasks():
    """Remove all scheduled tasks."""
    for task in load_tasks():
        try: scheduler.remove_job(task['id'])
        except: pass
    save_tasks([])

# ── ONE-TIME REMINDER ─────────────────────────────────────────
def remind_once(message, delay_seconds):
    """Set a one-time reminder after delay."""
    def run():
        time.sleep(delay_seconds)
        speak(f"Reminder: {message}")
    threading.Thread(target=run, daemon=True).start()

# ── PARSE VOICE COMMAND ───────────────────────────────────────
def parse_schedule_command(query):
    """
    Parse natural language scheduling commands.
    Returns dict with schedule info or None.

    Examples:
    - "every morning at 9 open vs code"
    - "every day at 6 pm remind me to review notes"
    - "every monday at 10 am check github"
    - "every weekday at 8 30 open chrome and play lo-fi"
    """
    q = query.lower()

    # Extract time
    hour, minute = 9, 0

    # Match "at X am/pm" or "at X:XX"
    time_match = re.search(r'at\s+(\d{1,2})(?::(\d{2}))?\s*(am|pm)?', q)
    if time_match:
        hour = int(time_match.group(1))
        minute = int(time_match.group(2) or 0)
        ampm = time_match.group(3)
        if ampm == 'pm' and hour != 12: hour += 12
        if ampm == 'am' and hour == 12: hour = 0

    # Named times
    if 'morning' in q and 'at' not in q: hour, minute = 9, 0
    elif 'afternoon' in q and 'at' not in q: hour, minute = 14, 0
    elif 'evening' in q and 'at' not in q: hour, minute = 18, 0
    elif 'night' in q and 'at' not in q: hour, minute = 21, 0
    elif 'noon' in q: hour, minute = 12, 0
    elif 'midnight' in q: hour, minute = 0, 0

    # Extract days
    days = 'mon-sun'  # default: every day
    if 'weekday' in q or 'working day' in q: days = 'mon-fri'
    elif 'weekend' in q: days = 'sat,sun'
    elif 'monday' in q: days = 'mon'
    elif 'tuesday' in q: days = 'tue'
    elif 'wednesday' in q: days = 'wed'
    elif 'thursday' in q: days = 'thu'
    elif 'friday' in q: days = 'fri'
    elif 'saturday' in q: days = 'sat'
    elif 'sunday' in q: days = 'sun'

    # Extract the actual command to run
    command = q
    # Remove scheduling words to get the action
    for phrase in ['every morning', 'every evening', 'every afternoon', 'every night',
                   'every day', 'every weekday', 'every weekend', 'every monday',
                   'every tuesday', 'every wednesday', 'every thursday', 'every friday',
                   'every saturday', 'every sunday', 'schedule', 'every']:
        command = command.replace(phrase, '')

    # Remove time part
    if time_match:
        command = command.replace(time_match.group(0), '')

    command = re.sub(r'\s+', ' ', command).strip()

    if not command:
        return None

    return {
        'hour': hour,
        'minute': minute,
        'days': days,
        'command': command,
        'id': f"task_{hour}_{minute}_{command[:10].replace(' ','_')}"
    }

# ── HANDLE VOICE COMMANDS ─────────────────────────────────────
def handle_scheduler_command(query, speak_fn):
    """
    Process scheduler-related voice commands.
    Returns True if handled.
    """
    q = query.lower()

    # SCHEDULE NEW TASK
    if any(p in q for p in ['every morning', 'every evening', 'every day', 'every night',
                              'every weekday', 'every monday', 'every tuesday', 'schedule']):
        info = parse_schedule_command(q)
        if info:
            success = schedule_task(
                task_id=info['id'],
                command=info['command'],
                hour=info['hour'],
                minute=info['minute'],
                days=info['days']
            )
            if success:
                days_str = info['days']
                time_str = f"{info['hour']:02d}:{info['minute']:02d}"
                speak_fn(f"Done! I'll {info['command']} every {days_str} at {time_str}.")
            else:
                speak_fn("Couldn't schedule that task.")
            return True

    # LIST TASKS
    elif any(p in q for p in ['my schedule', 'scheduled tasks', 'list tasks', 'what tasks', 'show schedule']):
        tasks = list_tasks()
        if tasks:
            speak_fn(f"You have {len(tasks)} scheduled tasks:")
            for t in tasks:
                speak_fn(f"Every {t['days']} at {t['hour']:02d}:{t['minute']:02d} — {t['command']}")
        else:
            speak_fn("No scheduled tasks yet.")
        return True

    # CLEAR ALL
    elif 'clear schedule' in q or 'delete all tasks' in q or 'remove all tasks' in q:
        clear_all_tasks()
        speak_fn("All scheduled tasks cleared.")
        return True

    return False

if __name__ == "__main__":
    print("Testing scheduler...")
    def test_speak(t): print(f"SPEAK: {t}")
    init(test_speak, None)
    result = parse_schedule_command("every morning at 9 open vs code and play lo-fi music")
    print(f"Parsed: {result}")