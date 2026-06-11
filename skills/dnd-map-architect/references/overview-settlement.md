# Settlement Overview (Level 2)

Zoom-out scheme of a village, town, or city. 50-500 ft per square (default
100 ft), square grid. Read `overview-rules.md` first.

## Intake Questions

Required:

- What settlement is this (village, town, city), and roughly how large
  (population or extent in ft/miles)?
- What are the major districts or quarters?
- Walls and gates: is the settlement walled, and where are the gates?
- Audience: DM version or player version?

Adaptive (ask only when relevant):

- Water: river, harbor, coast, canals - where do they run?
- Which roads matter (gate-to-gate arteries, market squares, docks)?
- Which landmarks deserve labeled callouts (keep, temple, market, guildhall)?
- Which site maps (dungeons, keeps, manors) should embed as children, and do
  their spec files exist?

## Spec Notes

- `scale.level`: `"settlement"`; `unit_per_cell` 50-500 ft.
- Children are site maps (or battlemaps); most render as blocks at 50-100 ft
  per cell and as markers at coarser scales. Apply the block/marker rule from
  `overview-rules.md`.
- Features: districts, walls, gates, water, roads, and squares as rectangles
  with a `kind`.

## Prompt Template

```text
Create a strict top-down city-plan scheme of {name}, a {overview_type}.

Coordinate grid (most important):
- Columns labeled 0-{width_cells - 1} along the top edge
- Rows labeled 0-{height_cells - 1} along the left edge
- Exactly {width_cells} columns and {height_cells} rows of equal squares
- Dark grid lines drawn above all art and labels

Scale (must stay accurate):
- {unit_per_cell} ft per square
- Scale bar spanning exactly {scale_bar_length_cells} squares, labeled
  "{scale_bar_length_cells x unit_per_cell} ft"
- Print: {paper}, {physical_grid_mm} mm per square inside {margin_mm} mm
  margins, {dpi} DPI (omit this line when print is disabled)

Layout (source of truth):
- {each district block with exact rows/columns}
- {walls and gates with exact cells}
- {water cells: river, harbor, coast}
- {roads as routes between gates, squares, and districts}
- {each child site as a block or labeled marker at exact cells}
- {landmark callouts with short labels}

Rendering requirements:
- District blocks with rooftop-texture fill, no individual building interiors
- Walls as bold outlines with clear gate gaps
- Roads clearly readable between blocks; water clearly distinct from land
- Light parchment cartographic style; labels short and legible
```

## Negative Constraints

```text
Negative constraints (strict):
- No isometric view, perspective angle, or 3D camera
- No extra rows or columns beyond {width_cells} x {height_cells}
- No people, creatures, carts, armies, or building interiors
- No hidden, cropped, faded, or missing grid cells
- No decorative border that changes the mapped area
- No grid lines obscured by art, rooftops, water, or labels
- No scale bar shorter or longer than {scale_bar_length_cells} grid cells
- Player version only: no hidden or secret locations rendered
```

## Post-Generation Checklist

1. Numbered columns and rows are visible with exact counts.
2. Count cells on both axes; they must match the spec.
3. The scale bar spans exactly `length_cells` cells and its label equals
   `length_cells x unit_per_cell` ft.
4. Districts, walls, gates, water, and roads sit where the spec places them.
5. Every child site block or marker sits at its declared cells.
6. Landmark labels are legible and match the spec names.
7. Print: a measured cell equals `physical_grid_mm`; the scale bar measures
   true.
