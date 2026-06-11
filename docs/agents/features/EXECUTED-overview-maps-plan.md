Status: executed
Type: feature
Author: Juce

# Overview Map Scales Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add an overview (zoom-out) map mode to `skills/dnd-map-architect` with four scale levels (site, settlement, region, world), a validated scale chain to existing battlemaps, per-scale intake/prompt references, and a new spec validator with tests.

**Architecture:** Shared rules live in one reference (`overview-rules.md`); each scale gets one self-contained reference with intake questions, prompt template, negative constraints, and checklist. A standalone validator script mirrors the existing `validate_dungeon_spec.py` pattern (stdlib only, `{ok, errors, warnings}` report, `CODE: message` errors) and cross-checks child spec files for footprint accuracy.

**Tech Stack:** Python 3 stdlib (json, math, argparse, unittest), Markdown skill references. Run all Python through `.venv` (create with `python3 -m venv .venv` if missing; no dependencies needed).

**Spec:** `EXECUTED-overview-maps.md` (sibling artifact; renamed in Task 10).

Branch: all tasks run on `feat/overview-map-scales`. Use repo-relative paths in all committed files and commands.

---

### Task 1: Shared overview rules reference

**Files:**
- Create: `skills/dnd-map-architect/references/overview-rules.md`

- [ ] **Step 1: Create the file with exactly this content**

````markdown
# Overview Map Rules

Shared rules for all zoom-out (overview) map scales. Read this file plus exactly
one scale file (`overview-site.md`, `overview-settlement.md`,
`overview-region.md`, `overview-world.md`) per overview request.

## Scale Ladder

| Level | Covers | Unit per grid cell | Default | Default grid |
|---|---|---|---|---|
| battlemap (level 0) | single encounter area | 5 ft per square | 5 ft | square |
| site (level 1) | whole dungeon, building, fortress | 10-50 ft per square | 10 ft | square |
| settlement (level 2) | village, town, city | 50-500 ft per square | 100 ft | square |
| region (level 3) | province, march, wilderness | 1-10 miles per hex | 6 miles | hex |
| world (level 4) | continent, known world | 25-100 miles per hex | 50 miles | hex |

- Units are feet for levels 0-2 and miles for levels 3-4; 1 mile = 5280 ft.
- Region and world maps default to pointy-top hexes with offset coordinates;
  square grids are allowed when the user prefers them.
- A `unit_per_cell` outside the level's range is a blocking error; pick the
  next level instead of stretching the scale.

## Scale Chain

An overview map may place lower-level maps on itself as `children`:

- Every child declares a real-world `footprint` (width x height in ft or miles).
- **Block**: when the footprint spans at least one parent cell on either axis,
  the child renders as a block of `ceil(footprint / unit_per_cell)` cells per
  axis at a declared cell position.
- **Marker**: when the footprint is smaller than one parent cell on both axes,
  the child renders as a labeled point-of-interest marker in one cell.
- When the child has its own spec file, reference it with `spec_path` (relative
  to the parent spec file). The validator cross-checks the declared footprint
  against the child spec's grid math and fails on any mismatch.
- A child's level must be strictly lower than the parent's level.

Worked example: the bundled Ember Archive battlemap is 24 x 18 squares at 5 ft
= 120 x 90 ft. On a site overview at 10 ft per square it is a 12 x 9 block. On
a region map at 1 mile per hex it is a marker.

## Scale Bar

Every overview map carries a scale bar:

- It spans a whole number of grid cells (`scale_bar.length_cells`).
- Its label states the real-world length: `length_cells x unit_per_cell`
  (for example 5 squares = 50 ft, or 5 hexes = 30 miles).
- On printed maps the bar must measure true: bar length in mm equals
  `length_cells x physical_grid_mm`.

## Schematic Discipline

Overview maps are schemes, not battlemaps:

- Show blocks, routes, markers, terrain, water, walls, and labels.
- Never render furniture, creatures, tokens, NPCs, armies, or tactical detail.
- Label key locations with short names; numbered coordinates handle the rest.

## Grid And Coordinates

- The numbered coordinate grid leads every prompt: columns 0 to width-1 along
  the top, rows 0 to height-1 along the left, exact counts stated.
- Grid lines are drawn above all art, terrain, blocks, and labels.
- Square grids require identical pixels per cell on both axes.

## Print Math

Work in millimeters. Defaults: 28 mm per cell, 6 mm margins, 300 DPI
(consistent with `print-rules.md`).

Square grids use the `print-rules.md` formulas:
`usable_mm = paper_side - 2 x margin_mm`, then
`max_cells = floor(usable_mm / physical_grid_mm)` per axis.

Hex grids tile differently. For pointy-top hexes with flat-to-flat width `w`
mm and corner-to-corner height `h = 2w / sqrt(3)`:

- `columns_max = floor((usable_width - 0.5w) / w)` (offset rows shift by w/2).
- `rows_max = floor((usable_height - 0.25h) / 0.75h)` (rows overlap by h/4).
- Flat-top hexes swap the axes.

Worked example - A3 landscape (408 x 285 mm usable) at 28 mm flat-to-flat,
pointy-top: `h = 32.3 mm`; columns = floor((408 - 14) / 28) = 14; rows =
floor((285 - 8.1) / 24.2) = 11. A region map prints 14 x 11 hexes per sheet.

## Overview Spec Shape

```json
{
  "map_kind": "overview",
  "identity": {"name": "...", "overview_type": "..."},
  "scale": {"level": "site", "unit_per_cell": 10},
  "technical": {
    "grid_type": "square",
    "width_cells": 14,
    "height_cells": 10,
    "image_dimensions_px": [1400, 1000],
    "scale_bar": {"length_cells": 5, "label_units": 50},
    "print": {"enabled": true, "paper": "A3", "physical_grid_mm": 28, "margin_mm": 6, "split_pages": false}
  },
  "features": [
    {"id": "approach", "name": "Approach Road", "kind": "route", "x": 0, "y": 9, "width": 14, "height": 1}
  ],
  "children": [
    {
      "id": "ember-archive", "name": "Ember Archive", "level": "battlemap",
      "representation": "block", "x": 1, "y": 0,
      "footprint": {"width": 120, "height": 90, "unit": "ft"},
      "block": {"width": 12, "height": 9},
      "spec_path": "valid-dungeon-spec.json"
    }
  ]
}
```

Hex grids add `"orientation": "pointy"` and `"coordinate_system": "offset"`
inside `technical`. Validate every overview spec with
`scripts/validate_overview_spec.py` before writing any image prompt.
````

- [ ] **Step 2: Commit**

```bash
git add skills/dnd-map-architect/references/overview-rules.md
git commit -m "Add shared overview map rules reference

Scale ladder, scale chain with block/marker math, scale bar, hex and
square print-fit formulas, and the overview JSON spec shape."
```

---

### Task 2: Overview validator tests (failing first)

**Files:**
- Create: `skills/dnd-map-architect/tests/test_validate_overview_spec.py`

- [ ] **Step 1: Create the test file with exactly this content**

```python
import importlib.util
import json
import pathlib
import tempfile
import unittest


SCRIPT_PATH = pathlib.Path(__file__).resolve().parents[1] / "scripts" / "validate_overview_spec.py"


def load_validator():
    spec = importlib.util.spec_from_file_location("validate_overview_spec", SCRIPT_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def site_spec():
    return {
        "map_kind": "overview",
        "identity": {"name": "Ember Archive Site Plan", "overview_type": "dungeon complex"},
        "scale": {"level": "site", "unit_per_cell": 10},
        "technical": {
            "grid_type": "square",
            "width_cells": 14,
            "height_cells": 10,
            "image_dimensions_px": [1400, 1000],
            "scale_bar": {"length_cells": 5, "label_units": 50},
            "print": {
                "enabled": True,
                "paper": "A3",
                "physical_grid_mm": 28,
                "margin_mm": 6,
                "split_pages": False,
            },
        },
        "features": [
            {"id": "approach", "name": "Approach Road", "kind": "route", "x": 0, "y": 9, "width": 14, "height": 1},
        ],
        "children": [
            {
                "id": "ember-archive",
                "name": "Ember Archive",
                "level": "battlemap",
                "representation": "block",
                "x": 1,
                "y": 0,
                "footprint": {"width": 120, "height": 90, "unit": "ft"},
                "block": {"width": 12, "height": 9},
            },
        ],
    }


def region_spec():
    return {
        "map_kind": "overview",
        "identity": {"name": "Emberfall March", "overview_type": "region"},
        "scale": {"level": "region", "unit_per_cell": 1},
        "technical": {
            "grid_type": "hex",
            "orientation": "pointy",
            "coordinate_system": "offset",
            "width_cells": 14,
            "height_cells": 11,
            "scale_bar": {"length_cells": 5},
            "print": {"enabled": False},
        },
        "features": [],
        "children": [
            {
                "id": "greywater",
                "name": "Greywater",
                "level": "settlement",
                "representation": "block",
                "x": 4,
                "y": 5,
                "footprint": {"width": 2, "height": 1, "unit": "miles"},
                "block": {"width": 2, "height": 1},
            },
        ],
    }


def codes(report):
    return [message.split(":")[0] for message in report["errors"] + report["warnings"]]


class ValidateOverviewSpecTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.validator = load_validator()

    def validate(self, spec, base_dir=None):
        return self.validator.validate_spec(spec, base_dir=base_dir)

    def test_valid_site_spec_passes(self):
        report = self.validate(site_spec())
        self.assertEqual(report["errors"], [])
        self.assertTrue(report["ok"])

    def test_valid_region_spec_passes(self):
        report = self.validate(region_spec())
        self.assertEqual(report["errors"], [])
        self.assertTrue(report["ok"])

    def test_map_kind_required(self):
        spec = site_spec()
        del spec["map_kind"]
        self.assertIn("MAP_KIND_INVALID", codes(self.validate(spec)))

    def test_identity_required_fields(self):
        spec = site_spec()
        spec["identity"] = {}
        report_codes = codes(self.validate(spec))
        self.assertIn("IDENTITY_MISSING_NAME", report_codes)
        self.assertIn("IDENTITY_MISSING_OVERVIEW_TYPE", report_codes)

    def test_scale_level_invalid(self):
        spec = site_spec()
        spec["scale"]["level"] = "kingdom"
        self.assertIn("SCALE_LEVEL_INVALID", codes(self.validate(spec)))

    def test_battlemap_is_not_an_overview_level(self):
        spec = site_spec()
        spec["scale"]["level"] = "battlemap"
        self.assertIn("SCALE_LEVEL_INVALID", codes(self.validate(spec)))

    def test_scale_unit_out_of_range(self):
        spec = site_spec()
        spec["scale"]["unit_per_cell"] = 60
        self.assertIn("SCALE_UNIT_OUT_OF_RANGE", codes(self.validate(spec)))

    def test_scale_unit_invalid(self):
        spec = site_spec()
        spec["scale"]["unit_per_cell"] = 0
        self.assertIn("SCALE_UNIT_INVALID", codes(self.validate(spec)))

    def test_grid_dimensions_invalid(self):
        spec = site_spec()
        spec["technical"]["width_cells"] = 0
        self.assertIn("GRID_WIDTH_INVALID", codes(self.validate(spec)))

    def test_hex_requires_orientation(self):
        spec = region_spec()
        del spec["technical"]["orientation"]
        self.assertIn("GRID_HEX_ORIENTATION_REQUIRED", codes(self.validate(spec)))

    def test_hex_requires_coordinate_system(self):
        spec = region_spec()
        del spec["technical"]["coordinate_system"]
        self.assertIn("GRID_HEX_COORDINATE_SYSTEM_REQUIRED", codes(self.validate(spec)))

    def test_pixels_per_cell_must_divide(self):
        spec = site_spec()
        spec["technical"]["image_dimensions_px"] = [1401, 1000]
        self.assertIn("GRID_NON_INTEGER_PIXELS_PER_CELL", codes(self.validate(spec)))

    def test_pixels_per_cell_distorted(self):
        spec = site_spec()
        spec["technical"]["image_dimensions_px"] = [1400, 1100]
        self.assertIn("GRID_DISTORTED", codes(self.validate(spec)))

    def test_scale_bar_missing(self):
        spec = site_spec()
        del spec["technical"]["scale_bar"]
        self.assertIn("SCALE_BAR_MISSING", codes(self.validate(spec)))

    def test_scale_bar_length_invalid(self):
        spec = site_spec()
        spec["technical"]["scale_bar"]["length_cells"] = 0
        self.assertIn("SCALE_BAR_INVALID", codes(self.validate(spec)))

    def test_scale_bar_too_long(self):
        spec = site_spec()
        spec["technical"]["scale_bar"]["length_cells"] = 15
        self.assertIn("SCALE_BAR_INVALID", codes(self.validate(spec)))

    def test_scale_bar_label_mismatch(self):
        spec = site_spec()
        spec["technical"]["scale_bar"]["label_units"] = 40
        self.assertIn("SCALE_BAR_MISMATCH", codes(self.validate(spec)))

    def test_feature_out_of_bounds(self):
        spec = site_spec()
        spec["features"][0]["width"] = 15
        self.assertIn("FEATURE_OUT_OF_BOUNDS", codes(self.validate(spec)))

    def test_feature_duplicate_id(self):
        spec = site_spec()
        spec["features"].append(dict(spec["features"][0]))
        self.assertIn("FEATURE_DUPLICATE_ID", codes(self.validate(spec)))

    def test_child_level_invalid(self):
        spec = site_spec()
        spec["children"][0]["level"] = "cosmos"
        self.assertIn("CHAIN_LEVEL_INVALID", codes(self.validate(spec)))

    def test_child_level_not_lower(self):
        spec = site_spec()
        spec["children"][0]["level"] = "site"
        self.assertIn("CHAIN_LEVEL_NOT_LOWER", codes(self.validate(spec)))

    def test_child_footprint_invalid(self):
        spec = site_spec()
        spec["children"][0]["footprint"]["width"] = -5
        self.assertIn("CHAIN_FOOTPRINT_INVALID", codes(self.validate(spec)))

    def test_child_representation_invalid(self):
        spec = site_spec()
        spec["children"][0]["representation"] = "icon"
        self.assertIn("CHAIN_REPRESENTATION_INVALID", codes(self.validate(spec)))

    def test_block_size_mismatch(self):
        spec = site_spec()
        spec["children"][0]["block"] = {"width": 11, "height": 9}
        self.assertIn("CHAIN_BLOCK_SIZE_MISMATCH", codes(self.validate(spec)))

    def test_block_size_uses_ceiling(self):
        spec = site_spec()
        spec["children"][0]["footprint"] = {"width": 115, "height": 85, "unit": "ft"}
        spec["children"][0]["block"] = {"width": 12, "height": 9}
        report = self.validate(spec)
        self.assertEqual(report["errors"], [])

    def test_block_out_of_bounds(self):
        spec = site_spec()
        spec["children"][0]["x"] = 3
        self.assertIn("CHAIN_OUT_OF_BOUNDS", codes(self.validate(spec)))

    def test_marker_required_for_subcell_footprint(self):
        spec = region_spec()
        spec["children"].append(
            {
                "id": "ember-archive",
                "name": "Ember Archive",
                "level": "battlemap",
                "representation": "block",
                "x": 2,
                "y": 2,
                "footprint": {"width": 120, "height": 90, "unit": "ft"},
                "block": {"width": 1, "height": 1},
            }
        )
        self.assertIn("CHAIN_REPRESENTATION_MUST_BE_MARKER", codes(self.validate(spec)))

    def test_block_required_for_cell_spanning_footprint(self):
        spec = site_spec()
        spec["children"][0]["representation"] = "marker"
        del spec["children"][0]["block"]
        self.assertIn("CHAIN_REPRESENTATION_MUST_BE_BLOCK", codes(self.validate(spec)))

    def test_child_spec_missing(self):
        spec = site_spec()
        spec["children"][0]["spec_path"] = "missing.json"
        with tempfile.TemporaryDirectory() as tmp:
            self.assertIn("CHAIN_CHILD_SPEC_MISSING", codes(self.validate(spec, base_dir=tmp)))

    def test_child_spec_cross_check_passes(self):
        spec = site_spec()
        spec["children"][0]["spec_path"] = "child.json"
        child = {"technical": {"width_squares": 24, "height_squares": 18, "tile_scale_ft": 5}}
        with tempfile.TemporaryDirectory() as tmp:
            (pathlib.Path(tmp) / "child.json").write_text(json.dumps(child), encoding="utf-8")
            report = self.validate(spec, base_dir=tmp)
        self.assertEqual(report["errors"], [])

    def test_child_spec_footprint_mismatch(self):
        spec = site_spec()
        spec["children"][0]["spec_path"] = "child.json"
        child = {"technical": {"width_squares": 20, "height_squares": 18, "tile_scale_ft": 5}}
        with tempfile.TemporaryDirectory() as tmp:
            (pathlib.Path(tmp) / "child.json").write_text(json.dumps(child), encoding="utf-8")
            self.assertIn("CHAIN_FOOTPRINT_MISMATCH", codes(self.validate(spec, base_dir=tmp)))

    def test_child_spec_level_mismatch(self):
        spec = region_spec()
        spec["children"].append(
            {
                "id": "old-keep",
                "name": "Old Keep",
                "level": "battlemap",
                "representation": "marker",
                "x": 7,
                "y": 3,
                "footprint": {"width": 140, "height": 100, "unit": "ft"},
                "spec_path": "child.json",
            }
        )
        child = {
            "map_kind": "overview",
            "scale": {"level": "site", "unit_per_cell": 10},
            "technical": {"width_cells": 14, "height_cells": 10},
        }
        with tempfile.TemporaryDirectory() as tmp:
            (pathlib.Path(tmp) / "child.json").write_text(json.dumps(child), encoding="utf-8")
            self.assertIn("CHAIN_LEVEL_MISMATCH", codes(self.validate(spec, base_dir=tmp)))

    def test_print_requires_split(self):
        spec = site_spec()
        spec["technical"]["width_cells"] = 20
        spec["technical"]["image_dimensions_px"] = [2000, 1000]
        self.assertIn("PRINT_REQUIRES_SPLIT", codes(self.validate(spec)))

    def test_hex_print_requires_split(self):
        spec = region_spec()
        spec["technical"]["width_cells"] = 15
        spec["technical"]["print"] = {
            "enabled": True,
            "paper": "A3",
            "physical_grid_mm": 28,
            "margin_mm": 6,
            "split_pages": False,
        }
        self.assertIn("PRINT_REQUIRES_SPLIT", codes(self.validate(spec)))

    def test_print_underfill_warning(self):
        spec = site_spec()
        spec["technical"]["width_cells"] = 7
        spec["technical"]["height_cells"] = 5
        spec["technical"]["image_dimensions_px"] = [700, 500]
        spec["features"] = []
        spec["children"] = []
        report = self.validate(spec)
        self.assertEqual(report["errors"], [])
        self.assertIn("PRINT_UNDERFILL", codes(report))


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run the tests to verify they fail for the right reason**

Run: `.venv/bin/python skills/dnd-map-architect/tests/test_validate_overview_spec.py`
Expected: FAIL during `setUpClass` with `FileNotFoundError` (the validator script does not exist yet). If `.venv` is missing, first run `python3 -m venv .venv`.

Do not commit yet; Task 3 commits tests and implementation together.

---

### Task 3: Overview validator implementation

**Files:**
- Create: `skills/dnd-map-architect/scripts/validate_overview_spec.py`
- Test: `skills/dnd-map-architect/tests/test_validate_overview_spec.py` (from Task 2)

- [ ] **Step 1: Create the script with exactly this content**

```python
#!/usr/bin/env python3
"""Validate overview (zoom-out) map specs for scale, chain, grid, and print."""

import argparse
import json
import math
import os
import sys

MM_PER_INCH = 25.4
FT_PER_MILE = 5280
REL_TOL = 1e-6
SQRT3 = math.sqrt(3)

SCALE_LEVELS = {
    "battlemap": {"rank": 0, "unit": "ft"},
    "site": {"rank": 1, "unit": "ft", "min_unit": 10, "max_unit": 50},
    "settlement": {"rank": 2, "unit": "ft", "min_unit": 50, "max_unit": 500},
    "region": {"rank": 3, "unit": "miles", "min_unit": 1, "max_unit": 10},
    "world": {"rank": 4, "unit": "miles", "min_unit": 25, "max_unit": 100},
}
GRID_TYPES = {"square", "hex"}
HEX_ORIENTATIONS = {"pointy", "pointy-top", "flat", "flat-top"}
HEX_COORDINATE_SYSTEMS = {"axial", "offset"}
FOOTPRINT_UNITS = {"ft", "miles"}
PAPER_SIZES = {
    "A4": (210, 297),
    "A3": (297, 420),
    "Letter": (215.9, 279.4),
    "Ledger": (279.4, 431.8),
}


def validate_spec(spec, base_dir=None):
    errors = []
    warnings = []

    if not isinstance(spec, dict):
        return {"ok": False, "errors": ["SPEC_INVALID: root must be an object"], "warnings": []}

    if spec.get("map_kind") != "overview":
        errors.append('MAP_KIND_INVALID: map_kind must be "overview"')

    identity = spec.get("identity")
    if not isinstance(identity, dict):
        errors.append("SPEC_MISSING: identity must be an object")
    else:
        _require_string(identity, "name", "IDENTITY_MISSING_NAME", errors)
        _require_string(identity, "overview_type", "IDENTITY_MISSING_OVERVIEW_TYPE", errors)

    scale_context = _validate_scale(spec, errors)
    grid_context = _validate_technical(spec, errors)
    _validate_scale_bar(scale_context, grid_context, errors)
    _validate_features(spec, grid_context, errors)
    _validate_children(spec, scale_context, grid_context, base_dir, errors)
    _validate_print(grid_context, errors, warnings)

    return {"ok": not errors, "errors": errors, "warnings": warnings}


def _require_string(parent, key, code, errors):
    value = parent.get(key)
    if not isinstance(value, str) or value == "":
        errors.append(f"{code}: {key} must be a non-empty string")


def _positive_int(value):
    return isinstance(value, int) and not isinstance(value, bool) and value > 0


def _nonnegative_int(value):
    return isinstance(value, int) and not isinstance(value, bool) and value >= 0


def _number(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def _positive_number(value):
    return _number(value) and value > 0


def _nonnegative_number(value):
    return _number(value) and value >= 0


def _to_ft(value, unit):
    return value * FT_PER_MILE if unit == "miles" else value


def _validate_scale(spec, errors):
    scale = spec.get("scale")
    if not isinstance(scale, dict):
        errors.append("SPEC_MISSING: scale must be an object")
        return {}

    level = scale.get("level")
    info = SCALE_LEVELS.get(level)
    if info is None or info["rank"] == 0:
        overview_levels = sorted(name for name, data in SCALE_LEVELS.items() if data["rank"] > 0)
        errors.append(f"SCALE_LEVEL_INVALID: scale.level must be one of {overview_levels}")
        return {}

    context = {"level": level, "rank": info["rank"], "unit": info["unit"]}
    unit_per_cell = scale.get("unit_per_cell")
    if not _positive_number(unit_per_cell):
        errors.append("SCALE_UNIT_INVALID: scale.unit_per_cell must be a positive number")
        return context

    if not info["min_unit"] <= unit_per_cell <= info["max_unit"]:
        errors.append(
            f"SCALE_UNIT_OUT_OF_RANGE: {level} requires {info['min_unit']}-{info['max_unit']} "
            f"{info['unit']} per cell"
        )
    context["unit_per_cell"] = unit_per_cell
    return context


def _validate_technical(spec, errors):
    technical = spec.get("technical")
    if not isinstance(technical, dict):
        errors.append("SPEC_MISSING: technical must be an object")
        return {}

    context = {"technical": technical}
    grid_type = technical.get("grid_type")
    if grid_type not in GRID_TYPES:
        errors.append(f"GRID_TYPE_INVALID: grid_type must be one of {sorted(GRID_TYPES)}")
    context["grid_type"] = grid_type

    width = technical.get("width_cells")
    height = technical.get("height_cells")
    if not _positive_int(width):
        errors.append("GRID_WIDTH_INVALID: width_cells must be a positive integer")
        width = None
    if not _positive_int(height):
        errors.append("GRID_HEIGHT_INVALID: height_cells must be a positive integer")
        height = None
    context["width_cells"] = width
    context["height_cells"] = height

    if grid_type == "hex":
        orientation = technical.get("orientation")
        coordinate_system = technical.get("coordinate_system")
        if orientation not in HEX_ORIENTATIONS:
            errors.append(
                f"GRID_HEX_ORIENTATION_REQUIRED: hex grids require orientation, one of {sorted(HEX_ORIENTATIONS)}"
            )
        if coordinate_system not in HEX_COORDINATE_SYSTEMS:
            errors.append(
                "GRID_HEX_COORDINATE_SYSTEM_REQUIRED: hex grids require coordinate_system, "
                f"one of {sorted(HEX_COORDINATE_SYSTEMS)}"
            )
        context["orientation"] = orientation

    image_dims = technical.get("image_dimensions_px")
    if image_dims is not None:
        if (
            not isinstance(image_dims, list)
            or len(image_dims) != 2
            or not all(_positive_int(value) for value in image_dims)
        ):
            errors.append("GRID_IMAGE_DIMENSIONS_INVALID: image_dimensions_px must be [width_px, height_px]")
        elif grid_type == "square" and width and height:
            px_w, px_h = image_dims
            if px_w % width != 0 or px_h % height != 0:
                errors.append("GRID_NON_INTEGER_PIXELS_PER_CELL: image dimensions must divide evenly by grid cells")
            elif px_w // width != px_h // height:
                errors.append("GRID_DISTORTED: pixels per cell differ across axes")
            else:
                context["pixels_per_cell"] = px_w // width

    return context


def _validate_scale_bar(scale_context, grid_context, errors):
    technical = grid_context.get("technical")
    if technical is None:
        return
    scale_bar = technical.get("scale_bar")
    if not isinstance(scale_bar, dict):
        errors.append("SCALE_BAR_MISSING: technical.scale_bar is required on overview maps")
        return

    length_cells = scale_bar.get("length_cells")
    if not _positive_int(length_cells):
        errors.append("SCALE_BAR_INVALID: scale_bar.length_cells must be a positive integer")
        return
    width_cells = grid_context.get("width_cells")
    if width_cells and length_cells > width_cells:
        errors.append("SCALE_BAR_INVALID: scale_bar.length_cells exceeds map width")

    label_units = scale_bar.get("label_units")
    unit_per_cell = scale_context.get("unit_per_cell")
    if label_units is not None and unit_per_cell:
        expected = length_cells * unit_per_cell
        if not _number(label_units) or abs(label_units - expected) > REL_TOL * max(1.0, abs(expected)):
            errors.append(f"SCALE_BAR_MISMATCH: label_units must equal length_cells x unit_per_cell = {expected}")


def _validate_features(spec, grid_context, errors):
    features = spec.get("features", [])
    if not isinstance(features, list):
        errors.append("SPEC_INVALID: features must be a list")
        return

    width_limit = grid_context.get("width_cells")
    height_limit = grid_context.get("height_cells")
    seen = set()
    for feature in features:
        if not isinstance(feature, dict):
            errors.append("FEATURE_INVALID: each feature must be an object")
            continue
        feature_id = feature.get("id")
        if not isinstance(feature_id, str) or feature_id == "":
            errors.append("FEATURE_MISSING_ID: every feature needs a string id")
            continue
        if feature_id in seen:
            errors.append(f"FEATURE_DUPLICATE_ID: {feature_id}")
            continue
        seen.add(feature_id)

        x = feature.get("x")
        y = feature.get("y")
        width = feature.get("width")
        height = feature.get("height")
        if not all(_nonnegative_int(value) for value in (x, y)) or not all(
            _positive_int(value) for value in (width, height)
        ):
            errors.append(
                f"FEATURE_GEOMETRY_INVALID: {feature_id} needs non-negative integer x, y "
                "and positive integer width, height"
            )
            continue
        if width_limit and x + width > width_limit:
            errors.append(f"FEATURE_OUT_OF_BOUNDS: {feature_id} exceeds map width")
        if height_limit and y + height > height_limit:
            errors.append(f"FEATURE_OUT_OF_BOUNDS: {feature_id} exceeds map height")


def _validate_children(spec, scale_context, grid_context, base_dir, errors):
    children = spec.get("children", [])
    if not isinstance(children, list):
        errors.append("SPEC_INVALID: children must be a list")
        return

    parent_rank = scale_context.get("rank")
    parent_unit = scale_context.get("unit")
    unit_per_cell = scale_context.get("unit_per_cell")
    width_limit = grid_context.get("width_cells")
    height_limit = grid_context.get("height_cells")
    seen = set()

    for child in children:
        if not isinstance(child, dict):
            errors.append("CHAIN_CHILD_INVALID: each child must be an object")
            continue
        child_id = child.get("id")
        if not isinstance(child_id, str) or child_id == "":
            errors.append("CHAIN_CHILD_MISSING_ID: every child needs a string id")
            continue
        if child_id in seen:
            errors.append(f"CHAIN_DUPLICATE_CHILD_ID: {child_id}")
            continue
        seen.add(child_id)

        level = child.get("level")
        info = SCALE_LEVELS.get(level)
        if info is None:
            errors.append(f"CHAIN_LEVEL_INVALID: {child_id} level must be one of {sorted(SCALE_LEVELS)}")
        elif parent_rank is not None and info["rank"] >= parent_rank:
            errors.append(f"CHAIN_LEVEL_NOT_LOWER: {child_id} level {level} is not below the parent level")

        footprint = child.get("footprint")
        footprint_ft = None
        if (
            not isinstance(footprint, dict)
            or not _positive_number(footprint.get("width"))
            or not _positive_number(footprint.get("height"))
            or footprint.get("unit") not in FOOTPRINT_UNITS
        ):
            errors.append(
                f"CHAIN_FOOTPRINT_INVALID: {child_id} footprint needs positive width, height and unit ft or miles"
            )
        else:
            footprint_ft = (
                _to_ft(footprint["width"], footprint["unit"]),
                _to_ft(footprint["height"], footprint["unit"]),
            )

        representation = child.get("representation")
        if representation not in {"block", "marker"}:
            errors.append(f"CHAIN_REPRESENTATION_INVALID: {child_id} representation must be block or marker")
            representation = None

        cells = None
        if footprint_ft and unit_per_cell and parent_unit:
            cell_ft = _to_ft(unit_per_cell, parent_unit)
            cells = (footprint_ft[0] / cell_ft, footprint_ft[1] / cell_ft)
            if representation == "block" and cells[0] < 1 and cells[1] < 1:
                errors.append(
                    f"CHAIN_REPRESENTATION_MUST_BE_MARKER: {child_id} footprint is smaller than one cell on both axes"
                )
            if representation == "marker" and (cells[0] >= 1 or cells[1] >= 1):
                errors.append(f"CHAIN_REPRESENTATION_MUST_BE_BLOCK: {child_id} footprint spans at least one cell")

        x = child.get("x")
        y = child.get("y")
        if not _nonnegative_int(x) or not _nonnegative_int(y):
            errors.append(f"CHAIN_POSITION_INVALID: {child_id} x and y must be non-negative integers")
            x = y = None

        if representation == "block":
            block = child.get("block")
            if (
                not isinstance(block, dict)
                or not _positive_int(block.get("width"))
                or not _positive_int(block.get("height"))
            ):
                errors.append(f"CHAIN_BLOCK_INVALID: {child_id} block needs positive integer width and height")
            else:
                if cells:
                    expected = (math.ceil(cells[0] - REL_TOL), math.ceil(cells[1] - REL_TOL))
                    if (block["width"], block["height"]) != expected:
                        errors.append(
                            f"CHAIN_BLOCK_SIZE_MISMATCH: {child_id} block must be {expected[0]}x{expected[1]} "
                            "cells (ceil of footprint / unit_per_cell)"
                        )
                if x is not None and width_limit and x + block["width"] > width_limit:
                    errors.append(f"CHAIN_OUT_OF_BOUNDS: {child_id} block exceeds map width")
                if y is not None and height_limit and y + block["height"] > height_limit:
                    errors.append(f"CHAIN_OUT_OF_BOUNDS: {child_id} block exceeds map height")
        elif representation == "marker":
            if x is not None and width_limit and x >= width_limit:
                errors.append(f"CHAIN_OUT_OF_BOUNDS: {child_id} marker x exceeds map width")
            if y is not None and height_limit and y >= height_limit:
                errors.append(f"CHAIN_OUT_OF_BOUNDS: {child_id} marker y exceeds map height")

        spec_path = child.get("spec_path")
        if spec_path is not None:
            _cross_check_child_spec(child_id, spec_path, level, footprint_ft, base_dir, errors)


def _cross_check_child_spec(child_id, spec_path, declared_level, footprint_ft, base_dir, errors):
    if not isinstance(spec_path, str) or spec_path == "":
        errors.append(f"CHAIN_CHILD_SPEC_INVALID: {child_id} spec_path must be a non-empty string")
        return
    path = spec_path if os.path.isabs(spec_path) else os.path.join(base_dir or ".", spec_path)
    if not os.path.isfile(path):
        errors.append(f"CHAIN_CHILD_SPEC_MISSING: {child_id} spec_path {spec_path} does not exist")
        return
    try:
        with open(path, "r", encoding="utf-8") as handle:
            child_spec = json.load(handle)
    except (OSError, ValueError):
        errors.append(f"CHAIN_CHILD_SPEC_INVALID: {child_id} spec_path {spec_path} is not readable JSON")
        return

    size = _child_spec_size_ft(child_spec)
    if size is None:
        errors.append(f"CHAIN_CHILD_SPEC_INVALID: {child_id} spec_path {spec_path} has no usable grid and scale")
        return
    spec_width_ft, spec_height_ft, spec_level = size

    if declared_level is not None and spec_level != declared_level:
        errors.append(f"CHAIN_LEVEL_MISMATCH: {child_id} declares level {declared_level} but spec is {spec_level}")
    if footprint_ft is not None:
        checks = (
            (footprint_ft[0], spec_width_ft, "width"),
            (footprint_ft[1], spec_height_ft, "height"),
        )
        for declared, actual, axis in checks:
            if abs(declared - actual) > REL_TOL * max(1.0, abs(actual)):
                errors.append(
                    f"CHAIN_FOOTPRINT_MISMATCH: {child_id} {axis} {declared} ft does not match child spec {actual} ft"
                )


def _child_spec_size_ft(child_spec):
    if not isinstance(child_spec, dict):
        return None
    technical = child_spec.get("technical")
    if not isinstance(technical, dict):
        return None

    if child_spec.get("map_kind") == "overview":
        scale = child_spec.get("scale")
        if not isinstance(scale, dict):
            return None
        info = SCALE_LEVELS.get(scale.get("level"))
        unit_per_cell = scale.get("unit_per_cell")
        width = technical.get("width_cells")
        height = technical.get("height_cells")
        if info is None or info["rank"] == 0 or not _positive_number(unit_per_cell):
            return None
        if not _positive_int(width) or not _positive_int(height):
            return None
        return (
            _to_ft(width * unit_per_cell, info["unit"]),
            _to_ft(height * unit_per_cell, info["unit"]),
            scale.get("level"),
        )

    width = technical.get("width_squares")
    height = technical.get("height_squares")
    tile_scale = technical.get("tile_scale_ft")
    if not _positive_int(width) or not _positive_int(height) or not _positive_number(tile_scale):
        return None
    return (width * tile_scale, height * tile_scale, "battlemap")


def _validate_print(grid_context, errors, warnings):
    technical = grid_context.get("technical")
    if technical is None:
        return
    print_spec = technical.get("print", {})
    if not isinstance(print_spec, dict):
        errors.append("PRINT_SPEC_INVALID: print must be an object")
        return
    enabled = print_spec.get("enabled")
    if not isinstance(enabled, bool):
        errors.append("PRINT_ENABLED_INVALID: enabled must be true or false")
        return
    if enabled is not True:
        return

    paper = print_spec.get("paper")
    if not isinstance(paper, str) or paper not in PAPER_SIZES:
        errors.append(f"PRINT_PAPER_INVALID: paper must be one of {sorted(PAPER_SIZES)}")
        return
    physical_cell = print_spec.get("physical_grid_mm")
    if not _positive_number(physical_cell):
        errors.append("PRINT_GRID_INVALID: physical_grid_mm must be positive")
        return
    margin = print_spec.get("margin_mm", 0)
    if not _nonnegative_number(margin):
        errors.append("PRINT_MARGIN_INVALID: margin_mm cannot be negative")
        return
    if margin < 5:
        warnings.append("PRINT_MARGIN_TIGHT: margins below 5 mm may be clipped")
    split_pages = print_spec.get("split_pages")
    if split_pages is not None and not isinstance(split_pages, bool):
        errors.append("PRINT_SPLIT_PAGES_INVALID: split_pages must be true or false")
        return
    dpi = print_spec.get("dpi")
    if dpi is not None and not _positive_number(dpi):
        errors.append("PRINT_DPI_INVALID: dpi must be positive")
        return

    width_cells = grid_context.get("width_cells")
    height_cells = grid_context.get("height_cells")
    if not width_cells or not height_cells:
        return

    if grid_context.get("grid_type") == "hex":
        hex_height = 2 * physical_cell / SQRT3
        map_width = width_cells * physical_cell + 0.5 * physical_cell
        map_height = 0.25 * hex_height + height_cells * 0.75 * hex_height
        if grid_context.get("orientation") in {"flat", "flat-top"}:
            map_width = 0.25 * hex_height + width_cells * 0.75 * hex_height
            map_height = height_cells * physical_cell + 0.5 * physical_cell
    else:
        map_width = width_cells * physical_cell
        map_height = height_cells * physical_cell

    paper_width, paper_height = PAPER_SIZES[paper]
    usable_width = paper_width - margin * 2
    usable_height = paper_height - margin * 2
    fits_portrait = map_width <= usable_width and map_height <= usable_height
    fits_landscape = map_width <= usable_height and map_height <= usable_width
    if not fits_portrait and not fits_landscape and split_pages is not True:
        errors.append("PRINT_REQUIRES_SPLIT: map exceeds single-page usable area without split_pages")
    elif (fits_portrait or fits_landscape) and usable_width > 0 and usable_height > 0:
        coverage = (map_width * map_height) / (usable_width * usable_height)
        if coverage < 0.5:
            warnings.append(
                f"PRINT_UNDERFILL: map fills only {round(coverage * 100)}% of the usable page; "
                "increase the grid or reduce paper size to reach the page edges"
            )

    pixels_per_cell = grid_context.get("pixels_per_cell")
    if dpi is not None and pixels_per_cell:
        expected = physical_cell / MM_PER_INCH * dpi
        if expected > 0 and abs(pixels_per_cell - expected) / expected > 0.02:
            actual_mm = pixels_per_cell / dpi * MM_PER_INCH
            warnings.append(
                f"PRINT_DPI_MISMATCH: {pixels_per_cell} px/cell at {dpi} DPI prints "
                f"{actual_mm:.1f} mm cells, not {physical_cell} mm; use {round(expected)} px/cell"
            )


def main(argv=None):
    parser = argparse.ArgumentParser(description="Validate an overview map JSON spec.")
    parser.add_argument("spec", help="Path to an overview spec JSON file")
    args = parser.parse_args(argv)

    with open(args.spec, "r", encoding="utf-8") as handle:
        spec = json.load(handle)

    report = validate_spec(spec, base_dir=os.path.dirname(os.path.abspath(args.spec)))
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 2: Run the test suite, expect all tests to pass**

Run: `.venv/bin/python skills/dnd-map-architect/tests/test_validate_overview_spec.py`
Expected: `OK` with 35 tests.

- [ ] **Step 3: Confirm no regression and compile both files**

Run: `.venv/bin/python skills/dnd-map-architect/tests/test_validate_dungeon_spec.py`
Expected: `OK`.
Run: `.venv/bin/python -m py_compile skills/dnd-map-architect/scripts/validate_overview_spec.py skills/dnd-map-architect/tests/test_validate_overview_spec.py`
Expected: exit 0, no output.

- [ ] **Step 4: Commit**

```bash
git add skills/dnd-map-architect/scripts/validate_overview_spec.py skills/dnd-map-architect/tests/test_validate_overview_spec.py
git commit -m "Add overview spec validator with scale chain checks

Validates scale level and unit range, square and hex grids, scale bar
math, feature bounds, child block/marker representation with ceil
footprint math, child spec cross-checks, and print fit including hex
paper-fit formulas."
```

---

### Task 4: Bundled overview example spec

**Files:**
- Create: `skills/dnd-map-architect/examples/valid-overview-spec.json`

- [ ] **Step 1: Create the file with exactly this content**

```json
{
  "map_kind": "overview",
  "identity": {
    "name": "Ember Archive Site Plan",
    "overview_type": "dungeon complex"
  },
  "scale": {"level": "site", "unit_per_cell": 10},
  "technical": {
    "grid_type": "square",
    "width_cells": 14,
    "height_cells": 10,
    "image_dimensions_px": [1400, 1000],
    "scale_bar": {"length_cells": 5, "label_units": 50},
    "print": {
      "enabled": true,
      "paper": "A3",
      "physical_grid_mm": 28,
      "margin_mm": 6,
      "split_pages": false
    }
  },
  "features": [
    {"id": "approach", "name": "Approach Road", "kind": "route", "x": 0, "y": 9, "width": 14, "height": 1}
  ],
  "children": [
    {
      "id": "ember-archive",
      "name": "Ember Archive",
      "level": "battlemap",
      "representation": "block",
      "x": 1,
      "y": 0,
      "footprint": {"width": 120, "height": 90, "unit": "ft"},
      "block": {"width": 12, "height": 9},
      "spec_path": "valid-dungeon-spec.json"
    }
  ]
}
```

- [ ] **Step 2: Validate the example end to end (exercises the spec_path cross-check against the bundled battlemap example)**

Run: `.venv/bin/python skills/dnd-map-architect/scripts/validate_overview_spec.py skills/dnd-map-architect/examples/valid-overview-spec.json`
Expected: exit 0; JSON report with `"ok": true`, `"errors": []`.

- [ ] **Step 3: Commit**

```bash
git add skills/dnd-map-architect/examples/valid-overview-spec.json
git commit -m "Add bundled overview example chained to battlemap example

Site-level overview of the Ember Archive: 14x10 cells at 10 ft per
square, A3 print block, and a 12x9 child block cross-checked against
examples/valid-dungeon-spec.json."
```

---

### Task 5: Site overview scale reference

**Files:**
- Create: `skills/dnd-map-architect/references/overview-site.md`

- [ ] **Step 1: Create the file with exactly this content**

````markdown
# Site Overview (Level 1)

Zoom-out scheme of one whole dungeon complex, building, fortress, temple, or
lair. 10-50 ft per square (default 10 ft), square grid. Read
`overview-rules.md` first; it defines the scale ladder, scale chain, scale
bar, and print math used here.

## Intake Questions

Required:

- What is the site (dungeon, fortress, manor, temple, cave system)?
- Which floor or level does this sheet show? One overview map per floor;
  stairs and shafts are cross-floor markers.
- What real-world footprint does the site cover, or which battlemaps compose it?
- Audience: DM version (secrets visible) or player version (secrets hidden)?

Adaptive (ask only when relevant):

- Which existing battlemap specs should embed as children (file paths)?
- What named wings or zones exist, and roughly where do they sit?
- Where are the entrances, and which connections matter (corridors, stairs,
  bridges, underground passages)?
- Should one edge show exterior context (approach road, cliff, surrounding
  settlement)?

## Spec Notes

- `scale.level`: `"site"`; `unit_per_cell` 10-50 ft.
- Children are battlemaps only; they are almost always blocks. Cross-check
  each with `spec_path`.
- Features: wings, courtyards, routes, and entrances as rectangles; stairs
  and secret passages as 1-cell features with a `kind`.

## Prompt Template

```text
Create a strict top-down orthographic site overview scheme (an architectural
plan, not a battlemap).

Coordinate grid (most important):
- Columns labeled 0-{width_cells - 1} along the top edge
- Rows labeled 0-{height_cells - 1} along the left edge
- Exactly {width_cells} columns and {height_cells} rows of equal squares
- Dark grid lines drawn above all art, blocks, shadows, and labels

Scale (must stay accurate):
- {unit_per_cell} ft per square
- Scale bar spanning exactly {scale_bar_length_cells} squares, labeled
  "{scale_bar_length_cells x unit_per_cell} ft"
- Print: {paper}, {physical_grid_mm} mm per square inside {margin_mm} mm
  margins, {dpi} DPI (omit this line when print is disabled)

Site identity:
- Name: {name}; type: {overview_type}; atmosphere: {atmosphere}

Layout (source of truth):
- {each child block: "{name}: rows {y}-{y + height - 1}, columns {x}-{x + width - 1}"}
- {each feature: wings, routes, entrances, stairs with exact rows/columns}
- {short label on every block and marker}

Rendering requirements:
- Simplified architectural blocks with wall outlines, no interior furniture
- Routes and connections drawn as clear corridors or dashed paths
- Entrances marked with arrows; stairs with standard stair glyphs
- Light parchment scheme style; art never obscures grid lines or labels
```

## Negative Constraints

```text
Negative constraints (strict):
- No isometric view, perspective angle, or 3D camera
- No extra rows or columns beyond {width_cells} x {height_cells}
- No furniture, room interiors, creatures, tokens, monsters, or NPCs
- No hidden, cropped, faded, or missing grid cells
- No decorative border that changes the mapped area
- No grid lines obscured by art, blocks, shadows, or labels
- No scale bar shorter or longer than {scale_bar_length_cells} grid cells
- Player version only: no secret rooms or hidden passages rendered
```

## Post-Generation Checklist

1. Numbered columns and rows are visible with exact counts.
2. Count cells on both axes; they must match the spec.
3. The scale bar spans exactly `length_cells` cells and its label equals
   `length_cells x unit_per_cell` ft.
4. Every child block sits at its declared rows/columns at the declared size.
5. Entrances, stairs, and routes appear where the spec places them.
6. No interior furniture or tactical detail leaked in.
7. Player version: secrets are absent.
8. Print: a measured cell equals `physical_grid_mm`; the scale bar measures
   `length_cells x physical_grid_mm`.
````

- [ ] **Step 2: Commit**

```bash
git add skills/dnd-map-architect/references/overview-site.md
git commit -m "Add site overview scale reference

Intake questions, spec notes, prompt template, negative constraints,
and post-generation checklist for level-1 dungeon/site overview maps."
```

---

### Task 6: Settlement overview scale reference

**Files:**
- Create: `skills/dnd-map-architect/references/overview-settlement.md`

- [ ] **Step 1: Create the file with exactly this content**

````markdown
# Settlement Overview (Level 2)

Zoom-out scheme of a village, town, or city. 50-500 ft per square (default
100 ft), square grid. Read `overview-rules.md` first.

## Intake Questions

Required:

- What settlement is this (village, town, city), and roughly how large
  (population or extent in ft/miles)?
- What are the major districts or quarters?
- Walls and gates: is the settlement walled, and where are the gates?
- Audience: DM version or player version?

Adaptive (ask only when relevant):

- Water: river, harbor, coast, canals - where do they run?
- Which roads matter (gate-to-gate arteries, market squares, docks)?
- Which landmarks deserve labeled callouts (keep, temple, market, guildhall)?
- Which site maps (dungeons, keeps, manors) should embed as children, and do
  their spec files exist?

## Spec Notes

- `scale.level`: `"settlement"`; `unit_per_cell` 50-500 ft.
- Children are site maps (or battlemaps); most render as blocks at 50-100 ft
  per cell and as markers at coarser scales. Apply the block/marker rule from
  `overview-rules.md`.
- Features: districts, walls, gates, water, roads, and squares as rectangles
  with a `kind`.

## Prompt Template

```text
Create a strict top-down city-plan scheme of {name}, a {overview_type}.

Coordinate grid (most important):
- Columns labeled 0-{width_cells - 1} along the top edge
- Rows labeled 0-{height_cells - 1} along the left edge
- Exactly {width_cells} columns and {height_cells} rows of equal squares
- Dark grid lines drawn above all art and labels

Scale (must stay accurate):
- {unit_per_cell} ft per square
- Scale bar spanning exactly {scale_bar_length_cells} squares, labeled
  "{scale_bar_length_cells x unit_per_cell} ft"
- Print: {paper}, {physical_grid_mm} mm per square inside {margin_mm} mm
  margins, {dpi} DPI (omit this line when print is disabled)

Layout (source of truth):
- {each district block with exact rows/columns}
- {walls and gates with exact cells}
- {water cells: river, harbor, coast}
- {roads as routes between gates, squares, and districts}
- {each child site as a block or labeled marker at exact cells}
- {landmark callouts with short labels}

Rendering requirements:
- District blocks with rooftop-texture fill, no individual building interiors
- Walls as bold outlines with clear gate gaps
- Roads clearly readable between blocks; water clearly distinct from land
- Light parchment cartographic style; labels short and legible
```

## Negative Constraints

```text
Negative constraints (strict):
- No isometric view, perspective angle, or 3D camera
- No extra rows or columns beyond {width_cells} x {height_cells}
- No people, creatures, carts, armies, or building interiors
- No hidden, cropped, faded, or missing grid cells
- No decorative border that changes the mapped area
- No grid lines obscured by art, rooftops, water, or labels
- No scale bar shorter or longer than {scale_bar_length_cells} grid cells
- Player version only: no hidden or secret locations rendered
```

## Post-Generation Checklist

1. Numbered columns and rows are visible with exact counts.
2. Count cells on both axes; they must match the spec.
3. The scale bar spans exactly `length_cells` cells and its label equals
   `length_cells x unit_per_cell` ft.
4. Districts, walls, gates, water, and roads sit where the spec places them.
5. Every child site block or marker sits at its declared cells.
6. Landmark labels are legible and match the spec names.
7. Print: a measured cell equals `physical_grid_mm`; the scale bar measures
   true.
````

- [ ] **Step 2: Commit**

```bash
git add skills/dnd-map-architect/references/overview-settlement.md
git commit -m "Add settlement overview scale reference

Intake questions, spec notes, prompt template, negative constraints,
and post-generation checklist for level-2 settlement maps."
```

---

### Task 7: Region overview scale reference

**Files:**
- Create: `skills/dnd-map-architect/references/overview-region.md`

- [ ] **Step 1: Create the file with exactly this content**

````markdown
# Region Overview (Level 3)

Hex-crawl scheme of a province, march, or wilderness region. 1-10 miles per
hex (default 6 miles), pointy-top hexes with offset coordinates by default
(square grid allowed). Read `overview-rules.md` first.

## Intake Questions

Required:

- What region is this, and what does it border?
- What is the dominant terrain mix (forest, hills, mountains, swamp, plains,
  coast)?
- Which settlements and sites must appear, and where roughly?
- How many miles per hex (or what total extent must fit the sheet)?

Adaptive (ask only when relevant):

- Roads and rivers: which routes connect the settlements?
- Political borders: whose territory, and do borders need to be visible?
- Should hexes carry travel annotations (for example one hex = one day on
  foot at 6 miles per hex)?
- Which child maps (settlements, sites) have spec files to chain?

## Spec Notes

- `scale.level`: `"region"`; `unit_per_cell` 1-10 miles; `grid_type` hex with
  `orientation` and `coordinate_system`, or square.
- Children: settlements and sites. At miles per hex nearly all are markers;
  a sprawling city may be a block (apply the rule from `overview-rules.md`).
- Features: terrain areas, rivers, roads, and borders as rectangles or
  cell-run routes with a `kind`.
- A3 landscape at 28 mm flat-to-flat pointy hexes fits 14 x 11 hexes (see
  the worked example in `overview-rules.md`).

## Prompt Template

```text
Create a top-down regional hex map of {name}, a {overview_type}.

Hex grid (most important):
- Pointy-top hexes in offset rows
- Columns labeled 0-{width_cells - 1} along the top edge
- Rows labeled 0-{height_cells - 1} along the left edge
- Exactly {width_cells} columns and {height_cells} rows of equal hexes
- Dark hex outlines drawn above all terrain art

Scale (must stay accurate):
- {unit_per_cell} miles per hex
- Scale bar spanning exactly {scale_bar_length_cells} hexes, labeled
  "{scale_bar_length_cells x unit_per_cell} miles"
- Print: {paper}, {physical_grid_mm} mm flat-to-flat per hex inside
  {margin_mm} mm margins, {dpi} DPI (omit this line when print is disabled)

Layout (source of truth):
- {terrain per area: forest, hills, mountains, swamp, plains with hex ranges}
- {rivers and roads as hex-to-hex routes}
- {political borders as dashed lines along hex edges}
- {each child settlement or site as a block or keyed marker at exact hexes}
- {short labels on settlements, sites, and major terrain}

Rendering requirements:
- Classic hex-crawl cartography: one dominant terrain symbol per hex
- Settlement icons sized by type (village, town, city); sites as keyed symbols
- Rivers, roads, and borders readable above terrain, below hex outlines and
  labels
```

## Negative Constraints

```text
Negative constraints (strict):
- No isometric view, perspective angle, or 3D camera
- No extra hex columns or rows beyond {width_cells} x {height_cells}
- No armies, creatures, monsters, or battle scenes
- No hidden, cropped, faded, or missing hexes
- No decorative border that changes the mapped area
- No hex outlines obscured by terrain art or labels
- No scale bar shorter or longer than {scale_bar_length_cells} hexes
```

## Post-Generation Checklist

1. Numbered hex columns and rows are visible with exact counts.
2. Count hexes on both axes; they must match the spec.
3. The scale bar spans exactly `length_cells` hexes and its label equals
   `length_cells x unit_per_cell` miles.
4. Terrain areas, rivers, roads, and borders sit where the spec places them.
5. Every settlement and site marker or block sits at its declared hex.
6. Hex outlines are continuous across the whole map.
7. Print: a measured hex equals `physical_grid_mm` flat-to-flat; the scale
   bar measures true.
````

- [ ] **Step 2: Commit**

```bash
git add skills/dnd-map-architect/references/overview-region.md
git commit -m "Add region overview scale reference

Intake questions, spec notes, hex prompt template, negative
constraints, and post-generation checklist for level-3 region maps."
```

---

### Task 8: World overview scale reference

**Files:**
- Create: `skills/dnd-map-architect/references/overview-world.md`

- [ ] **Step 1: Create the file with exactly this content**

````markdown
# World Overview (Level 4)

Atlas-style scheme of a continent or the known world. 25-100 miles per hex
(default 50 miles), pointy-top hexes with offset coordinates by default
(square grid allowed). Read `overview-rules.md` first.

## Intake Questions

Required:

- What does the sheet cover: one continent, several, or the known world?
- Which kingdoms or realms must appear, and which borders matter?
- What are the defining physical features (coastlines, mountain ranges,
  great rivers, seas)?
- How many miles per hex (or what total extent must fit the sheet)?

Adaptive (ask only when relevant):

- Capitals and major cities: which deserve markers and labels?
- Climate bands or biomes: should the map show them (tundra, desert, jungle)?
- Sea routes or trade lanes between ports?
- Which child region maps have spec files to chain?

## Spec Notes

- `scale.level`: `"world"`; `unit_per_cell` 25-100 miles; `grid_type` hex
  with `orientation` and `coordinate_system`, or square.
- Children: regions (blocks when they span hexes) and settlements (markers;
  even a large city is far below one 50-mile hex).
- Features: landmasses, seas, mountain ranges, rivers, kingdom borders, and
  climate bands as rectangles or cell-run routes with a `kind`.

## Prompt Template

```text
Create a top-down atlas hex map of {name}, a {overview_type}.

Hex grid (most important):
- Pointy-top hexes in offset rows
- Columns labeled 0-{width_cells - 1} along the top edge
- Rows labeled 0-{height_cells - 1} along the left edge
- Exactly {width_cells} columns and {height_cells} rows of equal hexes
- Dark hex outlines drawn above all terrain art

Scale (must stay accurate):
- {unit_per_cell} miles per hex
- Scale bar spanning exactly {scale_bar_length_cells} hexes, labeled
  "{scale_bar_length_cells x unit_per_cell} miles"
- Print: {paper}, {physical_grid_mm} mm flat-to-flat per hex inside
  {margin_mm} mm margins, {dpi} DPI (omit this line when print is disabled)

Layout (source of truth):
- {coastlines and seas with hex ranges}
- {mountain ranges, great rivers, deserts, forests with hex ranges}
- {kingdom borders as dashed lines along hex edges}
- {each child region as a block and each capital or major city as a keyed
  marker at exact hexes}
- {label hierarchy: realms largest, regions medium, cities smallest}

Rendering requirements:
- Atlas cartography: muted terrain fills, clear coastlines, elegant labels
- Capitals as distinct star or keep icons; other cities as smaller dots
- Borders, rivers, and routes readable above terrain, below hex outlines and
  labels
```

## Negative Constraints

```text
Negative constraints (strict):
- No isometric view, perspective angle, or 3D camera
- No extra hex columns or rows beyond {width_cells} x {height_cells}
- No armies, creatures, monsters, ships in battle, or scene illustrations
- No hidden, cropped, faded, or missing hexes
- No decorative border that changes the mapped area
- No hex outlines obscured by terrain art or labels
- No scale bar shorter or longer than {scale_bar_length_cells} hexes
```

## Post-Generation Checklist

1. Numbered hex columns and rows are visible with exact counts.
2. Count hexes on both axes; they must match the spec.
3. The scale bar spans exactly `length_cells` hexes and its label equals
   `length_cells x unit_per_cell` miles.
4. Coastlines, ranges, rivers, and borders sit where the spec places them.
5. Every region block and city marker sits at its declared hex.
6. The label hierarchy reads correctly (realm over region over city).
7. Print: a measured hex equals `physical_grid_mm` flat-to-flat; the scale
   bar measures true.
````

- [ ] **Step 2: Commit**

```bash
git add skills/dnd-map-architect/references/overview-world.md
git commit -m "Add world overview scale reference

Intake questions, spec notes, atlas prompt template, negative
constraints, and post-generation checklist for level-4 world maps."
```

---

### Task 9: Wire overview mode into SKILL.md, packaging, and commands

**Files:**
- Modify: `skills/dnd-map-architect/SKILL.md`
- Modify: `skills/dnd-map-architect/agents/openai.yaml`
- Modify: `AGENTS.md` (section 10 commands only; `CLAUDE.md`/`GEMINI.md` are symlinks)

- [ ] **Step 1: Update the SKILL.md frontmatter description**

Replace the `description:` line with:

```yaml
description: Use when designing a dungeon, cave, fortress, lair, encounter map, printable battlemap, VTT map, terrain-module layout, overview or zoom-out map of a dungeon complex, city, settlement, region, or world, or an image-generation prompt for tabletop RPG maps.
```

- [ ] **Step 2: Add a Map Modes section directly after the intro paragraph (before "## Required Workflow")**

```markdown
## Map Modes

- **Battlemap mode** (tactical encounter maps): follow the Required Workflow below.
- **Overview mode** (zoom-out schemes: whole dungeon or site, settlement, region, world): read `references/overview-rules.md` plus exactly one scale file (`overview-site.md`, `overview-settlement.md`, `overview-region.md`, `overview-world.md`), then follow the Overview Workflow.
```

- [ ] **Step 3: Add an Overview Workflow section directly after "## Required Workflow"**

```markdown
## Overview Workflow

1. **Overview intake**: Pick the scale level from the ladder in `references/overview-rules.md`; ask the scale file's intake questions.
2. **JSON overview specification**: Build a spec matching the shape in `references/overview-rules.md`: scale, grid, scale bar, print target, features, and children with real-world footprints.
3. **Composition pass**: Place features and child blocks or markers; verify the scale chain math (block = ceil of footprint / unit_per_cell, marker when smaller than one cell).
4. **Validation pass**: Run `scripts/validate_overview_spec.py` against the spec. Treat errors as blockers, exactly as in battlemap mode.
5. **Image prompt generation**: Use the scale file's prompt template only when validation passes; otherwise output blocker corrections.
6. **Image generation, post-generation validation, correction loop**: Follow battlemap mode steps 7-9 using the scale file's post-generation checklist.
```

- [ ] **Step 4: Append the new references to the Reference Map list**

```markdown
- `references/overview-rules.md`: Scale ladder, scale chain, scale bar, and print math shared by all overview maps.
- `references/overview-site.md`: Site (dungeon complex) overview intake and prompts.
- `references/overview-settlement.md`: Settlement overview intake and prompts.
- `references/overview-region.md`: Region hex-map intake and prompts.
- `references/overview-world.md`: World atlas intake and prompts.
- `examples/valid-overview-spec.json`: Valid overview spec accepted by the bundled overview validator.
```

- [ ] **Step 5: Extend the Validator section with the overview command (after the existing command block)**

```markdown
For overview (zoom-out) specs, run the overview validator the same way:

​```bash
.venv/bin/python skills/dnd-map-architect/scripts/validate_overview_spec.py skills/dnd-map-architect/examples/valid-overview-spec.json
​```
```

(Remove the zero-width characters around the inner backticks when editing; they only keep this plan's fencing intact.)

- [ ] **Step 6: Update `skills/dnd-map-architect/agents/openai.yaml`**

```yaml
interface:
  display_name: "DND Map Architect"
  short_description: "Design validated D&D battlemaps and scale-accurate overview maps"
  default_prompt: "Use $dnd-map-architect to design a tactically playable, grid-consistent D&D battlemap for my encounter."
```

- [ ] **Step 7: Update AGENTS.md section 10 Commands**

Replace the existing test/validate/lint lines with:

```markdown
- Test skill validators: `.venv/bin/python skills/dnd-map-architect/tests/test_validate_dungeon_spec.py` and `.venv/bin/python skills/dnd-map-architect/tests/test_validate_overview_spec.py`
- Validate bundled examples: `.venv/bin/python skills/dnd-map-architect/scripts/validate_dungeon_spec.py skills/dnd-map-architect/examples/valid-dungeon-spec.json` and `.venv/bin/python skills/dnd-map-architect/scripts/validate_overview_spec.py skills/dnd-map-architect/examples/valid-overview-spec.json`
- Lint/typecheck: `.venv/bin/python -m py_compile skills/dnd-map-architect/scripts/validate_dungeon_spec.py skills/dnd-map-architect/scripts/validate_overview_spec.py skills/dnd-map-architect/tests/test_validate_dungeon_spec.py skills/dnd-map-architect/tests/test_validate_overview_spec.py`
```

- [ ] **Step 8: Commit**

```bash
git add skills/dnd-map-architect/SKILL.md skills/dnd-map-architect/agents/openai.yaml AGENTS.md
git commit -m "Wire overview mode into skill routing and project commands

SKILL.md gains overview trigger wording, a Map Modes routing rule, the
Overview Workflow, reference map entries, and the overview validator
command; openai.yaml and AGENTS.md section 10 follow."
```

---

### Task 10: Final verification, artifact closure, and PR

**Files:**
- Rename: `docs/agents/features/PLANNED-overview-maps.md` -> `docs/agents/features/EXECUTED-overview-maps.md`
- Rename: `docs/agents/features/PLANNED-overview-maps-plan.md` -> `docs/agents/features/EXECUTED-overview-maps-plan.md`

- [ ] **Step 1: Run the full verification suite**

```bash
.venv/bin/python skills/dnd-map-architect/tests/test_validate_dungeon_spec.py
.venv/bin/python skills/dnd-map-architect/tests/test_validate_overview_spec.py
.venv/bin/python skills/dnd-map-architect/scripts/validate_dungeon_spec.py skills/dnd-map-architect/examples/valid-dungeon-spec.json
.venv/bin/python skills/dnd-map-architect/scripts/validate_overview_spec.py skills/dnd-map-architect/examples/valid-overview-spec.json
.venv/bin/python -m py_compile skills/dnd-map-architect/scripts/validate_dungeon_spec.py skills/dnd-map-architect/scripts/validate_overview_spec.py skills/dnd-map-architect/tests/test_validate_dungeon_spec.py skills/dnd-map-architect/tests/test_validate_overview_spec.py
```

Expected: both test suites `OK`, both validators exit 0 with `"ok": true`, py_compile silent.

- [ ] **Step 2: Close out both artifacts per docs/AGENTS.md**

Rename both `PLANNED-*` files to `EXECUTED-*` with `git mv`, set their
`Status:` lines to `executed`, and append to each:

```markdown
## Outcome

Implemented as planned. (State "Implemented with changes" plus a summary if
anything diverged.) Doc Review Criteria checked for SKILL.md and the new
references: terminology consistent, examples runnable, no secrets or local
paths; backend/API and security dimensions not applicable to these docs.

## Current Accuracy

Accurate as of execution; the shipped code and references are the source of
truth.
```

- [ ] **Step 3: Commit closure, push, and open the PR**

```bash
git add -A docs/agents/features
git commit -m "Close out overview maps design and plan artifacts as executed"
git push -u origin feat/overview-map-scales
gh pr create --title "Add overview (zoom-out) map mode with accurate scale chain" --body "..."
```

PR body: summarize the scale ladder, scale chain validation, new references,
validator and tests, and the verification commands run. End the body with the
project's standard generated-with line if required by reviewers.

## Outcome

Implemented with changes. All ten tasks executed on `feat/overview-map-scales`
in plan order with per-task commits. Divergence from the written plan: the
final test count is 38, not 35 - after the validator code review, a follow-up
commit added tests for the flat-top hex print path, marker out-of-bounds, and
duplicate child ids. No other deviations; file contents otherwise match the
plan's embedded sources.

## Current Accuracy

Accurate as of execution, including the test-count divergence noted above. The
shipped implementation is the source of truth.
