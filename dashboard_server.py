import asyncio
import json
from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse

app = FastAPI()

html = """
<!DOCTYPE html>
<html>
<head>
<title>Warhead System Dashboard</title>
<style>
body {
  background: #111;
  color: #0f0;
  font-family: monospace;
  text-align: center;
}
#radar {
  width: 600px;
  height: 600px;
  border: 2px solid #0f0;
  border-radius: 50%;
  margin: auto;
  position: relative;
}
.target {
  width: 8px;
  height: 8px;
  background: red;
  border-radius: 50%;
  position: absolute;
}
</style>
</head>
<body>
<h1>Warhead Live Radar Simulation</h1>
<div id="radar"></div>

<script>
let ws = new WebSocket("ws://localhost:8000/ws");

ws.onmessage = function(event) {
    const data = JSON.parse(event.data);

    let radar = document.getElementById("radar");
    radar.innerHTML = "";

    data.targets.forEach(t => {
        let dot = document.createElement("div");
        dot.className = "target";
        dot.style.left = (300 + t.x) + "px";
        dot.style.top = (300 - t.y) + "px";
        radar.appendChild(dot);
    });
}
</script>
</body>
</html>
"""

@app.get("/")
async def get():
    return HTMLResponse(html)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    # SAMPLE SIMULATION LOOP (we replace this with the real one)
    import math
    angle = 0

    while True:
        # Dummy targets flying in circles
        targets = [
            {"x": 200 * math.cos(angle), "y": 200 * math.sin(angle)},
            {"x": 100 * math.cos(-angle), "y": 100 * math.sin(-angle)},
        ]

        await websocket.send_text(json.dumps({"targets": targets}))

        angle += 0.1
        await asyncio.sleep(0.05)
