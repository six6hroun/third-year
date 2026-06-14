// ==================== ГЛОБАЛЬНЫЕ ПЕРЕМЕННЫЕ ====================
let scene, camera, renderer, controls;
let surfaceMesh;
let beeSpheres = [];
let bestMarker = null;

let bees = [];
let bestPosition = [0, 0];
let bestValue = Infinity;
let currentIteration = 0;
let maxIterations = 200;
let isRunning = false;
let animationTimeout = null;

let chart;
let chartData = [];

// Параметры пчелиного алгоритма
let scoutsCount = 16;
let eliteSites = 2;
let goodSites = 3;
let beesPerElite = 7;
let beesPerGood = 4;
let searchRadius = 0.2;

// Область поиска (зависит от функции)
let bounds = { xmin: -5.12, xmax: 5.12, ymin: -5.12, ymax: 5.12 };
let currentFunction = "rastrigin";

// ==================== ЦЕЛЕВЫЕ ФУНКЦИИ ====================
function rastrigin(x, y) {
    return 20 + (x*x - 10 * Math.cos(2 * Math.PI * x)) + (y*y - 10 * Math.cos(2 * Math.PI * y));
}

function rosenbrock(x, y) {
    return (1 - x)*(1 - x) + 100 * (y - x*x)*(y - x*x);
}

function himmelblau(x, y) {
    return (x*x + y - 11)*(x*x + y - 11) + (x + y*y - 7)*(x + y*y - 7);
}

function getFunction(name) {
    if (name === "rastrigin") {
        return { fn: rastrigin, bounds: { xmin: -5.12, xmax: 5.12, ymin: -5.12, ymax: 5.12 }, name: "Растригина" };
    }
    if (name === "rosenbrock") {
        return { fn: rosenbrock, bounds: { xmin: -2, xmax: 2, ymin: -1, ymax: 3 }, name: "Розенброка" };
    }
    if (name === "himmelblau") {
        return { fn: himmelblau, bounds: { xmin: -5, xmax: 5, ymin: -5, ymax: 5 }, name: "Химмельблау" };
    }
    return { fn: rastrigin, bounds: { xmin: -5.12, xmax: 5.12, ymin: -5.12, ymax: 5.12 }, name: "Растригина" };
}

// ==================== ПЧЕЛИНЫЙ АЛГОРИТМ ====================
function initBees() {
    const funcData = getFunction(currentFunction);
    const targetFn = funcData.fn;
    bounds = funcData.bounds;
    
    bees = [];
    for (let i = 0; i < scoutsCount; i++) {
        let x = rand(bounds.xmin, bounds.xmax);
        let y = rand(bounds.ymin, bounds.ymax);
        bees.push({
            position: [x, y],
            value: targetFn(x, y)
        });
    }
    updateBest();
}

function updateBest() {
    const targetFn = getFunction(currentFunction).fn;
    for (let bee of bees) {
        let val = targetFn(bee.position[0], bee.position[1]);
        if (val < bestValue) {
            bestValue = val;
            bestPosition = [bee.position[0], bee.position[1]];
        }
    }
}

// Одна итерация пчелиного алгоритма
function beesIteration() {
    const funcData = getFunction(currentFunction);
    const targetFn = funcData.fn;
    
    // 1. Вычисляем значения всех пчел
    for (let bee of bees) {
        bee.value = targetFn(bee.position[0], bee.position[1]);
    }
    
    // 2. Сортируем по возрастанию (лучшие первые)
    bees.sort((a, b) => a.value - b.value);
    
    // 3. Выделяем элитные и перспективные участки
    let elite = bees.slice(0, eliteSites);
    let good = bees.slice(eliteSites, eliteSites + goodSites);
    
    // 4. Создаем новую популяцию
    let newBees = [];
    
    // Элитные участки
    for (let site of elite) {
        for (let i = 0; i < beesPerElite; i++) {
            let newX = site.position[0] + rand(-searchRadius, searchRadius);
            let newY = site.position[1] + rand(-searchRadius, searchRadius);
            newX = clamp(newX, bounds.xmin, bounds.xmax);
            newY = clamp(newY, bounds.ymin, bounds.ymax);
            newBees.push({
                position: [newX, newY],
                value: targetFn(newX, newY)
            });
        }
    }
    
    // Перспективные участки
    for (let site of good) {
        for (let i = 0; i < beesPerGood; i++) {
            let newX = site.position[0] + rand(-searchRadius, searchRadius);
            let newY = site.position[1] + rand(-searchRadius, searchRadius);
            newX = clamp(newX, bounds.xmin, bounds.xmax);
            newY = clamp(newY, bounds.ymin, bounds.ymax);
            newBees.push({
                position: [newX, newY],
                value: targetFn(newX, newY)
            });
        }
    }
    
    // Пчелы-разведчики
    let scouts = [];
    for (let i = 0; i < scoutsCount; i++) {
        let x = rand(bounds.xmin, bounds.xmax);
        let y = rand(bounds.ymin, bounds.ymax);
        scouts.push({
            position: [x, y],
            value: targetFn(x, y)
        });
    }
    
    // Объединяем
    let allBees = [...newBees, ...scouts];
    allBees.sort((a, b) => a.value - b.value);
    bees = allBees.slice(0, scoutsCount + beesPerElite * eliteSites + beesPerGood * goodSites);
    
    updateBest();
    return bestValue;
}

// ==================== 3D ВИЗУАЛИЗАЦИЯ ====================
function createSurface() {
    const funcData = getFunction(currentFunction);
    const targetFn = funcData.fn;
    const b = funcData.bounds;
    
    const segments = 140;
    const vertices = [];
    const colors = [];
    const indices = [];
    
    let minZ = Infinity, maxZ = -Infinity;
    const zvals = [];
    
    for (let i = 0; i <= segments; i++) {
        const x = b.xmin + (i / segments) * (b.xmax - b.xmin);
        for (let j = 0; j <= segments; j++) {
            const y = b.ymin + (j / segments) * (b.ymax - b.ymin);
            let z = targetFn(x, y);
            if (currentFunction === "rosenbrock") z = Math.min(z, 500);
            if (currentFunction === "himmelblau") z = Math.min(z, 200);
            zvals.push(z);
            minZ = Math.min(minZ, z);
            maxZ = Math.max(maxZ, z);
        }
    }
    
    let range = Math.max(maxZ - minZ, 0.1);
    let k = 0;
    for (let i = 0; i <= segments; i++) {
        const x = b.xmin + (i / segments) * (b.xmax - b.xmin);
        for (let j = 0; j <= segments; j++) {
            const y = b.ymin + (j / segments) * (b.ymax - b.ymin);
            let z = zvals[k++];
            let t = (z - minZ) / range;
            let height = t * 3;
            
            vertices.push(x, height, y);
            // Цвет от желтого (низ) к красному (высоко)
            colors.push(1, 0.5 + t * 0.5, 0.2);
        }
    }
    
    for (let i = 0; i < segments; i++) {
        for (let j = 0; j < segments; j++) {
            const a = i * (segments + 1) + j;
            const bIdx = a + 1;
            const c = a + segments + 1;
            const d = c + 1;
            indices.push(a, bIdx, c);
            indices.push(bIdx, d, c);
        }
    }
    
    const geom = new THREE.BufferGeometry();
    geom.setAttribute("position", new THREE.Float32BufferAttribute(vertices, 3));
    geom.setAttribute("color", new THREE.Float32BufferAttribute(colors, 3));
    geom.setIndex(indices);
    geom.computeVertexNormals();
    
    return new THREE.Mesh(geom, new THREE.MeshPhongMaterial({ vertexColors: true, side: THREE.DoubleSide, shininess: 60 }));
}

function updateSurface() {
    if (surfaceMesh) scene.remove(surfaceMesh);
    surfaceMesh = createSurface();
    scene.add(surfaceMesh);
}

function updateBeesVisualization() {
    beeSpheres.forEach(s => scene.remove(s));
    beeSpheres = [];
    
    if (!bees.length) return;
    
    const funcData = getFunction(currentFunction);
    const targetFn = funcData.fn;
    const b = funcData.bounds;
    
    let minVal = Infinity, maxVal = -Infinity;
    for (let bee of bees) {
        let val = targetFn(bee.position[0], bee.position[1]);
        if (currentFunction === "rosenbrock") val = Math.min(val, 500);
        if (currentFunction === "himmelblau") val = Math.min(val, 200);
        minVal = Math.min(minVal, val);
        maxVal = Math.max(maxVal, val);
    }
    let range = Math.max(maxVal - minVal, 0.1);
    
    for (let bee of bees) {
        let val = targetFn(bee.position[0], bee.position[1]);
        if (currentFunction === "rosenbrock") val = Math.min(val, 500);
        if (currentFunction === "himmelblau") val = Math.min(val, 200);
        let t = (val - minVal) / range;
        let height = t * 3;
        
        const sphere = new THREE.Mesh(
            new THREE.SphereGeometry(0.07, 16, 16),
            new THREE.MeshStandardMaterial({ color: 0xffaa33 })
        );
        sphere.position.set(bee.position[0], height + 0.05, bee.position[1]);
        scene.add(sphere);
        beeSpheres.push(sphere);
    }
    
    if (bestMarker) scene.remove(bestMarker);
    let bestVal = targetFn(bestPosition[0], bestPosition[1]);
    if (currentFunction === "rosenbrock") bestVal = Math.min(bestVal, 500);
    if (currentFunction === "himmelblau") bestVal = Math.min(bestVal, 200);
    let bestT = (bestVal - minVal) / range;
    let bestHeight = bestT * 3;
    
    bestMarker = new THREE.Mesh(
        new THREE.SphereGeometry(0.11, 24, 24),
        new THREE.MeshStandardMaterial({ color: 0xff3333 })
    );
    bestMarker.position.set(bestPosition[0], bestHeight + 0.08, bestPosition[1]);
    scene.add(bestMarker);
}

// ==================== UI ОБНОВЛЕНИЯ ====================
function updateUI() {
    document.getElementById("iter-count").textContent = currentIteration;
    document.getElementById("best-x").textContent = bestPosition[0].toFixed(6);
    document.getElementById("best-y").textContent = bestPosition[1].toFixed(6);
    document.getElementById("best-f").textContent = bestValue.toFixed(8);
}

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
            plugins: { legend: { position: "top" } }
        }
    });
}

function updateChart(value) {
    chart.data.labels.push(currentIteration);
    chart.data.datasets[0].data.push(value);
    chart.update();
}

function resetChart() {
    chart.data.labels = [];
    chart.data.datasets[0].data = [];
    chart.update();
}

// ==================== УПРАВЛЕНИЕ ====================
function stopAlgorithm() {
    if (animationTimeout) clearTimeout(animationTimeout);
    isRunning = false;
}

function startAlgorithm() {
    if (isRunning) stopAlgorithm();
    
    scoutsCount = parseInt(document.getElementById("scouts-count").value);
    eliteSites = parseInt(document.getElementById("elite-sites").value);
    goodSites = parseInt(document.getElementById("good-sites").value);
    beesPerElite = parseInt(document.getElementById("bees-elite").value);
    beesPerGood = parseInt(document.getElementById("bees-good").value);
    searchRadius = parseFloat(document.getElementById("search-radius").value);
    maxIterations = parseInt(document.getElementById("max-iter").value);
    currentFunction = document.getElementById("function-select").value;
    
    currentIteration = 0;
    bestValue = Infinity;
    resetChart();
    updateSurface();
    initBees();
    updateUI();
    updateBeesVisualization();
    
    isRunning = true;
    
    function step() {
        if (!isRunning) return;
        if (currentIteration >= maxIterations) {
            stopAlgorithm();
            return;
        }
        
        let val = beesIteration();
        currentIteration++;
        updateUI();
        updateBeesVisualization();
        updateChart(val);
        
        animationTimeout = setTimeout(step, 60);
    }
    
    step();
}

function resetAlgorithm() {
    stopAlgorithm();
    currentFunction = document.getElementById("function-select").value;
    updateSurface();
    bestValue = Infinity;
    currentIteration = 0;
    initBees();
    resetChart();
    updateUI();
    updateBeesVisualization();
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
    
    const ambient = new THREE.AmbientLight(0x404060);
    scene.add(ambient);
    const dirLight = new THREE.DirectionalLight(0xffffff, 1);
    dirLight.position.set(5, 10, 7);
    scene.add(dirLight);
    const fillLight = new THREE.PointLight(0x4466cc, 0.3);
    fillLight.position.set(-3, 4, 5);
    scene.add(fillLight);
    
    surfaceMesh = createSurface();
    scene.add(surfaceMesh);
    
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

// ==================== ВСПОМОГАТЕЛЬНЫЕ ====================
function rand(a, b) { return a + Math.random() * (b - a); }
function clamp(v, a, b) { return Math.max(a, Math.min(b, v)); }

// ==================== ЗАПУСК ====================
document.addEventListener("DOMContentLoaded", () => {
    init3D();
    initChart();
    initBees();
    updateUI();
    updateBeesVisualization();
    
    document.getElementById("start-btn").addEventListener("click", startAlgorithm);
    document.getElementById("reset-btn").addEventListener("click", resetAlgorithm);
    document.getElementById("function-select").addEventListener("change", resetAlgorithm);
});