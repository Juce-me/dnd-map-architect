# ChatGPT Battlemap Prompt — Sheet 2 (The Great Library of Nalrock, Levels 3–4)

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
- Dark grid lines must remain visible across the whole map, including door thresholds, archway openings, staircase landings, and corridor mouths.

Do not make a decorative border that changes the playable area. The numbered labels may sit outside or on the very edge, but the playable grid itself must remain exactly 10×14.

---

## Dungeon Identity

- **Type:** Dwarven library vault (secret, untouched, preserved knowledge).
- **Atmosphere:** Vast shelves, hidden secrets, magical aura around vault, very high ceilings (narrative only; does not affect tactical grid), dust in hidden areas.
- **Civilization:** Dwarven (original builders; vault remains locked away from abandonment above).
- **Gameplay Focus:** Exploration (with puzzle discovery), hazard navigation, and boss combat.

---

## Layout (Source of Truth)

### Rooms

**Keep this map SIMPLE and large-scale. Get the three room dimensions and the grid right first; use few, clearly-placed objects with lots of open floor. Do not clutter the rooms.**

1. **L3-Reading (Grand Reading Hall) — ENTRY FROM RECEPTION (NORTH)**  
   Position: (0, 0) — top, rows 0–5  
   Size: 10 wide × 6 tall  
   Role: The party arrives here from the Reception Hall (Sheet 1, which stacks directly above). **The connection to the Reception is at the NORTH edge (top), not the south.**  
   Features (sparse — mostly open floor):
   - **NORTH ENTRY — main doorway from the Reception (Sheet 1):** Cut a clear 2-square-wide ARCHWAY DOORWAY through the NORTH wall at columns 3–4, row 0 (top edge). Open stone gateway with a visible floor threshold on squares (3,0) and (4,0), opening to black/empty space beyond the top wall. A few stone steps just inside. **This doorway is the ONLY opening in the north wall**; the rest of the top wall is solid stone. Do NOT draw stairs running off the top edge — draw a gateway set INTO the wall.
   - A row of tall bookshelves along the EAST and WEST walls only (left and right edges). Leave the middle of the room open.
   - 2–3 large reading tables in the open floor (light cover).
   - 2 stone columns (around (2,3) and (7,3)), 1 square each.
   - Keep squares (3,0) and (4,0) clear so the north doorway is not blocked.
   - **Connection to Hazard:** Corridor SOUTH at columns 3–4, between rows 5 and 6 (bottom edge).
   - *DM note (do NOT draw):* one east-wall statue is the secret-passage hint; the passage itself is hidden and is NOT rendered on the map.

2. **L3-L4-Hazard (Hazardous Transition)**  
   Position: (0, 6) — center, rows 6–8  
   Size: 10 wide × 3 tall  
   Features (sparse):
   - Collapsed, cracked stone floor across most of the band — the defining feature. Broken, uneven tiles; a few loose rocks. No furniture, no clutter beyond rubble.
   - **Connection to Reading:** Corridor NORTH at columns 3–4, between rows 5 and 6.
   - **Connection to Archive:** Stairs SOUTH at columns 3–4, between rows 8 and 9.
   - *DM note:* difficult terrain (DC 10 Acrobatics) + occasional falling debris (DC 12 Dex, 1d6). Telegraph with visible cracks; no need for extra detail.

3. **L4-Archive (Hidden Archive Vault)**  
   Position: (0, 9) — bottom, rows 9–13  
   Size: 10 wide × 5 tall  
   Features (sparse — open vault chamber):
   - Reinforced stone vault; faint glowing runes along the walls (atmosphere only).
   - A few low shelves against the EAST and WEST walls. Otherwise open floor.
   - **Puzzle Chamber:** Four stone pedestals in a tight 2×2 cluster, occupying roughly the single square at (4, 11). This is the puzzle (DM-run). Render four short pillars; keep them compact.
   - **Connection to Hazard:** Stairs NORTH at columns 3–4, between rows 8 and 9.
   - **SOUTH/bottom wall (row 13) is SEALED** — one continuous carved stone wall with a central dwarven seal medallion. No doorway, no stairs, no gap.
   - *DM note (do NOT draw):* a dormant construct guardian and the vault contents live here; do not render them.

### Corridors / Openings (only these — no others)

1. **North entry doorway** — archway through the north wall at columns 3–4, row 0. Party's entry from the Reception.
2. **Reading → Hazard** — corridor at columns 3–4, between rows 5 and 6. Width 2–3 squares.
3. **Hazard → Archive** — stone staircase at columns 3–4, between rows 8 and 9. Width 2 squares.

**The secret passage (odd statue → vault) is NOT drawn on the map. Do not render any hidden tunnel, faint passage, or side opening.**
---

## Tactical Requirements

**NOTE:** The following tactical descriptions are for the DM's reference only. **Do not render monsters, enemies, or NPCs on the battlemap itself.** The map should show only the interior layout and tactical cover. Players will place tokens on the map during play to represent characters and enemies.

### Exploration: L3-Reading Hall
- **Objective:** Explore the hall; find the hidden way down.
- **Key Feature (DM-only):** One east-wall statue is the secret-passage hint. **Neither the statue-as-trigger nor the passage is drawn on the map** — the DM narrates it. Finding it requires investigation / Perception (DC 13). The passage bypasses the hazard.
- **Cover:** Wall bookshelves and the few tables provide cover.
- **Sightlines:** Open central floor with a couple of columns.

### Hazard: L3-L4 Transition
- **Objective:** Navigate treacherous passage to reach vault.
- **Difficult Terrain:** Central 5×5 area (cracked floor). Movement through at half speed; DC 10 Acrobatics to cross at normal speed. **Render this visibly on the map.**
- **Falling Debris:** Random hazard (1 in 6 per round). DC 12 Dex save or 1d6 damage. Visually telegraph with visible cracks, loose stones, and precarious ceiling supports. **Render this as cracked floor and unstable stonework on the map.**
- **Stealth:** Parties moving carefully can minimize hazard triggers (DM discretion).
- **Combat:** Unlikely unless party lingers; designed as a gauntlet/endurance challenge.

### Encounter: Construct Guardian (L4-Archive)
- **Enemy (DM reference):** 1 construct guardian (stone golem, CR 5, ~70 HP, high AC, low mobility). **Do not render the construct on the map—only the vault space where it awakens.**
- **Placement (DM reference):** Dormant near vault entrance (position (2, 10) approximately).
- **Trigger:** Incorrect puzzle solution awakens the construct.
- **Behavior:** Attack intruders until destroyed OR puzzle is solved correctly (which halts combat without destroying the construct).
- **Arena:** Vault chamber (10 wide × 5 tall) provides space for movement and positioning. Puzzle occupies (4, 11), leaving flanking and movement opportunities.
- **Difficulty:** Hard for a 5th-level party of 5 PCs. Stone golems are resistant to magic, relying on physical damage.
- **Victory:** Defeat construct or solve puzzle correctly.

### Puzzle: Four Books Logic Riddle
- **Location:** L4-Archive, (4, 11) — single tactical square representing four pedestals.
- **Mechanics (DM-controlled):** Party discovers or recalls four books (provided by DM). Books represent different historical/magical concepts. A riddle or logic puzzle determines the correct placement order on pedestals.
- **Example riddle theme:** "Order the books by the founding of Nalrock: geology (origin), military history (expansion), trade agreements (prosperity), arcane research (downfall)."
- **Correct Solution:** Vault unseals peacefully; party gains access to quest objective.
- **Incorrect Solution:** Construct awakens; party must defeat it or restart the puzzle (if possible).
- **Rendering:** Show four stone pedestals clustered at (4, 11), or mark as a single "puzzle chamber" square clearly visible and labeled.

---

## Rendering Requirements

- **Top-down orthographic battlemap.** No perspective, no isometric view.
- **Interior only.** Show tactical layout, walls, stairs, corridors, cover, and architectural features. **Do not render monsters, enemies, NPCs, or player characters on the map.** Players will place tokens for encounters during play.
- **Clear walkable spaces** (stone floors, vault floor).
- **Distinct walls, doors, staircases, and archways** visibly separated and labeled.
- **North entry doorway** (L3): Draw a clear 2-square-wide archway doorway cut THROUGH the north wall at columns 3–4, row 0, with a visible floor threshold and a few stone steps just inside. It opens to dark/empty space beyond the top wall (the corridor back to the Reception). It is the party's entry and the ONLY opening in the north wall. Do NOT render stairs spilling off the top edge — render a gateway set into the wall. Keep squares (3,0) and (4,0) clear of bookshelves.
- **Keep it sparse and large-scale.** Few objects, lots of open floor. Prioritize correct room dimensions and a clean readable grid over decoration.
- **Bookshelves** (L3): only along the EAST and WEST walls; leave the center open. Plus 2–3 reading tables and 2 columns.
- **Hazard zone** (L3-L4): cracked, broken stone floor across the band with a few loose rocks. No furniture.
- **Staircase** (L3→L4) should be clearly marked with visual stairs descending at columns 3–4.
- **Pedestals** (L4): four short stone pillars in a tight 2×2 cluster around square (4, 11). Otherwise the vault is open, with a few low shelves on the east/west walls and faint wall runes.
- **NO secret passage / hidden tunnel** anywhere on the map. Do not draw any faint passage, side opening, or hidden door.
- **Playable grid squares** must remain readable; objects should sit within single squares and not crowd the floor.

---

## Negative Constraints (Do NOT)

- Do NOT use perspective view, isometric view, or 3D camera.
- Do NOT warp, stretch, bend, or fade the grid. All squares must be identical size.
- Do NOT add extra rows or extra columns; the grid must be exactly 10×14.
- Do NOT draw any art, furniture, shadow, or texture over the grid lines; the grid sits on top.
- Do NOT add a large black void between rooms.
- Do NOT omit grid lines on any square, including stair landings, archway interiors, corridor mouths, or dark areas.
- Do NOT paint door art, ornamental tiles, or texture fills over grid lines.
- Do NOT create disconnected rooms or floating corridors.
- Do NOT add extra rooms, doors, walls, pits, or blocked paths beyond the topology specified.
- Do NOT add any opening, doorway, gate, or stairway on the outer walls except the single NORTH entry doorway at columns 3–4, row 0. The north wall (apart from that doorway), both side walls, and the SOUTH/bottom wall are solid stone. In particular the vault's south wall (bottom edge, row 13) is a sealed terminus — no exit there.
- Do NOT render stairs running off the top edge of the image; the north entry is a doorway set INTO the north wall.
- Do NOT place bookshelves, furniture, or debris so densely that tokens cannot stand in combat spaces or move through corridors.
- Do NOT hide the north doorway, the central staircases, or the vault in visual noise. Make them recognizable.
- Do NOT crowd the rooms — keep them sparse and large-scale with open floor.
- Do NOT crop the outer grid or use a decorative border that changes playable dimensions.
- Do NOT move or resize rooms. Room positions, sizes, and connections are fixed.
- Do NOT change the grid scale or square size.
- Do NOT render the four pedestals as taking more than 1 tactical square of space. They are abstracted mechanically; show them clearly but compactly.

---

## Post-Generation Validation Checklist

After ChatGPT generates the map:

1. **Count grid squares:** Confirm exactly 10 wide × 14 tall (no extra rows or columns) ✓
2. **Confirm numbered labels:** Columns 0–9 along the top, rows 0–13 along the left, aligned to squares ✓
3. **Confirm grid is on top:** Grid lines drawn above all art, furniture, and shadows—nothing painted over them ✓
4. **Confirm room positions and sizes:**
   - L3-Reading: (0, 0), 10×6 ✓
   - L3-L4-Hazard: (0, 6), 10×3 ✓
   - L4-Archive: (0, 9), 10×5 ✓
5. **Confirm NORTH entry + sealed walls:** A 2-square archway doorway is cut through the north wall at columns 3–4, row 0 (threshold + steps inside), and it is the ONLY opening in the north wall — no stairs spill off the top edge. No stray openings on the side walls, and the vault's south/bottom wall (row 13) is solid with no exit ✓
6. **Confirm corridors (only these):**
   - L3→Hazard at columns 3–4, rows 5–6, width 2–3 ✓
   - Hazard→L4 stairs at columns 3–4, rows 8–9, width 2 ✓
   - NO secret passage / hidden tunnel drawn anywhere ✓
7. **Confirm hazard zone:** Cracked/broken floor across L3-L4 (rows 6–8); no furniture ✓
8. **Confirm vault:** Four pedestals clustered at ~(4, 11); otherwise open floor with faint wall runes ✓
9. **Confirm sparseness:** Rooms are uncluttered — bookshelves only on east/west walls, lots of open floor ✓
10. **Confirm grid continuity:** Every square has visible grid lines, including stair landings and archway interiors ✓
11. **Confirm print validity:** A3 portrait, 28 mm grid, 6 mm margins → 10×14 squares (280×392 mm grid). When rendered at 331 px/sq for 300 DPI, each square measures 28 mm on paper ✓

---

**This is Sheet 2 of 2.** Party enters from Sheet 1: the Reception's SOUTH stairs descend to the NORTH entry of L3-Reading (top edge, columns 3–4, row 0). They explore, discover the odd statue (optional secret passage), navigate the hazard south, and reach the vault puzzle and construct guardian.

---

## DM Notes (Not for ChatGPT)

- **Puzzle mechanic:** You control the four books, riddle, and solution. Party discovers books scattered in L3-Reading or brought to the vault. Riddle should be logical, solvable with investigation.
- **Construct stats:** Use a standard stone golem (CR 5, 70 HP, AC 17, resistant to magic, low Dex). Or reskin as an animated suit of dwarf-forged armor (similar stats).
- **Secret passage discovery:** Reward good investigation/perception rolls. Odd statue should stand out (different color, pose, newer-looking, unusual engraving) but not instant. Make it an "aha!" moment for thorough players.
- **Hazard scaling:** For a 5th-level party, 1d6 falling damage per trigger is appropriate. Adjust upward (2d6) or downward (1d4) based on party resilience.
- **Pacing:** If party solves puzzle correctly, L4-Archive is a short victory encounter. If they fail, construct combat adds 1–2 rounds of action. Either way, they retrieve the vault contents and complete the objective.
