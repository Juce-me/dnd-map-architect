# Print, VTT, And Terrain Rules

## Print Targets

Default printable assumptions:

- Physical grid: 1 inch per square for 5 ft scale.
- Margin safety: 0.25 inches unless the user specifies otherwise.
- Paper: ask the user for A4, A3, Letter, Ledger, or custom.
- Split pages: required for most full battlemaps at 1 inch squares.

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
