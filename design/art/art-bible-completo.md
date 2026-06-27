# Art Bible — El Jardín Interior

> Documento maestro de dirección visual. Define el lenguaje artístico del juego.
> Versión: 1.0 | Target: Godot 4 · Pixel art 2D · Tablet

---

## Section 1: Visual Identity Statement

**"Pixel art cálido y redondeado donde cada personaje, entorno e interfaz comunica seguridad emocional y descubrimiento cognitivo a través de formas orgánicas, paletas armónicas iluminadas por luz dorada y una paleta de 16 colores por sprite que prioriza la legibilidad en tablet."**

### Principios de soporte

| # | Principio | Test de diseño |
|---|-----------|----------------|
| 1 | **Calidez estructural** — curvas sobre rectas, B ezier sobre poligonales, contornos suaves | Un sprite cualquiera reducido a 32×32 px debe conservar su forma reconocible sin bordes duros |
| 2 | **Contención emocional** — la paleta y la luz envuelven al jugador sin generar ansiedad | Un prototipo en tablet debe poder jugarse 30 min sin fatiga visual ni irritación cromática |
| 3 | **Lecturabilidad jerárquica** — personaje > interactivo > fondo en contraste y detalle | En una captura en escala de grises, el protagonista debe diferenciarse del fondo por al menos 3 pasos de valor |

### Qué NO es El Jardín Interior
- No es oscuro, ni melancólico, ni abstracto — incluso los biomas de "confusión" usan luz tenue, no oscuridad
- No es hyper-detallado — cada sprite respeta su paleta de 16 colores y su resolución target
- No es infantil — es accesible; el pixel art redondeado comunica seguridad sin subestimar al jugador

---

## Section 2: Color System

### Paleta primaria

| Color | Hex | Role |
|-------|-----|------|
| Dorado tenue | `#F5D78E` | Luz principal, calidez, esperanza |
| Verde musgo | `#7BA05B` | Naturaleza base, crecimiento |
| Marfil | `#FFF3E0` | Fondos claros, UI, texto |
| Marrón tierra | `#8B6F47` | Suelo, troncos, estructuras |
| Azul cielo | `#A8D5E2` | Agua, cielo, calma |
| Rosa pétalo | `#F2B5C4` | Acento emocional, personajes |
| Gris cálido | `#C4BBAF` | Sombra suave, transiciones |
| Blanco roto | `#F5F0E8` | Background general |

### Colores semánticos

| Color | Comunica | Uso en el juego |
|-------|----------|-----------------|
| **Dorado** `#F5D78E` | Logro, descubrimiento, calidez divina | Destellos al completar un área, luz de tutorial, partículas de recompensa |
| **Verde** `#7BA05B` | Crecimiento, salud, naturaleza segura | Vegetación base, barras de vida/energía, bioma Jardín Central |
| **Azul claro** `#A8D5E2` | Calma, fluidez, introspección | Agua, meditación, bioma Río Memoria, burbujas de diálogo interno |
| **Rosa** `#F2B5C4` | Emoción, vulnerabilidad, conexión | Personajes principales (Pájaro, Mariposa), corazones, eventos emocionales |
| **Marrón** `#8B6F47` | Estabilidad, estructura, arraigo | Suelo, construcciones, mobiliario, troncos |
| **Naranja** `#E8A853` | Curiosidad, descubrimiento, energía suave | Interactivos resaltados, signos de pregunta, bioma Bosque Atención |
| **Lavanda** `#C5B4E3` | Imaginación, misterio suave | Bioma Gruta Visual, transiciones de área, efectos de ensueño |
| **Gris azulado** `#8FA3A9` | Confusión, pausa, incertidumbre | Bioma Camino Velocidad en estado difícil, bloques de rompecabezas |
| **Rojo vivo** `#D4756B` | Alerta, peligro suave, urgencia | NO usar en entorno — solo en UI crítica (temporizador bajo, salud crítica) |
| **Blanco** `#FFFFFF` | Claridad, revelación, verdad | Iluminación activa, texto importante, partículas de revelación |

### Paleta por bioma (8 biomas)

| Bioma | Color base | Acento | Sombra | Temperatura |
|-------|-----------|--------|--------|-------------|
| **Jardín Central** | `#7BA05B` verde | `#F5D78E` dorado | `#5A7A3E` | Cálida |
| **Bosque Atención** | `#4A7C59` verde bosque | `#E8A853` naranja | `#2E4F37` | Neutra-cálida |
| **Río Memoria** | `#6BB5C9` azul lago | `#F2B5C4` rosa | `#3D7A8A` | Fría |
| **Montaña Razonamiento** | `#9DB5B2` gris-verde | `#C5B4E3` lavanda | `#6B8280` | Neutra-fría |
| **Valle Lenguaje** | `#D4C5A0` beige | `#E8836B` terracota | `#A89770` | Cálida |
| **Torre Matemáticas** | `#8FA3A9` gris azulado | `#4A90D9` azul | `#5C6E73` | Fría |
| **Gruta Visual** | `#2D2D3F` noche | `#C5B4E3` lavanda | `#1A1A28` | Fría-tenue |
| **Camino Velocidad** | `#D4A56A` dorado tierra | `#F5D78E` dorado | `#A87D45` | Cálida |

### Colorblind safety

| Tipo | Ajuste |
|------|--------|
| Deuteranopia | Incrementar contraste verde-marrón: vegetación usa `#6B9B4E`, suelo `#9B7B4E` |
| Tritanopia | No usar azul-verde como único diferenciador; añadir textura o brillo |
| Escala de grises | Cada sprite supera test de 3 pasos de valor entre personaje/fondo |
| Tooltip | Todos los elementos codificados por color tienen un icono o texto alternativo |

---

## Section 3: Shape Language

### Vocabulario geométrico del juego

```
Formas permitidas:     círculos, óvalos, espirales, arcos, curvas Bezier suaves
Formas condicionales:  rectángulos de esquinas redondeadas (UI), triángulos (orejas/alas/picos)
Formas prohibidas:     ángulos agudos (< 45°), polígonos irregulares, simetría perfecta
```

### Silueta de personajes — regla del thumbnail

Cada personaje reducido a 24×24 px debe ser identificable por silueta:

| Personaje | Silueta thumbnail | Clave de lectura |
|-----------|------------------|------------------|
| Protagonista | Óvalo vertical + mochila redonda | Cabeza grande, cuerpo pequeño (3:2 ratio) |
| Tortuga | Óvalo horizontal + cúpula | Caparazón de media esfera |
| Zorro | Triángulo orejas + cono cola | Orejas puntiagudas arriba, cola abajo |
| Búho | Círculo + dos topes (orejas pluma) | Cabeza redonda, cuerpo rechoncho |
| Mariposa | Dos óvalos (alas) + línea | Alas simétricas, cuerpo línea fina |
| Caracol | Espiral + rectángulo base | Espiral dominante 60% del sprite |
| Pájaro | Círculo + triángulo (pico) + forma pluma | Redondo compacto |

### Geometría del entorno — las curvas gobiernan

- 90% de los tiles de entorno usan al menos una curva visible
- Caminos: bordes difuminados, nunca líneas rectas de tile a tile
- Árboles: copas circulares, troncos con curvatura orgánica
- Rocas: óvalos irregulares, nunca cubos ni pirámides
- Arquitectura humana (puentes, torres): esquinas redondeadas (radio mínimo 4 px)

### Formas heroicas vs formas de fondo

| Elemento | Contorno | Saturación | Detalle |
|----------|----------|------------|---------|
| Personajes (heroicos) | Borde negro 2 px | 100% sat | 16 colores, sombreado completo |
| Interactivos | Borde negro 1 px + brillo | 80-100% sat | 8-12 colores |
| Fondo lejano | Sin borde | 40-60% sat | 4-6 colores, sin sombra |

### Qué formas evitar (y por qué)

| Forma | Motivo |
|-------|--------|
| Ángulos agudos (< 45°) | Comunican agresión, peligro, ansiedad — opuesto a la identidad visual |
| Simetría perfecta | Se siente artificial, robótica — el juego es orgánico y humano |
| Píxel solitario (aliasing) | Rompe la limpieza del pixel art redondeado |
| Líneas paralelas rectas muy juntas | Generan Moiré en tablet y fatiga visual |
| Polígonos cóncavos complejos | Ilegibles a escala tablet |

---

## Section 4: Lighting & Atmosphere

### Matriz de iluminación por estado de juego

| Estado | Emoción target | Temperatura color | Energía visual | Elemento que lleva el estado |
|--------|---------------|-------------------|----------------|---------------------------|
| **Exploración** | Curiosidad, calma | Cálida `#F5D78E` → `#FFF3E0` | Media-suave | Luz de atardecer desde la derecha, sombras largas y suaves |
| **Logro** | Orgullo, satisfacción | Dorada `#FFD700` → blanca | Alta | Destello radial desde el personaje, partículas ascendentes doradas |
| **Confusión** | Incertidumbre, pausa | Neutra-fría `#C4BBAF` → `#8FA3A9` | Baja | Niebla tenue, sombras que se alargan, luz ambiental plana |
| **Frustración** | Tensión baja, desafío | Fría `#6B8280` → `#4A5C5A` | Baja-media | Relámpagos tenues azul-gris, parpadeo de luz cada 3s |
| **Vulnerabilidad** | Introspección, apertura | Rosa tenue `#F2B5C4` → lavanda | Muy baja | Aura suave alrededor del personaje, luz focal tipo spotlight |
| **Introspección** | Reflexión, conexión | Azul claro `#A8D5E2` → blanco | Mínima | Efecto acuático: ondas de luz en el suelo, partículas lentas |

### Reglas de lighting global

| Regla | Valor |
|-------|-------|
| Dirección de luz por defecto | Desde arriba-derecha (sol de media tarde) |
| Intensidad máxima de luz directa | 60% del blanco puro |
| Número máximo de luces dinámicas en pantalla | 3 (tablet performance) |
| Modo de mezcla de luces | Add (nunca multiply — oscurece demasiado) |
| Sombras | Suaves, 40% opacidad, radio 24-48 px |
| Transición entre estados de luz | 0.5-1.5s easing in-out |

---

## Section 5: Character Design Direction

### Protagonista

| Atributo | Especificación |
|----------|---------------|
| **Silueta** | Óvalo vertical (cabeza grande, torso pequeño). Proporción cabeza:cuerpo 3:2. Mochila redonda a la espalda. |
| **Proporciones** | 32×48 px (ancho×alto). Cabeza 24×24, torso 20×24, piernas 16×16. |
| **Colores** | Pelo `#5C3A21`, piel `#F5D0A9`, ropa `#E8A853` (naranja tierra), mochila `#7BA05B`. |
| **Expresiones** | 5: neutral (sonrisa suave), curioso (ojos abiertos, ceja levantada), pensativo (mirada lateral, mano en mentón), alegre (ojos en arco, sonrisa), confundido (cejas fruncidas suaves). |
| **Animación** | Idle: respiración suave (ciclo 1.5s). Walk: 4 frames, pasos lentos-compasivos. Talk: 2 frames, la cabeza se inclina ligeramente. |
| **Principio** | El protagonista NO corre — camina. Su movimiento es pausado, deliberado, como quien explora un jardín por primera vez. |

### Tortuga (Sabiduría, Paciencia)

| Atributo | Especificación |
|----------|---------------|
| **Silueta** | Óvalo horizontal. Caparazón tipo cúpula (media esfera). Patas cortas. |
| **Proporciones** | 40×32 px. Caparazón 32×20, cabeza 12×10, patas 8×6 c/u. |
| **Colores** | Caparazón `#7BA05B` con espiral `#F5D78E`, piel `#8B6F47`, bufanda `#D4756B` (rojo suave), ojos `#2D2D2D` grandes y redondos. |
| **Expresiones** | Paciente (ojos semicerrados, sonrisa mínima), sabio (ojos abiertos, mirada fija), divertido (ojos en arco). |
| **Animación** | Idle: movimiento de cabeza cada 4s (mira a izquierda y derecha lentamente). Walk: 4 frames, muy lento — cada paso es deliberado. Talk: asentimiento suave. |
| **Principio** | La tortuga es el mentor tranquilo. Nunca se apresura. Su animación más rápida sigue siendo lenta comparada con cualquier otro personaje. |

### Zorro (Curiosidad, Astucia)

| Atributo | Especificación |
|----------|---------------|
| **Silueta** | Triángulo (orejas) + cono (cuerpo) + cono invertido (cola). Vertical estilizado. |
| **Proporciones** | 28×40 px. Cabeza 16×16, cuerpo 20×20, cola 12×24. |
| **Colores** | Pelaje `#E8A853` (naranja), pecho `#FFF3E0`, punta cola `#FFFFFF`, orejas `#D4756B` interior, ojos `#4A90D9` (azul curioso). |
| **Expresiones** | Curioso (orejas erguidas, cabeza ladeada), alerta (orejas hacia adelante), contento (ojos cerrados en arco), sorprendido (ojos redondos, orejas hacia atrás). |
| **Animación** | Idle: orejas se mueven independientemente (cada 0.8s), cola se mece. Walk: 4 frames, saltarín y rápido. Talk: cabeza se ladea con curiosidad. |
| **Principio** | El zorro es energía curiosa. Sus orejas son antenas emocionales — siempre en movimiento, siempre leyendo el entorno. |

### Búho (Conocimiento, Observación)

| Atributo | Especificación |
|----------|---------------|
| **Silueta** | Círculo (cuerpo) + dos triángulos suaves (orejas pluma). Rechoncho, compacto. |
| **Proporciones** | 28×32 px. Cuerpo 24×24, cabeza 20×20 (se superpone al cuerpo), orejas pluma 8×6 c/u. |
| **Colores** | Plumas `#C4BBAF` (gris cálido), pecho `#FFF3E0`, anteojos `#8B6F47`, ojos `#F5D78E` (dorado), pico `#E8A853`. |
| **Expresiones** | Seria-cálida (ojos serenos, sin sonrisa), observadora (mirada lateral), iluminada (ojos brillan, alas se abren ligeramente). |
| **Animación** | Idle: parpadeo lento cada 3s, la cabeza gira 180° (como búho real). Walk: 4 frames, bamboleo. Talk: inclinación de cabeza. |
| **Principio** | El búho es el bibliotecario del jardín. Su movimiento es contenido, preciso. Cuando habla, es pausado — cada palabra tiene peso. |

### Mariposa (Ligereza, Transformación)

| Atributo | Especificación |
|----------|---------------|
| **Silueta** | Dos óvalos (alas) unidos por una línea fina (cuerpo). Alas superiores más grandes que inferiores. |
| **Proporciones** | 32×24 px con alas extendidas. Cuerpo 2×10, ala superior 14×12, ala inferior 10×10. |
| **Colores** | Alas `#C5B4E3` (lavanda) con bordes `#F2B5C4` (rosa), cuerpo `#2D2D2D`, rastro de luz `#F5D78E` (dorado tenue, alpha 40%). |
| **Expresiones** | No tiene rostro visible — su emoción se comunica por velocidad de aleteo y brillo. |
| **Animación** | Idle: aleteo continuo 6 frames (bucle rápido). Walk: vuela en patrones de 8 — círculos y ochos. Talk: se posa en una flor cercana, alas se abren y cierran lentamente. |
| **Principio** | La mariposa es la guía espiritual. Nunca habla directamente — su presencia y movimiento comunican dirección emocional. Donde va la mariposa, hay algo importante. |

### Caracol (Reflexión, Ritmo Propio)

| Atributo | Especificación |
|----------|---------------|
| **Silueta** | Espiral (caparazón) + rectángulo alargado (cuerpo). Dominante la espiral (60% visual). |
| **Proporciones** | 24×20 px. Caparazón 20×16, cuerpo 24×6, ojos 4×4 c/u (en tallos). |
| **Colores** | Caparazón espiral multicolor: `#F2B5C4` → `#E8A853` → `#C5B4E3`, cuerpo `#D4C5A0`, tallos oculares `#C4BBAF`, ojos `#2D2D2D` saltones. Rastro: `#F5D78E` alpha 20%. |
| **Expresiones** | Ojos saltones que miran en todas direcciones independientemente. Contento (ojos en arco), curioso (tallos se estiran), asustado (ojos se retraen). |
| **Animación** | Idle: tallos oculares se mueven independientemente (patrón aleatorio). Walk: 4 frames, deslizamiento con onda corporal. Talk: un ojo mira al jugador, otro al horizonte. |
| **Principio** | El caracol es el filósofo del jardín. Su lentitud no es pereza — es profundidad. Cada pausa es una reflexión. |

### Pájaro (Alegría, Levedad)

| Atributo | Especificación |
|----------|---------------|
| **Silueta** | Círculo (cuerpo) + triángulo pequeño (pico) + forma de pluma (cola). Redondo y compacto. |
| **Proporciones** | 20×20 px. Cuerpo 16×14, cabeza 12×10, pico 6×4, cola 8×6. |
| **Colores** | Cuerpo `#F5D78E` (amarillo dorado), pecho `#F2B5C4` (rosa), pico `#E8A853`, patas `#8B6F47`, ojo `#2D2D2D`. |
| **Expresiones** | Contento (pico entreabierto como sonrisa), curioso (cabeza ladeada), cantando (pico abierto, ondas musicales). |
| **Animación** | Idle: brincos pequeños cada 1s, cabeza mira alrededor. Walk: 4 frames saltarines (nunca camina — brinca). Talk/tweet: 2 frames, ondas musicales visuales. |
| **Principio** | El pájaro es la alegría del jardín. Siempre está en movimiento — brinca, canta, vuela distancias cortas. Su animación nunca se detiene del todo. |

---

## Section 6: Environment Design Language

### Reglas transversales

- Todos los biomas comparten un **horizonte de tile con curvatura** (no bordes rectos de pantalla)
- **Transiciones entre biomas**: zona de amortiguación de 2-3 tiles con paleta mezclada + partículas de transición
- **Interactivos**: siempre un 20% más brillantes que el entorno, con borde de 1 px dorado
- **Evolución por perfil del paciente**: cada bioma tiene 3 estados visuales — inicial (bloqueado/apagado), en progreso (parcialmente iluminado), completado (lleno de luz y color)

### Jardín Central

| Atributo | Descripción |
|----------|-------------|
| **Arquitectura** | Círculos concéntricos. Fuente central. Caminos curvos de piedra clara. Bancos de madera redondeada. |
| **Vegetación** | Arbustos redondos, flores pequeñas (rosa, blanco), pasto suave. Árbol de la vida central. |
| **Paleta local** | `#7BA05B` verde, `#F5D78E` dorado, `#FFF3E0` marfil |
| **Elemento distintivo** | La fuente central con agua brillante que refleja el cielo |
| **Evolución** | *Bloqueado*: fuente seca, colores apagados. *Progreso*: fuente gotea, aparecen flores. *Completo*: fuente fluye, árbol florece, partículas doradas. |

### Bosque Atención

| Atributo | Descripción |
|----------|-------------|
| **Arquitectura** | Árboles altos y delgados que forman corredores visuales. Claros circulares. Senderos que convergen. |
| **Vegetación** | Helechos, musgo, hongos bioluminiscentes naranjas. Árboles de copa pequeña. |
| **Paleta local** | `#4A7C59` verde bosque, `#E8A853` naranja, `#2E4F37` sombra |
| **Elemento distintivo** | Hongos brillantes que titilan cuando el jugador está cerca |
| **Evolución** | *Bloqueado*: niebla espesa, hongos apagados. *Progreso*: la niebla se aclara, hongos encienden. *Completo*: rayos de luz atraviesan el dosel, todo iluminado. |

### Río Memoria

| Atributo | Descripción |
|----------|-------------|
| **Arquitectura** | Río serpenteante que cruza el bioma. Puentes de piedra arco. Orillas de guijarros redondos. |
| **Vegetación** | Juncos, lirios acuáticos, sauce llorón. Flores azules y rosas en la orilla. |
| **Paleta local** | `#6BB5C9` azul lago, `#F2B5C4` rosa, `#3D7A8A` sombra |
| **Elemento distintivo** | El agua muestra recuerdos — reflejos de escenas pasadas del paciente |
| **Evolución** | *Bloqueado*: agua turbia, sin reflejos. *Progreso*: agua más clara, reflejos fragmentados. *Completo*: agua cristalina, recuerdos nítidos. |

### Montaña Razonamiento

| Atributo | Descripción |
|----------|-------------|
| **Arquitectura** | Formaciones rocosas escalonadas. Plataformas de observación. Caminos en zigzag. |
| **Vegetación** | Pinos pequeños, líquenes, pasto alpino. Flores moradas escasas. |
| **Paleta local** | `#9DB5B2` gris-verde, `#C5B4E3` lavanda, `#6B8280` sombra |
| **Elemento distintivo** | Torres de observación con catalejos que revelan rutas ocultas |
| **Evolución** | *Bloqueado*: picos afilados, niebla densa. *Progreso*: rocas se redondean, niebla se disipa. *Completo*: vista despejada, flores moradas florecen. |

### Valle Lenguaje

| Atributo | Descripción |
|----------|-------------|
| **Arquitectura** | Valle abierto con colinas suaves. Pequeñas aldeas de estructuras curvas. Plazas de encuentro. |
| **Vegetación** | Campos de flores silvestres, árboles frutales dispersos, viñedos. |
| **Paleta local** | `#D4C5A0` beige, `#E8836B` terracota, `#A89770` sombra |
| **Elemento distintivo** | Ecos visuales — palabras escritas en el viento que se convierten en partículas de color |
| **Evolución** | *Bloqueado*: valle silencioso, sin viento ni ecos. *Progreso*: susurros visuales aparecen. *Completo*: valle lleno de palabras flotantes de colores. |

### Torre Matemáticas

| Atributo | Descripción |
|----------|-------------|
| **Arquitectura** | Torre espiral ascendente. Plataformas geométricas curvas. Escalones flotantes. |
| **Vegetación** | Mínima — musgo geométrico, enredaderas que forman patrones. |
| **Paleta local** | `#8FA3A9` gris azulado, `#4A90D9` azul, `#5C6E73` sombra |
| **Elemento distintivo** | Plataformas que se reconfiguran — geometría dinámica visible |
| **Evolución** | *Bloqueado*: plataformas estáticas, todo gris. *Progreso*: algunas plataformas se mueven, color aparece. *Completo*: torre viva con patrones animados y luz azul pulsante. |

### Gruta Visual

| Atributo | Descripción |
|----------|-------------|
| **Arquitectura** | Caverna subterránea con estalactitas redondeadas. Pasadizos curvos. Cámaras abiertas. |
| **Vegetación** | Cristales bioluminiscentes, hongos gigantes, musgo iridiscente. |
| **Paleta local** | `#2D2D3F` noche, `#C5B4E3` lavanda, `#1A1A28` sombra |
| **Elemento distintivo** | Proyecciones en las paredes — imágenes del subconsciente del paciente |
| **Evolución** | *Bloqueado*: oscuro, cristales sin luz. *Progreso*: algunos cristales iluminan, proyecciones aparecen. *Completo*: gruta iluminada, proyecciones claras y en movimiento. |

### Camino Velocidad

| Atributo | Descripción |
|----------|-------------|
| **Arquitectura** | Camino recto pero con bordes curvos. Estaciones de descanso circulares. Postes de luz. |
| **Vegetación** | Arbustos aerodinámicos, flores que se mecen con el viento. |
| **Paleta local** | `#D4A56A` dorado tierra, `#F5D78E` dorado, `#A87D45` sombra |
| **Elemento distintivo** | Líneas de viento visibles — la velocidad se siente visualmente |
| **Evolución** | *Bloqueado*: camino estático, sin viento. *Progreso*: brisa suave, flores se mecen. *Completo*: viento fluido, partículas de arrastre, sensación de movimiento. |

---

## Section 7: UI Visual Direction

### Estilo general: Semi-diegético

La UI existe en el mundo (diegética) para elementos centrales, pero usa superposición limpia (screen-space) para datos del paciente:

| Elemento | Estilo | Justificación |
|----------|--------|---------------|
| Menú principal | Screen-space, fondo del jardín | Establece atmósfera antes de jugar |
| HUD en juego | Diegético parcial: brújula, mapa | Inmersión, no romper la cuarta pared |
| Diálogos | Screen-space, panel inferior | Legibilidad en tablet |
| Inventario/Perfil | Pantalla completa con transición | Organización, datos del paciente |
| Barra de estado | Diegética: flores que crecen | Comunicación emocional en lugar de numérica |

### Tipografía

| Propiedad | Valor |
|-----------|-------|
| **Título** | Pixel art display, 16-24 px, tracking 2 |
| **Cuerpo** | Pixel art sans-serif, 12-14 px, tracking 1 |
| **Diálogos** | Pixel art serif (estilo novela visual), 14-16 px |
| **Números** | Pixel art mono, 14 px |
| **Tamaño mínimo en tablet** | 12 px body, 16 px interactivo |

### Iconografía

| Tipo | Estilo | Tamaño |
|------|--------|--------|
| Acción (hablar, examinar, usar) | Pixel art outlined, 1 px borde | 24×24 px |
| Emociones/Estados | Pixel art flat, colores semánticos | 16×16 px |
| Biomas/Mapa | Pixel art flat con detalle mínimo | 32×32 px |
| Habilidades/Items | Pixel art flat con sombra 1 px | 24×24 px |
| Decorativos (brújula, reloj) | Pixel art outlined con detalles | 32×32 px |

### Animación de UI

| Elemento | Animación | Timing |
|----------|-----------|--------|
| Transición de pantalla | Fundido a dorado (no a negro) | 0.5s ease-in-out |
| Hover en botón | Escala 1.05 + brillo +10% | 0.15s ease-out |
| Click | Escala 0.95 + sombra | 0.1s |
| Notificación | Slide-in desde arriba + fade | 0.3s |
| Tooltip | Fade-in 0.2s, esquinas redondeadas 4 px | 0.2s |
| Diálogo de personaje | Slide-up desde borde inferior | 0.3s ease-out |
| Barra de progreso (flor) | Crecimiento orgánico escalado | 1s ease-out |
| Partículas de UI | Estrellas/chispas en logro | 1.5s bucle |

### Accesibilidad

| Requisito | Especificación |
|-----------|---------------|
| Contraste mínimo | 4.5:1 texto, 3:1 elementos no-texto (WCAG AA) |
| Tamaño táctil mínimo | 44×44 px en tablet |
| Modo de alto contraste | Paleta alternativa con bordes 2 px |
| Tamaño de fuente ajustable | ×1.0, ×1.25, ×1.5 |
| Soporte de lector de pantalla | Alt text en todos los iconos, etiquetas aria |
| Indicador de foco | Anillo dorado pulsante de 2 px |
| Daltonismo | Modo con texturas además de color en todos los iconos funcionales |

---

## Section 8: Asset Standards

### Resoluciones

| Asset | Resolución base | Escalado | Notas |
|-------|----------------|----------|-------|
| **Tile de entorno** | 32×32 px | 1× (nativo) | Exportado a 64×64 para tablets densas |
| **Tile de suelo** | 32×32 px | 1× | Autotile con 4 variantes por tipo |
| **Sprite personaje** | 128×128 px | Renderizado a 32×48 en juego | Hoja de animación completa |
| **Retrato personaje** | 32×32 px | 2× (64×64 en diálogo) | Pixel art detallado |
| **Icono UI** | 32×32 px | 1× | Escalable a 24×24 y 48×48 |
| **Elemento interactivo** | 32×32 px | 1× | Brillo adicional cuando es relevante |
| **Partícula** | 8×8 a 16×16 px | 1× | Almacenada en atlas de partículas |
| **Fondo de pantalla** | 1024×768 px | 1× (ajustado al viewport) | Diseñado para 4:3 tablet |
| **Tile de transición** | 32×32 px | 1× | 2 tiles de mezcla entre biomas |

### Formatos y empaquetado

| Propiedad | Especificación |
|-----------|---------------|
| **Formato** | PNG RGBA 8-bit |
| **Atlas** | Por personaje (idle + walk + talk en un solo PNG) |
| **Hoja de tiles** | 512×512 px (16×16 tiles por hoja) |
| **Compresión** | lossless PNG (crush con pngquant a 256 colores por atlas) |
| **Metadatos** | Archivo .json por atlas con rectángulos de frame y tiempos |

### Animaciones — frames por dirección

| Animación | Frames | Direcciones | Total frames | FPS |
|-----------|--------|-------------|-------------|-----|
| Idle | 3 | 4 (N, S, E, W) | 12 | 6 |
| Walk | 4 | 4 | 16 | 12 |
| Talk | 2 | 4 | 8 | 6 |
| Interact | 3 | 4 | 12 | 8 |
| Emote | 4 | 1 (frontal) | 4 | 8 |

### Paleta por sprite

| Tipo de sprite | Colores máximos | Transparencia |
|----------------|----------------:|:-------------:|
| Personaje principal | 16 | No |
| NPC | 12 | No |
| Tile de entorno | 8 | Sí (recortes de vegetación) |
| Tile de suelo | 6 | No |
| Icono UI | 8 | Sí (fondos) |
| Partícula | 4 | Sí (obligatorio) |
| Retrato | 16 | No |

### Budget de memoria para tablet

| Categoría | Budget estimado | Notas |
|-----------|-----------------|-------|
| Texturas de personajes (6 personajes × 4 atlases) | 6 MB | 256×256 atlas, compresión PNG |
| Hojas de tiles (8 biomas × 512×512) | 8 MB | 1 MB por bioma |
| UI (iconos, paneles, fuentes) | 3 MB | Atlas único UI 1024×1024 |
| Retratos (7 personajes × 64×64) | 0.3 MB | Atlas de retratos |
| Partículas (1 atlas 256×256) | 0.5 MB | Spritesheet de partículas genéricas |
| **Total texturas VRAM** | **~18 MB** | Muy por debajo del límite de tablet (~128 MB) |
| **Total RAM** | ~64 MB (incluyendo buffers, audio, código) | Baseline seguro |

### Guidelines de exportación

1. Todos los sprites se exportan con `Filter: Nearest` (pixel art nítido)
2. No se usa mip-mapping (sprites mantienen tamaño fijo en cámara ortográfica)
3. Atlas agrupados por escena/bioma para minimizar cambios de textura (draw calls)
4. Los sprites de personaje usan `Centered` pivot
5. Los tiles usan `(0,0)` pivot (esquina superior izquierda)
6. Máximo 2 atlas cargados simultáneamente por escena (excluyendo UI)

---

## Section 9: Reference Direction

### 1. Stardew Valley (ConcernedApe, 2016)

| Tomar | Evitar |
|-------|--------|
| **Sistema de tiles orgánicos**: cómo Stardew mezcla tiles de suelo y vegetación para crear transiciones suaves | **Rutinas diarias estrictas**: no queremos horarios rígidos de NPC — El Jardín Interior es más fluido |
| **Paleta cálida y vibrante**: el uso de colores saturados sin ser chillones | **Simetría de mapas**: Stardew tiene granjas cuadriculadas — nosotros priorizamos curvas |
| **Lecturabilidad de cultivos**: cada planta es única y reconocible a 32×32 | **Exceso de items**: nuestro inventario es mínimo, emocional |
| **Animaciones de personaje simples pero expresivas**: 4 direcciones, pocos frames | **Estilo chibi extremo**: nuestras proporciones son más realistas (cabeza 3:2 no 2:1) |

### 2. Ghibli Movies (Especialmente Mi Vecino Totoro, El Viaje de Chihiro)

| Tomar | Evitar |
|-------|--------|
| **Tratamiento de la naturaleza como personaje**: los árboles, el viento y el agua tienen personalidad | **Escala épica**: no tenemos presupuesto ni necesidad de planos secuencia de 2 minutos |
| **Iluminación dorada de atardecer**: la calidez de la luz de Ghibli es nuestra referencia principal | **Diseño de criaturas complejas**: nuestras criaturas son simples, de pixel art |
| **Expresividad sin palabras**: cómo Ghibli comunica emoción con lenguaje corporal y encuadre | **Animación fluida 24fps**: trabajamos con 12fps para animaciones, 6fps para idle |
| **Transiciones de estado emocional**: cambios de paleta que reflejan el estado interno del personaje | **Fondos ultra-detallados**: nuestros fondos son stylized, no realistas |

### 3. Monument Valley (ustwo games, 2014)

| Tomar | Evitar |
|-------|--------|
| **Geometría imposible pero serena**: cómo MV usa formas imposibles que no generan ansiedad sino asombro | **Falta de agencia**: Monument Valley es un pasillo — nosotros tenemos exploración libre |
| **Paleta limitada por nivel**: cada capítulo de MV usa una paleta reducida y coherente | **Falta de personajes**: nuestro juego está centrado en personajes |
| **Escala y ritmo pausado**: la velocidad de movimiento y la distancia entre elementos fomenta la calma | **Esterilidad visual**: MV es minimalista frío — nosotros somos cálidos y orgánicos |
| **Siluetas heroicas**: cómo los personajes destacan contra fondos simples | **Sin interacción ambiental**: nuestro mundo responde al jugador |

### 4. GRIS (Nomada Studio, 2018)

| Tomar | Evitar |
|-------|--------|
| **Paleta emocional por capítulo**: cómo el color define el estado emocional y evoluciona con la narrativa | **Silencio total**: El Jardín Interior tiene diálogo y banda sonora |
| **Uso de la luz como metáfora**: luz que regresa cuando el personaje sana | **Falta de gameplay mecánico**: GRIS es plataformas puro — nosotros tenemos interacción, puzzle, diálogo |
| **Minimalismo expresivo**: menos es más — cómo GRIS comunica dolor y sanación sin palabras | **Depuración cromática extrema**: nosotros usamos color desde el inicio, no solo al final |
| **Animación fluida del personaje**: la capa de GRIS es uno de los mejores rigs 2D de la década | **Sin sistema de interacción**: nuestro juego requiere tocar, hablar, resolver |

### 5. Flower (Thatgamecompany, 2009)

| Tomar | Evitar |
|-------|--------|
| **Movimiento como meditación**: cómo Flower convierte el movimiento en experiencia sensorial | **Falta de objetivos claros**: necesitamos estructura de juego, no solo experiencia |
| **Viento como elemento de juego**: partículas y dirección visual que guían al jugador naturalmente | **Control por inclinación**: nuestro target tablet permite touch, no giroscopio |
| **Naturaleza que responde al jugador**: el césped, las flores y los árboles reaccionan a la presencia | **Ausencia de fracaso**: El Jardín Interior tiene desafío, aunque sea suave |
| **Evolución del color**: de entornos grises a explosiones de color | **Cámara dinámica extrema**: nosotros usamos cámara fija top-down con scroll |

### Otras referencias secundarias

| Juego/Arte | Qué tomar |
|------------|-----------|
| **Hollow Knight** (equilibrio de oscuridad y luz en paleta) | Contraste, iluminación ambiental |
| **Spiritfarer** (gestión emocional con color) | Cómo colores semánticos comunican estados |
| **A Short Hike** (exploración relajada) | Ritmo, escala, libertad |
| **Wabi-Sabi** (estética japonesa) | Imperfección intencional, asimetría orgánica |
| **Yoshitaka Amano** (ilustraciones) | Uso de curvas y fluidez en personajes |

---

## Apéndice A: Checklist de consistencia visual

Usar esta checklist antes de integrar cualquier asset nuevo al juego:

- [ ] ¿Respeta la paleta de 16 colores por sprite?
- [ ] ¿Pasa el test de thumbnail (reconocible a 24×24 px)?
- [ ] ¿Tiene al menos una curva visible en su forma?
- [ ] ¿Evita ángulos agudos (< 45°)?
- [ ] ¿El personaje contrasta con el fondo en escala de grises (3+ pasos de valor)?
- [ ] ¿La animación tiene 3 frames idle, 4 walk, 2 talk?
- [ ] ¿Usa colores semánticos correctos según la emoción target?
- [ ] ¿El formato es PNG RGBA con compresión lossless?
- [ ] ¿Está dentro del budget de memoria (18 MB texturas total)?
- [ ] ¿Tiene variante accesible (alto contraste / icono alternativo)?

---

## Apéndice B: Glosario visual

| Término | Definición en este proyecto |
|---------|-----------------------------|
| **Pixel art redondeado** | Pixel art donde las curvas se construyen con patrones de 2:1 (no 1:1) para suavizar bordes |
| **Luz dorada** | Iluminación con temperatura `#F5D78E` — tono amarillo-dorado, no blanco |
| **Contención emocional** | Principio de diseño donde la paleta, forma y luz envuelven al jugador en seguridad |
| **Orgánico suave** | Formas que imitan la naturaleza sin ser realistas — curvas imperfectas intencionales |
| **Brillo semántico** | Intensidad de brillo que comunica importancia: 0% fondo, 40% explorable, 80% interactivo |
| **Evolución cromática** | Cambio gradual de paleta en un bioma a medida que el perfil del paciente progresa |

---

*Documento generado para el equipo de arte de "El Jardín Interior". Toda decisión visual debe poder trazarse a una regla de este documento.*
