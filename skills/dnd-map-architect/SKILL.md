---
name: dnd-map-architect
description: Use when designing a dungeon, cave, fortress, lair, encounter map, printable battlemap, VTT map, terrain-module layout, overview or zoom-out map of a dungeon complex, city, settlement, region, or world, or an image-generation prompt for tabletop RPG maps.
---

# DND Map Architect

Use this skill to create Dungeons & Dragons battlemaps that are playable first and attractive second. Never start with image generation. Always produce and validate a logical dungeon plan before writing or using an image prompt.

## Map Modes

- **Battlemap mode** (tactical encounter maps): follow the Required Workflow below.
- **Overview mode** (zoom-out schemes: whole dungeon or site, settlement, region, world): read `references/overview-rules.md` plus exactly one scale file (`overview-site.md`, `overview-settlement.md`, `overview-region.md`, `overview-world.md`), then follow the Overview Workflow.

## Required Workflow

1. **Dungeon intake**: Collect identity, technical constraints, tactical constraints, and dungeon features. Read `references/intake-schema.md`.
2. **JSON dungeon specification**: Convert intake into a deterministic JSON spec with rooms, corridors, encounters, grid settings, print/VTT targets, and unresolved assumptions.
3. **Topology generation**: Build a connected room graph before spatial layout. Read `references/topology-engine.md`.
4. **Tactical layout pass**: Size rooms, corridors, cover, sightlines, chokepoints, stealth routes, and boss traversal. Read `references/tactical-rules.md`.
5. **Validation pass**: Validate structure, tactics, grid, and print/VTT constraints. Read `references/validation-rules.md`; also read `references/print-rules.md` when print, VTT, or modular terrain output matters. Run `scripts/validate_dungeon_spec.py` against the JSON spec before image prompting.
6. **Image prompt generation**: Generate map prompts only after validator-backed validation has no blocking errors. If validation has blockers, output blocker corrections instead of an image prompt. Read `references/prompt-templates.md`.
7. **Image generation**: Use the active image tool only after the user approves or requests generation.
8. **Post-generation validation**: Review the generated map against topology, grid, tactical, and print constraints. Do not accept a pretty but unplayable result.
9. **Correction loop**: Produce targeted correction prompts and updated validation notes until the map is usable.

## Overview Workflow

1. **Overview intake**: Pick the scale level from the ladder in `references/overview-rules.md`; ask the scale file's intake questions.
2. **JSON overview specification**: Build a spec matching the shape in `references/overview-rules.md`: scale, grid, scale bar, print target, features, and children with real-world footprints.
3. **Composition pass**: Place features and child blocks or markers; verify the scale chain math (block = ceil of footprint / unit_per_cell, marker when smaller than one cell).
4. **Validation pass**: Run `scripts/validate_overview_spec.py` against the spec. Treat errors as blockers, exactly as in battlemap mode.
5. **Image prompt generation**: Use the scale file's prompt template only when validation passes; otherwise output blocker corrections.
6. **Image generation, post-generation validation, correction loop**: Follow battlemap mode steps 7-9 using the scale file's post-generation checklist.

## Operating Rules

- Separate logic from visuals: topology and tactical layout are source of truth; art direction is downstream.
- Ask adaptive follow-up questions when missing information affects playability, scale, output format, or image generation.
- If the user gives enough constraints to proceed, state assumptions and continue.
- Reject invalid topology before prompt generation: disconnected rooms, trapped large creatures, broken corridors, non-integer grids, and impossible print scaling are blockers.
- Do not use prose-only dungeon plans as a bypass for validator-backed image prompt generation.
- Keep grid math exact: square maps require identical pixels per square on both axes; print maps work in millimeters and require physical grid size, margins, DPI, and a grid sized to fit the chosen paper.
- Preserve gameplay usability over aesthetics: every combat space needs movement, cover logic, line-of-sight intent, and reachable objectives.
- Treat tactical objects as grid-scale pieces: furniture, columns, walls, stairs, cover, and obstacles must occupy whole grid-square footprints, with a minimum footprint of 1 square.
- Never let terrain erase scale squares: grid lines must remain visible over and through every occupied footprint, including fountains, columns, tables, counters, stairs, and walls.
- Output correction recommendations as concrete changes, not vague style notes.

## Required Outputs

Produce these artifacts for each full map request:

1. **JSON dungeon specification**: Machine-validatable spec plus a short summary of identity, constraints, and assumptions.
2. **Room topology graph**: Nodes, links, locks, secret paths, stairs, and traversal constraints.
3. **Encounter placement plan**: Encounter role, enemy sizes, terrain role, objectives, and pacing.
4. **Tactical notes**: Movement, cover, sightlines, stealth routes, chokepoints, hazards, verticality.
5. **Image generation prompt or blocker corrections**: Positive prompt plus negative constraints only when validation passes; otherwise list the corrections needed before prompting.
6. **Validation report**: Blocking errors, warnings, and checked layers.
7. **Correction recommendations**: Ordered fixes for topology, tactics, grid, print/VTT, or prompt issues.

## Reference Map

- `references/intake-schema.md`: Required and adaptive intake fields.
- `references/topology-engine.md`: Graph-first dungeon planning and topology output format.
- `references/tactical-rules.md`: Creature size, movement, combat, stealth, cover, and encounter rules.
- `references/validation-rules.md`: Structural, tactical, grid, print, VTT, and post-generation validation.
- `references/print-rules.md`: Print, VTT, and modular terrain compatibility rules.
- `references/prompt-templates.md`: Prompt templates and correction prompt patterns.
- `examples/valid-dungeon-spec.json`: Valid JSON spec accepted by the bundled validator.
- `examples/worked-output.md`: Example complete artifact set.
- `references/overview-rules.md`: Scale ladder, scale chain, scale bar, and print math shared by all overview maps.
- `references/overview-site.md`: Site (dungeon complex) overview intake and prompts.
- `references/overview-settlement.md`: Settlement overview intake and prompts.
- `references/overview-region.md`: Region hex-map intake and prompts.
- `references/overview-world.md`: World atlas intake and prompts.
- `examples/valid-overview-spec.json`: Valid overview spec accepted by the bundled overview validator.

## Validator

Run the bundled validator on JSON specs from the project-local virtual environment when available:

```bash
.venv/bin/python skills/dnd-map-architect/scripts/validate_dungeon_spec.py skills/dnd-map-architect/examples/valid-dungeon-spec.json
```

For overview (zoom-out) specs, run the overview validator the same way:

```bash
.venv/bin/python skills/dnd-map-architect/scripts/validate_overview_spec.py skills/dnd-map-architect/examples/valid-overview-spec.json
```

If the skill is installed outside this repo, use the active environment's `python` with the same script path. Treat validator errors as blockers. Validator warnings require an explicit user-visible note or a spec adjustment. The validator provides deterministic checks; it does not replace tactical judgment or post-generation image review.
