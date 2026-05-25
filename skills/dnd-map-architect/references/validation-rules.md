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

Warn on:

- Every route funnels through a single one-square chokepoint.
- No cover in ranged-heavy rooms.
- No alternate path in stealth-focused maps.
- Excessive decorative clutter over playable grid squares.

## Grid Validation

For square grids:

- `image_width_px / width_squares` must be an integer.
- `image_height_px / height_squares` must be an integer.
- Both pixel-per-square values must match.
- Corridor path segments must be orthogonal.
- Grid lines must remain straight and evenly spaced.
- Tokens must fit cleanly in every walkable square.

For hex grids:

- Declare orientation: pointy-top or flat-top.
- Declare coordinate system: axial or offset.
- Diagonal neighbor path steps are allowed when the path still attaches to connected room boundaries.
- Avoid image prompts that imply square tiles.

## Print Validation

Block or correct:

- Missing paper size for printable output.
- `print.enabled` must be true or false.
- `split_pages` must be true or false when present.
- Missing physical grid size.
- Negative margins.
- Output that cannot fit single-page and lacks split-page support.

Warn:

- Margins below 0.2 inches.
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
  "warnings": ["PRINT_MARGIN_TIGHT: margins below 0.2 inches may be clipped"]
}
```

No image prompt should be produced while `errors` is non-empty; provide blocker corrections instead.
