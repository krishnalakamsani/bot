from fastapi import FastAPI
import threading
import asyncio
import time
import pandas as pd

from dhan_ws import DhanWebSocket

app = FastAPI(title="Algo Backend")

running = False
state = "IDLE"

# ---------------- Candle Builder ----------------

class CandleBuilder:
    def __init__(self, interval=30):
        self.interval = interval
        self.reset()

    def reset(self):
        self.start_ts = None
        self.open = self.high = self.low = self.close = None

    def add_tick(self, price):
        now = int(time.time())

        if self.start_ts is None:
            self.start_ts = now
            self.open = self.high = self.low = self.close = price
            return None

        if now - self.start_ts < self.interval:
            self.high = max(self.high, price)
            self.low = min(self.low, price)
            self.close = price
            return None

        candle = {
            "open": self.open,
            "high": self.high,
            "low": self.low,
            "close": self.close,
            "volume": 0
        }

        self.reset()
        return candle


# ---------------- Algo Logic ----------------

builder = CandleBuilder(30)
df = pd.DataFrame(columns=["open", "high", "low", "close", "volume"])

def on_tick(tick):
    global state, df

    price = tick.get("ltp")
    if not price:
        return

    candle = builder.add_tick(price)
    if candle:
        df = pd.concat([df, pd.DataFrame([candle])], ignore_index=True)

        if len(df) > 2:
            # simple demo state logic (replace later)
            state = "IN_POSITION" if state == "IDLE" else "IDLE"
            print("NEW CANDLE:", candle, "STATE:", state)


async def algo_loop():
    ws = DhanWebSocket(on_tick, lambda: running)
    await ws.connect()


def start_algo():
    asyncio.run(algo_loop())


# ---------------- API ----------------

@app.post("/start")
def start():
    global running
    if not running:
        running = True
        threading.Thread(target=start_algo, daemon=True).start()
    return {"running": running}


@app.post("/stop")
def stop():
    global running
    running = False
    return {"running": running}


@app.get("/status")
def status_api():
    return {"running": running, "state": state}
