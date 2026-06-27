# B2g - Gruta Visual

## Dimensiones
- **Grid:** 45x45 tiles (1440x1440 px)
- **Tile size:** 32x32 px
- **Z-index:** 0-3

## Tilemap Layout

### Capa Suelo
- Roca de caverna (3 variantes oscuras)
- Cristales en el suelo (decorativos + interactivos)
- Arena brillante en algunas secciones

### Capa Paredes (Z-index 2)
- Paredes de roca con bordes irregulares
- Formaciones de estalactitas/estalagmitas
- Muros que se abren al resolver puzzles

### Capa Espejos (Z-index 1)
- 5 espejos grandes distribuidos
- Reflejan áreas lejanas (portal visual)
- Se empañan/limpian con puzzles

### Capa Cristales (Z-index 0, glow overlay)
- Cristales de 6 colores (rojo, azul, verde, amarillo, púrpura, blanco)
- Brillo animado (frecuencia variable por color)

### Layout Esquemático
```
[E1][C][ ][ ][E2][ ][C][ ][ ]...
[ ][ ][R][R][ ][ ][ ][ ][C][ ]
[ ][C][ ][ ][ ][E3][ ][ ][ ][ ]
[ ][ ][ ][L][L][L][ ][C][ ][ ]
[E4][ ][L][ ][ ][L][ ][ ][E5]
[ ][C][L][ ][ ][L][ ][C][ ][ ]
[ ][ ][ ][L][L][L][ ][ ][ ][ ]
  ... conexiones ...
```
- E = Espejo, C = Cristal interactivo
- L = Laberinto, R = Rotación

### Zonas Clave

| Zona | Posición | Función |
|------|----------|---------|
| Entrada Norte | (20, 0)-(22,0) | Desde Torre/Gruta |
| Cámara Espejo #1 | (5, 5) | Rotación de cristales |
| Cámara Espejo #2 | (38, 8) | Laberinto reflejado |
| Cámara Espejo #3 | (15, 22) | Puzzles visuales |
| Cámara Espejo #4 | (5, 38) | Discriminación visual |
| Cámara Espejo #5 (final) | (38, 38) | Puzzle combinado |
| Zorro NPC | (22, 22) | Centro de la gruta |

## Puzzles

### 1. Rotación de Cristales (3-12 años)
- **Ubicación:** Cámara Espejo #1 + dispersos
- **Mecánica:** Cristal flotante que rota en 3D
- **Tarea:** Girar hasta que coincida con forma objetivo
- **Input:** Rotación por pasos (45°), botón de confirmación

| Edad | Ejes de rotación | Formas | Pasos máx |
|------|-----------------|--------|-----------|
| 3-6 | 1 eje (2D) | 2 formas | 4 |
| 6-12 | 2 ejes | 4 formas | 6 |
| 12-17 | 2 ejes + mirror | 6 formas | 8 |
| 17+ | 3 ejes + mirror | 8 formas | 12 |

### 2. Laberintos Reflejados (6-17+ años)
- **Ubicación:** Cámara Espejo #2 (38, 8)
- **Mecánica:** Laberinto que se ve en espejo está INVERTIDO
- **Tarea:** Navegar el laberinto viendo SOLO el reflejo
- **Visual:** Espejo ocupa media pantalla, cámara dividida

| Edad | Laberinto tamaño | Espejos | Tiempo |
|------|-----------------|---------|--------|
| 3-6 | 5x5 | 1 (sin invertir) | ∞ |
| 6-12 | 7x7 | 1 (invertido) | 60s |
| 12-17 | 9x9 | 2 (invertido + rotado) | 45s |
| 17+ | 11x11 | 3 (invertido + rotado + escala) | 30s |

### 3. Discriminación Visual (3-17+ años)
- **Ubicación:** Cámara Espejo #4 + pasillos
- **Mecánica:** Grupo de cristales similares
- **Tarea:** Encontrar el que es diferente
- **Variaciones:** Color, forma, tamaño, orientación

| Edad | Items | Diferencias | Tiempo |
|------|-------|-------------|--------|
| 3-6 | 4 items | 2 diferencias notables | 10s |
| 6-12 | 6 items | 1 diferencia sutil | 8s |
| 12-17 | 8 items | 1 diferencia muy sutil | 6s |
| 17+ | 10 items | Diferencia + cambio contexto | 5s |

### 4. Puzzle Final: Espejo Total
- **Ubicación:** Cámara Espejo #5 (38, 38)
- **Mecánica:** 5 espejos deben alinearse para enfocar haz de luz
- **Tarea:** Rotar cada espejo al ángulo correcto
- **Feedback visual:** Haz de luz que recorre la gruta
- **Completado:** Luz ilumina toda la gruta, revela cristal secreto

## NPC

### Zorro
- **Posición:** Centro (22, 22), se mueve entre espejos
- **Apariencia:** Zorro plateado/azul, ojos brillantes
- **Movimiento:** Teletransporta entre espejos (aparición/desaparición)
- **Diálogo:**
  - 1er encuentro: "La luz viaja recta, pero tú no. ¿Qué ves cuando te miras al espejo? No siempre es lo que esperas."
  - Hint: "Gira el cristal hasta que sientas que encaja. Tu ojo lo sabe antes que tu mente."
  - Completado: "Has visto la gruta desde todos los ángulos. Nada escapa a tu mirada ahora."
  - Especial: "No todos los espejos muestran la realidad. Algunos muestran lo que podría ser."

## Conexiones

| Zona | Dirección | Tile | Tipo |
|------|-----------|------|------|
| B2a Jardín Central | Este | (44, 22)-(44,24) | Puerta de cristal |
| B2e Valle Lenguaje | Oeste | (0, 15)-(0,17) | Caverna de letras |
| B2f Torre Matemáticas | Norte | (20, 0)-(22,0) | Escalera ascendente |
| B2h Camino Velocidad | Sur | (20, 44)-(22,44) | Túnel de espejos |

## Eventos Trigger

### GR-1: Reflejos
- Al acercarse a espejo: aparece versión reflejada del jugador
- Reflejo imita movimientos con delay de 0.5s
- Puzzle ocasional: reflejo hace algo diferente, hay que copiarlo

### GR-2: Oscuridad
- Gruta tiene ciclo de luz (cristales brillan rítmicamente)
- Cada 15s: pulso de oscuridad de 2s (solo brillan cristales)
- Durante oscuridad: ciertos puzzles solo visibles entonces

### GR-3: Cristal Secreto
- Al completar puzzle final: cristal central emerge del suelo
- Al tocarlo: visión de todas las zonas simultáneamente
- Desbloquea: atajo a cualquier zona desde gruta

## Dificultad por Edad

| Edad | Rotación | Laberinto Reflejado | Discriminación | Tiempo |
|------|----------|--------------------|---------------|--------|
| 3-6 | 1 eje, guiado | 5x5 sin invertir | 4 items | 8 min |
| 6-12 | 2 ejes | 7x7 invertido | 6 items | 12 min |
| 12-17 | 2 ejes + mirror | 9x9 2 espejos | 8 items | 18 min |
| 17+ | 3 ejes + mirror | 11x11 todo | 10 items | 25 min |

## Walkability (C2)
- 50% caminable (muchas paredes de roca)
- Pasillos de 2-3 tiles
- Espejos son sólidos (no se atraviesan)
- Cristales: decorativos (chocan) e interactivos (se tocan)
- Sin muerte, sin caídas
- Speed: 0.9x (terreno irregular)
