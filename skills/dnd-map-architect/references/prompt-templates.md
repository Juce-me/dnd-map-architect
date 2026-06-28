# Prompt Templates

Generate prompts only after the topology and validation pass. The prompt must preserve the dungeon plan, not invent a new one.

## Battlemap Prompt Template

**Critical: derive the grid scale from the paper FIRST (see `references/print-rules.md`), then build the prompt. Picking a square count before checking the page is the most common reason a printed map "misses" the sheet. Emphasis on grid visibility and exact coordinate labeling improves model accuracy significantly.**

Before writing the prompt, lock the scale:

1. `usable_mm = paper_side - 2 × margin_mm` for each axis, in the chosen orientation.
2. `max_squares = floor(usable_mm / physical_grid_mm)` per axis.
3. `width_squares` × `height_squares` must be ≤ those maxima. State the orientation that matches the chosen dimensions (portrait when height > width, landscape when width > height) — do not mislabel it.

Reference scales at 28 mm/square, 6 mm margins:
- A3 portrait (297 × 420 mm): 10 × 14 squares (grid 280 × 392 mm).
- A3 landscape (420 × 297 mm): 14 × 10 squares (grid 392 × 280 mm).
- A4 portrait (210 × 297 mm): 7 × 10 squares (grid 196 × 280 mm).

```text
Create a strict top-down orthographic D&D battlemap.

Paper and grid scale (most important — fixes the printed size):
- Paper: {paper}, {paper_width_mm} by {paper_height_mm} mm, {print_orientation} (height {>|<} width must match this label).
- Physical grid: {physical_grid_mm} mm per square inside {margin_mm} mm margins.
- This yields exactly {width_squares} columns by {height_squares} rows (grid {grid_width_mm} by {grid_height_mm} mm).
- Print resolution: {dpi} DPI, so render {print_pixels_per_square} px per square ({print_image_width_px} by {print_image_height_px} px) so each square measures {physical_grid_mm} mm on paper.

Coordinate grid (must be visible):
- Columns labeled {start_col}–{end_col} along the top edge
- Rows labeled {start_row}–{end_row} along the left edge
- Exactly {width_squares} columns and {height_squares} rows
- Every grid square must be equal size
- Dark grid lines must remain visible across the whole map

Do not make a decorative border that changes the playable area.
The numbered labels may sit outside or on the very edge of the playable area, but the playable grid itself must remain exactly {width_squares}×{height_squares}.

Scale: {tile_scale_ft} ft per square.
Output size: {image_width_px} by {image_height_px} px, exactly {pixels_per_square} px per square.

Dungeon identity:
- Type: {dungeon_type}
- Atmosphere: {atmosphere}
- Style: {architectural_style}

Layout (source of truth):
{room_list_with_specific_row_col_coordinates}
{walls_doors_stairs_with_exact_grid_positions}
{connection_points_and_passageways}

Grid-scale object footprints (mandatory):
- Every tactical object must occupy whole grid squares and be at least 1 square.
- Furniture, columns, walls, stairs, cover, obstacles, statues, planters, fountains, shelves, cabinets, and counters must use integer footprints such as 1x1, 1x2, 2x1, or 2x2.
- No furniture, column, wall, stair, or cover object may be smaller than one full grid square or sit across partial squares.
- The occupied footprint of each tactical object must be obvious and aligned to grid-square boundaries. Round or curved objects must be abstracted into square, rectangular, or stepped full-cell footprints; decorative curves may sit inside the footprint but must not change which squares are occupied.
- All visible parts of a tactical object must stay inside its declared footprint, including column bases, plinth caps, table edges, shadows, highlights, and decorative overhangs. A 1x1 object must fit entirely inside one square.
- Grid lines must remain visible on top of every occupied footprint. Multi-square objects must show their internal scale-square subdivisions: a 2x2 fountain must show the internal cross of four squares, tables/counters/stairs/shelves must be subdivided by grid lines, and 1x1 columns/plinths must leave all four cell edges readable.
- Small decorative details may appear only as flat texture; they must not imply cover, block movement, hide grid lines, or make token placement ambiguous.

Example of exact specification (adapt as needed):
- Rows {start_row}–{room1_end}: {room1_name}, {room1_width}×{room1_height} squares
- Dividing wall between rows {wall_row1} and {wall_row2}
- {doorway_width}-square doorway at columns {col_start}–{col_end} between rows {row1} and {row2}
- Stairs at columns {col_start}–{col_end} on row {row_num}

Tactical readability:
- Furniture must not overcrowd the room
- Leave clear token-playable squares throughout
- Cover objects should be visible, occupy whole-square footprints, and not cover the grid
- Grid lines must be drawn above all art, furniture, terrain, shadows, stairs, doors, and thresholds, including through fountains, columns, tables, counters, shelves, and wall bands

Rendering requirements:
- Strict top-down orthographic view (no perspective, no isometric)
- Every grid square visible and labeled with coordinates
- Clear walls, doors, stairs, and walkable spaces
- Furniture and cover visible as full-square tactical pieces, with walkable squares unambiguous
- Dark grid lines continuous across all squares

No decorative borders. No grid distortion. No sub-square tactical objects. No missing squares at doorways or thresholds.
```

## Negative Constraints

**Use this exact list for all map prompts:**

```text
Negative constraints (strict):
- No isometric view
- No perspective angle
- No 3D camera
- No extra rows or columns beyond the specified grid size
- No large black void or gaps between rooms
- No hidden, cropped, or faded grid squares
- No decorative border that changes the playable area
- No grid lines obscured by art, furniture, shadows, doors, stairs, or thresholds
- No monsters, enemies, or NPCs rendered on the map
- No missing grid squares at doorways, thresholds, or archway openings
- No furniture, columns, walls, stairs, cover, or obstacles smaller than one full grid square
- No partial-square tactical object footprints
- No curved, diagonal, or organic terrain footprints that cross grid lines ambiguously
- No tactical object art, cap, base, shadow, or overhang spilling outside its declared grid footprint
- No grid lines missing inside occupied terrain footprints
- No multi-square fountain, table, counter, stair, shelf, wall band, or terrain feature without visible internal scale-square subdivisions
- No 1x1 column, statue, or plinth covering the readable grid boundary of its square
- Grid lines must be visible and continuous across the entire map
- All {width_squares}×{height_squares} squares must be equally sized and labeled with coordinates
```

## Post-Generation Review Checklist

**Critical checks (in order):**

1. **Coordinate grid:** Confirm numbered columns (0–{width-1}) and rows (0–{height-1}) are visible on all edges.
2. **Grid count:** Count grid squares horizontally and vertically. Must be exactly {width_squares}×{height_squares}.
3. **Grid size:** Every grid square must be identical size. No distortion, warping, or fading.
4. **Grid visibility:** Dark grid lines must be visible across the entire map, including door thresholds, stair landings, and all archway openings. A single missing or faded square breaks token alignment.
5. **Room positions:** Confirm each room exists at the specified rows/columns and is the correct size.
6. **Doorways and connections:** Confirm walls, doorways, and stairs are positioned exactly as specified.
7. **Object footprint scale:** Every tactical object is at least one full square and aligned to whole grid-square boundaries; no furniture, column, wall, stair, cover, fountain, counter, table, or obstacle is drawn as a partial-square, diagonal, curved, or ambiguous terrain footprint, and no visible overhang spills outside the declared footprint.
8. **Scale squares over terrain:** Grid lines remain visible over occupied terrain; a multi-square object such as a fountain/table/counter/stair/shelf/wall band shows internal scale-square subdivisions, and every 1x1 column/plinth leaves its cell boundary readable.
9. **Furniture and cover:** Furniture should be visible but must not obscure grid lines or create impassable squares.
10. **No decorative border:** Labels may sit on the edge, but the playable area remains exactly {width_squares}×{height_squares}. No extra border or void area.
11. **Tactical readability:** All intended token-playable squares should be clear and unobstructed.
12. **Print alignment (if applicable):** Measure a test page - each square must equal the spec's `physical_grid_mm`, and the full sheet must match the chosen paper.

**If any check fails:** Use the Correction Prompt Template to request a revision targeting the specific issue.

## Correction Prompt Template

```text
Revise the battlemap to fix these blocking gameplay issues while preserving the existing art style:

Required corrections:
{ordered_correction_list}

Do not change:
- Map size: {width_squares} by {height_squares} squares.
- Output size: {image_width_px} by {image_height_px} px.
- Pixels per square: {pixels_per_square}.
- Physical print scale: {physical_grid_mm} mm per square on {paper}.
- Room topology: {topology_summary}.

The corrected map must keep a straight, evenly spaced, non-distorted grid and must keep all intended combat spaces token-playable.
```
