// ==================== ГЛОБАЛЬНЫЕ ПЕРЕМЕННЫЕ ====================
let scene, camera, renderer, controls;
let surfaceMesh;
let particleSpheres = [];
let bestMarker = null;

let swarm = [];
let globalBestPosition = [0, 0];
let globalBestValue = Infinity;

let currentIteration = 0;
let maxIterations = 200;
let isRunning = false;
let animFrame = null;
let animationTimeout = null;

let chart;
let chartData = [];

// Границы области (функция Растригина определена на [-5.12, 5.12])
const X_MIN = -5.12;
const X_MAX = 5.12;
const Y_MIN = -5.12;
const Y_MAX = 5.12;

// Параметры PSO
let inertia = 0.729;
let c1 = 1.494;
let c2 = 1.494;
let animationDelay = 100; // задержка в мс

// ==================== ФУНКЦИЯ РАСТРИГИНА ====================
function rastrigin(x, y) {
    return 20 + (x*x - 10 * Math.cos(2 * Math.PI * x)) + (y*y - 10 * Math.cos(2 * Math.PI * y));
}

// ==================== ИНИЦИАЛИЗАЦИЯ РОЯ ====================
function initSwarm(size) {
    swarm = [];
    for (let i = 0; i < size; i++) {
        let pos = [rand(X_MIN, X_MAX), rand(Y_MIN, Y_MAX)];
        let vel = [rand(-1, 1), rand(-1, 1)];
        let fit = rastrigin(pos[0], pos[1]);
        
        swarm.push({
            position: pos,
            velocity: vel,
            bestPos: [pos[0], pos[1]],
            bestVal: fit
        });
    }
    
    // Находим глобальный лучший
    globalBestValue = Infinity;
    for (let p of swarm) {
        if (p.bestVal < globalBestValue) {
            globalBestValue = p.bestVal;
            globalBestPosition = [p.bestPos[0], p.bestPos[1]];
        }
    }
}

// ==================== ОДНА ИТЕРАЦИЯ PSO ====================
function psoIteration() {
    let newGlobalBest = globalBestValue;
    let newGlobalBestPos = [globalBestPosition[0], globalBestPosition[1]];
    
    for (let p of swarm) {
        // Случайные числа
        let r1 = Math.random();
        let r2 = Math.random();
        
        // Обновление скорости
        let newVx = inertia * p.velocity[0] +
                    c1 * r1 * (p.bestPos[0] - p.position[0]) +
                    c2 * r2 * (globalBestPosition[0] - p.position[0]);
        
        let newVy = inertia * p.velocity[1] +
                    c1 * r1 * (p.bestPos[1] - p.position[1]) +
                    c2 * r2 * (globalBestPosition[1] - p.position[1]);
        
        // Обновление позиции
        let newX = p.position[0] + newVx;
        let newY = p.position[1] + newVy;
        
        // Ограничение границ
        newX = clamp(newX, X_MIN, X_MAX);
        newY = clamp(newY, Y_MIN, Y_MAX);
        
        p.velocity = [newVx, newVy];
        p.position = [newX, newY];
        
        let fitness = rastrigin(newX, newY);
        
        // Обновление личного лучшего
        if (fitness < p.bestVal) {
            p.bestVal = fitness;
            p.bestPos = [newX, newY];
        }
        
        // Обновление глобального лучшего
        if (p.bestVal < newGlobalBest) {
            newGlobalBest = p.bestVal;
            newGlobalBestPos = [p.bestPos[0], p.bestPos[1]];
        }
    }
    
    globalBestValue = newGlobalBest;
    globalBestPosition = newGlobalBestPos;
}

// ==================== 3D ВИЗУАЛИЗАЦИЯ ПОВЕРХНОСТИ ====================
function createSurface() {
    const segments = 140;
    const vertices = [];
    const colors = [];
    const indices = [];
    
    let minZ = Infinity;
    let maxZ = -Infinity;
    const zvals = [];
    
    // Сначала вычисляем все значения для нормализации
    for (let i = 0; i <= segments; i++) {
        const x = X_MIN + (i / segments) * (X_MAX - X_MIN);
        for (let j = 0; j <= segments; j++) {
            const y = Y_MIN + (j / segments) * (Y_MAX - Y_MIN);
            const z = rastrigin(x, y);
            zvals.push(z);
            minZ = Math.min(minZ, z);
            maxZ = Math.max(maxZ, z);
        }
    }
    
    let k = 0;
    for (let i = 0; i <= segments; i++) {
        const x = X_MIN + (i / segments) * (X_MAX - X_MIN);
        for (let j = 0; j <= segments; j++) {
            const y = Y_MIN + (j / segments) * (Y_MAX - Y_MIN);
            let z = zvals[k++];
            
            const zn = (z - minZ) / (maxZ - minZ);
            const height = zn * 3;
            
            vertices.push(x, height, y);
            
            // Цвет: от синего (низ) к красному (высоко)
            const r = zn;
            const g = 0.2 + zn * 0.5;
            const b = 1 - zn;
            colors.push(r, g, b);
        }
    }
    
    for (let i = 0; i < segments; i++) {
        for (let j = 0; j < segments; j++) {
            const a = i * (segments + 1) + j;
            const b = a + 1;
            const c = a + segments + 1;
            const d = c + 1;
            indices.push(a, b, c);
            indices.push(b, d, c);
        }
    }
    
    const geom = new THREE.BufferGeometry();
    geom.setAttribute("position", new THREE.Float32BufferAttribute(vertices, 3));
    geom.setAttribute("color", new THREE.Float32BufferAttribute(colors, 3));
    geom.setIndex(indices);
    geom.computeVertexNormals();
    
    return new THREE.Mesh(geom, new THREE.MeshPhongMaterial({
        vertexColors: true,
        side: THREE.DoubleSide,
        shininess: 60
    }));
}

// ==================== ВИЗУАЛИЗАЦИЯ ЧАСТИЦ ====================
function updateVisualization() {
    // Удаляем старые частицы
    particleSpheres.forEach(s => scene.remove(s));
    particleSpheres = [];
    
    if (!swarm.length) return;
    
    // Вычисляем диапазон высот для масштабирования
    let minVal = Infinity, maxVal = -Infinity;
    for (let p of swarm) {
        let val = rastrigin(p.position[0], p.position[1]);
        minVal = Math.min(minVal, val);
        maxVal = Math.max(maxVal, val);
    }
    
    for (let p of swarm) {
        const val = rastrigin(p.position[0], p.position[1]);
        const t = (val - minVal) / (maxVal - minVal);
        const height = t * 3;
        
        // СИНИЕ и БОЛЬШИЕ частицы (радиус 0.1 вместо 0.05)
        const sphere = new THREE.Mesh(
            new THREE.SphereGeometry(0.12, 24, 24),  // Увеличен размер
            new THREE.MeshStandardMaterial({ 
                color: 0x3388ff,      // Ярко-синий
                emissive: 0x002244,   // Свечение
                shininess: 80,
                metalness: 0.3
            })
        );
        sphere.position.set(p.position[0], height + 0.08, p.position[1]);
        scene.add(sphere);
        particleSpheres.push(sphere);
    }
    
    // Лучшая частица (золотая/оранжевая, тоже увеличенная)
    if (bestMarker) scene.remove(bestMarker);
    const bestVal = rastrigin(globalBestPosition[0], globalBestPosition[1]);
    const bestT = (bestVal - minVal) / (maxVal - minVal);
    const bestHeight = bestT * 3;
    
    bestMarker = new THREE.Mesh(
        new THREE.SphereGeometry(0.15, 32, 32),  // Ещё больше
        new THREE.MeshStandardMaterial({ 
            color: 0xff6600,      // Оранжевый
            emissive: 0x442200,
            shininess: 90,
            metalness: 0.2
        })
    );
    bestMarker.position.set(globalBestPosition[0], bestHeight + 0.1, globalBestPosition[1]);
    scene.add(bestMarker);
}

// ==================== ОБНОВЛЕНИЕ UI ====================
function updateUI() {
    document.getElementById("iter-count").textContent = currentIteration;
    document.getElementById("best-x").textContent = globalBestPosition[0].toFixed(6);
    document.getElementById("best-y").textContent = globalBestPosition[1].toFixed(6);
    document.getElementById("best-f").textContent = globalBestValue.toFixed(8);
}

// ==================== ГРАФИК СХОДИМОСТИ ====================
function initChart() {
    const ctx = document.getElementById("chart").getContext("2d");
    chart = new Chart(ctx, {
        type: "line",
        data: {
            labels: [],
            datasets: [{
                label: "Лучшее f(x,y)",
                data: [],
                borderColor: "red",
                fill: false,
                tension: 0.1
            }]
        },
        options: {
            responsive: true,
            animation: false,
            plugins: {
                legend: { position: "top" }
            }
        }
    });
}

function updateChart() {
    chart.data.labels.push(currentIteration);
    chart.data.datasets[0].data.push(globalBestValue);
    chart.update();
}

function resetChart() {
    chart.data.labels = [];
    chart.data.datasets[0].data = [];
    chart.update();
}

// ==================== АЛГОРИТМ (ЦИКЛ С ЗАДЕРЖКОЙ) ====================
function stopAlgorithm() {
    if (animFrame) {
        cancelAnimationFrame(animFrame);
        animFrame = null;
    }
    if (animationTimeout) {
        clearTimeout(animationTimeout);
        animationTimeout = null;
    }
    isRunning = false;
}

function startAlgorithm() {
    if (isRunning) stopAlgorithm();
    
    // Читаем параметры
    const swarmSize = parseInt(document.getElementById("swarm-size").value);
    maxIterations = parseInt(document.getElementById("max-iter").value);
    inertia = parseFloat(document.getElementById("inertia").value);
    c1 = parseFloat(document.getElementById("c1").value);
    c2 = parseFloat(document.getElementById("c2").value);
    animationDelay = parseInt(document.getElementById("animation-delay").value);
    
    currentIteration = 0;
    chartData = [];
    resetChart();
    
    initSwarm(swarmSize);
    updateUI();
    updateVisualization();
    
    isRunning = true;
    
    // Рекурсивная функция с задержкой вместо requestAnimationFrame
    function stepWithDelay() {
        if (!isRunning) return;
        if (currentIteration >= maxIterations) {
            stopAlgorithm();
            return;
        }
        
        psoIteration();
        currentIteration++;
        
        updateUI();
        updateVisualization();
        updateChart();
        
        // Используем setTimeout для控制 скорости (задержка в мс)
        animationTimeout = setTimeout(stepWithDelay, animationDelay);
    }
    
    stepWithDelay();
}

function resetAlgorithm() {
    stopAlgorithm();
    
    const swarmSize = parseInt(document.getElementById("swarm-size").value);
    currentIteration = 0;
    
    initSwarm(swarmSize);
    resetChart();
    updateUI();
    updateVisualization();
}

// ==================== ВСПОМОГАТЕЛЬНЫЕ ====================
function rand(a, b) {
    return a + Math.random() * (b - a);
}

function clamp(v, a, b) {
    return Math.max(a, Math.min(b, v));
}

// ==================== 3D СЦЕНА ====================
function init3D() {
    scene = new THREE.Scene();
    scene.background = new THREE.Color(0xffffff);
    scene.fog = new THREE.FogExp2(0xffffff, 0.008);
    
    camera = new THREE.PerspectiveCamera(45, window.innerWidth / window.innerHeight, 0.1, 1000);
    camera.position.set(8, 6, 8);
    camera.lookAt(0, 1.5, 0);
    
    renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setSize(window.innerWidth, window.innerHeight);
    document.body.appendChild(renderer.domElement);
    
    controls = new THREE.OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;
    controls.dampingFactor = 0.05;
    controls.target.set(0, 1.5, 0);
    
    // Освещение
    const ambient = new THREE.AmbientLight(0x404060);
    scene.add(ambient);
    const dirLight = new THREE.DirectionalLight(0xffffff, 1);
    dirLight.position.set(5, 10, 7);
    scene.add(dirLight);
    const fillLight = new THREE.PointLight(0x4466cc, 0.3);
    fillLight.position.set(-3, 4, 5);
    scene.add(fillLight);
    
    // Дополнительный свет для подсветки синих частиц
    const backLight = new THREE.PointLight(0x3366ff, 0.2);
    backLight.position.set(0, 3, 0);
    scene.add(backLight);
    
    // Поверхность
    const surface = createSurface();
    scene.add(surface);
    
    // Сетка
    const grid = new THREE.GridHelper(15, 20, 0x888888, 0xcccccc);
    grid.position.y = -0.3;
    scene.add(grid);
    
    animate();
}

function animate() {
    requestAnimationFrame(animate);
    controls.update();
    renderer.render(scene, camera);
}

window.addEventListener("resize", () => {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
});

// ==================== ЗАПУСК ====================
document.addEventListener("DOMContentLoaded", () => {
    init3D();
    initChart();
    
    document.getElementById("start-btn").addEventListener("click", startAlgorithm);
    document.getElementById("reset-btn").addEventListener("click", resetAlgorithm);
    
    // Инициализация роя по умолчанию
    initSwarm(80);
    updateUI();
    updateVisualization();
});