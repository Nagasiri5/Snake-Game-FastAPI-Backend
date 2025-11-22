from fastapi import FastAPI, WebSocket, WebSocketDisconnect   # FastAPI → main framework, WebSocket → real-time 2-way connection (browser ↔ server)
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles    # StaticFiles → serve HTML, JS, CSS files
from fastapi.responses import HTMLResponse     # HTMLResponse → send index.html as response
import asyncio                                 # asyncio → async tasks (game update)
from game import SnakeGame

app = FastAPI()    # FastAPI Initialization
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or restrict to your S3 domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount('/static', StaticFiles(directory='static'), name='static')  # Serve HTML/JS/CSS from static/ folder

# Single-player demo: one game per websocket connection

@app.get('/')       # Return static/index.html
async def index():
    return HTMLResponse(open('static/index.html').read())      # http://localhost:8000/ loads the HTML game page

@app.websocket('/ws')  # New snakegame for every individual client
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()            # Accepts the client’s connection
    game = SnakeGame(width=20, height=20)    # Creates a new game board (20x20) for new player

    async def sender():
        # send state 10x / sec
        try:
            while True:
                game.step()     # Update the game state (game.step())
                await websocket.send_json({'type': 'state', 'data': game.get_state()})
                if not game.alive:
                    await websocket.send_json({'type':'gameover', 'data': {'score': game.score}})
                    break
                await asyncio.sleep(0.1)  # Send the updated state (snake, food, score, etc.) to the frontend 10 times per second
        except Exception:
            pass

    sender_task = asyncio.create_task(sender())

    try:     
        while True:                  # Waits for JSON messages from the frontend
            msg = await websocket.receive_json()
            if msg.get('type') == 'dir':        # user pressed an arrow key → changes direction
                dx, dy = msg.get('dx'), msg.get('dy')
                game.set_direction(dx, dy)
            if msg.get('type') == 'reset':      # 'reset' → restart the game
                game.reset()

    # Exception Handling
    except WebSocketDisconnect:            # If the user closes the tab or disconnects → stop the sender loop.
        sender_task.cancel()
    except Exception:
        sender_task.cancel()

        await websocket.close()
