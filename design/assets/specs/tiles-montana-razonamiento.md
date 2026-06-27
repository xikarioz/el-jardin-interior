# Asset Spec: Tiles — Montaña del Razonamiento

## Source
tile

## Visual Rules (from Art Bible)
- Shape: angular, geométrico
- Primary colors: #6B6B6B, #8B8B8B, #B8B8B8, #4A90D9
- Size: 32×32 per tile
- Semantic meaning: lógica, estructura, claridad mental, altura

## Tiles Required
| Tile ID | Type | Palette | Notes |
|---------|------|---------|-------|
| stone_floor | suelo | #8B8B8B, #7A7A7A | Suelo de piedra gris |
| stone_floor_dark | suelo | #6B6B6B, #5A5A5A | Piedra más oscura, variación |
| stone_floor_light | suelo | #B8B8B8, #A8A8A8 | Piedra clara, reflejo |
| cliff_face | estructura | #6B6B6B, #5A5A5A | Pared de acantilado |
| cliff_top | estructura | #8B8B8B, #7A7A7A | Borde superior acantilado |
| crystal_blue | decoración | #4A90D9, #6DB8E8 | Cristal azul brillante |
| crystal_white | decoración | #FFFFFF, #E0E0E0 | Cristal blanco puro |
| geometric_glyph | decoración | #4A90D9, #F0C060 | Glifo geométrico en suelo |
| puzzle_pedestal | estructura | #B8B8B8, #6B6B6B | Pedestal para acertijos |
| cloud_top | decoración | #FFFFFF, #E0E0E0 | Nube desde arriba |
| ladder_rope | estructura | #8B6F47, #6B4F27 | Escalera de cuerda |
| snow_patch | suelo | #F0F0F0, #E0E0E0 | Parche de nieve en altura |

## AI Prompt
Tile pixel art 32×32 de montaña rocosa con geometrías marcadas. Piedras grises (#6B6B6B-#B8B8B8) con vetas y textura de corteza terrestre. Cristales azules y blancos emergiendo de la roca. Glifos geométricos brillantes en el suelo. Acantilados verticales imponentes. Nubes rodeando las alturas. Ambiente de claridad mental y estructura lógica. Tileable, paleta limitada a 12 colores.

## Acceptance Criteria
- [ ] All tiles within 32×32 bounds
- [ ] Cliff tiles stackan verticalmente sin costura
- [ ] Palette matches Art Bible
- [ ] Cristales con efecto de brillo
- [ ] Glifos visibles sobre piedra oscura
- [ ] Snow patch solo en zonas altas
