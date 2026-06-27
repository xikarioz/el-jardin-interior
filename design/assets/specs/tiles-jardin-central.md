# Asset Spec: Tiles — Jardín Central

## Source
tile

## Visual Rules (from Art Bible)
- Shape: orgánico, bordes suaves
- Primary colors: #A8D5BA, #7EC8A0, #D4A76A, #F0C060
- Size: 32×32 per tile
- Semantic meaning: seguridad, armonía, punto de partida acogedor

## Tiles Required
| Tile ID | Type | Palette | Notes |
|---------|------|---------|-------|
| grass_01 | suelo | #A8D5BA, #8BC4A0 | Pasto base con variación sutil |
| grass_02 | suelo | #A8D5BA, #7EC8A0 | Pasto con flores pequeñas blancas |
| grass_03 | suelo | #A8D5BA, #B5D8C0 | Pasto más claro, borde de camino |
| dirt_path | suelo | #D4A76A, #C49A5C | Camino de tierra, textura granular |
| dirt_path_corner | suelo | #D4A76A, #C49A5C | Esquina camino, 4 rotaciones |
| flower_bed | decoración | #F0C060, #E8A84A, #E8B4B8 | Macizo de flores 3 colores |
| bush | decoración | #7EC8A0, #6BB890 | Arbusto redondo pequeño |
| tree_base | objeto | #6B4226, #5A3820 | Base de tronco |
| tree_top | objeto | #7EC8A0, #A8D5BA | Copa de árbol, conecta con base |
| fountain_base | estructura | #B8B8B8, #A0A0A0 | Base de fuente central |
| fountain_water | estructura | #4A90D9, #6DB8E8 | Agua de fuente con brillo |
| bench | objeto | #8B6F47, #7A5E3A | Banco de madera |
| fence | estructura | #8B6F47, #7A5E3A | Cerca de madera, horizontal/vertical |
| lamp_post | estructura | #6B6B6B, #F0C060 | Poste de farolillo |
| gate | estructura | #8B6F47, #F0C060 | Puerta de entrada a biomas |

## AI Prompt
Tile pixel art 32×32 para jardín central estilo acogedor. Césped verde suave (#A8D5BA) con transiciones suaves a caminos de tierra (#D4A76A). Flores amarillas y rosas pequeñas. Arbustos redondeados. Fuente central con agua azul brillante. Farolillos dorados. Sin bordes duros, todo con transiciones orgánicas. Conjunto tileable sin costuras visibles. Paleta limitada a 12 colores.

## Acceptance Criteria
- [ ] All tiles within 32×32 bounds
- [ ] Tileable seamless en todas direcciones
- [ ] Palette matches Art Bible
- [ ] Grass tiles tienen variación sutil para evitar repetición
- [ ] Dirt path tiles funcionan como conjunto con esquinas
- [ ] Tree base + tree top se conectan verticalmente
