---
name: dnd-map-architect
description: Use when designing a dungeon, cave, fortress, lair, encounter map, printable battlemap, VTT map, terrain-module layout, or image-generation prompt for tabletop RPG combat.
---

# DND Map Architect

Use this skill to create Dungeons & Dragons battlemaps that are playable first and attractive second. Never start with image generation. Always produce and validate a logical dungeon plan before writing or using an image prompt.

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

## Operating Rules

- Separate logic from visuals: topology and tactical layout are source of truth; art direction is downstream.
- Ask adaptive follow-up questions when missing information affects playability, scale, output format, or image generation.
- If the user gives enough constraints to proceed, state assumptions and continue.
- Reject invalid topology before prompt generation: disconnected rooms, trapped large creatures, broken corridors, non-integer grids, and impossible print scaling are blockers.
- Do not use prose-only dungeon plans as a bypass for validator-backed image prompt generation.
- Keep grid math exact: square maps require identical pixels per square on both axes; print maps require physical grid size and margin safety.
- Preserve gameplay usability over aesthetics: every combat space needs movement, cover logic, line-of-sight intent, and reachable objectives.
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

## Validator

Run the bundled validator on JSON specs from the project-local virtual environment when available:

```bash
.venv/bin/python skills/dnd-map-architect/scripts/validate_dungeon_spec.py skills/dnd-map-architect/examples/valid-dungeon-spec.json
```

If the skill is installed outside this repo, use the active environment's `python` with the same script path. Treat validator errors as blockers. Validator warnings require an explicit user-visible note or a spec adjustment. The validator provides deterministic checks; it does not replace tactical judgment or post-generation image review.
