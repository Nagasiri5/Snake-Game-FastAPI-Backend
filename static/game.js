// static/game.js
const canvas = document.getElementById('c');
const ctx = canvas.getContext('2d');
const scoreEl = document.getElementById('score');
const resetBtn = document.getElementById('reset');

const ws = new WebSocket((location.protocol === 'https:' ? 'wss://' : 'ws://') + location.host + '/ws');
let state = null;

ws.onopen = () => console.log('ws open');
ws.onmessage = (ev) => {
  const msg = JSON.parse(ev.data);
  if (msg.type === 'state') {
    state = msg.data;
    render(state);
  } else if (msg.type === 'gameover') {
    alert('Game over! Score: ' + msg.data.score);
  }
};

function render(s) {
  const w = s.width, h = s.height;
  const cw = canvas.width / w, ch = canvas.height / h;
  ctx.clearRect(0,0,canvas.width, canvas.height);

  // food
  if (s.food) {
    ctx.fillStyle = 'red';
    ctx.fillRect(s.food[0]*cw, s.food[1]*ch, cw, ch);
  }

  // snake
  ctx.fillStyle = 'green';
  s.snake.forEach(([x,y]) => ctx.fillRect(x*cw, y*ch, cw, ch));

  scoreEl.textContent = s.score;
}

// keyboard
window.addEventListener('keydown', e => {
  const map = {
    'ArrowUp': [0,-1],
    'ArrowDown': [0,1],
    'ArrowLeft': [-1,0],
    'ArrowRight': [1,0]
  };
  if (map[e.key]) {
    ws.send(JSON.stringify({type:'dir', dx: map[e.key][0], dy: map[e.key][1]}));
  }
});

resetBtn.addEventListener('click', () => ws.send(JSON.stringify({type:'reset'})));