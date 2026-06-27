# Asset Spec: Tiles — Valle del Lenguaje

## Source
tile

## Visual Rules (from Art Bible)
- Shape: curvo, fluido, letras
- Primary colors: #F0C060, #E8A84A, #A8D5BA, #E8B4B8
- Size: 32×32 per tile
- Semantic meaning: comunicación, expresión, flujo de palabras

## Tiles Required
| Tile ID | Type | Palette | Notes |
|---------|------|---------|-------|
| meadow_floor | suelo | #A8D5BA, #8BC4A0 | Pradera suave base |
| flower_letter_a | decoración | #F0C060, #E8A84A | Flor con forma de A |
| flower_letter_b | decoración | #E8B4B8, #D4A0A4 | Flor con forma de B |
| flower_letter_c | decoración | #4A90D9, #6DB8E8 | Flor con forma de C |
| path_words | suelo | #F0C060, alpha 30% | Camino con palabras sutiles |
| scroll_paper | objeto | #FFF5F0, #E8DCC8 | Pergamino abierto |
| quill | objeto | #8B6F47, #F0C060 | Pluma de escribir |
| bookshelf | estructura | #8B6F47, #D4C4A0 | Estante de libros pequeño |
| floating_word | decoración | #F0C060, #E8A84A | Palabra flotante brillante |
| echo_ring | efecto | #E8B4B8, alpha 30% | Anillo de eco/sonido |
| poetry_tree | objeto | #7EC8A0, #E8B4B8 | Árbol con versos colgando |
| bridge_rainbow | estructura | #E8B4B8, #F0C060, #4A90D9 | Puente arcoíris pequeño |

## AI Prompt
Tile pixel art 32×32 de valle bucólico lleno de lenguaje. Pradera verde suave (#A8D5BA) con flores que forman letras. Palabras brillantes flotando en el aire. Pergaminos y plumas como objetos. Árbol con poemas colgando de sus ramas. Anillos de eco rosados. Puente arcoíris. Ambiente de creatividad y comunicación. Tileable con paleta limitada a 14 colores. Flores-letra distinguibles a 32×32.

## Acceptance Criteria
- [ ] All tiles within 32×32 bounds
- [ ] Tileable seamless
- [ ] Palette matches Art Bible
- [ ] Flores con forma de letra legibles
- [ ] Palabras flotantes visibles sin saturar
- [ ] Bridge tiles conectan ambos lados
