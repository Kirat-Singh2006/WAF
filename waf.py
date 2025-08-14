import re
from flask import Flask, request, abort
import sys, time
from datetime import datetime
from colorama import init, Fore, Style

init()

# Your hot pink ANSI color
PINK = "\033[38;5;205m"
RESET = "\033[0m"

banner = (
    PINK +
    r"""
  _____                _____        ______  _____   ______         _____    ____   ____ 
 |\    \   _____   ___|\    \   ___|\     \|\    \ |\     \    ___|\    \  |    | |    |
 | |    | /    /| |    |\    \ |     \     \\\    \| \     \  /    /\    \ |    | |    |
 \/     / |    || |    | |    ||     ,_____/|\|    \  \     ||    |  |    ||    |_|    |
 /     /_  \   \/ |    |/____/ |     \--'\_|/ |     \  |    ||    |  |____||    .-.    |
|     // \  \   \ |    |\    \ |     /___/|   |      \ |    ||    |   ____ |    | |    |
|    |/   \ |    ||    | |    ||     \____|\  |    |\ \|    ||    |  |    ||    | |    |
|\ ___/\   \|   /||____| |____||____ '     /| |____||\_____/||\ ___\/    /||____| |____|
| |   | \______/ ||    | |    ||    /_____/ | |    |/ \|   ||| |   /____/ ||    | |    |
 \|___|/\ |    | ||____| |____||____|     | / |____|   |___|/ \|___|    | /|____| |____|
    \(   \|____|/   \(     )/    \( |_____|/    \(       )/     \( |____|/   \(     )/  
     '      )/       '     '      '    )/        '       '       '   )/       '     '
""" +
    RESET
)

def type_out(text, delay=0.002):
    """Print text with typewriter effect."""
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)

# Print the banner with animation
type_out(banner)

# Footer
footer = (
    Fore.WHITE +
    "\n****************************************************************\n"
    "*  Copyright of wrench, 2025                           *\n"
    f"*  Loaded at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}                *\n"
    "****************************************************************" +
    Style.RESET_ALL
)
type_out(footer, delay=0.001)


app = Flask(__name__)

rules = {
    'sql_injection': re.compile(r'(union|select|insert|delete|update|drop|alter).*', re.IGNORECASE),
    'xss_attack': re.compile(r'(<script>|<iframe>).*', re.IGNORECASE),
    'path_traversal': re.compile(r'(\.\./|\.\.).*', re.IGNORECASE)
}

@app.before_request
def check_req_for():
    for attk_type, pattern in rules.items():
        if pattern.search(request.path) or pattern.search(request.query_string.decode()):
            abort(403, description=f"Request blocked by WAF: detected {attk_type}")

@app.route('/')
def home():
    return 'Welcome to the safe web application guarded by our WAF!'

if __name__ == '__main__':
    app.run(port=5000)
