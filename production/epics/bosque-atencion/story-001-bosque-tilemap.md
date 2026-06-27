# Story: Bosque Atención — Tilemap y Navegación

## Epic
E06 — Bosque Atención

## Description
Crear el mapa del Bosque Atención en Godot 4.4. Implementar un TileMap de 50x40
con tiles de bosque (forest_grass, forest_dirt, tree_trunk, tree_top, mushroom,
leaves). El player spawnea en la entrada desde Jardín Central. El Zorro NPC
aparece como guía en la entrada. Definir 3 zonas de puzzle (Area2D con metadata
`test_type`) distribuidas en el mapa. Incluir camino de vuelta visual al
Jardín Central.

## GDD Requirement
TR-001, TR-002, TR-003, TR-004, TR-005, TR-006 (zona física para cada test)

## Acceptance Criteria
- [ ] TileMap 50x40 carga sin errores en escena `bosque_atencion.tscn`
- [ ] Tiles de terreno, decoración y colisión funcionan correctamente
- [ ] Player spawnea en la entrada con posición correcta
- [ ] Zorro NPC visible en la entrada, con animación idle
- [ ] 3 zonas de puzzle identificables visualmente (claros)
- [ ] Cada zona es Area2D con `test_type` en metadata
- [ ] Camino de vuelta a Jardín Central visible y conectable
- [ ] Capa de colisión impide salirse del mapa
- [ ] Iluminación ambiente (WorldEnvironment) aplicada

## Implementation Notes
- Engine: Godot 4.4 GDScript
- Assigned Agent: level-designer
- Tilemap: 3 capas (terreno, decoración, colisión)
- Tamaño tile: 16x16 px
- Zonas puzzle: Area2D con CollisionShape2D, script que emite
  `test_triggered(test_type: String)`
- Zorro: Sprite2D + AnimationPlayer + diálogo inicial
- Camino: TileMap path + señal de transición de escena
- Usar `GameManager.goto_scene()` para transición desde el camino

## Test Evidence Path
`tests/scenes/bosque-atencion/test_bosque_tilemap.gd`
- Verificar que todas las zonas tienen metadata correcta
- Verificar que el player spawnea en posición válida
- Verificar que el Zorro está presente
