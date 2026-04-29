<!DOCTYPE html>
<html>
<head>
    <title>TMNT 2003: PURPLE NYC NIGHTS</title>
    <style>
        body { margin: 0; background: #0a0515; overflow: hidden; font-family: 'Orbitron', sans-serif; color: #a0f; }
        canvas { display: block; }
        #ui { position: absolute; top: 20px; left: 20px; background: rgba(20, 10, 40, 0.85); padding: 15px; border: 2px solid #a0f; box-shadow: 0 0 15px #a0f; pointer-events: none; z-index: 100; border-radius: 5px; }
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&display=swap');
    </style>
</head>
<body>
    <div id="ui">
        [ SECTOR <span id="lvl">1</span> ] <br>
        NEO-NYC: VIOLET DISTRICT<br>
        [ARROWS] MOVE/AIM | [S] THROW SAI
    </div>
    <canvas id="gameCanvas"></canvas>

<script>
const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');

let width, height, rooftopBase;
let currentLevel = 1;
let levelData = [];
let enemies = [];
let bullets = []; 
let cameraX = 0;
let animTick = 0;
let speechTimer = 0;
let screenShake = 0;

const player = {
    x: 100, y: 0, w: 50, h: 60,
    vx: 0, vy: 0, speed: 2.2, jumpForce: -20,
    grounded: false, color: '#2e5a1c', mask: '#ff0000', shell: '#5c4033'
};

const keys = {};

const backgroundBuildings = [];
for(let i=0; i<40; i++) {
    backgroundBuildings.push({
        x: i * 400, w: 250 + Math.random() * 200, h: 400 + Math.random() * 600,
        color: i % 2 === 0 ? '#150a25' : '#1a0d30', parallax: 0.3,
        windows: Math.random() > 0.5
    });
}

function generateLevel(num) {
    levelData = []; enemies = []; bullets = [];
    const length = 60 + (num * 3);
    
    // Safety Floor (The "Street" underneath)
    levelData.push({ x: -1000, y: height - 50, w: length * 350, h: 200, type: 'street' });

    for (let i = 0; i < length; i++) {
        let isGap = i > 4 && Math.random() < 0.25;
        if (!isGap) {
            let ry = height * 0.5 + (Math.random() * 200);
            levelData.push({ x: i * 300, y: ry, w: 260, h: height, type: 'roof' });
            if (i > 5 && Math.random() < 0.35) {
                enemies.push({ x: i * 300 + 100, y: ry - 100, phase: Math.random() * 6 });
            }
        }
    }
    levelData.push({ x: length * 300, y: height * 0.5, w: 400, h: height, type: 'goal' });
}

function resize() {
    width = canvas.width = window.innerWidth;
    height = canvas.height = window.innerHeight;
    generateLevel(currentLevel);
}
window.addEventListener('resize', resize);
resize();

window.addEventListener('keydown', e => {
    keys[e.code] = true;
    if(e.code === 'KeyS') shoot();
});
window.addEventListener('keyup', e => keys[e.code] = false);

function shoot() {
    let vx = 0, vy = 0;
    if (keys['ArrowUp']) vy = -18;
    else if (keys['ArrowDown']) vy = 18;
    else vx = 18 * (player.vx >= 0 ? 1 : -1);
    if (vx === 0 && vy === 0) vx = 18;
    bullets.push({ x: player.x + 25, y: player.y + 20, vx, vy, rotation: 0 });
}

function update() {
    if (keys['ArrowRight']) { player.vx += player.speed; }
    if (keys['ArrowLeft']) { player.vx -= player.speed; }
    player.vx *= 0.88; player.x += player.vx;
    player.vy += 0.85; player.y += player.vy;

    player.grounded = false;
    levelData.forEach(tile => {
        if (player.x + player.w > tile.x && player.x < tile.x + tile.w &&
            player.y + player.h > tile.y && player.y + player.h < tile.y + player.vy + 15) {
            player.y = tile.y - player.h; player.vy = 0; player.grounded = true;
            if (tile.type === 'goal') nextLevel();
        }
    });

    if (keys['ArrowUp'] && player.grounded) { player.vy = player.jumpForce; player.grounded = false; }

    enemies.forEach((en, i) => {
        en.y += Math.sin(Date.now()/300 + en.phase) * 1.2;
        bullets.forEach((b, bi) => {
            if (b.x > en.x && b.x < en.x+60 && b.y > en.y && b.y < en.y+60) {
                enemies.splice(i, 1); bullets.splice(bi, 1);
                speechTimer = 60; screenShake = 10;
            }
        });
    });

    cameraX += (player.x - cameraX - width / 3) * 0.1;
    bullets.forEach((b, i) => { 
        b.x += b.vx; b.y += b.vy; b.rotation += 0.5;
        if(Math.abs(b.x-player.x)>2000) bullets.splice(i,1); 
    });
    
    if (speechTimer > 0) speechTimer--;
    if (screenShake > 0) screenShake *= 0.9;
    animTick++;
}

function drawBackground() {
    // Purple Night Gradient
    let grd = ctx.createLinearGradient(0,0,0,height);
    grd.addColorStop(0, "#0a0515");
    grd.addColorStop(1, "#2a1040");
    ctx.fillStyle = grd;
    ctx.fillRect(0,0,width,height);

    backgroundBuildings.forEach(b => {
        let px = (b.x - cameraX * b.parallax) % (backgroundBuildings.length * 400);
        if (px < -600) px += backgroundBuildings.length * 400;
        ctx.fillStyle = b.color;
        ctx.fillRect(px, height - b.h, b.w, b.h);
        
        // Window lights
        if(b.windows) {
            ctx.fillStyle = "#80f4ff22";
            for(let r=0; r<6; r++) {
                for(let c=0; c<4; c++) {
                    ctx.fillRect(px + 20 + c*40, height - b.h + 40 + r*60, 15, 25);
                }
            }
        }
    });
}

function drawSpeechBubble(x, y) {
    ctx.save();
    ctx.translate(x + 50, y - 40);
    ctx.fillStyle = "white"; ctx.strokeStyle = "black"; ctx.lineWidth = 2;
    ctx.beginPath(); ctx.moveTo(0,0); ctx.lineTo(120,0); ctx.lineTo(120,-40); ctx.lineTo(0,-40); ctx.closePath();
    ctx.fill(); ctx.stroke();
    ctx.beginPath(); ctx.moveTo(10,0); ctx.lineTo(0,15); ctx.lineTo(20,0); ctx.fill(); ctx.stroke();
    ctx.fillStyle = "purple"; ctx.font = "bold 14px Orbitron"; ctx.textAlign = "center";
    ctx.fillText("COWABUNGA!", 60, -15);
    ctx.restore();
}

function drawRaphael(p) {
    ctx.save();
    ctx.translate(p.x + p.w/2, p.y + p.h/2);
    ctx.scale(p.vx >= 0 ? 1 : -1, 1);
    ctx.fillStyle = p.shell;
    ctx.beginPath(); ctx.ellipse(-5, 5, 24, 30, 0, 0, Math.PI * 2); ctx.fill();
    ctx.fillStyle = p.color;
    ctx.fillRect(-15, -10, 30, 35);
    let legMove = Math.sin(animTick * 0.25) * 15;
    ctx.strokeStyle = p.color; ctx.lineWidth = 7;
    ctx.beginPath(); ctx.moveTo(-8, 20); ctx.lineTo(-12 - (p.vx?legMove:0), 42); ctx.stroke();
    ctx.beginPath(); ctx.moveTo(8, 20); ctx.lineTo(12 + (p.vx?legMove:0), 42); ctx.stroke();
    ctx.fillStyle = '#e8c985'; ctx.fillRect(-12, -5, 24, 28);
    ctx.fillStyle = p.color;
    ctx.beginPath(); ctx.ellipse(12, -22, 20, 16, 0, 0, Math.PI * 2); ctx.fill();
    ctx.fillStyle = p.mask; ctx.fillRect(2, -28, 28, 10);
    ctx.beginPath(); ctx.moveTo(-5, -23); ctx.quadraticCurveTo(-30, -23 + Math.sin(animTick*0.15)*12, -45, -10);
    ctx.lineWidth = 5; ctx.strokeStyle = p.mask; ctx.stroke();
    ctx.fillStyle = '#fff'; ctx.fillRect(14, -26, 5, 5); ctx.fillRect(23, -26, 5, 5);
    ctx.restore();
}

function draw() {
    drawBackground();
    ctx.save();
    let sx = (Math.random() - 0.5) * screenShake;
    let sy = (Math.random() - 0.5) * screenShake;
    ctx.translate(-cameraX + sx, sy);

    levelData.forEach(tile => {
        // Grey and Purple platform scheme
        ctx.fillStyle = "#201535"; 
        ctx.strokeStyle = tile.type === 'goal' ? '#ff0' : "#a0f";
        ctx.lineWidth = 4;
        ctx.fillRect(tile.x, tile.y, tile.w, tile.h);
        ctx.strokeRect(tile.x, tile.y, tile.w, tile.h);
        
        // Roof detail
        if(tile.type === 'roof') {
            ctx.fillStyle = "#150a25";
            ctx.fillRect(tile.x + 20, tile.y + 10, tile.w - 40, 10);
        }
    });

    enemies.forEach(en => {
        ctx.save();
        ctx.translate(en.x + 30, en.y + 30);
        ctx.shadowBlur = 15; ctx.shadowColor = "#0ff";
        ctx.fillStyle = "#ff00ff";
        ctx.beginPath(); ctx.arc(0, 0, 24, 0, Math.PI*2); ctx.fill();
        ctx.restore();
    });

    drawRaphael(player);
    bullets.forEach(b => {
        ctx.save();
        ctx.translate(b.x, b.y);
        ctx.rotate(b.rotation);
        ctx.strokeStyle = '#fff'; ctx.lineWidth = 3;
        ctx.beginPath(); ctx.moveTo(0, -15); ctx.lineTo(0, 15); ctx.stroke();
        ctx.beginPath(); ctx.moveTo(-8, 0); ctx.lineTo(8, 0); ctx.stroke();
        ctx.restore();
    });

    if (speechTimer > 0) drawSpeechBubble(player.x, player.y);

    ctx.restore();
    update();
    requestAnimationFrame(draw);
}

function nextLevel() {
    currentLevel++;
    document.getElementById('lvl').innerText = currentLevel;
    player.x = 100; player.y = 0;
    generateLevel(currentLevel);
}

draw();
</script>
</body>
</html>
