/**
 * Haldor & Vey — Atelier Watch House Interactive Viewer
 * Plain vanilla JavaScript module using Three.js 0.170.0
 */

import * as THREE from 'three';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
import { DRACOLoader } from 'three/addons/loaders/DRACOLoader.js';
import { MeshoptDecoder } from 'three/addons/libs/meshopt_decoder.module.js';
import { RoomEnvironment } from 'three/addons/environments/RoomEnvironment.js';

/* --- LOCAL EDITIONS DATA --- */
const EDITIONS = {
  'serein-02': {
    id: 'serein-02',
    name: 'Serein No. 02',
    calibre: 'calibre H-02',
    eyebrow: 'SERIES I / HAND-WOUND',
    tags: ['manual', 'silver dial', 'edition 24'],
    lede: 'A frost-silver dial gives the exposed balance a quieter stage.',
    traits: [
      { label: 'Case', value: '37 mm', icon: 'ruler' },
      { label: 'Calibre', value: 'HV-02', icon: 'gauge' },
      { label: 'Reserve', value: '58 hours', icon: 'rotate-cw' },
      { label: 'Water', value: '3 bar', icon: 'waves' }
    ],
    setting: 'Studio morning',
    detailAction: 'See balance detail',
    caption: 'The balance breathes beneath a veil of steel.',
    crop: '48% 38%',
    image: 'assets/watch-serein-02.png',
    model: 'assets/models/serein-02.glb'
  },
  'nacre-05': {
    id: 'nacre-05',
    name: 'Nacre No. 05',
    calibre: 'calibre H-05',
    eyebrow: 'SERIES II / AUTOMATIC',
    tags: ['automatic', 'pearl dial', 'edition 18'],
    lede: 'A pale face and open rotor settle into the room without asking for attention.',
    traits: [
      { label: 'Case', value: '39 mm', icon: 'ruler' },
      { label: 'Calibre', value: 'HV-05', icon: 'gauge' },
      { label: 'Reserve', value: '54 hours', icon: 'rotate-cw' },
      { label: 'Water', value: '5 bar', icon: 'waves' }
    ],
    setting: 'Low-lit dinner',
    detailAction: 'See movement detail',
    caption: 'The rotor catches light, then returns to shadow.',
    crop: '56% 43%',
    image: 'assets/watch-nacre-05.png',
    model: 'assets/models/nacre-05.glb'
  },
  'orison-08': {
    id: 'orison-08',
    name: 'Orison No. 08',
    calibre: 'calibre H-08',
    eyebrow: 'SERIES III / GMT',
    tags: ['GMT', 'slate dial', 'edition 16'],
    lede: 'A second timezone circles a deep grey dial with deliberate restraint.',
    traits: [
      { label: 'Case', value: '40 mm', icon: 'ruler' },
      { label: 'Calibre', value: 'HV-08', icon: 'gauge' },
      { label: 'Reserve', value: '47 hours', icon: 'rotate-cw' },
      { label: 'Water', value: '10 bar', icon: 'waves' }
    ],
    setting: 'Night departure',
    detailAction: 'See GMT detail',
    caption: 'A second hour waits beneath the darker ring.',
    crop: '51% 46%',
    image: 'assets/watch-orison-08.png',
    model: 'assets/models/orison-08.glb'
  },
  'hedra-11': {
    id: 'hedra-11',
    name: 'Hedra No. 11',
    calibre: 'calibre H-11',
    eyebrow: 'SERIES IV / CHRONOGRAPH',
    tags: ['chronograph', 'umber dial', 'edition 12'],
    lede: 'Two recessed counters bring a warm, measured pulse to the case.',
    traits: [
      { label: 'Case', value: '41 mm', icon: 'ruler' },
      { label: 'Calibre', value: 'HV-11', icon: 'gauge' },
      { label: 'Reserve', value: '46 hours', icon: 'rotate-cw' },
      { label: 'Water', value: '5 bar', icon: 'waves' }
    ],
    setting: 'Late workshop',
    detailAction: 'See counter detail',
    caption: 'The chronograph rests until the room asks for time.',
    crop: '54% 52%',
    image: 'assets/watch-hedra-11.png',
    model: 'assets/models/hedra-11.glb'
  },
  'kestrel-14': {
    id: 'kestrel-14',
    name: 'Kestrel No. 14',
    calibre: 'calibre H-14',
    eyebrow: 'SERIES V / FIELD',
    tags: ['manual', 'sand dial', 'edition 30'],
    lede: 'A durable brushed case pairs legible markers with a softened canvas strap.',
    traits: [
      { label: 'Case', value: '38 mm', icon: 'ruler' },
      { label: 'Calibre', value: 'HV-14', icon: 'gauge' },
      { label: 'Reserve', value: '63 hours', icon: 'rotate-cw' },
      { label: 'Water', value: '10 bar', icon: 'waves' }
    ],
    setting: 'Cold platform',
    detailAction: 'See case detail',
    caption: 'Every marker holds its place against the weather.',
    crop: '50% 45%',
    image: 'assets/watch-kestrel-14.png',
    model: 'assets/models/kestrel-14.glb'
  },
  'vanta-17': {
    id: 'vanta-17',
    name: 'Vanta No. 17',
    calibre: 'calibre H-17',
    eyebrow: 'SERIES VI / CALENDAR',
    tags: ['calendar', 'black dial', 'edition 10'],
    lede: 'A black lacquer dial frames a clean calendar aperture and polished moon phase.',
    traits: [
      { label: 'Case', value: '39 mm', icon: 'ruler' },
      { label: 'Calibre', value: 'HV-17', icon: 'gauge' },
      { label: 'Reserve', value: '50 hours', icon: 'rotate-cw' },
      { label: 'Water', value: '3 bar', icon: 'waves' }
    ],
    setting: 'Evening reception',
    detailAction: 'See calendar detail',
    caption: 'A small aperture keeps the month in view.',
    crop: '52% 40%',
    image: 'assets/watch-vanta-17.png',
    model: 'assets/models/vanta-17.glb'
  }
};

/* --- DOM ELEMENTS --- */
const canvas = document.getElementById('webgl-canvas');
const stageContainer = document.getElementById('stage-container');
const stageFallbackWrap = document.getElementById('stage-fallback-wrap');
const stageFallbackImg = document.getElementById('stage-fallback-img');
const stageCaption = document.getElementById('stage-caption');
const stageHint = document.getElementById('stage-hint');
const groundBloom = document.getElementById('ground-bloom');
const exitFocusBtn = document.getElementById('exit-focus-btn');
const accessibleAnnouncer = document.getElementById('accessible-announcer');

const btnZoomIn = document.getElementById('btn-zoom-in');
const btnZoomOut = document.getElementById('btn-zoom-out');
const btnExpandViewer = document.getElementById('btn-expand-viewer');
const btnToggleDaylight = document.getElementById('btn-toggle-daylight');

const btnTurnLeft = document.getElementById('btn-turn-left');
const btnTurnFull = document.getElementById('btn-turn-full');
const btnTurnRight = document.getElementById('btn-turn-right');

const watchTabs = document.querySelectorAll('.watch-tab');
const detailEyebrow = document.getElementById('detail-eyebrow');
const detailTitle = document.getElementById('detail-title');
const detailTags = document.getElementById('detail-tags');
const detailLede = document.getElementById('detail-lede');
const traitsList = document.getElementById('traits-list');
const detailSetting = document.getElementById('detail-setting');
const detailActionText = document.getElementById('detail-action-text');
const movementCrop = document.getElementById('movement-crop');
const editionSearch = document.getElementById('edition-search');

/* --- STATE --- */
let activeEditionId = 'nacre-05';
let isDaylight = false;
let isFocusMode = false;
let isReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

// Motion / Pose targets
const HOME_YAW = 0.45;
const HOME_PITCH = 0.12;
const HOME_DISTANCE = 1.85;

let currentYaw = HOME_YAW;
let targetYaw = HOME_YAW;
let currentPitch = HOME_PITCH;
let targetPitch = HOME_PITCH;
let currentDistance = HOME_DISTANCE;
let targetDistance = HOME_DISTANCE;

// Drag & Inertia
let isDragging = false;
let pointerStartX = 0;
let pointerStartY = 0;
let lastPointerX = 0;
let lastPointerY = 0;
let angularVelX = 0;
let angularVelY = 0;
let lastInputTime = performance.now();
let hintFaded = false;

// Selection transition state
let isSwappingModel = false;
let isRotatingFull = false;
let fullRotationStartTime = 0;
let fullRotationStartAngle = 0;

// Theme transition state
let themeAnimStartTime = 0;
let isThemeTransitioning = false;
let startKeyColor = new THREE.Color(0xFFE3CA);
let targetKeyColor = new THREE.Color(0xFFE3CA);
let startRimIntensity = 2.6;
let targetRimIntensity = 2.6;
let startEnvIntensity = 0.55;
let targetEnvIntensity = 0.55;

// Three.js instances
let renderer, scene, camera;
let pivot, spin, holder;
let keyLight, rimLight, fillLight, groundSprite;
let modelCache = new Map();
let currentLoadedMesh = null;
let gltfLoader, dracoLoader;
let isLoopRunning = false;
let animationFrameId = null;
let frameCount = 0;

/* --- REDUCED MOTION LISTENER --- */
window.matchMedia('(prefers-reduced-motion: reduce)').addEventListener('change', (e) => {
  isReducedMotion = e.matches;
  if (isReducedMotion) {
    angularVelX = 0;
    angularVelY = 0;
    spin.rotation.y = 0;
    holder.position.y = 0;
  }
});

/* --- INITIALIZE THREE.JS --- */
function initThree() {
  try {
    // 1. Renderer
    renderer = new THREE.WebGLRenderer({
      canvas: canvas,
      alpha: true,
      antialias: true,
      powerPreference: 'high-performance',
      preserveDrawingBuffer: true
    });
    renderer.outputColorSpace = THREE.SRGBColorSpace;
    renderer.toneMapping = THREE.NeutralToneMapping;
    renderer.toneMappingExposure = 1.1;
    renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 1.75));

    // 2. Scene
    scene = new THREE.Scene();

    // 3. Environment (PMREM from RoomEnvironment)
    const pmremGenerator = new THREE.PMREMGenerator(renderer);
    pmremGenerator.compileEquirectangularShader();
    const roomEnv = new RoomEnvironment();
    const envTexture = pmremGenerator.fromScene(roomEnv).texture;
    scene.environment = envTexture;
    scene.environmentIntensity = 0.55;
    pmremGenerator.dispose();
    roomEnv.dispose();

    // 4. Camera (Perspective)
    const width = window.innerWidth;
    const height = window.innerHeight;
    camera = new THREE.PerspectiveCamera(40, width / height, 0.1, 25);
    camera.position.set(0, 0, currentDistance);

    // 5. Hierarchy: pivot > spin > holder
    pivot = new THREE.Group();
    spin = new THREE.Group();
    holder = new THREE.Group();

    pivot.rotation.x = HOME_PITCH;
    pivot.rotation.y = HOME_YAW;

    pivot.add(spin);
    spin.add(holder);
    scene.add(pivot);

    // 6. Lights
    // Warm vellum key at (4.0, 5.1, 5.8) with #FFE3CA and intensity 2.4
    keyLight = new THREE.DirectionalLight(0xFFE3CA, 2.4);
    keyLight.position.set(4.0, 5.1, 5.8);
    keyLight.target = holder;
    scene.add(keyLight);
    scene.add(keyLight.target);

    // Terracotta rim at (-4.6, 1.7, -3.5) with #D67A4F and intensity 2.6 (behind and left)
    rimLight = new THREE.DirectionalLight(0xD67A4F, 2.6);
    rimLight.position.set(-4.6, 1.7, -3.5);
    rimLight.target = holder;
    scene.add(rimLight);
    scene.add(rimLight.target);

    // Neutral fill at intensity .30
    fillLight = new THREE.DirectionalLight(0xFFFFFF, 0.40);
    fillLight.position.set(0.0, 1.0, 4.5);
    fillLight.target = holder;
    scene.add(fillLight);
    scene.add(fillLight.target);

    // Ambient light to ensure rich visibility on dark dials and textures
    const ambientLight = new THREE.AmbientLight(0xFFF5EB, 1.25);
    scene.add(ambientLight);

    // 7. Soft radial ground sprite under watch
    const groundCanvas = document.createElement('canvas');
    groundCanvas.width = 256;
    groundCanvas.height = 256;
    const gctx = groundCanvas.getContext('2d');
    const grad = gctx.createRadialGradient(128, 128, 0, 128, 128, 128);
    grad.addColorStop(0, 'rgba(214, 122, 79, 0.32)');
    grad.addColorStop(0.45, 'rgba(214, 122, 79, 0.10)');
    grad.addColorStop(1, 'rgba(214, 122, 79, 0)');
    gctx.fillStyle = grad;
    gctx.fillRect(0, 0, 256, 256);

    const groundTex = new THREE.CanvasTexture(groundCanvas);
    const groundMat = new THREE.SpriteMaterial({
      map: groundTex,
      transparent: true,
      opacity: 0.85,
      blending: THREE.NormalBlending
    });
    groundSprite = new THREE.Sprite(groundMat);
    groundSprite.scale.set(2.4, 0.9, 1.0);
    groundSprite.position.set(0, -1.05, 0);
    scene.add(groundSprite);

    // 8. Loaders
    gltfLoader = new GLTFLoader();
    dracoLoader = new DRACOLoader();
    dracoLoader.setDecoderPath('assets/draco/');
    gltfLoader.setDRACOLoader(dracoLoader);
    gltfLoader.setMeshoptDecoder(MeshoptDecoder);

    // 9. Resize & camera principal point setup
    updateCameraAndResize();

    const resizeObserver = new ResizeObserver(() => {
      updateCameraAndResize();
    });
    resizeObserver.observe(document.body);
    resizeObserver.observe(stageContainer);

    window.addEventListener('resize', updateCameraAndResize);

    // Expose for debugging/inspection
    window.__THREE_DEBUG__ = {
      scene, camera, renderer, pivot, spin, holder, modelCache,
      getLoopState: () => ({ isLoopRunning, frameCount })
    };

    // 10. Load initial model
    loadWatchModel('nacre-05');

    // Start render loop
    startRenderLoop();

  } catch (err) {
    console.warn('WebGL initialization failed, switching to transparent PNG fallback:', err);
    showFallbackState(activeEditionId);
  }
}

/* --- CAMERA PRINCIPAL POINT REMAPPING --- */
function updateCameraAndResize() {
  if (!renderer || !camera) return;

  const width = window.innerWidth;
  const height = window.innerHeight;

  renderer.setSize(width, height, false);
  camera.aspect = width / height;

  if (isFocusMode) {
    // In focus mode, expanded stage aims at viewport midpoint
    camera.clearViewOffset();
  } else {
    // Remap camera principal point onto middle-column stage center
    const stageRect = stageContainer.getBoundingClientRect();
    const stageCenterX = stageRect.left + stageRect.width / 2;
    const stageCenterY = stageRect.top + stageRect.height / 2;
    const screenCenterX = width / 2;
    const screenCenterY = height / 2;

    const offsetX = stageCenterX - screenCenterX;
    const offsetY = stageCenterY - screenCenterY;

    // Shift principal point without geometric distortion
    camera.setViewOffset(width, height, -offsetX, -offsetY, width, height);
  }

  camera.updateProjectionMatrix();
  renderSingleFrame();
}

/* --- MODEL LOADING & NORMALIZATION --- */
async function loadWatchModel(editionId) {
  const edition = EDITIONS[editionId];
  if (!edition) return;

  // Check cache
  if (modelCache.has(editionId)) {
    const cachedModel = modelCache.get(editionId);
    displayModel(cachedModel);
    return;
  }

  try {
    const gltf = await new Promise((resolve, reject) => {
      gltfLoader.load(edition.model, resolve, undefined, reject);
    });

    const model = gltf.scene;

    // Apply physically based shading & preserve metalness/roughness
    model.traverse((child) => {
      if (child.isMesh && child.material) {
        child.material.side = THREE.DoubleSide;
        if (child.material.map) {
          child.material.map.colorSpace = THREE.SRGBColorSpace;
          child.material.map.needsUpdate = true;
        }
        if (!child.material.isMeshStandardMaterial && !child.material.isMeshPhysicalMaterial) {
          child.material = new THREE.MeshStandardMaterial({
            color: child.material.color,
            map: child.material.map,
            metalness: child.material.metalness ?? 0.8,
            roughness: child.material.roughness ?? 0.25
          });
          child.material.side = THREE.DoubleSide;
        }
        child.material.needsUpdate = true;
      }
    });

    // Center model and normalize bounding radius to 1.0
    const box = new THREE.Box3().setFromObject(model);
    const center = new THREE.Vector3();
    box.getCenter(center);
    const sphere = new THREE.Sphere();
    box.getBoundingSphere(sphere);
    const radius = sphere.radius || 1.0;

    // Center and scale to normalized unit size
    model.position.sub(center);
    const scale = 1.0 / radius;
    model.scale.set(scale, scale, scale);

    const modelGroup = new THREE.Group();
    modelGroup.add(model);

    modelCache.set(editionId, modelGroup);
    displayModel(modelGroup);

  } catch (err) {
    console.warn(`GLB loading failed for ${edition.name}, showing matching PNG fallback:`, err);
    showFallbackState(editionId);
  }
}

function displayModel(newModelGroup) {
  // Hide fallback if visible
  stageFallbackWrap.classList.remove('is-visible');

  // Remove existing model from holder
  while (holder.children.length > 0) {
    holder.remove(holder.children[0]);
  }

  holder.add(newModelGroup);
  currentLoadedMesh = newModelGroup;

  renderSingleFrame();
}

function showFallbackState(editionId) {
  const edition = EDITIONS[editionId];
  if (!edition) return;

  stageFallbackImg.src = edition.image;
  stageFallbackWrap.classList.add('is-visible');
}

/* --- THEME TOGGLE & SMOOTH 600ms LIGHTING CURVE --- */
function toggleDaylight() {
  isDaylight = !isDaylight;
  document.documentElement.setAttribute('data-theme', isDaylight ? 'daylight' : 'dark');
  btnToggleDaylight.setAttribute('aria-pressed', isDaylight ? 'true' : 'false');

  if (isReducedMotion) {
    applyThemeLightingInstant(isDaylight);
    return;
  }

  // Set up 600ms easing targets
  themeAnimStartTime = performance.now();
  isThemeTransitioning = true;

  if (keyLight) startKeyColor.copy(keyLight.color);
  targetKeyColor.set(isDaylight ? 0xFFF0DD : 0xFFE3CA);

  startRimIntensity = rimLight ? rimLight.intensity : 2.6;
  targetRimIntensity = isDaylight ? 1.15 : 2.6;

  startEnvIntensity = scene ? scene.environmentIntensity : 0.55;
  targetEnvIntensity = isDaylight ? 0.70 : 0.55;
}

function applyThemeLightingInstant(daylight) {
  if (keyLight) keyLight.color.set(daylight ? 0xFFF0DD : 0xFFE3CA);
  if (rimLight) rimLight.intensity = daylight ? 1.15 : 2.6;
  if (scene) scene.environmentIntensity = daylight ? 0.70 : 0.55;
  if (groundSprite) {
    groundSprite.material.color.set(daylight ? 0x9B4B35 : 0xD67A4F);
    groundSprite.material.opacity = daylight ? 0.45 : 0.85;
  }
  renderSingleFrame();
}

// Cubic-bezier (.22,.8,.2,1) solver approximation
function solveCubicBezier(p1x, p1y, p2x, p2y, t) {
  // Approximate cubic bezier easing
  const u = 1 - t;
  return 3 * u * u * t * p1y + 3 * u * t * t * p2y + t * t * t;
}

function updateThemeTransition(now) {
  if (!isThemeTransitioning) return;

  const elapsed = now - themeAnimStartTime;
  const progress = Math.min(1.0, elapsed / 600);
  const eased = solveCubicBezier(0.22, 0.8, 0.2, 1.0, progress);

  if (keyLight) {
    keyLight.color.lerpColors(startKeyColor, targetKeyColor, eased);
  }
  if (rimLight) {
    rimLight.intensity = THREE.MathUtils.lerp(startRimIntensity, targetRimIntensity, eased);
  }
  if (scene) {
    scene.environmentIntensity = THREE.MathUtils.lerp(startEnvIntensity, targetEnvIntensity, eased);
  }

  if (progress >= 1.0) {
    isThemeTransitioning = false;
  }
}

/* --- SELECTION CHANGE & CHOREOGRAPHED TRANSITIONS --- */
function selectEdition(editionId) {
  if (editionId === activeEditionId || isSwappingModel) return;

  const oldEdition = EDITIONS[activeEditionId];
  const newEdition = EDITIONS[editionId];
  if (!newEdition) return;

  activeEditionId = editionId;
  fadeHint();

  // Update tabs active state
  watchTabs.forEach((tab) => {
    const isSelected = tab.getAttribute('data-edition') === editionId;
    tab.classList.toggle('is-active', isSelected);
    tab.setAttribute('aria-selected', isSelected ? 'true' : 'false');
  });

  // Update live-region title
  accessibleAnnouncer.textContent = `${newEdition.name} selected`;

  // Pre-update static elements before incoming animation
  stageCaption.textContent = newEdition.caption;
  movementCrop.style.backgroundImage = `url('${newEdition.image}')`;
  movementCrop.style.backgroundPosition = newEdition.crop;

  if (isReducedMotion) {
    // 1ms immediate state change
    applyDetailCardData(newEdition);
    loadWatchModel(editionId);
    return;
  }

  // --- Choreographed 3D and UI Transition ---
  isSwappingModel = true;

  // 1. Shrink ground bloom to scaleX(.68) in 300ms
  groundBloom.classList.remove('is-restoring');
  groundBloom.classList.add('is-shrinking');

  // 2. Sink existing card blocks in 140ms
  const detailBlocks = document.querySelectorAll('.detail-block');
  detailBlocks.forEach((block) => block.classList.add('is-sinking'));

  // 3. Send outgoing holder 26px right in screen space and scale to .90 over 300ms
  const swapStartTime = performance.now();
  const outgoingStartPos = holder.position.x;
  const outgoingStartScale = holder.scale.x;

  function animateOutgoing(now) {
    const elapsed = now - swapStartTime;
    const progress = Math.min(1.0, elapsed / 300);
    const ease = progress * progress; // ease-in

    // 26px in world coordinates is approx +0.075 units
    holder.position.x = THREE.MathUtils.lerp(outgoingStartPos, 0.08, ease);
    const s = THREE.MathUtils.lerp(outgoingStartScale, 0.90, ease);
    holder.scale.set(s, s, s);

    if (progress < 1.0) {
      requestAnimationFrame(animateOutgoing);
    } else {
      // Step 4: Swap model asset
      loadWatchModel(editionId);

      // Update detail card content before incoming rows appear
      applyDetailCardData(newEdition);

      // Step 5: Bring incoming holder from 30px left (-0.09) and .88 scale over 480ms with cubic-bezier(.16,1,.3,1)
      // and restore ground bloom with same easing
      groundBloom.classList.remove('is-shrinking');
      groundBloom.classList.add('is-restoring');

      const incomingStartTime = performance.now();

      function animateIncoming(inNow) {
        const inElapsed = inNow - incomingStartTime;
        const inProgress = Math.min(1.0, inElapsed / 480);
        const inEase = solveCubicBezier(0.16, 1.0, 0.3, 1.0, inProgress);

        holder.position.x = THREE.MathUtils.lerp(-0.09, 0.0, inEase);
        const inScale = THREE.MathUtils.lerp(0.88, 1.0, inEase);
        holder.scale.set(inScale, inScale, inScale);

        if (inProgress < 1.0) {
          requestAnimationFrame(animateIncoming);
        } else {
          holder.position.x = 0;
          holder.scale.set(1, 1, 1);
          isSwappingModel = false;
        }
      }

      requestAnimationFrame(animateIncoming);

      // Step 6: Return eyebrow, title, tags, lede, traits, setting, detail action in order
      // Offset every return by 45ms. Each rises 12px and fades over 320ms.
      const blockOrder = [
        document.querySelector('.detail-eyebrow-block'),
        document.querySelector('.detail-title-block'),
        document.querySelector('.detail-tags-block'),
        document.querySelector('.detail-lede-block'),
        document.querySelector('.detail-traits-block'),
        document.querySelector('.detail-setting-block'),
        document.querySelector('.detail-action-block')
      ];

      blockOrder.forEach((block, idx) => {
        if (!block) return;
        setTimeout(() => {
          block.classList.remove('is-sinking');
        }, idx * 45);
      });
    }
  }

  requestAnimationFrame(animateOutgoing);
}

function applyDetailCardData(edition) {
  detailEyebrow.textContent = edition.eyebrow;
  detailTitle.textContent = edition.name;
  detailLede.textContent = edition.lede;
  detailSetting.textContent = edition.setting;
  detailActionText.textContent = edition.detailAction;

  // Tags
  detailTags.innerHTML = '';
  edition.tags.forEach((tag) => {
    const span = document.createElement('span');
    span.className = 'tag-pill';
    span.setAttribute('role', 'listitem');
    span.textContent = tag;
    detailTags.appendChild(span);
  });

  // Traits
  document.getElementById('trait-val-case').textContent = edition.traits[0].value;
  document.getElementById('trait-val-calibre').textContent = edition.traits[1].value;
  document.getElementById('trait-val-reserve').textContent = edition.traits[2].value;
  document.getElementById('trait-val-water').textContent = edition.traits[3].value;
}

/* --- FOCUS MODE (EXPAND VIEWER) --- */
function toggleFocusMode() {
  isFocusMode = !isFocusMode;
  document.body.classList.toggle('is-focus-mode', isFocusMode);
  btnExpandViewer.setAttribute('aria-pressed', isFocusMode ? 'true' : 'false');

  if (isFocusMode) {
    exitFocusBtn.focus();
  } else {
    btnExpandViewer.focus();
  }

  updateCameraAndResize();
}

/* --- GESTURE & POINTER CONTROLS --- */
function setupInteractions() {
  // 1. Stage Drag & Rotate
  stageContainer.addEventListener('pointerdown', (e) => {
    // Only drag on primary click/touch
    if (e.button !== 0) return;
    isDragging = true;
    stageContainer.classList.add('is-dragging');
    pointerStartX = e.clientX;
    pointerStartY = e.clientY;
    lastPointerX = e.clientX;
    lastPointerY = e.clientY;
    angularVelX = 0;
    angularVelY = 0;
    lastInputTime = performance.now();
    fadeHint();

    stageContainer.setPointerCapture(e.pointerId);
  });

  stageContainer.addEventListener('pointermove', (e) => {
    if (!isDragging) return;
    const dx = e.clientX - lastPointerX;
    const dy = e.clientY - lastPointerY;
    lastPointerX = e.clientX;
    lastPointerY = e.clientY;

    const SENSITIVITY = 0.007;
    angularVelX = dx * SENSITIVITY;
    angularVelY = dy * SENSITIVITY;

    targetYaw += angularVelX;
    targetPitch = THREE.MathUtils.clamp(targetPitch + angularVelY, -0.48, 0.48);
    lastInputTime = performance.now();
  });

  function stopDrag(e) {
    if (!isDragging) return;
    isDragging = false;
    stageContainer.classList.remove('is-dragging');
    try {
      stageContainer.releasePointerCapture(e.pointerId);
    } catch (_) {}
  }

  stageContainer.addEventListener('pointerup', stopDrag);
  stageContainer.addEventListener('pointercancel', stopDrag);

  // 2. Wheel Zoom (clamp 0.55 to 3.4)
  stageContainer.addEventListener('wheel', (e) => {
    e.preventDefault();
    const zoomDelta = e.deltaY * 0.0016;
    targetDistance = THREE.MathUtils.clamp(targetDistance + zoomDelta, 0.55, 3.4);
    lastInputTime = performance.now();
    fadeHint();
  }, { passive: false });

  // 3. Double-click reset to home yaw .45, pitch .12, distance
  stageContainer.addEventListener('dblclick', () => {
    targetYaw = HOME_YAW;
    targetPitch = HOME_PITCH;
    targetDistance = HOME_DISTANCE;
    angularVelX = 0;
    angularVelY = 0;
    lastInputTime = performance.now();
    fadeHint();
  });

  // 4. Utility Controls
  btnZoomIn.addEventListener('click', () => {
    targetDistance = THREE.MathUtils.clamp(targetDistance - 0.16, 0.55, 3.4);
    lastInputTime = performance.now();
    fadeHint();
  });

  btnZoomOut.addEventListener('click', () => {
    targetDistance = THREE.MathUtils.clamp(targetDistance + 0.16, 0.55, 3.4);
    lastInputTime = performance.now();
    fadeHint();
  });

  btnExpandViewer.addEventListener('click', toggleFocusMode);
  exitFocusBtn.addEventListener('click', toggleFocusMode);
  btnToggleDaylight.addEventListener('click', toggleDaylight);

  // 5. Turn Controls
  // Left arrow: changes target yaw by Math.PI / 4
  btnTurnLeft.addEventListener('click', () => {
    targetYaw -= Math.PI / 4;
    lastInputTime = performance.now();
    fadeHint();
  });

  // Right arrow: changes target yaw by Math.PI / 4
  btnTurnRight.addEventListener('click', () => {
    targetYaw += Math.PI / 4;
    lastInputTime = performance.now();
    fadeHint();
  });

  // Full rotation (360°): adds Math.PI * 2 over 900ms
  btnTurnFull.addEventListener('click', () => {
    if (isRotatingFull) return;
    if (isReducedMotion) {
      targetYaw += Math.PI * 2;
      currentYaw = targetYaw;
      return;
    }
    isRotatingFull = true;
    fullRotationStartTime = performance.now();
    fullRotationStartAngle = currentYaw;
    lastInputTime = performance.now();
    fadeHint();
  });

  // 6. Tabs
  watchTabs.forEach((tab) => {
    tab.addEventListener('click', () => {
      const id = tab.getAttribute('data-edition');
      selectEdition(id);
    });
  });

  // 7. Search filter
  editionSearch.addEventListener('input', (e) => {
    const query = e.target.value.toLowerCase().trim();
    if (!query) return;

    for (const [id, ed] of Object.entries(EDITIONS)) {
      if (
        ed.name.toLowerCase().includes(query) ||
        ed.calibre.toLowerCase().includes(query) ||
        ed.tags.some((t) => t.toLowerCase().includes(query)) ||
        ed.lede.toLowerCase().includes(query)
      ) {
        selectEdition(id);
        break;
      }
    }
  });

  // 8. Movement detail action trigger
  document.getElementById('btn-detail-action').addEventListener('click', () => {
    // Smoothly focus closer to watch movement
    targetDistance = THREE.MathUtils.clamp(targetDistance - 0.35, 0.65, 3.4);
    lastInputTime = performance.now();
  });
}

function fadeHint() {
  if (!hintFaded && stageHint) {
    stageHint.classList.add('is-faded');
    hintFaded = true;
  }
}

/* --- RENDER LOOP & IDLE BEHAVIOR --- */
function startRenderLoop() {
  if (isLoopRunning) return;
  isLoopRunning = true;

  function loop(now) {
    if (!isLoopRunning) return;
    frameCount++;

    animationFrameId = requestAnimationFrame(loop);

    // Update 600ms lighting transitions
    updateThemeTransition(now);

    // Handle full 360 rotation over 900ms
    if (isRotatingFull) {
      const elapsed = now - fullRotationStartTime;
      const progress = Math.min(1.0, elapsed / 900);
      const ease = solveCubicBezier(0.22, 0.8, 0.2, 1.0, progress);
      currentYaw = fullRotationStartAngle + Math.PI * 2 * ease;
      targetYaw = currentYaw;
      if (progress >= 1.0) {
        isRotatingFull = false;
      }
    }

    // Apply inertia damping (.925 per rendered frame)
    if (!isDragging && !isRotatingFull && !isReducedMotion) {
      angularVelX *= 0.925;
      angularVelY *= 0.925;
      targetYaw += angularVelX;
      targetPitch = THREE.MathUtils.clamp(targetPitch + angularVelY, -0.48, 0.48);
    }

    // Smoothly interpolate current yaw, pitch, distance toward targets
    if (isReducedMotion) {
      currentYaw = targetYaw;
      currentPitch = targetPitch;
      currentDistance = targetDistance;
    } else {
      currentYaw += (targetYaw - currentYaw) * 0.12;
      currentPitch += (targetPitch - currentPitch) * 0.12;
      currentDistance += (targetDistance - currentDistance) * 0.12;
    }

    // Idle Rest State:
    // After 2800ms without stage input, ease yaw and pitch toward saved pose using .018 interpolation.
    // During rest state: add sin(time * .00055) * .04 yaw to spin.
    // Add sin(time * .0007) * .018 vertical motion to holder.
    // Stop idle movement while dragging, swapping models, using reduced motion, or changing focus state.
    const idleElapsed = now - lastInputTime;
    const canIdle = !isDragging && !isSwappingModel && !isReducedMotion && !isFocusMode && !isRotatingFull;

    if (canIdle && idleElapsed > 2800) {
      targetYaw += (HOME_YAW - targetYaw) * 0.018;
      targetPitch += (HOME_PITCH - targetPitch) * 0.018;

      spin.rotation.y = Math.sin(now * 0.00055) * 0.04;
      holder.position.y = Math.sin(now * 0.0007) * 0.018;
    } else {
      spin.rotation.y = 0;
      if (!isSwappingModel) holder.position.y = 0;
    }

    pivot.rotation.y = currentYaw;
    pivot.rotation.x = currentPitch;
    camera.position.z = currentDistance;

    // Render Three.js frame
    renderer.render(scene, camera);
  }

  animationFrameId = requestAnimationFrame(loop);
}

function renderSingleFrame() {
  if (renderer && scene && camera) {
    pivot.rotation.y = currentYaw;
    pivot.rotation.x = currentPitch;
    camera.position.z = currentDistance;
    renderer.render(scene, camera);
  }
}

function stopRenderLoop() {
  isLoopRunning = false;
  if (animationFrameId) {
    cancelAnimationFrame(animationFrameId);
    animationFrameId = null;
  }
}

/* --- VISIBILITY & INTERSECTION OBSERVER SUSPENSION --- */
function setupVisibilitySuspension() {
  // Suspend when tab is hidden
  document.addEventListener('visibilitychange', () => {
    if (document.hidden) {
      stopRenderLoop();
    } else {
      startRenderLoop();
    }
  });

  // Suspend render loop with IntersectionObserver at .05 threshold
  const observer = new IntersectionObserver((entries) => {
    const entry = entries[0];
    if (entry && entry.isIntersecting) {
      startRenderLoop();
    } else {
      stopRenderLoop();
    }
  }, { threshold: 0.05 });

  observer.observe(stageContainer);
}

/* --- BOOTSTRAP --- */
window.addEventListener('DOMContentLoaded', () => {
  initThree();
  setupInteractions();
  setupVisibilitySuspension();
});
