# B2a - Jardín Central (Hub)

## Dimensiones
- **Grid:** 40x30 tiles (32x32px = 1280x960 px)
- **Tile size:** 32x32 px
- **Z-index:** 0

## Tilemap Layout

### Capa Suelo (Tierra/Pasto)
```
  0 1 2 3 4 5 6 7 8 9 ... 39
0 [P][P][P][P][P][P][P][P][P][P] ...
1 [P][P][P][P][P][P][P][P][P][P]
2 [P][P][P][P][P][P][P][P][P][P]
3 [P][P][P][C][C][C][P][P][P][P]  ← C = camino central
...  hasta fila 29
```

### Capa Caminos
- **Anillo circular** alrededor del Árbol (radio 8 tiles)
- **8 radios** que parten del anillo hacia los bordes del mapa
- Cada radio es de 3 tiles de ancho
- Color del camino varía por zona destino (azul→río, verde→bosque, etc.)

### Capa Agua
- Estanque pequeño (6x4 tiles) en esquina NO
- Fuente central (3x3) al lado del Árbol

### Capa Decoración
- Flores: 12 grupos de 3-5 tiles
- Arbustos en bordes
- Bancos de piedra (4)
- Farolas (6)

## Árbol del Saber
- **Posición:** Centro exacto (19, 14)
- **Tamaño:** 7x9 tiles
- **Glow:** Efecto de partículas pulsantes (verde-dorado)
- **Alrededor:** Círculo de tierra 5x5, agua 7x7
- **Interacción:** Al acercarse, reproduce sonido ambiente + mensaje "Las raíces conectan todo conocimiento"

## NPCs

### Tortuga (Bienvenida)
- **Posición:** (5, 14) — entrada sur
- **Apariencia:** Tortuga anciana con lentes, bastón
- **Diálogo:** "Bienvenido al Jardín Interior. Cada sendero aguza una facultad de tu mente. Elige con sabiduría."
- **Spritesheet:** 4 frames idle, animación hablar
- **Movimiento:** Estático (sentada en banco)

### Mariposa (guía tutorial)
- **Posición:** Vuela alrededor del Árbol
- **Path:** Órbita elíptica (rx=6, ry=4)
- **Diálogo opcional:** Ofrece tour rápido

## Conexiones a Otras Zonas

| Zona | Dirección | Puerta (tile) | Color camino |
|------|-----------|---------------|-------------|
| B2b Bosque Atención | Norte | (19, 0) | Verde esmeralda |
| B2c Río Memoria | Este | (39, 14) | Azul profundo |
| B2d Montaña Razonamiento | NO | (6, 0) | Gris pizarra |
| B2e Valle Lenguaje | NE | (33, 0) | Amarillo oro |
| B2f Torre Matemáticas | Oeste | (0, 14) | Púrpura |
| B2g Gruta Visual | Sur | (19, 29) | Naranja |
| B2h Camino Velocidad | SE | (33, 29) | Rojo coral |
| Tutorial (T1) | SO | (6, 29) | Blanco |

## Eventos Trigger

### Trigger T1: Primera Entrada
- **Condición:** Jugador entra al mapa por primera vez
- **Acción:** Cámara lenta zoom out, texto "EL JARDÍN INTERIOR" con fade, Tortuga habla

### Trigger T2: Desbloquear Zona
- **Condición:** Completar puzzle en zona secundaria
- **Acción:** Árbol emite pulso de luz, camino se ilumina en esa dirección
- **Variable:** zona_[nombre]_desbloqueada = true

### Trigger T3: Todas las Zonas
- **Condición:** 7 zonas completadas
- **Acción:** Árbol florece, cutscene final, desbloquea zona secreta (B3)

## Dificultad por Edad

| Edad | Complejidad | Adaptaciones |
|------|-------------|-------------|
| 3-6 | Tutorial forzado, íconos grandes | NPC Tortuga da misiones simples de exploración |
| 6-12 | Libre exploración, hint system | Mapas con brújula |
| 12-17 | Sin tutorial forzado, retos opcionales | Puzzle de combinación de zonas |
| 17+ | Speedrun mode, lore profundo | Lore oculto en inscripciones del Árbol |

## Música
- **BGM:** Ambiente cálido (G menor, 80 BPM)
- **Stems:**
  - Stem1: Arpa (loop 8 compases)
  - Stem2: Flauta dulce (entra al explorar)
  - Stem3: Cuerdas (entra cerca del Árbol)
  - Stem4: Percusión suave (entra de noche/mazmorra)
- **Transiciones:** Crossfade de 2s entre stems

## Walkability (C2)
- 90% del mapa caminable
- Obstáculos: agua, arbustos densos, árbol decorativo
- Zonas bloqueadas: caminos sin desbloquear (cubiertos de niebla/pared invisible)
- Speed: 1.0x (base)
