# B2e - Valle Lenguaje

## Dimensiones
- **Grid:** 55x35 tiles (1760x1120 px)
- **Tile size:** 32x32 px
- **Z-index:** 0-2

## Tilemap Layout

### Capa Suelo
- Prado de flores silvestres (multicolor)
- Colinas suaves (gradiente de 3 tonos de verde)
- Arroyo pequeño serpenteante (2-3 tiles ancho)

### Capa Elementos
- **Libros gigantes:** 3 libros abiertos (5x7 tiles cada uno) como plataformas
- **Árboles de letras:** 6 árboles cuyas hojas forman letras
- **Palabras flotantes:** Partículas con forma de sílabas
- **Estantes:** 2 estructuras con libros apilables

### Layout Esquemático
```
[Árbol A][Árbol B][Árbol C]   ... fila 0-10
  [Libro1][  ]  [Estante1]
[Árbol D]  [Libro2]  [Árbol E]
  [Rimas]  [Centro]  [Sílabas]
[Árbol F]  [Libro3]   [Estante2]
    ... conexión Bosque/Jardín ...
```

### Zonas Clave

| Zona | Posición | Tema |
|------|----------|------|
| Entrada Sur | Fila 30-34 | Bienvenida del Pájaro |
| Árbol de Rimas | (10, 12) | Rimas en canopy |
| Gran Libro #1 | (18, 20) | Vocabulario |
| Gran Libro #2 | (30, 15) | Gramática |
| Gran Libro #3 | (40, 25) | Narrativa |
| Estante Silábico | (45, 8) | Sílabas |
| Claro Central | (25, 18) | Pájaro NPC |

## Puzzles

### 1. Rimas en Árboles (3-12 años)
- **Ubicación:** 6 árboles alrededor del valle
- **Mecánica:** Árbol muestra una palabra en su tronco
- **Tarea:** Tocar la hoja con la palabra que rima
- **Visual:** Hojas brillan, palabras aparecen con glow

| Edad | Palabras | Opciones | Tipo de rima |
|------|----------|----------|-------------|
| 3-6 | 3 letras | 2 opciones | Rima consonante perfecta (sol-gol) |
| 6-12 | 4-5 letras | 4 opciones | Rima asonante + consonante |
| 12-17 | 6+ letras | 5 opciones | Rima compleja + aliteración |
| 17+ | Palabras compuestas | 6 opciones | Multirrima + métrica |

### 2. Sílabas en el Viento (6-17+ años)
- **Ubicación:** Estante Silábico (45, 8)
- **Mecánica:** Sílabas flotan como hojas al viento
- **Tarea:** Atrapar sílabas en orden para formar palabra
- **Visual:** Partículas con texto, estela de luz

| Edad | Sílabas por palabra | Velocidad | Distractores |
|------|-------------------|-----------|-------------|
| 3-6 | 2 sílabas (CV) | Lenta | No |
| 6-12 | 2-3 sílabas | Media | 1 distractor |
| 12-17 | 3-4 sílabas | Rápida | 2 distractores |
| 17+ | 4-5 sílabas (CCV/CCVC) | Muy rápida | 3 distractores + ruido |

### 3. Completar Historia (12-17+ años)
- **Ubicación:** Gran Libro #3 (40, 25)
- **Mecánica:** Libro muestra historia con espacios en blanco
- **Tarea:** Seleccionar palabra correcta para completar
- **Opción múltiple:** 4 opciones con distractores semánticos

| Edad | Longitud texto | Blancos | Tipo |
|------|--------------|---------|------|
| 3-6 | 1 oración | 1 | Imagen + palabra |
| 6-12 | 2-3 oraciones | 2-3 | Párrafo simple |
| 12-17 | Párrafo (50-80 pal) | 3-5 | Texto expositivo |
| 17+ | Texto largo (100+ pal) | 5-7 | Texto narrativo + inferencia |

## NPC

### Pájaro
- **Posición:** Claro Central (25, 18) y posado en libros
- **Apariencia:** Pájaro azul/amarillo, plumaje con letras
- **Movimiento:** Vuela entre los 3 libros grandes + árboles
- **Diálogo:**
  - 1er encuentro: "Las palabras construyen mundos. Cada libro que abras te dará una nueva palabra. ¿Cuál será la tuya?"
  - Hint: "La rima es el eco de las letras. Escucha bien."
  - Completado: "Has llenado el valle de historias. Ahora el Jardín entero tiene voz."

## Conexiones

| Zona | Dirección | Tile | Tipo |
|------|-----------|------|------|
| B2a Jardín Central | Sur | (25, 34)-(27,34) | Arco de letras |
| B2b Bosque Atención | Oeste | (0, 10)-(0,12) | Túnel de enredaderas |
| B2d Montaña Razonamiento | Oeste | (0, 0)-(0,2) | Túnel de viento |
| B2f Torre Matemáticas | Sur | (45, 34)-(47,34) | Puente de sílabas |
| B2g Gruta Visual | Este | (54, 20)-(54,22) | Caverna de letras |

## Eventos Trigger

### VL-1: Palabra del Día
- Al entrar: una palabra especial flota sobre el valle
- Si el jugador la toca: +10 puntos bonus
- Palabra cambia cada día real (seed = date)
- Efecto: partículas doradas, sonido de campana

### VL-2: Eco Literario
- Después de completar 3 puzzles: los libros cantan (texto a voz)
- Cita aleatoria de literatura infantil
- Bonus: desbloquea entrada decorativa

### VL-3: Tormenta de Letras
- Si el jugador falla 3 veces en sílabas:
- Animación: viento, letras vuelan, se reordenan
- Pájaro aparece: "A veces las letras se desordenan. Respira y vuelve a intentarlo."

## Dificultad por Edad

| Edad | Rimas | Sílabas | Historia | Tiempo |
|------|-------|---------|----------|--------|
| 3-6 | 3 pares, guiado visual | Solo 2 sílabas | Imagen + 1 palabra | 8 min |
| 6-12 | 5 pares | 3 sílabas, 1 distractor | 2-3 blancos | 12 min |
| 12-17 | 7 pares + aliteración | 4 sílabas, 2 distractores | Párrafo completo | 18 min |
| 17+ | 10 pares + creación | 5 sílabas, 3 distractores | Texto + inferencia | 25 min |

## Walkability (C2)
- 70% caminable
- Libros gigantes: plataformas elevadas (subir por raíces)
- Arroyo: cruce por piedras (3 puntos)
- Sin muerte, sin caídas
- Speed: 1.0x
