# The Great Library of Nalrock — Two-Sheet Battlemap Summary

**Project Status:** ✓ Design validated, ready for ChatGPT image generation.

---

## Quick Facts

- **Location:** The Great Library of Nalrock, Knowhere (dwarven, abandoned 2–3 years).
- **Party:** 5th level, 5 PCs.
- **Objective:** Retrieval raid—back and forth through levels 1–4.
- **Print Target:** Two A3 sheets (297 × 420 mm), 28 mm grid per square.
- **Grid:** 10 wide × 14 tall squares per sheet.

---

## Sheet 1: Levels 1–2 (Enclosed Garden + Reception Hall)

| Room | Position | Size | Role | Encounter |
|------|----------|------|------|-----------|
| L2-Reception | (0, 6) | 10×8 | **Main entry (WEST door)** | 4 council cultists (red robes) |
| L1-Garden | (0, 0) | 10×6 | Isolated side-room | 2 guard drakes (optional) |

**Entrances & connections:**
- **West entrance** (Reception west wall, col 0, rows 9–10) — library's main door from the city; party's entry point.
- **Garden door** (cols 3–4, rows 5–6) — single door; the isolated garden's only access, off the Reception's north wall.
- **South stairs** (Reception, cols 3–4, row 13) — descend to Sheet 2.

**Tactics:** Party enters west into the Reception (main cultist fight). The Enclosed Garden is an isolated dead-end detour (optional drake lair). Light to moderate cover (benches, statues, desks).

---

## Sheet 2: Levels 3–4 (Grand Reading Hall + Hidden Archive)

| Room | Position | Size | Role | Encounter/Feature |
|------|----------|------|------|-------------------|
| L3-Reading | (0, 0) | 10×6 | Exploration | None (hint: odd statue → secret passage) |
| L3-L4-Hazard | (0, 6) | 10×3 | Hazard transition | Difficult terrain + falling debris (DC 10 Acrobatics, DC 12 Dex save) |
| L4-Archive | (0, 9) | 10×5 | Puzzle + Boss | Construct guardian (triggered on wrong puzzle solution) |

**Entrances & connections:**
- **North entry** (Reading Hall north wall, cols 3–4, row 0) — stairs up to the Reception (Sheet 1 stacks above). This is where the party enters Sheet 2.
- L3→Hazard: 3-square-wide corridor, SOUTH edge of the Reading Hall.
- Hazard→L4: 2-square-wide staircase.
- L3→L4 (secret): 1-square-wide hidden passage behind odd statue; bypasses hazard.

**Tactics:** Dense bookshelves in L3 (exploration, cover). Hazard zone punishes speed but avoidable. L4 vault is a puzzle chamber—construct only awakens on failure. Four stone pedestals (abstracted to 1 tactical square) represent the book-placement logic puzzle.

---

## Topology Graph

```
[CITY] → WEST entrance
    ↓
L2-Reception (cultists)  ──north door──  L1-Enclosed Garden (isolated, optional drakes)
    ↓ (SOUTH stairs, Sheet 1 → Sheet 2)
L3-Reading (exploration + secret hint)   ← entry at NORTH edge
    ├→ (south corridor) L3-L4-Hazard (difficult terrain)
    │   ↓ (staircase)
    │   L4-Archive (puzzle + construct)
    └→ (secret passage) L4-Archive (directly, bypassing hazard)
```

---

## Validated JSON Specs

Both specs pass the dnd-map-architect validator with no errors or warnings.

- **Sheet 1 JSON:** `nalrock-sheet1.json` (10×14 grid, 2 encounters, 1 corridor)
- **Sheet 2 JSON:** `nalrock-sheet2.json` (10×14 grid, 3 rooms, 1 hazard, 1 encounter, 3 corridors including secret passage)

---

## ChatGPT Image Generation Prompts

Two detailed prompts ready to paste into ChatGPT:

- **Sheet 1 Prompt:** `chatgpt-prompt-sheet1.md`  
  → Copy paste directly into ChatGPT. Includes exact grid specs, print math, room coordinates, cover placement, and negative constraints.

- **Sheet 2 Prompt:** `chatgpt-prompt-sheet2.md`  
  → Copy paste directly into ChatGPT. Includes exploration hints, hazard mechanics, puzzle abstraction, and post-generation checklist.

---

## How to Use These Prompts with ChatGPT

1. Copy the text from `chatgpt-prompt-sheet1.md` and paste into a new ChatGPT conversation.
2. Request the image. ChatGPT will generate a top-down grid battlemap.
3. **Review the output** against the post-generation checklist at the end of each prompt.
4. If the grid is distorted, rooms are moved, or grid lines are missing on door thresholds, use the **correction prompt template** (in `prompt-templates.md`) to request a revision.
5. Repeat for Sheet 2.

---

## Key Features by Sheet

### Sheet 1: Combat-Focused
- ✓ West entrance into the Reception (main cultist fight).
- ✓ Isolated Enclosed Garden as an optional dead-end detour (drake lair).
- ✓ Light to moderate cover (desks, columns, statues).
- ✓ South stairs descend to Level 3 (Sheet 2).

### Sheet 2: Exploration + Puzzle + Hazard + Boss
- ✓ Hidden secret (odd statue → secret passage).
- ✓ Hazard zone with environmental challenge (cracked floor, falling debris).
- ✓ Optional bypass (secret passage avoids hazard).
- ✓ Puzzle mechanic (4 books, logic riddle, construct trigger).
- ✓ Boss encounter (construct guardian, CR 5, dormant until puzzle fails).

---

## Printing

Each A3 sheet, **portrait** (297 × 420 mm), with 28 mm grid squares and 6 mm margins.

**Grid scale (derived from the page, not chosen):**
- Usable area: (297 − 12) × (420 − 12) = 285 × 408 mm
- Squares that fit: floor(285/28) × floor(408/28) = **10 columns × 14 rows**
- Printed grid area: 280 × 392 mm (centered, thin border inside the usable area)

**Print resolution:** 300 DPI
**Pixels per square:** 331 px (28 mm ÷ 25.4 × 300)
**Grid render size:** 3310 × 4634 px (at 300 DPI, each square renders exactly 28 mm on paper)

When printed:
- Each grid square = 28 mm × 28 mm
- Printed grid = 280 mm × 392 mm
- Margins = 6 mm minimum on all sides

**Pro tip:** Test print on a sample A3 sheet and measure a grid square with a ruler to confirm it's 28 mm before printing the final maps. Print at 100% / "actual size" — do NOT use "fit to page," which rescales the grid.

---

## DM Prep Checklist

- [ ] Generate Sheet 1 image from ChatGPT (print battlemap).
- [ ] Generate Sheet 2 image from ChatGPT (print battlemap).
- [ ] Review both maps against post-generation checklists.
- [ ] Print on A3 paper or upload to VTT (100 px/sq if using digital).
- [ ] Prepare 2 medium guard drakes (CR 2–3) with ~60 HP each.
- [ ] Prepare 4 robed cultist enemies (CR 1/4–1/2) with ~20 HP each.
- [ ] Design the 4 books + logic riddle for the L4 puzzle.
- [ ] Prepare stone golem or construct guardian (CR 5, ~70 HP, high AC, magic resistant).
- [ ] Prepare quest-relevant vault contents (scrolls, maps, research notes).
- [ ] Set up back-and-forth encounter triggers (drakes don't pursue; cultists defend; construct only awakens on puzzle failure).

---

## Encounter Summary for Quick Reference

| Encounter | Location | Enemy | Count | Size | Difficulty | Trigger | Objective |
|-----------|----------|-------|-------|------|------------|---------|-----------
| Council Cultists | L2-Reception (west entry) | Robed Agent | 4 | Medium | Moderate | On entry through west door | Defeat to reach south stairs |
| Guard Drakes | L1-Enclosed Garden (isolated) | Drake | 2 | Medium | Moderate | Optional — only if garden door opened | Clear for lore/loot, or skip |
| Hazard Transition | L3-L4 | Environmental | — | — | Hard | Navigating stairs | Survive cracked floor, falling debris |
| Construct Guardian | L4-Archive | Golem/Construct | 1 | Medium | Hard | Wrong puzzle | Defeat or solve puzzle correctly |

---

## Next Steps

1. **Copy Sheet 1 prompt** (`chatgpt-prompt-sheet1.md`) into ChatGPT.
2. **Request image generation.** Tell ChatGPT: "Create this D&D battlemap."
3. **Review output.** Check grid count, room positions, cover placement, and grid continuity.
4. **Request revisions if needed** using the correction prompt template.
5. **Repeat for Sheet 2.**
6. **Print or import** to your VTT at 100 px per square (or 331 px per square for 300 DPI A3 print).
7. **Run the raid.** Two sheets, four encounters (or fewer if party solves puzzle correctly).

---

## Files in This Project

- `nalrock-sheet1.json` — Validated dungeon spec (Sheet 1).
- `nalrock-sheet2.json` — Validated dungeon spec (Sheet 2).
- `chatgpt-prompt-sheet1.md` — ChatGPT image generation prompt (copy/paste ready).
- `chatgpt-prompt-sheet2.md` — ChatGPT image generation prompt (copy/paste ready).
- `BATTLE-MAP-SUMMARY.md` — This file (overview and DM reference).

All artifacts generated by **dnd-map-architect** skill via topology validation and prompt generation.

---

**Ready to generate images.** Paste either ChatGPT prompt into your preferred AI image tool and let it render the maps.
