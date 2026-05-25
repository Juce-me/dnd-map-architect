# Topology Engine

Generate dungeon logic before spatial layout. The topology is the source of truth for room existence, connectivity, locks, secrets, encounter pacing, and traversal constraints.

## Topology Pass

1. Define required rooms from narrative and tactical roles.
2. Assign each room a role: entry, transition, combat, exploration, puzzle, hazard, rest, secret, treasure, mini-boss, boss, exit.
3. Create a connected graph from entrance to primary objective.
4. Add optional branches only when they have a gameplay reason: scouting, reward, bypass, flank, risk, lore, shortcut.
5. Add locks and keys as graph constraints, not visual decoration.
6. Add stairs, portals, bridges, or one-way links as explicit edge types.
7. Mark secret rooms with `accessible_from` and clue source.
8. Check pacing: entry pressure, discovery, escalation, set-piece, reveal, finale, exit.

## Room Node Contract

```json
{
  "id": "vault",
  "name": "Forge Vault",
  "type": "boss",
  "x": 7,
  "y": 10,
  "width": 12,
  "height": 7,
  "secret": false,
  "notes": ["main objective", "ritual focus"]
}
```

Coordinates use grid squares. `x` and `y` describe the upper-left grid coordinate. Width and height are measured in full grid squares.

## Edge Contract

```json
{
  "id": "c2",
  "connects": ["stacks", "vault"],
  "width_squares": 3,
  "path": [[13, 7], [13, 10]],
  "edge_type": "corridor",
  "door_type": "stone double door"
}
```

Use orthogonal path segments for square grids. Hex maps may use axial or offset coordinates, but state the coordinate system explicitly.

## Graph Rules

- Every non-secret room must be reachable from an entrance.
- Every secret room must be reachable through a declared secret door, hidden passage, teleport, crawlspace, or puzzle.
- Room IDs, corridor IDs, and corridor endpoint IDs must be non-empty strings.
- Corridors connect rooms; they must not float without endpoints.
- Room footprints must not overlap.
- Doors must sit on a room boundary and connect to a corridor or adjacent room.
- Stairs, ladders, shafts, and portals must have source and destination nodes.
- Boss arenas and large-monster chambers must not depend on corridors that the creature cannot traverse unless the boss is intentionally static.

## Narrative Flow Patterns

- **Linear pressure**: entry -> skirmish -> puzzle/hazard -> mini-boss -> boss.
- **Looped infiltration**: entry -> fork -> stealth route and main route -> convergence -> objective -> shortcut exit.
- **Keyed fortress**: entry -> guard ring -> key objective -> locked inner chamber -> finale.
- **Ritual escalation**: omen -> cult workroom -> sacrifice prep -> ritual chamber -> unstable exit.
- **Lair with territory**: outer signs -> patrol paths -> den hazards -> nest/hoard -> escape pressure.

Prefer one clear primary path plus meaningful optional loops over random branching.
