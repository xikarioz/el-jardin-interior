# Asset Spec: Tiles — Torre de las Matemáticas

## Source
tile

## Visual Rules (from Art Bible)
- Shape: geométrico, simétrico, preciso
- Primary colors: #2D3436, #4A90D9, #F0C060, #E8A84A
- Size: 32×32 per tile
- Semantic meaning: orden numérico, precisión, patrones, descubrimiento

## Tiles Required
| Tile ID | Type | Palette | Notes |
|---------|------|---------|-------|
| floor_white | suelo | #F0F0F0, #E0E0E0 | Suelo claro tipo tablero |
| floor_black | suelo | #2D3436, #1A1A1A | Suelo oscuro tipo tablero |
| floor_grid | suelo | #4A90D9, alpha 20% | Suelo con cuadrícula azul |
| number_tile_1 | decoración | #F0C060, #E8A84A | Baldosa número 1 |
| number_tile_2 | decoración | #F0C060, #E8A84A | Baldosa número 2 |
| number_tile_3 | decoración | #F0C060, #E8A84A | Baldosa número 3 |
| math_symbol_plus | decoración | #4A90D9, #6DB8E8 | Símbolo + flotante |
| math_symbol_minus | decoración | #4A90D9, #6DB8E8 | Símbolo - flotante |
| math_symbol_mult | decoración | #4A90D9, #6DB8E8 | Símbolo × flotante |
| pillar_base | estructura | #8B8B8B, #6B6B6B | Base de columna |
| pillar_top | estructura | #8B8B8B, #6B6B6B | Capitel de columna |
| gear | decoración | #F0C060, #E8A84A | Engranaje dorado decorativo |
| window_arch | estructura | #4A90D9, #B8B8B8 | Ventana arco apuntado |
| staircase | estructura | #8B8B8B, #6B6B6B | Escalones hacia arriba |

## AI Prompt
Tile pixel art 32×32 de torre académica con estética de tablero de ajedrez mezclada con números y símbolos. Suelo claro y oscuro alternado. Símbolos matemáticos flotantes azules (#4A90D9). Baldosas con números dorados (#F0C060). Columnas grises con capiteles decorados. Engranajes dorados como detalle. Ventanas en arco con luz azul. Ambiente de orden, precisión y descubrimiento intelectual. Tileable, paleta limitada a 12 colores.

## Acceptance Criteria
- [ ] All tiles within 32×32 bounds
- [ ] Floor tiles alternan sin costura
- [ ] Palette matches Art Bible
- [ ] Números y símbolos legibles a 32×32
- [ ] Pillar base + top stackean verticalmente
- [ ] Grid sutil, no domina visualmente
