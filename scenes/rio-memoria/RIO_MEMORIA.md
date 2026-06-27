# B2c - Río Memoria

## Dimensiones
- **Grid:** 45x35 tiles (1440x1120 px)
- **Tile size:** 32x32 px
- **Z-index:** 0-2

## Tilemap Layout

### Capa Suelo
- Pasto ribereño (verde claro)
- Arena/orilla en bordes del río
- Rocas decorativas

### Capa Río (Z-index 1 - sobre el jugador si está en agua)
- **Río serpenteante:** 4-6 tiles de ancho
- **Path:** S-curve ocupando 30% del mapa
- **Tile de agua:** Animado (3 frames, 0.5s loop)
- **Profundidad:** 2 variantes (superficial caminable, profunda bloqueada)

### Capa Puentes (Z-index 2)
- 5 puentes de piedra
- 3 puentes de madera
- Se iluminan al completar puzzles

### Layout Esquemático
```
← Jardín Central    (entrada 0,15-17)
                    ↓
[ ][ ][ ][R][R][R][ ][ ][ ][ ]...
[ ][P][ ][R][R][R][ ][P][ ][ ]
[R][R][R][R][R][ ][ ][ ][ ][ ]
[R][R][R][R][R][ ][L][L][L][ ]
[ ][ ][P][ ][ ][ ][L][L][L][ ]
[ ][ ][ ][ ][P][ ][ ][ ][ ][ ]
  ... río serpentea ...
→ Bosque Atención (44, 20-22)
```
- R = Río, P = Puente, L = Luciérnagas (área puzzle)

## Puzzles

### 1. Luciérnagas Corsi
- **Ubicación:** 4 áreas junto al río
- **Mecánica:** Luciérnagas brillan en secuencia
- **Tarea:** Repetir la secuencia tocando en orden
- **Visual:** Luz pulsante con trail de partículas

| Área | Posición | Secuencia inicial | Longitud máx |
|------|----------|------------------|-------------|
| 1 | (5, 8) | 4 luciérnagas | 6 |
| 2 | (15, 12) | 5 luciérnagas | 8 |
| 3 | (30, 25) | 6 luciérnagas | 9 |
| 4 | (40, 30) | 7 luciérnagas | 10 |

### 2. Secuencia de Sonidos (Span)
- **Ubicación:** Caracol NPC + piedras musicales
- **Mecánica:** Caracol reproduce secuencia de notas en piedras
- **Tarea:** Tocar piedras en orden inverso (Backward Span)
- **Piedras:** 9 piedras distribuidas en medio círculo
- **Feedback:** Luz + tono por piedra

### 3. Pares de Memoria
- **Ubicación:** 3 zonas de descanso
- **Mecánica:** Hojas que al tocarse revelan un símbolo
- **Tarea:** Encontrar pares iguales
- **Grid:** 4x4 hojas
- **Tema:** Animales del Jardín

| Edad | Grid | Pares | Tiempo límite |
|------|------|-------|--------------|
| 3-6 | 3x2 | 3 | ∞ |
| 6-12 | 4x3 | 6 | 60s |
| 12-17 | 4x4 | 8 | 45s |
| 17+ | 5x4 | 10 | 30s |

## NPC

### Caracol
- **Posición:** (22, 17) — curva central del río
- **Apariencia:** Caracol azul con concha espiral brillante
- **Movimiento:** Estático sobre una piedra
- **Diálogo:**
  - 1er encuentro: "El río fluye solo en una dirección, pero la memoria viaja en ambas. ¿Puedes recordar el camino de vuelta?"
  - Hint: "Las luciérnagas bailan al mismo compás que tus recuerdos. Obsérvalas con cuidado."
  - Completado: "Has nadado contracorriente y has vuelto. La memoria es un músculo; lo has ejercitado bien."

## Conexiones

| Zona | Dirección | Tile | Tipo |
|------|-----------|------|------|
| B2a Jardín Central | Oeste | (0, 15-17) | Puente de piedra |
| B2b Bosque Atención | Norte | (20, 0)-(22,0) | Cascada |
| B2f Torre Matemáticas | Sur | (30, 34)-(32,34) | Túnel de raíces |
| B2d Montaña Razonamiento | Este | (44, 10)-(44,12) | Puente colgante |

## Eventos Trigger

### RM-1: Flow del río
- Río tiene corriente visual (partículas)
- Si jugador está en agua superficial: empujado suavemente downstream
- Velocidad: 0.2 tiles/s

### RM-2: Memo-Flash
- Al completar secuencia de luciérnagas: flashback visual de 0.5s
- Muestra imagen de otra zona (preview desbloqueable)
- 4 flashbacks = 4 zonas diferentes

### RM-3: Sincronía
- Si el jugador completa 2 puzzles seguidos sin error: modo "flow"
- Efecto: partículas doradas, música se intensifica, speed 1.2x

## Dificultad por Edad

| Edad | Corsi | Span | Pares | Tiempo total |
|------|-------|------|-------|-------------|
| 3-6 | 3 items, ayuda visual | Solo forward, 3 items | 3 pares | 8 min |
| 6-12 | 5 items | Forward + backward 4 items | 6 pares | 12 min |
| 12-17 | 7 items | Backward 6 items | 8 pares | 15 min |
| 17+ | 9 items | Dual task (forward+backward) | 10 pares | 20 min |

## Walkability (C2)
- 60% caminable (río ocupa 30%, rocas 10%)
- Puentes: únicos cruces seguros
- Agua superficial: 5 tiles cruce lento (0.5x speed)
- Agua profunda: bloqueada visualmente (oscura)
- Speed: 0.9x base
