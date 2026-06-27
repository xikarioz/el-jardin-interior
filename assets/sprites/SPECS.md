# SPECS — El Jardín Interior

## Paleta de color (tonos argentinos cálidos)

| Nombre | Hex | Uso |
|--------|-----|-----|
| Verde Pampa | `#4A7C3F` | pasto, hojas |
| Verde Yerba | `#6B8E23` | arbustos, follaje |
| Celeste Cielo | `#87CEEB` | cielo, agua clara |
| Azul Río | `#4682B4` | ríos, lagos |
| Marrón Tierra | `#8B4513` | tierra, troncos |
| Ocre Pampa | `#D2B48C` | caminos, arena |
| Blanco Nube | `#F5F5DC` | nubes, fondos |
| Gris Piedra | `#696969` | rocas, sombras |
| Rojo Pasión | `#CD5C5C` | flores, detalles |
| Naranja Sol | `#FF8C00` | frutos, amanecer |
| Rosa Flor | `#FFB6C1` | flores, magia |
| Violeta Lejano | `#9370DB` | atardecer, magia |
| Oro Trigo | `#DAA520` | cosecha, detalles |
| Marrón Gráfito | `#2F1B0E` | outlines, texto |
| Piel Cálida | `#F0C8A0` | piel personajes |
| Piel Media | `#D2A679` | piel tono medio |

## Tamaños

| Elemento | Píxeles |
|----------|---------|
| Tiles | 32×32 |
| Personajes | 32×32 |
| Retratos | 16×16 |
| UI | 16×16 base |
| Objetos | 32×32 |

## Animaciones por personaje

| Personaje | Idle | Walk (4 dirs) | Talk | Sing | Especial |
|-----------|------|---------------|------|------|----------|
| Protagonista | ✓ | ✓ | - | - | Cape |
| Tortuga | ✓ | ✓ | ✓ | - | - |
| Zorro | ✓ | ✓ | ✓ | - | - |
| Búho | ✓ | ✓ | - | - | - |
| Mariposa | ✓ (partículas) | - | - | - | - |
| Caracol | ✓ | ✓ | - | - | - |
| Pájaro | ✓ | - | - | ✓ | - |
| Retratos (50) | 1 frame c/u | - | - | - | - |

## Formato
- PNG con canal alfa
- Spritesheet por personaje (no atlas global)
- 32×32 frames individuales para facilitar el import en Godot

## Convención de nombres
- `{personaje}_{animacion}_{dirección}.png`
- Direcciones: `down`, `left`, `right`, `up`
- Retratos: `portrait_{nombre}.png`
- UI: prefijo descriptivo
- Objetos: nombre directo
