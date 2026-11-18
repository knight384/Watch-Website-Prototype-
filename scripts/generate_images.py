import math
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

os.makedirs('assets', exist_ok=True)

def create_hero_plates():
    print("Generating hero-plate.jpg and poster.jpg...")
    # 2560 x 1440 hero plate
    w, h = 2560, 1440
    
    # Base dark plum palette: #1C1016 (28, 16, 22), #28171E (40, 23, 30), #12090E (18, 9, 14)
    # Plum cast near 70% x and 45% y
    img = Image.new('RGB', (w, h), (24, 14, 19))
    draw = ImageDraw.Draw(img)
    
    # Vertical gradient
    for y in range(h):
        factor = y / h
        # Top is slightly darker, middle has gentle warmth, bottom sinks to deep dark field
        r = int(22 * (1 - factor*0.4) + 12 * (1 - abs(factor - 0.45)))
        g = int(12 * (1 - factor*0.4) + 6 * (1 - abs(factor - 0.45)))
        b = int(16 * (1 - factor*0.4) + 9 * (1 - abs(factor - 0.45)))
        draw.line([(0, y), (w, y)], fill=(r, g, b))
        
    # Add plum cast radial warmth near 70% x (1792) and 45% y (648)
    spot_w, spot_h = 1600, 1200
    spot = Image.new('RGBA', (spot_w, spot_h), (0, 0, 0, 0))
    spot_draw = ImageDraw.Draw(spot)
    cx, cy = spot_w // 2, spot_h // 2
    max_r = min(cx, cy)
    for r in range(max_r, 0, -8):
        alpha = int(45 * (1 - (r / max_r) ** 1.8))
        # Warm plum/terracotta tone
        spot_draw.ellipse([cx - r, cy - int(r*0.75), cx + r, cy + int(r*0.75)], fill=(120, 52, 65, alpha))
        
    # Warm key highlight in the spot center
    for r in range(max_r // 2, 0, -6):
        alpha = int(35 * (1 - (r / (max_r // 2)) ** 1.5))
        spot_draw.ellipse([cx - r, cy - int(r*0.65), cx + r, cy + int(r*0.65)], fill=(214, 122, 79, alpha))
        
    spot = spot.filter(ImageFilter.GaussianBlur(60))
    img.paste(spot, (int(w * 0.70 - cx), int(h * 0.45 - cy)), spot)
    
    # Atelier studio horizon pedestal / soft reflection line around y = 0.78
    pedestal = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    pdraw = ImageDraw.Draw(pedestal)
    p_y = int(h * 0.76)
    pdraw.rectangle([0, p_y, w, h], fill=(16, 9, 13, 180))
    # Subtle studio horizon rim light
    pdraw.line([(0, p_y), (w, p_y)], fill=(180, 110, 115, 25), width=2)
    pedestal = pedestal.filter(ImageFilter.GaussianBlur(12))
    img.paste(pedestal, (0, 0), pedestal)
    
    # Architectural soft dark vignette
    vignette = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    vdraw = ImageDraw.Draw(vignette)
    for r in range(1200, 400, -20):
        # corners get darker
        pass
    
    # Save hero-plate.jpg
    img.save('assets/hero-plate.jpg', quality=94)
    print("Saved assets/hero-plate.jpg (2560x1440)")
    
    # Resize to 1600x900 for poster.jpg
    poster = img.resize((1600, 900), Image.Resampling.LANCZOS)
    poster.save('assets/poster.jpg', quality=92)
    print("Saved assets/poster.jpg (1600x900)")

create_hero_plates()

def draw_watch_image(spec):
    name = spec['id']
    filename = f"assets/watch-{name}.png"
    print(f"Generating {filename}...")
    
    W, H = 1200, 1400
    img = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    cx, cy = 600, 650
    case_radius = 290
    bezel_inner = 240
    dial_radius = 236
    
    # --- 1. Straps ---
    strap_w = 230
    strap_left = cx - strap_w // 2
    strap_right = cx + strap_w // 2
    
    # Upper strap (y: 80 to 420)
    # Lower strap (y: 880 to 1320)
    strap_color = spec['strap_color']
    stitch_color = spec['stitch_color']
    
    for y_range, direction in [((80, 420), 'up'), ((880, 1320), 'down')]:
        y1, y2 = y_range
        strap_layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
        sdraw = ImageDraw.Draw(strap_layer)
        
        # Base strap shape with slightly rounded end
        sdraw.rectangle([strap_left, y1, strap_right, y2], fill=strap_color)
        
        # Texture / leather shading
        for sy in range(y1, y2, 4):
            # Vertical gradient & side curvature shading
            progress = (sy - y1) / (y2 - y1)
            shade_factor = 0.85 + 0.3 * math.sin(progress * math.pi)
            for sx in range(strap_left, strap_right, 6):
                dist_center = abs(sx - cx) / (strap_w / 2)
                side_shade = 1.0 - (dist_center ** 2) * 0.4
                r = int(strap_color[0] * shade_factor * side_shade)
                g = int(strap_color[1] * shade_factor * side_shade)
                b = int(strap_color[2] * shade_factor * side_shade)
                sdraw.point((sx, sy), fill=(r, g, b, 255))
        
        # Stitching lines
        stitch_inset = 18
        stitch_x_left = strap_left + stitch_inset
        stitch_x_right = strap_right - stitch_inset
        for sy in range(y1 + 10, y2 - 10, 16):
            sdraw.line([(stitch_x_left, sy), (stitch_x_left, sy + 8)], fill=stitch_color, width=3)
            sdraw.line([(stitch_x_right, sy), (stitch_x_right, sy + 8)], fill=stitch_color, width=3)
            
        img.paste(strap_layer, (0, 0), strap_layer)

    # --- 2. Lugs & Case Dropshadow ---
    shadow = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    sh_draw = ImageDraw.Draw(shadow)
    sh_draw.ellipse([cx - case_radius - 20, cy - case_radius - 10, cx + case_radius + 20, cy + case_radius + 40], fill=(0, 0, 0, 160))
    shadow = shadow.filter(ImageFilter.GaussianBlur(28))
    img.paste(shadow, (0, 0), shadow)
    
    # 4 Lugs
    lug_metal = spec['case_metal']
    lug_pts_top_left = [(cx - 210, cy - 140), (cx - 190, cy - 360), (cx - 120, cy - 360), (cx - 140, cy - 140)]
    lug_pts_top_right = [(cx + 140, cy - 140), (cx + 120, cy - 360), (cx + 190, cy - 360), (cx + 210, cy - 140)]
    lug_pts_bot_left = [(cx - 210, cy + 140), (cx - 190, cy + 360), (cx - 120, cy + 360), (cx - 140, cy + 140)]
    lug_pts_bot_right = [(cx + 140, cy + 140), (cx + 120, cy + 360), (cx + 190, cy + 360), (cx + 210, cy + 140)]
    
    for pts in [lug_pts_top_left, lug_pts_top_right, lug_pts_bot_left, lug_pts_bot_right]:
        draw.polygon(pts, fill=lug_metal)
        # Bevel highlight
        draw.line([pts[1], pts[2]], fill=(255, 255, 255, 120), width=3)
        draw.line([pts[0], pts[1]], fill=(100, 100, 100, 100), width=2)
        
    # --- 3. Crown & Pushers ---
    crown_x = cx + case_radius - 10
    crown_y = cy
    crown_w = 48
    crown_h = 70
    draw.rounded_rectangle([crown_x, crown_y - crown_h//2, crown_x + crown_w, crown_y + crown_h//2], radius=6, fill=lug_metal)
    # Fluting
    for fy in range(crown_y - crown_h//2 + 6, crown_y + crown_h//2 - 6, 8):
        draw.line([(crown_x + 4, fy), (crown_x + crown_w - 4, fy)], fill=(40, 40, 40, 150), width=2)
        draw.line([(crown_x + 4, fy+1), (crown_x + crown_w - 4, fy+1)], fill=(255, 255, 255, 180), width=1)
        
    if spec.get('pushers'):
        # Hedra Chronograph pushers at 2 and 4 o'clock
        for angle in [-math.pi/5, math.pi/5]:
            px = cx + int((case_radius + 14) * math.cos(angle))
            py = cy + int((case_radius + 14) * math.sin(angle))
            pw, ph = 30, 22
            draw.rounded_rectangle([px - pw//2, py - ph//2, px + pw//2, py + ph//2], radius=4, fill=lug_metal)
            draw.ellipse([px - pw//2 + 4, py - ph//2 + 4, px + pw//2 - 4, py + ph//2 - 4], fill=(220, 220, 220, 255))

    # --- 4. Main Case & Bezel ---
    # Outer case ring
    for r in range(case_radius, bezel_inner, -1):
        ratio = (r - bezel_inner) / (case_radius - bezel_inner)
        # Metallic circular gradient
        base = lug_metal
        if spec.get('case_finish') == 'matte':
            # Bead blasted matte finish
            val = int(140 + 30 * ratio)
            c = (val, val, val, 255)
        else:
            # Polished stepped bevel
            val = int(base[0] * (0.7 + 0.45 * math.sin(ratio * math.pi)))
            val = min(255, max(0, val))
            c = (val, int(base[1] * val / base[0]), int(base[2] * val / base[0]), 255)
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=c, width=2)
        
    # Bezel inner polished lip
    draw.ellipse([cx - bezel_inner, cy - bezel_inner, cx + bezel_inner, cy + bezel_inner], outline=(255, 255, 255, 160), width=2)
    draw.ellipse([cx - dial_radius, cy - dial_radius, cx + dial_radius, cy + dial_radius], outline=(20, 20, 20, 200), width=3)

    # --- 5. Dial Face ---
    dial_img = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    ddraw = ImageDraw.Draw(dial_img)
    
    dial_type = spec['dial_type']
    if dial_type == 'pearl':
        # Nacre Mother-of-Pearl: soft iridescent cloud gradient
        ddraw.ellipse([cx - dial_radius, cy - dial_radius, cx + dial_radius, cy + dial_radius], fill=(245, 240, 236, 255))
        # Iridescent soft clouds
        for a, col in [(0.4, (240, 215, 225, 60)), (1.2, (220, 235, 240, 50)), (2.5, (250, 235, 215, 70)), (4.0, (230, 220, 240, 50))]:
            swirl_x = cx + int(80 * math.cos(a))
            swirl_y = cy + int(80 * math.sin(a))
            ddraw.ellipse([swirl_x - 120, swirl_y - 90, swirl_x + 120, swirl_y + 90], fill=col)
            
    elif dial_type == 'silver':
        # Serein Frost Silver
        ddraw.ellipse([cx - dial_radius, cy - dial_radius, cx + dial_radius, cy + dial_radius], fill=(228, 230, 232, 255))
        for r in range(dial_radius, 0, -4):
            factor = 0.94 + 0.12 * math.cos(r * 0.1)
            c = int(228 * factor)
            ddraw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(c, c, c+2, 255), width=2)
            
    elif dial_type == 'slate':
        # Orison Slate Grey
        ddraw.ellipse([cx - dial_radius, cy - dial_radius, cx + dial_radius, cy + dial_radius], fill=(48, 54, 58, 255))
        # Sunburst grain
        for i in range(180):
            ang = i * (math.pi / 90)
            ex = cx + int(dial_radius * math.cos(ang))
            ey = cy + int(dial_radius * math.sin(ang))
            shade = 45 + int(20 * (math.sin(ang * 4) ** 2))
            ddraw.line([(cx, cy), (ex, ey)], fill=(shade, shade+4, shade+8, 120), width=2)
        # Inner 24-hr GMT track ring
        gmt_r = int(dial_radius * 0.68)
        ddraw.ellipse([cx - gmt_r, cy - gmt_r, cx + gmt_r, cy + gmt_r], outline=(30, 35, 38, 255), width=22)
        for h_24 in range(24):
            ang = -math.pi/2 + h_24 * (math.pi / 12)
            hx = cx + int(gmt_r * math.cos(ang))
            hy = cy + int(gmt_r * math.sin(ang))
            ddraw.ellipse([hx-2, hy-2, hx+2, hy+2], fill=(214, 122, 79, 255) if h_24 % 6 == 0 else (160, 165, 170, 200))
            
    elif dial_type == 'umber':
        # Hedra Umber
        ddraw.ellipse([cx - dial_radius, cy - dial_radius, cx + dial_radius, cy + dial_radius], fill=(62, 42, 34, 255))
        # Concentric warm grain
        for r in range(dial_radius, 0, -3):
            factor = 0.92 + 0.14 * (math.sin(r * 0.15) ** 2)
            c_r = int(66 * factor)
            c_g = int(45 * factor)
            c_b = int(36 * factor)
            ddraw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(c_r, c_g, c_b, 255), width=2)
        # Dual subdials at 3 and 9 o'clock
        for sub_x in [cx - 95, cx + 95]:
            sub_r = 52
            ddraw.ellipse([sub_x - sub_r, sub_y := cy, sub_x + sub_r, sub_y + sub_r], fill=(48, 32, 26, 255))
            for sr in range(sub_r, 0, -4):
                ddraw.ellipse([sub_x - sr, cy - sr, sub_x + sr, cy + sr], outline=(80, 56, 44, 200), width=1)
            # subdial hand
            ddraw.line([(sub_x, cy), (sub_x + 22, cy - 14)], fill=(220, 200, 180, 255), width=2)
            
    elif dial_type == 'sand':
        # Kestrel Sand (Field)
        ddraw.ellipse([cx - dial_radius, cy - dial_radius, cx + dial_radius, cy + dial_radius], fill=(218, 205, 182, 255))
        # Fine matte stipple
        for r in range(dial_radius, 0, -5):
            ddraw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(208, 195, 172, 180), width=2)
            
    elif dial_type == 'black':
        # Vanta Black Lacquer
        ddraw.ellipse([cx - dial_radius, cy - dial_radius, cx + dial_radius, cy + dial_radius], fill=(12, 11, 14, 255))
        # Moonphase aperture at 6 o'clock (cy + 90)
        mp_cx, mp_cy = cx, cy + 90
        mp_w, mp_h = 75, 45
        ddraw.ellipse([mp_cx - mp_w, mp_cy - mp_h, mp_cx + mp_w, mp_cy + mp_h], fill=(10, 16, 32, 255), outline=(180, 150, 90, 200), width=2)
        # Golden moon
        ddraw.ellipse([mp_cx - 16, mp_cy - 16, mp_cx + 16, mp_cy + 16], fill=(235, 195, 105, 255))
        # Stars
        for sx, sy in [(mp_cx - 35, mp_cy - 10), (mp_cx + 38, mp_cy - 8), (mp_cx - 18, mp_cy + 12), (mp_cx + 25, mp_cy + 14)]:
            ddraw.ellipse([sx-1, sy-1, sx+1, sy+1], fill=(255, 240, 200, 255))
        # Date window at 3 o'clock
        dw_x, dw_y = cx + 115, cy
        ddraw.rectangle([dw_x - 16, dw_y - 12, dw_x + 16, dw_y + 12], fill=(245, 242, 238, 255), outline=(160, 140, 100, 255), width=2)
        ddraw.text((dw_x - 8, dw_y - 8), "17", fill=(20, 20, 20, 255))

    # Open balance wheel for Serein (at 6 o'clock)
    if spec['id'] == 'serein-02':
        bal_x, bal_y = cx, cy + 95
        bal_r = 54
        ddraw.ellipse([bal_x - bal_r, bal_y - bal_r, bal_x + bal_r, bal_y + bal_r], fill=(30, 32, 36, 255), outline=(140, 145, 150, 255), width=3)
        # Golden balance wheel rim
        ddraw.ellipse([bal_x - 42, bal_y - 42, bal_x + 42, bal_y + 42], outline=(225, 185, 95, 255), width=4)
        # Screws on balance rim
        for sa in range(0, 360, 45):
            s_rad = sa * math.pi / 180
            sc_x = bal_x + int(42 * math.cos(s_rad))
            sc_y = bal_y + int(42 * math.sin(s_rad))
            ddraw.ellipse([sc_x-2, sc_y-2, sc_x+2, sc_y+2], fill=(245, 215, 130, 255))
        # Steel bridge across
        ddraw.line([(bal_x - 52, bal_y), (bal_x + 52, bal_y)], fill=(200, 205, 210, 255), width=6)
        # Ruby jewel in center
        ddraw.ellipse([bal_x - 6, bal_y - 6, bal_x + 6, bal_y + 6], fill=(195, 30, 60, 255), outline=(225, 185, 95, 255), width=2)
        
    # Open movement aperture for Nacre (at 6 o'clock)
    if spec['id'] == 'nacre-05':
        bal_x, bal_y = cx, cy + 90
        bal_r = 46
        ddraw.ellipse([bal_x - bal_r, bal_y - bal_r, bal_x + bal_r, bal_y + bal_r], fill=(35, 25, 28, 255), outline=(210, 160, 120, 255), width=3)
        # Golden balance wheel
        ddraw.ellipse([bal_x - 34, bal_y - 34, bal_x + 34, bal_y + 34], outline=(230, 190, 110, 255), width=3)
        # Rose gold skeleton bridge
        ddraw.line([(bal_x - 44, bal_y), (bal_x + 44, bal_y)], fill=(215, 165, 130, 255), width=5)
        ddraw.ellipse([bal_x - 5, bal_y - 5, bal_x + 5, bal_y + 5], fill=(205, 40, 75, 255), outline=(230, 190, 110, 255), width=2)

    # Dial Chapter Ring & Markers
    index_col = spec['marker_color']
    for hour in range(12):
        angle = hour * (math.pi / 6) - math.pi / 2
        # Outer tick
        r_out = dial_radius - 12
        r_in = dial_radius - 38 if hour % 3 == 0 else dial_radius - 28
        
        x_out = cx + int(r_out * math.cos(angle))
        y_out = cy + int(r_out * math.sin(angle))
        x_in = cx + int(r_in * math.cos(angle))
        y_in = cy + int(r_in * math.sin(angle))
        
        # Faceted 3D index marker
        thick = 6 if hour % 3 == 0 else 4
        ddraw.line([(x_in, y_in), (x_out, y_out)], fill=index_col, width=thick)
        # Specular glint on index
        ddraw.line([(x_in, y_in), (x_in + int((x_out-x_in)*0.5), y_in + int((y_out-y_in)*0.5))], fill=(255, 255, 255, 180), width=thick-2)
        
    # Minute track dots/ticks
    for m in range(60):
        if m % 5 != 0:
            angle = m * (math.pi / 30) - math.pi / 2
            r_out = dial_radius - 12
            r_in = dial_radius - 20
            ddraw.line([(cx + int(r_out * math.cos(angle)), cy + int(r_out * math.sin(angle))),
                        (cx + int(r_in * math.cos(angle)), cy + int(r_in * math.sin(angle)))],
                       fill=(index_col[0], index_col[1], index_col[2], 120), width=2)
                       
    # Brand inscription at 12 o'clock
    # "HALDOR & VEY"
    # "GENÈVE"
    text_y = cy - 105
    brand_col = (index_col[0], index_col[1], index_col[2], 230)
    # Draw simple clean lettering representation
    ddraw.line([(cx - 45, text_y), (cx + 45, text_y)], fill=brand_col, width=2)
    ddraw.line([(cx - 25, text_y + 12), (cx + 25, text_y + 12)], fill=(index_col[0], index_col[1], index_col[2], 150), width=1)

    # --- 6. Hands ---
    hand_col = spec['hand_color']
    
    # Hour hand (pointing towards 10:10 / angle ~ -2.0 rad)
    h_angle = -2.15
    h_len = int(dial_radius * 0.52)
    hx = cx + int(h_len * math.cos(h_angle))
    hy = cy + int(h_len * math.sin(h_angle))
    ddraw.line([(cx, cy), (hx, hy)], fill=hand_col, width=8)
    ddraw.line([(cx, cy), (hx, hy)], fill=(255, 255, 255, 160), width=3) # reflection
    
    # Minute hand (pointing towards ~ 1:52 / angle ~ -0.45 rad)
    m_angle = -0.45
    m_len = int(dial_radius * 0.78)
    mx = cx + int(m_len * math.cos(m_angle))
    my = cy + int(m_len * math.sin(m_angle))
    ddraw.line([(cx, cy), (mx, my)], fill=hand_col, width=6)
    ddraw.line([(cx, cy), (mx, my)], fill=(255, 255, 255, 160), width=2)
    
    # GMT hand if Orison
    if spec['id'] == 'orison-08':
        gmt_ang = 1.35
        gmt_len = int(dial_radius * 0.68)
        gx = cx + int(gmt_len * math.cos(gmt_ang))
        gy = cy + int(gmt_len * math.sin(gmt_ang))
        ddraw.line([(cx, cy), (gx, gy)], fill=(214, 122, 79, 255), width=3)
        # GMT arrow head
        ddraw.polygon([(gx, gy), (gx - 10, gy - 8), (gx - 12, gy + 8)], fill=(214, 122, 79, 255))

    # Second hand (sweeping thin needle)
    s_angle = 1.85
    s_len = int(dial_radius * 0.84)
    s_col = spec.get('sec_color', (214, 122, 79, 255))
    sx = cx + int(s_len * math.cos(s_angle))
    sy = cy + int(s_len * math.sin(s_angle))
    s_tail_x = cx - int(40 * math.cos(s_angle))
    s_tail_y = cy - int(40 * math.sin(s_angle))
    ddraw.line([(s_tail_x, s_tail_y), (sx, sy)], fill=s_col, width=2)
    
    # Center pinion cap
    ddraw.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], fill=hand_col, outline=(40, 40, 40, 200), width=2)
    ddraw.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], fill=(255, 255, 255, 255))
    
    # Merge dial
    img.paste(dial_img, (0, 0), dial_img)
    
    # --- 7. Sapphire Crystal Reflection & Glint ---
    glass = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    gdraw = ImageDraw.Draw(glass)
    # Curved soft white/cyan reflection arc across top-left
    for r in range(dial_radius - 8, dial_radius - 40, -1):
        gdraw.arc([cx - r, cy - r, cx + r, cy + r], start=190, end=300, fill=(255, 255, 255, 22), width=3)
    # Anti-reflective subtle purple-blue hue
    for r in range(dial_radius - 20, dial_radius - 70, -2):
        gdraw.arc([cx - r, cy - r, cx + r, cy + r], start=210, end=270, fill=(160, 180, 240, 16), width=2)
    # Pinpoint specular highlight at 10 o'clock on bezel
    glint_x = cx - int(bezel_inner * 0.72)
    glint_y = cy - int(bezel_inner * 0.72)
    gdraw.ellipse([glint_x - 14, glint_y - 14, glint_x + 14, glint_y + 14], fill=(255, 255, 255, 140))
    glass = glass.filter(ImageFilter.GaussianBlur(3))
    img.paste(glass, (0, 0), glass)
    
    img.save(filename, 'PNG')
    print(f"Saved {filename}")

# Watch specifications matching the prompt
WATCH_SPECS = [
    {
        'id': 'serein-02',
        'strap_color': (42, 28, 22, 255),
        'stitch_color': (85, 60, 48, 220),
        'case_metal': (218, 222, 226, 255),
        'dial_type': 'silver',
        'marker_color': (45, 50, 55, 255),
        'hand_color': (35, 65, 115, 255), # blued steel
        'sec_color': (35, 65, 115, 255),
    },
    {
        'id': 'nacre-05',
        'strap_color': (88, 38, 48, 255), # burgundy taupe
        'stitch_color': (210, 185, 175, 220),
        'case_metal': (235, 195, 170, 255), # rose gold
        'dial_type': 'pearl',
        'marker_color': (210, 160, 130, 255),
        'hand_color': (215, 165, 135, 255),
        'sec_color': (214, 122, 79, 255),
    },
    {
        'id': 'orison-08',
        'strap_color': (36, 40, 44, 255), # anthracite slate
        'stitch_color': (214, 122, 79, 220), # orange accent stitch
        'case_metal': (190, 195, 200, 255),
        'dial_type': 'slate',
        'marker_color': (220, 225, 230, 255),
        'hand_color': (230, 232, 235, 255),
        'sec_color': (214, 122, 79, 255),
    },
    {
        'id': 'hedra-11',
        'strap_color': (110, 68, 42, 255), # amber saddle leather
        'stitch_color': (195, 155, 115, 220),
        'case_metal': (215, 218, 222, 255),
        'dial_type': 'umber',
        'marker_color': (235, 215, 185, 255),
        'hand_color': (235, 220, 195, 255),
        'sec_color': (214, 122, 79, 255),
        'pushers': True,
    },
    {
        'id': 'kestrel-14',
        'strap_color': (98, 92, 74, 255), # olive canvas
        'stitch_color': (165, 160, 135, 220),
        'case_metal': (155, 160, 165, 255),
        'case_finish': 'matte',
        'dial_type': 'sand',
        'marker_color': (30, 32, 28, 255),
        'hand_color': (25, 28, 24, 255),
        'sec_color': (180, 50, 40, 255),
    },
    {
        'id': 'vanta-17',
        'strap_color': (18, 18, 20, 255), # glossy black
        'stitch_color': (60, 60, 65, 220),
        'case_metal': (225, 228, 232, 255), # platinum mirror
        'dial_type': 'black',
        'marker_color': (240, 242, 245, 255),
        'hand_color': (245, 248, 250, 255),
        'sec_color': (215, 175, 95, 255), # gold
    }
]

for s in WATCH_SPECS:
    draw_watch_image(s)

print("All watch PNGs generated successfully.")
