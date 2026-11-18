import struct
import json
import math
import io
import os
from PIL import Image, ImageDraw, ImageFilter

os.makedirs('assets/models', exist_ok=True)

def generate_dial_texture(spec):
    size = 512
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    cx, cy = size // 2, size // 2
    r_dial = 246

    d_type = spec['dial_type']
    
    # 1. Base Dial Color / Background
    if d_type == 'pearl':
        # Nacre Mother-of-Pearl
        draw.ellipse([cx - r_dial, cy - r_dial, cx + r_dial, cy + r_dial], fill=(244, 238, 232, 255))
        for a, col in [(0.5, (238, 210, 222, 90)), (1.8, (215, 230, 235, 80)), (3.2, (248, 230, 208, 100)), (4.7, (225, 212, 238, 70))]:
            sx = cx + int(70 * math.cos(a))
            sy = cy + int(70 * math.sin(a))
            draw.ellipse([sx - 110, sy - 90, sx + 110, sy + 90], fill=col)
            
    elif d_type == 'silver':
        # Serein Frost Silver sunburst
        draw.ellipse([cx - r_dial, cy - r_dial, cx + r_dial, cy + r_dial], fill=(225, 228, 232, 255))
        for i in range(360):
            ang = i * math.pi / 180
            ex = cx + int(r_dial * math.cos(ang))
            ey = cy + int(r_dial * math.sin(ang))
            val = 215 + int(28 * (math.sin(ang * 8) ** 2))
            draw.line([(cx, cy), (ex, ey)], fill=(val, val+2, val+4, 180), width=2)
            
    elif d_type == 'slate':
        # Orison Slate Grey
        draw.ellipse([cx - r_dial, cy - r_dial, cx + r_dial, cy + r_dial], fill=(54, 60, 65, 255))
        for i in range(360):
            ang = i * math.pi / 180
            ex = cx + int(r_dial * math.cos(ang))
            ey = cy + int(r_dial * math.sin(ang))
            val = 50 + int(24 * (math.sin(ang * 6) ** 2))
            draw.line([(cx, cy), (ex, ey)], fill=(val, val+3, val+6, 160), width=2)
        r_gmt = int(r_dial * 0.65)
        draw.ellipse([cx - r_gmt, cy - r_gmt, cx + r_gmt, cy + r_gmt], outline=(35, 40, 44, 255), width=24)
        for h24 in range(24):
            ang = -math.pi/2 + h24 * (math.pi / 12)
            gx = cx + int(r_gmt * math.cos(ang))
            gy = cy + int(r_gmt * math.sin(ang))
            col = (214, 122, 79, 255) if h24 % 6 == 0 else (180, 185, 190, 220)
            draw.ellipse([gx-3, gy-3, gx+3, gy+3], fill=col)
            
    elif d_type == 'umber':
        # Hedra Umber
        draw.ellipse([cx - r_dial, cy - r_dial, cx + r_dial, cy + r_dial], fill=(72, 48, 38, 255))
        for r in range(r_dial, 0, -3):
            factor = 0.9 + 0.18 * (math.sin(r * 0.2) ** 2)
            c = (int(74 * factor), int(50 * factor), int(40 * factor), 255)
            draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=c, width=2)
        for sub_x in [cx - 96, cx + 96]:
            sr = 50
            draw.ellipse([sub_x - sr, cy - sr, sub_x + sr, cy + sr], fill=(52, 34, 26, 255), outline=(140, 100, 80, 255), width=2)
            for s_r in range(sr, 0, -4):
                draw.ellipse([sub_x - s_r, cy - s_r, sub_x + s_r, cy + s_r], outline=(85, 58, 46, 180), width=1)
                
    elif d_type == 'sand':
        # Kestrel Sand
        draw.ellipse([cx - r_dial, cy - r_dial, cx + r_dial, cy + r_dial], fill=(222, 210, 188, 255))
        for r in range(r_dial, 0, -4):
            draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(214, 202, 180, 160), width=2)
            
    elif d_type == 'black':
        # Vanta Black Lacquer
        draw.ellipse([cx - r_dial, cy - r_dial, cx + r_dial, cy + r_dial], fill=(18, 17, 20, 255))
        for r in range(r_dial, 0, -4):
            val = int(16 + 12 * (1 - r / r_dial))
            draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(val, val-1, val+2, 255), width=2)
        # Moonphase aperture at 6 o'clock
        mp_cx, mp_cy = cx, cy + 92
        draw.ellipse([mp_cx - 72, mp_cy - 44, mp_cx + 72, mp_cy + 44], fill=(12, 18, 36, 255), outline=(214, 175, 95, 255), width=2)
        draw.ellipse([mp_cx - 18, mp_cy - 18, mp_cx + 18, mp_cy + 18], fill=(235, 195, 110, 255))
        # Stars
        for sx, sy in [(mp_cx - 36, mp_cy - 10), (mp_cx + 38, mp_cy - 8), (mp_cx - 16, mp_cy + 12), (mp_cx + 26, mp_cy + 14)]:
            draw.ellipse([sx-2, sy-2, sx+2, sy+2], fill=(255, 240, 200, 255))
        # Date window at 3 o'clock
        dw_x, dw_y = cx + 115, cy
        draw.rectangle([dw_x - 16, dw_y - 12, dw_x + 16, dw_y + 12], fill=(245, 242, 238, 255), outline=(190, 160, 100, 255), width=2)
        draw.text((dw_x - 7, dw_y - 7), "17", fill=(20, 20, 20, 255))

    # Open balance / rotor bridge at 6 o'clock for Serein and Nacre
    if spec['id'] == 'serein-02':
        bx, by = cx, cy + 94
        draw.ellipse([bx - 52, by - 52, bx + 52, by + 52], fill=(32, 34, 38, 255), outline=(160, 165, 170, 255), width=3)
        draw.ellipse([bx - 40, by - 40, bx + 40, by + 40], outline=(230, 190, 100, 255), width=4)
        draw.line([(bx - 50, by), (bx + 50, by)], fill=(210, 215, 220, 255), width=6)
        draw.ellipse([bx - 7, by - 7, bx + 7, by + 7], fill=(200, 35, 65, 255), outline=(230, 190, 100, 255), width=2)
        
    elif spec['id'] == 'nacre-05':
        bx, by = cx, cy + 90
        draw.ellipse([bx - 46, by - 46, bx + 46, by + 46], fill=(38, 28, 32, 255), outline=(220, 170, 130, 255), width=3)
        draw.ellipse([bx - 34, by - 34, bx + 34, by + 34], outline=(235, 195, 120, 255), width=3)
        draw.line([(bx - 44, by), (bx + 44, by)], fill=(225, 175, 140, 255), width=5)
        draw.ellipse([bx - 6, by - 6, bx + 6, by + 6], fill=(210, 45, 80, 255), outline=(235, 195, 120, 255), width=2)

    # Dial Chapter Ring & Markers
    mk_col = spec['marker_color']
    for h in range(12):
        ang = h * (math.pi / 6) - math.pi / 2
        r_out = r_dial - 10
        r_in = r_dial - 36 if h % 3 == 0 else r_dial - 26
        x1 = cx + int(r_out * math.cos(ang))
        y1 = cy + int(r_out * math.sin(ang))
        x2 = cx + int(r_in * math.cos(ang))
        y2 = cy + int(r_in * math.sin(ang))
        draw.line([(x1, y1), (x2, y2)], fill=mk_col, width=6 if h % 3 == 0 else 4)

    # Minute track dots
    for m in range(60):
        if m % 5 != 0:
            ang = m * (math.pi / 30) - math.pi / 2
            mx = cx + int((r_dial - 12) * math.cos(ang))
            my = cy + int((r_dial - 12) * math.sin(ang))
            draw.ellipse([mx - 2, my - 2, mx + 2, my + 2], fill=(mk_col[0], mk_col[1], mk_col[2], 180))

    # Brand text representation at 12 o'clock
    ty = cy - 95
    b_col = (mk_col[0], mk_col[1], mk_col[2], 240)
    draw.line([(cx - 42, ty), (cx + 42, ty)], fill=b_col, width=2)
    draw.line([(cx - 24, ty + 10), (cx + 24, ty + 10)], fill=(mk_col[0], mk_col[1], mk_col[2], 160), width=1)

    buf = io.BytesIO()
    img.save(buf, format='PNG')
    return buf.getvalue()


def build_full_watch_glb(spec):
    filename = spec['file']
    print(f"Building high-fidelity GLB: {filename}...")

    vertices = []
    normals = []
    uvs = []
    indices = []
    primitives = []

    def add_primitive(verts, norms, uvs_list, inds, mat_idx):
        nonlocal vertices, normals, uvs, indices, primitives
        base_v = len(vertices)
        min_p = [float('inf')]*3
        max_p = [float('-inf')]*3
        for v in verts:
            for i in range(3):
                min_p[i] = min(min_p[i], v[i])
                max_p[i] = max(max_p[i], v[i])
            vertices.append(v)
        normals.extend(norms)
        uvs.extend(uvs_list)
        idx_start = len(indices)
        for ind in inds:
            indices.append(ind)
        primitives.append({
            "material": mat_idx,
            "vertex_offset": base_v,
            "vertex_count": len(verts),
            "index_offset": idx_start,
            "index_count": len(inds),
            "min_pos": min_p,
            "max_pos": max_p
        })

    # --- GEOMETRY BUILDERS ---

    # 1. Bezel Ring (Annulus facing +Z)
    def make_annulus(r_inner, r_outer, z, normal, segments, mat_idx):
        verts, norms, uv_arr, inds = [], [], [], []
        nx, ny, nz = normal
        for i in range(segments + 1):
            theta = (i / segments) * 2 * math.pi
            cos_t, sin_t = math.cos(theta), math.sin(theta)
            # inner
            verts.append([r_inner * cos_t, r_inner * sin_t, z])
            norms.append([nx, ny, nz])
            uv_arr.append([0.5 + 0.5 * (r_inner/r_outer) * cos_t, 0.5 + 0.5 * (r_inner/r_outer) * sin_t])
            # outer
            verts.append([r_outer * cos_t, r_outer * sin_t, z])
            norms.append([nx, ny, nz])
            uv_arr.append([0.5 + 0.5 * cos_t, 0.5 + 0.5 * sin_t])

        for i in range(segments):
            idx = i * 2
            inds.extend([idx, idx + 1, idx + 2])
            inds.extend([idx + 2, idx + 1, idx + 3])

        add_primitive(verts, norms, uv_arr, inds, mat_idx)

    # 2. Beveled Ring / Frustum
    def make_frustum(r_top, r_bot, z_top, z_bot, segments, mat_idx):
        verts, norms, uv_arr, inds = [], [], [], []
        dz = z_top - z_bot
        dr = r_bot - r_top
        length = math.sqrt(dr*dr + dz*dz)
        nr = dz / length
        nz = dr / length

        for i in range(segments + 1):
            theta = (i / segments) * 2 * math.pi
            cos_t, sin_t = math.cos(theta), math.sin(theta)
            # top
            verts.append([r_top * cos_t, r_top * sin_t, z_top])
            norms.append([nr * cos_t, nr * sin_t, nz])
            uv_arr.append([i / segments, 1.0])
            # bot
            verts.append([r_bot * cos_t, r_bot * sin_t, z_bot])
            norms.append([nr * cos_t, nr * sin_t, nz])
            uv_arr.append([i / segments, 0.0])

        for i in range(segments):
            idx = i * 2
            inds.extend([idx, idx + 1, idx + 2])
            inds.extend([idx + 2, idx + 1, idx + 3])

        add_primitive(verts, norms, uv_arr, inds, mat_idx)

    # 3. Dial Disc (at z=0.045) with Texturing
    def make_dial_disc(radius, z, segments, mat_idx):
        verts, norms, uv_arr, inds = [], [], [], []
        verts.append([0.0, 0.0, z])
        norms.append([0.0, 0.0, 1.0])
        uv_arr.append([0.5, 0.5])

        for i in range(segments + 1):
            theta = (i / segments) * 2 * math.pi
            cos_t, sin_t = math.cos(theta), math.sin(theta)
            verts.append([radius * cos_t, radius * sin_t, z])
            norms.append([0.0, 0.0, 1.0])
            uv_arr.append([0.5 + 0.5 * cos_t, 0.5 - 0.5 * sin_t])

        for i in range(segments):
            inds.extend([0, i + 1, i + 2])

        add_primitive(verts, norms, uv_arr, inds, mat_idx)

    # 4. Rotated Hand Builder
    def make_watch_hand(angle, length, width_base, width_tip, z, height, mat_idx):
        verts, norms, uv_arr, inds = [], [], [], []
        cos_a = math.cos(angle)
        sin_a = math.sin(angle)
        perp_x = -sin_a
        perp_y = cos_a

        pts_2d = [
            (-perp_x * width_base / 2, -perp_y * width_base / 2),
            ( perp_x * width_base / 2,  perp_y * width_base / 2),
            (cos_a * length + perp_x * width_tip / 2, sin_a * length + perp_y * width_tip / 2),
            (cos_a * length - perp_x * width_tip / 2, sin_a * length - perp_y * width_tip / 2)
        ]

        top_start = len(verts)
        for px, py in pts_2d:
            verts.append([px, py, z + height/2])
            norms.append([0.0, 0.0, 1.0])
            uv_arr.append([0.5, 0.5])
        inds.extend([top_start, top_start + 1, top_start + 2, top_start, top_start + 2, top_start + 3])

        bot_start = len(verts)
        for px, py in pts_2d:
            verts.append([px, py, z - height/2])
            norms.append([0.0, 0.0, -1.0])
            uv_arr.append([0.5, 0.5])
        inds.extend([bot_start, bot_start + 2, bot_start + 1, bot_start, bot_start + 3, bot_start + 2])

        add_primitive(verts, norms, uv_arr, inds, mat_idx)

    # 5. Box Helper
    def make_box(center, size, mat_idx):
        cx, cy, cz = center
        sx, sy, sz = size[0]/2, size[1]/2, size[2]/2
        verts, norms, uv_arr, inds = [], [], [], []
        faces = [
            ([cx-sx, cy-sy, cz+sz], [cx+sx, cy-sy, cz+sz], [cx+sx, cy+sy, cz+sz], [cx-sx, cy+sy, cz+sz], [0, 0, 1]),
            ([cx+sx, cy-sy, cz-sz], [cx-sx, cy-sy, cz-sz], [cx-sx, cy+sy, cz-sz], [cx+sx, cy+sy, cz-sz], [0, 0, -1]),
            ([cx-sx, cy+sy, cz+sz], [cx+sx, cy+sy, cz+sz], [cx+sx, cy+sy, cz-sz], [cx-sx, cy+sy, cz-sz], [0, 1, 0]),
            ([cx-sx, cy-sy, cz-sz], [cx+sx, cy-sy, cz-sz], [cx+sx, cy-sy, cz+sz], [cx-sx, cy-sy, cz+sz], [0, -1, 0]),
            ([cx+sx, cy-sy, cz+sz], [cx+sx, cy-sy, cz-sz], [cx+sx, cy+sy, cz-sz], [cx+sx, cy+sy, cz+sz], [1, 0, 0]),
            ([cx-sx, cy-sy, cz-sz], [cx-sx, cy-sy, cz+sz], [cx-sx, cy+sy, cz+sz], [cx-sx, cy+sy, cz-sz], [-1, 0, 0])
        ]
        for p0, p1, p2, p3, n in faces:
            base = len(verts)
            verts.extend([p0, p1, p2, p3])
            norms.extend([n, n, n, n])
            uv_arr.extend([[0, 0], [1, 0], [1, 1], [0, 1]])
            inds.extend([base, base + 1, base + 2, base, base + 2, base + 3])
        add_primitive(verts, norms, uv_arr, inds, mat_idx)

    # 6. Curved Strap
    def make_curved_strap(is_top, length, width, thickness, mat_idx):
        verts, norms, uv_arr, inds = [], [], [], []
        segments = 16
        half_w = width / 2
        sign = 1 if is_top else -1

        for i in range(segments + 1):
            t = i / segments
            y = sign * (0.86 + t * length)
            z = -0.04 - 0.42 * (t ** 1.5)
            dz = -0.42 * 1.5 * (t ** 0.5)
            ny = sign * dz
            nz = -1.0
            nl = math.sqrt(ny*ny + nz*nz)
            ny /= nl
            nz /= nl

            verts.append([-half_w, y, z + thickness/2])
            norms.append([0.0, -ny, -nz])
            uv_arr.append([0.0, t])

            verts.append([half_w, y, z + thickness/2])
            norms.append([0.0, -ny, -nz])
            uv_arr.append([1.0, t])

            verts.append([-half_w, y, z - thickness/2])
            norms.append([0.0, ny, nz])
            uv_arr.append([0.0, t])

            verts.append([half_w, y, z - thickness/2])
            norms.append([0.0, ny, nz])
            uv_arr.append([1.0, t])

        for i in range(segments):
            idx = i * 4
            nxt = (i + 1) * 4
            inds.extend([idx, idx + 1, nxt + 1, idx, nxt + 1, nxt])
            inds.extend([idx + 2, nxt + 3, idx + 3, idx + 2, nxt + 2, nxt + 3])
            inds.extend([idx, nxt, nxt + 2, idx, nxt + 2, idx + 2])
            inds.extend([idx + 1, nxt + 3, nxt + 1, idx + 1, idx + 3, nxt + 3])

        add_primitive(verts, norms, uv_arr, inds, mat_idx)

    # --- ASSEMBLE WATCH MESH ---
    # Bezel Top Face (Annulus at z = 0.08, r_in = 0.73, r_out = 0.88)
    make_annulus(r_inner=0.73, r_outer=0.88, z=0.08, normal=(0, 0, 1), segments=48, mat_idx=0)

    # Bezel Outer Chamfer (from r=0.88, z=0.08 down to r=0.93, z=0.03)
    make_frustum(r_top=0.88, r_bot=0.93, z_top=0.08, z_bot=0.03, segments=48, mat_idx=0)

    # Main Case Cylindrical Wall (from r=0.93, z=0.03 down to r=0.93, z=-0.12)
    make_frustum(r_top=0.93, r_bot=0.93, z_top=0.03, z_bot=-0.12, segments=48, mat_idx=0)

    # Inner Bezel Step (from r=0.73, z=0.08 down to r=0.72, z=0.045)
    make_frustum(r_top=0.73, r_bot=0.72, z_top=0.08, z_bot=0.045, segments=48, mat_idx=0)

    # Dial Face Disc (at z=0.045, radius=0.72)
    make_dial_disc(radius=0.72, z=0.045, segments=48, mat_idx=1)

    # Caseback Chamfer (from r=0.93, z=-0.12 to r=0.75, z=-0.15)
    make_frustum(r_top=0.93, r_bot=0.75, z_top=-0.12, z_bot=-0.15, segments=48, mat_idx=0)

    # 12 3D Metallic Hour Markers
    for h in range(12):
        ang = h * (math.pi / 6)
        r_mid = 0.61
        mx = r_mid * math.cos(ang)
        my = r_mid * math.sin(ang)
        hl = 0.08 if h % 3 == 0 else 0.05
        make_box([mx, my, 0.058], [hl, 0.03, 0.015], mat_idx=3)

    # 3D Hands at 10:10 pose
    make_watch_hand(angle=-2.15, length=0.42, width_base=0.042, width_tip=0.016, z=0.065, height=0.014, mat_idx=3)
    make_watch_hand(angle=-0.45, length=0.62, width_base=0.034, width_tip=0.014, z=0.076, height=0.012, mat_idx=3)
    make_watch_hand(angle=1.85, length=0.68, width_base=0.015, width_tip=0.008, z=0.086, height=0.008, mat_idx=4)
    make_annulus(0.0, 0.05, 0.09, (0, 0, 1), 24, 3)

    # 4 Solid Beveled Lugs
    lug_x = 0.54
    lug_y = 0.82
    make_box([-lug_x,  lug_y, -0.04], [0.14, 0.34, 0.16], 0)
    make_box([ lug_x,  lug_y, -0.04], [0.14, 0.34, 0.16], 0)
    make_box([-lug_x, -lug_y, -0.04], [0.14, 0.34, 0.16], 0)
    make_box([ lug_x, -lug_y, -0.04], [0.14, 0.34, 0.16], 0)

    # Winding Crown at 3 o'clock
    make_box([0.98, 0.0, -0.035], [0.12, 0.16, 0.12], 0)

    # Chronograph pushers if Hedra
    if spec.get('pushers'):
        p_ang1, p_ang2 = math.pi / 4.5, -math.pi / 4.5
        make_box([0.92 * math.cos(p_ang1), 0.92 * math.sin(p_ang1), -0.035], [0.10, 0.10, 0.10], 0)
        make_box([0.92 * math.cos(p_ang2), 0.92 * math.sin(p_ang2), -0.035], [0.10, 0.10, 0.10], 0)

    # Straps (top and bottom)
    make_curved_strap(is_top=True, length=0.82, width=0.74, thickness=0.06, mat_idx=2)
    make_curved_strap(is_top=False, length=0.82, width=0.74, thickness=0.06, mat_idx=2)

    # Movement Rotor on back (exhibition caseback)
    make_box([0.0, 0.20, -0.155], [0.50, 0.24, 0.02], 5)

    # --- GENERATE EMBEDDED DIAL TEXTURE ---
    dial_png_bytes = generate_dial_texture(spec)

    # --- PACK BINARY BUFFERS ---
    raw_pos = bytearray()
    for v in vertices:
        raw_pos.extend(struct.pack('<3f', v[0], v[1], v[2]))

    raw_norm = bytearray()
    for n in normals:
        raw_norm.extend(struct.pack('<3f', n[0], n[1], n[2]))

    raw_uv = bytearray()
    for uv in uvs:
        raw_uv.extend(struct.pack('<2f', uv[0], uv[1]))

    raw_idx = bytearray()
    for idx in indices:
        raw_idx.extend(struct.pack('<I', idx))

    def pad4(b, pad_byte=b'\x00'):
        pad = (4 - (len(b) % 4)) % 4
        return b + pad_byte * pad

    pos_bytes = pad4(raw_pos)
    norm_bytes = pad4(raw_norm)
    uv_bytes = pad4(raw_uv)
    idx_bytes = pad4(raw_idx)
    img_bytes = pad4(dial_png_bytes)

    pos_offset = 0
    norm_offset = pos_offset + len(pos_bytes)
    uv_offset = norm_offset + len(norm_bytes)
    idx_offset = uv_offset + len(uv_bytes)
    img_offset = idx_offset + len(idx_bytes)
    total_bin_length = img_offset + len(img_bytes)

    bin_buffer = pos_bytes + norm_bytes + uv_bytes + idx_bytes + img_bytes

    buffer_views = [
        {"buffer": 0, "byteOffset": pos_offset, "byteLength": len(raw_pos), "target": 34962},
        {"buffer": 0, "byteOffset": norm_offset, "byteLength": len(raw_norm), "target": 34962},
        {"buffer": 0, "byteOffset": uv_offset, "byteLength": len(raw_uv), "target": 34962},
        {"buffer": 0, "byteOffset": idx_offset, "byteLength": len(raw_idx), "target": 34963},
        {"buffer": 0, "byteOffset": img_offset, "byteLength": len(dial_png_bytes)}
    ]

    accessors = []
    gltf_primitives = []

    for prim in primitives:
        idx_acc = len(accessors)
        accessors.append({
            "bufferView": 3,
            "byteOffset": prim["index_offset"] * 4,
            "componentType": 5125,
            "count": prim["index_count"],
            "type": "SCALAR"
        })

        pos_acc = len(accessors)
        accessors.append({
            "bufferView": 0,
            "byteOffset": prim["vertex_offset"] * 12,
            "componentType": 5126,
            "count": prim["vertex_count"],
            "type": "VEC3",
            "min": prim["min_pos"],
            "max": prim["max_pos"]
        })

        norm_acc = len(accessors)
        accessors.append({
            "bufferView": 1,
            "byteOffset": prim["vertex_offset"] * 12,
            "componentType": 5126,
            "count": prim["vertex_count"],
            "type": "VEC3"
        })

        uv_acc = len(accessors)
        accessors.append({
            "bufferView": 2,
            "byteOffset": prim["vertex_offset"] * 8,
            "componentType": 5126,
            "count": prim["vertex_count"],
            "type": "VEC2"
        })

        gltf_primitives.append({
            "attributes": {
                "POSITION": pos_acc,
                "NORMAL": norm_acc,
                "TEXCOORD_0": uv_acc
            },
            "indices": idx_acc,
            "material": prim["material"]
        })

    materials = [
        # 0: Case Metal
        {
            "name": "CaseMetal",
            "pbrMetallicRoughness": {
                "baseColorFactor": spec['case_color'],
                "metallicFactor": 0.95,
                "roughnessFactor": 0.20 if spec.get('case_finish') != 'matte' else 0.55
            }
        },
        # 1: Dial with embedded texture!
        {
            "name": "Dial",
            "pbrMetallicRoughness": {
                "baseColorTexture": {"index": 0},
                "metallicFactor": spec.get('dial_metallic', 0.20),
                "roughnessFactor": spec.get('dial_roughness', 0.35)
            }
        },
        # 2: Strap
        {
            "name": "Strap",
            "pbrMetallicRoughness": {
                "baseColorFactor": spec['strap_color'],
                "metallicFactor": 0.05,
                "roughnessFactor": 0.70
            }
        },
        # 3: Hands & Markers
        {
            "name": "HandsAndMarkers",
            "pbrMetallicRoughness": {
                "baseColorFactor": spec['hands_color'],
                "metallicFactor": 0.95,
                "roughnessFactor": 0.15
            }
        },
        # 4: Accent / Sec hand
        {
            "name": "Accent",
            "pbrMetallicRoughness": {
                "baseColorFactor": spec['accent_color'],
                "metallicFactor": 0.85,
                "roughnessFactor": 0.20
            }
        },
        # 5: Exhibition Rotor
        {
            "name": "MovementRotor",
            "pbrMetallicRoughness": {
                "baseColorFactor": [0.94, 0.78, 0.45, 1.0],
                "metallicFactor": 0.94,
                "roughnessFactor": 0.22
            }
        }
    ]

    textures = [{"sampler": 0, "source": 0}]
    images = [{"bufferView": 4, "mimeType": "image/png"}]
    samplers = [{"magFilter": 9729, "minFilter": 9987, "wrapS": 33071, "wrapT": 33071}]

    gltf_dict = {
        "asset": {"version": "2.0", "generator": "HaldorVeyGLBBuilderV2"},
        "scenes": [{"nodes": [0]}],
        "nodes": [{"mesh": 0, "name": "WatchMesh"}],
        "meshes": [{"name": spec['name'], "primitives": gltf_primitives}],
        "materials": materials,
        "textures": textures,
        "images": images,
        "samplers": samplers,
        "accessors": accessors,
        "bufferViews": buffer_views,
        "buffers": [{"byteLength": total_bin_length}]
    }

    json_str = json.dumps(gltf_dict, separators=(',', ':'))
    json_bytes = json_str.encode('utf-8')
    json_pad = (4 - (len(json_bytes) % 4)) % 4
    json_bytes += b' ' * json_pad

    total_glb_len = 12 + 8 + len(json_bytes) + 8 + len(bin_buffer)
    glb_bytes = bytearray()
    glb_bytes.extend(struct.pack('<3I', 0x46546C67, 2, total_glb_len))
    glb_bytes.extend(struct.pack('<2I', len(json_bytes), 0x4E4F534A))
    glb_bytes.extend(json_bytes)
    glb_bytes.extend(struct.pack('<2I', len(bin_buffer), 0x004E4942))
    glb_bytes.extend(bin_buffer)

    with open(filename, 'wb') as f:
        f.write(glb_bytes)
    print(f"Successfully generated {filename} ({len(glb_bytes)} bytes)")

MODEL_SPECS = [
    {
        'file': 'assets/models/serein-02.glb',
        'id': 'serein-02',
        'name': 'Serein No. 02',
        'case_color': [0.92, 0.94, 0.96, 1.0],
        'dial_type': 'silver',
        'marker_color': (45, 50, 55, 255),
        'dial_metallic': 0.45,
        'dial_roughness': 0.32,
        'strap_color': [0.28, 0.18, 0.14, 1.0],
        'hands_color': [0.20, 0.40, 0.75, 1.0],
        'accent_color': [0.20, 0.40, 0.75, 1.0]
    },
    {
        'file': 'assets/models/nacre-05.glb',
        'id': 'nacre-05',
        'name': 'Nacre No. 05',
        'case_color': [0.95, 0.80, 0.70, 1.0],
        'dial_type': 'pearl',
        'marker_color': (210, 160, 130, 255),
        'dial_metallic': 0.15,
        'dial_roughness': 0.28,
        'strap_color': [0.48, 0.22, 0.26, 1.0],
        'hands_color': [0.95, 0.78, 0.65, 1.0],
        'accent_color': [0.86, 0.48, 0.32, 1.0]
    },
    {
        'file': 'assets/models/orison-08.glb',
        'id': 'orison-08',
        'name': 'Orison No. 08',
        'case_color': [0.80, 0.82, 0.85, 1.0],
        'dial_type': 'slate',
        'marker_color': (220, 225, 230, 255),
        'dial_metallic': 0.35,
        'dial_roughness': 0.38,
        'strap_color': [0.25, 0.28, 0.31, 1.0],
        'hands_color': [0.92, 0.93, 0.95, 1.0],
        'accent_color': [0.88, 0.48, 0.28, 1.0]
    },
    {
        'file': 'assets/models/hedra-11.glb',
        'id': 'hedra-11',
        'name': 'Hedra No. 11',
        'case_color': [0.90, 0.92, 0.94, 1.0],
        'dial_type': 'umber',
        'marker_color': (235, 215, 185, 255),
        'dial_metallic': 0.28,
        'dial_roughness': 0.40,
        'strap_color': [0.55, 0.35, 0.22, 1.0],
        'hands_color': [0.94, 0.88, 0.80, 1.0],
        'accent_color': [0.86, 0.48, 0.32, 1.0],
        'pushers': True
    },
    {
        'file': 'assets/models/kestrel-14.glb',
        'id': 'kestrel-14',
        'name': 'Kestrel No. 14',
        'case_color': [0.72, 0.74, 0.76, 1.0],
        'case_finish': 'matte',
        'dial_type': 'sand',
        'marker_color': (32, 34, 30, 255),
        'dial_metallic': 0.05,
        'dial_roughness': 0.70,
        'strap_color': [0.45, 0.42, 0.32, 1.0],
        'hands_color': [0.18, 0.19, 0.16, 1.0],
        'accent_color': [0.75, 0.25, 0.20, 1.0]
    },
    {
        'file': 'assets/models/vanta-17.glb',
        'id': 'vanta-17',
        'name': 'Vanta No. 17',
        'case_color': [0.94, 0.95, 0.97, 1.0],
        'dial_type': 'black',
        'marker_color': (240, 242, 245, 255),
        'dial_metallic': 0.40,
        'dial_roughness': 0.18,
        'strap_color': [0.18, 0.18, 0.20, 1.0],
        'hands_color': [0.96, 0.97, 0.98, 1.0],
        'accent_color': [0.94, 0.78, 0.45, 1.0]
    }
]

for s in MODEL_SPECS:
    build_full_watch_glb(s)

print("All GLB models regenerated successfully!")
