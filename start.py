import os
from bot.runner import BotRunner
from flask import Flask, redirect
import threading

# Create Flask app first
app = Flask(__name__)

# Then define routes
@app.route('/')
def root():
    return redirect('/health', code=302)

@app.route('/health')
def health_check():
    return "OK", 200

if __name__ == '__main__':
    try:
        # Start bot in background thread
        bot_thread = threading.Thread(target=lambda: BotRunner().run())
        bot_thread.daemon = True
        bot_thread.start()

        # Start Flask server in main thread
        app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))

    except KeyboardInterrupt:
        print("Shutting down...")
        if bot_thread.is_alive():
            # You should define this or handle safely
            # For now, just print
            print("Cleaning up...")