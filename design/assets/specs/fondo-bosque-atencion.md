# Asset Spec: Fondo — Bosque de la Atención

## Source
fondo

## Visual Rules (from Art Bible)
- Shape: vertical, denso, rayos de luz
- Primary colors: #2D5016, #4A7C2E, #F0C060, #87CEEB
- Size: 512×256 por capa
- Semantic meaning: concentración, enfoque, paz mental

## Layers Required
| Layer | Speed | Content | Palette |
|-------|-------|---------|---------|
| sky_faint | 0.0 | Cielo apenas visible entre copas | #87CEEB, alpha 40% |
| trees_far | 0.15 | Árboles lejanos densos | #1A3A0A, #2D5016 |
| trees_mid | 0.3 | Troncos y copas medianas | #3A6B1E, #4A7C2E |
| light_rays | 0.5 | Rayos de sol atravesando hojas | #F0C060, alpha 30% |
| foreground | 0.7 | Setas, helechos, arbustos | #6B8F3A, #D94040, #F0C060 |

## AI Prompt
Pixel art fondo parallax 512×256 de bosque frondoso con luz filtrada. Cielo apenas visible a través de copas densas. Múltiples capas de árboles en verdes oscuros. Rayos de sol dorados diagonales atravesando las hojas. Setas rojas brillantes como puntos de atención en primer plano. Helechos y arbustos bajos. Ambiente de calma y concentración. 5 capas separadas. Rayos con transparencia.

## Acceptance Criteria
- [ ] All layers within 512×256 bounds
- [ ] Capas de árboles crean profundidad
- [ ] Palette matches Art Bible
- [ ] Rayos de sol con transparencia visible
- [ ] Setas rojas destacan en foreground
- [ ] Tileable horizontalmente
