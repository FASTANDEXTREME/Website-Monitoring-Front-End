from flask import Flask, render_template
import threading
import time
import random

app = Flask(__name__)

site_is_up = True

def toggle_website_availability():
    global site_is_up
    while True:
        downtime = random.randint(10, 15) * 60
        downtime_start = random.randint(0, 3600 - downtime)
        time.sleep(downtime_start)
        site_is_up = False
        print("Website is down for maintenance...")
        time.sleep(downtime)

        site_is_up = True
        print("Website is back up!")
        time.sleep(3600 - downtime_start - downtime)  #
threading.Thread(target=toggle_website_availability, daemon=True).start()

@app.route('/')
def home():
    if not site_is_up:
        return "Website is temporarily down. Please try again later.", 503
    return render_template('site.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=7070)
