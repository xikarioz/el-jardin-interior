# B2h - Camino Velocidad + Socioemocional

## Dimensiones
- **Grid:** 60x20 tiles (1920x640 px — horizontal scope)
- **Tile size:** 32x32 px
- **Z-index:** 0-2

## Tilemap Layout

### Capa Suelo
- Camino de tierra (5 tiles ancho) que cruza el mapa horizontalmente
- Pasto a ambos lados (2-3 tiles)
- Flores decorativas en bordes

### Capa Objetos (Z-index 1)
- Obstáculos en el camino (20+ posiciones)
- Estímulos visuales laterales
- Postes de meta cada 15 tiles

### Capa Aire (Z-index 2)
- Pájaros voladores (decoración)
- Nubes de distracción
- Brillo de velocidad

### Layout Esquemático
```
  ↑ Jardín        ↑ Gruta
  Central         Visual
  (tile 18,0)     (tile 40,0)

[O][ ][ ][E][ ][O][ ][E][ ][O]... fila 2 (arriba)
[ ][C][ ][ ][ ][ ][ ][ ][ ][ ]  fila 3 (camino)
[ ][ ][ ][ ][ ][ ][ ][ ][ ][ ]  fila 4 (camino)
[ ][ ][ ][ ][ ][ ][ ][ ][ ][ ]  fila 5 (camino)
[ ][C][ ][ ][ ][ ][ ][ ][ ][ ]  fila 6 (camino)
[O][ ][E][ ][O][ ][ ][E][ ][O]... fila 7 (abajo)
```
- C = Camino, O = Obstáculo
- E = Estímulo (rápido)

### Secciones del Camino (12 tiles cada una)

| Sección | Tiles X | Tema |
|---------|---------|------|
| Entrada | 0-11 | Zona de aclimatación (sin obstáculos) |
| Velocidad 1 | 12-23 | Obstáculos simples (piedras) |
| Emociones | 24-35 | Caras + reacciones emocionales |
| Velocidad 2 | 36-47 | Obstáculos complejos (cambiantes) |
| Social | 48-59 | Escenas sociales + decisiones |

## Puzzles

### 1. Estímulos Rápidos (CPT / Tiempo de Reacción)
- **Ubicación:** Todo el camino, postes de estímulo cada 4-6 tiles
- **Mecánica:** Estímulo visual aparece en poste
- **Tarea:** Presionar acción solo para estímulo objetivo
- **Estímulos:** Círculos de colores, formas geométricas, iconos
- **Presentación:** 200-800ms, intervalo 1-3s

| Edad | Tiempo estímulo | Target/Distractor ratio | Velocidad jugador |
|------|-----------------|------------------------|------------------|
| 3-6 | 800ms | 60/40 (fácil) | Caminata |
| 6-12 | 500ms | 50/50 | Trote |
| 12-17 | 300ms | 40/60 | Carrera |
| 17+ | 200ms | 30/70 | Sprint + obstáculos |

### 2. Reconocimiento de Caras (Socioemocional)
- **Ubicación:** Sección Emociones (tiles 24-35)
- **Mecánica:** Caras aparecen en burbujas a los lados
- **Tarea:** Identificar emoción (feliz, triste, enojado, sorprendido, asustado, neutro)

| Edad | Emociones | Sutiliza | Contexto |
|------|-----------|----------|----------|
| 3-6 | 3 (feliz, triste, enojado) | Explícita | Sin contexto |
| 6-12 | 4-5 emociones | Moderada | Contexto simple |
| 12-17 | 6 emociones | Sutil | Contexto social |
| 17+ | 6 + microexpresiones | Muy sutil | Contexto ambiguo |

- **Visual:** Caras estilo pixel art 24x32, 4 frames por emoción
- **Feedback visual:** Cara se expande si acierta, se tapa si falla
- **Score:** Precisión + velocidad de respuesta

### 3. Escenas Sociales (Socioemocional + Decisión)
- **Ubicación:** Sección Social (tiles 48-59)
- **Mecánica:** Viñeta de escena social en el camino (detiene avance)
- **Tarea:** Elegir respuesta correcta entre 3 opciones
- **Tema:** Compartir, ayudar, esperar turno, pedir ayuda, consolar

| Edad | Escenas | Opciones | Feedback |
|------|---------|----------|----------|
| 3-6 | 2 escenas, muy simples | 2 opciones visuales | Carita feliz/triste |
| 6-12 | 3 escenas | 3 opciones | Explicación breve |
| 12-17 | 4 escenas, complejas | 3-4 opciones | Consecuencia mostrada |
| 17+ | 5 escenas, ambiguas | 4 opciones | Dilema moral + consecuencia |

- **Ejemplo escena 3-6:** "Un amigo se cayó. ¿Qué haces?" → [Ayudar] [Ignorar] [Reír]
- **Ejemplo escena 17+:** "Ganaste un premio pero tu amigo no. Él está triste. ¿Qué dices?" → opciones con matiz social

### 4. Obstáculos + Estímulo Dual (12-17+ años)
- **Ubicación:** Velocidad 2 (tiles 36-47)
- **Mecánica:** Esquivar obstáculos MIENTRAS responde a estímulos laterales
- **Tarea:** Dual-task: navegación + atención selectiva
- **Obstáculos:** Rocas, arbustos, charcos que aparecen súbitamente

## NPCs

### Pájaro (Velocidad)
- **Posición:** Vuela en paralelo al jugador (tiles 0-35)
- **Apariencia:** Pájaro naranja/rojo, estela de velocidad
- **Movimiento:** Sigue al jugador, adelanta en rectas
- **Diálogo:**
  - 1er encuentro: "¿Qué tan rápido puedes pensar? El camino no perdona la distracción. ¡Acompáñame!"
  - Hint: "No mires todos los estímulos. Solo los que importan."
  - Checkpoint: "Vas bien. Pero lo rápido no siempre es mejor. ¿Viste las caras en el camino?"

### Tortuga (Socioemocional)
- **Posición:** Sentada en Sección Emociones (tile 30, 12)
- **Apariencia:** Tortuga con bufanda de arcoíris
- **Movimiento:** Quieta, gira cabeza para mirar caras
- **Diálogo:**
  - "Las caras cuentan historias. ¿Ves al que está feliz? ¿Y al que necesita ayuda?"
  - Hint: "No todas las sonrisas son iguales. Mira los ojos."
  - Completado: "Has recorrido el camino más rápido que nadie... pero también has visto a los demás. Eso es lo que importa."

## Conexiones

| Zona | Dirección | Tile | Tipo |
|------|-----------|------|------|
| B2a Jardín Central | Oeste | (0, 5)-(0,7) | Arco de velocidad |
| B2f Torre Matemáticas | Norte | (18, 0)-(20,0) | Túnel de luz |
| B2g Gruta Visual | Norte | (40, 0)-(42,0) | Túnel de espejos |
| B3 (secreta) | Este | (59, 10)-(59,12) | Puerta de luz (desbloqueable) |

## Eventos Trigger

### CV-1: Sprint
- Al llegar a sección Velocidad: overlay de speed
- Barra de velocidad que se llena al responder rápido
- Llena: bonus puntos, efecto visual de motion blur

### CV-2: Pausa Emocional
- Al entrar a sección Emociones: música cambia a tono reflexivo
- Velocidad se reduce automáticamente a 0.5x
- Indicador visual: burbujas de diálogo con caras

### CV-3: Dilema Social
- Escena social detiene el movimiento
- Cámara enfoca la escena (zoom parcial)
- Después de elegir: NPC reacciona (feedback emocional)
- Decisiones afectan: relación con NPCs en otras zonas

### CV-4: Contrarreloj
- Camino completo tiene timer global (60-180s según edad)
- Timer solo corre en secciones de velocidad
- Se pausa en secciones social/emocional
- Bonus: tiempo restante se convierte en puntos

## Dificultad por Edad

| Edad | Estímulos | Caras | Social | Obstáculos | Timer |
|------|-----------|-------|--------|------------|-------|
| 3-6 | 800ms, 60/40 | 3 emociones | 2 escenas | No | ∞ |
| 6-12 | 500ms, 50/50 | 4-5 emociones | 3 escenas | Simples | 120s |
| 12-17 | 300ms, 40/60 | 6 emociones | 4 escenas | Complejos | 90s |
| 17+ | 200ms, 30/70 | 6 + micro | 5 escenas | Dual-task | 60s |

## Walkability (C2)
- 85% caminable (camino recto)
- Obstáculos: esquivables (no dañan, solo ralentizan)
- Bordes: bloqueados por arbustos decorativos
- Sin muerte, sin caídas
- Speed dinámico: 0.5x (sección social), 0.8x-1.5x (sección velocidad según edad)
- Checkpoints automáticos cada sección
