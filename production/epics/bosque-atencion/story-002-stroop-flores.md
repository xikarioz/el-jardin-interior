# Story: Minijuego Stroop — El Claro de las Flores

## Epic
E06 — Bosque Atención

## Description
Crear el minijuego Stroop camuflado como un claro de flores mágicas. En pantalla
aparecen 3 flores, cada una con un pétalo que muestra una palabra de color
(ej: "ROJO", "AZUL", "VERDE") pintada con una tinta que puede coincidir o no.
El jugador debe tocar la flor donde el color de la tinta coincide con la palabra.
Son 10 rondas con 5 segundos cada una.

## GDD Requirement
TR-001 — Stroop (atención selectiva / interferencia)

## Acceptance Criteria
- [ ] Escena `scenes/tests/stroop_scene.tscn` carga sin errores
- [ ] 3 flores en pantalla con palabras de color y tintas variables
- [ ] En cada ronda hay exactamente 1 flor correcta (tinta = palabra)
- [ ] Timer de 5s por ronda visible (barra o número)
- [ ] Touch en flor correcta → feedback positivo (flor brilla + sonido)
- [ ] Touch en flor incorrecta → feedback negativo (flor se marchita)
- [ ] Timeout → cuenta como incorrecto, pasa a siguiente ronda
- [ ] Al completar 10 rondas → emite señal `completed(score, rt_data)`
- [ ] Score mostrado al final (aciertos / 10)
- [ ] Tiempo de reacción registrado por ronda en ms
- [ ] Diseño visual coherente con el bosque (flores estilizadas)

## Implementation Notes
- Engine: Godot 4.4 GDScript
- Assigned Agent: gameplay-programmer
- Estructura: Control con nodos Button/TextureButton para cada flor
- Palabras: ["ROJO", "AZUL", "VERDE", "AMARILLO", "VIOLETA"]
- Colores tinta: Color.RED, Color.BLUE, Color.GREEN, Color.YELLOW, Color.VIOLET
- Lógica: Array de rondas pre-generadas, 50% congruentes / 50% incongruentes
- Feedback: Tween para animación de brillo/marchitamiento (~0.5s)
- Señal `completed(score: Dictionary)` con `{hits, misses, timeouts, rt_data}`
- Conectar señal desde `GameManager` o desde zona del bosque

## Test Evidence Path
`tests/scenes/bosque-atencion/test_stroop.gd`
- 10 rondas se ejecutan completas
- Score calculado correctamente
- Tiempo de reacción registrado
- Señal completed emitida al final
