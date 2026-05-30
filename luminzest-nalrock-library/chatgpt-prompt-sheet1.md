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

1. **L1-Entrance (Entrance Garden)**  
   Position: (0, 0) — top-left corner  
   Size: 10 wide × 6 tall  
   Features:
   - Enclosed underground garden beneath a very high vaulted stone ceiling (high ceilings do not affect grid).
   - Stone pathways and benches (non-tactical, descriptive; no movement impedance).
   - Hardy underground trees and shrubs as partial cover (scattered, allow movement through).
   - Dwarven statues (decorative, non-blocking, can provide light cover).
   - Dry fountain feature (non-tactical).
   - Overgrown but not wild (vegetation is sparse, does not fill squares).
   - **Encounter:** 2 guard drakes (Medium size), scattered throughout, defending the entrance. Drakes are hostile on sight but do not pursue beyond this room.
   - **Connection:** Corridor to L2-Reception at (3, 5)–(3, 6).

2. **L2-Reception (Reception Hall)**  
   Position: (0, 6) — center-bottom  
   Size: 10 wide × 8 tall  
   Features:
   - Grand dwarven architecture (high columns and archways).
   - Stone columns throughout (partial cover, non-blocking, scattered; each ~1 square).
   - Large reception desk and visitor counters (heavy cover, 2×2 footprint each, scattered throughout).
   - Records cabinets (heavy cover, scattered 1×2 clusters).
   - Benches (light cover, scattered).
   - Decorative murals on walls (non-tactical, descriptive).
   - Dust-covered documents scattered on desks (non-tactical, lore).
   - **Encounter:** 4 council cultists in red robes (Medium size, lightly armored), scattered behind desks and cabinets. Hostile to party. Defend the inner library entrance.
   - **Connections:** Corridor back to L1-Entrance at (3, 6)–(3, 5); corridor north to L3-Reading at (3, 13)–(3, 14).

### Corridors

1. **Corridor L1→L2** (c1-entrance-to-reception)  
   Connects: L1-Entrance (3, 6) to L2-Reception (3, 6).  
   Width: 2 squares.  
   Features: Plain stone walls, dim magical lanterns, dust.

---

## Tactical Requirements

**NOTE:** The following encounter descriptions are for the DM's reference only. **Do not render monsters, enemies, or NPCs on the battlemap itself.** The map should show only the interior layout and tactical cover. Players will place tokens on the map during play to represent characters and enemies.

### Encounter 1: Guard Drakes (L1-Entrance)
- **Enemy count:** 2 medium guard drakes.
- **Placement notes (DM reference):** Scattered throughout the garden, near entrance doors and among statues/flora.
- **Behavior:** Territorial; attack on sight. Will not pursue into Reception Hall.
- **Tactical use of cover:** Light (benches, statues, fountain). Party can use vegetation and structures for movement and partial cover.
- **Sightlines:** Open garden, good visibility.
- **Objective:** Defeat drakes or pass through to corridors.

### Encounter 2: Council Cultists (L2-Reception)
- **Enemy count:** 4 medium robed cultists.
- **Placement notes (DM reference):** Distributed around desks and cabinets; some use furniture for cover.
- **Behavior:** Hostile; defend the hall and north passage.
- **Tactical use of cover:** Moderate (desks, counters, cabinets provide heavy cover; columns provide partial cover).
- **Sightlines:** Columns and furniture create sight-line breaks and tactical positioning.
- **Objective:** Defeat cultists to proceed north into Level 3.

### Pacing
- Entrance combat: Immediate threat.
- Reception combat: Mid-complexity encounter with cover and cultist positioning.
- Exit through north corridor leads to Level 3 (Sheet 2).

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
- **Stairs down to Level 3:** Position at north exit (3, 13–14) to indicate vertical transition.

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
   - L1-Entrance: (0, 0), 10×6 ✓
   - L2-Reception: (0, 6), 10×8 ✓
3. **Confirm corridors:** C1 at (3, 5)–(3, 6), width 2 ✓; north exit at (3, 13)–(3, 14) ✓
4. **Confirm cover placement:** Desks, cabinets, columns visible but not blocking movement ✓
5. **Confirm grid continuity:** Every square has visible grid lines, including door thresholds and archway interiors ✓
6. **Confirm encounter spaces:** Combat areas are token-playable ✓
7. **Confirm print validity:** A3 portrait, 28 mm grid, 6 mm margins → 10×14 squares (280×392 mm grid). When rendered at 331 px/sq for 300 DPI, each square measures 28 mm on paper ✓

---

**This is Sheet 1 of 2.** After the party defeats the cultists in L2-Reception, they proceed north through the stairs into Sheet 2 (Level 3 Grand Reading Hall and Level 4 Hidden Archive).
