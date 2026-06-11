# World Overview (Level 4)

Atlas-style scheme of a continent or the known world. 25-100 miles per hex
(default 50 miles), pointy-top hexes with offset coordinates by default
(square grid allowed). Read `overview-rules.md` first.

## Intake Questions

Required:

- What does the sheet cover: one continent, several, or the known world?
- Which kingdoms or realms must appear, and which borders matter?
- What are the defining physical features (coastlines, mountain ranges,
  great rivers, seas)?
- How many miles per hex (or what total extent must fit the sheet)?

Adaptive (ask only when relevant):

- Capitals and major cities: which deserve markers and labels?
- Climate bands or biomes: should the map show them (tundra, desert, jungle)?
- Sea routes or trade lanes between ports?
- Which child region maps have spec files to chain?

## Spec Notes

- `scale.level`: `"world"`; `unit_per_cell` 25-100 miles; `grid_type` hex
  with `orientation` and `coordinate_system`, or square.
- Children: regions (blocks when they span hexes) and settlements (markers;
  even a large city is far below one 50-mile hex).
- Features: landmasses, seas, mountain ranges, rivers, kingdom borders, and
  climate bands as rectangles or cell-run routes with a `kind`.

## Prompt Template

```text
Create a top-down atlas hex map of {name}, a {overview_type}.

Hex grid (most important):
- Pointy-top hexes in offset rows
- Columns labeled 0-{width_cells - 1} along the top edge
- Rows labeled 0-{height_cells - 1} along the left edge
- Exactly {width_cells} columns and {height_cells} rows of equal hexes
- Dark hex outlines drawn above all terrain art

Scale (must stay accurate):
- {unit_per_cell} miles per hex
- Scale bar spanning exactly {scale_bar_length_cells} hexes, labeled
  "{scale_bar_length_cells x unit_per_cell} miles"
- Print: {paper}, {physical_grid_mm} mm flat-to-flat per hex inside
  {margin_mm} mm margins, {dpi} DPI (omit this line when print is disabled)

Layout (source of truth):
- {coastlines and seas with hex ranges}
- {mountain ranges, great rivers, deserts, forests with hex ranges}
- {kingdom borders as dashed lines along hex edges}
- {each child region as a block and each capital or major city as a keyed
  marker at exact hexes}
- {label hierarchy: realms largest, regions medium, cities smallest}

Rendering requirements:
- Atlas cartography: muted terrain fills, clear coastlines, elegant labels
- Capitals as distinct star or keep icons; other cities as smaller dots
- Borders, rivers, and routes readable above terrain, below hex outlines and
  labels
```

## Negative Constraints

```text
Negative constraints (strict):
- No isometric view, perspective angle, or 3D camera
- No extra hex columns or rows beyond {width_cells} x {height_cells}
- No armies, creatures, monsters, ships in battle, or scene illustrations
- No hidden, cropped, faded, or missing hexes
- No decorative border that changes the mapped area
- No hex outlines obscured by terrain art or labels
- No scale bar shorter or longer than {scale_bar_length_cells} hexes
```

## Post-Generation Checklist

1. Numbered hex columns and rows are visible with exact counts.
2. Count hexes on both axes; they must match the spec.
3. The scale bar spans exactly `length_cells` hexes and its label equals
   `length_cells x unit_per_cell` miles.
4. Coastlines, ranges, rivers, and borders sit where the spec places them.
5. Every region block and city marker sits at its declared hex.
6. The label hierarchy reads correctly (realm over region over city).
7. Print: a measured hex equals `physical_grid_mm` flat-to-flat; the scale
   bar measures true.
