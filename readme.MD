🐍 FastAPI Snake Game

A real-time Snake Game backend built using Python, FastAPI, and WebSockets.
This project delivers a fully interactive browser-based Snake experience powered by a lightweight, modular backend designed for real-time state updates.

🚀 Features

Real-time gameplay using WebSockets

Modular Python game engine (clean and easy to extend)

FastAPI backend for smooth routing and communication

Static HTML/JS client to play the game in your browser

Auto-reload support for development using Uvicorn

Lightweight & beginner-friendly structure

📂 Project Structure
.
├── main.py
├── game.py
├── static/
│   └── index.html
│   └── game.js
│   └── style.css
└── requirements.txt

🛠️ Installation & Setup

Clone the repository

git clone <https://github.com/Sabbir-Azim/Snake-Game-FastAPI-Backend.git>


pip install -r requirements.txt


Run the FastAPI server

uvicorn main:app --reload


Open the game in your browser

👉 http://localhost:8000/static/index.html

🎮 How It Works

Each client connects via WebSocket

The backend maintains:

Snake position

Direction

Food generation

Game-over logic

The server sends continuous state updates → the browser renders them in real time.

📦 Tech Stack

Python

FastAPI

Uvicorn

WebSockets

HTML + JS (for the client)

🤝 Contributing

Feel free to submit issues or open PRs if you want to improve the game, add UI, or extend game logic!

📜 License

MIT License — use and modify freely.