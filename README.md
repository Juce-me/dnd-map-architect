# DND Map Architect

DND Map Architect is an agent skill for designing tactically playable, structurally valid Dungeons & Dragons battlemaps. It keeps map work grounded in a machine-validatable dungeon plan before any image prompt is written.

The skill is built for tabletop RPG map requests such as dungeons, caves, lairs, fortresses, encounter maps, printable battlemaps, VTT maps, and modular terrain layouts.

## What It Does

- Collects dungeon identity, tactical constraints, grid settings, print targets, VTT targets, and encounter requirements.
- Produces a JSON dungeon specification with rooms, corridors, encounters, grid dimensions, print settings, and assumptions.
- Plans topology before visuals, so room connectivity, secrets, locks, stairs, and traversal constraints are explicit.
- Validates deterministic map constraints with `skills/dnd-map-architect/scripts/validate_dungeon_spec.py`.
- Blocks image prompt generation when the logical map has structural, tactical, grid, or print errors.
- Generates image prompts only after validator-backed checks pass.
- Provides post-generation review and correction guidance so a pretty map is not accepted when it is unplayable.

The bundled validator has no third-party Python dependencies. It checks deterministic constraints such as reachability, room overlap, corridor attachment, creature traversal width, boss-room size, square-grid pixel math, hex metadata, and print split requirements. It does not replace human review of generated art, line of sight, visual grid drift, or overall encounter quality.

## Repository Layout

```text
skills/dnd-map-architect/
  SKILL.md                         Main skill instructions
  agents/openai.yaml               Codex UI metadata
  examples/valid-dungeon-spec.json Valid validator fixture
  examples/worked-output.md        Example output shape
  references/                      Intake, topology, tactical, print, prompt, and validation rules
  scripts/validate_dungeon_spec.py JSON spec validator
  tests/test_validate_dungeon_spec.py
```

## Install For Claude Code

Clone the repository, then symlink the skill into Claude Code's personal skills directory:

```bash
git clone git@github.com:Juce-me/dnd-map-architect.git
cd dnd-map-architect
mkdir -p ~/.claude/skills
ln -s "$PWD/skills/dnd-map-architect" ~/.claude/skills/dnd-map-architect
```

Restart Claude Code or start a fresh session so it reloads available skills.

Claude Code matches skills by their `description` field, so a plain natural-language request is enough — no special prefix needed:

```text
Design a tactically playable D&D battlemap for a 4-player level 6 party in a flooded crypt.
```

To invoke it explicitly instead, name the skill in the request:

```text
Use the dnd-map-architect skill to design a printable boss lair for a Huge construct.
```

## Install For Codex

Clone the repository, then symlink the skill into Codex's personal skills directory. Codex distributions differ on where personal skills live; install into whichever path your setup uses:

```bash
git clone git@github.com:Juce-me/dnd-map-architect.git
cd dnd-map-architect

# Most setups
mkdir -p ~/.agents/skills
ln -s "$PWD/skills/dnd-map-architect" ~/.agents/skills/dnd-map-architect

# Some setups use ~/.codex/skills instead
mkdir -p ~/.codex/skills
ln -s "$PWD/skills/dnd-map-architect" ~/.codex/skills/dnd-map-architect
```

Start a fresh Codex session after installing so the skill metadata is loaded.

In Codex, invoke the skill with its `$`-prefixed name:

```text
Use $dnd-map-architect to create a printable VTT-ready boss lair map.
```

## Usage Example

A typical session walks through six steps:

1. **Request.** "Design a printable battlemap for a 4-player level 6 party. Boss is a Huge construct. FoundryVTT target, US Letter print."
2. **Intake.** The skill confirms party size and level, encounter intent, grid type and scale, print and VTT targets, and any tactical constraints (cover, sightlines, chokepoints, stealth routes).
3. **JSON dungeon spec.** It produces a deterministic spec with rooms, corridors, encounters, grid metadata, print settings, and any unresolved assumptions called out explicitly.
4. **Validation.** It runs `scripts/validate_dungeon_spec.py` against the spec. Errors such as unreachable rooms, corridors too narrow for the boss, oversized rooms relative to the grid, or print-page math mistakes are fixed before continuing.
5. **Image prompt.** Only after validation returns `"ok": true` does the skill emit the image-generation prompt.
6. **Post-generation review.** It flags visual checks the validator cannot perform on its own, such as grid drift, line-of-sight regressions, and door alignment.

See [`skills/dnd-map-architect/examples/worked-output.md`](skills/dnd-map-architect/examples/worked-output.md) for a complete end-to-end example, including the JSON spec, topology graph, validator report, and final image prompt.

## Verify The Skill

From the repository root:

```bash
.venv/bin/python skills/dnd-map-architect/tests/test_validate_dungeon_spec.py
.venv/bin/python skills/dnd-map-architect/scripts/validate_dungeon_spec.py skills/dnd-map-architect/examples/valid-dungeon-spec.json
```

Expected result:

- The test suite passes.
- The bundled valid spec returns `"ok": true` with no errors or warnings.

If `.venv` does not exist, use your active Python 3 environment. The validator and tests use only the Python standard library.
