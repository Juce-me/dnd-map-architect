# Site Overview (Level 1)

Zoom-out scheme of one whole dungeon complex, building, fortress, temple, or
lair. 10-50 ft per square (default 10 ft), square grid. Read
`overview-rules.md` first; it defines the scale ladder, scale chain, scale
bar, and print math used here.

## Intake Questions

Required:

- What is the site (dungeon, fortress, manor, temple, cave system)?
- Which floor or level does this sheet show? One overview map per floor;
  stairs and shafts are cross-floor markers.
- What real-world footprint does the site cover, or which battlemaps compose it?
- Audience: DM version (secrets visible) or player version (secrets hidden)?

Adaptive (ask only when relevant):

- Which existing battlemap specs should embed as children (file paths)?
- What named wings or zones exist, and roughly where do they sit?
- Where are the entrances, and which connections matter (corridors, stairs,
  bridges, underground passages)?
- Should one edge show exterior context (approach road, cliff, surrounding
  settlement)?

## Spec Notes

- `scale.level`: `"site"`; `unit_per_cell` 10-50 ft.
- Children are battlemaps only; they are almost always blocks. Cross-check
  each with `spec_path`.
- Features: wings, courtyards, routes, and entrances as rectangles; stairs
  and secret passages as 1-cell features with a `kind`.

## Prompt Template

```text
Create a strict top-down orthographic site overview scheme (an architectural
plan, not a battlemap).

Coordinate grid (most important):
- Columns labeled 0-{width_cells - 1} along the top edge
- Rows labeled 0-{height_cells - 1} along the left edge
- Exactly {width_cells} columns and {height_cells} rows of equal squares
- Dark grid lines drawn above all art, blocks, shadows, and labels

Scale (must stay accurate):
- {unit_per_cell} ft per square
- Scale bar spanning exactly {scale_bar_length_cells} squares, labeled
  "{scale_bar_length_cells x unit_per_cell} ft"
- Print: {paper}, {physical_grid_mm} mm per square inside {margin_mm} mm
  margins, {dpi} DPI (omit this line when print is disabled)

Site identity:
- Name: {name}; type: {overview_type}; atmosphere: {atmosphere}

Layout (source of truth):
- {each child block: "{name}: rows {y}-{y + height - 1}, columns {x}-{x + width - 1}"}
- {each feature: wings, routes, entrances, stairs with exact rows/columns}
- {short label on every block and marker}

Rendering requirements:
- Simplified architectural blocks with wall outlines, no interior furniture
- Routes and connections drawn as clear corridors or dashed paths
- Entrances marked with arrows; stairs with standard stair glyphs
- Light parchment scheme style; art never obscures grid lines or labels
```

## Negative Constraints

```text
Negative constraints (strict):
- No isometric view, perspective angle, or 3D camera
- No extra rows or columns beyond {width_cells} x {height_cells}
- No furniture, room interiors, creatures, tokens, monsters, or NPCs
- No hidden, cropped, faded, or missing grid cells
- No decorative border that changes the mapped area
- No grid lines obscured by art, blocks, shadows, or labels
- No scale bar shorter or longer than {scale_bar_length_cells} grid cells
- Player version only: no secret rooms or hidden passages rendered
```

## Post-Generation Checklist

1. Numbered columns and rows are visible with exact counts.
2. Count cells on both axes; they must match the spec.
3. The scale bar spans exactly `length_cells` cells and its label equals
   `length_cells x unit_per_cell` ft.
4. Every child block sits at its declared rows/columns at the declared size.
5. Entrances, stairs, and routes appear where the spec places them.
6. No interior furniture or tactical detail leaked in.
7. Player version: secrets are absent.
8. Print: a measured cell equals `physical_grid_mm`; the scale bar measures
   `length_cells x physical_grid_mm`.
