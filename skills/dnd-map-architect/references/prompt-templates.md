# Prompt Templates

Generate prompts only after the topology and validation pass. The prompt must preserve the dungeon plan, not invent a new one.

## Battlemap Prompt Template

```text
Create a top-down Dungeons & Dragons battlemap with an exact {grid_type} grid.

Map size: {width_squares} by {height_squares} squares.
Scale: {tile_scale_ft} ft per square.
Output size: {image_width_px} by {image_height_px} px, exactly {pixels_per_square} px per square.
Print target (include when printing to paper):
- Paper: {paper}, {paper_width_mm} by {paper_height_mm} mm, {print_orientation}.
- Physical grid: {physical_grid_mm} mm per square inside {margin_mm} mm margins.
- Printed map area: {map_width_mm} by {map_height_mm} mm; each square must measure {physical_grid_mm} mm on paper.
- Print resolution: {dpi} DPI, so render {print_pixels_per_square} px per square ({print_image_width_px} by {print_image_height_px} px) to hit that physical size.
Grid: straight, evenly spaced, non-distorted, aligned edge to edge.

Dungeon identity:
- Type: {dungeon_type}
- Architecture: {architectural_style}
- Civilization: {civilization}
- Atmosphere: {atmosphere}
- Corruption state: {corruption_state}

Layout source of truth:
{room_list_with_coordinates}
{corridor_list_with_coordinates}
{stairs_secret_paths_and_locks}

Tactical requirements:
{encounter_placement_plan}
{cover_sightline_hazard_notes}
{creature_traversal_constraints}

Rendering requirements:
- Top-down orthographic battlemap.
- Clear walls, doors, stairs, ledges, hazards, and walkable spaces.
- Playable grid squares remain readable and token-safe.
- The grid must cover every square of the image, including door thresholds, stair landings, corridor mouths, archway interiors, and any dark or void area outside rooms. No square may be obscured or overwritten by door art, threshold tiles, decorative inlays, or texture fills.
- Do not change room count, room positions, corridor connections, or grid scale.
```

## Negative Constraints

Append relevant constraints:

```text
Do not use perspective view.
Do not warp, stretch, bend, or fade the grid.
Do not omit grid lines on any square. Door thresholds, stair landings, archway openings, and corridor entrances must show the same continuous grid as the rest of the map.
Do not paint door art, ornamental tiles, or texture fills over grid lines.
Do not create disconnected rooms or floating corridors.
Do not add extra rooms, doors, walls, pits, or blocked paths that contradict the topology.
Do not place furniture or rubble so densely that tokens cannot stand in intended combat spaces.
Do not hide doors or stairs in visual noise.
Do not crop the outer grid.
Do not use a decorative border that changes the playable dimensions.
```

## Post-Generation Review Checklist

Check the generated image against the plan:

- Count grid squares horizontally and vertically.
- Confirm pixels per square or physical square alignment.
- Confirm grid lines are continuous on every square, including door thresholds, stair landings, archway interiors, and void areas outside rooms. A single missing square at a doorway breaks token alignment for that square.
- Confirm every room exists and is connected as specified.
- Confirm corridors have the specified width.
- Confirm doors align with walls and corridors.
- Confirm boss and large creature spaces are maneuverable.
- Confirm cover and hazards do not invalidate movement.
- Confirm print margins, split pages, or VTT dimensions remain valid.
- For print: measure a test page - each square must equal the spec's `physical_grid_mm`, and the full sheet must match the chosen paper.

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
