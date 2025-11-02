"""
Passenger WSGI file for running Telegram bot on cPanel.
This file makes the bot compatible with cPanel's Setup Python App.
"""

import sys
import os
import subprocess
import signal
from pathlib import Path

# Add application directory to Python path
APP_DIR = Path(__file__).parent.resolve()
sys.path.insert(0, str(APP_DIR))

# Configuration
PID_FILE = APP_DIR / 'bot.pid'
LOG_FILE = APP_DIR / 'bot.log'

def is_bot_running():
    """Check if the bot is already running."""
    if not PID_FILE.exists():
        return False
    
    try:
        with open(PID_FILE, 'r') as f:
            pid = int(f.read().strip())
        
        # Check if process exists
        os.kill(pid, 0)
        return True
    except (OSError, ValueError, ProcessLookupError):
        # Process doesn't exist, clean up PID file
        if PID_FILE.exists():
            PID_FILE.unlink()
        return False

def start_bot():
    """Start the Telegram bot as a background process."""
    if is_bot_running():
        return True
    
    try:
        # Start the bot process
        process = subprocess.Popen(
            [sys.executable, str(APP_DIR / 'bot.py')],
            cwd=str(APP_DIR),
            stdout=open(LOG_FILE, 'a'),
            stderr=subprocess.STDOUT,
            start_new_session=True,
            env=os.environ.copy()
        )
        
        # Save PID
        with open(PID_FILE, 'w') as f:
            f.write(str(process.pid))
        
        return True
    except Exception as e:
        print(f"Error starting bot: {e}", file=sys.stderr)
        return False

def stop_bot():
    """Stop the Telegram bot."""
    if not PID_FILE.exists():
        return True
    
    try:
        with open(PID_FILE, 'r') as f:
            pid = int(f.read().strip())
        
        # Send SIGTERM to gracefully stop the bot
        os.kill(pid, signal.SIGTERM)
        
        # Clean up PID file
        if PID_FILE.exists():
            PID_FILE.unlink()
        
        return True
    except (OSError, ValueError, ProcessLookupError):
        # Process doesn't exist, just clean up
        if PID_FILE.exists():
            PID_FILE.unlink()
        return True

# Start the bot when this module is loaded
start_bot()

def application(environ, start_response):
    """
    WSGI application entry point.
    This satisfies Passenger's requirement for a WSGI application.
    """
    # Get the request path
    path = environ.get('PATH_INFO', '/')
    
    # Check bot status
    bot_status = "Running ✅" if is_bot_running() else "Stopped ❌"
    
    # Simple status page
    if path == '/':
        status = '200 OK'
        response_headers = [
            ('Content-Type', 'text/html; charset=utf-8'),
            ('Cache-Control', 'no-cache, no-store, must-revalidate')
        ]
        start_response(status, response_headers)
        
        html_content = f'''
<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Telegram Warehouse Bot</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            margin: 0;
            padding: 20px;
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
        }}
        .container {{
            background: white;
            border-radius: 15px;
            padding: 40px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
            max-width: 600px;
            width: 100%;
        }}
        h1 {{
            color: #667eea;
            margin-bottom: 20px;
            text-align: center;
        }}
        .status {{
            background: #f0f4f8;
            padding: 20px;
            border-radius: 10px;
            margin: 20px 0;
        }}
        .status-item {{
            display: flex;
            justify-content: space-between;
            padding: 10px 0;
            border-bottom: 1px solid #ddd;
        }}
        .status-item:last-child {{
            border-bottom: none;
        }}
        .label {{
            font-weight: bold;
            color: #555;
        }}
        .value {{
            color: #333;
        }}
        .success {{
            color: #10b981;
            font-weight: bold;
        }}
        .error {{
            color: #ef4444;
            font-weight: bold;
        }}
        .info {{
            background: #e0e7ff;
            padding: 15px;
            border-radius: 8px;
            margin-top: 20px;
            font-size: 14px;
            color: #4338ca;
        }}
        .footer {{
            text-align: center;
            margin-top: 30px;
            color: #888;
            font-size: 12px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🤖 ربات مدیریت انبار</h1>
        <h2 style="text-align: center; color: #764ba2;">Telegram Warehouse Bot</h2>
        
        <div class="status">
            <div class="status-item">
                <span class="label">وضعیت (Status):</span>
                <span class="value {'success' if is_bot_running() else 'error'}">{bot_status}</span>
            </div>
            <div class="status-item">
                <span class="label">دایرکتوری (Directory):</span>
                <span class="value">{APP_DIR}</span>
            </div>
            <div class="status-item">
                <span class="label">Python:</span>
                <span class="value">{sys.version.split()[0]}</span>
            </div>
            <div class="status-item">
                <span class="label">PID فایل (File):</span>
                <span class="value">{'موجود ✓' if PID_FILE.exists() else 'وجود ندارد ✗'}</span>
            </div>
        </div>
        
        <div class="info">
            <strong>📱 نحوه استفاده:</strong><br>
            1. ربات خود را در تلگرام پیدا کنید<br>
            2. دستور /start را ارسال کنید<br>
            3. از منوهای دکمه‌ای استفاده کنید
        </div>
        
        <div class="info" style="background: #fef3c7; color: #92400e;">
            <strong>⚠️ نکته:</strong><br>
            برای راه‌اندازی مجدد، از دکمه Restart در cPanel > Setup Python App استفاده کنید.
        </div>
        
        <div class="footer">
            <p>CI-FARCO Warehousing System</p>
            <p>Powered by Python-Telegram-Bot</p>
        </div>
    </div>
</body>
</html>
        '''
        
        return [html_content.encode('utf-8')]
    
    elif path == '/status':
        # JSON status endpoint
        status = '200 OK'
        response_headers = [
            ('Content-Type', 'application/json'),
            ('Cache-Control', 'no-cache, no-store, must-revalidate')
        ]
        start_response(status, response_headers)
        
        import json
        status_data = {
            'running': is_bot_running(),
            'pid_file_exists': PID_FILE.exists(),
            'app_dir': str(APP_DIR),
            'python_version': sys.version.split()[0]
        }
        
        return [json.dumps(status_data, ensure_ascii=False).encode('utf-8')]
    
    else:
        # 404 for other paths
        status = '404 Not Found'
        response_headers = [('Content-Type', 'text/plain')]
        start_response(status, response_headers)
        return [b'Not Found']

# Graceful shutdown handler
def shutdown_handler(signum, frame):
    """Handle shutdown signals."""
    stop_bot()
    sys.exit(0)

signal.signal(signal.SIGTERM, shutdown_handler)
signal.signal(signal.SIGINT, shutdown_handler)

