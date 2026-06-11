# Region Overview (Level 3)

Hex-crawl scheme of a province, march, or wilderness region. 1-10 miles per
hex (default 6 miles), pointy-top hexes with offset coordinates by default
(square grid allowed). Read `overview-rules.md` first.

## Intake Questions

Required:

- What region is this, and what does it border?
- What is the dominant terrain mix (forest, hills, mountains, swamp, plains,
  coast)?
- Which settlements and sites must appear, and where roughly?
- How many miles per hex (or what total extent must fit the sheet)?

Adaptive (ask only when relevant):

- Roads and rivers: which routes connect the settlements?
- Political borders: whose territory, and do borders need to be visible?
- Should hexes carry travel annotations (for example one hex = one day on
  foot at 6 miles per hex)?
- Which child maps (settlements, sites) have spec files to chain?

## Spec Notes

- `scale.level`: `"region"`; `unit_per_cell` 1-10 miles; `grid_type` hex with
  `orientation` and `coordinate_system`, or square.
- Children: settlements and sites. At miles per hex nearly all are markers;
  a sprawling city may be a block (apply the rule from `overview-rules.md`).
- Features: terrain areas, rivers, roads, and borders as rectangles or
  cell-run routes with a `kind`.
- A3 landscape at 28 mm flat-to-flat pointy hexes fits 14 x 11 hexes (see
  the worked example in `overview-rules.md`).

## Prompt Template

```text
Create a top-down regional hex map of {name}, a {overview_type}.

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
- {terrain per area: forest, hills, mountains, swamp, plains with hex ranges}
- {rivers and roads as hex-to-hex routes}
- {political borders as dashed lines along hex edges}
- {each child settlement or site as a block or keyed marker at exact hexes}
- {short labels on settlements, sites, and major terrain}

Rendering requirements:
- Classic hex-crawl cartography: one dominant terrain symbol per hex
- Settlement icons sized by type (village, town, city); sites as keyed symbols
- Rivers, roads, and borders readable above terrain, below hex outlines and
  labels
```

## Negative Constraints

```text
Negative constraints (strict):
- No isometric view, perspective angle, or 3D camera
- No extra hex columns or rows beyond {width_cells} x {height_cells}
- No armies, creatures, monsters, or battle scenes
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
4. Terrain areas, rivers, roads, and borders sit where the spec places them.
5. Every settlement and site marker or block sits at its declared hex.
6. Hex outlines are continuous across the whole map.
7. Print: a measured hex equals `physical_grid_mm` flat-to-flat; the scale
   bar measures true.
