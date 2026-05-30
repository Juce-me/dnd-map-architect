# ChatGPT Battlemap Prompt — Sheet 1 (The Great Library of Nalrock, Levels 1–2)

Create a strict top-down orthographic D&D battlemap.

## Paper and Grid Scale (most important — fixes the printed size)

This map is sized to A3 paper at a 28 mm grid. The grid scale is derived from the page, not chosen arbitrarily:
- **Paper:** A3, 297 by 420 mm, **portrait orientation** (height 420 > width 297).
- **Physical grid:** 28 mm per square inside 6 mm margins.
- **Usable area:** (297 − 12) × (420 − 12) = 285 × 408 mm → floor(285/28) × floor(408/28) = **10 columns by 14 rows**.
- **Printed grid area:** 280 by 392 mm (10 × 28 mm by 14 × 28 mm), centered inside the usable area with a thin border.
- **Print resolution:** 300 DPI, so render 331 px per square (3310 by 4634 px) so each square measures exactly 28 mm on paper.

**Scale:** 10 ft per square (50 ft per 5-square area).  
**Output size:** 1000 by 1400 pixels, exactly 100 px per square (for digital/VTT use).

## Coordinate Grid (must be visible)

- Columns labeled 0–9 along the top edge.
- Rows labeled 0–13 along the left edge.
- Exactly 10 columns and 14 rows.
- Every grid square must be equal size.
- Dark grid lines must remain visible across the whole map, including door thresholds, archway openings, and corridor mouths.

Do not make a decorative border that changes the playable area. The numbered labels may sit outside or on the very edge, but the playable grid itself must remain exactly 10×14.

---

## Dungeon Identity

- **Type:** Dwarven library (abandoned, neglected, not ruined).
- **Atmosphere:** Quiet and still, cool underground air, dim magical lanterns (some flickering), dust on floors and shelves, preserved rather than destroyed.
- **Civilization:** Dwarven (original builders; currently abandoned for 2–3 years).
- **Gameplay Focus:** Combat (2 encounters) and exploration.

---

## Layout (Source of Truth)

### Rooms

1. **L1-Entrance (Enclosed Garden) — ISOLATED**  
   Position: (0, 0) — top, rows 0–5  
   Size: 10 wide × 6 tall  
   Role: Isolated, enclosed underground garden. **Dead-end** — its ONLY opening is a single door on its south wall into the Reception Hall. No exit to the surface, no other passages.  
   Features:
   - Enclosed underground garden beneath a very high vaulted stone ceiling (high ceilings do not affect grid).
   - Stone pathways and benches (non-tactical, descriptive; no movement impedance).
   - Hardy underground trees and shrubs as partial cover (scattered, allow movement through).
   - Dwarven statues (decorative, non-blocking, can provide light cover).
   - Dry fountain feature (non-tactical).
   - Overgrown but not wild (vegetation is sparse, does not fill squares).
   - Painted mountain murals on the enclosing walls.
   - **Connection:** Single door on the south wall to L2-Reception at columns 3–4, between rows 5 and 6. This is the garden's only way in or out.

2. **L2-Reception (Reception Hall) — MAIN ENTRANCE**  
   Position: (0, 6) — rows 6–13  
   Size: 10 wide × 8 tall  
   Role: The library's main entry hall. **The party enters here through the WEST entrance.**  
   Features:
   - **WEST ENTRANCE:** Large entrance doors on the WEST wall (column 0, around rows 9–10), opening from the city outside. This is the library's main door and the party's entry point. Show a 2-square-wide doorway/threshold here.
   - Grand dwarven architecture (high columns and archways).
   - Stone columns throughout (partial cover, non-blocking, scattered; each ~1 square).
   - Large reception desk and visitor counters (heavy cover, 2×2 footprint each, scattered throughout).
   - Records cabinets (heavy cover, scattered 1×2 clusters).
   - Benches (light cover, scattered).
   - Decorative murals and painted mountain windows on walls (non-tactical, descriptive).
   - Dust-covered documents scattered on desks (non-tactical, lore).
   - **Connections:**
     - West entrance door (column 0, rows 9–10) — from the city.
     - North door to the isolated Enclosed Garden at columns 3–4, between rows 5 and 6.
     - **SOUTH stairs down to Sheet 2** (Grand Reading Hall) at columns 3–4 on row 13 (bottom edge).

### Corridors / Openings

1. **Garden door** (c1-entrance-to-reception)  
   Connects: L2-Reception (north wall) to L1-Enclosed Garden (south wall) at columns 3–4, between rows 5 and 6.  
   Width: 2 squares.  
   Features: Single stone doorway; the garden's only access. Plain stone walls, dim lanterns, dust.

2. **West entrance** (main door from the city)  
   On the WEST wall of the Reception (column 0, rows 9–10). 2-square-wide threshold. Party's entry point onto the map.

3. **South stairs to Sheet 2**  
   On the SOUTH edge of the Reception (columns 3–4, row 13). Stairs descend to the Grand Reading Hall on Sheet 2.

---

## Tactical Requirements

**NOTE:** The following encounter descriptions are for the DM's reference only. **Do not render monsters, enemies, or NPCs on the battlemap itself.** The map should show only the interior layout and tactical cover. Players will place tokens on the map during play to represent characters and enemies.

### Encounter 1: Guard Drakes (Enclosed Garden — isolated, optional)
- **Enemy count:** 2 medium guard drakes.
- **Placement notes (DM reference):** Lairing in the isolated garden, among statues/flora. The garden is a dead-end side area off the Reception; this fight is optional unless the party opens the north door.
- **Behavior:** Territorial; attack on sight. Will not pursue out of the garden.
- **Tactical use of cover:** Light (benches, statues, fountain). Party can use vegetation and structures for movement and partial cover.
- **Sightlines:** Open garden, good visibility.
- **Objective:** Clear the garden if explored (lore/loot); otherwise bypassable.

### Encounter 2: Council Cultists (L2-Reception — main entry)
- **Enemy count:** 4 medium robed cultists.
- **Placement notes (DM reference):** Distributed around desks and cabinets near the west entrance; some use furniture for cover.
- **Behavior:** Hostile; defend the hall against intruders coming through the west door.
- **Tactical use of cover:** Moderate (desks, counters, cabinets provide heavy cover; columns provide partial cover).
- **Sightlines:** Columns and furniture create sight-line breaks and tactical positioning.
- **Objective:** Defeat cultists to reach the south stairs down to Level 3.

### Pacing
- Entry: Party comes in through the WEST entrance into the Reception.
- Reception combat: Main fight — cover and cultist positioning.
- Optional garden detour (north door): isolated drake lair.
- Exit: SOUTH stairs (row 13) descend to Level 3 (Sheet 2).

---

## Rendering Requirements

- **Top-down orthographic battlemap.** No perspective, no isometric view.
- **Interior only.** Show tactical layout, walls, doors, corridors, cover, and architectural features. **Do not render monsters, enemies, NPCs, or player characters on the map.** Players will place tokens for encounters during play.
- **Clear walkable spaces** (stone floors, pathways).
- **Distinct walls, doors, and corridors** visibly separated from combat areas.
- **Light cover** (benches, statues, vegetation) should be recognizable but not densely packed or blocking movement.
- **Heavy cover** (desks, counters, cabinets, columns) should be clearly positioned and leave token-playable space around them.
- **Decorative painted windows** (non-tactical, atmospheric): Scatter painted or frescoed windows along the walls of L1-Entrance and L2-Reception showing mountain vistas—painted murals depicting the peaks and valleys of Nalrock visible from above ground. These are artistic illusions on the stone walls, giving the sense of looking out to the surface world. **Do not block movement or grid squares.**
- **Playable grid squares** must remain readable; tokens must fit safely in intended combat spaces. Desks and cabinets should not fill entire squares—arrange in 2×1 or 1×2 clusters, leaving walkable spaces.
- **Hazards:** None in this sheet.
- **Stairs, doors, and archways:** Show clearly; grid must be continuous across thresholds and archway openings.
- **West entrance:** Render a clear 2-square-wide entrance doorway on the WEST wall of the Reception (column 0, rows 9–10) — the library's main door from the city.
- **South stairs down to Level 3:** Position at the SOUTH edge of the Reception (columns 3–4, row 13) to indicate the descent to Sheet 2.
- **Isolated garden:** The garden (rows 0–5) connects to the Reception by a single door on its south wall (columns 3–4, rows 5–6) and has no other openings.

---

## Negative Constraints (Do NOT)

- Do NOT use perspective view, isometric view, or 3D rendering.
- Do NOT warp, stretch, bend, or fade the grid. All squares must be identical size.
- Do NOT omit grid lines on any square, including door thresholds, archway interiors, corridor mouths, or dark void areas.
- Do NOT paint door art, ornamental tiles, or texture fills over grid lines.
- Do NOT create disconnected rooms or floating corridors.
- Do NOT add extra rooms, doors, walls, pits, or blocked paths beyond the topology specified.
- Do NOT place furniture or rubble so densely that tokens cannot stand in combat spaces.
- Do NOT hide doors, stairs, or entrances in visual noise.
- Do NOT crop the outer grid or use a decorative border that changes playable dimensions.
- Do NOT move or resize rooms. Room positions, sizes, and connections are fixed.
- Do NOT change the grid scale or square size.

---

## Post-Generation Validation Checklist

After ChatGPT generates the map:

1. **Count grid squares:** Confirm 10 wide × 14 tall.
2. **Confirm room positions and sizes:**
   - L1-Enclosed Garden: (0, 0), 10×6 ✓
   - L2-Reception: (0, 6), 10×8 ✓
3. **Confirm openings:** West entrance on Reception west wall (col 0, rows 9–10) ✓; garden door at cols 3–4 between rows 5–6 ✓; south stairs to Sheet 2 at cols 3–4, row 13 ✓
4. **Confirm garden is isolated:** Garden has exactly one opening (the south door to the Reception) and no other exits ✓
5. **Confirm cover placement:** Desks, cabinets, columns visible but not blocking movement ✓
6. **Confirm grid continuity:** Every square has visible grid lines, including door thresholds and archway interiors ✓
7. **Confirm encounter spaces:** Combat areas are token-playable ✓
8. **Confirm print validity:** A3 portrait, 28 mm grid, 6 mm margins → 10×14 squares (280×392 mm grid). When rendered at 331 px/sq for 300 DPI, each square measures 28 mm on paper ✓

---

**This is Sheet 1 of 2.** The party enters through the WEST door into the Reception Hall, clears it, and descends the SOUTH stairs (row 13) into Sheet 2 (Level 3 Grand Reading Hall and Level 4 Hidden Archive). The Enclosed Garden is an isolated optional detour off the Reception's north door.
