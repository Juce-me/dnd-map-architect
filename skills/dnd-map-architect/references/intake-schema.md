# Intake Schema

Use intake to gather only information that changes topology, tactics, grid math, print output, or prompt constraints. Ask follow-up questions one at a time when the missing answer would change the plan.

## Required Categories

### Dungeon Identity

- `dungeon_type`: crypt, dwarven library, drow manor, fungal cavern, ruined fortress, spider temple, custom.
- `architectural_style`: natural cave, cut stone, carved temple, organic hive, modular terrain, mixed.
- `civilization`: current or original builders.
- `atmosphere`: grounded art direction, not a substitute for structure.
- `corruption_state`: pristine, ruined, flooded, burned, overgrown, magically warped.
- `gameplay_focus`: combat, exploration, stealth, chase, ritual interruption, defense, boss fight.
- `narrative_role`: entrance, midpoint, finale, side objective, lair, ambush site.

### Technical Constraints

- `grid_type`: square or hex.
- `orientation` and `coordinate_system`: required for hex grids; coordinate system must be axial or offset.
- `tile_scale_ft`: default 5.
- `width_squares` and `height_squares`: exact map size.
- `image_dimensions_px`: exact output pixels when VTT or image generation is needed.
- `print`: enabled, paper, `physical_grid_mm`, `margin_mm`, `dpi`, split-pages requirement. When printing to a single sheet, derive `width_squares`/`height_squares` from the page (see `references/print-rules.md`), do not pick them first and hope they fit.
- `vtt_target`: FoundryVTT, Roll20, Owlbear Rodeo, generic VTT, none.
- `terrain_system`: Dwarven Forge, WarLock Tiles, Dragonlock, printable terrain, none.
- `wall_thickness_squares`: default 0.5 for drawn maps; terrain systems may require whole-tile walls.
- `corridor_width_squares`: minimum planned width by traversal requirement.
- `map_ratio`: inferred from grid dimensions unless the user requires a format.

### Tactical Constraints

- `party_level` and `party_size`.
- `enemy_types`: creature families or encounter groups.
- `largest_creature_size`: tiny, small, medium, large, huge, gargantuan.
- `largest_creature_traversal.required`: whether the largest creature must move through corridors.
- `combat_density`: low, medium, high.
- `stealth_focus`: none, optional, primary.
- `ranged_combat_viability`: low, medium, high.
- `verticality_requirements`: none, balconies, pits, stairs, ledges, bridges, multi-level.

### Dungeon Features

- `traps`: trigger, telegraph, avoid path, combat relevance.
- `puzzles`: location, space requirements, player interaction points.
- `secret_rooms`: access method, reachable source room, clue placement.
- `ritual_chambers`: focal point, approach lanes, interruption positions.
- `treasure_vaults`: lock flow, guard flow, reward visibility.
- `environmental_hazards`: fire, acid, water, spores, rubble, falling, magical zones.
- `magical_systems`: portals, wards, rotating rooms, one-way doors, gravity shifts.
- `interactive_objects`: levers, statues, braziers, bookshelves, machinery, terrain controls.

## Adaptive Follow-Up Triggers

Ask these only when relevant:

- Huge or gargantuan creature: "Must that creature traverse corridors, or can it remain in a dedicated arena?"
- Boss encounter: "Should the boss arena support phases, lair actions, reinforcements, or terrain transformation?"
- Printable output: "Which paper size, square size in mm, margin in mm, and print DPI do you need?"
- VTT output: "Which VTT and pixels-per-square target should the map use?"
- Stealth focus: "Do you want alternate routes, hidden passages, line-of-sight blockers, or bypassable encounters?"
- Modular terrain: "Which terrain system and available module sizes should constrain rooms and corridors?"
- Ranged-heavy encounter: "Should there be long lanes, elevated positions, partial cover, or deliberate line-of-sight breaks?"
- Puzzle or ritual: "Does the interactive area need to remain usable during combat?"
- Secret rooms: "Should secrets be optional rewards, tactical flanks, or required progression?"

## Assumption Rules

If the user gives a high-level request and wants momentum, assume:

- Square grid, 5 ft per square.
- Medium party of 4 unless party size is given.
- Largest creature must fit only where it appears unless traversal is explicitly required.
- Generic VTT with 100 px per square if VTT output is requested without target details.
- Print maps use a 28 mm grid (25.4 mm for a true 1-inch grid), 6 mm margins, and 300 DPI unless the user specifies otherwise.

State assumptions before topology generation.
