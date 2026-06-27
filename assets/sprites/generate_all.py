#!/usr/bin/env python3
"""
Generador masivo de sprites para El Jardín Interior.
Usa PIL/Pillow para crear pixel art 32x32 y 16x16.
"""
import os, math
from PIL import Image, ImageDraw

BASE = os.path.dirname(os.path.abspath(__file__))

# ── Paleta ──────────────────────────────────────────────────
C = {
    "verde_pampa":   (74, 124, 63),
    "verde_yerba":   (107, 142, 35),
    "celeste_cielo": (135, 206, 235),
    "azul_rio":      (70, 130, 180),
    "marron_tierra": (139, 90, 43),
    "ocre_pampa":    (210, 180, 140),
    "blanco_nube":   (245, 245, 220),
    "gris_piedra":   (105, 105, 105),
    "rojo_pasion":   (205, 92, 92),
    "naranja_sol":   (255, 140, 0),
    "rosa_flor":     (255, 182, 193),
    "violeta_lejano":(147, 112, 219),
    "oro_trigo":     (218, 165, 32),
    "marron_grafito":(47, 27, 14),
    "piel_calida":   (240, 200, 160),
    "piel_media":    (210, 166, 121),
    "negro":         (0, 0, 0),
    "blanco":        (255, 255, 255),
    "gris_claro":    (200, 200, 200),
    "verde_oscuro":  (34, 80, 34),
    "azul_oscuro":   (25, 25, 112),
    "rojo_oscuro":   (139, 0, 0),
    "marron_claro":  (160, 120, 60),
    "amarillo":      (255, 255, 0),
    "naranja_claro": (255, 200, 100),
}

def new_img(size, bg=None):
    im = Image.new("RGBA", (size, size), (0,0,0,0) if bg is None else bg)
    return im, ImageDraw.Draw(im)

def save(img, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    img.save(path, "PNG")

# ── PROTAGONISTA ────────────────────────────────────────────
def prota_idle(direction):
    """Protagonista 32x32 idle en 4 direcciones"""
    im, d = new_img(32)
    cx, cy = 16, 18  # center
    piel = C["piel_calida"]
    pelo = (60, 30, 10)
    remera = C["verde_pampa"]
    pant = C["marron_tierra"]
    botas = (40, 20, 5)

    # Cuerpo base
    d.ellipse([cx-7, cy-10, cx+7, cy+4], fill=piel)  # cabeza
    if direction == "down":
        d.rectangle([cx-6, cy+4, cx+6, cy+14], fill=remera)  # torso
        d.rectangle([cx-7, cy+14, cx-2, cy+20], fill=pant)   # pierna izq
        d.rectangle([cx+2, cy+14, cx+7, cy+20], fill=pant)   # pierna der
        d.rectangle([cx-8, cy+18, cx-3, cy+20], fill=botas)  # bota izq
        d.rectangle([cx+3, cy+18, cx+8, cy+20], fill=botas)  # bota der
        d.rectangle([cx-7, cy+4, cx-2, cy+10], fill=piel)    # brazo izq
        d.rectangle([cx+2, cy+4, cx+7, cy+10], fill=piel)    # brazo der
        # Cara
        d.ellipse([cx-4, cy-5, cx-2, cy-3], fill=C["negro"]) # ojo izq
        d.ellipse([cx+2, cy-5, cx+4, cy-3], fill=C["negro"]) # ojo der
        d.arc([cx-2, cy-4, cx+2, cy-1], 0, 180, fill=C["negro"]) # sonrisa
        # Pelo
        d.arc([cx-8, cy-12, cx+8, cy-4], 180, 360, fill=pelo)
        d.polygon([(cx-8,cy-6),(cx-10,cy-10),(cx-6,cy-12)], fill=pelo)
        d.polygon([(cx+8,cy-6),(cx+10,cy-10),(cx+6,cy-12)], fill=pelo)
    elif direction == "up":
        d.rectangle([cx-6, cy+4, cx+6, cy+14], fill=remera)
        d.rectangle([cx-7, cy+14, cx-2, cy+20], fill=pant)
        d.rectangle([cx+2, cy+14, cx+7, cy+20], fill=pant)
        d.ellipse([cx-7, cy-10, cx+7, cy+4], fill=pelo)
    elif direction == "left":
        d.ellipse([cx-7, cy-10, cx+3, cy+4], fill=piel)
        d.rectangle([cx-2, cy+4, cx+6, cy+14], fill=remera)
        d.rectangle([cx-3, cy+14, cx+2, cy+20], fill=pant)
        d.rectangle([cx+3, cy+14, cx+7, cy+20], fill=pant)
        d.ellipse([cx-4, cy-5, cx-2, cy-3], fill=C["negro"])
        d.arc([cx-8, cy-12, cx+4, cy-4], 180, 360, fill=pelo)
    elif direction == "right":
        d.ellipse([cx-3, cy-10, cx+7, cy+4], fill=piel)
        d.rectangle([cx-6, cy+4, cx+2, cy+14], fill=remera)
        d.rectangle([cx-7, cy+14, cx-2, cy+20], fill=pant)
        d.rectangle([cx+2, cy+14, cx+7, cy+20], fill=pant)
        d.ellipse([cx+2, cy-5, cx+4, cy-3], fill=C["negro"])
        d.arc([cx-4, cy-12, cx+8, cy-4], 180, 360, fill=pelo)
    return im

def prota_walk(direction):
    """Walk frame ligeramente desplazado vs idle"""
    im, d = new_img(32)
    cx, cy = 16, 18
    piel = C["piel_calida"]
    pelo = (60, 30, 10)
    remera = C["verde_pampa"]
    pant = C["marron_tierra"]

    d.ellipse([cx-7, cy-10, cx+7, cy+4], fill=piel)
    offset = 1 if direction in ("left","right") else 0
    if direction == "down":
        d.rectangle([cx-6, cy+4+offset, cx+6, cy+14+offset], fill=remera)
        d.rectangle([cx-8, cy+16, cx-2, cy+22], fill=pant)  # paso
        d.rectangle([cx+2, cy+14, cx+7, cy+20], fill=pant)
        d.ellipse([cx-4, cy-5, cx-2, cy-3], fill=C["negro"])
        d.ellipse([cx+2, cy-5, cx+4, cy-3], fill=C["negro"])
        d.arc([cx-2, cy-4, cx+2, cy-1], 0, 180, fill=C["negro"])
        d.arc([cx-8, cy-12, cx+8, cy-4], 180, 360, fill=pelo)
    elif direction == "up":
        d.rectangle([cx-6, cy+4, cx+6, cy+14], fill=remera)
        d.rectangle([cx-7, cy+14, cx-2, cy+20], fill=pant)
        d.rectangle([cx+2, cy+14, cx+7, cy+20], fill=pant)
        d.ellipse([cx-7, cy-10, cx+7, cy+4], fill=pelo)
    elif direction == "left":
        d.ellipse([cx-7, cy-10, cx+3, cy+4], fill=piel)
        d.rectangle([cx-2, cy+4, cx+6, cy+14], fill=remera)
        d.rectangle([cx-5, cy+14, cx+1, cy+20], fill=pant)
        d.rectangle([cx+3, cy+15, cx+8, cy+21], fill=pant)
        d.ellipse([cx-4, cy-5, cx-2, cy-3], fill=C["negro"])
        d.arc([cx-8, cy-12, cx+4, cy-4], 180, 360, fill=pelo)
    elif direction == "right":
        d.ellipse([cx-3, cy-10, cx+7, cy+4], fill=piel)
        d.rectangle([cx-6, cy+4, cx+2, cy+14], fill=remera)
        d.rectangle([cx-3, cy+15, cx+2, cy+21], fill=pant)
        d.rectangle([cx+4, cy+14, cx+9, cy+20], fill=pant)
        d.ellipse([cx+2, cy-5, cx+4, cy-3], fill=C["negro"])
        d.arc([cx-4, cy-12, cx+8, cy-4], 180, 360, fill=pelo)
    return im

def prota_cape():
    im, d = new_img(32)
    cx, cy = 16, 16
    rojo = C["rojo_pasion"]
    oro = C["oro_trigo"]
    # Capa cayendo
    d.polygon([(cx-8,cy-6),(cx-12,cy+14),(cx-6,cy+15),(cx-5,cy-8)], fill=rojo)
    d.polygon([(cx+8,cy-6),(cx+12,cy+14),(cx+6,cy+15),(cx+5,cy-8)], fill=rojo)
    d.polygon([(cx-10,cy+14),(cx+10,cy+14),(cx+8,cy+15),(cx-8,cy+15)], fill=rojo)
    # Cierre dorado
    d.point((cx, cy-2), fill=oro)
    d.point((cx, cy-1), fill=oro)
    d.point((cx-1, cy-2), fill=oro)
    d.point((cx+1, cy-2), fill=oro)
    return im

# ── ANIMALES ────────────────────────────────────────────────
def tortuga_idle():
    im, d = new_img(32)
    cx, cy = 16, 16
    verde = C["verde_pampa"]
    marron = C["marron_tierra"]
    piel = (180, 200, 100)
    # Caparazón
    d.ellipse([cx-10, cy-6, cx+10, cy+8], fill=verde)
    d.arc([cx-8, cy-8, cx+8, cy+2], 180, 360, fill=marron, width=2)
    # Patrón caparazón
    d.line([cx, cy-6, cx, cy+2], fill=marron)
    d.line([cx-5, cy-4, cx+5, cy-4], fill=marron)
    # Cabeza
    d.ellipse([cx+8, cy-10, cx+14, cy-2], fill=piel)
    d.point((cx+10, cy-7), fill=C["negro"])
    d.point((cx+12, cy-7), fill=C["negro"])
    d.arc([cx+9, cy-6, cx+13, cy-3], 0, 180, fill=C["negro"])
    # Patas
    d.ellipse([cx-10, cy+6, cx-6, cy+11], fill=piel)
    d.ellipse([cx+6, cy+6, cx+10, cy+11], fill=piel)
    d.ellipse([cx-10, cy-8, cx-6, cy-3], fill=piel)
    return im

def tortuga_walk():
    im, d = new_img(32)
    cx, cy = 16, 18
    verde = C["verde_pampa"]
    marron = C["marron_tierra"]
    piel = (180, 200, 100)
    d.ellipse([cx-10, cy-8, cx+10, cy+6], fill=verde)
    d.arc([cx-8, cy-10, cx+8, cy+0], 180, 360, fill=marron, width=2)
    d.ellipse([cx+8, cy-12, cx+14, cy-4], fill=piel)
    d.point((cx+10, cy-9), fill=C["negro"])
    d.point((cx+12, cy-9), fill=C["negro"])
    d.ellipse([cx-12, cy+4, cx-7, cy+10], fill=piel)
    d.ellipse([cx+7, cy+5, cx+12, cy+10], fill=piel)
    return im

def tortuga_talk():
    im = tortuga_idle()
    d = ImageDraw.Draw(im)
    cx, cy = 16, 16
    d.ellipse([cx+9, cy-6, cx+13, cy-3], fill=C["blanco"])
    return im

def zorro_idle():
    im, d = new_img(32)
    cx, cy = 16, 14
    naranja = C["naranja_sol"]
    blanco = C["blanco_nube"]
    # Cuerpo
    d.ellipse([cx-8, cy-4, cx+8, cy+10], fill=naranja)
    d.polygon([(cx-12,cy-8),(cx-4,cy-4),(cx-6,cy-10)], fill=naranja)  # oreja izq
    d.polygon([(cx+12,cy-8),(cx+4,cy-4),(cx+6,cy-10)], fill=naranja)  # oreja der
    d.polygon([(cx-14,cy-6),(cx-8,cy-2),(cx-12,cy-10)], fill=blanco) # punta oreja
    d.polygon([(cx+14,cy-6),(cx+8,cy-2),(cx+12,cy-10)], fill=blanco)
    # Cara
    d.ellipse([cx-7, cy-6, cx+7, cy+4], fill=naranja)
    d.polygon([(cx-4,cy-2),(cx,cy+2),(cx+4,cy-2)], fill=blanco)  # hocico
    d.point((cx-3, cy-3), fill=C["negro"])  # ojo izq
    d.point((cx+3, cy-3), fill=C["negro"])  # ojo der
    d.point((cx, cy-1), fill=C["negro"])    # nariz
    # Cola
    d.polygon([(cx+6,cy+8),(cx+14,cy+6),(cx+12,cy+12),(cx+8,cy+12)], fill=naranja)
    d.polygon([(cx+12,cy+8),(cx+14,cy+6),(cx+13,cy+10)], fill=blanco)
    # Patas
    d.ellipse([cx-7, cy+8, cx-3, cy+14], fill=naranja)
    d.ellipse([cx+3, cy+8, cx+7, cy+14], fill=naranja)
    return im

def zorro_walk():
    im, d = new_img(32)
    cx, cy = 16, 15
    naranja = C["naranja_sol"]
    d.ellipse([cx-8, cy-4, cx+8, cy+10], fill=naranja)
    d.polygon([(cx-12,cy-8),(cx-4,cy-4),(cx-6,cy-10)], fill=naranja)
    d.polygon([(cx+12,cy-8),(cx+4,cy-4),(cx+6,cy-10)], fill=naranja)
    d.ellipse([cx-7, cy-6, cx+7, cy+4], fill=naranja)
    d.point((cx-3, cy-3), fill=C["negro"])
    d.point((cx+3, cy-3), fill=C["negro"])
    d.point((cx, cy-1), fill=C["negro"])
    d.ellipse([cx-8, cy+9, cx-4, cy+15], fill=naranja)
    d.ellipse([cx+4, cy+8, cx+8, cy+14], fill=naranja)
    return im

def zorro_talk():
    im = zorro_idle()
    d = ImageDraw.Draw(im)
    cx, cy = 16, 14
    d.ellipse([cx-2, cy+1, cx+2, cy+3], fill=C["rojo_pasion"])
    return im

def buho_idle():
    im, d = new_img(32)
    cx, cy = 16, 14
    marron = C["marron_tierra"]
    ocre = C["ocre_pampa"]
    # Cuerpo
    d.ellipse([cx-9, cy-5, cx+9, cy+12], fill=marron)
    # Ojos grandes
    d.ellipse([cx-7, cy-8, cx-2, cy-2], fill=C["blanco"])
    d.ellipse([cx+2, cy-8, cx+7, cy-2], fill=C["blanco"])
    d.ellipse([cx-5, cy-6, cx-4, cy-4], fill=C["negro"])  # pupila
    d.ellipse([cx+4, cy-6, cx+5, cy-4], fill=C["negro"])
    # Pico
    d.polygon([(cx-2,cy-3),(cx+2,cy-3),(cx,cy)], fill=C["naranja_sol"])
    # Cejas (cejas de búho distintivas)
    d.line([cx-9, cy-10, cx-2, cy-9], fill=C["negro"], width=1)
    d.line([cx+2, cy-9, cx+9, cy-10], fill=C["negro"], width=1)
    # Alas
    d.arc([cx-12, cy-2, cx-8, cy+8], 90, 270, fill=ocre, width=2)
    d.arc([cx+8, cy-2, cx+12, cy+8], 270, 90, fill=ocre, width=2)
    # Patas
    d.line([cx-3, cy+12, cx-3, cy+16], fill=C["naranja_sol"])
    d.line([cx+3, cy+12, cx+3, cy+16], fill=C["naranja_sol"])
    return im

def buho_walk():
    im, d = new_img(32)
    cx, cy = 16, 13
    marron = C["marron_tierra"]
    d.ellipse([cx-9, cy-4, cx+9, cy+12], fill=marron)
    d.ellipse([cx-7, cy-8, cx-2, cy-2], fill=C["blanco"])
    d.ellipse([cx+2, cy-8, cx+7, cy-2], fill=C["blanco"])
    d.ellipse([cx-5, cy-6, cx-4, cy-4], fill=C["negro"])
    d.ellipse([cx+4, cy-6, cx+5, cy-4], fill=C["negro"])
    d.polygon([(cx-2,cy-3),(cx+2,cy-3),(cx,cy)], fill=C["naranja_sol"])
    d.line([cx-4, cy+12, cx-5, cy+16], fill=C["naranja_sol"])
    d.line([cx+4, cy+12, cx+5, cy+16], fill=C["naranja_sol"])
    return im

def mariposa_idle():
    im, d = new_img(32)
    cx, cy = 16, 16
    violeta = C["violeta_lejano"]
    rosa = C["rosa_flor"]
    # Alas
    d.ellipse([cx-12, cy-8, cx-2, cy+4], fill=violeta)
    d.ellipse([cx+2, cy-8, cx+12, cy+4], fill=violeta)
    d.ellipse([cx-8, cy-2, cx-2, cy+8], fill=rosa)
    d.ellipse([cx+2, cy-2, cx+8, cy+8], fill=rosa)
    # Cuerpo
    d.ellipse([cx-2, cy-4, cx+2, cy+8], fill=C["negro"])
    # Antenas
    d.line([cx-1, cy-4, cx-4, cy-10], fill=C["negro"])
    d.line([cx+1, cy-4, cx+4, cy-10], fill=C["negro"])
    d.point((cx-4, cy-10), fill=C["amarillo"])
    d.point((cx+4, cy-10), fill=C["amarillo"])
    # Partículas (puntos brillantes)
    for _ in range(6):
        import random
        px = random.randint(0, 31)
        py = random.randint(0, 31)
        d.point((px, py), fill=(255,255,255,100))
    return im

def caracol_idle():
    im, d = new_img(32)
    cx, cy = 16, 18
    ocre = C["ocre_pampa"]
    marron = C["marron_claro"]
    # Concha espiral
    d.ellipse([cx-8, cy-6, cx+8, cy+6], fill=ocre)
    d.arc([cx-6, cy-4, cx+6, cy+4], 0, 360, fill=marron, width=1)
    d.arc([cx-4, cy-2, cx+4, cy+2], 0, 360, fill=marron, width=1)
    # Cuerpo
    d.ellipse([cx-4, cy+4, cx+4, cy+10], fill=C["piel_calida"])
    # Antenas
    d.line([cx-2, cy-6, cx-4, cy-12], fill=C["gris_piedra"])
    d.line([cx+2, cy-6, cx+4, cy-12], fill=C["gris_piedra"])
    d.point((cx-4, cy-12), fill=C["negro"])
    d.point((cx+4, cy-12), fill=C["negro"])
    return im

def caracol_walk():
    im = caracol_idle()
    d = ImageDraw.Draw(im)
    cx, cy = 16, 18
    d.ellipse([cx-5, cy+8, cx+5, cy+11], fill=C["piel_calida"])
    return im

def pajaro_idle():
    im, d = new_img(32)
    cx, cy = 16, 16
    celeste = C["celeste_cielo"]
    amarillo = C["amarillo"]
    # Cuerpo
    d.ellipse([cx-8, cy-4, cx+8, cy+8], fill=celeste)
    d.ellipse([cx-6, cy-6, cx+4, cy+2], fill=celeste)  # cabeza
    d.point((cx-4, cy-4), fill=C["negro"])  # ojo
    d.polygon([(cx+2,cy-2),(cx+6,cy-1),(cx+2,cy)], fill=C["naranja_sol"])  # pico
    # Ala
    d.polygon([(cx+4,cy+2),(cx+10,cy+6),(cx+4,cy+8)], fill=C["azul_rio"])
    # Cola
    d.polygon([(cx-6,cy+6),(cx-12,cy+10),(cx-8,cy+8)], fill=C["azul_rio"])
    # Patas
    d.line([cx-2, cy+8, cx-3, cy+13], fill=C["negro"])
    d.line([cx+2, cy+8, cx+3, cy+13], fill=C["negro"])
    return im

def pajaro_sing():
    im, d = new_img(32)
    cx, cy = 16, 16
    celeste = C["celeste_cielo"]
    d.ellipse([cx-8, cy-4, cx+8, cy+8], fill=celeste)
    d.ellipse([cx-6, cy-6, cx+4, cy+2], fill=celeste)
    d.point((cx-4, cy-4), fill=C["negro"])
    d.ellipse([cx+1, cy-3, cx+5, cy+1], fill=C["rojo_pasion"])  # pico abierto cantando
    d.polygon([(cx+4,cy+2),(cx+10,cy+6),(cx+4,cy+8)], fill=C["azul_rio"])
    d.polygon([(cx-6,cy+6),(cx-12,cy+10),(cx-8,cy+8)], fill=C["azul_rio"])
    d.point((cx+7, cy-5), fill=C["naranja_sol"])  # nota musical
    d.point((cx+9, cy-8), fill=C["naranja_sol"])
    d.line([cx+7, cy-5, cx+9, cy-8], fill=C["naranja_sol"])
    return im

# ── RETRATOS 16×16 ─────────────────────────────────────────
PERSONAJES = {
    "messi":         (C["piel_calida"], (50,30,10), C["celeste_cielo"], "by"),
    "mafalda":       (C["piel_calida"], (30,30,10), C["negro"], "bow"),
    "frida_kahlo":   (C["piel_media"], (20,10,5), C["rojo_pasion"], "flow"),
    "san_martin":    (C["piel_calida"], (10,10,10), C["azul_rio"], "mil"),
    "eva_peron":     (C["piel_calida"], (200,180,100), C["rosa_flor"], "elegant"),
    "bowie":         (C["piel_calida"], (220,180,50), C["naranja_sol"], "ziggy"),
    "maradona":      (C["piel_media"], (30,20,10), C["celeste_cielo"], "curly"),
    "gardel":        (C["piel_calida"], (20,15,10), C["gris_piedra"], "smile"),
    "quino":         (C["piel_calida"], (60,60,60), C["gris_claro"], "glasses"),
    "charly_garcia": (C["piel_calida"], (10,10,10), C["negro"], "long"),
    "manu_ginobili": (C["piel_calida"], (70,50,20), C["celeste_cielo"], "bold"),
    "snoopy":        (C["blanco"], C["blanco"], C["negro"], "dog"),
    "laika":         (C["marron_claro"], C["marron_claro"], C["gris_claro"], "dog"),
    "ellie_up":      (C["piel_calida"], (60,60,60), C["rosa_flor"], "round"),
    "totoro":        (C["gris_piedra"], C["gris_piedra"], C["verde_pampa"], "big"),
    "woody":         (C["piel_calida"], (180,120,60), C["rojo_pasion"], "cowboy"),
    "merida":        (C["piel_calida"], (200,100,30), C["verde_pampa"], "curly"),
    "mulan":         (C["piel_media"], (20,10,5), C["rojo_pasion"], "updo"),
    "astrid":        (C["piel_calida"], (220,180,50), C["verde_oscuro"], "braid"),
    "goku_nino":     (C["piel_calida"], (30,20,10), C["naranja_sol"], "spike"),
    "sakura":        (C["piel_calida"], (200,150,100), C["rosa_flor"], "flow"),
    "naruto":        (C["piel_calida"], (220,180,50), C["naranja_sol"], "spike"),
    "simba":         (C["oro_trigo"], C["oro_trigo"], C["marron_claro"], "lion"),
    "walle":         (C["gris_piedra"], C["gris_piedra"], C["amarillo"], "robot"),
    "eva_walle":     (C["blanco"], C["blanco"], C["celeste_cielo"], "smooth"),
    "miguel_coco":   (C["piel_media"], (30,20,10), C["rojo_pasion"], "smile"),
    "hector_coco":   (C["piel_calida"], (10,10,10), C["marron_claro"], "skeleton"),
    "arlo":          (C["verde_yerba"], C["verde_yerba"], C["naranja_sol"], "dino"),
    "po_kungfu":     (C["piel_calida"], (30,20,10), C["rojo_pasion"], "round"),
    "shrek":         (C["verde_pampa"], C["verde_pampa"], C["marron_tierra"], "big"),
    "fiona":         (C["verde_pampa"], (200,100,50), C["rosa_flor"], "round"),
    "hiccup":        (C["piel_calida"], (30,20,10), C["verde_oscuro"], "spike"),
    "toothless":     (C["negro"], C["negro"], C["verde_yerba"], "dragon"),
    "elsa":          (C["piel_calida"], (180,200,220), C["celeste_cielo"], "braid"),
    "ana":           (C["piel_calida"], (150,100,50), C["marron_tierra"], "twin"),
    "olaf":          (C["blanco"], C["blanco"], C["naranja_sol"], "snow"),
    "moana":         (C["piel_media"], (30,10,5), C["rojo_pasion"], "curl"),
    "maui":          (C["piel_media"], (50,30,10), C["verde_pampa"], "tattoo"),
    "vaiana":        (C["piel_media"], (30,10,5), C["verde_pampa"], "curl"),
    "spiderman_miles": (C["piel_media"], (30,20,10), C["rojo_pasion"], "mask"),
    "tiana":         (C["piel_media"], (30,20,10), C["verde_pampa"], "updo"),
    "rapunzel":      (C["piel_calida"], (200,180,100), C["rosa_flor"], "long"),
    "flynn":         (C["piel_calida"], (150,120,80), C["marron_claro"], "smile"),
    "judy_hopps":    (C["gris_claro"], C["gris_claro"], C["azul_rio"], "bunny"),
    "nick_wilde":    (C["naranja_sol"], C["naranja_sol"], C["verde_pampa"], "fox"),
    "ralph":         (C["rojo_pasion"], C["rojo_pasion"], C["marron_claro"], "big"),
    "vanellope":     (C["piel_calida"], (30,10,5), C["rosa_flor"], "twin"),
    "baymax":        (C["blanco"], C["blanco"], C["rojo_pasion"], "balloon"),
    "hiro":          (C["piel_calida"], (30,20,10), C["negro"], "spike"),
    "joy":           (C["piel_calida"], (100,150,255), C["amarillo"], "glow"),
    "sadness":       (C["piel_calida"], (50,50,120), C["azul_oscuro"], "round"),
    "bing_bong":     (C["rosa_flor"], C["rosa_flor"], (200,100,150), "round"),
}

def make_portrait(skin, hair, accent, style):
    im, d = new_img(16)
    cx, cy = 8, 8
    # Cabeza base
    d.ellipse([cx-5, cy-5, cx+5, cy+5], fill=skin)
    # Ojos
    d.point((cx-3, cy-2), fill=C["negro"])
    d.point((cx+3, cy-2), fill=C["negro"])
    if style == "smile":
        d.arc([cx-2, cy-1, cx+2, cy+2], 0, 180, fill=C["negro"])
    elif style == "dog":
        d.ellipse([cx-5, cy-5, cx+5, cy+5], fill=skin)
        d.point((cx-2, cy-2), fill=C["negro"])
        d.point((cx+2, cy-2), fill=C["negro"])
        d.point((cx, cy), fill=C["negro"])
        d.ellipse([cx-4, cy-6, cx-1, cy-3], fill=hair)
        d.ellipse([cx+1, cy-6, cx+4, cy-3], fill=hair)
    elif style == "lion":
        d.ellipse([cx-6, cy-6, cx+6, cy+6], fill=accent)
        d.ellipse([cx-4, cy-4, cx+4, cy+4], fill=skin)
        d.point((cx-2, cy-2), fill=C["negro"])
        d.point((cx+2, cy-2), fill=C["negro"])
        d.point((cx, cy), fill=C["marron_tierra"])
    elif style == "robot":
        d.rectangle([cx-5, cy-5, cx+5, cy+5], fill=skin)
        d.point((cx-3, cy-2), fill=C["amarillo"])
        d.point((cx+3, cy-2), fill=C["amarillo"])
        d.rectangle([cx-2, cy, cx+2, cy+1], fill=accent)
    elif style == "skeleton":
        d.ellipse([cx-5, cy-5, cx+5, cy+5], fill=C["blanco_nube"])
        d.point((cx-3, cy-2), fill=C["negro"])
        d.point((cx+3, cy-2), fill=C["negro"])
        d.rectangle([cx-2, cy, cx+2, cy+1], fill=C["negro"])
    elif style == "dino":
        d.ellipse([cx-6, cy-6, cx+6, cy+6], fill=skin)
        d.point((cx-2, cy-2), fill=C["blanco"])
        d.point((cx+2, cy-2), fill=C["blanco"])
        d.point((cx-2, cy-2), fill=C["negro"])
        d.point((cx+2, cy-2), fill=C["negro"])
        d.polygon([(cx+2,cy-4),(cx+6,cy-7),(cx+4,cy-3)], fill=C["verde_oscuro"])
    elif style == "dragon":
        d.ellipse([cx-5, cy-5, cx+5, cy+5], fill=skin)
        d.point((cx-2, cy-2), fill=C["verde_yerba"])
        d.point((cx+2, cy-2), fill=C["verde_yerba"])
        d.point((cx, cy), fill=C["naranja_sol"])
        d.polygon([(cx-5,cy-5),(cx-7,cy-8),(cx-3,cy-6)], fill=skin)
        d.polygon([(cx+5,cy-5),(cx+7,cy-8),(cx+3,cy-6)], fill=skin)
    elif style == "snow":
        d.ellipse([cx-4, cy-4, cx+4, cy+4], fill=skin)
        d.ellipse([cx-5, cy-1, cx+5, cy+4], fill=skin)
        d.point((cx-2, cy-2), fill=C["negro"])
        d.point((cx+2, cy-2), fill=C["negro"])
        d.polygon([(cx-1,cy),(cx+1,cy),(cx,cy+2)], fill=C["naranja_sol"])
    elif style == "mask":
        d.ellipse([cx-5, cy-5, cx+5, cy+5], fill=skin)
        d.rectangle([cx-5, cy-4, cx+5, cy], fill=C["rojo_pasion"])
        d.point((cx-2, cy-2), fill=C["blanco"])
        d.point((cx+2, cy-2), fill=C["blanco"])
    elif style == "bunny":
        d.ellipse([cx-5, cy-4, cx+5, cy+4], fill=skin)
        d.ellipse([cx-3, cy-7, cx-1, cy-3], fill=C["blanco"])
        d.ellipse([cx+1, cy-7, cx+3, cy-3], fill=C["blanco"])
        d.point((cx-2, cy-1), fill=C["negro"])
        d.point((cx+2, cy-1), fill=C["negro"])
        d.point((cx, cy+1), fill=C["rosa_flor"])
    elif style == "fox":
        d.ellipse([cx-5, cy-5, cx+5, cy+5], fill=skin)
        d.polygon([(cx-6,cy-7),(cx-3,cy-4),(cx-4,cy-7)], fill=C["blanco"])
        d.polygon([(cx+6,cy-7),(cx+3,cy-4),(cx+4,cy-7)], fill=C["blanco"])
        d.point((cx-2, cy-2), fill=C["verde_yerba"])
        d.point((cx+2, cy-2), fill=C["verde_yerba"])
        d.ellipse([cx-2, cy, cx+2, cy+2], fill=C["blanco"])
        d.point((cx, cy), fill=C["negro"])
    elif style == "balloon":
        d.ellipse([cx-5, cy-5, cx+5, cy+5], fill=C["blanco"])
        d.point((cx-2, cy-2), fill=C["negro"])
        d.point((cx+2, cy-2), fill=C["negro"])
        d.ellipse([cx-1, cy, cx+1, cy+1], fill=accent)
    elif style == "glow":
        d.ellipse([cx-5, cy-5, cx+5, cy+5], fill=skin)
        d.point((cx-2, cy-2), fill=C["azul_oscuro"])
        d.point((cx+2, cy-2), fill=C["azul_oscuro"])
        d.ellipse([cx-5, cy, cx+5, cy+3], fill=C["blanco"])
        d.ellipse([cx-6, cy-6, cx+6, cy+6], fill=accent)  # glow
        d.ellipse([cx-5, cy-5, cx+5, cy+5], fill=skin)  # re-draw face
        d.point((cx-2, cy-2), fill=C["azul_oscuro"])
        d.point((cx+2, cy-2), fill=C["azul_oscuro"])
        d.ellipse([cx-5, cy, cx+5, cy+3], fill=C["blanco"])
    elif style == "tattoo":
        d.ellipse([cx-5, cy-5, cx+5, cy+5], fill=skin)
        d.point((cx-2, cy-2), fill=C["negro"])
        d.point((cx+2, cy-2), fill=C["negro"])
        d.arc([cx-4, cy-2, cx+4, cy+3], 0, 180, fill=C["negro"])
        d.line([cx, cy-5, cx, cy+5], fill=C["verde_oscuro"])
    else:
        # Pelo genérico
        d.ellipse([cx-5, cy-7, cx+5, cy-2], fill=hair)  # flequillo genérico
        if style == "curly":
            d.ellipse([cx-6, cy-7, cx+6, cy-2], fill=hair)
            for dx in [-4,0,4]:
                d.ellipse([cx+dx-2, cy-8, cx+dx+2, cy-4], fill=hair)
        elif style == "braid":
            d.ellipse([cx-5, cy-7, cx+5, cy-2], fill=hair)
            d.polygon([(cx-5,cy-5),(cx-8,cy-2),(cx-6,cy)], fill=hair)
        elif style == "updo":
            d.ellipse([cx-5, cy-7, cx+5, cy-2], fill=hair)
            d.ellipse([cx-3, cy-9, cx+3, cy-5], fill=hair)
        elif style == "twin":
            d.ellipse([cx-5, cy-7, cx+5, cy-2], fill=hair)
            d.ellipse([cx-6, cy-4, cx-3, cy], fill=hair)
            d.ellipse([cx+3, cy-4, cx+6, cy], fill=hair)
        elif style == "long":
            d.ellipse([cx-5, cy-7, cx+5, cy-2], fill=hair)
            d.rectangle([cx-5, cy-4, cx-2, cy+4], fill=hair)
            d.rectangle([cx+2, cy-4, cx+5, cy+4], fill=hair)
        elif style == "flow":
            d.ellipse([cx-6, cy-7, cx+6, cy-2], fill=hair)
            d.polygon([(cx-5,cy-4),(cx-7,cy+2),(cx-5,cy+3)], fill=hair)
            d.polygon([(cx+5,cy-4),(cx+7,cy+2),(cx+5,cy+3)], fill=hair)
        elif style == "bow":
            d.ellipse([cx-5, cy-7, cx+5, cy-2], fill=hair)
            # Moño
            d.ellipse([cx+4, cy-6, cx+7, cy-3], fill=C["rojo_pasion"])
        elif style == "elegant":
            d.ellipse([cx-5, cy-7, cx+5, cy-2], fill=hair)
            d.ellipse([cx-4, cy-9, cx+4, cy-5], fill=hair)
        elif style == "ziggy":
            d.polygon([(cx-5,cy-5),(cx-3,cy-9),(cx-1,cy-5),(cx+1,cy-9),(cx+3,cy-5),(cx+5,cy-9),(cx+5,cy-2)], fill=C["naranja_sol"])
        elif style == "spike":
            for dx in [-4,-2,0,2,4]:
                d.polygon([(cx+dx-1,cy-5),(cx+dx,cy-9),(cx+dx+1,cy-5)], fill=hair)
        elif style == "glasses":
            d.ellipse([cx-5, cy-7, cx+5, cy-2], fill=hair)
            d.ellipse([cx-5, cy-4, cx-1, cy-1], fill=None, outline=C["negro"])
            d.ellipse([cx+1, cy-4, cx+5, cy-1], fill=None, outline=C["negro"])
            d.line([cx-1, cy-3, cx+1, cy-3], fill=C["negro"])
        elif style == "bold":
            d.ellipse([cx-5, cy-6, cx+5, cy-3], fill=hair)
        elif style == "big":
            d.ellipse([cx-6, cy-6, cx+6, cy+6], fill=skin)
            d.point((cx-3, cy-2), fill=C["negro"])
            d.point((cx+3, cy-2), fill=C["negro"])
            d.ellipse([cx-2, cy, cx+2, cy+2], fill=C["negro"])
        elif style == "cowboy":
            d.ellipse([cx-5, cy-5, cx+5, cy+2], fill=skin)
            d.rectangle([cx-6, cy-8, cx+6, cy-4], fill=hair)
            d.rectangle([cx-7, cy-8, cx-5, cy-5], fill=hair)
            d.rectangle([cx+5, cy-8, cx+7, cy-5], fill=hair)
        elif style == "curl":
            d.ellipse([cx-5, cy-7, cx+5, cy-5], fill=hair)
            d.ellipse([cx-5, cy-6, cx-1, cy-1], fill=hair)
            d.ellipse([cx+1, cy-6, cx+5, cy-1], fill=hair)
            # añadir acento como collar o flor
            d.point((cx-4, cy+3), fill=accent)
            d.point((cx+4, cy+3), fill=accent)
        elif style == "round":
            d.ellipse([cx-6, cy-6, cx+6, cy+6], fill=skin)
            d.point((cx-3, cy-2), fill=C["negro"])
            d.point((cx+3, cy-2), fill=C["negro"])
            d.point((cx, cy+1), fill=C["negro"])
        elif style == "smooth":
            d.ellipse([cx-4, cy-5, cx+4, cy+5], fill=skin)
            d.point((cx-2, cy-2), fill=C["negro"])
            d.point((cx+2, cy-2), fill=C["negro"])
        else:
            d.point((cx, cy), fill=C["negro"])
    return im

# ── UI ──────────────────────────────────────────────────────
def btn_normal():
    im, d = new_img(32)
    d.rectangle([0,0,31,31], fill=C["marron_tierra"])
    d.rectangle([2,2,29,29], fill=C["ocre_pampa"])
    d.rectangle([4,4,27,27], fill=C["marron_claro"])
    return im

def btn_hover():
    im, d = new_img(32)
    d.rectangle([0,0,31,31], fill=C["oro_trigo"])
    d.rectangle([2,2,29,29], fill=C["naranja_sol"])
    d.rectangle([4,4,27,27], fill=C["naranja_claro"])
    return im

def btn_press():
    im, d = new_img(32)
    d.rectangle([0,0,31,31], fill=C["marron_grafito"])
    d.rectangle([2,2,29,29], fill=C["marron_tierra"])
    d.rectangle([4,4,27,27], fill=C["marron_claro"])
    return im

def dialog_bubble():
    im, d = new_img(32)
    d.ellipse([2,2,30,26], fill=C["blanco_nube"])
    d.ellipse([0,0,30,26], fill=None, outline=C["negro"], width=1)
    # Pico de burbuja
    d.polygon([(6,24),(10,30),(14,24)], fill=C["blanco_nube"])
    d.polygon([(6,24),(10,30),(14,24)], fill=None, outline=C["negro"])
    d.point((3, 8), fill=C["negro"])
    d.point((8, 5), fill=C["negro"])
    d.point((13, 8), fill=C["negro"])
    return im

def hud_brújula():
    im, d = new_img(16)
    rojo = C["rojo_pasion"]
    d.ellipse([0,0,15,15], fill=C["ocre_pampa"])
    d.polygon([(8,1),(5,8),(11,8)], fill=rojo)  # N rojo
    d.polygon([(8,15),(5,8),(11,8)], fill=C["gris_piedra"])
    d.ellipse([7,7,9,9], fill=C["oro_trigo"])
    return im

def icon_seed():
    im, d = new_img(16)
    d.ellipse([4,6,12,14], fill=C["marron_tierra"])
    d.line([8,6,8,2], fill=C["verde_pampa"])
    d.point((8, 2), fill=C["verde_yerba"])
    return im

def icon_flower():
    im, d = new_img(16)
    d.line([8,12,8,5], fill=C["verde_pampa"])
    d.ellipse([5,2,11,8], fill=C["rojo_pasion"])
    d.ellipse([6,3,10,7], fill=C["rosa_flor"])
    d.point((8,5), fill=C["amarillo"])
    return im

def icon_tool():
    im, d = new_img(16)
    d.rectangle([6,2,10,8], fill=C["marron_tierra"])  # mango
    d.rectangle([5,8,11,12], fill=C["gris_piedra"])   # pala
    return im

def menu_tree():
    im, d = new_img(32)
    d.rectangle([14,16,18,28], fill=C["marron_tierra"])  # tronco
    d.ellipse([4,0,28,20], fill=C["verde_pampa"])
    d.ellipse([8,4,24,16], fill=C["verde_yerba"])
    d.ellipse([12,6,20,14], fill=C["verde_oscuro"])
    d.ellipse([12,8,16,12], fill=C["oro_trigo"])  # fruto
    return im

# ── OBJETOS ────────────────────────────────────────────────
def seed():
    im, d = new_img(16)
    d.ellipse([5,4,11,12], fill=C["marron_tierra"])
    d.line([8,4,8,2], fill=C["verde_pampa"])
    return im

def watercan():
    im, d = new_img(32)
    d.rectangle([6,10,14,24], fill=C["gris_piedra"])  # cuerpo
    d.rectangle([6,24,20,26], fill=C["gris_claro"])    # base
    d.rectangle([14,12,22,16], fill=C["gris_claro"])   # pico
    d.rectangle([4,8,8,12], fill=C["gris_piedra"])     # asa
    d.ellipse([16,12,18,14], fill=C["celeste_cielo"])  # agua
    return im

def glowing_flower(color):
    im, d = new_img(32)
    cx, cy = 16, 16
    d.line([cx, cy+8, cx, cy-2], fill=C["verde_pampa"])
    d.ellipse([cx-6, cy-8, cx+6, cy+2], fill=color)
    d.ellipse([cx-4, cy-6, cx+4, cy], fill=C["amarillo"])
    # Brillo
    d.ellipse([cx-8, cy-10, cx+8, cy+4], fill=color+(80,))
    return im

def stone():
    im, d = new_img(24)
    d.ellipse([2,4,22,20], fill=C["gris_piedra"])
    d.ellipse([6,6,18,18], fill=C["gris_claro"])
    return im

def feather():
    im, d = new_img(24)
    d.ellipse([2,4,20,20], fill=C["blanco_nube"])
    d.line([12,4,12,20], fill=C["negro"])
    return im

def music_note():
    im, d = new_img(16)
    d.ellipse([8,10,14,15], fill=C["naranja_sol"])
    d.rectangle([10,2,12,12], fill=C["naranja_sol"])
    d.line([8,12,12,10], fill=C["naranja_sol"])
    return im

# ── GENERAR TODO ────────────────────────────────────────────
def generate_all():
    results = []
    def gen(name, img, subdir=""):
        path = os.path.join(BASE, subdir, name)
        save(img, path)
        results.append(path)

    # Protagonista
    for d in ["down","left","right","up"]:
        gen(f"prota_idle_{d}.png", prota_idle(d), "protagonista")
        gen(f"prota_walk_{d}.png", prota_walk(d), "protagonista")
    gen("prota_cape_idle.png", prota_cape(), "protagonista")

    # Animales
    gen("tortuga_idle.png", tortuga_idle(), "animales")
    gen("tortuga_walk.png", tortuga_walk(), "animales")
    gen("tortuga_talk.png", tortuga_talk(), "animales")
    gen("zorro_idle.png", zorro_idle(), "animales")
    gen("zorro_walk.png", zorro_walk(), "animales")
    gen("zorro_talk.png", zorro_talk(), "animales")
    gen("buho_idle.png", buho_idle(), "animales")
    gen("buho_walk.png", buho_walk(), "animales")
    gen("mariposa_idle.png", mariposa_idle(), "animales")
    gen("caracol_idle.png", caracol_idle(), "animales")
    gen("caracol_walk.png", caracol_walk(), "animales")
    gen("pajaro_idle.png", pajaro_idle(), "animales")
    gen("pajaro_sing.png", pajaro_sing(), "animales")

    # Retratos 16×16
    for name, (skin, hair, accent, style) in PERSONAJES.items():
        gen(f"portrait_{name}.png", make_portrait(skin, hair, accent, style), "retratos")

    # UI
    gen("btn_normal.png", btn_normal(), "ui")
    gen("btn_hover.png", btn_hover(), "ui")
    gen("btn_press.png", btn_press(), "ui")
    gen("dialog_bubble.png", dialog_bubble(), "ui")
    gen("hud_brújula.png", hud_brújula(), "ui")
    gen("icon_seed.png", icon_seed(), "ui")
    gen("icon_flower.png", icon_flower(), "ui")
    gen("icon_tool.png", icon_tool(), "ui")
    gen("menu_tree.png", menu_tree(), "ui")

    # Objetos
    gen("seed.png", seed(), "objetos")
    gen("watercan.png", watercan(), "objetos")
    for color_name, color in [("rojo",C["rojo_pasion"]), ("rosa",C["rosa_flor"]),
                              ("violeta",C["violeta_lejano"]), ("naranja",C["naranja_sol"]),
                              ("oro",C["oro_trigo"])]:
        gen(f"glowing_flower_{color_name}.png", glowing_flower(color), "objetos")
    gen("stone.png", stone(), "objetos")
    gen("feather.png", feather(), "objetos")
    gen("music_note.png", music_note(), "objetos")

    print(f"✓ Generados {len(results)} sprites")
    for r in results:
        print(f"  → {r}")
    return results

if __name__ == "__main__":
    generate_all()
