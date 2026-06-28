# Validation Rules

Run validation before image prompting and again after image generation. Treat validation as an engineering gate, not a style critique. Image prompts require a JSON spec and a passing validator-backed validation report.

## Structural Validation

Block on:

- Required identity fields must be non-empty strings.
- Non-secret room unreachable from entrance.
- Secret room without a declared accessible source.
- Room IDs, corridor IDs, and corridor endpoint IDs must be non-empty strings.
- Corridor without at least two valid room endpoints.
- Corridor path without continuous orthogonal geometry on square grids.
- Door without a target room or corridor.
- Room outside map bounds.
- Overlapping room footprints.
- Duplicate room or corridor IDs.
- Stairs, ladders, portals, or shafts without both endpoints.
- Wall gaps that create unintended access.

## Tactical Validation

Block on:

- Largest traversing creature cannot fit through required corridor.
- `largest_creature_traversal` must be an object when present.
- Boss room dimension is below creature footprint plus movement allowance.
- Combat room cannot fit party tokens plus enemies.
- Objective is unreachable during the encounter.
- Required stealth route does not exist.
- Required ranged combat has no viable sightline.
- Hazard, trap, or puzzle cannot be bypassed, disabled, or intentionally engaged.
- Tactical furniture, columns, walls, stairs, cover, obstacles, or similar map elements are drawn or specified smaller than one full grid square.
- Tactical objects have partial-square, diagonal, or ambiguous footprints that make occupied and walkable squares unclear.
- Tactical terrain crosses grid lines organically instead of having a cell-bound occupied footprint aligned to square boundaries.
- Tactical object art, shadows, caps, or overhangs spill outside the declared occupied footprint into neighboring squares.
- Grid lines disappear, stop, or become unreadable inside occupied terrain footprints such as fountains, tables, counters, stairs, columns, wall bands, or shelves.
- Multi-square terrain does not show internal scale-square subdivisions; for example, a 2 x 2 fountain without a visible internal grid cross is invalid.
- 1 x 1 columns, statues, or plinths cover their square's grid boundary so the occupied cell is not readable.

Warn on:

- Every route funnels through a single one-square chokepoint.
- No cover in ranged-heavy rooms.
- No alternate path in stealth-focused maps.
- Excessive decorative clutter over playable grid squares.
- Decorative sub-square detail reads as tactical cover, an obstacle, or a token-placement boundary.
- Round or curved terrain is not abstracted into an obvious square, rectangular, or stepped grid footprint.

## Grid Validation

For square grids:

- `image_width_px / width_squares` must be an integer.
- `image_height_px / height_squares` must be an integer.
- Both pixel-per-square values must match.
- Corridor path segments must be orthogonal.
- Grid lines must remain straight and evenly spaced.
- Tokens must fit cleanly in every walkable square.
- Tactical object footprints must align to whole grid squares; no object may partially consume a square.
- Occupied squares must be visually obvious from each object's outer footprint.
- A 1 x 1 object must fit entirely within one square, including decorative cap, base, and shadow.
- The grid must be visible above every terrain object and must subdivide every multi-square terrain footprint.

For hex grids:

- Declare orientation: pointy-top or flat-top.
- Declare coordinate system: axial or offset.
- Diagonal neighbor path steps are allowed when the path still attaches to connected room boundaries.
- Avoid image prompts that imply square tiles.

## Print Validation

All print fields are millimeters. Block or correct:

- Missing paper size for printable output.
- `print.enabled` must be true or false.
- `split_pages` must be true or false when present.
- Missing or non-positive `physical_grid_mm`.
- Negative `margin_mm`.
- Non-positive `dpi` when present.
- Output that cannot fit single-page and lacks split-page support (`PRINT_REQUIRES_SPLIT`).

Warn:

- Margins below 5 mm (`PRINT_MARGIN_TIGHT`).
- Map fills under half the usable page (`PRINT_UNDERFILL`): the grid is too small for the paper, or the paper too big for the grid. This is the check that catches a map whose squares are the right size but whose overall sheet does not match the page.
- Declared `dpi` and image pixels imply a printed square size that differs from `physical_grid_mm` (`PRINT_DPI_MISMATCH`).
- Very large page splits with no overlap or assembly labels.
- Dark backgrounds that waste ink unless requested.

## VTT Validation

Check:

- Pixels per square match the target VTT.
- Map dimensions are not excessively large for upload limits.
- Grid can be disabled or aligned in the VTT if grid is baked in.
- Walls, doors, and lighting notes are exportable as setup instructions when not embedded.

## Bundled Validator

Use:

```bash
.venv/bin/python skills/dnd-map-architect/scripts/validate_dungeon_spec.py <spec.json>
```

Use the active environment's `python` when the skill is installed outside the project. The validator checks deterministic structural, tactical, grid, and print constraints. It does not prove complete tactical quality and does not replace human review of generated images, line-of-sight nuance, or visual grid drift.

Report format:

```json
{
  "ok": false,
  "errors": ["STRUCTURE_UNREACHABLE_ROOM: vault is not reachable from entry"],
  "warnings": ["PRINT_MARGIN_TIGHT: margins below 5 mm may be clipped"]
}
```

No image prompt should be produced while `errors` is non-empty; provide blocker corrections instead.
