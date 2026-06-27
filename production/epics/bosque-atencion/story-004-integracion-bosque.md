# Story: Integración Bosque Atención — Flujo Completo

## Epic
E06 — Bosque Atención

## Description
Conectar todos los componentes del Bosque Atención en un flujo jugable completo.
Al entrar a una zona de puzzle (Area2D), el minijuego correspondiente se instancia.
Al completarlo, feedback visual (flor crece en el mapa), el perfil del jugador se
actualiza con los scores, y el Zorro da un diálogo de guía contextual basado en
el Capítulo 2. Las flores decorativas persisten como marcador de progreso.

## GDD Requirement
TR-001, TR-002, TR-003 (integración de todos los tests del bosque)

## Acceptance Criteria
- [ ] Player entra a zona de puzzle → minijuego se instancia automáticamente
- [ ] Al completar minijuego → señal `completed(score)` recibida por Bosque
- [ ] Flor decorativa aparece en la zona completada (Sprite en TileMap)
- [ ] Flores persisten al recargar escena (save/load vía perfil)
- [ ] Perfil del jugador actualizado con scores del test
- [ ] Zorro emite diálogo contextual al completar zona
- [ ] Diálogo del Zorro basado en páginas 11-20 del Capítulo 2
- [ ] Transición suave: mundo → minijuego → mundo (sin cortes bruscos)
- [ ] Múltiples zonas completables en cualquier orden
- [ 】 Camino de vuelta a Jardín Central funcional
- [ ] Si todas las zonas están completas → Zorro da diálogo de despedida
- [ ] Tests unitarios para cada paso del flujo

## Implementation Notes
- Engine: Godot 4.4 GDScript
- Assigned Agent: gameplay-programmer (lead), level-designer (support)
- Instanciación: `PackedScene.instantiate()` desde zona → `add_child()` al árbol
- Señales: zona emite `test_triggered` → GameManager instancia → test emite
  `completed` → Bosque escucha → feedback visual + perfil
- Flor decorativa: instanciar Sprite2D en posición global de la zona, agregar
  a capa de decoración del TileMap
- Persistencia: `ProfileManager.add_result(test_type, score_data)` y
  `ProfileManager.get_completed_zones()` → al cargar bosque, revisar y colocar flores
- Diálogo Zorro: archivo JSON de diálogos por zona y estado
  (`assets/dialogue/bosque-atencion/zorro_dialogues.json`)
- Transición: CanvasLayer para fade in/out (AnimationPlayer)
- Despedida Zorro: verificar `get_completed_zones().size() >= total_zonas`

### Diálogos del Zorro (Capítulo 2)

| Evento | Diálogo |
|--------|---------|
| Primer encuentro | "El bosque cambia frente a tus ojos. No todo es lo que parece, igual que las palabras que ves." |
| Al completar Stroop | "Las flores te enseñaron a mirar más allá de las apariencias. Bien hecho." |
| Al completar Flanker | "Ignorar lo que distrae es un don. Las flechas ya no te confunden." |
| Al completar CPT/SART | "Mantuviste la mirada fija incluso cuando el bosque parpadeaba." |
| Despedida (todo completo) | "Has aprendido a ver con claridad. El río te espera al otro lado del puente." |

## Test Evidence Path
`tests/scenes/bosque-atencion/test_bosque_integration.gd`
- Flujo completo: entrar zona → test instancia → completar → feedback → perfil
- Flor decorativa persiste al recargar escena
- Diálogos contextuales correctos
- Transición Jardín Central funciona
