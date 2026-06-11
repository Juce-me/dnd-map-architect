Status: executed
Type: feature
Author: Juce

# Overview Maps: Zoom-Out Schemes With Accurate Scale

Add an overview (zoom-out) map mode to `skills/dnd-map-architect`: scheme maps of
dungeon complexes, settlements, regions, and continents that keep accurate,
chainable scale with the existing battlemap workflow.

## Goal

A user can ask for a zoom-out map at any of four scale levels and get the same
discipline as battlemaps: intake questions, a machine-validatable JSON spec, a
validator pass, and only then an image-generation prompt. Maps at different zoom
levels stay dimensionally consistent: a battlemap occupies a correctly sized,
correctly placed footprint on its parent overview, and so on up the chain.

## What Exactly Changes

### 1. Scale ladder (core concept)

| Level | Name | Unit per grid cell | Default grid |
|---|---|---|---|
| 0 | `battlemap` (existing flow) | 5 ft per square (`tile_scale_ft`) | square |
| 1 | `site` (dungeon/building overview) | 10–50 ft per square | square |
| 2 | `settlement` (village/town/city) | 50–500 ft per square | square |
| 3 | `region` (province/wilderness) | 1–10 miles per hex | hex (square allowed) |
| 4 | `world` (continent) | 25–100 miles per hex | hex (square allowed) |

- Units: feet for levels 0–2, miles for levels 3–4. 1 mile = 5280 ft.
- Hex grids reuse the existing conventions from `validate_dungeon_spec.py`:
  orientation `pointy`/`flat`, coordinate system `axial`/`offset`.

### 2. Scale chain (parent/child linkage)

An overview spec may declare `children`: maps of any strictly lower level placed
on it. Each child declares a real-world footprint (width × height in ft or
miles) and either:

- `representation: "block"` — occupies `ceil(footprint / unit_per_cell)` cells
  per axis at a declared grid position; required when the footprint spans ≥ 1
  parent cell on either axis.
- `representation: "marker"` — a labeled point of interest at one cell; required
  when the footprint is smaller than 1 parent cell on both axes.

If a child entry includes `spec_path` (relative to the overview spec file), the
validator loads that spec and cross-checks the declared footprint against the
child's own grid math (battlemap: `width_squares × tile_scale_ft`; overview:
`width_cells × unit_per_cell`), converting ft/miles as needed. Mismatch,
out-of-bounds placement, wrong block size, or a child level ≥ parent level are
blocking errors.

Worked example (uses the bundled battlemap example): Ember Archive is 24 × 18
squares at 5 ft = 120 × 90 ft. On a `site` overview at 10 ft per square it is a
12 × 9 block. On a `region` map at 1 mile per hex it is a marker (120 ft ≪ 1
mile).

### 3. New reference files under `skills/dnd-map-architect/references/`

- `overview-rules.md` — shared rules for all overview scales:
  - The scale ladder and chain/representation rules above.
  - Scale bar: required on every overview map; spans a whole number of grid
    cells; label must equal `length_cells × unit_per_cell` (e.g. 5 squares =
    50 ft, or 5 hexes = 30 miles). On print maps the bar must measure true on
    paper (cells × physical cell mm).
  - Print math: squares reuse the `print-rules.md` formulas. Hexes get explicit
    paper-fit formulas (pointy-top, offset rows, flat-to-flat cell width `w`,
    corner height `h = 2w/√3`): `columns_max = floor((usable_w − 0.5w) / w)`,
    `rows_max = floor((usable_h − 0.25h) / 0.75h)`; flat-top swaps axes.
    Default physical cell 28 mm, 6 mm margins, 300 DPI, consistent with
    `print-rules.md`.
  - Schematic discipline: overview maps show blocks, routes, markers, labels,
    and terrain — never furniture, tokens, creatures, or tactical detail.
  - Numbered coordinate grid leads every prompt (per project learning), grid
    lines drawn above all art.
- `overview-site.md`, `overview-settlement.md`, `overview-region.md`,
  `overview-world.md` — one per scale, each containing:
  - Scale-specific intake questions (the "what else goes into the prompt"
    set). Site: floors/levels shown, wings/zones, entrances, child battlemaps,
    DM vs player version (secrets shown or hidden). Settlement: districts,
    walls/gates, water, roads, landmarks, callout buildings, size class.
    Region: terrain mix, settlements, roads/rivers, political borders,
    dungeon/site markers, travel-time annotations. World: kingdoms, coastlines,
    mountain ranges, climate bands, capitals, sea routes, label hierarchy.
  - Spec fields specific to the scale.
  - An image-prompt template following the battlemap template skeleton:
    numbered coordinate grid first, paper/scale block, layout as source of
    truth, scale bar requirement, rendering requirements.
  - Adapted negative constraints (no monsters/armies/people rendered, no
    perspective, no missing or faded grid cells, no decorative border changing
    the mapped area).
  - A post-generation review checklist (grid count, scale bar measures true,
    child footprints at declared positions, labels legible at print size).

### 4. New validator and tests

- `skills/dnd-map-architect/scripts/validate_overview_spec.py` — standalone,
  same report shape as the existing validator (`{ok, errors, warnings}`, error
  codes like `SCALE_LEVEL_INVALID`, `CHAIN_FOOTPRINT_MISMATCH`,
  `CHAIN_CHILD_SPEC_MISSING`, `SCALE_BAR_MISMATCH`, `PRINT_REQUIRES_SPLIT`).
  Checks: scale level/unit range/unit kind, grid validity (hex orientation and
  coordinate system required for hex), integer pixels per cell on both axes,
  feature and child bounds, representation rule, child spec cross-check, scale
  bar math, print fit (square and hex formulas), underfill warning.
- `skills/dnd-map-architect/tests/test_validate_overview_spec.py` — mirrors the
  existing test structure (importlib loading, unittest, valid-spec fixture plus
  per-error-code cases).
- `skills/dnd-map-architect/examples/valid-overview-spec.json` — a `site`-level
  overview chained via `spec_path` to `examples/valid-dungeon-spec.json` using
  the 12 × 9 block math above.

### 5. SKILL.md and packaging updates

- Frontmatter `description` gains trigger wording: dungeon overview, city or
  settlement map, region map, world/overworld map, zoom-out scheme.
- New "Map Modes" routing rule: battlemap/encounter requests use the existing
  workflow; overview requests read `references/overview-rules.md` plus exactly
  one matching scale file.
- Overview workflow: intake → JSON overview spec → composition pass (features +
  scale chain) → validation via `validate_overview_spec.py` → image prompt or
  blocker corrections → post-generation review → correction loop.
- Reference Map and Validator sections list the new files and command.
- `agents/openai.yaml` `short_description` mentions overview maps.
- Root `AGENTS.md` section 10 gains the new test and validate commands
  (`CLAUDE.md`/`GEMINI.md` are symlinks; no separate edit).

## Forbidden Regressions

- Existing battlemap workflow, references, validator, example spec, and tests
  are unchanged except for the SKILL.md additions listed above.
- `validate_dungeon_spec.py` output for `examples/valid-dungeon-spec.json` is
  unchanged.
- Existing test suite passes unmodified.

## Files Allowed To Touch

- `skills/dnd-map-architect/SKILL.md`
- `skills/dnd-map-architect/references/overview-rules.md` (new)
- `skills/dnd-map-architect/references/overview-site.md` (new)
- `skills/dnd-map-architect/references/overview-settlement.md` (new)
- `skills/dnd-map-architect/references/overview-region.md` (new)
- `skills/dnd-map-architect/references/overview-world.md` (new)
- `skills/dnd-map-architect/scripts/validate_overview_spec.py` (new)
- `skills/dnd-map-architect/tests/test_validate_overview_spec.py` (new)
- `skills/dnd-map-architect/examples/valid-overview-spec.json` (new)
- `skills/dnd-map-architect/agents/openai.yaml`
- `AGENTS.md` (section 10 commands only)
- `docs/agents/features/` (this artifact and the implementation plan)

## Expected Behavior

- "Give me a map of the whole dungeon" → site-level intake questions, spec,
  validation, then a prompt that renders a labeled scheme at e.g. 10 ft/square
  with a scale bar, chained to any existing battlemap specs.
- "Map the city around it" → settlement-level flow; the dungeon site appears as
  a correctly sized block or marker.
- Validation failures produce blocker corrections instead of an image prompt,
  exactly as the battlemap flow does.
- Printed overviews on A3 at 28 mm cells keep a measurable scale bar.

## Acceptance Criteria

1. `.venv/bin/python skills/dnd-map-architect/scripts/validate_overview_spec.py
   skills/dnd-map-architect/examples/valid-overview-spec.json` exits 0 with no
   errors, and the example chains to `valid-dungeon-spec.json` via `spec_path`.
2. Violations (bad level, wrong unit, footprint mismatch, missing child spec,
   bad scale bar, print overflow without split, non-integer pixels per cell,
   missing hex orientation) each produce their distinct blocking error code,
   covered by tests.
3. `.venv/bin/python skills/dnd-map-architect/tests/test_validate_overview_spec.py`
   and the existing `tests/test_validate_dungeon_spec.py` both pass.
4. `py_compile` passes on both scripts and both test files.
5. SKILL.md routes overview requests to `overview-rules.md` plus exactly one
   scale reference; each scale file contains intake questions, a prompt
   template, negative constraints, and a post-generation checklist.

## Implementation Notes

Execute via subagent-driven development (per user request): one subagent per
scale reference file working from the committed `overview-rules.md`, one for
the validator + tests (TDD), then an integration review. The implementation
plan will be a sibling artifact in this folder.

## Outcome

Implemented with changes. The test suite grew from the planned 35 to 38 tests:
a post-review commit added coverage for the flat-top hex print-fit axis swap,
marker out-of-bounds placement, and duplicate child ids. Two template
placeholders are intentionally outside the validated spec shape: `{dpi}` falls
back to the 300 DPI default in `overview-rules.md`, and `{atmosphere}` in
`overview-site.md` is filled from conversation context (the validator ignores
extra identity fields). Everything else shipped as planned.

Doc Review Criteria checked for SKILL.md, AGENTS.md section 10, and the five
new reference files: terminology is consistent (cell, scale ladder,
block/marker, scale bar used uniformly), documented commands and examples were
run and pass, primary flows (battlemap mode vs overview mode) are described
end-to-end, and no secrets, machine paths, or personal data appear. Backend/API
and security/privacy dimensions are not applicable to these docs.

## Current Accuracy

Accurate as of execution. The shipped code, references, and tests are the
source of truth; see `EXECUTED-overview-maps-plan.md` for the task-level record.
