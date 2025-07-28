from flask import Flask
from utils.performance import PerformanceMonitor

app = Flask(__name__)

@app.route("/")
def home():
    monitor = PerformanceMonitor()
    monitor.start()
    # Simulate some work
    import time
    time.sleep(0.2)
    elapsed = monitor.elapsed()
    return f"Dashboard loaded! PerformanceMonitor: {elapsed:.4f} seconds"

if __name__ == "__main__":
    app.run(debug=True)