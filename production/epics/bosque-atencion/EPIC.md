# EPIC: E06 — Bosque Atención

> Layer: Feature
> Status: 🔴 Not Started
> Animal Guía: Zorro
> Ambientación: Capítulo 2 — El Bosque que Cambia (páginas 11-20 del cuaderno)
> Tests a camuflar: Stroop, Flanker, CPT, SART, D2, Cancelación (30 tests en total)

## Descripción Narrativa

El Jardín Interior da paso a un bosque donde los árboles cambian de color y las hojas
susurran palabras que no siempre coinciden con lo que muestran. El Zorro — astuto y
silencioso — guía al jugador a través de claros de concentración, enseñándole a
ignorar distracciones y enfocarse en lo esencial.

Cada claro del bosque es un test de atención camuflado:
- **Claro de las Flores** → Stroop (atención selectiva)
- **Claro de las Flechas** → Flanker (control inhibitorio)
- **Claro de las Luces** → CPT / SART (atención sostenida)
- **Sendas de Búsqueda** → D2 / Cancelación (rastreo visual)

## GDD Requirements

| ID | Test Clínico | Mecánica Camuflada | Zona |
|----|-------------|-------------------|------|
| TR-001 | Stroop | Tocar flor donde tinta = palabra | Claro Flores |
| TR-002 | Flanker | Tocar dirección de flecha central ignorando laterales | Claro Flechas |
| TR-003 | CPT | Presionar ante no-X (o estímulo diana) | Claro Luces |
| TR-004 | SART | No presionar ante GO (variante CPT) | Claro Luces |
| TR-005 | D2 | Marcar dianas entre distractores similares | Senda Búsqueda |
| TR-006 | Cancelación | Tachar estímulos objetivo en matriz visual | Senda Búsqueda |

## ADRs

### ADR-006-01: TileMap 50x40 como base del bosque
**Contexto**: El bosque necesita un mapa lo suficientemente grande para 3-4 zonas
de puzzle con corredores de conexión.
**Decisión**: Usar TileMap 50x40 con tiles de 16x16 px, capa de terreno,
capa de decoración, capa de colisión.
**Consecuencias**: Fácil iteración visual, compatible con sistema de
camino de retorno al Jardín Central.

### ADR-006-02: Zonas de puzzle como Area2D con metadata
**Contexto**: Cada claro activa un minijuego distinto. Necesitamos un mecanismo
genérico de detección.
**Decisión**: Cada zona es un Area2D con `test_type` en metadata
("stroop", "flanker", "cpt", "sart", "d2", "cancelacion"). El player
entra → señal `test_triggered(test_type)` → GameManager instancia escena.
**Consecuencias**: Fácil agregar nuevas zonas sin tocar código del mapa.

### ADR-006-03: Minijuegos como escenas independientes
**Contexto**: Cada test es autónomo pero comparte interfaz de resultados.
**Decisión**: Cada minijuego es una escena Godot separada en
`scenes/tests/`. Emiten señal `completed(score, rt_data)` que el
Bosque escucha para feedback visual.
**Consecuencias**: Desarrollo paralelo, testeo aislado, reutilización
desde otros epics.

### ADR-006-04: Flor decorativa como marcador de progreso
**Contexto**: El jugador necesita ver qué puzzles completó.
**Decisión**: Al completar un test, aparece una flor decorativa en el
TileMap en la posición de la zona. Las flores persisten entre sesiones.
**Consecuencias**: Feedback visual inmediato, sensación de jardín que
crece.

## Conexiones

| Desde | Hacia | Tipo |
|-------|-------|------|
| Bosque Atención | Jardín Central | Camino de vuelta (escena conn) |
| Bosque Atención | Río Memoria (E07) | Puente de troncos (bloqueado hasta completar 2 claros) |

## Dependencias

- E01 (Foundation): Sistema de movimiento del player, escenas base
- E03 (Personality Engine): Perfil del jugador donde se guardan scores
- E04 (Test Engine): Pipeline de resultados clínicos

## Archivos Clave

```
scenes/bosque-atencion/
  bosque_atencion.tscn
  zonas/
    claro_flores.tscn
    claro_flechas.tscn
    claro_luces.tscn
    senda_busqueda.tscn
  npc/
    zorro.tscn

scenes/tests/
  stroop_scene.tscn
  flanker_scene.tscn
  cpt_scene.tscn
  sart_scene.tscn
  d2_scene.tscn
  cancelacion_scene.tscn

tests/scenes/bosque-atencion/
  test_stroop.gd
  test_flanker.gd
  test_bosque_integration.gd
```
