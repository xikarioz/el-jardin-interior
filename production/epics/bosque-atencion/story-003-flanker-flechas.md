# Story: Minijuego Flanker — El Claro de las Flechas

## Epic
E06 — Bosque Atención

## Description
Crear el minijuego Flanker camuflado como un claro donde aparecen 5 flechas
alineadas. Solo importa la flecha del medio; las laterales pueden apuntar en
la misma dirección (congruente) o en dirección opuesta (incongruente).
El jugador toca la mitad izquierda o derecha de la pantalla para indicar
hacia dónde apunta la flecha central. Son 20 ensayos.

## GDD Requirement
TR-002 — Flanker (control inhibitorio / interferencia)

## Acceptance Criteria
- [ ] Escena `scenes/tests/flanker_scene.tscn` carga sin errores
- [ ] 5 flechas horizontales en pantalla (→ o ←) en cada ensayo
- [ ] Flecha central es el estímulo objetivo
- [ ] Ensayos congruentes (<<<<< o >>>>>) e incongruentes (<<><< o >><>>)
- [ ] Touch en mitad izquierda = flecha izquierda, mitad derecha = flecha derecha
- [ ] Feedback visual inmediato (correcto: verde / incorrecto: rojo)
- [ ] Timer por ensayo: 3s (timeout si no responde)
- [ ] ISI (intervalo entre estímulos): 1.5s con fijación central
- [ ] 20 ensayos totales (10 congruentes, 10 incongruentes)
- [ ] Tiempo de reacción medido por ensayo (critical para efecto flanker)
- [ ] Señal `completed(score, rt_data)` con medias por condición
- [ ] Efecto flanker calculable: RT_incongruente - RT_congruente

## Implementation Notes
- Engine: Godot 4.4 GDScript
- Assigned Agent: gameplay-programmer
- Input: Area2D touch zones (izquierda/derecha) o botones táctiles
- Flechas: Sprite2D o TextureRect con textura de flecha → / ←
- Secuencia: Array pre-generado de 20 ensayos (orden aleatorio)
- Timing: Timer para ensayo, Timer para ISI
- Señal `completed(score: Dictionary)` con:
  `{hits, misses, rt_congruent_mean, rt_incongruent_mean, flanker_effect_ms}`
- Fijación: cruz "+" central durante ISI

## Test Evidence Path
`tests/scenes/bosque-atencion/test_flanker.gd`
- 20 ensayos ejecutados
- RTs registrados por condición
- Efecto flanker positivo (incongruente > congruente)
- Señal completed emitida
