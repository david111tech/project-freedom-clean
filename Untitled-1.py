warhead/client.py
import asyncio

class WarheadClient:
    async def connect(self):
        print("CLIENT ONLINE — awaiting instructions...")
        await asyncio.sleep(1)
        print("Connection stable ✔")
