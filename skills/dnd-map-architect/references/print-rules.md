# Print, VTT, And Terrain Rules

## Print Targets

Work in millimeters. Inches are never stored in the spec.

Default printable assumptions:

- Physical grid: 28 mm per square (heroic-scale miniatures); set 25.4 mm for a true 1-inch grid.
- Margin safety: 6 mm unless the user specifies otherwise. Most desktop printers cannot print the outer ~5 mm of a sheet, so treat 0 mm margins as full-bleed only.
- Paper (portrait, width x height): A4 210 x 297 mm, A3 297 x 420 mm, Letter 215.9 x 279.4 mm, Ledger 279.4 x 431.8 mm. Ask the user, or take custom dimensions.
- Print resolution: 300 DPI default. Required px per square = `physical_grid_mm / 25.4 x DPI`, so 25.4 mm at 300 DPI is 300 px and 28 mm at 300 DPI is 331 px.
- Split pages: required whenever the map area exceeds one usable sheet.

Size the grid to the page, not the page to the grid. For a single sheet:

1. `usable_mm = paper_side - 2 x margin_mm` for each axis; try both orientations.
2. `max_squares = floor(usable_mm / physical_grid_mm)` per axis.
3. Choose `width_squares` x `height_squares` within those maxima.

Worked example - single A3 at 28 mm/square, 6 mm margins, landscape:

- usable = (420 - 12) x (297 - 12) = 408 x 285 mm.
- max = floor(408 / 28) x floor(285 / 28) = 14 x 10 squares (392 x 280 mm).
- 420 / 28 = 15 exactly, but 297 / 28 = 10.6, so the short edge never fills with whole 28 mm squares; expect a thin border there. Squares that are individually correct on a grid not sized this way is exactly what makes a map "miss" A3.

Include page-splitting notes:

- Page count and orientation.
- Overlap amount if needed.
- Cut or assembly labels.
- Whether the grid is baked into the image.
- Ink safety if large dark fills are present.

## VTT Targets

Common defaults:

- FoundryVTT: 100 px per square is a practical default.
- Roll20: 70 px per square is common; confirm when precision matters.
- Generic VTT: 100 px per square unless user specifies.

For VTT output, provide:

- Map dimensions in squares and pixels.
- Pixels per square.
- Grid type and whether the visual grid is included.
- Suggested wall, door, light, difficult terrain, and elevation notes.

## Modular Terrain Compatibility

When the user requests Dwarven Forge, WarLock Tiles, Dragonlock, or printable terrain:

- Ask for the system and available module inventory if exact assembly matters.
- Prefer room dimensions that map to common module sizes.
- Use corridor widths the terrain system can physically build.
- Treat walls as physical thickness, not just image outlines.
- Output tile counts, room modules, corridor modules, doors, stairs, and special pieces.

## Terrain Assembly Output

Use this compact format:

```text
Terrain system: WarLock Tiles
Rooms:
- Entry Hall: 6x5 floor, 2 doors, 18 wall segments
- Forge Vault: 12x7 floor, double door, 4 pillars, 1 raised dais
Corridors:
- c1: 3-wide, 2-square run
- c2: 3-wide, 3-square run
Special:
- 1 stair, 2 secret-door wall pieces, 4 half-height cover pieces
```

Do not claim exact commercial tile counts unless the user provides inventory or module dimensions.
