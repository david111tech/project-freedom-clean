import asyncio
from warhead.client import WarheadClient

async def main():
    print("🚀 WARHEAD SYSTEM LAUNCHING...")
    client = WarheadClient()
    await client.connect()

if __name__ == "__main__":
    asyncio.run(main())
