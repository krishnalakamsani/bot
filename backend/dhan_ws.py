import json
import asyncio
import websockets

class DhanWebSocket:
    def __init__(self, on_tick, should_run):
        self.on_tick = on_tick
        self.should_run = should_run

    async def connect(self):
        uri = "wss://api-feed.dhan.co/marketfeed"
        async with websockets.connect(uri) as ws:
            await self.subscribe(ws)

            while self.should_run():
                msg = await ws.recv()
                data = json.loads(msg)
                self.on_tick(data)

    async def subscribe(self, ws):
        payload = {
            "action": "subscribe",
            "symbols": ["NIFTY"],
            "mode": "ltp"
        }
        await ws.send(json.dumps(payload))
