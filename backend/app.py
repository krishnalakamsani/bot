from fastapi import FastAPI
import threading, time, pandas as pd

app = FastAPI()

running = False
state = "IDLE"

def algo_loop():
    global running, state
    df = pd.read_csv("sample_30s.csv")
    for i in range(2, len(df)):
        if not running:
            break
        state = "IN_POSITION" if i % 2 == 0 else "IDLE"
        time.sleep(1)

@app.post("/start")
def start():
    global running
    if not running:
        running = True
        threading.Thread(target=algo_loop, daemon=True).start()
    return {"running": running}

@app.post("/stop")
def stop():
    global running
    running = False
    return {"running": running}

@app.get("/status")
def status():
    return {"running": running, "state": state}