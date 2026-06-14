let scene, camera, renderer, controls;
let surface;

let population = [];
let points = [];
let bestPoint;

let generation = 0;
let running = false;

let chart;
let chartData = [];

const X_MIN = -2;
const X_MAX = 2;
const Y_MIN = -1;
const Y_MAX = 3;

init();
createSurface();
initChart();
animate();

function init() {
    scene = new THREE.Scene();
    scene.background = new THREE.Color(0xffffff);

    camera = new THREE.PerspectiveCamera(
        45,
        window.innerWidth / window.innerHeight,
        0.1,
        1000
    );

    camera.position.set(4, 4, 6);

    renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setSize(window.innerWidth, window.innerHeight);

    document.body.appendChild(renderer.domElement);

    controls = new THREE.OrbitControls(
        camera,
        renderer.domElement
    );

    scene.add(new THREE.AmbientLight(0xffffff, 0.6));

    const light = new THREE.DirectionalLight(0xffffff, 0.8);
    light.position.set(5, 10, 7);
    scene.add(light);

    window.addEventListener("resize", onResize);

    document
        .getElementById("start-btn")
        .addEventListener("click", startGA);
}

function rosenbrock(x, y) {
    return (1 - x) * (1 - x) +
           100 * (y - x * x) * (y - x * x);
}

function createSurface() {
    const seg = 140;

    const vertices = [];
    const colors = [];
    const indices = [];

    let minZ = Infinity;
    let maxZ = -Infinity;

    const zvals = [];

    for (let i = 0; i <= seg; i++) {
        const x = X_MIN + (i / seg) * (X_MAX - X_MIN);

        for (let j = 0; j <= seg; j++) {
            const y = Y_MIN + (j / seg) * (Y_MAX - Y_MIN);

            const z = rosenbrock(x, y);

            zvals.push(z);

            minZ = Math.min(minZ, z);
            maxZ = Math.max(maxZ, z);
        }
    }

    let k = 0;

    for (let i = 0; i <= seg; i++) {
        const x = X_MIN + (i / seg) * (X_MAX - X_MIN);

        for (let j = 0; j <= seg; j++) {
            const y = Y_MIN + (j / seg) * (Y_MAX - Y_MIN);

            let z = zvals[k++];

            const zn = (z - minZ) / (maxZ - minZ);
            const height = zn * 3;

            vertices.push(x, height, y);

            const r = 0.267 + zn * 0.7;
            const g = 0.004 + zn * 0.9;
            const b = 0.329 + (1 - zn) * 0.7;

            colors.push(r, g, b);
        }
    }

    for (let i = 0; i < seg; i++) {
        for (let j = 0; j < seg; j++) {
            const a = i * (seg + 1) + j;
            const b = a + 1;
            const c = a + seg + 1;
            const d = c + 1;

            indices.push(a, b, c);
            indices.push(b, d, c);
        }
    }

    const geom = new THREE.BufferGeometry();

    geom.setAttribute(
        "position",
        new THREE.Float32BufferAttribute(vertices, 3)
    );

    geom.setAttribute(
        "color",
        new THREE.Float32BufferAttribute(colors, 3)
    );

    geom.setIndex(indices);
    geom.computeVertexNormals();

    surface = new THREE.Mesh(
        geom,
        new THREE.MeshPhongMaterial({
            vertexColors: true,
            side: THREE.DoubleSide
        })
    );

    scene.add(surface);
}

function startGA() {
    running = true;
    generation = 0;
    chartData = [];

    initPopulation();
    iterate();
}

function initPopulation() {
    population = [];

    const size = parseInt(
        document.getElementById("pop-size").value
    );

    for (let i = 0; i < size; i++) {
        population.push({
            x: rand(X_MIN, X_MAX),
            y: rand(Y_MIN, Y_MAX)
        });
    }
}

function iterate() {
    if (!running) return;

    const maxGen = parseInt(
        document.getElementById("max-gen").value
    );

    generation++;

    population.forEach(p => {
        p.value = rosenbrock(p.x, p.y);
    });

    population.sort((a, b) => a.value - b.value);

    drawPopulation();
    updateInfo();

    chartData.push(population[0].value);
    updateChart();

    if (generation >= maxGen) {
        running = false;
        return;
    }

    nextGeneration();

    requestAnimationFrame(iterate);
}

function nextGeneration() {
    const pc = parseFloat(
        document.getElementById("pc").value
    );

    const pm = parseFloat(
        document.getElementById("pm").value
    );

    const elite = parseInt(
        document.getElementById("elite").value
    );

    const newPop = [];

    for (let i = 0; i < elite; i++) {
        newPop.push(population[i]);
    }

    while (newPop.length < population.length) {
        const p1 = select();
        const p2 = select();

        let child;

        if (Math.random() < pc) {
            child = {
                x: (p1.x + p2.x) / 2,
                y: (p1.y + p2.y) / 2
            };
        } else {
            child = { ...p1 };
        }

        if (Math.random() < pm) {
            child.x += rand(-0.2, 0.2);
            child.y += rand(-0.2, 0.2);
        }

        child.x = clamp(child.x, X_MIN, X_MAX);
        child.y = clamp(child.y, Y_MIN, Y_MAX);

        newPop.push(child);
    }

    population = newPop;
}

function select() {
    return population[
        Math.floor(Math.random() * 10)
    ];
}

function drawPopulation() {
    points.forEach(p => scene.remove(p));
    points = [];

    population.forEach(p => {
        const z = normalizeZ(rosenbrock(p.x, p.y));

        const mesh = new THREE.Mesh(
            new THREE.SphereGeometry(0.04, 16, 16),
            new THREE.MeshBasicMaterial({ color: 0x000000 })
        );

        mesh.position.set(p.x, z, p.y);

        scene.add(mesh);
        points.push(mesh);
    });

    if (bestPoint) scene.remove(bestPoint);

    const best = population[0];

    bestPoint = new THREE.Mesh(
        new THREE.SphereGeometry(0.08, 16, 16),
        new THREE.MeshBasicMaterial({ color: 0xff0000 })
    );

    bestPoint.position.set(
        best.x,
        normalizeZ(best.value),
        best.y
    );

    scene.add(bestPoint);
}

function updateInfo() {
    const best = population[0];

    document.getElementById("gen-count").textContent = generation;
    document.getElementById("best-x").textContent = best.x.toFixed(4);
    document.getElementById("best-y").textContent = best.y.toFixed(4);
    document.getElementById("best-f").textContent = best.value.toFixed(6);
}

function normalizeZ(z) {
    return Math.log(z + 1) / 3;
}

function initChart() {
    const ctx = document
        .getElementById("chart")
        .getContext("2d");

    chart = new Chart(ctx, {
        type: "line",
        data: {
            labels: [],
            datasets: [{
                label: "Best f(x,y)",
                data: [],
                borderColor: "red",
                fill: false
            }]
        },
        options: {
            responsive: true,
            animation: false
        }
    });
}

function updateChart() {
    chart.data.labels.push(generation);
    chart.data.datasets[0].data.push(
        population[0].value
    );

    chart.update();
}

function rand(a, b) {
    return a + Math.random() * (b - a);
}

function clamp(v, a, b) {
    return Math.max(a, Math.min(b, v));
}

function animate() {
    requestAnimationFrame(animate);
    renderer.render(scene, camera);
}

function onResize() {
    camera.aspect =
        window.innerWidth / window.innerHeight;

    camera.updateProjectionMatrix();

    renderer.setSize(
        window.innerWidth,
        window.innerHeight
    );
}