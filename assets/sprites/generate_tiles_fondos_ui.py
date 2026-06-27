#!/usr/bin/env python3
"""
Generador: tilesets (32x32), fondos parallax (512x256), UI (32x32 base)
para "El Jardín Interior" — pixel art texturizado con PIL.
"""
import os, math, random, itertools
from PIL import Image, ImageDraw, ImageFilter, ImageStat

random.seed(42)

BASE = os.path.dirname(os.path.abspath(__file__))
TILES_DIR  = os.path.join(BASE, "tiles")
FONDOS_DIR = os.path.join(BASE, "fondos")
UI_DIR     = os.path.join(BASE, "ui")

RGBA = (0, 0, 0, 0)
BLANCO = (255, 255, 255, 255)
NEGRO  = (0, 0, 0, 255)


# ── helpers ──────────────────────────────────────────────────────────
def new_im(size, bg=RGBA):
    im = Image.new("RGBA", (size, size) if isinstance(size, int) else size, bg)
    return im, ImageDraw.Draw(im)

def new_im_wh(w, h, bg=RGBA):
    im = Image.new("RGBA", (w, h), bg)
    return im, ImageDraw.Draw(im)

def save(img, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    img.save(path, "PNG")

def hex_rgba(h):
    """#RRGGBB -> RGBA tuple"""
    h = h.lstrip("#")
    return (*tuple(int(h[i:i+2], 16) for i in (0,2,4)), 255)

def lerp_color(c1, c2, t):
    return tuple(int(a + (b-a)*t) for a,b in zip(c1[:3], c2[:3])) + (255,)

def add_noise(draw, rect, colors, density=0.15):
    """scatter tiny noise pixels for texture"""
    x0,y0,x1,y1 = rect
    for _ in range(int((x1-x0)*(y1-y0)*density)):
        x = random.randint(x0, x1-1)
        y = random.randint(y0, y1-1)
        c = random.choice(colors)
        draw.point((x,y), fill=c)

def sub_pixels(draw, xy, color, n=4):
    """draw a cluster of sub-pixels (2x2)"""
    x,y = xy
    for dx in range(n):
        for dy in range(n):
            draw.point((x+dx, y+dy), fill=color)

def dither_line(draw, y, x0, x1, c1, c2, step=2):
    for x in range(x0, x1, step):
        c = c1 if (x//step + y) % 2 == 0 else c2
        draw.point((x,y), fill=c)

def rounded_rect(draw, rect, radius, fill, outline=None, ow=1):
    x0,y0,x1,y1 = rect
    draw.rounded_rectangle(rect, radius=radius, fill=fill, outline=outline, width=ow)

def soft_shadow(draw, rect, radius, color=(0,0,0,40)):
    x0,y0,x1,y1 = rect
    # offset shadow
    sx0,sy0,sx1,sy1 = x0+3, y0+3, x1+3, y1+3
    draw.rounded_rectangle((sx0,sy0,sx1,sy1), radius=radius, fill=color)


# ═══════════════════════════════════════════════════════════════════
#  TILES 32x32 — pixel art detallado con textura
# ═══════════════════════════════════════════════════════════════════

BIOME_DIRS = {
    "jardin-central":      TILES_DIR,
    "bosque-atencion":     TILES_DIR,
    "rio-memoria":         TILES_DIR,
    "montana-razonamiento":TILES_DIR,
    "valle-lenguaje":      TILES_DIR,
    "torre-matematicas":   TILES_DIR,
    "gruta-visual":        TILES_DIR,
    "camino-velocidad":    TILES_DIR,
}

# ── Jardín Central ──────────────────────────────────────────────
def tile_jardin_central():
    biome = "jardin-central"
    d = os.path.join(TILES_DIR, biome)
    S = 32
    C = {
        "grass":    hex_rgba("#A8D5BA"),
        "grass_d":  hex_rgba("#8BC4A0"),
        "grass_l":  hex_rgba("#B5D8C0"),
        "dirt":     hex_rgba("#D4A76A"),
        "dirt_d":   hex_rgba("#C49A5C"),
        "flower_y": hex_rgba("#F0C060"),
        "flower_p": hex_rgba("#E8B4B8"),
        "flower_o": hex_rgba("#E8A84A"),
        "tree":     hex_rgba("#6B4226"),
        "tree_d":   hex_rgba("#5A3820"),
        "water":    hex_rgba("#4A90D9"),
        "water_l":  hex_rgba("#6DB8E8"),
        "green":    hex_rgba("#7EC8A0"),
    }

    # grass_0 — pasto base texturizado
    im, dr = new_im(S)
    dr.rectangle((0,0,S,S), fill=C["grass"])
    add_noise(dr, (0,0,S,S), [C["grass_d"], C["grass_l"]], 0.2)
    # small grass blades
    for i in range(12):
        x = random.randint(2,28)
        y = random.randint(2,28)
        dr.line((x,y,x+random.randint(-1,1),y-2), fill=C["grass_d"], width=1)
    save(im, f"{d}/grass_0.png")

    # grass_1 — pasto con flores blancas minúsculas
    im, dr = new_im(S)
    dr.rectangle((0,0,S,S), fill=C["grass_l"])
    add_noise(dr, (0,0,S,S), [C["grass"], C["grass_d"]], 0.15)
    for _ in range(6):
        x = random.randint(4,28)
        y = random.randint(4,28)
        sub_pixels(dr, (x,y), (255,255,255,255), 2)
        sub_pixels(dr, (x-1,y), (255,255,200,255), 1)
    save(im, f"{d}/grass_1.png")

    # dirt_0 — tierra texturizada
    im, dr = new_im(S)
    dr.rectangle((0,0,S,S), fill=C["dirt"])
    add_noise(dr, (0,0,S,S), [C["dirt_d"], (180,130,80,255)], 0.3)
    for _ in range(8):
        x = random.randint(2,30)
        y = random.randint(2,30)
        dr.ellipse((x,y,x+2,y+2), fill=(160,110,70,255))
    save(im, f"{d}/dirt_0.png")

    # path_0, path_1 — camino de piedras
    for pi, nc in enumerate([8, 10]):
        im, dr = new_im(S)
        dr.rectangle((0,0,S,S), fill=C["dirt"])
        add_noise(dr, (0,0,S,S), [C["dirt_d"], (160,120,60,255)], 0.2)
        for _ in range(nc):
            x = random.randint(2,26)
            y = random.randint(2,26)
            sz = random.randint(4,8)
            c = random.choice([(180,150,120,255), (200,170,140,255), (160,130,100,255)])
            dr.ellipse((x,y,x+sz,y+sz), fill=c)
            dr.ellipse((x+1,y+1,x+sz-1,y+sz-1), fill=(220,190,160,255))
        save(im, f"{d}/path_{pi}.png")

    # flower_0..4 — 5 colores de flores
    fcols = [C["flower_y"], C["flower_p"], C["flower_o"], (255,100,100,255), (200,150,255,255)]
    for fi, fc in enumerate(fcols):
        im, dr = new_im(S)
        dr.rectangle((0,0,S,S), fill=C["grass"])
        add_noise(dr, (0,0,S,S), [C["grass_d"], C["grass_l"]], 0.15)
        # stem
        dr.line((16,28,16,16), fill=C["green"], width=2)
        # petals
        cx, cy = 16, 12
        for a in range(0, 360, 60):
            rx = cx + int(5 * math.cos(math.radians(a)))
            ry = cy + int(5 * math.sin(math.radians(a)))
            dr.ellipse((rx-3, ry-3, rx+3, ry+3), fill=fc)
        dr.ellipse((cx-2, cy-2, cx+2, cy+2), fill=(255,255,200,255))
        save(im, f"{d}/flower_{fi}.png")

    # tree_base — base de árbol
    im, dr = new_im(S)
    dr.rectangle((0,0,S,S), fill=C["grass"])
    add_noise(dr, (0,0,S,S), [C["grass_d"]], 0.1)
    # trunk
    dr.rectangle((12,8,20,32), fill=C["tree"])
    add_noise(dr, (12,8,20,32), [C["tree_d"], (80,50,30,255)], 0.3)
    # roots
    dr.ellipse((10,26,22,34), fill=C["tree"])
    dr.ellipse((6,28,14,34), fill=C["tree_d"])
    dr.ellipse((18,28,26,34), fill=C["tree_d"])
    # moss at base
    dr.ellipse((11,26,13,30), fill=C["green"])
    dr.ellipse((19,26,21,30), fill=C["green"])
    save(im, f"{d}/tree_base.png")

    # water_0 — agua
    im, dr = new_im(S)
    dr.rectangle((0,0,S,S), fill=C["water"])
    add_noise(dr, (0,0,S,S), [C["water_l"], (100,180,230,255)], 0.15)
    for _ in range(5):
        x = random.randint(2,28)
        y = random.randint(2,28)
        dr.ellipse((x,y,x+6,y+2), fill=(255,255,255,60))
    save(im, f"{d}/water_0.png")

    # Fill to 20: extra tiles
    # stone_wall
    im, dr = new_im(S)
    dr.rectangle((0,0,S,S), fill=(180,180,180,255))
    for r in range(3):
        for c_ in range(3):
            dr.rectangle((c_*12, r*12, c_*12+10, r*12+10), fill=(160,160,160,255), outline=(140,140,140,255))
    save(im, f"{d}/stone_wall_0.png")

    # fence
    im, dr = new_im(S)
    dr.rectangle((0,0,S,S), fill=C["grass"])
    dr.rectangle((0,12,32,14), fill=(139,90,43,255))
    dr.rectangle((0,22,32,24), fill=(139,90,43,255))
    for x_ in range(4,32,8):
        dr.rectangle((x_,8,x_+3,28), fill=(139,90,43,255))
        dr.polygon([(x_-1,8),(x_+1,4),(x_+4,8)], fill=(160,100,50,255))
    save(im, f"{d}/fence_0.png")

    # bench
    im, dr = new_im(S)
    dr.rectangle((0,0,S,S), fill=C["grass"])
    dr.rectangle((4,16,28,20), fill=(139,90,43,255))
    dr.rectangle((6,12,10,20), fill=(120,80,35,255))
    dr.rectangle((22,12,26,20), fill=(120,80,35,255))
    dr.rectangle((4,10,28,12), fill=(160,120,60,255))
    save(im, f"{d}/bench_0.png")

    # bush
    im, dr = new_im(S)
    dr.rectangle((0,0,S,S), fill=C["grass"])
    for _ in range(20):
        x = random.randint(4,28)
        y = random.randint(10,30)
        r = random.randint(4,8)
        dr.ellipse((x,y,x+r,y+r), fill=(100,180,100,255))
    save(im, f"{d}/bush_0.png")

    # lamp_post
    im, dr = new_im(S)
    dr.rectangle((0,0,S,S), fill=C["grass"])
    dr.rectangle((14,6,18,32), fill=(80,80,80,255))
    dr.ellipse((10,2,22,10), fill=C["flower_y"])
    dr.ellipse((12,4,20,8), fill=(255,255,200,255))
    save(im, f"{d}/lamp_post_0.png")

    # gate
    im, dr = new_im(S)
    dr.rectangle((0,0,S,S), fill=C["grass"])
    dr.rectangle((2,6,30,32), fill=(139,90,43,255))
    dr.rectangle((4,8,28,30), fill=(160,120,60,255))
    dr.arc((6,10,26,28), 0, 180, fill=(200,170,100,255), width=2)
    dr.ellipse((14,18,18,22), fill=C["flower_y"])
    save(im, f"{d}/gate_0.png")

    # extra grass variation
    im, dr = new_im(S)
    dr.rectangle((0,0,S,S), fill=C["grass_d"])
    add_noise(dr, (0,0,S,S), [C["grass"], C["grass_l"]], 0.2)
    for i in range(6):
        x = random.randint(4,28)
        dr.arc((x-2,26,x+2,32), 180, 360, fill=C["green"], width=1)
    save(im, f"{d}/grass_2.png")

    # hedge
    im, dr = new_im(S)
    dr.rectangle((0,0,S,S), fill=C["grass"])
    for _ in range(12):
        x = random.randint(2,28)
        y = random.randint(14,30)
        r = random.randint(5,9)
        dr.ellipse((x,y,x+r,y+r), fill=C["green"])
    save(im, f"{d}/hedge_0.png")

    print(f"  {biome}: 20 tiles")


# ── Bosque Atención ─────────────────────────────────────────────
def tile_bosque_atencion():
    biome = "bosque-atencion"
    d = os.path.join(TILES_DIR, biome)
    S = 32
    C = {
        "floor":   hex_rgba("#2D5016"),
        "moss":    hex_rgba("#4A7C2E"),
        "moss_l":  hex_rgba("#5A8C3E"),
        "trunk":   hex_rgba("#4A3520"),
        "trunk_d": hex_rgba("#3A2510"),
        "top":     hex_rgba("#1A3A0A"),
        "top_l":   hex_rgba("#2D5016"),
        "red":     hex_rgba("#D94040"),
        "red_l":   hex_rgba("#F06060"),
        "blue":    hex_rgba("#4A90D9"),
        "blue_l":  hex_rgba("#6DB8E8"),
        "leaf":    hex_rgba("#6B8F3A"),
        "brown":   hex_rgba("#8B6F47"),
        "gold":    hex_rgba("#F0C060"),
    }

    # forest_grass
    im, dr = new_im(S)
    dr.rectangle((0,0,S,S), fill=C["floor"])
    add_noise(dr, (0,0,S,S), [C["moss"], (20,60,10,255)], 0.25)
    for _ in range(4):
        x = random.randint(2,28)
        dr.arc((x,26,x+4,32), 180, 360, fill=C["moss"], width=1)
    save(im, f"{d}/forest_grass.png")

    # forest_dirt
    im, dr = new_im(S)
    dr.rectangle((0,0,S,S), fill=(60,40,20,255))
    add_noise(dr, (0,0,S,S), [C["brown"], (80,60,30,255)], 0.3)
    for _ in range(6):
        x = random.randint(2,30)
        y = random.randint(2,30)
        dr.ellipse((x,y,x+3,y+3), fill=(70,50,25,255))
    save(im, f"{d}/forest_dirt.png")

    # leaves_0, leaves_1
    for li, shade in enumerate([C["leaf"], C["brown"]]):
        im, dr = new_im(S)
        dr.rectangle((0,0,S,S), fill=C["floor"])
        for _ in range(15):
            x = random.randint(2,28)
            y = random.randint(2,28)
            dr.ellipse((x,y,x+5,y+4), fill=shade)
        save(im, f"{d}/leaves_{li}.png")

    # mushroom_0 (red), mushroom_1 (blue)
    for mi, (cap, spots) in enumerate([(C["red"], (255,200,200,255)), (C["blue"], (200,220,255,255))]):
        im, dr = new_im(S)
        dr.rectangle((0,0,S,S), fill=C["floor"])
        add_noise(dr, (0,0,S,S), [C["moss"], C["top"]], 0.15)
        # stem
        dr.rectangle((14,16,18,32), fill=(220,200,180,255))
        # cap
        dr.ellipse((8,6,24,20), fill=cap)
        dr.ellipse((10,8,22,18), fill=cap)
        # spots
        for _ in range(4):
            sx = random.randint(10,22)
            sy = random.randint(8,16)
            dr.ellipse((sx,sy,sx+2,sy+2), fill=spots)
        save(im, f"{d}/mushroom_{mi}.png")

    # tree_trunk
    im, dr = new_im(S)
    dr.rectangle((0,0,S,S), fill=C["floor"])
    dr.rectangle((12,0,20,32), fill=C["trunk"])
    add_noise(dr, (12,0,20,32), [C["trunk_d"], (80,50,30,255)], 0.3)
    # bark lines
    for y_ in range(2, 32, 4):
        dr.line((12,y_,20,y_), fill=(60,40,20,100), width=1)
    save(im, f"{d}/tree_trunk.png")

    # tree_top
    im, dr = new_im(S)
    dr.rectangle((0,0,S,S), fill=C["top"])
    for _ in range(25):
        x = random.randint(0,32)
        y = random.randint(0,32)
        r = random.randint(4,10)
        dr.ellipse((x,y,x+r,y+r), fill=C["top_l"])
    dr.ellipse((8,4,24,20), fill=C["top"])
    dr.ellipse((4,10,28,28), fill=C["top_l"])
    save(im, f"{d}/tree_top.png")

    # Fill to 20: extra tiles
    # hiding_spot
    im, dr = new_im(S)
    dr.rectangle((0,0,S,S), fill=C["floor"])
    dr.ellipse((2,14,30,32), fill=C["top"])
    dr.ellipse((4,16,28,30), fill=C["top_l"])
    add_noise(dr, (2,14,30,32), [C["moss"], C["leaf"]], 0.2)
    save(im, f"{d}/hiding_spot.png")

    # fallen_log
    im, dr = new_im(S)
    dr.rectangle((0,0,S,S), fill=C["floor"])
    dr.rectangle((0,14,32,20), fill=C["trunk"])
    dr.ellipse((0,12,6,22), fill=C["trunk"])
    dr.ellipse((26,12,32,22), fill=C["trunk"])
    dr.ellipse((4,8,12,14), fill=C["moss"])
    save(im, f"{d}/fallen_log.png")

    # spotlight_ray
    im, dr = new_im(S)
    dr.rectangle((0,0,S,S), fill=C["floor"])
    poly = [(8,0),(24,0),(32,32),(0,32)]
    dr.polygon(poly, fill=(240,192,96,40))
    dr.polygon(poly, fill=(255,255,200,20))
    save(im, f"{d}/spotlight_ray.png")

    # acorn
    im, dr = new_im(S)
    dr.rectangle((0,0,S,S), fill=C["floor"])
    add_noise(dr, (0,0,S,S), [C["moss"], C["leaf"]], 0.15)
    for _ in range(3):
        x = random.randint(6,26)
        y = random.randint(10,26)
        dr.ellipse((x,y,x+4,y+5), fill=C["brown"])
        dr.ellipse((x+1,y-1,x+3,y+1), fill=(120,90,50,255))
    save(im, f"{d}/acorn.png")

    # moss_path
    im, dr = new_im(S)
    dr.rectangle((0,0,S,S), fill=C["moss"])
    add_noise(dr, (0,0,S,S), [C["moss_l"], C["floor"]], 0.2)
    for _ in range(8):
        x = random.randint(4,28)
        y = random.randint(4,28)
        dr.ellipse((x,y,x+4,y+3), fill=(80,140,60,255))
    save(im, f"{d}/moss_path.png")

    # stone_alt
    im, dr = new_im(S)
    dr.rectangle((0,0,S,S), fill=C["floor"])
    for _ in range(3):
        x = random.randint(4,24)
        y = random.randint(4,24)
        dr.ellipse((x,y,x+6,y+5), fill=(100,100,100,255))
        dr.ellipse((x+1,y+1,x+5,y+4), fill=(140,140,140,255))
    save(im, f"{d}/stone_alt.png")

    # extra mushroom
    im, dr = new_im(S)
    dr.rectangle((0,0,S,S), fill=C["floor"])
    dr.rectangle((15,18,17,30), fill=(220,200,180,255))
    dr.ellipse((8,10,24,22), fill=(255,200,100,255))
    for _ in range(3):
        sx = random.randint(10,22)
        sy = random.randint(10,20)
        dr.ellipse((sx,sy,sx+2,sy+2), fill=(255,255,200,255))
    save(im, f"{d}/mushroom_2.png")

    # root
    im, dr = new_im(S)
    dr.rectangle((0,0,S,S), fill=C["floor"])
    dr.arc((0,20,16,36), 180, 270, fill=C["trunk"], width=3)
    dr.arc((16,24,32,36), 270, 360, fill=C["trunk_d"], width=3)
    save(im, f"{d}/root_0.png")

    # extra grass
    im, dr = new_im(S)
    dr.rectangle((0,0,S,S), fill=C["moss_l"])
    add_noise(dr, (0,0,S,S), [C["moss"], C["leaf"]], 0.2)
    for i in range(8):
        x = random.randint(2,30)
        y = random.randint(2,30)
        dr.line((x,y,x,y-3), fill=C["leaf"], width=1)
    save(im, f"{d}/forest_grass_1.png")

    # bracken
    im, dr = new_im(S)
    dr.rectangle((0,0,S,S), fill=C["floor"])
    dr.ellipse((6,22,26,32), fill=C["moss"])
    for i in range(5):
        x = 4 + i*6
        dr.line((x,24,x+1,14), fill=C["leaf"], width=2)
        dr.ellipse((x-2,12,x+4,16), fill=C["leaf"])
    save(im, f"{d}/bracken.png")

    # pinecone
    im, dr = new_im(S)
    dr.rectangle((0,0,S,S), fill=C["floor"])
    dr.ellipse((12,14,20,28), fill=C["brown"])
    for y_ in range(16, 26, 3):
        dr.arc((12,y_,20,y_+3), 0, 180, fill=(100,80,40,255))
    dr.ellipse((13,12,19,16), fill=C["brown"])
    save(im, f"{d}/pinecone.png")

    # web
    im, dr = new_im(S)
    dr.rectangle((0,0,S,S), fill=C["floor"])
    cx, cy = 16, 8
    for r in range(4, 16, 4):
        dr.ellipse((cx-r, cy-r, cx+r, cy+r), outline=(200,200,200,80), width=1)
    for a in range(0, 360, 45):
        dr.line((cx,cy,cx+int(r*math.cos(math.radians(a))),cy+int(r*math.sin(math.radians(a)))), fill=(200,200,200,60), width=1)
    save(im, f"{d}/web.png")

    print(f"  {biome}: 20 tiles")


# ── Río Memoria ─────────────────────────────────────────────────
def tile_rio_memoria():
    biome = "rio-memoria"
    d = os.path.join(TILES_DIR, biome)
    S = 32
    C = {
        "water_d": hex_rgba("#2A6BA8"),
        "water":   hex_rgba("#4A90D9"),
        "water_l": hex_rgba("#6DB8E8"),
        "sand":    hex_rgba("#D4C4A0"),
        "sand_d":  hex_rgba("#C4B490"),
        "pebble":  hex_rgba("#B8B8B8"),
        "peb_d":   hex_rgba("#A0A0A0"),
        "orb_b":   hex_rgba("#4A90D9"),
        "orb_p":   hex_rgba("#C9A8E8"),
        "wood":    hex_rgba("#8B6F47"),
        "wood_d":  hex_rgba("#7A5E3A"),
        "brown":   hex_rgba("#5A3820"),
        "green":   hex_rgba("#7EC8A0"),
        "gold":    hex_rgba("#F0C060"),
    }

    for fi in range(3):
        im, dr = new_im(S)
        dr.rectangle((0,0,S,S), fill=C["water_d"])
        # flow lines with offset per frame
        off = fi * 3
        for w in range(0, 36, 6):
            x = (w + off) % 32
            dr.ellipse((x, 20, x+8, 22), fill=(255,255,255,50))
            dr.ellipse((x-2, 8, x+6, 10), fill=(100,180,230,60))
        dr.ellipse((2,2,30,6), fill=(255,255,255,30))
        dr.ellipse((4,26,28,30), fill=(255,255,255,20))
        save(im, f"{d}/river_{fi}.png")

    # sand_0
    im, dr = new_im(S)
    dr.rectangle((0,0,S,S), fill=C["sand"])
    add_noise(dr, (0,0,S,S), [C["sand_d"], (200,180,140,255)], 0.25)
    for _ in range(5):
        x = random.randint(2,28)
        y = random.randint(2,28)
        dr.ellipse((x,y,x+2,y+2), fill=(180,160,120,255))
    save(im, f"{d}/sand_0.png")

    # pebble_0, pebble_1
    for pi in range(2):
        im, dr = new_im(S)
        dr.rectangle((0,0,S,S), fill=C["sand"])
        add_noise(dr, (0,0,S,S), [C["sand_d"]], 0.15)
        for _ in range(4+pi*2):
            x = random.randint(4,24)
            y = random.randint(4,24)
            sz = random.randint(3,6)
            dr.ellipse((x,y,x+sz,y+sz), fill=C["pebble"])
            dr.ellipse((x+1,y+1,x+sz-1,y+sz-1), fill=C["peb_d"])
        save(im, f"{d}/pebble_{pi}.png")

    # bridge_0
    im, dr = new_im(S)
    dr.rectangle((0,0,S,S), fill=C["water_d"])
    dr.rectangle((0,14,32,20), fill=C["wood"])
    dr.rectangle((0,10,32,12), fill=C["wood_d"])
    dr.rectangle((0,22,32,24), fill=C["wood_d"])
    # rails
    dr.rectangle((2,4,4,14), fill=C["wood"])
    dr.rectangle((28,4,30,14), fill=C["wood"])
    dr.rectangle((2,2,30,4), fill=C["wood"])
    add_noise(dr, (0,14,32,20), [C["wood_d"]], 0.2)
    save(im, f"{d}/bridge_0.png")

    # Fill to 20
    # water_calm
    im, dr = new_im(S)
    dr.rectangle((0,0,S,S), fill=C["water"])
    for _ in range(8):
        x = random.randint(2,28)
        y = random.randint(2,28)
        dr.ellipse((x,y,x+5,y+2), fill=(255,255,255,40))
    dr.ellipse((6,4,26,8), fill=(255,255,255,25))
    save(im, f"{d}/water_calm.png")

    # bank_top
    im, dr = new_im(S)
    dr.rectangle((0,0,S,S), fill=C["brown"])
    add_noise(dr, (0,0,S,S), [(80,50,30,255)], 0.2)
    dr.rectangle((0,20,32,32), fill=C["water_d"])
    dr.ellipse((0,16,32,24), fill=C["brown"])
    save(im, f"{d}/bank_top.png")

    # bank_bottom
    im, dr = new_im(S)
    dr.rectangle((0,0,S,S), fill=C["water_d"])
    dr.rectangle((0,0,32,12), fill=C["brown"])
    dr.ellipse((0,8,32,18), fill=C["brown"])
    add_noise(dr, (0,0,32,14), [(80,50,30,255)], 0.2)
    save(im, f"{d}/bank_bottom.png")

    # memory_orb_blue
    im, dr = new_im(S)
    dr.rectangle((0,0,S,S), fill=C["water_d"])
    for r in reversed(range(4, 12, 2)):
        a = 255 - (r-4)*40
        dr.ellipse((16-r,16-r,16+r,16+r), fill=(*C["orb_b"][:3], a))
    dr.ellipse((10,10,22,22), fill=(255,255,255,200))
    dr.ellipse((12,12,20,20), fill=C["orb_b"])
    save(im, f"{d}/memory_orb_blue.png")

    # memory_orb_purple
    im, dr = new_im(S)
    dr.rectangle((0,0,S,S), fill=C["water_d"])
    for r in reversed(range(4, 12, 2)):
        a = 255 - (r-4)*40
        dr.ellipse((16-r,16-r,16+r,16+r), fill=(*C["orb_p"][:3], a))
    dr.ellipse((10,10,22,22), fill=(255,255,255,200))
    dr.ellipse((12,12,20,20), fill=C["orb_p"])
    save(im, f"{d}/memory_orb_purple.png")

    # willow_trunk
    im, dr = new_im(S)
    dr.rectangle((0,0,S,S), fill=C["brown"])
    dr.rectangle((13,0,19,32), fill=(80,50,30,255))
    dr.rectangle((14,0,18,32), fill=(100,70,40,255))
    save(im, f"{d}/willow_trunk.png")

    # willow_leaves
    im, dr = new_im(S)
    dr.rectangle((0,0,S,S), fill=C["water_l"])
    for _ in range(20):
        x = random.randint(0,32)
        y = random.randint(0,32)
        dr.line((x,y,x+random.randint(-3,3),y+4), fill=C["green"], width=1)
    dr.ellipse((0,-4,32,8), fill=C["green"])
    save(im, f"{d}/willow_leaves.png")

    # ripple
    im, dr = new_im(S)
    dr.rectangle((0,0,S,S), fill=C["water_d"])
    dr.ellipse((4,12,28,20), fill=(255,255,255,30))
    dr.ellipse((8,14,24,18), fill=(255,255,255,40))
    save(im, f"{d}/ripple.png")

    # grass bank
    im, dr = new_im(S)
    dr.rectangle((0,0,S,S), fill=C["green"])
    dr.rectangle((0,20,32,32), fill=C["water_d"])
    dr.ellipse((0,16,32,24), fill=C["green"])
    save(im, f"{d}/bank_grass.png")

    # reed
    im, dr = new_im(S)
    dr.rectangle((0,0,S,S), fill=C["water_d"])
    for i in range(4):
        x = 6 + i*8
        dr.line((x,32,x+random.randint(-2,2),8), fill=C["green"], width=2)
        dr.ellipse((x-2,4,x+2,10), fill=(120,80,40,255))
    save(im, f"{d}/reed.png")

    # floating_petal
    im, dr = new_im(S)
    dr.rectangle((0,0,S,S), fill=C["water"])
    for _ in range(4):
        x = random.randint(4,24)
        y = random.randint(4,24)
        dr.ellipse((x,y,x+3,y+2), fill=(255,200,220,180))
    save(im, f"{d}/floating_petal.png")

    # lotus
    im, dr = new_im(S)
    dr.rectangle((0,0,S,S), fill=C["water"])
    dr.ellipse((10,18,22,30), fill=C["green"])
    for a in range(0, 360, 72):
        rx = 16 + int(6 * math.cos(math.radians(a)))
        ry = 18 + int(4 * math.sin(math.radians(a)))
        dr.ellipse((rx-3, ry-3, rx+3, ry+3), fill=(255,200,220,200))
    save(im, f"{d}/lotus.png")

    # firefly
    im, dr = new_im(S)
    dr.rectangle((0,0,S,S), fill=C["water_d"])
    for _ in range(4):
        fx = random.randint(4,28)
        fy = random.randint(4,28)
        for r in range(6, 2, -2):
            dr.ellipse((fx-r, fy-r, fx+r, fy+r), fill=(*C["gold"][:3], 40-r*5))
        dr.ellipse((fx-1, fy-1, fx+1, fy+1), fill=(255,255,200,255))
    save(im, f"{d}/firefly.png")

    print(f"  {biome}: 20 tiles")


# ── Montaña Razonamiento ────────────────────────────────────────
def tile_montana_razonamiento():
    biome = "montana-razonamiento"
    d = os.path.join(TILES_DIR, biome)
    S = 32
    C = {
        "stone":   hex_rgba("#8B8B8B"),
        "stone_d": hex_rgba("#6B6B6B"),
        "stone_l": hex_rgba("#B8B8B8"),
        "crystal": hex_rgba("#4A90D9"),
        "cry_l":   hex_rgba("#6DB8E8"),
        "snow":    hex_rgba("#F0F0F0"),
        "snow_l":  hex_rgba("#FFFFFF"),
        "gold":    hex_rgba("#F0C060"),
        "blue":    hex_rgba("#4A90D9"),
    }

    im, dr = new_im(S)
    dr.rectangle((0,0,S,S), fill=C["stone"])
    add_noise(dr, (0,0,S,S), [C["stone_d"], C["stone_l"]], 0.25)
    for _ in range(4):
        x = random.randint(2,28)
        y = random.randint(2,28)
        dr.line((x,y,x+4,y+2), fill=(120,120,120,255), width=1)
    save(im, f"{d}/stone_0.png")

    im, dr = new_im(S)
    dr.rectangle((0,0,S,S), fill=C["stone_d"])
    add_noise(dr, (0,0,S,S), [(100,100,100,255), C["stone"]], 0.3)
    for _ in range(3):
        x = random.randint(2,28)
        y = random.randint(2,28)
        dr.line((x,y,x+6,y), fill=(80,80,80,255), width=1)
    save(im, f"{d}/stone_1.png")

    # cliff_0
    im, dr = new_im(S)
    dr.rectangle((0,0,S,S), fill=C["stone"])
    dr.rectangle((0,0,32,8), fill=C["stone_l"])
    dr.rectangle((0,6,32,8), fill=C["stone"])
    # crack
    for y_ in range(8, 32, 4):
        dr.line((16+y_%8, y_, 24, y_+2), fill=(80,80,80,255), width=1)
    add_noise(dr, (0,8,S,S), [C["stone_d"]], 0.2)
    save(im, f"{d}/cliff_0.png")

    # snow_patch
    im, dr = new_im(S)
    dr.rectangle((0,0,S,S), fill=C["stone"])
    dr.ellipse((2,2,30,30), fill=C["snow"])
    dr.ellipse((4,4,28,28), fill=C["snow_l"])
    add_noise(dr, (4,4,28,28), [C["snow"], (200,200,210,255)], 0.15)
    save(im, f"{d}/snow_patch.png")

    # flag_0
    im, dr = new_im(S)
    dr.rectangle((0,0,S,S), fill=C["stone"])
    dr.rectangle((14,2,16,32), fill=(100,80,60,255))
    dr.polygon([(16,2),(30,6),(16,10)], fill=C["gold"])
    dr.polygon([(16,2),(28,6),(16,10)], fill=(255,200,100,255))
    save(im, f"{d}/flag_0.png")

    # Fill to 20
    im, dr = new_im(S)
    dr.rectangle((0,0,S,S), fill=C["stone_l"])
    add_noise(dr, (0,0,S,S), [C["stone"], (200,200,200,255)], 0.2)
    save(im, f"{d}/stone_light.png")

    # crystal_blue
    im, dr = new_im(S)
    dr.rectangle((0,0,S,S), fill=C["stone_d"])
    for r in reversed(range(4, 12, 2)):
        a = 255 - (r-4)*50
        dr.polygon([(16,4-r),(16+r,20),(16-r,20)], fill=(*C["crystal"][:3], a))
    dr.polygon([(16,2),(18,18),(14,18)], fill=C["cry_l"])
    save(im, f"{d}/crystal_0.png")

    im, dr = new_im(S)
    dr.rectangle((0,0,S,S), fill=C["stone"])
    dr.polygon([(8,4),(24,8),(20,28),(12,28)], fill=C["crystal"])
    dr.polygon([(10,6),(22,9),(19,26),(13,26)], fill=C["cry_l"])
    save(im, f"{d}/crystal_1.png")

    # glyph
    im, dr = new_im(S)
    dr.rectangle((0,0,S,S), fill=C["stone"])
    dr.ellipse((6,6,26,26), fill=C["stone_l"], outline=C["gold"], width=2)
    dr.line((16,10,16,22), fill=C["gold"], width=2)
    dr.line((10,16,22,16), fill=C["gold"], width=2)
    dr.ellipse((12,12,20,20), outline=C["gold"], width=1)
    save(im, f"{d}/glyph.png")

    # pedestal
    im, dr = new_im(S)
    dr.rectangle((0,0,S,S), fill=C["stone"])
    dr.polygon([(8,32),(24,32),(28,20),(4,20)], fill=C["stone_l"])
    dr.polygon([(10,20),(22,20),(24,10),(8,10)], fill=C["stone"])
    dr.ellipse((8,6,24,14), fill=C["stone_l"])
    dr.ellipse((14,22,18,26), fill=C["gold"])
    save(im, f"{d}/pedestal.png")

    # ladder
    im, dr = new_im(S)
    dr.rectangle((0,0,S,S), fill=C["stone"])
    dr.rectangle((8,0,10,32), fill=(120,80,40,255))
    dr.rectangle((22,0,24,32), fill=(120,80,40,255))
    for y_ in range(0, 32, 6):
        dr.rectangle((8,y_,24,y_+2), fill=(140,100,50,255))
    save(im, f"{d}/ladder.png")

    # cloud
    im, dr = new_im(S)
    dr.rectangle((0,0,S,S), fill=(135,206,235,255))
    for _ in range(8):
        x = random.randint(4,28)
        y = random.randint(4,24)
        r = random.randint(6,12)
        dr.ellipse((x,y,x+r,y+r), fill=(255,255,255,200))
    save(im, f"{d}/cloud.png")

    # extra stone
    im, dr = new_im(S)
    dr.rectangle((0,0,S,S), fill=C["stone_d"])
    add_noise(dr, (0,0,S,S), [C["stone"], C["stone_l"]], 0.2)
    for _ in range(6):
        x = random.randint(4,24)
        y = random.randint(4,24)
        dr.ellipse((x,y,x+4,y+3), fill=C["stone_l"])
    save(im, f"{d}/stone_2.png")

    # extra crystals
    im, dr = new_im(S)
    dr.rectangle((0,0,S,S), fill=C["stone"])
    dr.polygon([(4,28),(8,10),(12,28)], fill=C["crystal"])
    dr.polygon([(5,28),(8,12),(11,28)], fill=C["cry_l"])
    dr.polygon([(20,28),(24,14),(28,28)], fill=C["crystal"])
    dr.polygon([(21,28),(24,16),(27,28)], fill=C["cry_l"])
    save(im, f"{d}/crystal_cluster.png")

    # plateau
    im, dr = new_im(S)
    dr.rectangle((0,0,S,S), fill=C["stone_d"])
    dr.rectangle((0,16,32,32), fill=C["stone"])
    dr.line((0,16,32,16), fill=C["stone_l"], width=2)
    add_noise(dr, (0,16,32,32), [C["stone_l"]], 0.15)
    save(im, f"{d}/plateau.png")

    # watchtower
    im, dr = new_im(S)
    dr.rectangle((0,0,S,S), fill=C["stone"])
    dr.rectangle((8,8,24,32), fill=C["stone_d"])
    dr.rectangle((6,4,26,10), fill=C["stone_l"])
    dr.rectangle((12,4,20,8), fill=C["gold"])
    save(im, f"{d}/watchtower.png")

    # rope_bridge
    im, dr = new_im(S)
    dr.rectangle((0,0,S,S), fill=C["stone_d"])
    dr.line((0,18,32,14), fill=(120,80,40,255), width=2)
    dr.line((0,22,32,18), fill=(120,80,40,255), width=2)
    for x in range(4, 32, 8):
        dr.rectangle((x,12,x+2,24), fill=(100,70,35,255))
    save(im, f"{d}/rope_bridge.png")

    # gem
    im, dr = new_im(S)
    dr.rectangle((0,0,S,S), fill=C["stone"])
    dr.polygon([(16,2),(28,12),(24,28),(8,28),(4,12)], fill=C["gold"])
    dr.polygon([(16,4),(26,12),(22,26),(10,26),(6,12)], fill=(255,255,200,200))
    save(im, f"{d}/gem.png")

    # campfire
    im, dr = new_im(S)
    dr.rectangle((0,0,S,S), fill=C["stone_d"])
    dr.rectangle((12,24,20,32), fill=(80,50,30,255))
    dr.polygon([(16,2),(20,14),(12,14)], fill=C["gold"])
    dr.polygon([(16,4),(18,12),(14,12)], fill=(255,255,200,255))
    save(im, f"{d}/campfire.png")

    # snow_rock
    im, dr = new_im(S)
    dr.rectangle((0,0,S,S), fill=C["stone"])
    dr.ellipse((4,16,28,32), fill=C["stone_d"])
    dr.ellipse((6,4,26,20), fill=C["snow"])
    dr.ellipse((8,6,24,18), fill=C["snow_l"])
    save(im, f"{d}/snow_rock.png")

    print(f"  {biome}: 20 tiles")


# ── Valle Lenguaje ──────────────────────────────────────────────
def tile_valle_lenguaje():
    biome = "valle-lenguaje"
    d = os.path.join(TILES_DIR, biome)
    S = 32
    C = {
        "meadow":  hex_rgba("#A8D5BA"),
        "mead_d":  hex_rgba("#8BC4A0"),
        "gold":    hex_rgba("#F0C060"),
        "gold_d":  hex_rgba("#E8A84A"),
        "pink":    hex_rgba("#E8B4B8"),
        "pink_d":  hex_rgba("#D4A0A4"),
        "blue":    hex_rgba("#4A90D9"),
        "paper":   hex_rgba("#FFF5F0"),
        "paper_d": hex_rgba("#E8DCC8"),
        "brown":   hex_rgba("#8B6F47"),
        "wood":    hex_rgba("#D4C4A0"),
        "green":   hex_rgba("#7EC8A0"),
    }
    LETTERS = "ABC"

    # book_0, book_1
    for bi in range(2):
        im, dr = new_im(S)
        dr.rectangle((0,0,S,S), fill=C["meadow"])
        colors = [C["gold"], C["pink"], C["blue"]]
        c = colors[bi % 3]
        # book shape
        dr.rectangle((8,10,24,28), fill=c)
        dr.rectangle((6,8,22,26), fill=C["paper"])
        dr.line((14,8,14,26), fill=(200,180,160,255), width=2)
        # cover
        dr.rectangle((8,10,24,12), fill=c)
        dr.rectangle((8,26,24,28), fill=c)
        save(im, f"{d}/book_{bi}.png")

    # path_letter
    im, dr = new_im(S)
    dr.rectangle((0,0,S,S), fill=C["meadow"])
    add_noise(dr, (0,0,S,S), [C["mead_d"]], 0.15)
    for li, ch in enumerate("A"):
        x = 8 + li*16
        dr.text((x,10), ch, fill=(*C["gold"][:3], 100))
    save(im, f"{d}/path_letter.png")

    # grass_flower
    im, dr = new_im(S)
    dr.rectangle((0,0,S,S), fill=C["meadow"])
    add_noise(dr, (0,0,S,S), [C["mead_d"], C["green"]], 0.15)
    for _ in range(6):
        x = random.randint(4,28)
        y = random.randint(4,28)
        dr.line((x,y,x,y-4), fill=C["green"], width=1)
        sub_pixels(dr, (x-1,y-5), (255,255,255,255), 2)
    save(im, f"{d}/grass_flower.png")

    # ink_0
    im, dr = new_im(S)
    dr.rectangle((0,0,S,S), fill=C["paper"])
    add_noise(dr, (0,0,S,S), [C["paper_d"]], 0.15)
    for _ in range(5):
        x = random.randint(4,28)
        y = random.randint(4,28)
        r = random.randint(3,8)
        dr.ellipse((x,y,x+r,y+r), fill=(30,30,80,180))
        dr.ellipse((x+1,y+1,x+r-1,y+r-1), fill=(50,50,100,150))
    save(im, f"{d}/ink_0.png")

    # Fill to 20
    # letter flowers A, B, C
    for li, (ch, col) in enumerate([("A", C["gold"]), ("B", C["pink"]), ("C", C["blue"])]):
        im, dr = new_im(S)
        dr.rectangle((0,0,S,S), fill=C["meadow"])
        dr.line((16,28,16,12), fill=C["green"], width=2)
        # petals
        cx, cy = 16, 8
        for a in range(0, 360, 60):
            rx = cx + int(5 * math.cos(math.radians(a)))
            ry = cy + int(5 * math.sin(math.radians(a)))
            dr.ellipse((rx-3, ry-3, rx+3, ry+3), fill=col)
        dr.text((14, 5), ch, fill=(255,255,255,255))
        save(im, f"{d}/flower_letter_{ch.lower()}.png")

    # scroll
    im, dr = new_im(S)
    dr.rectangle((0,0,S,S), fill=C["meadow"])
    dr.ellipse((4,8,28,28), fill=C["paper"])
    dr.ellipse((4,6,28,10), fill=C["brown"])
    dr.ellipse((4,26,28,30), fill=C["brown"])
    for i, ch in enumerate("AB"):
        dr.text((8+i*10, 14), ch, fill=(100,80,60,180))
    save(im, f"{d}/scroll.png")

    # quill
    im, dr = new_im(S)
    dr.rectangle((0,0,S,S), fill=C["meadow"])
    dr.line((6,26,20,6), fill=(200,180,160,255), width=2)
    dr.line((20,6,24,2), fill=(200,180,160,255), width=1)
    dr.ellipse((4,24,8,28), fill=C["gold"])
    save(im, f"{d}/quill.png")

    # bookshelf
    im, dr = new_im(S)
    dr.rectangle((0,0,S,S), fill=C["meadow"])
    dr.rectangle((2,2,30,30), fill=C["brown"])
    dr.rectangle((2,4,30,14), fill=C["gold"])
    dr.rectangle((2,18,30,28), fill=C["blue"])
    dr.rectangle((2,2,30,4), fill=C["wood"])
    dr.rectangle((2,14,30,18), fill=C["wood"])
    dr.rectangle((2,28,30,30), fill=C["wood"])
    save(im, f"{d}/bookshelf.png")

    # floating_word
    im, dr = new_im(S)
    dr.rectangle((0,0,S,S), fill=C["meadow"])
    for r in range(6, 0, -2):
        dr.ellipse((16-r,16-r,16+r,16+r), fill=(*C["gold"][:3], 40))
    dr.text((6,10), "Habla", fill=(*C["gold"][:3], 200))
    save(im, f"{d}/floating_word.png")

    # echo_ring
    im, dr = new_im(S)
    dr.rectangle((0,0,S,S), fill=C["meadow"])
    dr.ellipse((4,10,28,24), outline=(*C["pink"][:3], 80), width=2)
    dr.ellipse((8,12,24,22), outline=(*C["pink"][:3], 120), width=1)
    save(im, f"{d}/echo_ring.png")

    # poetry_tree
    im, dr = new_im(S)
    dr.rectangle((0,0,S,S), fill=C["meadow"])
    dr.rectangle((14,16,18,32), fill=C["brown"])
    dr.ellipse((4,0,28,18), fill=C["green"])
    # hanging verses
    for i in range(3):
        x = 8 + i*8
        dr.line((x,12,x,20), fill=(200,180,160,255), width=1)
        dr.ellipse((x-2,18,x+2,22), fill=C["paper"])
    save(im, f"{d}/poetry_tree.png")

    # rainbow_bridge
    im, dr = new_im(S)
    dr.rectangle((0,0,S,S), fill=C["meadow"])
    for i, col in enumerate([(255,0,0,200), (255,165,0,200), (255,255,0,200), (0,200,0,200), (0,0,255,200), (128,0,128,200)]):
        dr.arc((4+i*2, 12+i*2, 28-i*2, 32), 0, 180, fill=col, width=2)
    save(im, f"{d}/rainbow_bridge.png")

    # speech_bubble
    im, dr = new_im(S)
    dr.rectangle((0,0,S,S), fill=C["meadow"])
    dr.ellipse((6,8,26,26), fill=C["paper"])
    dr.ellipse((8,10,24,24), fill=C["paper_d"])
    dr.ellipse((20,24,26,30), fill=C["paper"])
    dr.text((10,14), "!", fill=(*C["gold"][:3], 200))
    save(im, f"{d}/speech_bubble.png")

    # ink_well
    im, dr = new_im(S)
    dr.rectangle((0,0,S,S), fill=C["meadow"])
    dr.ellipse((8,20,24,32), fill=C["brown"])
    dr.ellipse((8,18,24,24), fill=(60,40,20,255))
    dr.ellipse((12,8,20,20), fill=(60,40,20,255))
    dr.ellipse((14,10,18,14), fill=(30,20,60,255))
    save(im, f"{d}/ink_well.png")

    # feather
    im, dr = new_im(S)
    dr.rectangle((0,0,S,S), fill=C["meadow"])
    dr.line((24,4,8,28), fill=(200,180,160,255), width=2)
    for i in range(5):
        x = 20 - i*3
        y = 8 + i*4
        dr.line((x,y,x-4,y-2), fill=(200,180,160,255), width=1)
    save(im, f"{d}/feather.png")

    # star_flower
    im, dr = new_im(S)
    dr.rectangle((0,0,S,S), fill=C["meadow"])
    dr.line((16,28,16,14), fill=C["green"], width=2)
    for a in range(0, 360, 72):
        rx = 16 + int(6 * math.cos(math.radians(a)))
        ry = 10 + int(6 * math.sin(math.radians(a)))
        dr.polygon([(rx,ry-3),(rx+2,ry),(rx,ry+3),(rx-2,ry)], fill=C["gold"])
    dr.ellipse((14,8,18,12), fill=(255,255,200,255))
    save(im, f"{d}/star_flower.png")

    # word_bridge
    im, dr = new_im(S)
    dr.rectangle((0,0,S,S), fill=C["meadow"])
    dr.rectangle((0,14,32,18), fill=C["gold"])
    for i,ch in enumerate("ABC"):
        dr.text((4+i*10, 10), ch, fill=(*C["brown"][:3], 200))
    save(im, f"{d}/word_bridge.png")

    print(f"  {biome}: 20 tiles")


# ── Torre Matemáticas ───────────────────────────────────────────
def tile_torre_matematicas():
    biome = "torre-matematicas"
    d = os.path.join(TILES_DIR, biome)
    S = 32
    C = {
        "white":   (240,240,240,255),
        "black":   hex_rgba("#2D3436"),
        "grid":    hex_rgba("#4A90D9"),
        "gold":    hex_rgba("#F0C060"),
        "gold_d":  hex_rgba("#E8A84A"),
        "blue":    hex_rgba("#4A90D9"),
        "blue_l":  hex_rgba("#6DB8E8"),
        "gray":    hex_rgba("#8B8B8B"),
        "gray_d":  hex_rgba("#6B6B6B"),
    }

    # tile_floor
    im, dr = new_im(S)
    dr.rectangle((0,0,S,S), fill=C["white"])
    dr.rectangle((0,0,15,15), fill=C["white"], outline=C["black"], width=1)
    dr.rectangle((16,0,31,15), fill=C["black"])
    dr.rectangle((0,16,15,31), fill=C["black"])
    dr.rectangle((16,16,31,31), fill=C["white"], outline=C["black"], width=1)
    save(im, f"{d}/tile_floor.png")

    # number_0..9
    for ni in range(10):
        im, dr = new_im(S)
        if (ni // 4) % 2 == 0:
            dr.rectangle((0,0,S,S), fill=C["white"])
        else:
            dr.rectangle((0,0,S,S), fill=C["black"])
        dr.text((8,6), str(ni), fill=(*C["gold"][:3], 220))
        save(im, f"{d}/number_{ni}.png")

    # stair_0, stair_1
    for si in range(2):
        im, dr = new_im(S)
        dr.rectangle((0,0,S,S), fill=C["gray"])
        off = si * 4
        for s in range(4):
            sy = 24 - s*6
            sx = 4 + off + s*6
            dr.rectangle((sx,sy,sx+6,sy+4), fill=C["gray_d"], outline=(150,150,150,255), width=1)
        save(im, f"{d}/stair_{si}.png")

    # gear_0
    im, dr = new_im(S)
    dr.rectangle((0,0,S,S), fill=C["black"])
    dr.ellipse((8,8,24,24), fill=C["gold"])
    dr.ellipse((12,12,20,20), fill=C["black"])
    for a in range(0, 360, 45):
        rx = 16 + int(10 * math.cos(math.radians(a)))
        ry = 16 + int(10 * math.sin(math.radians(a)))
        dr.rectangle((rx-2, ry-2, rx+2, ry+2), fill=C["gold_d"])
    save(im, f"{d}/gear_0.png")

    # Fill to 20
    # math symbols
    for sym, col in [("+", C["blue"]), ("-", C["blue"]), ("×", C["blue"]), ("÷", C["blue"])]:
        im, dr = new_im(S)
        dr.rectangle((0,0,S,S), fill=C["white"] if sym != "÷" else C["black"])
        dr.text((8,6), sym, fill=(*col[:3], 200))
        save(im, f"{d}/symbol_{sym}.png")

    # pillar_base
    im, dr = new_im(S)
    dr.rectangle((0,0,S,S), fill=C["gray"])
    dr.rectangle((8,0,24,32), fill=C["gray_d"])
    dr.rectangle((6,0,26,4), fill=C["white"])
    dr.rectangle((6,28,26,32), fill=C["white"])
    add_noise(dr, (8,4,24,28), [(130,130,130,255)], 0.15)
    save(im, f"{d}/pillar_base.png")

    # pillar_top
    im, dr = new_im(S)
    dr.rectangle((0,0,S,S), fill=C["gray"])
    dr.polygon([(4,10),(16,0),(28,10)], fill=C["white"])
    dr.rectangle((10,10,22,32), fill=C["gray_d"])
    dr.ellipse((12,10,20,14), fill=C["gold"])
    save(im, f"{d}/pillar_top.png")

    # window_arch
    im, dr = new_im(S)
    dr.rectangle((0,0,S,S), fill=C["gray_d"])
    dr.rectangle((6,10,26,30), fill=C["blue"])
    dr.arc((6,2,26,18), 180, 360, fill=C["white"], width=2)
    dr.rectangle((6,10,26,12), fill=C["white"])
    dr.line((16,10,16,30), fill=C["white"], width=1)
    save(im, f"{d}/window_arch.png")

    print(f"  {biome}: 20 tiles")


# ── Gruta Visual ────────────────────────────────────────────────
def tile_gruta_visual():
    biome = "gruta-visual"
    d = os.path.join(TILES_DIR, biome)
    S = 32
    C = {
        "floor":   hex_rgba("#1A1A2E"),
        "floor_l": hex_rgba("#2A2A4E"),
        "crystal": hex_rgba("#4A90D9"),
        "cry_l":   hex_rgba("#6DB8E8"),
        "purple":  hex_rgba("#C9A8E8"),
        "pink":    hex_rgba("#E8B4B8"),
        "gold":    hex_rgba("#F0C060"),
        "white":   (255,255,255,255),
    }

    # cave_wall
    im, dr = new_im(S)
    dr.rectangle((0,0,S,S), fill=C["floor"])
    add_noise(dr, (0,0,S,S), [C["floor_l"], (30,30,60,255)], 0.3)
    for _ in range(6):
        x = random.randint(2,28)
        y = random.randint(2,28)
        dr.ellipse((x,y,x+4,y+3), fill=(40,40,70,255))
    save(im, f"{d}/cave_wall.png")

    # crystal_0 (blue), crystal_1 (violet)
    for ci, col in enumerate([C["crystal"], C["purple"]]):
        im, dr = new_im(S)
        dr.rectangle((0,0,S,S), fill=C["floor"])
        dr.polygon([(8,4),(24,8),(20,28),(12,28)], fill=col)
        dr.polygon([(10,6),(22,9),(19,26),(13,26)], fill=(*col[:3], 180))
        dr.polygon([(14,8),(18,10),(17,22),(15,22)], fill=(255,255,255,100))
        save(im, f"{d}/crystal_{ci}.png")

    # mirror_0
    im, dr = new_im(S)
    dr.rectangle((0,0,S,S), fill=C["floor"])
    dr.ellipse((4,4,28,28), fill=C["floor_l"])
    dr.ellipse((6,6,26,26), fill=C["crystal"])
    dr.ellipse((8,8,24,24), fill=(200,230,255,255))
    dr.line((16,8,16,24), fill=(255,255,255,100), width=1)
    save(im, f"{d}/mirror_0.png")

    # shadow_0
    im, dr = new_im(S)
    dr.rectangle((0,0,S,S), fill=C["floor"])
    for _ in range(10):
        x = random.randint(2,28)
        y = random.randint(2,28)
        r = random.randint(4,10)
        dr.ellipse((x,y,x+r,y+r), fill=(10,10,30,120))
    save(im, f"{d}/shadow_0.png")

    # Fill to 20
    # stalactite
    im, dr = new_im(S)
    dr.rectangle((0,0,S,S), fill=C["floor"])
    dr.polygon([(8,0),(24,0),(20,12),(12,12)], fill=C["floor_l"])
    dr.polygon([(10,0),(22,0),(18,10),(14,10)], fill=(40,40,70,255))
    save(im, f"{d}/stalactite.png")

    # stalagmite
    im, dr = new_im(S)
    dr.rectangle((0,0,S,S), fill=C["floor"])
    dr.polygon([(10,32),(22,32),(24,20),(8,20)], fill=C["floor_l"])
    dr.polygon([(12,32),(20,32),(21,22),(11,22)], fill=(40,40,70,255))
    save(im, f"{d}/stalagmite.png")

    # illusion_a
    im, dr = new_im(S)
    dr.rectangle((0,0,S,S), fill=C["floor"])
    for r in range(0, 16, 4):
        dr.ellipse((16-r,16-r,16+r,16+r), outline=(*C["purple"][:3], 150-r*8), width=1)
    save(im, f"{d}/illusion_a.png")

    # illusion_b
    im, dr = new_im(S)
    dr.rectangle((0,0,S,S), fill=C["floor"])
    for i in range(8):
        x = i*4
        c = C["gold"] if i%2==0 else C["crystal"]
        dr.rectangle((x,0,x+2,32), fill=(*c[:3], 100))
    save(im, f"{d}/illusion_b.png")

    # prism
    im, dr = new_im(S)
    dr.rectangle((0,0,S,S), fill=C["floor"])
    dr.polygon([(16,4),(28,24),(4,24)], fill=(200,200,255,100))
    dr.polygon([(16,6),(26,23),(6,23)], fill=(255,255,255,80))
    dr.line((16,4,16,24), fill=(255,255,255,120), width=1)
    save(im, f"{d}/prism.png")

    # dream_bubble
    im, dr = new_im(S)
    dr.rectangle((0,0,S,S), fill=C["floor"])
    for r in reversed(range(4, 12, 2)):
        a = 255 - (r-4)*50
        dr.ellipse((16-r,16-r,16+r,16+r), fill=(*C["purple"][:3], a))
    dr.ellipse((12,12,20,20), fill=(255,255,255,200))
    save(im, f"{d}/dream_bubble.png")

    # canvas
    im, dr = new_im(S)
    dr.rectangle((0,0,S,S), fill=C["floor"])
    dr.rectangle((6,6,26,28), fill=(255,245,240,255))
    dr.rectangle((4,4,28,30), fill=(200,180,160,255))
    for _ in range(5):
        x = random.randint(8,24)
        y = random.randint(8,26)
        c = random.choice([C["gold"], C["pink"], C["crystal"], C["purple"]])
        dr.ellipse((x,y,x+3,y+3), fill=(*c[:3], 150))
    save(im, f"{d}/canvas.png")

    # paint splashes
    for si, col in enumerate([C["gold"], C["pink"], C["crystal"]]):
        im, dr = new_im(S)
        dr.rectangle((0,0,S,S), fill=C["floor"])
        for _ in range(8):
            x = random.randint(4,28)
            y = random.randint(4,28)
            r = random.randint(3,7)
            dr.ellipse((x,y,x+r,y+r), fill=(*col[:3], 100))
        save(im, f"{d}/splash_{si}.png")

    # mirror_pool
    im, dr = new_im(S)
    dr.rectangle((0,0,S,S), fill=C["floor"])
    dr.ellipse((4,8,28,26), fill=C["crystal"])
    dr.ellipse((6,10,26,24), fill=(200,230,255,200))
    dr.line((16,10,16,24), fill=(255,255,255,60), width=1)
    dr.ellipse((10,14,14,16), fill=(255,255,255,80))
    save(im, f"{d}/mirror_pool.png")

    # glowing_eye
    im, dr = new_im(S)
    dr.rectangle((0,0,S,S), fill=C["floor"])
    dr.ellipse((8,10,24,22), fill=C["gold"])
    dr.ellipse((12,14,20,18), fill=(255,255,200,255))
    dr.ellipse((15,15,17,17), fill=(50,30,10,200))
    save(im, f"{d}/glowing_eye.png")

    # void_pool
    im, dr = new_im(S)
    dr.rectangle((0,0,S,S), fill=C["floor"])
    dr.ellipse((6,6,26,26), fill=(0,0,10,255))
    dr.ellipse((8,8,24,24), fill=(20,20,50,255))
    for r in range(4, 14, 4):
        dr.ellipse((16-r,16-r,16+r,16+r), outline=(*C["purple"][:3], 60), width=1)
    save(im, f"{d}/void_pool.png")

    # easel
    im, dr = new_im(S)
    dr.rectangle((0,0,S,S), fill=C["floor"])
    dr.rectangle((14,4,18,28), fill=(120,80,40,255))
    dr.rectangle((6,8,26,18), fill=(255,245,240,255))
    dr.rectangle((8,10,24,16), fill=C["crystal"])
    save(im, f"{d}/easel.png")

    # tentacle
    im, dr = new_im(S)
    dr.rectangle((0,0,S,S), fill=C["floor"])
    dr.arc((0,14,16,32), 180, 360, fill=C["purple"], width=3)
    dr.arc((12,18,28,34), 180, 360, fill=C["pink"], width=3)
    save(im, f"{d}/tentacle.png")

    print(f"  {biome}: 20 tiles")


# ── Camino Velocidad ────────────────────────────────────────────
def tile_camino_velocidad():
    biome = "camino-velocidad"
    d = os.path.join(TILES_DIR, biome)
    S = 32
    C = {
        "track":   hex_rgba("#E8A84A"),
        "track_d": hex_rgba("#D4923A"),
        "white":   (255,255,255,255),
        "pink":    hex_rgba("#E8B4B8"),
        "pink_d":  hex_rgba("#D4A0A4"),
        "gold":    hex_rgba("#F0C060"),
        "gold_d":  hex_rgba("#E8A84A"),
    }

    im, dr = new_im(S)
    dr.rectangle((0,0,S,S), fill=C["track"])
    add_noise(dr, (0,0,S,S), [C["track_d"], C["gold"]], 0.2)
    dr.line((0,16,32,16), fill=C["white"], width=2)
    dr.line((0,20,32,20), fill=C["white"], width=1)
    save(im, f"{d}/road_0.png")

    im, dr = new_im(S)
    dr.rectangle((0,0,S,S), fill=C["white"])
    add_noise(dr, (0,0,S,S), [(240,240,240,255)], 0.2)
    dr.line((0,16,32,16), fill=C["track"], width=2)
    save(im, f"{d}/road_1.png")

    # arrow_0
    im, dr = new_im(S)
    dr.rectangle((0,0,S,S), fill=C["track_d"])
    # arrow shape
    dr.polygon([(16,4),(28,16),(20,16),(20,28),(12,28),(12,16),(4,16)], fill=C["gold"])
    save(im, f"{d}/arrow_0.png")

    # dash_0
    im, dr = new_im(S)
    dr.rectangle((0,0,S,S), fill=C["track"])
    for i in range(4):
        x = 2 + i*8
        dr.line((x,8,x+4,24), fill=(255,255,255,80), width=2)
    save(im, f"{d}/dash_0.png")

    # finish_0
    im, dr = new_im(S)
    dr.rectangle((0,0,S,S), fill=C["track"])
    for c_ in range(4):
        for r in range(4):
            x = c_*8
            y = r*8
            col = C["white"] if (c_+r) % 2 == 0 else C["gold"]
            dr.rectangle((x,y,x+8,y+8), fill=col)
    save(im, f"{d}/finish_0.png")

    # Fill to 20
    # arrows in all directions
    dirs = {"up": (16,4,28,16,20,16,20,28,12,28,12,16,4,16),
            "right": (28,16,16,4,16,12,4,12,4,20,16,20,16,28),
            "down": (16,28,4,16,12,16,12,4,20,4,20,16,28,16),
            "left": (4,16,16,28,16,20,28,20,28,12,16,12,16,4)}
    for dname, pts in dirs.items():
        im, dr = new_im(S)
        dr.rectangle((0,0,S,S), fill=C["track_d"])
        dr.polygon(pts, fill=C["gold"])
        save(im, f"{d}/arrow_{dname}.png")

    # speed_boost
    im, dr = new_im(S)
    dr.rectangle((0,0,S,S), fill=C["pink"])
    add_noise(dr, (0,0,S,S), [C["pink_d"]], 0.15)
    dr.ellipse((8,8,24,24), fill=(255,255,255,100))
    save(im, f"{d}/speed_boost.png")

    # start_line
    im, dr = new_im(S)
    dr.rectangle((0,0,S,S), fill=C["track"])
    dr.rectangle((14,0,18,32), fill=C["white"])
    save(im, f"{d}/start_line.png")

    # checkered_wall
    im, dr = new_im(S)
    for c_ in range(4):
        for r in range(4):
            x = c_*8
            y = r*8
            col = C["gold"] if (c_+r) % 2 == 0 else C["white"]
            dr.rectangle((x,y,x+8,y+8), fill=col)
    save(im, f"{d}/checkered_wall.png")

    # time_orb
    im, dr = new_im(S)
    for r in reversed(range(4, 12, 2)):
        a = 255 - (r-4)*50
        dr.ellipse((16-r,16-r,16+r,16+r), fill=(*C["gold"][:3], a))
    dr.ellipse((12,12,20,20), fill=(255,255,255,200))
    dr.text((13,12), "♪", fill=(*C["gold"][:3], 200))
    save(im, f"{d}/time_orb.png")

    # wind_swirl
    im, dr = new_im(S)
    dr.rectangle((0,0,S,S), fill=C["track"])
    for i in range(3):
        x = 2 + i*10
        dr.arc((x,8,x+8,24), 0, 180, fill=(255,255,255,60), width=2)
    save(im, f"{d}/wind_swirl.png")

    # boost_pad
    im, dr = new_im(S)
    dr.rectangle((0,0,S,S), fill=C["pink_d"])
    dr.rectangle((4,4,28,28), fill=C["pink"])
    dr.ellipse((10,12,22,20), fill=(255,255,255,80))
    dr.line((16,10,16,22), fill=C["white"], width=2)
    dr.line((10,16,22,16), fill=C["white"], width=2)
    save(im, f"{d}/boost_pad.png")

    # tunnel
    im, dr = new_im(S)
    dr.rectangle((0,0,S,S), fill=C["track_d"])
    dr.ellipse((4,4,28,28), fill=C["track"])
    dr.ellipse((8,8,24,24), fill=C["gold"])
    save(im, f"{d}/tunnel.png")

    # banner
    im, dr = new_im(S)
    dr.rectangle((0,0,S,S), fill=C["track"])
    dr.line((16,2,16,30), fill=(100,80,60,255), width=2)
    dr.polygon([(16,4),(28,10),(16,16)], fill=C["pink"])
    save(im, f"{d}/banner.png")

    # coin
    im, dr = new_im(S)
    dr.rectangle((0,0,S,S), fill=C["track"])
    dr.ellipse((8,8,24,24), fill=C["gold"])
    dr.ellipse((10,10,22,22), fill=(255,255,200,255))
    dr.text((13,12), "$", fill=(*C["gold_d"][:3], 220))
    save(im, f"{d}/coin.png")

    # ring
    im, dr = new_im(S)
    dr.rectangle((0,0,S,S), fill=C["track"])
    dr.ellipse((6,6,26,26), outline=C["gold"], width=3)
    dr.ellipse((10,10,22,22), outline=(255,255,200,255), width=2)
    save(im, f"{d}/ring.png")

    # flag_pole
    im, dr = new_im(S)
    dr.rectangle((0,0,S,S), fill=C["track"])
    dr.line((16,2,16,32), fill=(150,130,110,255), width=2)
    for i, col in enumerate([C["gold"], C["pink"], C["white"]]):
        dr.polygon([(16,4+i*6),(30,7+i*6),(16,10+i*6)], fill=col)
    save(im, f"{d}/flag_pole.png")

    print(f"  {biome}: 20 tiles")


# ── Generate all tiles ────────────────────────────────────────────────
def generate_all_tiles():
    print("=== TILES 32×32 ===")
    tile_jardin_central()
    tile_bosque_atencion()
    tile_rio_memoria()
    tile_montana_razonamiento()
    tile_valle_lenguaje()
    tile_torre_matematicas()
    tile_gruta_visual()
    tile_camino_velocidad()


# ═══════════════════════════════════════════════════════════════════
#  FONDOS PARALLAX 512×256 — degradados + siluetas pixel art
# ═══════════════════════════════════════════════════════════════════

def fondo_jardin_central():
    d = FONDOS_DIR
    W, H = 512, 256

    # Layer 0: sky
    im, dr = new_im_wh(W, H)
    for y in range(H):
        t = y / H
        r = int(135 + t*30)
        g = int(206 - t*20)
        b = int(235 - t*10)
        dr.line((0, y, W, y), fill=(r, g, b, 255))
    # clouds
    for cx in range(60, W, 120):
        for _ in range(5):
            ox = random.randint(-10, 10)
            oy = random.randint(-10, 10)
            dr.ellipse((cx+ox, 30+oy, cx+ox+40, 50+oy), fill=(255,255,255,200))
    save(im, f"{d}/jardin-central_0.png")

    # Layer 1: hills
    im, dr = new_im_wh(W, H)
    dr.rectangle((0,0,W,H), fill=RGBA)
    pts = []
    for x in range(0, W+2, 8):
        y = H - 40 - int(30 * math.sin(x * 0.02)) - int(15 * math.sin(x * 0.05))
        pts.append((x, y))
    pts.append((W, H))
    pts.append((0, H))
    dr.polygon(pts, fill=hex_rgba("#8BC4A0"))
    # second hill
    pts2 = []
    for x in range(0, W+2, 8):
        y = H - 60 - int(25 * math.sin(x * 0.025 + 1))
        pts2.append((x, y))
    pts2.append((W, H))
    pts2.append((0, H))
    dr.polygon(pts2, fill=hex_rgba("#7EC8A0"))
    save(im, f"{d}/jardin-central_1.png")

    # Layer 2: trees + foreground
    im, dr = new_im_wh(W, H)
    dr.rectangle((0,0,W,H), fill=RGBA)
    # grass base
    dr.rectangle((0, H-40, W, H), fill=hex_rgba("#A8D5BA"))
    # trees
    for tx in range(30, W, 80):
        dr.rectangle((tx, H-80, tx+6, H-40), fill=hex_rgba("#5A3820"))
        dr.ellipse((tx-15, H-105, tx+21, H-75), fill=hex_rgba("#6BB890"))
        dr.ellipse((tx-10, H-115, tx+16, H-85), fill=hex_rgba("#7EC8A0"))
    # flowers
    for _ in range(30):
        fx = random.randint(0, W)
        fy = H - random.randint(5, 20)
        dr.line((fx, fy, fx, fy-4), fill=hex_rgba("#7EC8A0"), width=1)
        col = random.choice([hex_rgba("#F0C060"), hex_rgba("#E8B4B8")])
        dr.ellipse((fx-2, fy-6, fx+2, fy-2), fill=col)
    save(im, f"{d}/jardin-central_2.png")
    print("  fondos/jardin-central: 3 layers")


def fondo_bosque_atencion():
    d = FONDOS_DIR
    W, H = 512, 256

    im, dr = new_im_wh(W, H)
    for y in range(H):
        t = y / H
        r = int(135 - t*60)
        g = int(206 - t*60)
        b = int(235 - t*40)
        dr.line((0, y, W, y), fill=(max(0,r), max(0,g), max(0,b), 80))
    save(im, f"{d}/bosque-atencion_0.png")

    im, dr = new_im_wh(W, H)
    for tx in range(0, W+20, 40):
        dr.rectangle((tx, 40, tx+8, H), fill=hex_rgba("#1A3A0A"))
        dr.ellipse((tx-12, 10, tx+20, 50), fill=hex_rgba("#2D5016"))
    save(im, f"{d}/bosque-atencion_1.png")

    im, dr = new_im_wh(W, H)
    dr.rectangle((0, H-60, W, H), fill=hex_rgba("#3A6B1E"))
    for tx in range(10, W, 60):
        dr.rectangle((tx, H-100, tx+6, H-60), fill=hex_rgba("#4A3520"))
        dr.ellipse((tx-10, H-125, tx+16, H-90), fill=hex_rgba("#4A7C2E"))
    # mushrooms
    for _ in range(8):
        mx = random.randint(10, W-10)
        my = H - random.randint(10, 30)
        dr.rectangle((mx, my, mx+2, my+6), fill=(220,200,180,255))
        dr.ellipse((mx-3, my-4, mx+5, my+2), fill=hex_rgba("#D94040"))
    # light rays
    for rx in range(30, W, 80):
        dr.polygon([(rx, 0), (rx+12, 0), (rx+30, H), (rx-10, H)], fill=(240,192,96,30))
    save(im, f"{d}/bosque-atencion_2.png")
    print("  fondos/bosque-atencion: 3 layers")


def fondo_rio_memoria():
    d = FONDOS_DIR
    W, H = 512, 256

    im, dr = new_im_wh(W, H)
    for y in range(H):
        t = y / H
        r = int(42 - t*20)
        g = int(42 - t*20)
        b = int(78 - t*30)
        dr.line((0, y, W, y), fill=(max(0,r), max(0,g), max(0,b), 255))
    for _ in range(40):
        sx = random.randint(0, W)
        sy = random.randint(0, H//2)
        dr.ellipse((sx, sy, sx+1, sy+1), fill=(255,255,255,150))
    save(im, f"{d}/rio-memoria_0.png")

    im, dr = new_im_wh(W, H)
    for mx in range(0, W, 80):
        dr.polygon([(mx, H-40), (mx+40, H-80), (mx+80, H-40)], fill=hex_rgba("#5A3820"))
    save(im, f"{d}/rio-memoria_1.png")

    im, dr = new_im_wh(W, H)
    dr.rectangle((0, H-50, W, H), fill=hex_rgba("#2A6BA8"))
    for _ in range(20):
        wx = random.randint(0, W)
        wy = H - random.randint(10, 45)
        dr.ellipse((wx, wy, wx+8, wy+2), fill=(255,255,255,50))
    for ox in range(20, W, 60):
        dr.ellipse((ox, H-55, ox+8, H-45), fill=hex_rgba("#C9A8E8"))
    save(im, f"{d}/rio-memoria_2.png")
    print("  fondos/rio-memoria: 3 layers")


def fondo_montana_razonamiento():
    d = FONDOS_DIR
    W, H = 512, 256

    im, dr = new_im_wh(W, H)
    for y in range(H):
        t = y / H
        r = int(42 - t*20)
        g = int(74 - t*30)
        b = int(139 - t*40)
        dr.line((0, y, W, y), fill=(max(0,r), max(0,g), max(0,b), 255))
    save(im, f"{d}/montana-razonamiento_0.png")

    im, dr = new_im_wh(W, H)
    pts = []
    for x in range(0, W+4, 4):
        y = H - 80 - int(50 * math.sin(x * 0.015)) - int(20 * math.sin(x * 0.03))
        pts.append((x, y))
    pts.append((W, H))
    pts.append((0, H))
    dr.polygon(pts, fill=hex_rgba("#8B8B8B"))
    for px in range(30, W, 70):
        dr.polygon([(px, H-140), (px+5, H-100), (px+10, H-140)], fill=hex_rgba("#FFFFFF"))
    save(im, f"{d}/montana-razonamiento_1.png")

    im, dr = new_im_wh(W, H)
    for cx in range(20, W, 90):
        dr.polygon([(cx, H-60), (cx+4, H-80), (cx+8, H-60)], fill=hex_rgba("#4A90D9"))
    # foreground rocks
    for _ in range(15):
        rx = random.randint(0, W)
        ry = H - random.randint(10, 30)
        dr.ellipse((rx, ry, rx+6, ry+4), fill=hex_rgba("#6B6B6B"))
    save(im, f"{d}/montana-razonamiento_2.png")
    print("  fondos/montana-razonamiento: 3 layers")


def fondo_valle_lenguaje():
    d = FONDOS_DIR
    W, H = 512, 256

    im, dr = new_im_wh(W, H)
    for y in range(H):
        t = y / H
        r = int(255 - t*30)
        g = int(228 - t*50)
        b = int(196 - t*60)
        dr.line((0, y, W, y), fill=(max(0,r), max(0,g), max(0,b), 255))
    save(im, f"{d}/valle-lenguaje_0.png")

    im, dr = new_im_wh(W, H)
    dr.rectangle((0, H-100, W, H), fill=hex_rgba("#8BC4A0"))
    pts = []
    for x in range(0, W+4, 4):
        y = H - 100 - int(20 * math.sin(x * 0.02))
        pts.append((x, y))
    pts.append((W, H))
    pts.append((0, H))
    dr.polygon(pts, fill=hex_rgba("#A8D5BA"))
    save(im, f"{d}/valle-lenguaje_1.png")

    im, dr = new_im_wh(W, H)
    dr.rectangle((0, H-60, W, H), fill=hex_rgba("#7EC8A0"))
    # floating words
    for fi, (wx, ch) in enumerate([(60,"A"),(150,"B"),(250,"C"),(350,"D"),(450,"E")]):
        dr.text((wx, H-90), ch, fill=(*hex_rgba("#F0C060")[:3], 180))
    # rainbow bridge
    for i, col in enumerate([(255,0,0,150),(255,165,0,150),(255,255,0,150),(0,200,0,150),(0,0,255,150),(128,0,128,150)]):
        dr.arc((100+i*2, H-100+i*2, 300-i*2, H), 0, 180, fill=col, width=3)
    save(im, f"{d}/valle-lenguaje_2.png")
    print("  fondos/valle-lenguaje: 3 layers")


def fondo_torre_matematicas():
    d = FONDOS_DIR
    W, H = 512, 256

    im, dr = new_im_wh(W, H)
    for y in range(H):
        t = y / H
        r = int(26 - t*10)
        g = int(26 - t*10)
        b = int(46 - t*20)
        dr.line((0, y, W, y), fill=(max(0,r), max(0,g), max(0,b), 255))
    for _ in range(30):
        sx, sy = random.randint(0,W), random.randint(0,H//2)
        dr.ellipse((sx, sy, sx+1, sy+1), fill=(255,255,255,150))
    save(im, f"{d}/torre-matematicas_0.png")

    im, dr = new_im_wh(W, H)
    # tower silhouette
    dr.rectangle((180, 40, 220, H), fill=hex_rgba("#2D3436"))
    dr.rectangle((170, 30, 230, 50), fill=hex_rgba("#4A90D9"))
    # windows
    for wy in range(60, H-20, 30):
        dr.ellipse((190, wy, 196, wy+10), fill=hex_rgba("#F0C060"))
        dr.ellipse((204, wy, 210, wy+10), fill=hex_rgba("#F0C060"))
    save(im, f"{d}/torre-matematicas_1.png")

    im, dr = new_im_wh(W, H)
    dr.rectangle((0, H-50, W, H), fill=hex_rgba("#5A5A5A"))
    # numbers floating
    for ni, (nx, num) in enumerate([(40,"1"),(100,"2"),(300,"3"),(400,"4"),(480,"5")]):
        dr.text((nx, H-80), num, fill=(*hex_rgba("#4A90D9")[:3], 150))
    # gears
    for gx in [50, 250, 450]:
        dr.ellipse((gx, H-70, gx+12, H-58), fill=hex_rgba("#F0C060"))
        dr.ellipse((gx+3, H-67, gx+9, H-61), fill=hex_rgba("#2D3436"))
    save(im, f"{d}/torre-matematicas_2.png")
    print("  fondos/torre-matematicas: 3 layers")


def fondo_gruta_visual():
    d = FONDOS_DIR
    W, H = 512, 256

    im, dr = new_im_wh(W, H)
    for y in range(H):
        t = y / H
        v = int(10 + t*20)
        dr.line((0, y, W, y), fill=(v, v, v+10, 255))
    save(im, f"{d}/gruta-visual_0.png")

    im, dr = new_im_wh(W, H)
    for cx in range(20, W, 60):
        dr.polygon([(cx, H-60), (cx+4, H-100), (cx+8, H-60)], fill=hex_rgba("#4A90D9"))
        dr.polygon([(cx+8, H-60), (cx+12, H-90), (cx+16, H-60)], fill=hex_rgba("#C9A8E8"))
    save(im, f"{d}/gruta-visual_1.png")

    im, dr = new_im_wh(W, H)
    dr.rectangle((0, H-40, W, H), fill=hex_rgba("#1A1A2E"))
    # dream bubbles
    for _ in range(10):
        bx = random.randint(10, W-10)
        by = random.randint(20, H-40)
        dr.ellipse((bx, by, bx+8, by+8), fill=(*hex_rgba("#C9A8E8")[:3], 80))
    # prism
    dr.polygon([(256, 40), (280, H-40), (220, H-40)], fill=(200,200,255,50))
    dr.line((256, 40, 256, H-40), fill=(255,255,255,60), width=1)
    # paint splashes
    for _ in range(12):
        sx = random.randint(10, W-10)
        sy = H - random.randint(10, 35)
        col = random.choice([hex_rgba("#F0C060"), hex_rgba("#E8B4B8"), hex_rgba("#4A90D9")])
        dr.ellipse((sx, sy, sx+6, sy+4), fill=(*col[:3], 80))
    save(im, f"{d}/gruta-visual_2.png")
    print("  fondos/gruta-visual: 3 layers")


def fondo_camino_velocidad():
    d = FONDOS_DIR
    W, H = 512, 256

    im, dr = new_im_wh(W, H)
    for y in range(H):
        t = y / H
        r = int(232 - t*60)
        g = int(164 - t*50)
        b = int(74 - t*40)
        dr.line((0, y, W, y), fill=(max(0,r), max(0,g), max(0,b), 255))
    save(im, f"{d}/camino-velocidad_0.png")

    im, dr = new_im_wh(W, H)
    for cx in range(0, W, 80):
        dr.ellipse((cx, 40, cx+60, 70), fill=(255,255,255,100))
    save(im, f"{d}/camino-velocidad_1.png")

    im, dr = new_im_wh(W, H)
    dr.rectangle((0, H-70, W, H), fill=hex_rgba("#E8A84A"))
    # speed lines
    for _ in range(20):
        lx = random.randint(0, W)
        ly = H - random.randint(10, 60)
        dr.line((lx, ly, lx+20, ly), fill=(255,255,255,80), width=1)
    # dash patterns
    for dx in range(0, W, 30):
        dr.rectangle((dx+5, H-30, dx+15, H-26), fill=(255,255,255,100))
    # checkered flag
    for c_ in range(6):
        for r in range(3):
            x = 400 + c_*10
            y = H-50 + r*10
            col = (255,255,255,200) if (c_+r) % 2 == 0 else hex_rgba("#F0C060")
            dr.rectangle((x, y, x+10, y+10), fill=col)
    save(im, f"{d}/camino-velocidad_2.png")
    print("  fondos/camino-velocidad: 3 layers")


def generate_all_fondos():
    print("\n=== FONDOS PARALLAX 512×256 ===")
    fondo_jardin_central()
    fondo_bosque_atencion()
    fondo_rio_memoria()
    fondo_montana_razonamiento()
    fondo_valle_lenguaje()
    fondo_torre_matematicas()
    fondo_gruta_visual()
    fondo_camino_velocidad()


# ═══════════════════════════════════════════════════════════════════
#  UI ELEMENTOS — botones, burbujas, iconos, HUD
# ═══════════════════════════════════════════════════════════════════

def generate_ui():
    print("\n=== UI ELEMENTOS ===")
    d = UI_DIR
    C = {
        "green":    hex_rgba("#A8D5BA"),
        "green_d":  hex_rgba("#8BC4A0"),
        "green_hv": hex_rgba("#7EC8A0"),
        "green_pr": hex_rgba("#6BB890"),
        "gold":     hex_rgba("#F0C060"),
        "gold_d":   hex_rgba("#E8A84A"),
        "gold_hv":  hex_rgba("#D4923A"),
        "pink":     hex_rgba("#E8B4B8"),
        "cream":    hex_rgba("#FFF5F0"),
        "cream_d":  hex_rgba("#E8DCC8"),
        "dark":     hex_rgba("#2D3436"),
        "blue":     hex_rgba("#4A90D9"),
        "blue_l":   hex_rgba("#6DB8E8"),
        "gray":     hex_rgba("#8B8B8B"),
    }

    # ── Buttons 128×48 ──
    def make_btn(fn, fill_top, fill_bot, border_col=None):
        im, dr = new_im_wh(128, 48)
        soft_shadow(dr, (0,0,128,48), 10)
        dr.rounded_rectangle((0,0,128,48), radius=10, fill=fill_top, outline=border_col, width=1)
        # gradient line at top
        dr.rounded_rectangle((2,2,126,24), radius=8, fill=(*fill_top[:3], 60))
        return im

    make_btn("btn_normal.png", C["green"], C["green_d"], C["green_d"])
    make_btn("btn_hover.png", C["green_hv"], C["green_d"], C["green_d"])
    make_btn("btn_press.png", C["green_pr"], C["green_hv"], C["green_d"])

    # ── Dialog bubble 256×96 ──
    im, dr = new_im_wh(256, 96)
    soft_shadow(dr, (0,0,256,96), 12)
    dr.rounded_rectangle((0,0,256,96), radius=12, fill=C["cream"], outline=C["cream_d"], width=2)
    # tail
    dr.polygon([(30, 84), (40, 96), (50, 84)], fill=C["cream"])
    dr.polygon([(30, 84), (40, 95), (50, 84)], fill=C["cream_d"])
    # text lines
    dr.rounded_rectangle((20, 16, 236, 36), radius=4, fill=(*C["cream_d"][:3], 80))
    dr.rounded_rectangle((20, 42, 200, 56), radius=4, fill=(*C["cream_d"][:3], 60))
    save(im, f"{d}/dialog_bubble.png")

    # ── Icons 32×32 ──
    # icon_seed
    im, dr = new_im(32)
    dr.ellipse((10,20,22,30), fill=(139,90,43,255))
    dr.ellipse((12,22,20,28), fill=(180,130,60,255))
    dr.line((16,20,16,8), fill=C["green"], width=2)
    dr.ellipse((12,2,20,12), fill=C["green"])
    save(im, f"{d}/icon_seed.png")

    # icon_flower
    im, dr = new_im(32)
    dr.line((16,28,16,14), fill=C["green"], width=2)
    for a in range(0, 360, 60):
        rx = 16 + int(6 * math.cos(math.radians(a)))
        ry = 10 + int(6 * math.sin(math.radians(a)))
        dr.ellipse((rx-3, ry-3, rx+3, ry+3), fill=C["pink"])
    dr.ellipse((13,7,19,13), fill=(255,255,200,255))
    save(im, f"{d}/icon_flower.png")

    # icon_tool
    im, dr = new_im(32)
    dr.rectangle((14,2,18,20), fill=(139,90,43,255))
    dr.rectangle((12,18,20,28), fill=(139,90,43,255))
    dr.ellipse((10,14,22,22), fill=(180,130,60,255))
    dr.ellipse((12,16,20,20), fill=C["green"])
    save(im, f"{d}/icon_tool.png")

    # ── HUD brújula 32×32 ──
    im, dr = new_im(32)
    dr.ellipse((4,4,28,28), outline=C["gold"], width=2)
    dr.polygon([(16,2),(20,12),(12,12)], fill=C["gold"])
    dr.polygon([(16,30),(20,20),(12,20)], fill=C["gold_d"])
    dr.line((4,16,12,16), fill=C["gold_d"], width=1)
    dr.line((20,16,28,16), fill=C["gold_d"], width=1)
    dr.ellipse((15,15,17,17), fill=C["gold"])
    save(im, f"{d}/hud_brújula.png")

    # ── Menu tree 32×32 ──
    im, dr = new_im(32)
    dr.rectangle((14,18,18,32), fill=(139,90,43,255))
    dr.ellipse((4,0,28,20), fill=C["green"])
    dr.ellipse((6,2,26,18), fill=C["green_hv"])
    dr.ellipse((8,4,24,16), fill=C["green"])
    save(im, f"{d}/menu_tree.png")

    # ── Extra biome icons 32×32 ──
    icons = {
        "icon_attention": (C["gold"], "eye"),    # ojo
        "icon_memory":    (C["blue"], "book"),    # libro
        "icon_reasoning": (C["gray"], "gear"),    # engranaje
        "icon_language":  (C["pink"], "letter"), # letra
        "icon_math":      (C["gold"], "num"),     # numero
        "icon_visual":    ((200,150,255,255), "brush"),
        "icon_speed":     (C["gold_d"], "bolt"),
    }
    for iname, (col, typ) in icons.items():
        im, dr = new_im(32)
        dr.rounded_rectangle((2,2,30,30), radius=6, fill=(*C["cream"][:3], 200), outline=col, width=2)
        if typ == "eye":
            dr.ellipse((8,10,24,22), fill=(255,255,255,255))
            dr.ellipse((12,14,20,18), fill=col)
        elif typ == "book":
            dr.rectangle((8,6,24,26), fill=(*col[:3], 200))
            dr.rectangle((10,8,22,12), fill=(255,255,255,200))
            dr.rectangle((10,14,22,16), fill=(255,255,255,150))
            dr.rectangle((10,18,22,20), fill=(255,255,255,150))
        elif typ == "gear":
            dr.ellipse((8,8,24,24), fill=(*col[:3], 200))
            dr.ellipse((12,12,20,20), fill=C["cream"])
            for a in range(0, 360, 60):
                rx = 16 + int(7 * math.cos(math.radians(a)))
                ry = 16 + int(7 * math.sin(math.radians(a)))
                dr.ellipse((rx-2, ry-2, rx+2, ry+2), fill=(*col[:3], 200))
        elif typ == "letter":
            dr.rectangle((8,6,24,26), fill=(*C["cream_d"][:3], 200))
            dr.ellipse((14,8,18,14), fill=(*col[:3], 200))
            dr.text((14,16), "A", fill=(*col[:3], 200))
        elif typ == "num":
            dr.text((10,6), "42", fill=(*col[:3], 220))
        elif typ == "brush":
            dr.line((8,22,22,8), fill=(139,90,43,255), width=3)
            dr.line((22,4,26,8), fill=(139,90,43,255), width=2)
            for _ in range(5):
                dx = random.randint(4, 28)
                dy = random.randint(4, 28)
                c = random.choice([C["gold"], C["pink"], C["blue"], C["green"]])
                dr.ellipse((dx, dy, dx+3, dy+3), fill=(*c[:3], 150))
        elif typ == "bolt":
            dr.polygon([(16,2),(26,16),(18,16),(14,30),(8,14),(16,14)], fill=(*col[:3], 220))
        save(im, f"{d}/{iname}.png")

    # ── health bar 128×16 ──
    im, dr = new_im_wh(128, 16)
    dr.rounded_rectangle((0,0,128,16), radius=4, fill=C["cream_d"])
    dr.rounded_rectangle((2,2,94,14), radius=3, fill=(80,200,80,255))
    dr.rounded_rectangle((96,2,126,14), radius=3, fill=(200,80,80,255))
    save(im, f"{d}/health_bar.png")

    # ── xp bar 128×16 ──
    im, dr = new_im_wh(128, 16)
    dr.rounded_rectangle((0,0,128,16), radius=4, fill=C["cream_d"])
    dr.rounded_rectangle((2,2,86,14), radius=3, fill=C["blue"])
    save(im, f"{d}/xp_bar.png")

    # ── stamina bar 128×16 ──
    im, dr = new_im_wh(128, 16)
    dr.rounded_rectangle((0,0,128,16), radius=4, fill=C["cream_d"])
    dr.rounded_rectangle((2,2,70,14), radius=3, fill=C["gold"])
    save(im, f"{d}/stamina_bar.png")

    # ── compass dots 256×8 ──
    im, dr = new_im_wh(256, 8)
    for i in range(32):
        x = 4 + i*8
        col = C["gold"] if i % 8 == 0 else C["cream_d"]
        dr.ellipse((x, 1, x+4, 7), fill=col)
    save(im, f"{d}/compass_dots.png")

    print("  ui: buttons, dialog_bubble, icons, HUD elements")


# ═══════════════════════════════════════════════════════════════════
#  MAIN
# ═══════════════════════════════════════════════════════════════════

def count_files():
    import subprocess
    for base, label in [(TILES_DIR, "tiles"), (FONDOS_DIR, "fondos"), (UI_DIR, "ui")]:
        r = subprocess.run(["find", base, "-name", "*.png"], capture_output=True, text=True)
        files = [f for f in r.stdout.strip().split("\n") if f]
        print(f"  {label}: {len(files)} files")


if __name__ == "__main__":
    import subprocess, sys

    # Ensure target dirs exist
    for d in [TILES_DIR, FONDOS_DIR, UI_DIR]:
        os.makedirs(d, exist_ok=True)

    generate_all_tiles()
    generate_all_fondos()
    generate_ui()

    print("\n═══════════════════════════════════")
    print(" GENERATION COMPLETE — FILE COUNT:")
    print("═══════════════════════════════════")
    count_files()
