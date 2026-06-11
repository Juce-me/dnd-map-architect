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
