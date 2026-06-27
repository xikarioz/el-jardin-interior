# Asset Spec: Protagonista

## Source
personaje

## Visual Rules (from Art Bible)
- Shape: organic, rounded
- Primary colors: rosa #E8B4B8, piel #FFE4C4, capa verde #A8D5BA, pelo #8B7355
- Size: 128×128 per frame
- Semantic meaning: curiosidad, descubrimiento, conexión con la naturaleza

## Sprite Sheets Required
| State | Frames | Directions | Size |
|-------|--------|-----------|------|
| idle | 4 | down, left, right, up | 128×128 |
| walk | 6 | down, left, right, up | 128×128 |
| talk | 3 | down | 128×128 |
| interact | 4 | down, left, right, up | 128×128 |
| happy | 3 | down | 128×128 |

## AI Prompt
Pixel art personaje infantil de 12-13 años, pelo castaño claro ondulado (#8B7355), piel cálida (#FFE4C4), mejillas sonrosadas (#E8B4B8). Viste una capa verde musgo (#A8D5BA) con capucha, camisa blanca y botas marrones. Expresión curiosa y amistosa, ojos grandes y brillantes. Estilo tierno y acogedor, proporciones chibi ligeras (cabeza 1/3 del cuerpo). Fondo transparente, bordes limpios, animación fluida en 4 direcciones.

## Acceptance Criteria
- [ ] All frames within 128×128 bounds
- [ ] Palette matches Art Bible (rosa, piel, capa verde, pelo)
- [ ] 4-directional sprites have consistent volume and proportion
- [ ] Walk cycle has weight and personality
- [ ] Capa se mueve ligeramente en animación walk
