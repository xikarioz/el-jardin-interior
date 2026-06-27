# B2d - Montaña Razonamiento

## Dimensiones
- **Grid:** 50x45 tiles (1600x1440 px)
- **Tile size:** 32x32 px
- **Z-index:** 0-4

## Tilemap Layout

### Capa Suelo
- Roca gris con variaciones (cobble, piedra lisa, gravilla)
- Musgo en zonas altas
- Nieve en pico (fila 0-5)

### Capa Elevación (Z-index 1-3)
- Sistema de 5 alturas con escaleras/rampas
- Plataformas flotantes (sombra proyectada)
- Acantilados con caída (respawn en checkpoint anterior)

| Nivel | Altura (tiles) | Color |
|-------|---------------|-------|
| Base | 0 | Gris oscuro |
| Bajo | 4 | Gris medio |
| Medio | 8 | Gris claro |
| Alto | 12 | Blanco/gris |
| Pico | 16 | Blanco/nieve |

### Capa Plataformas
- Layout escalonado
- 4 secciones principales conectadas por escaleras de piedra
- Puentes de cuerda (3)

### Layout Esquemático (perfil vertical)
```
  [N][N][N][ ]  ─── Pico (WCST final)
  [A][A][A][A][A]  ─── Zona BART
     [M][M][M][M][M]  ─── WCST inicial
[P][P][P][P][P]  ─── Entrada desde Río/Valle
[B][B][B][ ]  ─── Base
```

### Zonas Clave

1. **Base** (filas 35-44): Entrada, bienvenida Búho
2. **Ascenso Sur** (filas 25-34): Carteles WCST #1
3. **Meseta Central** (filas 15-24): Globos BART + WCST #2
4. **Ascenso Norte** (filas 5-14): Carteles WCST #3
5. **Pico** (filas 0-4): WCST final, vista panorámica

## Puzzles

### 1. Carteles WCST (Wisconsin Card Sorting)
- **Ubicación:** 4 carteles en ascenso
- **Mecánica:** Regla de clasificación cambia sin aviso
- **Tarea:** Colocar objeto en categoría correcta

| Cartel | Posición | Regla inicial | Regla cambia a |
|--------|----------|--------------|----------------|
| #1 | (10, 30) | Por color | Por forma |
| #2 | (25, 20) | Por forma | Por número |
| #3 | (40, 10) | Por número | Por color |
| #4 (final) | (25, 2) | Por color | Cada 3 aciertos cambia |

- **Visual:** Cartel de piedra con símbolos tallados que brillan
- **Feedback:** Acierto = cartel se ilumina verde; fallo = rojo + temblor
- **Aciertos para pasar:** 5 consecutivos por cartel

### 2. Globos BART (Balloon Analogue Risk Task)
- **Ubicación:** Meseta Central (25, 18)
- **Mecánica:** Globo que se infla, puede explotar
- **Tarea:** Inflar para ganar puntos, pero recoger antes que explote

| Parámetro | 3-6 | 6-12 | 12-17 | 17+ |
|-----------|-----|------|-------|-----|
| Infladas máx | 3 | 5 | 8 | 12 |
| Prob. explosión | 40% | 30% | 25% | 20% |
| Globos simultáneos | 1 | 2 | 3 | 4 |
| Puntos por inflada | 1 | 2 | 5 | 10 |

- **Visual:** Globo colorido que se expande, venas aparecen al 80%
- **Sonido:** Inflado que se tensa progresivamente
- **Explosión:** Partículas + sonido sorpresa (no violenta)

### 3. Reglas Mixtas
- **Ubicación:** Pico (25, 2)
- **Mecánica:** Combinación WCST + BART
- **Tarea:** Inflar globos siguiendo regla cambiante
- **Feedback:** Globo muestra color FORMA antes de inflar
- **Dificultad:** 3-6: no aplica; 6-12: 3 reglas; 12-17+: 5 reglas

## NPC

### Búho
- **Posición:** Base (5, 40) y Pico (25, 2)
- **Apariencia:** Búho nevado con monóculo
- **Movimiento:** Vuela entre base y pico (trigger por puzzle completado)
- **Diálogo Base:**
  - "Las reglas no están escritas en piedra... aunque parezca que sí. ¿Sabes cuándo cambian?"
  - "Inflar un globo trae recompensa, pero todo tiene un límite. Saber cuándo parar es sabiduría."
- **Diálogo Pico (completado):**
  - "Has escalado el pensamiento mismo. Desde aquí ves todos los caminos del Jardín."
- **Hint:** Aparece si el jugador falla 3 veces seguidas en WCST

## Conexiones

| Zona | Dirección | Tile | Tipo |
|------|-----------|------|------|
| B2c Río Memoria | Sur | (30, 44)-(32,44) | Puente de raíces |
| B2e Valle Lenguaje | Este | (49, 25)-(49,27) | Túnel de viento |
| B2f Torre Matemáticas | Oeste | (0, 15)-(0,17) | Camino de piedra |
| B2a Jardín Central | Oeste (bajo) | (0, 35)-(0,37) | Escalera descendente |

## Eventos Trigger

### MZ-1: Cambio de Regla
- Cuando el jugador completa 5 aciertos en WCST
- Efecto: pantalla parpadea, cartel se rescribe con nuevo símbolo
- Sonido: campanada + susurro "La regla ha cambiado"

### MZ-2: Caída
- Si jugador cae de plataforma: respawn en checkpoint anterior
- Checkpoints: cada cartel WCST + entrada de meseta
- No hay muerte permanente, solo reposicionamiento

### MZ-3: Vista Pico
- Al llegar al pico: cámara zoom out (50 tiles extra)
- Muestra: todos los mapas conectados desde la altura
- Efecto emotional: música se abre a cuerdas completas

## Dificultad por Edad

| Edad | WCST | BART | Reglas Mixtas | Tiempo |
|------|------|------|--------------|--------|
| 3-6 | 2 categorías, guiado | 1 globo, 3 infladas máx | No | 8 min |
| 6-12 | 3 categorías | 2 globos, riesgo medio | 3 reglas | 12 min |
| 12-17 | 4 categorías | 3 globos, riesgo alto | 4 reglas | 18 min |
| 17+ | 4 categorías + random | 4 globos, riesgo variable | 5 reglas + dual task | 25 min |

## Walkability (C2)
- **Caminable:** 40% (pendientes + plataformas)
- **Puentes:** 3 puentes de cuerda (1 tile ancho, animación de balanceo)
- **Escaleras:** 5 tramos de 4-6 escalones
- **Caídas:** 8 puntos de caída (respawn con checkpoint)
- **Speed:** 0.7x en ascenso, 1.0x en plano, 1.2x en descenso
- No hay muerte — reposicionamiento suave
