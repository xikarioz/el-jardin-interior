# Asset Spec: Tiles — Bosque de la Atención

## Source
tile

## Visual Rules (from Art Bible)
- Shape: orgánico, vertical (árboles altos)
- Primary colors: #2D5016, #4A7C2E, #6B8F3A, #F0C060
- Size: 32×32 per tile
- Semantic meaning: concentración, foco, misterio suave, detalles ocultos

## Tiles Required
| Tile ID | Type | Palette | Notes |
|---------|------|---------|-------|
| forest_floor | suelo | #2D5016, #3A6B1E | Suelo de bosque oscuro |
| moss_path | suelo | #4A7C2E, #5A8C3E | Camino cubierto de musgo |
| moss_path_corner | suelo | #4A7C2E, #5A8C3E | Esquina de camino musgo |
| tree_trunk | objeto | #4A3520, #3A2510 | Tronco recto, 2 alturas |
| tree_top_dense | objeto | #1A3A0A, #2D5016 | Copa densa, luz filtrada |
| mushroom_red | decoración | #D94040, #F06060 | Seta roja brillante (llama atención) |
| mushroom_blue | decoración | #4A90D9, #6DB8E8 | Seta azul (pista oculta) |
| leaf_pile | decoración | #6B8F3A, #8B6F47 | Montón de hojas |
| hiding_spot | estructura | #2D5016, #1A3A0A | Arbusto para esconderse |
| spotlight_ray | efecto | #F0C060, 30% alpha | Rayo de luz entre árboles |
| fallen_log | objeto | #5A3820, #4A2510 | Tronco caído horizontal |
| acorn | decoración | #8B6F47, #6B4F27 | Bellotas pequeñas en suelo |

## AI Prompt
Tile pixel art 32×32 de bosque denso pero acogedor. Suelo verde oscuro (#2D5016) con parches de musgo más claro (#4A7C2E). Árboles altos con copas densas que filtran la luz. Rayos de sol dorados sutiles (#F0C060 con alpha). Setas rojas y azules pequeñas como detalles de atención. Hojas caídas. Ambiente de concentración y descubrimiento. Tileable, paleta limitada a 14 colores.

## Acceptance Criteria
- [ ] All tiles within 32×32 bounds
- [ ] Tileable seamless
- [ ] Palette matches Art Bible
- [ ] Spotlights tienen transparencia
- [ ] Setas destacan visualmente del suelo
- [ ] Hiding spots se integran naturalmente
