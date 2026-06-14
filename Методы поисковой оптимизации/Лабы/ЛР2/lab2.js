// Глобальные переменные
let scene, camera, renderer, controls;
let surface, region, trajectory, points = [];
let startSphere, finalSphere;
let chart;

// Константы
const EPS = 1e-10;

// Инициализация при загрузке
init();
animate();

function init() {
    // Сцена
    scene = new THREE.Scene();
    scene.background = new THREE.Color(0x111122);

    // Камера
    camera = new THREE.PerspectiveCamera(
        45,
        window.innerWidth / window.innerHeight,
        0.1,
        1000
    );
    camera.position.set(4, 3, 6);
    camera.lookAt(0.5, 0, 0.5);

    // Рендерер
    renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.shadowMap.enabled = true;
    renderer.shadowMap.type = THREE.PCFSoftShadowMap;
    document.body.appendChild(renderer.domElement);

    // Освещение
    const ambientLight = new THREE.AmbientLight(0x404060);
    scene.add(ambientLight);

    const dirLight = new THREE.DirectionalLight(0xffffff, 1);
    dirLight.position.set(5, 10, 7);
    dirLight.castShadow = true;
    dirLight.shadow.mapSize.width = 1024;
    dirLight.shadow.mapSize.height = 1024;
    scene.add(dirLight);

    const backLight = new THREE.PointLight(0x4466ff, 0.5);
    backLight.position.set(-2, 1, -2);
    scene.add(backLight);

    // Вспомогательные элементы
    const gridHelper = new THREE.GridHelper(5, 20, 0x88aaff, 0x335588);
    gridHelper.position.y = -0.01;
    scene.add(gridHelper);

    const axesHelper = new THREE.AxesHelper(3);
    scene.add(axesHelper);

    // Загрузка OrbitControls
    const script = document.createElement('script');
    script.src = "https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js";
    script.onload = () => {
        controls = new THREE.OrbitControls(camera, renderer.domElement);
        controls.enableDamping = true;
        controls.dampingFactor = 0.05;
        controls.autoRotate = false;
        controls.target.set(0.5, 0, 0.5);
        controls.maxPolarAngle = Math.PI / 2;
    };
    document.head.appendChild(script);

    // Создание поверхности
    createSurface();
    
    // Создание сфер для точек
    startSphere = new THREE.Mesh(
        new THREE.SphereGeometry(0.08, 32),
        new THREE.MeshStandardMaterial({ 
            color: 0xff3333,
            emissive: 0x330000,
            roughness: 0.3,
            metalness: 0.1
        })
    );
    scene.add(startSphere);

    finalSphere = new THREE.Mesh(
        new THREE.SphereGeometry(0.1, 32),
        new THREE.MeshStandardMaterial({ 
            color: 0x33ff33,
            emissive: 0x003300,
            roughness: 0.3,
            metalness: 0.1
        })
    );
    scene.add(finalSphere);

    // Инициализация графика
    const ctx = document.getElementById('chart').getContext('2d');
    chart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: [],
            datasets: [{
                label: 'F(x)',
                data: [],
                borderColor: '#4CAF50',
                backgroundColor: 'rgba(76, 175, 80, 0.1)',
                borderWidth: 2,
                pointRadius: 2,
                pointHoverRadius: 5,
                fill: true,
                tension: 0.3
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            animation: false,
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                x: { 
                    title: { display: true, text: 'Итерация' },
                    grid: { color: 'rgba(0,0,0,0.1)' }
                },
                y: { 
                    title: { display: true, text: 'F(x)' },
                    grid: { color: 'rgba(0,0,0,0.1)' }
                }
            }
        }
    });

    // Обработчик кнопки
    document.getElementById("runBtn").addEventListener("click", run);
    
    // Обработчик изменения задачи
    document.getElementById("task").addEventListener("change", () => {
        createSurface();
        createRegion();
        updateTaskType();
    });
    
    // Обновление типа задачи при загрузке
    updateTaskType();
    
    // Обработчик ресайза
    window.addEventListener("resize", onWindowResize, false);
}

function updateTaskType() {
    let task = parseInt(document.getElementById("task").value);
    let optTypeSpan = document.getElementById("optType");
    if (task === 1) {
        optTypeSpan.textContent = "минимизация";
        optTypeSpan.style.color = "#2196F3";
    } else {
        optTypeSpan.textContent = "максимизация";
        optTypeSpan.style.color = "#FF9800";
    }
}

function onWindowResize() {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
}

// Целевая функция
function f(x1, x2) {
    let task = parseInt(document.getElementById("task").value);
    if (task === 1) {
        return 2*x1*x1 + 3*x2*x2 + 4*x1*x2 - 6*x1 - 3*x2;
    } else {
        return x1 + 2*x2 - x2*x2;
    }
}

// Градиент
function grad(x1, x2) {
    let task = parseInt(document.getElementById("task").value);
    if (task === 1) {
        return [4*x1 + 4*x2 - 6, 6*x2 + 4*x1 - 3];
    } else {
        return [1, 2 - 2*x2];
    }
}

// Проекция точки на допустимую область
function project(x1, x2) {
    let task = parseInt(document.getElementById("task").value);
    
    // 1. Проекция на неотрицательность
    x1 = Math.max(0, x1);
    x2 = Math.max(0, x2);
    
    if (task === 1) {
        // Задача 1: ограничения
        // x1 + x2 ≤ 1
        if (x1 + x2 > 1) {
            // Проекция на прямую x1 + x2 = 1
            let t = (x1 + x2 - 1) / 2;
            x1 -= t;
            x2 -= t;
        }
        
        // 2x1 + 3x2 ≤ 4 (обычно неактивно в оптимуме, но для полноты)
        if (2*x1 + 3*x2 > 4) {
            let lambda = (2*x1 + 3*x2 - 4) / (4 + 9);
            x1 -= 2*lambda;
            x2 -= 3*lambda;
        }
    } else {
        // Задача 2: ограничения
        // 3x1 + 2x2 ≤ 6
        if (3*x1 + 2*x2 > 6) {
            let lambda = (3*x1 + 2*x2 - 6) / (9 + 4);
            x1 -= 3*lambda;
            x2 -= 2*lambda;
        }
        
        // x1 + 2x2 ≤ 4
        if (x1 + 2*x2 > 4) {
            let lambda = (x1 + 2*x2 - 4) / (1 + 4);
            x1 -= lambda;
            x2 -= 2*lambda;
        }
    }
    
    return [x1, x2];
}

// Проверка допустимости точки
function isFeasible(x1, x2) {
    let task = parseInt(document.getElementById("task").value);
    
    if (x1 < -EPS || x2 < -EPS) return false;
    
    if (task === 1) {
        if (x1 + x2 > 1 + EPS) return false;
        if (2*x1 + 3*x2 > 4 + EPS) return false;
    } else {
        if (3*x1 + 2*x2 > 6 + EPS) return false;
        if (x1 + 2*x2 > 4 + EPS) return false;
    }
    
    return true;
}

// Метод проекции градиента
function gradientProjection(startX, startY, alpha, maxIter, epsilon) {
    let task = parseInt(document.getElementById("task").value);
    let maximize = (task === 2); // Задача 2 - максимизация
    
    let history = [];
    let x = startX, y = startY;
    
    // Проверяем начальную точку
    if (!isFeasible(x, y)) {
        [x, y] = project(x, y);
    }
    
    for (let i = 0; i < maxIter; i++) {
        let val = f(x, y);
        history.push({ x, y, z: val });
        
        let g = grad(x, y);
        
        // Направление: + градиент для максимизации, - градиент для минимизации
        let direction = maximize ? 1 : -1;
        
        // Пробный шаг
        let nx = x + direction * alpha * g[0];
        let ny = y + direction * alpha * g[1];
        
        // Проекция на допустимую область
        let [px, py] = project(nx, ny);
        
        // Критерий остановки: малое изменение
        if (Math.abs(px - x) < epsilon && Math.abs(py - y) < epsilon) {
            x = px;
            y = py;
            history.push({ x, y, z: f(x, y) });
            break;
        }
        
        x = px;
        y = py;
    }
    
    return history;
}

// Создание поверхности функции
function createSurface() {
    if (surface) scene.remove(surface);
    
    let task = parseInt(document.getElementById("task").value);
    
    const size = 2.5;
    const seg = 80;
    let vertices = [];
    let indices = [];
    
    // Определяем диапазон в зависимости от задачи
    let xMin = 0, xMax = (task === 1) ? 1.2 : 2.2;
    let yMin = 0, yMax = (task === 1) ? 1.2 : 2.2;
    
    for (let i = 0; i <= seg; i++) {
        let x = xMin + (xMax - xMin) * i / seg;
        for (let j = 0; j <= seg; j++) {
            let y = yMin + (yMax - yMin) * j / seg;
            let z = f(x, y);
            
            // Ограничиваем z для лучшей визуализации
            if (task === 1 && z < -5) z = -5;
            if (task === 2 && z > 3) z = 3;
            
            vertices.push(x, z, y);
        }
    }
    
    for (let i = 0; i < seg; i++) {
        for (let j = 0; j < seg; j++) {
            let a = i * (seg + 1) + j;
            let b = a + 1;
            let c = a + (seg + 1);
            let d = c + 1;
            
            indices.push(a, b, c);
            indices.push(b, d, c);
        }
    }
    
    const geom = new THREE.BufferGeometry();
    geom.setAttribute('position', new THREE.Float32BufferAttribute(vertices, 3));
    geom.setIndex(indices);
    geom.computeVertexNormals();
    
    // Цвет в зависимости от высоты
    const colors = [];
    for (let i = 0; i < vertices.length; i += 3) {
        let z = vertices[i + 1];
        let r = 0.2, g = 0.5, b = 1.0;
        
        if (task === 1) {
            // Сине-фиолетовая гамма для минимизации
            r = 0.3 + z * 0.2;
            g = 0.4 + z * 0.2;
            b = 0.9 - z * 0.1;
        } else {
            // Зелено-желтая гамма для максимизации
            r = 0.5 + z * 0.3;
            g = 0.8 - z * 0.1;
            b = 0.3;
        }
        
        colors.push(r, g, b);
    }
    geom.setAttribute('color', new THREE.Float32BufferAttribute(colors, 3));
    
    surface = new THREE.Mesh(
        geom,
        new THREE.MeshPhongMaterial({ 
            vertexColors: true,
            transparent: true,
            opacity: 0.7,
            side: THREE.DoubleSide,
            shininess: 30,
            emissive: 0x000000
        })
    );
    surface.castShadow = true;
    surface.receiveShadow = true;
    scene.add(surface);
}

// Создание допустимой области
function createRegion() {
    if (region) scene.remove(region);
    
    let task = parseInt(document.getElementById("task").value);
    let points = [];
    
    if (task === 1) {
        // Область: x1>=0, x2>=0, x1+x2<=1, 2x1+3x2<=4
        // Вершины многоугольника
        points.push([0, 0]);
        points.push([1, 0]);
        
        // Пересечение x1+x2=1 и 2x1+3x2=4
        let x1 = (1*3 - 1*4) / (1*3 - 1*2); // -1 / 1 = -1 (не входит)
        // Значит активна только x1+x2=1
        points.push([0, 1]);
    } else {
        // Область: x1>=0, x2>=0, 3x1+2x2<=6, x1+2x2<=4
        // Вершины:
        points.push([0, 0]);
        
        // Пересечение с осью X1: x1+2*0=4 => x1=4, но 3*4+0=12>6 -> не подходит
        // Пересечение 3x1+2x2=6 с осью X1: x1=2
        points.push([2, 0]);
        
        // Пересечение двух прямых:
        // 3x1+2x2=6 и x1+2x2=4
        // Вычитаем: 2x1=2 => x1=1, x2=(4-1)/2=1.5
        points.push([1, 1.5]);
        
        // Пересечение с осью X2: x1+2x2=4 => x2=2
        points.push([0, 2]);
    }
    
    // Строим треугольники от (0,0) к остальным вершинам
    let vertices = [];
    for (let i = 1; i < points.length; i++) {
        let p0 = points[0];
        let p1 = points[i];
        let p2 = points[(i + 1 < points.length) ? i + 1 : 1];
        
        // Вычисляем z как f(x,y) для наложения на поверхность
        let z0 = f(p0[0], p0[1]);
        let z1 = f(p1[0], p1[1]);
        let z2 = f(p2[0], p2[1]);
        
        vertices.push(p0[0], z0, p0[1]);
        vertices.push(p1[0], z1, p1[1]);
        vertices.push(p2[0], z2, p2[1]);
    }
    
    const geometry = new THREE.BufferGeometry();
    geometry.setAttribute('position', new THREE.Float32BufferAttribute(vertices, 3));
    
    const indices = [];
    for (let i = 0; i < vertices.length / 3; i++) {
        indices.push(i);
    }
    geometry.setIndex(indices);
    
    const material = new THREE.MeshBasicMaterial({ 
        color: task === 1 ? 0xffaa44 : 0x44aaff,
        transparent: true,
        opacity: 0.25,
        side: THREE.DoubleSide
    });
    
    region = new THREE.Mesh(geometry, material);
    scene.add(region);
    
    // Добавляем границы области
    let borderPoints = [];
    for (let i = 0; i < points.length; i++) {
        let p = points[i];
        borderPoints.push(new THREE.Vector3(p[0], f(p[0], p[1]), p[1]));
    }
    // Замыкаем
    borderPoints.push(new THREE.Vector3(points[0][0], f(points[0][0], points[0][1]), points[0][1]));
    
    const borderGeo = new THREE.BufferGeometry().setFromPoints(borderPoints);
    const borderLine = new THREE.Line(borderGeo, new THREE.LineBasicMaterial({ color: 0xffaa44, linewidth: 2 }));
    scene.add(borderLine);
}

// Отрисовка траектории
function drawTrajectory(hist) {
    // Удаляем старую траекторию
    if (trajectory) scene.remove(trajectory);
    points.forEach(p => scene.remove(p));
    points = [];
    
    if (hist.length < 2) return;
    
    // Траектория
    let pts = hist.map(p => new THREE.Vector3(p.x, p.z, p.y));
    trajectory = new THREE.Line(
        new THREE.BufferGeometry().setFromPoints(pts),
        new THREE.LineBasicMaterial({ color: 0xff6600, linewidth: 2 })
    );
    scene.add(trajectory);
    
    // Точки траектории
    hist.forEach((p, i) => {
        if (i % 3 === 0 || i === hist.length - 1) {
            let sphere = new THREE.Mesh(
                new THREE.SphereGeometry(0.04, 16),
                new THREE.MeshStandardMaterial({ 
                    color: i === 0 ? 0xff3333 : (i === hist.length - 1 ? 0x33ff33 : 0xffaa33),
                    emissive: i === 0 ? 0x330000 : (i === hist.length - 1 ? 0x003300 : 0x332200)
                })
            );
            sphere.position.set(p.x, p.z, p.y);
            scene.add(sphere);
            points.push(sphere);
        }
    });
}

// Основная функция запуска
function run() {
    // Получаем параметры
    let startX = parseFloat(document.getElementById("startX").value);
    let startY = parseFloat(document.getElementById("startY").value);
    let alpha = parseFloat(document.getElementById("alpha").value);
    let maxIter = parseInt(document.getElementById("iterMax").value);
    let epsilon = parseFloat(document.getElementById("epsilon").value);
    
    // Обновляем допустимую область
    createRegion();
    
    // Обновляем начальную точку
    startSphere.position.set(startX, f(startX, startY), startY);
    
    // Запускаем оптимизацию
    let history = gradientProjection(startX, startY, alpha, maxIter, epsilon);
    let last = history[history.length - 1];
    
    // Обновляем финальную точку
    finalSphere.position.set(last.x, last.z, last.y);
    
    // Рисуем траекторию
    drawTrajectory(history);
    
    // Обновляем информационную панель
    document.getElementById("iter").textContent = history.length;
    document.getElementById("point").textContent = `(${last.x.toFixed(4)}, ${last.y.toFixed(4)})`;
    document.getElementById("value").textContent = last.z.toFixed(6);
    
    // Обновляем статус
    let task = parseInt(document.getElementById("task").value);
    let isOptimal = isFeasible(last.x, last.y);
    document.getElementById("status").innerHTML = isOptimal ? 
        '<span style="color:#4CAF50;">✓ оптимально</span>' : 
        '<span style="color:#f44336;">✗ недопустимо</span>';
    
    // Обновляем график
    chart.data.labels = history.map((_, i) => i + 1);
    chart.data.datasets[0].data = history.map(p => p.z);
    chart.update();
    
    // Поворачиваем камеру для лучшего обзора, если нужно
    if (history.length > 0) {
        controls.target.set(last.x, last.z, last.y);
    }
}

// Анимация
function animate() {
    requestAnimationFrame(animate);
    
    if (controls) controls.update();
    
    renderer.render(scene, camera);
}