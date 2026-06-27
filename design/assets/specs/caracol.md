# Asset Spec: Caracol

## Source
personaje

## Visual Rules (from Art Bible)
- Shape: espiral, orgánico
- Primary colors: caparazón #C9A8E8, cuerpo #7EC8A0
- Size: 128×128 per frame
- Semantic meaning: introspección, contemplación, llevar el hogar a cuestas

## Sprite Sheets Required
| State | Frames | Directions | Size |
|-------|--------|-----------|------|
| idle | 2 | down, left, right | 128×128 |
| walk | 4 | down, left, right | 128×128 |
| talk | 2 | down | 128×128 |
| peek | 2 | down | 128×128 |
| retreat | 3 | down | 128×128 |

## AI Prompt
Pixel art caracol antropomórfico con caparazón en espiral de color lila suave (#C9A8E8) con destellos tornasolados. Cuerpo verde claro (#7EC8A0), ojos saltones en tallos delgados que se mueven independientemente. Caparazón grande con patrón espiral marcado en tono más oscuro. Sonrisa tímida y expresión amable. Estilo tierno y contemplativo. Fondo transparente, animación walk muy lenta con movimiento ondulante, caparazón estable durante el movimiento.

## Acceptance Criteria
- [ ] All frames within 128×128 bounds
- [ ] Palette matches Art Bible
- [ ] Espiral del caparazón claramente visible
- [ ] Ojos en tallos animados en talk/peek
- [ ] Movimiento walk ondulante y lento
