# Asset Spec: UI — Elementos de Interfaz

## Source
ui

## Visual Rules (from Art Bible)
- Shape: rounded, orgánico con bordes suaves
- Primary colors: #A8D5BA, #F0C060, #E8B4B8, #FFF5F0
- Size: 32×32 base, escalable
- Semantic meaning: accesibilidad, calidez, juego amigable

## Common Properties
- Border radius: 8px en todos los paneles
- Font style: sans-serif bold, color #2D3436
- Shadow: suave, color #2D3436 alpha 20%
- Hover state: escala 1.05
- Disabled state: alpha 50%

## Elements Required

### Buttons
| Element | State | Size | Palette | Notes |
|---------|-------|------|---------|-------|
| btn_primary | normal | 128×48 | #A8D5BA, #8BC4A0 | Botón principal verde |
| btn_primary | hover | 128×48 | #7EC8A0, #6BB890 | hover más oscuro |
| btn_primary | pressed | 128×48 | #6BB890, #5AA880 | pressed más oscuro |
| btn_secondary | normal | 128×48 | #F0C060, #E8A84A | Botón secundario dorado |
| btn_secondary | hover | 128×48 | #E8A84A, #D4923A | hover más oscuro |
| btn_secondary | pressed | 128×48 | #D4923A, #C08030 | pressed más oscuro |
| btn_icon | normal | 48×48 | #FFF5F0, #E8DCC8 | Botón cuadrado icono |
| btn_icon | hover | 48×48 | #E8DCC8, #D4C4A0 | hover más oscuro |
| btn_tab | normal | 96×32 | #FFF5F0, #E8DCC8 | Pestaña de menú |
| btn_tab | active | 96×32 | #A8D5BA, #8BC4A0 | Pestaña activa verde |

### Panels & Frames
| Element | Size | Palette | Notes |
|---------|------|---------|-------|
| panel_dialogue | 512×128 | #FFF5F0, #E8DCC8 | Panel de diálogo inferior, bordes redondeados |
| panel_inventory | 256×320 | #FFF5F0, #E8DCC8 | Inventario, fondo semitransparente |
| panel_menu | 256×320 | #FFF5F0, #E8DCC8 | Menú principal/pausa |
| panel_biome_select | 480×320 | #FFF5F0, #E8DCC8 | Selector de biomas |
| panel_quest | 320×256 | #FFF5F0, #E8DCC8 | Panel de misión/objetivo |
| panel_score | 160×64 | #FFF5F0, #E8DCC8 | Panel de puntuación HUD |
| frame_portrait | 64×64 | #A8D5BA, #8BC4A0 | Marco para retrato personaje |
| border_golden | 256×4 | #F0C060, #E8A84A | Borde decorativo dorado |

### Icons (32×32)
| Element | Type | Palette | Meaning |
|---------|------|---------|---------|
| icon_attention | action | #F0C060, #E8A84A | Ojo / Biome Atención |
| icon_memory | action | #4A90D9, #6DB8E8 | Libro / Biome Memoria |
| icon_reasoning | action | #B8B8B8, #8B8B8B | Engranaje / Biome Razonamiento |
| icon_language | action | #E8B4B8, #D4A0A4 | Letra / Biome Lenguaje |
| icon_math | action | #F0C060, #FFFFFF | Números / Biome Matemáticas |
| icon_visual | action | #C9A8E8, #E8B4B8 | Pincel / Biome Visual |
| icon_speed | action | #E8A84A, #FFFFFF | Relámpago / Biome Velocidad |
| icon_home | nav | #A8D5BA, #7EC8A0 | Casa / volver al jardín |
| icon_map | nav | #D4A76A, #C49A5C | Mapa |
| icon_settings | nav | #8B8B8B, #6B6B6B | Engranaje ajustes |
| icon_audio_on | toggle | #F0C060, #E8A84A | Altavoz activado |
| icon_audio_off | toggle | #6B6B6B, #5A5A5A | Altavoz silenciado |
| icon_star | feedback | #F0C060, #FFFFFF | Estrella / logro |
| icon_heart | feedback | #E8B4B8, #D4A0A4 | Corazón / vida |
| icon_orb | feedback | #4A90D9, #6DB8E8 | Orbe / coleccionable |
| icon_check | feedback | #7EC8A0, #6BB890 | Check / completado |
| icon_arrow_right | nav | #2D3436, #1A1A1A | Flecha derecha |
| icon_arrow_left | nav | #2D3436, #1A1A1A | Flecha izquierda |
| icon_interact | action | #F0C060, #FFFFFF | Mano / interactuar |
| icon_talk | action | #4A90D9, #6DB8E8 | Burbuja / hablar |

### HUD Elements
| Element | Size | Notes |
|---------|------|-------|
| health_bar | 128×16 | Barra de salud/progreso, verde a rojo |
| xp_bar | 128×16 | Barra de experiencia, azul |
| stamina_bar | 128×16 | Barra de energía/velocidad, amarilla |
| progress_circle | 48×48 | Círculo de progreso de actividad |
| minimap | 128×128 | Minimapa circular con marco dorado |
| compass_dots | 256×8 | Brújula de puntos direccionales |

### Cursors
| Element | Size | Notes |
|---------|------|-------|
| cursor_default | 24×24 | Mano abierta |
| cursor_interact | 24×24 | Mano señalando |
| cursor_talk | 24×24 | Burbuja de diálogo |
| cursor_grab | 24×24 | Mano agarrando |
| cursor_hidden | — | Invisible (cutscenes) |

### Text Elements
| Element | Font Size | Color | Usage |
|---------|-----------|-------|-------|
| heading_1 | 24px | #2D3436 | Títulos principales |
| heading_2 | 18px | #2D3436 | Subtítulos |
| body | 14px | #2D3436 | Texto normal |
| body_small | 12px | #5A5A5A | Texto secundario |
| dialogue_name | 14px | #8B6F47 | Nombre de personaje en diálogo |
| dialogue_text | 14px | #2D3436 | Texto de diálogo |

## AI Prompt
Pixel art UI elements 32×32 base para juego infantil educativo. Estilo redondeado y acogedor, bordes suaves. Iconos claros y legibles a 32×32 con paleta reducida. Botones verdes (#A8D5BA) y dorados (#F0C060). Paneles blanco crema (#FFF5F0) con sombra suave. Iconos representativos de cada biome cognitivo. Cursores de mano amigables. Elementos de HUD sencillos. Diseño limpio y accesible para niños.

## Acceptance Criteria
- [ ] Icons legibles a 32×32 con detalles mínimos
- [ ] Palette matches Art Bible
- [ ] Buttons tienen 3 estados visuales distinguibles
- [ ] Panels tienen borde redondeado y sombra
- [ ] Cursors reconocibles y funcionales
- [ ] HUD bars tienen color degradado
- [ ] Consistent border radius en todos los paneles
- [ ] States hover/pressed/disabled implementados
