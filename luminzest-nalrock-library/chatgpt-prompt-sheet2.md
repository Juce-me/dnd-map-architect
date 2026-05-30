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

1. **L3-Reading (Grand Reading Hall) — ENTRY FROM RECEPTION (NORTH)**  
   Position: (0, 0) — top, rows 0–5  
   Size: 10 wide × 6 tall  
   Role: The party arrives here from the Reception Hall (Sheet 1, which stacks directly above). **The connection to the Reception is at the NORTH edge (top), not the south.**  
   Features:
   - **NORTH ENTRY — main doorway from the Reception (Sheet 1):** Cut a clear 2-square-wide ARCHWAY DOORWAY through the NORTH wall at columns 3–4, row 0 (top edge). It is an open stone gateway with a visible threshold on the floor of squares (3,0) and (4,0), opening to black/empty space beyond the top wall (the corridor back to the Reception). Render a few stone steps just inside it. This is the party's entry. **This doorway is the ONLY opening in the north wall** — the rest of the top wall is solid stone (lined with bookshelves and windows). Do NOT draw stairs running off the top edge of the image; draw a doorway/gateway set INTO the wall.
   - Vast library hall with hundreds of bookshelves (heavy cover, dense throughout, 1×1 clusters; bookshelves do not block movement through squares but provide cover). Keep the bookshelves clear of squares (3,0) and (4,0) so the north doorway is not blocked.
   - Reading tables and study desks (light cover, scattered throughout).
   - High stone columns (partial cover, non-blocking, 1 square each, scattered).
   - Small private reading alcoves (light cover, nooks along walls).
   - Statues of famous scholars (decorative, non-blocking).
   - **Secret Feature — ODD STATUE (HINT TO HIDDEN PASSAGE):** One statue among the many is visually distinct — unusual pose, material, or engraving. Marked at position (8, 3) approximately. Player investigation or Perception check (DC 13) reveals it can be manipulated/pushed to open a hidden passage leading down to Level 4 Hidden Archive (secret corridor, bypasses hazard transition).
   - **Connection to Reception (Sheet 1):** NORTH stairs at columns 3–4, row 0 (top edge).
   - **Connection to Hazard:** Corridor SOUTH at columns 3–4, between rows 5 and 6 (bottom edge).
   - **Connection to Secret Passage:** Secret passage at (8, 6) leads to L4-Archive (8, 9).

2. **L3-L4-Hazard (Hazardous Transition)**  
   Position: (0, 6) — center  
   Size: 10 wide × 3 tall  
   Features:
   - Steep stone staircase descending to Level 4 (architectural feature, non-tactical).
   - Collapsed/broken floor tiles creating difficult terrain (scattered 5×5 area in center; see hazard details below).
   - Unstable ceiling supports and ancient stonework (risk of falling debris; see hazard details below).
   - Bioluminescent fungi patches (faint glow, non-tactical, atmospheric).
   - **Hazards:**
     - **Difficult Terrain (collapsed floor):** Central 5×5 area (approximately (2, 6) to (7, 9)) consists of cracked and uneven stones. Movement through = half speed; DC 10 Acrobatics check allows full-speed movement.
     - **Falling Debris:** Random hazard, 1 in 6 chance per round. When triggered: all creatures in the hazard zone must make a DC 12 Dexterity save or take 1d6 falling stone damage. Visible cracks and loose stones telegraph the danger.
   - **Connection to Reading:** Corridor north at (3, 5)–(3, 6).
   - **Connection to Archive:** Stairs south at (3, 8)–(3, 9).

3. **L4-Archive (Hidden Archive Vault)**  
   Position: (0, 9) — bottom  
   Size: 10 wide × 5 tall  
   Features:
   - Reinforced ancient vault chamber with high arched ceiling (architectural feature, non-tactical).
   - Stone walls inscribed with runes and protective glyphs (non-tactical, lore, glow faintly when puzzle is active).
   - Shelves with restricted manuscripts and tomes (light cover, scattered along walls).
   - **Puzzle Chamber:** Four stone pedestals arranged in a small cluster, abstracted to **1 tactical square at position (4, 11)**. This represents the mechanical puzzle: party must place 4 correct books on pedestals in the correct order per a logic riddle. DM adjudicates the puzzle and books.
   - **Encounter:** Construct guardian (stone golem or similar CR 5 construct) lies dormant near the vault entrance. **Trigger:** Incorrect puzzle solution awakens the construct, which attacks until defeated or puzzle is solved correctly. Correct solution does not trigger combat; vault opens peacefully.
   - **Vault contents:** Original founding records, forbidden research, secret maps (mechanical purpose: quest objective; player reward).
   - **Connections:** 
     - Stairs from hazard at (3, 8)–(3, 9).
     - Secret passage from L3-Reading at (8, 6)–(8, 9).

### Corridors

1. **Corridor L3→Hazard** (c2-reading-to-hazard)  
   Connects: L3-Reading (3, 6) to L3-L4-Hazard (3, 6).  
   Width: 3 squares.  
   Features: Plain stone walls, dim lighting, library entrance arch.

2. **Staircase Hazard→Archive** (c3-hazard-to-archive)  
   Connects: L3-L4-Hazard (3, 8) to L4-Archive (3, 9).  
   Width: 2 squares.  
   Features: Stone staircase descending, magical rune warnings.

3. **Secret Passage L3→L4** (c4-secret-passage)  
   Connects: L3-Reading (8, 6) to L4-Archive (8, 9).  
   Width: 1 square.  
   Features: Hidden passage triggered by odd statue manipulation; bypasses hazard transition entirely. Show as a faint passage or hidden door on the map if visually appropriate.

---

## Tactical Requirements

**NOTE:** The following tactical descriptions are for the DM's reference only. **Do not render monsters, enemies, or NPCs on the battlemap itself.** The map should show only the interior layout and tactical cover. Players will place tokens on the map during play to represent characters and enemies.

### Exploration: L3-Reading Hall
- **Objective:** Explore vast shelves, discover hidden clues.
- **Key Feature:** Odd statue at (8, 3) hints at secret passage. Visual distinctness (color, pose, material, engraving) should make it stand out to observant players without being obvious. **The statue itself should be rendered on the map; do not render the hidden passage mechanism—just the distinct statue.**
- **Cover:** Dense bookshelves and reading tables provide good cover for scouting or stealth.
- **Sightlines:** Columns and shelf clusters create partial sight-line breaks.
- **Challenge:** Finding the secret passage requires investigation or Perception check (DC 13).

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
- **Bookshelves** (L3) should be recognizable as cover, arranged in 1×1 clusters throughout, leaving walkable corridors between them.
- **Decorative painted windows** (optional, L3-Reading): If appropriate to the aesthetic, scatter subtle painted or frescoed windows on the outer walls of the reading hall showing mountain vistas—painted murals giving the illusion of windows to the surface world of Nalrock. **These are purely decorative and must not block movement or grid squares.**
- **Hazard zone** (L3-L4) should visibly show cracked floor tiles, unstable stonework, and loose debris. Central 5×5 area should appear damaged/difficult; surrounding areas are passable.
- **Staircase** (L3→L4) should be clearly marked with visual stairs descending.
- **Secret passage** (if rendered) should be hidden or very subtle at L3 (at odd statue location) and appear as a faint passage or hidden door leading down to L4.
- **Pedestals** (L4) should be rendered as four distinct stone pillars clustered in one tactical square at (4, 11), or clearly labeled as "Puzzle Chamber."
- **Vault entrance area:** Show space for the dormant construct location.
- **Vault contents/shrine:** Shelves with manuscripts along walls; glowing runes on walls (faint, non-distracting).
- **Playable grid squares** must remain readable; all combat spaces must be token-playable. Bookshelves, furniture, and pedestals should not fill entire squares—they provide cover without blocking movement.

---

## Negative Constraints (Do NOT)

- Do NOT use perspective view, isometric view, or 3D camera.
- Do NOT warp, stretch, bend, or fade the grid. All squares must be identical size.
- Do NOT add extra rows or extra columns; the grid must be exactly 10×14.
- Do NOT draw any art, furniture, shadow, or texture over the grid lines; the grid sits on top.
- Do NOT add a large black void between rooms.
- Do NOT omit grid lines on any square, including stair landings, archway interiors, secret passage entrances, corridor mouths, or dark areas.
- Do NOT paint door art, ornamental tiles, or texture fills over grid lines.
- Do NOT create disconnected rooms or floating corridors.
- Do NOT add extra rooms, doors, walls, pits, or blocked paths beyond the topology specified.
- Do NOT add any opening, doorway, gate, or stairway on the outer walls except the single NORTH entry doorway at columns 3–4, row 0. The north wall (apart from that doorway), both side walls, and the SOUTH/bottom wall are solid stone. In particular the vault's south wall (bottom edge, row 13) is a sealed terminus — no exit there.
- Do NOT render stairs running off the top edge of the image; the north entry is a doorway set INTO the north wall.
- Do NOT place bookshelves, furniture, or debris so densely that tokens cannot stand in combat spaces or move through corridors.
- Do NOT hide the staircase, secret passage entrance, or vault entrance in visual noise. Make them recognizable.
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
6. **Confirm corridors:**
   - L3→Hazard at (3, 5)–(3, 6), width 3 ✓
   - Hazard→L4 at (3, 8)–(3, 9), width 2 ✓
   - Secret passage at (8, 6)–(8, 9), width 1 ✓
7. **Confirm odd statue location:** Distinct statue at L3 (8, 3) area; visually unique ✓
8. **Confirm hazard zone:** Central area of L3-L4 shows cracked/difficult terrain, ~5×5 ✓
9. **Confirm vault features:** 
   - Four pedestals at (4, 11) in L4-Archive ✓
   - Construct dormant space near vault entrance ✓
   - Glowing runes on walls (faint, non-obstructing) ✓
10. **Confirm grid continuity:** Every square has visible grid lines, including stair landings, secret passage, and archway interiors ✓
11. **Confirm encounter spaces:** Vault chamber is token-playable, corridors are passable ✓
12. **Confirm print validity:** A3 portrait, 28 mm grid, 6 mm margins → 10×14 squares (280×392 mm grid). When rendered at 331 px/sq for 300 DPI, each square measures 28 mm on paper ✓

---

**This is Sheet 2 of 2.** Party enters from Sheet 1: the Reception's SOUTH stairs descend to the NORTH entry of L3-Reading (top edge, columns 3–4, row 0). They explore, discover the odd statue (optional secret passage), navigate the hazard south, and reach the vault puzzle and construct guardian.

---

## DM Notes (Not for ChatGPT)

- **Puzzle mechanic:** You control the four books, riddle, and solution. Party discovers books scattered in L3-Reading or brought to the vault. Riddle should be logical, solvable with investigation.
- **Construct stats:** Use a standard stone golem (CR 5, 70 HP, AC 17, resistant to magic, low Dex). Or reskin as an animated suit of dwarf-forged armor (similar stats).
- **Secret passage discovery:** Reward good investigation/perception rolls. Odd statue should stand out (different color, pose, newer-looking, unusual engraving) but not instant. Make it an "aha!" moment for thorough players.
- **Hazard scaling:** For a 5th-level party, 1d6 falling damage per trigger is appropriate. Adjust upward (2d6) or downward (1d4) based on party resilience.
- **Pacing:** If party solves puzzle correctly, L4-Archive is a short victory encounter. If they fail, construct combat adds 1–2 rounds of action. Either way, they retrieve the vault contents and complete the objective.
