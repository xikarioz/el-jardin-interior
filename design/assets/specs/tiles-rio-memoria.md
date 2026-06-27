# Asset Spec: Tiles — Río de la Memoria

## Source
tile

## Visual Rules (from Art Bible)
- Shape: fluido, ondulante
- Primary colors: #2A6BA8, #4A90D9, #6DB8E8, #C9A8E8
- Size: 32×32 per tile
- Semantic meaning: flujo de recuerdos, nostalgia, profundidad emocional

## Tiles Required
| Tile ID | Type | Palette | Notes |
|---------|------|---------|-------|
| water_flow | suelo | #2A6BA8, #4A90D9 | Agua fluyendo, animado |
| water_calm | suelo | #4A90D9, #6DB8E8 | Agua calmada, reflejos |
| water_bank_top | suelo | #8B6F47, #6B4F27 | Orilla superior |
| water_bank_bottom | suelo | #8B6F47, #6B4F27 | Orilla inferior |
| water_bank_left | suelo | #8B6F47, #6B4F27 | Orilla izquierda |
| water_bank_right | suelo | #8B6F47, #6B4F27 | Orilla derecha |
| sand_bank | suelo | #D4C4A0, #C4B490 | Banco de arena |
| pebble | decoración | #B8B8B8, #A0A0A0 | Piedras decorativas |
| memory_orb_blue | decoración | #4A90D9, #FFFFFF | Orbe de memoria azul brillante |
| memory_orb_purple | decoración | #C9A8E8, #FFFFFF | Orbe de memoria lila |
| willow_trunk | objeto | #5A3820, #4A2510 | Tronco de sauce |
| willow_leaves | objeto | #7EC8A0, #A8D5BA | Ramas colgantes de sauce |
| bridge_wood | estructura | #8B6F47, #7A5E3A | Puente de madera |
| reflection_ripple | efecto | #FFFFFF, 20% alpha | Onda de reflejo en agua |

## AI Prompt
Tile pixel art 32×32 de río sereno con agua azul profundo (#2A6BA8) a azul claro (#6DB8E8). Orillas de tierra marrón. Agua con ondas y reflejos sutiles. Sauces llorones en las orillas. Orbes brillantes flotando sobre el agua. Banco de arena ocasional. Ambiente nostálgico y tranquilo. Tiles de agua con animación de 2-3 frames para flujo. Paleta limitada a 14 colores.

## Acceptance Criteria
- [ ] All tiles within 32×32 bounds
- [ ] Water tiles tienen variante animada (2-3 frames)
- [ ] Orillas conectan correctamente en 4 direcciones
- [ ] Palette matches Art Bible
- [ ] Orbes tienen brillo visible
- [ ] Bridge tiles permiten paso horizontal
