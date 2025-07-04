import os
from bot.runner import BotRunner
from flask import Flask
import threading

app = Flask(__name__)

@app.route('/health')
def health_check():
    return "OK", 200

if __name__ == '__main__':
    # Start bot in background thread
    bot_thread = threading.Thread(target=lambda: BotRunner().run())
    bot_thread.daemon = True
    bot_thread.start()
    
    # Start Flask server in main thread
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))