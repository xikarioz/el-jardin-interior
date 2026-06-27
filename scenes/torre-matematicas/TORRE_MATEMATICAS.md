# B2f - Torre Matemáticas

## Dimensiones
- **Grid:** 35x50 tiles (1120x1600 px)
- **Tile size:** 32x32 px
- **Z-index:** 0-4 (vertical stacking)

## Tilemap Layout

### Capa Suelo
- Interior de torre: losetas de piedra numeradas
- Paredes de ladrillo con fórmulas grabadas
- Ventanas con vista al Jardín (fondo animado)

### Capa Espiral
- Torre en espiral ascendente
- 6 pisos conectados por escaleras de caracol
- Cada piso = 7-8 tiles de alto

| Piso | Altura (tiles) | Tema | Color |
|------|---------------|------|-------|
| Planta baja | 0-7 | Bienvenida, Mariposa | Crema |
| Piso 1 | 8-15 | Sumas + conteo | Amarillo |
| Piso 2 | 16-23 | Restas + comparación | Naranja |
| Piso 3 | 24-31 | Multiplicación | Rojo |
| Piso 4 | 32-39 | División + fracciones | Púrpura |
| Piso 5 (terraza) | 40-49 | Puzzle final, vista | Azul cielo |

### Layout Esquemático (vista 2D de cada piso)
```
Piso 2 (ejemplo) ─ 16x16 tile floor
[#][#][#][#][#][#][#][#][#][#]...
[#][ ][ ][P][P][P][ ][ ][ ][#]
[#][ ][ ][ ][ ][ ][ ][E][ ][#]
[#][ ][S][S][S][ ][ ][ ][ ][#]
[#][ ][ ][ ][ ][ ][ ][ ][ ][#]
[#][#][#][#][#][#][#][#][ ][ ]
                                  ↑ Escalera al piso 3
```
- # = Pared, P = Puente numérico
- S = Piedras puzzle, E = Escalera

## Puzzles

### 1. Puentes Numéricos (3-12 años)
- **Ubicación:** Cada piso, conector entre secciones
- **Mecánica:** Puente flotante con números faltantes
- **Tarea:** Colocar número correcto para completar secuencia
- **Visual:** Puente de luz, número se materializa al arrastrarlo

| Edad | Secuencia | Operación | Rango |
|------|-----------|-----------|-------|
| 3-6 | 1, 2, _, 4 | Conteo | 1-10 |
| 6-12 | 3, 6, _, 12 | Suma/multiplicación | 1-100 |
| 12-17 | 2, 4, 8, _, 32 | Potencias | 1-1000 |
| 17+ | Fibonacci/primates | Secuencia compleja | 1-∞ |

### 2. Piedras que Suman (6-17+ años)
- **Ubicación:** Cada piso, 3-5 piedras
- **Mecánica:** Piedras con números, al pisarlas suman
- **Tarea:** Llegar al número objetivo pisando las piedras correctas
- **Restricción:** No repetir piedra, orden importa

| Edad | Piedras | Objetivo | Tiempo |
|------|---------|----------|--------|
| 3-6 | 3 (2 opciones) | ≤ 5 | ∞ |
| 6-12 | 5 (sumas simples) | 10-20 | 30s |
| 12-17 | 7 (sumas + restas) | 25-50 | 20s |
| 17+ | 9 (ops combinadas) | 50-100 | 15s |

### 3. Torre de Secuencias (12-17+ años)
- **Ubicación:** Piso 5 terraza (25, 42)
- **Mecánica:** Panel con secuencia numérica incompleta
- **Tarea:** Completar los siguientes 3 términos
- **Tipos de secuencia:**
  - Aritmética (+n)
  - Geométrica (×n)
  - Fibonacci-like
  - Patrón posicional

### 4. Puzzle Final: Equilibrio
- **Ubicación:** Terraza (17, 45)
- **Mecánica:** Balanza con pesos de números
- **Tarea:** Balancear la ecuación (ambos lados igual valor)
- **Visual:** Balanza dorada, números como gemas
- Al completar: ventana se abre, luz entra, vista completa del Jardín

## NPC

### Mariposa
- **Posición:** Vuela entre pisos, descansa en escaleras
- **Apariencia:** Mariposa morada/dorada, alas con números
- **Movimiento:** Waypoints verticales, sigue al jugador si está cerca
- **Diálogo:**
  - 1er encuentro: "Los números tienen su propio lenguaje. La torre los cuenta todos."
  - Piso 3: "Multiplicar es sumar muchas veces. Como las alas de una mariposa batiendo juntas."
  - Hint: "Observa el patrón. El número que falta siempre está escondido entre los que ves."
  - Completado: "Has subido cada escalón numérico. Desde aquí, todo suma."

## Conexiones

| Zona | Dirección | Tile | Tipo |
|------|-----------|------|------|
| B2a Jardín Central | Oeste (base) | (0, 5)-(0,7) | Puerta de arco |
| B2c Río Memoria | Sur (base) | (15, 49)-(17,49) | Túnel de raíces |
| B2d Montaña Razonamiento | Este (piso 3) | (34, 28)-(34,30) | Puente aéreo |
| B2e Valle Lenguaje | Norte (base) | (15, 0)-(17,0) | Puente de sílabas |
| B2h Camino Velocidad | Este (base) | (34, 8)-(34,10) | Túnel de luz |

## Eventos Trigger

### TM-1: Ascenso
- Al subir escalera: contador de piso + efecto parallax
- Vista desde ventana cambia según altura
- Música se vuelve más compleja (se añaden capas)

### TM-2: Número Especial
- Cada piso tiene un número oculto en decoración
- Si el jugador lo encuentra y toca: puzzle bonus
- Pista: brilla tenuemente cada 5s

### TM-3: Caída
- Si el jugador cae desde un puente: respawn en entrada del piso
- Sin muerte, con animación de "resbale" y sonido de campana
- 2s de invulnerabilidad post-respawn

## Dificultad por Edad

| Edad | Puentes | Piedras | Secuencias | Tiempo |
|------|---------|---------|-----------|--------|
| 3-6 | Conteo 1-5 | 2 piedras, 1 op | No | 8 min |
| 6-12 | Suma/resta 1-20 | 4 piedras, 2 ops | Simple | 12 min |
| 12-17 | Mult/div 1-100 | 6 piedras, 3 ops | 3 tipos | 18 min |
| 17+ | Secuencias complejas | 8 piedras, todo ops | 5 tipos + creativo | 25 min |

## Walkability (C2)
- 55% caminable
- Escaleras conectan pisos (4 tiles de alto cada tramo)
- Puentes numéricos: solo caminables si acierta puzzle
- Sin muerte en caídas de puente (respawn suave)
- Speed: 1.0x en pisos, 0.6x en escaleras
