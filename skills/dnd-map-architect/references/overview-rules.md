# Overview Map Rules

Shared rules for all zoom-out (overview) map scales. Read this file plus exactly
one scale file (`overview-site.md`, `overview-settlement.md`,
`overview-region.md`, `overview-world.md`) per overview request.

## Scale Ladder

| Level | Covers | Unit per grid cell | Default | Default grid |
|---|---|---|---|---|
| battlemap (level 0) | single encounter area | 5 ft per square | 5 ft | square |
| site (level 1) | whole dungeon, building, fortress | 10-50 ft per square | 10 ft | square |
| settlement (level 2) | village, town, city | 50-500 ft per square | 100 ft | square |
| region (level 3) | province, march, wilderness | 1-10 miles per hex | 6 miles | hex |
| world (level 4) | continent, known world | 25-100 miles per hex | 50 miles | hex |

- Units are feet for levels 0-2 and miles for levels 3-4; 1 mile = 5280 ft.
- Region and world maps default to pointy-top hexes with offset coordinates;
  square grids are allowed when the user prefers them.
- A `unit_per_cell` outside the level's range is a blocking error; pick the
  next level instead of stretching the scale.

## Scale Chain

An overview map may place lower-level maps on itself as `children`:

- Every child declares a real-world `footprint` (width x height in ft or miles).
- **Block**: when the footprint spans at least one parent cell on either axis,
  the child renders as a block of `ceil(footprint / unit_per_cell)` cells per
  axis at a declared cell position.
- **Marker**: when the footprint is smaller than one parent cell on both axes,
  the child renders as a labeled point-of-interest marker in one cell.
- When the child has its own spec file, reference it with `spec_path` (relative
  to the parent spec file). The validator cross-checks the declared footprint
  against the child spec's grid math and fails on any mismatch.
- A child's level must be strictly lower than the parent's level.

Worked example: the bundled Ember Archive battlemap is 24 x 18 squares at 5 ft
= 120 x 90 ft. On a site overview at 10 ft per square it is a 12 x 9 block. On
a region map at 1 mile per hex it is a marker.

## Scale Bar

Every overview map carries a scale bar:

- It spans a whole number of grid cells (`scale_bar.length_cells`).
- Its label states the real-world length: `length_cells x unit_per_cell`
  (for example 5 squares = 50 ft, or 5 hexes = 30 miles).
- On printed maps the bar must measure true: bar length in mm equals
  `length_cells x physical_grid_mm`.

## Schematic Discipline

Overview maps are schemes, not battlemaps:

- Show blocks, routes, markers, terrain, water, walls, and labels.
- Never render furniture, creatures, tokens, NPCs, armies, or tactical detail.
- Label key locations with short names; numbered coordinates handle the rest.

## Grid And Coordinates

- The numbered coordinate grid leads every prompt: columns 0 to width-1 along
  the top, rows 0 to height-1 along the left, exact counts stated.
- Grid lines are drawn above all art, terrain, blocks, and labels.
- Square grids require identical pixels per cell on both axes.

## Print Math

Work in millimeters. Defaults: 28 mm per cell, 6 mm margins, 300 DPI
(consistent with `print-rules.md`).

Square grids use the `print-rules.md` formulas:
`usable_mm = paper_side - 2 x margin_mm`, then
`max_cells = floor(usable_mm / physical_grid_mm)` per axis.

Hex grids tile differently. For pointy-top hexes with flat-to-flat width `w`
mm and corner-to-corner height `h = 2w / sqrt(3)`:

- `columns_max = floor((usable_width - 0.5w) / w)` (offset rows shift by w/2).
- `rows_max = floor((usable_height - 0.25h) / 0.75h)` (rows overlap by h/4).
- Flat-top hexes swap the axes.

Worked example - A3 landscape (408 x 285 mm usable) at 28 mm flat-to-flat,
pointy-top: `h = 32.3 mm`; columns = floor((408 - 14) / 28) = 14; rows =
floor((285 - 8.1) / 24.2) = 11. A region map prints 14 x 11 hexes per sheet.

## Overview Spec Shape

```json
{
  "map_kind": "overview",
  "identity": {"name": "...", "overview_type": "..."},
  "scale": {"level": "site", "unit_per_cell": 10},
  "technical": {
    "grid_type": "square",
    "width_cells": 14,
    "height_cells": 10,
    "image_dimensions_px": [1400, 1000],
    "scale_bar": {"length_cells": 5, "label_units": 50},
    "print": {"enabled": true, "paper": "A3", "physical_grid_mm": 28, "margin_mm": 6, "split_pages": false}
  },
  "features": [
    {"id": "approach", "name": "Approach Road", "kind": "route", "x": 0, "y": 9, "width": 14, "height": 1}
  ],
  "children": [
    {
      "id": "ember-archive", "name": "Ember Archive", "level": "battlemap",
      "representation": "block", "x": 1, "y": 0,
      "footprint": {"width": 120, "height": 90, "unit": "ft"},
      "block": {"width": 12, "height": 9},
      "spec_path": "valid-dungeon-spec.json"
    }
  ]
}
```

Hex grids add `"orientation": "pointy"` and `"coordinate_system": "offset"`
inside `technical`. Validate every overview spec with
`scripts/validate_overview_spec.py` before writing any image prompt.
