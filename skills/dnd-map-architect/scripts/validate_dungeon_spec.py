#!/usr/bin/env python3
"""Validate structured DND battlemap specs for topology, tactics, grid, and print."""

import argparse
import json
import sys
from collections import defaultdict, deque


SIZE_FOOTPRINTS = {
    "tiny": 1,
    "small": 1,
    "medium": 1,
    "large": 2,
    "huge": 3,
    "gargantuan": 4,
}

GRID_TYPES = {"square", "hex"}
HEX_ORIENTATIONS = {"pointy", "pointy-top", "flat", "flat-top"}
HEX_COORDINATE_SYSTEMS = {"axial", "offset"}
PAPER_SIZES = {
    "A4": (8.27, 11.69),
    "A3": (11.69, 16.54),
    "Letter": (8.5, 11.0),
    "Ledger": (11.0, 17.0),
}


def validate_spec(spec):
    errors = []
    warnings = []

    if not isinstance(spec, dict):
        return {"ok": False, "errors": ["SPEC_INVALID: root must be an object"], "warnings": []}

    identity = _dict(spec, "identity", errors)
    technical = _dict(spec, "technical", errors)
    tactical = _dict(spec, "tactical", errors)
    rooms = _list(spec, "rooms", errors)
    corridors = _list(spec, "corridors", errors)
    encounters = spec.get("encounters", [])
    if not isinstance(encounters, list):
        errors.append("SPEC_INVALID: encounters must be a list")
        encounters = []

    if identity is not None:
        _require_string(identity, "name", "IDENTITY_MISSING_NAME", "IDENTITY_NAME_INVALID", errors)
        _require_string(
            identity,
            "dungeon_type",
            "IDENTITY_MISSING_DUNGEON_TYPE",
            "IDENTITY_DUNGEON_TYPE_INVALID",
            errors,
        )

    technical_context = _validate_technical(technical, errors, warnings) if technical is not None else {}
    room_index = _validate_rooms(rooms, technical_context, errors) if rooms is not None else {}
    _validate_corridors(corridors or [], room_index, technical_context, errors)
    _validate_connectivity(room_index, corridors or [], errors)
    _validate_tactics(tactical, room_index, corridors or [], encounters, errors, warnings)
    _validate_print(technical, technical_context, errors, warnings)

    return {"ok": not errors, "errors": errors, "warnings": warnings}


def _dict(parent, key, errors):
    value = parent.get(key)
    if not isinstance(value, dict):
        errors.append(f"SPEC_MISSING: {key} must be an object")
        return None
    return value


def _list(parent, key, errors):
    value = parent.get(key)
    if not isinstance(value, list):
        errors.append(f"SPEC_MISSING: {key} must be a list")
        return None
    return value


def _require_string(parent, key, missing_code, invalid_code, errors):
    value = parent.get(key)
    if value in (None, ""):
        errors.append(f"{missing_code}: {key} is required")
    elif not isinstance(value, str):
        errors.append(f"{invalid_code}: {key} must be a non-empty string")


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


def _valid_id(value):
    return isinstance(value, str) and value != ""


def _validate_technical(technical, errors, warnings):
    context = {}
    grid_type = technical.get("grid_type")
    if not isinstance(grid_type, str) or grid_type not in GRID_TYPES:
        errors.append(f"GRID_TYPE_INVALID: grid_type must be one of {sorted(GRID_TYPES)}")
    context["grid_type"] = grid_type

    width = technical.get("width_squares")
    height = technical.get("height_squares")
    if not _positive_int(width):
        errors.append("GRID_WIDTH_INVALID: width_squares must be a positive integer")
    if not _positive_int(height):
        errors.append("GRID_HEIGHT_INVALID: height_squares must be a positive integer")
    context["width_squares"] = width if _positive_int(width) else None
    context["height_squares"] = height if _positive_int(height) else None

    tile_scale = technical.get("tile_scale_ft")
    if not _positive_number(tile_scale):
        errors.append("GRID_SCALE_INVALID: tile_scale_ft must be positive")

    if grid_type == "hex":
        orientation = technical.get("orientation")
        coordinate_system = technical.get("coordinate_system")
        if not orientation:
            errors.append("GRID_HEX_ORIENTATION_REQUIRED: hex grids require orientation")
        elif not isinstance(orientation, str) or orientation not in HEX_ORIENTATIONS:
            errors.append(f"GRID_HEX_ORIENTATION_INVALID: orientation must be one of {sorted(HEX_ORIENTATIONS)}")
        if not coordinate_system:
            errors.append("GRID_HEX_COORDINATE_SYSTEM_REQUIRED: hex grids require coordinate_system")
        elif not isinstance(coordinate_system, str) or coordinate_system not in HEX_COORDINATE_SYSTEMS:
            errors.append(
                f"GRID_HEX_COORDINATE_SYSTEM_INVALID: coordinate_system must be one of {sorted(HEX_COORDINATE_SYSTEMS)}"
            )

    image_dims = technical.get("image_dimensions_px")
    if image_dims is not None:
        if (
            not isinstance(image_dims, list)
            or len(image_dims) != 2
            or not all(_positive_int(value) for value in image_dims)
        ):
            errors.append("GRID_IMAGE_DIMENSIONS_INVALID: image_dimensions_px must be [width_px, height_px]")
        elif context["width_squares"] and context["height_squares"] and grid_type == "square":
            width = context["width_squares"]
            height = context["height_squares"]
            px_w, px_h = image_dims
            if px_w % width != 0 or px_h % height != 0:
                errors.append("GRID_NON_INTEGER_PIXELS_PER_SQUARE: image dimensions must divide evenly by grid squares")
            else:
                x_pps = px_w // width
                y_pps = px_h // height
                if x_pps != y_pps:
                    errors.append("GRID_DISTORTED: pixels per square differ across axes")
                else:
                    context["pixels_per_square"] = x_pps
                    if x_pps < 50:
                        warnings.append("VTT_LOW_RESOLUTION: pixels per square below 50 may look soft")
                    if x_pps > 200:
                        warnings.append("VTT_HIGH_RESOLUTION: pixels per square above 200 may create large files")

    return context


def _validate_rooms(rooms, technical_context, errors):
    room_index = {}
    width_limit = technical_context.get("width_squares")
    height_limit = technical_context.get("height_squares")

    for room in rooms:
        if not isinstance(room, dict):
            errors.append("STRUCTURE_ROOM_INVALID: each room must be an object")
            continue

        room_id = room.get("id")
        if room_id in (None, ""):
            errors.append("STRUCTURE_ROOM_MISSING_ID: every room needs an id")
            continue
        if not _valid_id(room_id):
            errors.append("STRUCTURE_ROOM_ID_INVALID: every room id must be a non-empty string")
            continue
        if room_id in room_index:
            errors.append(f"STRUCTURE_DUPLICATE_ROOM_ID: {room_id}")
            continue
        room_index[room_id] = room

        for key in ("x", "y", "width", "height"):
            if not _nonnegative_int(room.get(key)):
                errors.append(f"STRUCTURE_ROOM_GEOMETRY_INVALID: {room_id}.{key} must be a non-negative integer")

        x = room.get("x")
        y = room.get("y")
        room_width = room.get("width")
        room_height = room.get("height")
        if all(_nonnegative_int(value) for value in (x, y, room_width, room_height)):
            if room_width <= 0 or room_height <= 0:
                errors.append(f"STRUCTURE_ROOM_GEOMETRY_INVALID: {room_id} dimensions must be positive")
            if width_limit and x + room_width > width_limit:
                errors.append(f"STRUCTURE_ROOM_OUT_OF_BOUNDS: {room_id} exceeds map width")
            if height_limit and y + room_height > height_limit:
                errors.append(f"STRUCTURE_ROOM_OUT_OF_BOUNDS: {room_id} exceeds map height")
            if room_width > 0 and room_height > 0:
                for other_id, other_room in room_index.items():
                    if other_id == room_id and other_room is room:
                        continue
                    if _rooms_overlap(room, other_room):
                        errors.append(f"STRUCTURE_ROOM_OVERLAP: {other_id} overlaps {room_id}")

        doors = room.get("doors", [])
        if not isinstance(doors, list):
            errors.append(f"STRUCTURE_DOORS_INVALID: {room_id} doors must be a list")
            doors = []
        for door in doors:
            if not isinstance(door, dict):
                errors.append(f"STRUCTURE_DOOR_INVALID: {room_id} door must be an object")
                continue
            if not door.get("to") and not door.get("corridor_id"):
                errors.append(f"STRUCTURE_DOOR_TARGET_MISSING: {room_id} door needs to or corridor_id")

    return room_index


def _rooms_overlap(first, second):
    first_values = (first.get("x"), first.get("y"), first.get("width"), first.get("height"))
    second_values = (second.get("x"), second.get("y"), second.get("width"), second.get("height"))
    if not all(_nonnegative_int(value) for value in first_values + second_values):
        return False

    first_x, first_y, first_width, first_height = first_values
    second_x, second_y, second_width, second_height = second_values
    if min(first_width, first_height, second_width, second_height) <= 0:
        return False

    return (
        first_x < second_x + second_width
        and first_x + first_width > second_x
        and first_y < second_y + second_height
        and first_y + first_height > second_y
    )


def _validate_corridors(corridors, room_index, technical_context, errors):
    corridor_ids = set()
    width_limit = technical_context.get("width_squares")
    height_limit = technical_context.get("height_squares")
    grid_type = technical_context.get("grid_type")

    for corridor in corridors:
        if not isinstance(corridor, dict):
            errors.append("STRUCTURE_CORRIDOR_INVALID: each corridor must be an object")
            continue

        corridor_id = corridor.get("id")
        if corridor_id in (None, ""):
            errors.append("STRUCTURE_CORRIDOR_MISSING_ID: every corridor needs an id")
            continue
        if not _valid_id(corridor_id):
            errors.append("STRUCTURE_CORRIDOR_ID_INVALID: every corridor id must be a non-empty string")
            continue
        if corridor_id in corridor_ids:
            errors.append(f"STRUCTURE_DUPLICATE_CORRIDOR_ID: {corridor_id}")
        corridor_ids.add(corridor_id)

        connects = corridor.get("connects")
        if not isinstance(connects, list) or len(connects) < 2:
            errors.append(f"STRUCTURE_CORRIDOR_CONNECTS_INVALID: {corridor_id} must connect at least two rooms")
        else:
            for room_id in connects:
                if not _valid_id(room_id):
                    errors.append(f"STRUCTURE_CORRIDOR_CONNECTS_ROOM_ID_INVALID: {corridor_id} connects entries must be room ids")
                    continue
                if room_id not in room_index:
                    errors.append(f"STRUCTURE_CORRIDOR_UNKNOWN_ROOM: {corridor_id} references {room_id}")

        width = corridor.get("width_squares")
        if not _positive_int(width):
            errors.append(f"STRUCTURE_CORRIDOR_WIDTH_INVALID: {corridor_id} width_squares must be positive")

        path = corridor.get("path")
        if not isinstance(path, list) or len(path) < 2:
            errors.append(f"STRUCTURE_CORRIDOR_PATH_INVALID: {corridor_id} path needs at least two points")
            continue

        previous = None
        valid_points = []
        for point in path:
            if (
                not isinstance(point, list)
                or len(point) != 2
                or not all(_nonnegative_int(value) for value in point)
            ):
                errors.append(f"STRUCTURE_CORRIDOR_POINT_INVALID: {corridor_id} path points must be [x, y]")
                previous = None
                continue
            valid_points.append(point)
            x, y = point
            if width_limit and not 0 <= x <= width_limit:
                errors.append(f"STRUCTURE_CORRIDOR_OUT_OF_BOUNDS: {corridor_id} point {point} exceeds map width")
            if height_limit and not 0 <= y <= height_limit:
                errors.append(f"STRUCTURE_CORRIDOR_OUT_OF_BOUNDS: {corridor_id} point {point} exceeds map height")
            if grid_type == "square" and previous is not None and previous[0] != x and previous[1] != y:
                errors.append(f"STRUCTURE_CORRIDOR_DIAGONAL_SEGMENT: {corridor_id} segment {previous}->{point} is not orthogonal")
            previous = point

        if isinstance(connects, list):
            for room_id in connects:
                if not _valid_id(room_id):
                    continue
                room = room_index.get(room_id)
                if room is None:
                    continue
                if not any(_point_touches_room_boundary(point, room) for point in valid_points):
                    errors.append(f"STRUCTURE_CORRIDOR_NOT_ATTACHED: {corridor_id} path does not attach to {room_id}")


def _point_touches_room_boundary(point, room):
    x, y = point
    room_values = (room.get("x"), room.get("y"), room.get("width"), room.get("height"))
    if not all(_nonnegative_int(value) for value in room_values):
        return False

    room_x, room_y, room_width, room_height = room_values
    if room_width <= 0 or room_height <= 0:
        return False

    on_vertical_edge = x in (room_x, room_x + room_width) and room_y <= y <= room_y + room_height
    on_horizontal_edge = y in (room_y, room_y + room_height) and room_x <= x <= room_x + room_width
    return on_vertical_edge or on_horizontal_edge


def _room_size(room):
    width = room.get("width")
    height = room.get("height")
    if not isinstance(width, int) or not isinstance(height, int):
        return None
    return width, height


def _validate_connectivity(room_index, corridors, errors):
    if not room_index:
        return

    entry_candidates = [
        room_id
        for room_id, room in room_index.items()
        if room.get("type") == "entry" or room.get("is_entrance") is True
    ]
    entry_id = entry_candidates[0] if entry_candidates else next(iter(room_index))

    graph = defaultdict(set)
    for corridor in corridors:
        if not isinstance(corridor, dict):
            continue
        connects = corridor.get("connects")
        if not isinstance(connects, list):
            continue
        valid = [room_id for room_id in connects if _valid_id(room_id) and room_id in room_index]
        for index, room_id in enumerate(valid):
            for other_id in valid[index + 1 :]:
                graph[room_id].add(other_id)
                graph[other_id].add(room_id)

    reachable = set()
    queue = deque([entry_id])
    while queue:
        room_id = queue.popleft()
        if room_id in reachable:
            continue
        reachable.add(room_id)
        queue.extend(graph[room_id] - reachable)

    for room_id, room in room_index.items():
        if room_id in reachable:
            continue
        is_secret = room.get("secret") is True or room.get("type") == "secret"
        if is_secret:
            accessible_from = room.get("accessible_from")
            if not accessible_from:
                errors.append(f"STRUCTURE_SECRET_INACCESSIBLE: {room_id} must declare accessible_from")
            elif not _valid_id(accessible_from):
                errors.append(f"STRUCTURE_SECRET_INACCESSIBLE: {room_id} accessible_from must be a room id")
            elif accessible_from not in reachable:
                errors.append(f"STRUCTURE_SECRET_INACCESSIBLE: {room_id} accessible_from {accessible_from} is not reachable")
        else:
            errors.append(f"STRUCTURE_UNREACHABLE_ROOM: {room_id} is not reachable from {entry_id}")


def _validate_tactics(tactical, room_index, corridors, encounters, errors, warnings):
    if tactical is None:
        return

    party_size = tactical.get("party_size")
    if not _positive_int(party_size):
        errors.append("TACTICAL_PARTY_SIZE_INVALID: party_size must be a positive integer")

    largest_size = str(tactical.get("largest_creature_size", "medium")).lower()
    if largest_size not in SIZE_FOOTPRINTS:
        errors.append(f"TACTICAL_CREATURE_SIZE_INVALID: largest_creature_size must be one of {sorted(SIZE_FOOTPRINTS)}")
        largest_size = "medium"
    largest_footprint = SIZE_FOOTPRINTS[largest_size]

    traversal = tactical.get("largest_creature_traversal", {})
    if not isinstance(traversal, dict):
        errors.append("TACTICAL_TRAVERSAL_INVALID: largest_creature_traversal must be an object")
    elif traversal.get("required") is True:
        for corridor in corridors:
            if not isinstance(corridor, dict):
                continue
            width = corridor.get("width_squares")
            if isinstance(width, int) and width < largest_footprint:
                errors.append(
                    f"TACTICAL_CORRIDOR_TOO_NARROW: {corridor.get('id')} width {width} < {largest_size} footprint {largest_footprint}"
                )

    for encounter in encounters:
        if not isinstance(encounter, dict):
            errors.append("TACTICAL_ENCOUNTER_INVALID: each encounter must be an object")
            continue
        room_id = encounter.get("room_id")
        if not _valid_id(room_id):
            errors.append(f"TACTICAL_ENCOUNTER_ROOM_ID_INVALID: {encounter.get('id')} room_id must be a room id")
            continue
        room = room_index.get(room_id)
        if room is None:
            errors.append(f"TACTICAL_ENCOUNTER_UNKNOWN_ROOM: {encounter.get('id')} references {room_id}")
            continue

        enemy_size_values = encounter.get("enemy_sizes", [])
        if not isinstance(enemy_size_values, list):
            errors.append(f"TACTICAL_ENEMY_SIZES_INVALID: {encounter.get('id')} enemy_sizes must be a list")
            enemy_size_values = []
        enemy_sizes = [str(size).lower() for size in enemy_size_values]
        invalid_sizes = [size for size in enemy_sizes if size not in SIZE_FOOTPRINTS]
        for size in invalid_sizes:
            errors.append(f"TACTICAL_ENEMY_SIZE_INVALID: {encounter.get('id')} uses {size}")

        encounter_footprint = max([SIZE_FOOTPRINTS.get(size, 1) for size in enemy_sizes] or [1])
        role = str(encounter.get("role", "")).lower()
        room_type = str(room.get("type", "")).lower()
        room_size = _room_size(room)
        if role == "boss" or room_type == "boss":
            min_side = encounter_footprint + 4
            if room_size is not None and (room_size[0] < min_side or room_size[1] < min_side):
                size_name = _size_name_for_footprint(encounter_footprint)
                errors.append(
                    f"TACTICAL_BOSS_ROOM_TOO_SMALL: {room_id} must be at least {min_side}x{min_side} for {size_name} boss play"
                )
        elif room_type == "combat" and room_size is not None:
            if room_size[0] < 5 or room_size[1] < 5:
                warnings.append(f"TACTICAL_COMBAT_ROOM_TIGHT: {room_id} is smaller than 5x5")

    stealth_focus = str(tactical.get("stealth_focus", "none")).lower()
    if stealth_focus in {"optional", "primary"} and not any(room.get("secret") for room in room_index.values()):
        warnings.append("TACTICAL_STEALTH_LOW_SUPPORT: stealth_focus is set but no secret or alternate path is declared")


def _size_name_for_footprint(footprint):
    for name, size in SIZE_FOOTPRINTS.items():
        if size == footprint:
            return name
    return "custom"


def _validate_print(technical, context, errors, warnings):
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

    physical_grid = print_spec.get("physical_grid_inches")
    if not _positive_number(physical_grid):
        errors.append("PRINT_GRID_INVALID: physical_grid_inches must be positive")
        return

    margin = print_spec.get("margin_inches", 0)
    if not _nonnegative_number(margin):
        errors.append("PRINT_MARGIN_INVALID: margin_inches cannot be negative")
        return
    elif margin < 0.2:
        warnings.append("PRINT_MARGIN_TIGHT: margins below 0.2 inches may be clipped")

    split_pages = print_spec.get("split_pages")
    if split_pages is not None and not isinstance(split_pages, bool):
        errors.append("PRINT_SPLIT_PAGES_INVALID: split_pages must be true or false")
        return

    width_squares = context.get("width_squares")
    height_squares = context.get("height_squares")
    if width_squares and height_squares:
        map_width = width_squares * physical_grid
        map_height = height_squares * physical_grid
        paper_width, paper_height = PAPER_SIZES[paper]
        usable_width = paper_width - margin * 2
        usable_height = paper_height - margin * 2
        fits_portrait = map_width <= usable_width and map_height <= usable_height
        fits_landscape = map_width <= usable_height and map_height <= usable_width
        if not fits_portrait and not fits_landscape and split_pages is not True:
            errors.append("PRINT_REQUIRES_SPLIT: map exceeds single-page usable area without split_pages")


def main(argv=None):
    parser = argparse.ArgumentParser(description="Validate a DND map architect JSON spec.")
    parser.add_argument("spec", help="Path to a dungeon spec JSON file")
    args = parser.parse_args(argv)

    with open(args.spec, "r", encoding="utf-8") as handle:
        spec = json.load(handle)

    report = validate_spec(spec)
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
