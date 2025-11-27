from warhead.core import greet

def test_greet():
    assert greet("David") == "Warhead ready, David"
"""
test_core.py — Phase 1A simulation engine (stationary target at EAST)

How to run (inside your activated venv):
  pip install websockets
  python test_core.py

What it does:
 - Simulation loop (update interval default 0.5s)
 - One stationary target placed to the EAST (x=+300, y=0)
 - Gatling fires a burst every 5 seconds
 - Simple hit-logic based on a simulated "price direction" (+1 => hit, -1 => miss)
 - Prints console logs
 - Broadcasts JSON packets to any WebSocket clients at ws://localhost:8765
"""

import asyncio
import json
import math
import random
import time
from dataclasses import dataclass, asdict
from typing import List, Dict, Any, Set

import websockets

# -------------------------
# Simulation parameters
# -------------------------
UPDATE_INTERVAL = 0.5      # seconds (foundation speed). We'll later reduce to 0.2 -> 0.1
GATLING_BURST_INTERVAL = 5.0  # seconds
RADAR_RANGE = 400          # visual radius (units)
GATLING_RANGE = 350        # effective range
CENTER = (0, 0)            # radar center

# Phase 1A target placement: EAST (x positive)
TARGET_EAST = {"id": "TGT-001", "x": 300.0, "y": 0.0, "vx": 0.0, "vy": 0.0}

# -------------------------
# Data classes
# -------------------------
@dataclass
class Target:
    id: str
    x: float
    y: float
    vx: float = 0.0
    vy: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

@dataclass
class Event:
    timestamp: float
    type: str
    payload: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        return {"timestamp": self.timestamp, "type": self.type, "payload": self.payload}


# -------------------------
# Simple Event Bus / Broadcaster
# -------------------------
class Broadcaster:
    def __init__(self):
        self._clients: Set[websockets.WebSocketServerProtocol] = set()
        self._lock = asyncio.Lock()

    async def register(self, ws: websockets.WebSocketServerProtocol):
        async with self._lock:
            self._clients.add(ws)
        print(f"[broadcaster] client registered: {ws.remote_address}")

    async def unregister(self, ws: websockets.WebSocketServerProtocol):
        async with self._lock:
            self._clients.discard(ws)
        print(f"[broadcaster] client disconnected: {ws.remote_address}")

    async def broadcast(self, packet: Dict[str, Any]):
        # send to all clients (best-effort; remove closed ones)
        if not self._clients:
            return
        message = json.dumps(packet)
        to_remove = []
        async with self._lock:
            for ws in list(self._clients):
                try:
                    await ws.send(message)
                except Exception:
                    to_remove.append(ws)
            for ws in to_remove:
                self._clients.discard(ws)


broadcaster = Broadcaster()

# -------------------------
# Simulation Engine
# -------------------------
class SimulationCore:
    def __init__(self, update_interval=UPDATE_INTERVAL):
        self.update_interval = update_interval
        self.targets: List[Target] = [Target(**TARGET_EAST)]
        self.start_time = time.time()
        self.last_gatling = self.start_time
        self.event_queue: asyncio.Queue = asyncio.Queue()

    def _distance(self, t: Target):
        dx = t.x - CENTER[0]
        dy = t.y - CENTER[1]
        return math.hypot(dx, dy)

    def _angle_to_target(self, t: Target):
        dx = t.x - CENTER[0]
        dy = t.y - CENTER[1]
        # angle in degrees, 0 at north, clockwise (for visualization you can transform)
        angle_rad = math.atan2(dy, dx)
        angle_deg = math.degrees(angle_rad)
        return (angle_deg + 360) % 360

    async def simulate_step(self):
        now = time.time()
        # Update targets (stationary in Phase 1A)
        # If moving phases, update pos here using vx, vy and elapsed dt

        # Build telemetry
        telemetry = {
            "time": now,
            "targets": [t.to_dict() for t in self.targets],
        }

        # Gatling logic: fire bursts every GATLING_BURST_INTERVAL
        if now - self.last_gatling >= GATLING_BURST_INTERVAL:
            self.last_gatling = now
            # For simplicity, gatling "scans" all targets and fires
            for t in self.targets:
                distance = self._distance(t)
                angle = self._angle_to_target(t)
                in_range = distance <= GATLING_RANGE

                # Simulate a "price direction" decision (placeholder for real data)
                price_dir = random.choice([-1, 1])  # -1 means down, +1 means up
                # The rule you described: up => hit, down => miss (you can invert)
                hit = (price_dir > 0) and in_range

                event_payload = {
                    "target_id": t.id,
                    "target_pos": {"x": t.x, "y": t.y},
                    "distance": distance,
                    "angle_deg": angle,
                    "in_range": in_range,
                    "price_dir": price_dir,
                    "hit": hit,
                }
                evt = Event(timestamp=now, type="gatling_fire", payload=event_payload)
                # publish to local queue and broadcaster
                await self.event_queue.put(evt)
                await broadcaster.broadcast({"event": evt.to_dict(), "telemetry": telemetry})
                # also print to console
                self._console_log(evt, telemetry)

    def _console_log(self, evt: Event, telemetry: Dict[str, Any]):
        ts = time.strftime("%H:%M:%S", time.localtime(evt.timestamp))
        p = evt.payload
        print(f"[{ts}] GATLING FIRE -> target={p['target_id']} pos=({p['target_pos']['x']:.0f},{p['target_pos']['y']:.0f}) "
              f"dist={p['distance']:.0f} angle={p['angle_deg']:.0f} range={p['in_range']} price_dir={p['price_dir']} hit={p['hit']}")

    async def run_loop(self):
        print("[sim] Starting simulation loop. Update interval:", self.update_interval)
        try:
            while True:
                await self.simulate_step()
                await asyncio.sleep(self.update_interval)
        except asyncio.CancelledError:
            print("[sim] Simulation loop cancelled, shutting down.")


# -------------------------
# WebSocket Server to broadcast simulation packets
# -------------------------
async def ws_handler(websocket, path):
    await broadcaster.register(websocket)
    try:
        # Keep the connection open until client disconnects
        while True:
            # Wait for ping or just sleep short
            try:
                msg = await asyncio.wait_for(websocket.recv(), timeout=60)
                # For this simple handler we ignore client messages.
            except asyncio.TimeoutError:
                # send a heartbeat/state packet occasionally
                state = {"type": "heartbeat", "time": time.time()}
                try:
                    await websocket.send(json.dumps(state))
                except Exception:
                    break
    except websockets.ConnectionClosed:
        pass
    finally:
        await broadcaster.unregister(websocket)

# -------------------------
# Startup & run
# -------------------------
async def main():
    sim = SimulationCore(update_interval=UPDATE_INTERVAL)

    # start websocket server
    ws_server = await websockets.serve(ws_handler, "0.0.0.0", 8765)
    print("[ws] WebSocket server listening on ws://localhost:8765")

    # run simulation loop
    sim_task = asyncio.create_task(sim.run_loop())

    # also run a light task that prints queue events (could drive the TUI)
    async def queue_watcher():
        while True:
            evt: Event = await sim.event_queue.get()
            # Here you can add logic to send events to an in-process TUI, etc.
            # For now we simply note it (console already printed in simulate)
            await asyncio.sleep(0)  # yield

    watcher_task = asyncio.create_task(queue_watcher())

    try:
        await sim_task
    finally:
        watcher_task.cancel()
        ws_server.close()
        await ws_server.wait_closed()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n[main] Interrupted by user. Exiting.")
