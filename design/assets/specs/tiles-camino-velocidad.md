# Asset Spec: Tiles — Camino de la Velocidad

## Source
tile

## Visual Rules (from Art Bible)
- Shape: lineal, dinámico, flechas
- Primary colors: #E8A84A, #F0C060, #FFFFFF, #E8B4B8
- Size: 32×32 per tile
- Semantic meaning: velocidad, agilidad mental, reflejos, urgencia positiva

## Tiles Required
| Tile ID | Type | Palette | Notes |
|---------|------|---------|-------|
| track_gold | suelo | #E8A84A, #D4923A | Pista dorada principal |
| track_white | suelo | #FFFFFF, #E0E0E0 | Pista blanca secundaria |
| track_arrow_up | suelo | #F0C060, #E8A84A | Flecha dirección arriba |
| track_arrow_right | suelo | #F0C060, #E8A84A | Flecha dirección derecha |
| track_arrow_down | suelo | #F0C060, #E8A84A | Flecha dirección abajo |
| track_arrow_left | suelo | #F0C060, #E8A84A | Flecha dirección izquierda |
| speed_boost | decoración | #E8B4B8, #FFE4C4 | Zona de impulso rosa |
| dash_dots | decoración | #FFFFFF, alpha 50% | Estelas de movimiento |
| checkered_wall | estructura | #F0C060, #E8A84A | Pared estilo bandera cuadros |
| start_line | suelo | #FFFFFF, #F0C060 | Línea de salida |
| finish_line | suelo | #F0C060, #E8A84A | Línea de meta cuadros |
| time_orb | decoración | #F0C060, #FFFFFF | Orbe de tiempo brillante |
| wind_swirl | efecto | #FFFFFF, alpha 30% | Remolino de viento |
| boost_pad | suelo | #E8B4B8, #D4A0A4 | Plataforma de impulso |

## AI Prompt
Tile pixel art 32×32 de camino de carrera estilizado. Pista dorada (#E8A84A) con flechas de dirección marcadas. Líneas de salida y meta. Zonas de impulso rosadas (#E8B4B8). Estelas de movimiento blancas. Paredes a cuadros amarillos y blancos. Orbes de tiempo flotantes. Ambiente de velocidad y energía positiva. Tileable para crear pistas en cualquier dirección. Paleta limitada a 10 colores, diseño limpio y legible.

## Acceptance Criteria
- [ ] All tiles within 32×32 bounds
- [ ] Flechas de dirección claramente legibles a 32×32
- [ ] Tracks conectan seamless en todas direcciones
- [ ] Palette matches Art Bible
- [ ] Boost pads destacan visualmente
- [ ] Start/finish line distinguibles entre sí
