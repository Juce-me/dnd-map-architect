# Worked Output

## JSON Dungeon Specification

Ember Archive is a ruined dwarven library built for a 4-player level 6 party. It uses a 24 x 18 square grid, 5 ft per square, 2400 x 1800 px output, FoundryVTT target, and printable Letter output at 28 mm per square (6 mm margins) split across pages.

The validator input is `examples/valid-dungeon-spec.json`.

## Room Topology Graph

```text
entry --c1--> stacks --c2--> vault
```

- `entry`: safe arrival, burned doors, first clue.
- `stacks`: skirmish room with shelving cover and broken sightlines.
- `vault`: huge boss arena with forge dais and ritual objective.

## Encounter Placement Plan

- `stacks`: medium cultists and one large construct enter from the far shelves; party enters from the west; cover is partial and does not block all movement.
- `vault`: huge ember guardian starts near the dais; party enters from north; objective can be reached without moving through the guardian footprint.

## Tactical Notes

- Corridors are 3 squares wide because the huge guardian may move between rooms.
- The boss arena is 12 x 7, meeting the minimum 7 x 7 huge boss rule.
- Shelves provide cover without removing all alternate movement lanes.

## Validation Report

```json
{
  "ok": true,
  "errors": [],
  "warnings": []
}
```

## Image Generation Prompt

```text
Create a top-down Dungeons & Dragons battlemap with an exact square grid.

Map size: 24 by 18 squares.
Scale: 5 ft per square.
Output size: 2400 by 1800 px, exactly 100 px per square.
Print target (Letter, split pages):
- Paper: Letter, 215.9 by 279.4 mm, landscape.
- Physical grid: 28 mm per square inside 6 mm margins.
- Printed map area: 672 by 504 mm, tiled across multiple Letter sheets with cut and assembly labels.
- Print resolution: 300 DPI, so the print export is 331 px per square (7944 by 5958 px); the 2400 by 1800 px output above is the FoundryVTT export at 100 px per square.
Grid: straight, evenly spaced, non-distorted, aligned edge to edge.

Dungeon identity:
- Type: dwarven library.
- Architecture: ruined cut stone archive with burned stacks and forge-vault masonry.
- Atmosphere: ember-lit, soot-stained, readable tactical terrain.

Layout source of truth:
- entry: Entry Hall at x1 y1, 6 by 5 squares.
- stacks: Burned Stacks at x9 y1, 8 by 6 squares.
- vault: Forge Vault at x7 y10, 12 by 7 squares.
- c1: 3-square-wide corridor from entry to stacks, path [7,3] to [9,3].
- c2: 3-square-wide corridor from stacks to vault, path [13,7] to [13,10].

Tactical requirements:
- stacks is a skirmish room with shelving cover and broken sightlines.
- vault is a huge boss arena with a forge dais and reachable ritual objective.
- Corridors remain 3 squares wide for huge creature traversal.

Negative constraints:
Do not use perspective view. Do not warp, stretch, bend, or fade the grid.
Do not create disconnected rooms or floating corridors. Do not add extra rooms, doors, walls, pits, or blocked paths that contradict the topology.
Do not place furniture or rubble so densely that tokens cannot stand in intended combat spaces. Do not crop the outer grid.
```

## Correction Recommendations

No correction required for the logical spec. Generated images must still be checked for grid distortion, room count, corridor width, and token-playable boss space.
