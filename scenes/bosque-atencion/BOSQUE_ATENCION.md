# B2b - Bosque Atención

## Dimensiones
- **Grid:** 50x40 tiles (1600x1280 px)
- **Tile size:** 32x32 px
- **Z-index:** 0-3 (capas de foliage)

## Tilemap Layout

### Capa Suelo
- Pasto oscuro con variaciones (hojarasca, musgo)
- Parches de tierra (10-15 áreas)
- Charco de agua (4) intermitentes

### Capa Árboles (Z-index 2)
- **Densidad:** Alta
- **Layout:** Agrupaciones de 4-6 tiles con pasillos estrechos
- 60% del mapa cubierto por canopy (efecto neblina)
- Claros estratégicos donde ocurren puzzles

### Capa Neblina (Z-index 3)
- Neblina animada (shader con ruido de Perlin)
- Se disipa al completar puzzles en cada área
- Oscurece bordes del mapa (efecto vignette)

### Layout Esquemático
```
N ← Bosque Atención

[Á][Á][Á][Á][F][F][Á][Á][Á][Á][Á]... (50)
[Á][Á][C][C][C][C][C][Á][Á][Á][Á]
[Á][C][E][E][E][E][E][C][Á][Á][Á]
[Á][C][E][S][S][S][E][C][Á][Á][Á]
   ⋮  Zona Central     ⋮
[Á][Á][Á][Á][C][Á][Á][Á][Á][Á][Á]
[Á][Á][Á][Á][C][Á][Á][Á][Á][Á][Á]
   ↓ conexión Jardín Central (19,0)
```
- Á = Árbol, F = Flores puzzle, C = Camino, S = Zona Stroop
- E = Zona Flanker/CPT

## Puzzles

### 1. Flores Stroop (3-6 años)
- **Ubicación:** 3 claros en zonas (10,8), (30,5), (20,30)
- **Mecánica:** Flor RGB que cambia de color cada 3s
- **Tarea:** Tocar flor del color que dice el texto (no el color que ves)
- **Dificultad:** 3 colores (3-6), 5 colores (6-12), 5 colores + distractores (12-17+)
- **Feedback:** Pétalos vuelan si acierta, se marchitan si falla

### 2. Flechas Flanker (6-12 años)
- **Ubicación:** Claro central (25, 20)
- **Layout:** 5x5 losetas en el piso con flechas grabadas
- **Tarea:** Caminar en dirección de la flecha central ignorando las laterales
- **Visual:** Flechas se iluminan en secuencia
- **Dificultad:** Congruente (3 flechas) → Incongruente (5 flechas con distractor)
- **Score:** Precisión + tiempo de respuesta

### 3. Estrellas CPT (12-17+ años)
- **Ubicación:** Dispersas en árboles (15 puntos)
- **Mecánica:** Estrellas brillan 500ms cada 2-5s (intervalo variable)
- **Tarea:** Presionar cuando aparezca estrella objetivo (no otras)
- **Target ratio:** 40% objetivo, 60% distractores
- **Duración:** 3 minutos, sin pausa
- **Score:** d' (sensibilidad), tiempo de reacción, falsas alarmas

## NPC

### Zorro Guía
- **Posición:** Entrada sur (19, 39)
- **Ruta:** Patrulla camino principal en loop
- **Apariencia:** Zorro rojo con bufanda verde
- **Diálogo:**
  - 1er encuentro: "Aquí las flores mienten y las estrellas juegan al escondite. Observa bien."
  - Hint: "¿De qué color era la flor cuando dijiste que era roja?"
  - Completado: "Has visto más allá de las apariencias. El camino al Jardín se ilumina."
- **Movimiento:** Waypoints con pausas de 3s

## Conexiones

| Zona | Dirección | Tile | Tipo |
|------|-----------|------|------|
| B2a Jardín Central | Sur | 19-21, 39 | Puerta arco de ramas |
| B2c Río Memoria | Este | 49, 15-17 | Puente de raíces |
| B2e Valle Lenguaje | NE | 49, 0-2 | Túnel de enredaderas |

## Eventos Trigger

### AT-1: Niebla inicial
- Entrada por sur: niebla cubre 80%, visibilidad 4 tiles
- Por cada puzzle completado: niebla se reduce 20%
- Todos completos: niebla desaparece, sol entra

### AT-2: Flora Reacción
- Flores reaccionan a presencia del jugador:
  - Se cierran si el jugador corre
  - Se abren si está quieto 2s
  - Siguen al jugador con la mirada (rotación)

### AT-3: CPT Fail
- Si jugador falla 5 estrellas seguidas → Zorro aparece y da hint
- Cooldown del hint: 30s

## Dificultad por Edad

| Edad | Stroop | Flanker | CPT | Tiempo total |
|------|--------|---------|-----|-------------|
| 3-6 | 3 colores, sin texto | 3 flechas congruentes | No activo | 5 min |
| 6-12 | 5 colores, texto simple | 5 flechas mixtas | 1 min, fácil | 10 min |
| 12-17 | 5 colores + distractor | 7 flechas, 80% incongruente | 2 min, medio | 15 min |
| 17+ | 7 colores + emociones | 9 flechas, random | 3 min, difícil | 20 min |

## Walkability (C2)
- 45% caminable (alta densidad de árboles)
- Pasillos de 2-3 tiles
- Zonas de puzzle: áreas abiertas de 7x7 mínimo
- No hay agujeros ni death zones
- Speed: 0.8x (terreno irregular)
