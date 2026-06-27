# Asset Spec: Tiles — Gruta de lo Visual

## Source
tile

## Visual Rules (from Art Bible)
- Shape: orgánico, curvo, abstracto
- Primary colors: #1A1A2E, #4A90D9, #C9A8E8, #F0C060
- Size: 32×32 per tile
- Semantic meaning: imaginación, sueños, percepción, ilusión

## Tiles Required
| Tile ID | Type | Palette | Notes |
|---------|------|---------|-------|
| cave_floor | suelo | #1A1A2E, #2A2A4E | Suelo de cueva oscuro |
| crystal_floor | suelo | #4A90D9, #6DB8E8 | Suelo con cristales azules |
| stalactite | estructura | #2A2A4E, #3A3A5E | Estalactita |
| stalagmite | estructura | #2A2A4E, #3A3A5E | Estalagmita |
| illusion_tile_a | decoración | #C9A8E8, #E8B4B8 | Patrón ilusión óptica A |
| illusion_tile_b | decoración | #4A90D9, #F0C060 | Patrón ilusión óptica B |
| prism | decoración | #FFFFFF, #F0C060, #4A90D9 | Prisma con destellos |
| dream_bubble | objeto | #C9A8E8, alpha 40% | Burbuja de sueño flotante |
| canvas | objeto | #FFF5F0, #8B6F47 | Lienzo/paleta de pintor |
| paint_splash_yellow | decoración | #F0C060, alpha 50% | Mancha de pintura amarilla |
| paint_splash_pink | decoración | #E8B4B8, alpha 50% | Mancha de pintura rosa |
| paint_splash_blue | decoración | #4A90D9, alpha 50% | Mancha de pintura azul |
| mirror_pool | suelo | #4A90D9, #FFFFFF | Piscina reflectante |
| glowing_eye | decoración | #F0C060, #E8A84A | Ojo brillante decorativo |

## AI Prompt
Tile pixel art 32×32 de gruta onírica y surrealista. Suelo oscuro (#1A1A2E) con cristales azules brillantes (#4A90D9). Estalactitas y estalagmitas de formas orgánicas. Patrones de ilusión óptica en el suelo. Prismas que reflejan luz. Burbujas de sueño flotantes lilas. Manchas de pintura de colores. Piscinas reflectantes. Ambiente de imaginación y fantasía visual. Tileable, paleta limitada a 14 colores con énfasis en contrastes.

## Acceptance Criteria
- [ ] All tiles within 32×32 bounds
- [ ] Cave floor y crystal floor son tileables
- [ ] Palette matches Art Bible
- [ ] Ilusión óptica distinguible aunque sutil
- [ ] Paint splashes tienen transparencia
- [ ] Mirror pool tiene efecto reflectante
