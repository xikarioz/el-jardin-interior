#!/usr/bin/env python3
"""
Generador de sprites 128×128 para "El Jardín Interior".
Cada frame es un PNG individual con fondo transparente.
Usa PIL para dibujo geométrico detallado estilo pixel-art.
"""
import os, math, random
from PIL import Image, ImageDraw

random.seed(42)
BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)))

SIZE = 128

def new_img(bg=None):
    return Image.new("RGBA", (SIZE, SIZE), (0,0,0,0) if bg is None else bg)

def save(img, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    img.save(path, "PNG")

def soft_shadow(d, shape, color, offset=3, alpha=60):
    """Dibuja una sombra suave desplazada."""
    if shape[0] == "ellipse":
        x1, y1, x2, y2 = shape[1:]
        d.ellipse([x1+offset, y1+offset, x2+offset, y2+offset],
                  fill=color+(alpha,))
    elif shape[0] == "polygon":
        pts = shape[1]
        shifted = [(x+offset, y+offset) for x,y in pts]
        d.polygon(shifted, fill=color+(alpha,))

def blush(d, cx, cy, color=(232,180,184,80)):
    """Mejillas sonrosadas."""
    d.ellipse([cx-22, cy+4, cx-6, cy+18], fill=color)
    d.ellipse([cx+6, cy+4, cx+22, cy+18], fill=color)

def big_eye(d, cx, cy, size=10):
    """Ojo grande y expresivo."""
    w = size * 2
    h = int(size * 2.2)
    d.ellipse([cx-w, cy-h, cx+w, cy+h], fill=(255,255,255))
    d.ellipse([cx-int(w*0.4), cy-int(h*0.2), cx+int(w*0.4), cy+int(h*0.6)],
              fill=(40,40,40))
    d.ellipse([cx-int(w*0.15), cy-int(h*0.1), cx+int(w*0.15), cy+int(h*0.2)],
              fill=(255,255,255,200))

def big_eye_closed(d, cx, cy, size=10):
    """Ojo cerrado (sonrisa feliz)."""
    w = size * 2
    h = int(size * 2.2)
    d.arc([cx-w, cy-h//2, cx+w, cy+h//2], 0, 180, fill=(40,40,40), width=3)

# ── PROTAGONISTA ─────────────────────────────────────────────

PROTA = {
    "piel":  (255,228,196),
    "rosa":  (232,180,184),
    "capa":  (168,213,186),
    "capa_osc": (130,185,155),
    "pelo":  (139,115,85),
    "pelo_osc": (100,80,55),
    "ojos":  (60,40,20),
    "botas": (80,60,40),
    "ropa":  (240,240,235),
    "pantalon": (100,130,110),
    "boca":  (200,120,120),
}

def _prota_cuerpo(d, cx, cy, frame, direction):
    p = PROTA
    # Sombra bajo personaje
    d.ellipse([cx-30, cy+52, cx+30, cy+62], fill=(0,0,0,30))

    # Cuerpo / torso
    body_bob = 0
    if direction == "walk":
        body_bob = [-2, 0, -1, 1][frame % 4]

    bb = body_bob

    # Capa (detrás del cuerpo)
    cape_offset = [0, -1, 1, 0][frame % 4] if direction == "walk" else 0
    d.polygon([
        (cx-34, cy-10+bb), (cx-44, cy+30+bb), (cx-40, cy+50+bb),
        (cx-30, cy+44+bb), (cx-20, cy+20+bb)
    ], fill=p["capa_osc"])
    d.polygon([
        (cx+34, cy-10+bb), (cx+44, cy+30+bb), (cx+40, cy+50+bb),
        (cx+30, cy+44+bb), (cx+20, cy+20+bb)
    ], fill=p["capa_osc"])
    # Capa posterior
    d.polygon([
        (cx-35, cy-5+bb), (cx+35, cy-5+bb),
        (cx+40, cy+52+bb), (cx-40, cy+52+bb)
    ], fill=p["capa"])

    # Torso (remera blanca)
    d.rounded_rectangle(
        [cx-20, cy+14+bb, cx+20, cy+42+bb], radius=8, fill=p["ropa"]
    )

    # Brazos
    arm_swing = [(-6, -4), (0, 2), (6, -2), (0, 0)][frame % 4] if direction == "walk" else (0, 0)
    # Brazo izquierdo
    d.polygon([
        (cx-20, cy+16+bb), (cx-28, cy+22+bb+arm_swing[0]),
        (cx-26, cy+36+bb+arm_swing[0]), (cx-18, cy+30+bb)
    ], fill=p["piel"])
    # Brazo derecho
    d.polygon([
        (cx+20, cy+16+bb), (cx+28, cy+22+bb+arm_swing[1]),
        (cx+26, cy+36+bb+arm_swing[1]), (cx+18, cy+30+bb)
    ], fill=p["piel"])

    # Pantalón
    leg_offsets = [(0, 0), (6, -2), (0, -4), (-6, -2)] if direction == "walk" else [(0, 0), (0, 0), (0, 0), (0, 0)]
    lo = leg_offsets[frame % 4] if direction == "walk" else (0, 0)
    d.rounded_rectangle(
        [cx-18, cy+40+bb, cx-4, cy+54+bb+lo[0]], radius=4, fill=p["pantalon"]
    )
    d.rounded_rectangle(
        [cx+4, cy+40+bb, cx+18, cy+54+bb+lo[1]], radius=4, fill=p["pantalon"]
    )

    # Botas
    d.rounded_rectangle(
        [cx-20, cy+50+bb+lo[0], cx-3, cy+57+bb+lo[0]], radius=3, fill=p["botas"]
    )
    d.rounded_rectangle(
        [cx+3, cy+50+bb+lo[1], cx+20, cy+57+bb+lo[1]], radius=3, fill=p["botas"]
    )

    return bb, arm_swing

def _prota_cabeza(d, cx, cy, frame, direction, talking=False):
    p = PROTA
    head_bob = 0
    if direction == "walk":
        head_bob = [-2, 0, -1, 1][frame % 4]

    # Cabeza
    head_y = cy - 20 + head_bob
    d.ellipse([cx-26, head_y-22, cx+26, head_y+22], fill=p["piel"])

    # Pelo (detrás)
    d.ellipse([cx-28, head_y-24, cx+28, head_y+6], fill=p["pelo"])
    # Flequillo
    d.ellipse([cx-28, head_y-24, cx+28, head_y-2], fill=p["pelo_osc"])
    # Mechones laterales
    d.ellipse([cx-30, head_y-18, cx-22, head_y+6], fill=p["pelo"])
    d.ellipse([cx+22, head_y-18, cx+30, head_y+6], fill=p["pelo"])

    # Ojos grandes
    eye_y = head_y + 2
    big_eye(d, cx-14, eye_y, 10)
    big_eye(d, cx+14, eye_y, 10)

    if frame == 1 and not talking:  # blink en frame 1 de idle
        big_eye_closed(d, cx-14, eye_y-2, 10)
        big_eye_closed(d, cx+14, eye_y-2, 10)

    # Cejas
    d.arc([cx-24, head_y-10, cx-4, head_y-2], 180, 360, fill=p["pelo_osc"], width=3)
    d.arc([cx+4, head_y-10, cx+24, head_y-2], 180, 360, fill=p["pelo_osc"], width=3)

    # Sonrisa / boca
    if talking:
        mouth_open = [2, 6][frame % 2]
        d.ellipse([cx-5, head_y+12, cx+5, head_y+12+mouth_open], fill=(60,30,30))
        d.ellipse([cx-4, head_y+13, cx+4, head_y+13+mouth_open-1], fill=(200,80,80))
    else:
        d.arc([cx-8, head_y+6, cx+8, head_y+14], 0, 180, fill=p["boca"], width=3)

    # Mejillas
    blush(d, cx, head_y, p["rosa"]+(100,))

    # Capucha de la capa sobre la cabeza
    d.arc([cx-34, head_y-18, cx+34, head_y+10], 180, 360, fill=p["capa"], width=4)

def _prota_side(d, cx, cy, frame, direction, facing_right):
    p = PROTA
    body_bob = [-2, 0, -1, 1][frame % 4] if direction == "walk" else 0
    arm_swing = [(-4, 4), (2, 0), (4, -2), (0, 2)][frame % 4] if direction == "walk" else (0, 0)
    sign = 1 if facing_right else -1

    # Sombra
    d.ellipse([cx-28, cy+52, cx+28, cy+62], fill=(0,0,0,30))

    # Capa
    x1 = cx-42*sign
    x2 = cx-20*sign
    d.ellipse([min(x1,x2), cy-10+body_bob, max(x1,x2), cy+50+body_bob], fill=p["capa_osc"])

    # Torso
    d.rounded_rectangle([cx-12, cy+14+body_bob, cx+20, cy+42+body_bob], radius=6, fill=p["ropa"])

    # Brazo
    d.polygon([
        (cx+18, cy+16+body_bob), (cx+26, cy+20+body_bob+arm_swing[1]),
        (cx+24, cy+34+body_bob+arm_swing[1]), (cx+16, cy+28+body_bob)
    ], fill=p["piel"])

    # Piernas
    lo = [(0, 0), (6, -2), (0, -4), (-6, -2)][frame % 4] if direction == "walk" else (0, 0)
    d.rounded_rectangle([cx-12, cy+40+body_bob, cx+2, cy+54+body_bob], radius=4, fill=p["pantalon"])
    d.rounded_rectangle([cx+6, cy+40+body_bob, cx+20, cy+54+body_bob+lo[1]], radius=4, fill=p["pantalon"])
    d.rounded_rectangle([cx-14, cy+50+body_bob, cx+1, cy+57+body_bob], radius=3, fill=p["botas"])
    d.rounded_rectangle([cx+5, cy+50+body_bob+lo[1], cx+22, cy+57+body_bob+lo[1]], radius=3, fill=p["botas"])

    # Cabeza
    head_y = cy - 20 + body_bob
    d.ellipse([cx-24, head_y-22, cx+22, head_y+22], fill=p["piel"])
    d.ellipse([cx-26, head_y-24, cx+24, head_y+6], fill=p["pelo"])
    d.ellipse([cx-26, head_y-24, cx+24, head_y-2], fill=p["pelo_osc"])

    big_eye(d, cx-6, head_y+2, 10)
    if frame == 1 and direction == "idle":
        big_eye_closed(d, cx-6, head_y, 10)
    d.arc([cx-18, head_y+6, cx+6, head_y+14], 0, 180, fill=p["boca"], width=3)
    blush(d, cx-4, head_y, p["rosa"]+(100,))

    # Capucha
    if facing_right:
        d.arc([cx-30, head_y-18, cx+20, head_y+10], 180, 360, fill=p["capa"], width=4)
    else:
        d.arc([cx-20, head_y-18, cx+30, head_y+10], 180, 360, fill=p["capa"], width=4)

def prota_idle(direction, frame):
    im = new_img()
    d = ImageDraw.Draw(im)
    cx, cy = SIZE//2, 60

    if direction == "down":
        _prota_cuerpo(d, cx, cy, frame, "idle")
        _prota_cabeza(d, cx, cy, frame, "idle")
    elif direction == "up":
        _prota_cuerpo(d, cx, cy, frame, "idle")
        _prota_cabeza(d, cx, cy, frame, "idle")
    elif direction == "left":
        _prota_side(d, cx, cy, frame, "idle", False)
    elif direction == "right":
        _prota_side(d, cx, cy, frame, "idle", True)

    return im

def prota_walk(direction, frame):
    im = new_img()
    d = ImageDraw.Draw(im)
    cx, cy = SIZE//2, 60

    if direction == "down":
        _prota_cuerpo(d, cx, cy, frame, "walk")
        _prota_cabeza(d, cx, cy, frame, "walk")
    elif direction == "up":
        _prota_cuerpo(d, cx, cy, frame, "walk")
        _prota_cabeza(d, cx, cy, frame, "walk")
    elif direction == "left":
        _prota_side(d, cx, cy, frame, "walk", False)
    elif direction == "right":
        _prota_side(d, cx, cy, frame, "walk", True)

    return im

# ── TORTUGA ──────────────────────────────────────────────────

TORTUGA = {
    "caparazon": (139,111,71),
    "cap_osc":   (110,85,55),
    "cap_claro": (160,130,90),
    "piel":      (126,200,160),
    "piel_osc":  (90,160,120),
    "bufanda":   (240,192,96),
    "buf_osc":   (200,155,70),
    "ojo":       (45,45,45),
    "antcojos":  (240,192,96),
}

def tortuga_idle(frame):
    im = new_img()
    d = ImageDraw.Draw(im)
    cx, cy = 64, 58

    # Sombra
    d.ellipse([cx-40, cy+48, cx+40, cy+58], fill=(0,0,0,30))

    # Caparazón
    breathe = [0, -2, 1, 0][frame % 3]
    d.ellipse([cx-38, cy-10+breathe, cx+38, cy+44+breathe], fill=TORTUGA["caparazon"])
    # Patrón de hexágonos / espiral en el caparazón
    d.ellipse([cx-30, cy-4+breathe, cx+30, cy+38+breathe], fill=TORTUGA["cap_osc"])
    d.ellipse([cx-22, cy+2+breathe, cx+22, cy+32+breathe], fill=TORTUGA["caparazon"])
    d.ellipse([cx-14, cy+8+breathe, cx+14, cy+26+breathe], fill=TORTUGA["cap_osc"])
    d.ellipse([cx-7, cy+13+breathe, cx+7, cy+22+breathe], fill=TORTUGA["caparazon"])

    # Cuerpo / piel base (asomando por abajo)
    d.ellipse([cx-28, cy+36+breathe, cx+28, cy+52+breathe], fill=TORTUGA["piel"])

    # Patas
    pwalk = [(0,0), (-3,1), (0,2), (3,1)][frame % 3]
    d.ellipse([cx-36, cy+38+pwalk[0], cx-20, cy+50+pwalk[0]], fill=TORTUGA["piel"])
    d.ellipse([cx+20, cy+38+pwalk[1], cx+36, cy+50+pwalk[1]], fill=TORTUGA["piel"])
    d.ellipse([cx-32, cy+46, cx-16, cy+55], fill=TORTUGA["piel_osc"])
    d.ellipse([cx+16, cy+46, cx+32, cy+55], fill=TORTUGA["piel_osc"])

    # Cabeza
    head_y = cy - 22 + breathe
    d.ellipse([cx-24, head_y-18, cx+24, head_y+18], fill=TORTUGA["piel"])

    # Parte superior cabeza más oscura
    d.ellipse([cx-22, head_y-18, cx+22, head_y-2], fill=TORTUGA["piel_osc"]+(100,))

    # Bufanda
    d.ellipse([cx-26, head_y+6, cx+26, head_y+20], fill=TORTUGA["bufanda"])
    d.ellipse([cx-24, head_y+8, cx+24, head_y+18], fill=TORTUGA["buf_osc"])
    # Bufanda colgando
    d.polygon([
        (cx-26, head_y+12), (cx-32, head_y+14),
        (cx-30, head_y+28), (cx-24, head_y+26)
    ], fill=TORTUGA["bufanda"])
    d.polygon([
        (cx+26, head_y+12), (cx+32, head_y+14),
        (cx+30, head_y+28), (cx+24, head_y+26)
    ], fill=TORTUGA["bufanda"])

    # Anteojos redondos
    d.ellipse([cx-18, head_y-8, cx-2, head_y+6], fill=None, outline=TORTUGA["antcojos"], width=3)
    d.ellipse([cx+2, head_y-8, cx+18, head_y+6], fill=None, outline=TORTUGA["antcojos"], width=3)
    d.line([cx-2, head_y-2, cx+2, head_y-2], fill=TORTUGA["antcojos"], width=3)

    # Ojos grandes y cálidos
    big_eye(d, cx-10, head_y, 7)
    big_eye(d, cx+10, head_y, 7)

    # Sonrisa paciente
    d.arc([cx-8, head_y+6, cx+8, head_y+14], 0, 180, fill=(60,40,20), width=2)

    # Blush
    blush(d, cx, head_y, (126,200,160,60))

    return im

def tortuga_walk(frame):
    im = new_img()
    d = ImageDraw.Draw(im)
    cx, cy = 64, 58

    d.ellipse([cx-40, cy+48, cx+40, cy+58], fill=(0,0,0,30))

    # Caminar: balanceo lento
    sway = [0, -3, 0, 3][frame % 4]
    lift = [0, -2, -4, -2][frame % 4]

    d.ellipse([cx-38, cy-10+lift, cx+38, cy+44+lift], fill=TORTUGA["caparazon"])
    d.ellipse([cx-30, cy-4+lift, cx+30, cy+38+lift], fill=TORTUGA["cap_osc"])
    d.ellipse([cx-22, cy+2+lift, cx+22, cy+32+lift], fill=TORTUGA["caparazon"])
    d.ellipse([cx-14, cy+8+lift, cx+14, cy+26+lift], fill=TORTUGA["cap_osc"])

    d.ellipse([cx-28, cy+36+lift, cx+28, cy+52+lift], fill=TORTUGA["piel"])

    # Patas caminando
    leg_pattern = [
        (-4, 4), (-2, -2), (4, -4), (2, 2)
    ]
    lp = leg_pattern[frame % 4]
    d.ellipse([cx-36+lp[0], cy+38, cx-20+lp[0], cy+50], fill=TORTUGA["piel"])
    d.ellipse([cx+20+lp[1], cy+38, cx+36+lp[1], cy+50], fill=TORTUGA["piel"])

    head_y = cy - 22 + lift
    d.ellipse([cx-24, head_y-18, cx+24, head_y+18], fill=TORTUGA["piel"])
    d.ellipse([cx-22, head_y-18, cx+22, head_y-2], fill=TORTUGA["piel_osc"]+(100,))

    # Bufanda ondeante
    scarf_sway = [0, 2, 4, 2][frame % 4]
    d.ellipse([cx-26, head_y+6, cx+26, head_y+20], fill=TORTUGA["bufanda"])
    d.ellipse([cx-24, head_y+8, cx+24, head_y+18], fill=TORTUGA["buf_osc"])
    d.polygon([
        (cx-26, head_y+12), (cx-32-scarf_sway, head_y+14),
        (cx-30-scarf_sway, head_y+28), (cx-24, head_y+26)
    ], fill=TORTUGA["bufanda"])
    d.polygon([
        (cx+26, head_y+12), (cx+32+scarf_sway, head_y+14),
        (cx+30+scarf_sway, head_y+28), (cx+24, head_y+26)
    ], fill=TORTUGA["bufanda"])

    d.ellipse([cx-18, head_y-8, cx-2, head_y+6], fill=None, outline=TORTUGA["antcojos"], width=3)
    d.ellipse([cx+2, head_y-8, cx+18, head_y+6], fill=None, outline=TORTUGA["antcojos"], width=3)
    d.line([cx-2, head_y-2, cx+2, head_y-2], fill=TORTUGA["antcojos"], width=3)

    big_eye(d, cx-10, head_y, 7)
    big_eye(d, cx+10, head_y, 7)
    d.arc([cx-8, head_y+6, cx+8, head_y+14], 0, 180, fill=(60,40,20), width=2)
    blush(d, cx, head_y, (126,200,160,60))

    return im

def tortuga_talk(frame):
    im = new_img()
    d = ImageDraw.Draw(im)
    cx, cy = 64, 58

    breathe = [0, -1][frame % 2]

    d.ellipse([cx-40, cy+48, cx+40, cy+58], fill=(0,0,0,30))
    d.ellipse([cx-38, cy-10+breathe, cx+38, cy+44+breathe], fill=TORTUGA["caparazon"])
    d.ellipse([cx-30, cy-4+breathe, cx+30, cy+38+breathe], fill=TORTUGA["cap_osc"])
    d.ellipse([cx-22, cy+2+breathe, cx+22, cy+32+breathe], fill=TORTUGA["caparazon"])
    d.ellipse([cx-14, cy+8+breathe, cx+14, cy+26+breathe], fill=TORTUGA["cap_osc"])

    d.ellipse([cx-28, cy+36+breathe, cx+28, cy+52+breathe], fill=TORTUGA["piel"])
    d.ellipse([cx-36, cy+38, cx-20, cy+50], fill=TORTUGA["piel"])
    d.ellipse([cx+20, cy+38, cx+36, cy+50], fill=TORTUGA["piel"])

    head_y = cy - 22 + breathe
    d.ellipse([cx-24, head_y-18, cx+24, head_y+18], fill=TORTUGA["piel"])
    d.ellipse([cx-22, head_y-18, cx+22, head_y-2], fill=TORTUGA["piel_osc"]+(100,))

    d.ellipse([cx-26, head_y+6, cx+26, head_y+20], fill=TORTUGA["bufanda"])
    d.ellipse([cx-24, head_y+8, cx+24, head_y+18], fill=TORTUGA["buf_osc"])

    d.ellipse([cx-18, head_y-8, cx-2, head_y+6], fill=None, outline=TORTUGA["antcojos"], width=3)
    d.ellipse([cx+2, head_y-8, cx+18, head_y+6], fill=None, outline=TORTUGA["antcojos"], width=3)
    d.line([cx-2, head_y-2, cx+2, head_y-2], fill=TORTUGA["antcojos"], width=3)

    big_eye(d, cx-10, head_y, 7)
    big_eye(d, cx+10, head_y, 7)

    # Boca abierta (hablando)
    mouth_h = [4, 8][frame % 2]
    d.ellipse([cx-7, head_y+8, cx+7, head_y+8+mouth_h], fill=(50,30,20))
    d.ellipse([cx-6, head_y+9, cx+6, head_y+9+mouth_h-1], fill=(200,80,80))

    blush(d, cx, head_y, (126,200,160,60))

    return im

# ── ZORRO ────────────────────────────────────────────────────

ZORRO = {
    "naranja":  (232,168,74),
    "naranja_osc": (190,130,50),
    "blanco":   (255,245,240),
    "gris":     (200,190,185),
    "ojo":      (45,52,54),
    "nariz":    (30,30,30),
    "boca":     (180,100,80),
    "oreja_int":(255,220,200),
}

def zorro_idle(frame):
    im = new_img()
    d = ImageDraw.Draw(im)
    cx, cy = 64, 56

    d.ellipse([cx-36, cy+48, cx+36, cy+56], fill=(0,0,0,30))

    breathe = [0, -2, 1][frame % 3]

    # Cola esponjosa
    tail_swish = [0, 3, 6][frame % 3]
    d.ellipse([cx+20, cy+12+tail_swish, cx+52, cy+44+tail_swish], fill=ZORRO["naranja"])
    d.ellipse([cx+36, cy+14+tail_swish, cx+50, cy+30+tail_swish], fill=ZORRO["blanco"])

    # Cuerpo
    d.ellipse([cx-24, cy-4+breathe, cx+24, cy+36+breathe], fill=ZORRO["naranja"])
    # Vientre blanco
    d.ellipse([cx-16, cy+4+breathe, cx+16, cy+32+breathe], fill=ZORRO["blanco"])

    # Brazos / patas delanteras
    d.ellipse([cx-28, cy+28, cx-14, cy+44], fill=ZORRO["naranja"])
    d.ellipse([cx+14, cy+28, cx+28, cy+44], fill=ZORRO["naranja"])
    d.ellipse([cx-26, cy+40, cx-12, cy+50], fill=ZORRO["gris"])
    d.ellipse([cx+12, cy+40, cx+26, cy+50], fill=ZORRO["gris"])

    # Piernas traseras
    d.ellipse([cx-22, cy+34, cx-10, cy+48], fill=ZORRO["naranja_osc"])
    d.ellipse([cx+10, cy+34, cx+22, cy+48], fill=ZORRO["naranja_osc"])

    # Cabeza
    head_y = cy - 28 + breathe
    d.ellipse([cx-26, head_y-18, cx+26, head_y+20], fill=ZORRO["naranja"])
    # Hocico blanco
    d.polygon([
        (cx-14, head_y+6), (cx, head_y+20), (cx+14, head_y+6)
    ], fill=ZORRO["blanco"])
    # Mejillas blancas
    d.ellipse([cx-24, head_y-4, cx-8, head_y+8], fill=ZORRO["blanco"])
    d.ellipse([cx+8, head_y-4, cx+24, head_y+8], fill=ZORRO["blanco"])

    # Orejas triangulares grandes
    d.polygon([
        (cx-22, head_y-14), (cx-30, head_y-32), (cx-12, head_y-20)
    ], fill=ZORRO["naranja"])
    d.polygon([
        (cx+22, head_y-14), (cx+30, head_y-32), (cx+12, head_y-20)
    ], fill=ZORRO["naranja"])
    # Interior orejas
    d.polygon([
        (cx-20, head_y-15), (cx-27, head_y-28), (cx-14, head_y-20)
    ], fill=ZORRO["oreja_int"])
    d.polygon([
        (cx+20, head_y-15), (cx+27, head_y-28), (cx+14, head_y-20)
    ], fill=ZORRO["oreja_int"])

    # Ojos almendrados
    d.ellipse([cx-16, head_y-2, cx-4, head_y+8], fill=ZORRO["blanco"])
    d.ellipse([cx+4, head_y-2, cx+16, head_y+8], fill=ZORRO["blanco"])
    d.ellipse([cx-13, head_y+1, cx-7, head_y+6], fill=ZORRO["ojo"])
    d.ellipse([cx+7, head_y+1, cx+13, head_y+6], fill=ZORRO["ojo"])
    d.ellipse([cx-11, head_y+2, cx-9, head_y+4], fill=(255,255,255,180))
    d.ellipse([cx+9, head_y+2, cx+11, head_y+4], fill=(255,255,255,180))

    # Nariz
    d.ellipse([cx-4, head_y+9, cx+4, head_y+14], fill=ZORRO["nariz"])

    # Sonrisa astuta
    d.arc([cx-8, head_y+11, cx+8, head_y+18], 0, 180, fill=ZORRO["boca"], width=2)

    # Cejas
    d.arc([cx-20, head_y-8, cx-4, head_y-2], 200, 360, fill=ZORRO["naranja_osc"], width=3)
    d.arc([cx+4, head_y-8, cx+20, head_y-2], 180, 340, fill=ZORRO["naranja_osc"], width=3)

    return im

def zorro_walk(frame):
    im = new_img()
    d = ImageDraw.Draw(im)
    cx, cy = 64, 56

    d.ellipse([cx-36, cy+48, cx+36, cy+56], fill=(0,0,0,30))

    lift = [0, -2, -3, -1][frame % 4]
    leg_swing = [(-4, 4), (0, 0), (4, -4), (0, 0)][frame % 4]

    tail_swish = [0, 4, 8, 4][frame % 4]
    d.ellipse([cx+20, cy+12+tail_swish, cx+52, cy+44+tail_swish], fill=ZORRO["naranja"])
    d.ellipse([cx+36, cy+14+tail_swish, cx+50, cy+30+tail_swish], fill=ZORRO["blanco"])

    d.ellipse([cx-24, cy-4+lift, cx+24, cy+36+lift], fill=ZORRO["naranja"])
    d.ellipse([cx-16, cy+4+lift, cx+16, cy+32+lift], fill=ZORRO["blanco"])

    d.ellipse([cx-28+leg_swing[0], cy+28, cx-14+leg_swing[0], cy+44], fill=ZORRO["naranja"])
    d.ellipse([cx+14+leg_swing[1], cy+28, cx+28+leg_swing[1], cy+44], fill=ZORRO["naranja"])

    head_y = cy - 28 + lift
    d.ellipse([cx-26, head_y-18, cx+26, head_y+20], fill=ZORRO["naranja"])
    d.polygon([(cx-14, head_y+6), (cx, head_y+20), (cx+14, head_y+6)], fill=ZORRO["blanco"])
    d.ellipse([cx-24, head_y-4, cx-8, head_y+8], fill=ZORRO["blanco"])
    d.ellipse([cx+8, head_y-4, cx+24, head_y+8], fill=ZORRO["blanco"])

    d.polygon([(cx-22, head_y-14), (cx-30, head_y-32), (cx-12, head_y-20)], fill=ZORRO["naranja"])
    d.polygon([(cx+22, head_y-14), (cx+30, head_y-32), (cx+12, head_y-20)], fill=ZORRO["naranja"])
    d.polygon([(cx-20, head_y-15), (cx-27, head_y-28), (cx-14, head_y-20)], fill=ZORRO["oreja_int"])
    d.polygon([(cx+20, head_y-15), (cx+27, head_y-28), (cx+14, head_y-20)], fill=ZORRO["oreja_int"])

    d.ellipse([cx-16, head_y-2, cx-4, head_y+8], fill=ZORRO["blanco"])
    d.ellipse([cx+4, head_y-2, cx+16, head_y+8], fill=ZORRO["blanco"])
    d.ellipse([cx-13, head_y+1, cx-7, head_y+6], fill=ZORRO["ojo"])
    d.ellipse([cx+7, head_y+1, cx+13, head_y+6], fill=ZORRO["ojo"])
    d.ellipse([cx-11, head_y+2, cx-9, head_y+4], fill=(255,255,255,180))
    d.ellipse([cx+9, head_y+2, cx+11, head_y+4], fill=(255,255,255,180))

    d.ellipse([cx-4, head_y+9, cx+4, head_y+14], fill=ZORRO["nariz"])
    d.arc([cx-8, head_y+11, cx+8, head_y+18], 0, 180, fill=ZORRO["boca"], width=2)

    return im

def zorro_talk(frame):
    im = new_img()
    d = ImageDraw.Draw(im)
    cx, cy = 64, 56

    d.ellipse([cx-36, cy+48, cx+36, cy+56], fill=(0,0,0,30))

    breathe = [0, -1][frame % 2]

    d.ellipse([cx+20, cy+12, cx+52, cy+44], fill=ZORRO["naranja"])
    d.ellipse([cx+36, cy+14, cx+50, cy+30], fill=ZORRO["blanco"])
    d.ellipse([cx-24, cy-4+breathe, cx+24, cy+36+breathe], fill=ZORRO["naranja"])
    d.ellipse([cx-16, cy+4+breathe, cx+16, cy+32+breathe], fill=ZORRO["blanco"])
    d.ellipse([cx-28, cy+28, cx-14, cy+44], fill=ZORRO["naranja"])
    d.ellipse([cx+14, cy+28, cx+28, cy+44], fill=ZORRO["naranja"])

    head_y = cy - 28 + breathe
    d.ellipse([cx-26, head_y-18, cx+26, head_y+20], fill=ZORRO["naranja"])
    d.polygon([(cx-14, head_y+6), (cx, head_y+20), (cx+14, head_y+6)], fill=ZORRO["blanco"])
    d.ellipse([cx-24, head_y-4, cx-8, head_y+8], fill=ZORRO["blanco"])
    d.ellipse([cx+8, head_y-4, cx+24, head_y+8], fill=ZORRO["blanco"])

    d.polygon([(cx-22, head_y-14), (cx-30, head_y-32), (cx-12, head_y-20)], fill=ZORRO["naranja"])
    d.polygon([(cx+22, head_y-14), (cx+30, head_y-32), (cx+12, head_y-20)], fill=ZORRO["naranja"])
    d.polygon([(cx-20, head_y-15), (cx-27, head_y-28), (cx-14, head_y-20)], fill=ZORRO["oreja_int"])
    d.polygon([(cx+20, head_y-15), (cx+27, head_y-28), (cx+14, head_y-20)], fill=ZORRO["oreja_int"])

    d.ellipse([cx-16, head_y-2, cx-4, head_y+8], fill=ZORRO["blanco"])
    d.ellipse([cx+4, head_y-2, cx+16, head_y+8], fill=ZORRO["blanco"])
    d.ellipse([cx-13, head_y+1, cx-7, head_y+6], fill=ZORRO["ojo"])
    d.ellipse([cx+7, head_y+1, cx+13, head_y+6], fill=ZORRO["ojo"])

    d.ellipse([cx-4, head_y+9, cx+4, head_y+14], fill=ZORRO["nariz"])

    # Boca hablando
    mouth_h = [4, 8][frame % 2]
    d.ellipse([cx-6, head_y+12, cx+6, head_y+12+mouth_h], fill=(40,20,20))
    d.ellipse([cx-5, head_y+13, cx+5, head_y+13+mouth_h-1], fill=(200,80,80))

    return im

# ── BÚHO ─────────────────────────────────────────────────────

BUHO = {
    "marron":    (139,111,71),
    "marron_osc":(110,85,55),
    "vientre":   (212,196,160),
    "antcojos":  (240,192,96),
    "ojos":      (255,240,180),
    "pupila":    (40,40,40),
    "pico":      (230,160,60),
    "patas":     (200,140,50),
    "blanco":    (240,230,210),
}

def buho_idle(frame):
    im = new_img()
    d = ImageDraw.Draw(im)
    cx, cy = 64, 56

    d.ellipse([cx-36, cy+44, cx+36, cy+54], fill=(0,0,0,30))

    breathe = [0, -2, 1][frame % 3]

    # Cuerpo redondo
    d.ellipse([cx-32, cy-10+breathe, cx+32, cy+40+breathe], fill=BUHO["marron"])

    # Vientre beige
    d.ellipse([cx-22, cy-2+breathe, cx+22, cy+36+breathe], fill=BUHO["vientre"])

    # Plumas textura
    for i in range(3):
        py = cy + 6 + i*8 + breathe
        d.arc([cx-18, py-2, cx-6, py+4], 180, 360, fill=BUHO["marron_osc"], width=2)
        d.arc([cx+6, py-2, cx+18, py+4], 180, 360, fill=BUHO["marron_osc"], width=2)

    # Plumas de "orejas" (tufts)
    d.polygon([
        (cx-28, cy-14+breathe), (cx-34, cy-30+breathe), (cx-22, cy-20+breathe)
    ], fill=BUHO["marron"])
    d.polygon([
        (cx+28, cy-14+breathe), (cx+34, cy-30+breathe), (cx+22, cy-20+breathe)
    ], fill=BUHO["marron"])
    d.polygon([
        (cx-26, cy-15+breathe), (cx-31, cy-27+breathe), (cx-23, cy-20+breathe)
    ], fill=BUHO["marron_osc"])
    d.polygon([
        (cx+26, cy-15+breathe), (cx+31, cy-27+breathe), (cx+23, cy-20+breathe)
    ], fill=BUHO["marron_osc"])

    # Alas
    d.ellipse([cx-40, cy-4+breathe, cx-28, cy+26+breathe], fill=BUHO["marron_osc"])
    d.ellipse([cx+28, cy-4+breathe, cx+40, cy+26+breathe], fill=BUHO["marron_osc"])

    # Cabeza
    head_y = cy - 18 + breathe
    d.ellipse([cx-28, head_y-20, cx+28, head_y+16], fill=BUHO["marron"])
    d.ellipse([cx-26, head_y-18, cx+26, head_y+14], fill=BUHO["vientre"])

    # Ojos grandes con anteojos
    # Círculo ocular
    d.ellipse([cx-22, head_y-10, cx-2, head_y+8], fill=BUHO["ojos"])
    d.ellipse([cx+2, head_y-10, cx+22, head_y+8], fill=BUHO["ojos"])
    # Pupilas grandes
    pupila_offset = [0, 2, -2][frame % 3]
    d.ellipse([cx-15+pupila_offset, head_y-4, cx-9+pupila_offset, head_y+2], fill=BUHO["pupila"])
    d.ellipse([cx+9+pupila_offset, head_y-4, cx+15+pupila_offset, head_y+2], fill=BUHO["pupila"])
    d.ellipse([cx-13+pupila_offset, head_y-3, cx-11+pupila_offset, head_y-1], fill=(255,255,255,180))
    d.ellipse([cx+11+pupila_offset, head_y-3, cx+13+pupila_offset, head_y-1], fill=(255,255,255,180))

    # Anteojos redondos dorados
    d.ellipse([cx-22, head_y-10, cx-2, head_y+8], fill=None, outline=BUHO["antcojos"], width=3)
    d.ellipse([cx+2, head_y-10, cx+22, head_y+8], fill=None, outline=BUHO["antcojos"], width=3)
    d.line([cx-2, head_y-2, cx+2, head_y-2], fill=BUHO["antcojos"], width=3)

    # Cejas expresivas
    d.arc([cx-26, head_y-16, cx-4, head_y-8], 200, 360, fill=BUHO["marron_osc"], width=3)
    d.arc([cx+4, head_y-16, cx+26, head_y-8], 180, 340, fill=BUHO["marron_osc"], width=3)

    # Pico
    d.polygon([(cx-5, head_y+4), (cx+5, head_y+4), (cx, head_y+12)], fill=BUHO["pico"])
    d.polygon([(cx-3, head_y+5), (cx+3, head_y+5), (cx, head_y+10)], fill=(255,200,100))

    # Patas
    d.line([cx-12, cy+40+breathe, cx-16, cy+50+breathe], fill=BUHO["patas"], width=4)
    d.line([cx+12, cy+40+breathe, cx+16, cy+50+breathe], fill=BUHO["patas"], width=4)
    d.line([cx-16, cy+50+breathe, cx-20, cy+52+breathe], fill=BUHO["patas"], width=3)
    d.line([cx-16, cy+50+breathe, cx-14, cy+52+breathe], fill=BUHO["patas"], width=3)
    d.line([cx+16, cy+50+breathe, cx+12, cy+52+breathe], fill=BUHO["patas"], width=3)
    d.line([cx+16, cy+50+breathe, cx+20, cy+52+breathe], fill=BUHO["patas"], width=3)

    return im

def buho_walk(frame):
    im = new_img()
    d = ImageDraw.Draw(im)
    cx, cy = 64, 56

    d.ellipse([cx-36, cy+44, cx+36, cy+54], fill=(0,0,0,30))

    lift = [0, -2, -4, -2][frame % 4]
    leg_pattern = [
        (-4, 4), (0, 0), (4, -4), (0, 0)
    ]
    lp = leg_pattern[frame % 4]

    d.ellipse([cx-32, cy-10+lift, cx+32, cy+40+lift], fill=BUHO["marron"])
    d.ellipse([cx-22, cy-2+lift, cx+22, cy+36+lift], fill=BUHO["vientre"])

    d.ellipse([cx-40, cy-4+lift, cx-28, cy+26+lift], fill=BUHO["marron_osc"])
    d.ellipse([cx+28, cy-4+lift, cx+40, cy+26+lift], fill=BUHO["marron_osc"])

    head_y = cy - 18 + lift
    d.ellipse([cx-28, head_y-20, cx+28, head_y+16], fill=BUHO["marron"])
    d.ellipse([cx-26, head_y-18, cx+26, head_y+14], fill=BUHO["vientre"])

    d.ellipse([cx-22, head_y-10, cx-2, head_y+8], fill=BUHO["ojos"])
    d.ellipse([cx+2, head_y-10, cx+22, head_y+8], fill=BUHO["ojos"])
    d.ellipse([cx-13, head_y-4, cx-9, head_y+2], fill=BUHO["pupila"])
    d.ellipse([cx+9, head_y-4, cx+13, head_y+2], fill=BUHO["pupila"])

    d.ellipse([cx-22, head_y-10, cx-2, head_y+8], fill=None, outline=BUHO["antcojos"], width=3)
    d.ellipse([cx+2, head_y-10, cx+22, head_y+8], fill=None, outline=BUHO["antcojos"], width=3)
    d.line([cx-2, head_y-2, cx+2, head_y-2], fill=BUHO["antcojos"], width=3)

    d.polygon([(cx-5, head_y+4), (cx+5, head_y+4), (cx, head_y+12)], fill=BUHO["pico"])

    # Patas caminando
    d.line([cx-12+lp[0], cy+40+lift, cx-16+lp[0], cy+50+lift], fill=BUHO["patas"], width=4)
    d.line([cx+12+lp[1], cy+40+lift, cx+16+lp[1], cy+50+lift], fill=BUHO["patas"], width=4)

    return im

# ── MARIPOSA ─────────────────────────────────────────────────

MARIPOSA = {
    "azul":     (74,144,217),
    "azul_claro": (126,200,227),
    "azul_osc": (50,110,180),
    "dorado":   (240,192,96),
    "cuerpo":   (60,60,70),
    "brillo":   (255,240,180),
}

def mariposa_idle(frame):
    im = new_img()
    d = ImageDraw.Draw(im)
    cx, cy = 64, 60

    # Partículas brillantes
    for _ in range(12):
        px = random.randint(8, 120)
        py = random.randint(8, 120)
        alpha = random.randint(40, 120)
        size = random.choice([2, 3, 4])
        d.ellipse([px-size//2, py-size//2, px+size//2, py+size//2],
                  fill=MARIPOSA["dorado"]+(alpha,))

    # Batido de alas
    wing_angle = [0, 8, 4][frame % 3]
    wing_lift = [0, -4, -2][frame % 3]

    # Ala izquierda superior
    d.ellipse([
        cx-48-wing_angle, cy-18+wing_lift, cx-8, cy+8+wing_lift
    ], fill=MARIPOSA["azul"]+(220,))
    d.ellipse([
        cx-44-wing_angle, cy-14+wing_lift, cx-12, cy+4+wing_lift
    ], fill=MARIPOSA["azul_claro"]+(200,))

    # Ala derecha superior
    d.ellipse([
        cx+8, cy-18+wing_lift, cx+48+wing_angle, cy+8+wing_lift
    ], fill=MARIPOSA["azul"]+(220,))
    d.ellipse([
        cx+12, cy-14+wing_lift, cx+44+wing_angle, cy+4+wing_lift
    ], fill=MARIPOSA["azul_claro"]+(200,))

    # Patrones dorados en alas
    d.ellipse([cx-32, cy-10+wing_lift, cx-20, cy+2+wing_lift],
              fill=MARIPOSA["dorado"]+(150,))
    d.ellipse([cx+20, cy-10+wing_lift, cx+32, cy+2+wing_lift],
              fill=MARIPOSA["dorado"]+(150,))

    # Venas de alas
    for angle in [-30, 0, 30]:
        rad = math.radians(angle)
        dx = int(20 * math.cos(rad))
        dy = int(20 * math.sin(rad))
        d.line([cx-10, cy-4+wing_lift, cx-10-dx, cy-8+wing_lift+dy],
               fill=MARIPOSA["azul_osc"]+(100,), width=2)
        d.line([cx+10, cy-4+wing_lift, cx+10+dx, cy-8+wing_lift+dy],
               fill=MARIPOSA["azul_osc"]+(100,), width=2)

    # Ala inferior izquierda
    d.ellipse([
        cx-32, cy+4+wing_lift, cx-4, cy+22+wing_lift
    ], fill=MARIPOSA["azul_claro"]+(180,))

    # Ala inferior derecha
    d.ellipse([
        cx+4, cy+4+wing_lift, cx+32, cy+22+wing_lift
    ], fill=MARIPOSA["azul_claro"]+(180,))

    # Cuerpo
    d.ellipse([cx-6, cy-10, cx+6, cy+24], fill=MARIPOSA["cuerpo"])
    d.ellipse([cx-4, cy-6, cx+4, cy+20], fill=(80,80,90))

    # Cabeza
    d.ellipse([cx-8, cy-18, cx+8, cy-6], fill=MARIPOSA["cuerpo"])
    d.ellipse([cx-6, cy-16, cx+6, cy-8], fill=(80,80,90))

    # Ojos grandes
    d.ellipse([cx-6, cy-14, cx-2, cy-10], fill=(255,255,255))
    d.ellipse([cx+2, cy-14, cx+6, cy-10], fill=(255,255,255))
    d.ellipse([cx-5, cy-13, cx-3, cy-11], fill=(20,20,30))
    d.ellipse([cx+3, cy-13, cx+5, cy-11], fill=(20,20,30))

    # Antenas curvas
    d.arc([cx-14, cy-34, cx-2, cy-18], 180, 360, fill=MARIPOSA["cuerpo"], width=2)
    d.arc([cx+2, cy-34, cx+14, cy-18], 180, 360, fill=MARIPOSA["cuerpo"], width=2)
    d.ellipse([cx-12, cy-34, cx-8, cy-30], fill=MARIPOSA["dorado"])
    d.ellipse([cx+8, cy-34, cx+12, cy-30], fill=MARIPOSA["dorado"])

    return im

# ── CARACOL ──────────────────────────────────────────────────

CARACOL = {
    "caparazon":    (201,168,232),
    "cap_osc":      (170,135,205),
    "cap_claro":    (220,195,240),
    "cuerpo":       (126,200,160),
    "cuerpo_osc":   (90,160,120),
    "rastro":       (180,220,190,80),
    "ojo":          (40,40,40),
    "mejilla":      (200,150,180,60),
}

def caracol_idle(frame):
    im = new_img()
    d = ImageDraw.Draw(im)
    cx, cy = 62, 58

    breathe = [0, -1, 1][frame % 3]

    # Rastro brillante
    d.ellipse([cx-50, cy+46, cx-10, cy+56], fill=CARACOL["rastro"])
    d.ellipse([cx-40, cy+48, cx-20, cy+54], fill=(200,230,200,60))

    # Cuerpo
    d.ellipse([cx-32, cy+14+breathe, cx+20, cy+48+breathe], fill=CARACOL["cuerpo"])
    d.ellipse([cx-28, cy+18+breathe, cx+16, cy+44+breathe], fill=CARACOL["cuerpo_osc"]+(100,))

    # Caparazón en espiral
    d.ellipse([cx-24, cy-24+breathe, cx+28, cy+20+breathe], fill=CARACOL["caparazon"])
    # Espiral
    d.ellipse([cx-18, cy-18+breathe, cx+22, cy+14+breathe], fill=CARACOL["cap_osc"])
    d.ellipse([cx-12, cy-12+breathe, cx+16, cy+8+breathe], fill=CARACOL["caparazon"])
    d.ellipse([cx-6, cy-6+breathe, cx+10, cy+2+breathe], fill=CARACOL["cap_osc"])
    d.ellipse([cx-2, cy-2+breathe, cx+6, cy+0+breathe], fill=CARACOL["cap_claro"])

    # Destellos en caparazón
    d.ellipse([cx+12, cy-16+breathe, cx+18, cy-10+breathe],
              fill=(255,255,255,40))
    d.ellipse([cx-14, cy+4+breathe, cx-8, cy+10+breathe],
              fill=(255,255,255,40))

    # Ojos en tallos
    stalk_bob = [0, -2, 2][frame % 3]
    d.line([cx-8, cy-22+breathe, cx-14, cy-38+stalk_bob+breathe],
           fill=CARACOL["cuerpo_osc"], width=3)
    d.line([cx+4, cy-22+breathe, cx+10, cy-38+stalk_bob+breathe],
           fill=CARACOL["cuerpo_osc"], width=3)

    d.ellipse([cx-18, cy-42+stalk_bob+breathe, cx-10, cy-34+stalk_bob+breathe],
              fill=CARACOL["cuerpo"])
    d.ellipse([cx+6, cy-42+stalk_bob+breathe, cx+14, cy-34+stalk_bob+breathe],
              fill=CARACOL["cuerpo"])
    d.ellipse([cx-16, cy-40+stalk_bob+breathe, cx-12, cy-36+stalk_bob+breathe],
              fill=CARACOL["ojo"])
    d.ellipse([cx+8, cy-40+stalk_bob+breathe, cx+12, cy-36+stalk_bob+breathe],
              fill=CARACOL["ojo"])
    d.ellipse([cx-15, cy-39+stalk_bob+breathe, cx-13, cy-37+stalk_bob+breathe],
              fill=(255,255,255,180))
    d.ellipse([cx+9, cy-39+stalk_bob+breathe, cx+11, cy-37+stalk_bob+breathe],
              fill=(255,255,255,180))

    # Carita (sonrisa tímida)
    d.arc([cx-12, cy+16+breathe, cx-2, cy+24+breathe], 0, 180, fill=(60,40,20), width=2)
    d.arc([cx+2, cy+16+breathe, cx+12, cy+24+breathe], 0, 180, fill=(60,40,20), width=2)
    blush(d, cx-2, cy+12+breathe, CARACOL["mejilla"])

    # Pie (base del cuerpo)
    d.ellipse([cx-36, cy+40+breathe, cx+24, cy+52+breathe], fill=CARACOL["cuerpo_osc"])

    return im

def caracol_walk(frame):
    im = new_img()
    d = ImageDraw.Draw(im)
    cx, cy = 62, 58

    # Movimiento ondulante
    wave = [0, -3, 0, 3][frame % 4]
    lift = [0, -1, -2, -1][frame % 4]

    # Rastro
    trail_len = [0, 4, 8, 12][frame % 4]
    d.ellipse([cx-50-trail_len, cy+46, cx-10-trail_len, cy+56], fill=CARACOL["rastro"])
    d.ellipse([cx-40-trail_len, cy+48, cx-20-trail_len, cy+54], fill=(200,230,200,60))

    d.ellipse([cx-32+wave, cy+14+lift, cx+20+wave, cy+48+lift], fill=CARACOL["cuerpo"])
    d.ellipse([cx-28+wave, cy+18+lift, cx+16+wave, cy+44+lift], fill=CARACOL["cuerpo_osc"]+(100,))

    d.ellipse([cx-24+wave, cy-24+lift, cx+28+wave, cy+20+lift], fill=CARACOL["caparazon"])
    d.ellipse([cx-18+wave, cy-18+lift, cx+22+wave, cy+14+lift], fill=CARACOL["cap_osc"])
    d.ellipse([cx-12+wave, cy-12+lift, cx+16+wave, cy+8+lift], fill=CARACOL["caparazon"])
    d.ellipse([cx-6+wave, cy-6+lift, cx+10+wave, cy+2+lift], fill=CARACOL["cap_osc"])

    stalk_bob = 0
    d.line([cx-8+wave, cy-22+lift, cx-14+wave, cy-38+stalk_bob+lift],
           fill=CARACOL["cuerpo_osc"], width=3)
    d.line([cx+4+wave, cy-22+lift, cx+10+wave, cy-38+stalk_bob+lift],
           fill=CARACOL["cuerpo_osc"], width=3)

    d.ellipse([cx-18+wave, cy-42+stalk_bob+lift, cx-10+wave, cy-34+stalk_bob+lift],
              fill=CARACOL["cuerpo"])
    d.ellipse([cx+6+wave, cy-42+stalk_bob+lift, cx+14+wave, cy-34+stalk_bob+lift],
              fill=CARACOL["cuerpo"])
    d.ellipse([cx-16+wave, cy-40+stalk_bob+lift, cx-12+wave, cy-36+stalk_bob+lift],
              fill=CARACOL["ojo"])
    d.ellipse([cx+8+wave, cy-40+stalk_bob+lift, cx+12+wave, cy-36+stalk_bob+lift],
              fill=CARACOL["ojo"])

    d.arc([cx-12+wave, cy+16+lift, cx-2+wave, cy+24+lift], 0, 180, fill=(60,40,20), width=2)
    d.arc([cx+2+wave, cy+16+lift, cx+12+wave, cy+24+lift], 0, 180, fill=(60,40,20), width=2)

    d.ellipse([cx-36+wave, cy+40+lift, cx+24+wave, cy+52+lift], fill=CARACOL["cuerpo_osc"])

    return im

# ── PÁJARO ───────────────────────────────────────────────────

PAJARO = {
    "amarillo":  (240,192,96),
    "amar_osc":  (200,155,65),
    "pecho":     (232,180,184),
    "pecho_osc": (200,145,150),
    "pico":      (240,160,60),
    "pico_osc":  (200,125,40),
    "ojo":       (40,40,40),
    "ala":       (215,165,75),
    "pata":      (200,140,70),
    "pluma":     (255,200,120),
}

def pajaro_idle(frame):
    im = new_img()
    d = ImageDraw.Draw(im)
    cx, cy = 60, 62

    d.ellipse([cx-30, cy+40, cx+30, cy+50], fill=(0,0,0,25))

    breathe = [0, -2, 1][frame % 3]

    # Cuerpo redondeado
    d.ellipse([cx-24, cy-12+breathe, cx+24, cy+30+breathe], fill=PAJARO["amarillo"])

    # Pecho rosado
    d.ellipse([cx-16, cy-4+breathe, cx+16, cy+26+breathe], fill=PAJARO["pecho"])

    # Ala
    d.ellipse([cx+10, cy-6+breathe, cx+28, cy+16+breathe], fill=PAJARO["ala"])

    # Cola
    d.polygon([
        (cx-20, cy+16+breathe), (cx-32, cy+24+breathe),
        (cx-18, cy+26+breathe), (cx-28, cy+30+breathe),
        (cx-16, cy+28+breathe)
    ], fill=PAJARO["amar_osc"])

    # Patas
    leg_bob = [0, -1, 0][frame % 3]
    d.line([cx-6, cy+30+breathe, cx-8, cy+40+breathe+leg_bob],
           fill=PAJARO["pata"], width=3)
    d.line([cx+6, cy+30+breathe, cx+8, cy+40+breathe+leg_bob],
           fill=PAJARO["pata"], width=3)
    d.line([cx-8, cy+40+breathe+leg_bob, cx-12, cy+43+breathe+leg_bob],
           fill=PAJARO["pata"], width=2)
    d.line([cx-8, cy+40+breathe+leg_bob, cx-5, cy+43+breathe+leg_bob],
           fill=PAJARO["pata"], width=2)
    d.line([cx+8, cy+40+breathe+leg_bob, cx+5, cy+43+breathe+leg_bob],
           fill=PAJARO["pata"], width=2)
    d.line([cx+8, cy+40+breathe+leg_bob, cx+12, cy+43+breathe+leg_bob],
           fill=PAJARO["pata"], width=2)

    # Cabeza
    head_y = cy - 22 + breathe
    d.ellipse([cx-20, head_y-16, cx+20, head_y+12], fill=PAJARO["amarillo"])

    # Pluma en la cabeza
    d.polygon([
        (cx+6, head_y-14), (cx+14, head_y-28), (cx+10, head_y-16)
    ], fill=PAJARO["pluma"])
    d.polygon([
        (cx+8, head_y-15), (cx+13, head_y-25), (cx+10, head_y-16)
    ], fill=PAJARO["amar_osc"])

    # Ojo grande
    d.ellipse([cx+4, head_y-6, cx+14, head_y+2], fill=(255,255,255))
    d.ellipse([cx+7, head_y-4, cx+11, head_y], fill=(255,255,255))
    d.ellipse([cx+7, head_y-3, cx+11, head_y+1], fill=PAJARO["ojo"])
    d.ellipse([cx+8, head_y-2, cx+10, head_y], fill=(255,255,255,200))

    # Pico
    d.polygon([(cx-4, head_y-2), (cx-14, head_y), (cx-4, head_y+4)],
              fill=PAJARO["pico"])
    d.line([cx-4, head_y-2, cx-14, head_y], fill=PAJARO["pico_osc"], width=1)
    d.line([cx-4, head_y+4, cx-14, head_y], fill=PAJARO["pico_osc"], width=1)

    # Mejilla
    d.ellipse([cx-4, head_y-2, cx+4, head_y+6], fill=PAJARO["pecho"]+(100,))

    return im

def pajaro_sing(frame):
    im = new_img()
    d = ImageDraw.Draw(im)
    cx, cy = 60, 62

    d.ellipse([cx-30, cy+40, cx+30, cy+50], fill=(0,0,0,25))

    head_tilt = [0, -3][frame % 2]
    breathe = [0, -1][frame % 2]

    d.ellipse([cx-24, cy-12+breathe, cx+24, cy+30+breathe], fill=PAJARO["amarillo"])
    d.ellipse([cx-16, cy-4+breathe, cx+16, cy+26+breathe], fill=PAJARO["pecho"])
    d.ellipse([cx+10, cy-6+breathe, cx+28, cy+16+breathe], fill=PAJARO["ala"])
    d.polygon([
        (cx-20, cy+16+breathe), (cx-32, cy+24+breathe),
        (cx-18, cy+26+breathe), (cx-28, cy+30+breathe),
        (cx-16, cy+28+breathe)
    ], fill=PAJARO["amar_osc"])

    d.line([cx-6, cy+30+breathe, cx-8, cy+40], fill=PAJARO["pata"], width=3)
    d.line([cx+6, cy+30+breathe, cx+8, cy+40], fill=PAJARO["pata"], width=3)

    head_y = cy - 22 + head_tilt + breathe
    d.ellipse([cx-20, head_y-16, cx+20, head_y+12], fill=PAJARO["amarillo"])

    d.polygon([
        (cx+6, head_y-14), (cx+14, head_y-28-head_tilt), (cx+10, head_y-16)
    ], fill=PAJARO["pluma"])

    d.ellipse([cx+4, head_y-6, cx+14, head_y+2], fill=(255,255,255))
    d.ellipse([cx+7, head_y-3, cx+11, head_y+1], fill=PAJARO["ojo"])
    d.ellipse([cx+8, head_y-2, cx+10, head_y], fill=(255,255,255,200))

    # Pico abierto (cantando)
    d.ellipse([cx-14, head_y-4, cx-4, head_y+4], fill=PAJARO["pico"])
    d.ellipse([cx-12, head_y-2, cx-6, head_y+2], fill=(200,80,60))

    # Notas musicales
    if frame == 1:
        d.ellipse([cx-38, head_y-20, cx-32, head_y-14], fill=PAJARO["pico"]+(200,))
        d.ellipse([cx-30, head_y-28, cx-24, head_y-22], fill=PAJARO["pico"]+(180,))
        d.line([cx-35, head_y-14, cx-35, head_y-30], fill=PAJARO["pico"]+(200,), width=2)
        d.line([cx-27, head_y-22, cx-27, head_y-36], fill=PAJARO["pico"]+(180,), width=2)
        d.arc([cx-38, head_y-32, cx-32, head_y-26], 180, 360, fill=PAJARO["pico"]+(200,), width=2)
        d.arc([cx-30, head_y-40, cx-24, head_y-34], 180, 360, fill=PAJARO["pico"]+(180,), width=2)

    return im

# ── GENERAR TODO ─────────────────────────────────────────────

COUNT = 0
def gen(name, img, subdir=""):
    global COUNT
    path = os.path.join(BASE, subdir, name)
    save(img, path)
    COUNT += 1
    print(f"  → {path}")

def generate_all():
    global COUNT
    print("=" * 60)
    print("  Generando sprites 128×128 — El Jardín Interior")
    print("=" * 60)

    # ── PROTAGONISTA ──
    print("\n📋 Protagonista:")
    for d in ["down", "left", "right", "up"]:
        for f in range(3):
            gen(f"prota_idle_{d}_{f}.png", prota_idle(d, f), "protagonista")
        for f in range(4):
            gen(f"prota_walk_{d}_{f}.png", prota_walk(d, f), "protagonista")

    # ── TORTUGA ──
    print("\n📋 Tortuga:")
    for f in range(3):
        gen(f"tortuga_idle_down_{f}.png", tortuga_idle(f), "animales")
    for f in range(4):
        gen(f"tortuga_walk_down_{f}.png", tortuga_walk(f), "animales")
    for f in range(2):
        gen(f"tortuga_talk_down_{f}.png", tortuga_talk(f), "animales")

    # ── ZORRO ──
    print("\n📋 Zorro:")
    for f in range(3):
        gen(f"zorro_idle_down_{f}.png", zorro_idle(f), "animales")
    for f in range(4):
        gen(f"zorro_walk_down_{f}.png", zorro_walk(f), "animales")
    for f in range(2):
        gen(f"zorro_talk_down_{f}.png", zorro_talk(f), "animales")

    # ── BÚHO ──
    print("\n📋 Búho:")
    for f in range(3):
        gen(f"buho_idle_down_{f}.png", buho_idle(f), "animales")
    for f in range(4):
        gen(f"buho_walk_down_{f}.png", buho_walk(f), "animales")

    # ── MARIPOSA ──
    print("\n📋 Mariposa:")
    for f in range(3):
        gen(f"mariposa_idle_down_{f}.png", mariposa_idle(f), "animales")

    # ── CARACOL ──
    print("\n📋 Caracol:")
    for f in range(3):
        gen(f"caracol_idle_down_{f}.png", caracol_idle(f), "animales")
    for f in range(4):
        gen(f"caracol_walk_down_{f}.png", caracol_walk(f), "animales")

    # ── PÁJARO ──
    print("\n📋 Pájaro:")
    for f in range(3):
        gen(f"pajaro_idle_down_{f}.png", pajaro_idle(f), "animales")
    for f in range(2):
        gen(f"pajaro_sing_down_{f}.png", pajaro_sing(f), "animales")

    print("\n" + "=" * 60)
    print(f"  ✅ Total: {COUNT} archivos generados")
    print("=" * 60)

if __name__ == "__main__":
    generate_all()
