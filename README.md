# Haldor & Vey — Atelier Watch House

An interactive, one-screen product viewer for the fictional **Haldor & Vey** watch house. Built with pure vanilla HTML5, CSS3, and an ES module using Three.js 0.170.0.

![Haldor & Vey Watch Viewer](assets/hero-plate.jpg)

---

## Features

- **Interactive 3D Watch Study**: Alpha-enabled WebGL canvas running Three.js 0.170.0 with physically based PBR shading, metallic reflections, and `RoomEnvironment` PMREM lighting.
- **Atmospheric Palette**: 8-layer composite background:
  1. `hero-plate.jpg` (2560×1440 gallery background) with silent `poster.jpg` fallback
  2. `plum-cast` radial warmth near 70% X and 45% Y
  3. `top-shade` (28% black upper gradient)
  4. `lower-shade` (58% terminal opacity black gradient)
  5. `webgl-canvas` (single alpha canvas across the entire viewport)
  6. `ground-bloom` (restrained radial bloom underneath the case)
  7. `static-grain` (monochrome film grain)
  8. HTML interface
- **Six Local Watch Editions**:
  - **Serein No. 02**: Hand-wound, frost-silver dial, exposed balance wheel beneath steel bridge.
  - **Nacre No. 05**: Automatic, iridescent mother-of-pearl dial with warm rose gold tones.
  - **Orison No. 08**: GMT complication, deep slate-grey dial with 24-hour ring and burnt-orange GMT hand.
  - **Hedra No. 11**: Chronograph, rich umber dial with dual recessed subdial counters and pump pushers.
  - **Kestrel No. 14**: Field watch, matte sand dial with military Arabic numerals and canvas strap.
  - **Vanta No. 17**: Calendar watch, ultra-deep black lacquer dial with moonphase aperture.
- **Lighting & Daylight Choreography**:
  - Dark mode tokens and daylight mode tokens transition over 600ms via `cubic-bezier(.22, .8, .2, 1)`.
  - Three.js warm vellum key light, terracotta rim light, and environment intensity dynamically animate through the same 600ms curve.
- **Gestures & Controls**:
  - Pointer capture rotation with angular velocity and `.925` inertial decay per frame.
  - Wheel and pinch distance adjustment clamped between `0.55` and `3.4`.
  - Double-click resets to home pose (`yaw: 0.45`, `pitch: 0.12`).
  - Quarter-turn buttons (`±45°`) and full 360° rotation over 900ms.
  - Rest state easing toward home pose after 2800ms of inactivity with subtle idle breathing.
  - Focus mode (expanded viewer) that clears interface elements and realigns camera.
- **Zero Remote Dependencies at Runtime**: All models (`.glb`), transparent cut-outs (`.png`), gallery plates (`.jpg`), and Draco decoders are local assets.
- **Accessibility & Performance**:
  - Full WCAG AA compliance, semantic markup, and polite screen reader announcements (`aria-live="polite"`).
  - Respects `prefers-reduced-motion: reduce` with 1ms state transitions and disabled inertia.
  - Render loop automatically suspends when hidden or off-screen.

---

## Project Structure

```text
├── index.html                  # Semantic one-screen viewer layout
├── styles.css                  # Custom properties, glassmorphism, responsive grid
├── app.js                      # Vanilla Three.js 3D viewer & state choreography
├── .gitignore                  # Clean repository ignore rules
├── assets/
│   ├── hero-plate.jpg          # 2560×1440 static gallery backdrop
│   ├── poster.jpg              # 1600×900 fallback backdrop
│   ├── watch-*.png             # Transparent cut-outs for all 6 editions
│   ├── models/
│   │   └── *.glb               # glTF 2.0 binary models with PBR materials
│   └── draco/
│       ├── draco_decoder.js
│       ├── draco_decoder.wasm
│       └── draco_wasm_wrapper.js
└── scripts/
    ├── generate_images.py      # Image generator for backdrops and cut-outs
    └── generate_models.py      # Procedural glTF 2.0 binary watch builder
```

---

## Getting Started

No build process or installation is required. Run any static HTTP server:

```bash
# Python
python -m http.server 8080

# Or Node npx serve
npx serve .
```

Open `http://localhost:8080` in any modern web browser.
