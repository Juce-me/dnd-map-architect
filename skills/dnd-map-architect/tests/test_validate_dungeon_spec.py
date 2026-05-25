import importlib.util
import pathlib
import unittest


SCRIPT_PATH = pathlib.Path(__file__).resolve().parents[1] / "scripts" / "validate_dungeon_spec.py"


def load_validator():
    spec = importlib.util.spec_from_file_location("validate_dungeon_spec", SCRIPT_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def valid_spec():
    return {
        "identity": {
            "name": "Ember Archive",
            "dungeon_type": "dwarven library",
            "gameplay_focus": ["combat", "exploration"],
        },
        "technical": {
            "grid_type": "square",
            "tile_scale_ft": 5,
            "width_squares": 24,
            "height_squares": 18,
            "image_dimensions_px": [2400, 1800],
            "vtt_target": "FoundryVTT",
            "print": {
                "enabled": True,
                "paper": "Letter",
                "physical_grid_inches": 1,
                "margin_inches": 0.25,
                "split_pages": True,
            },
        },
        "tactical": {
            "party_level": 6,
            "party_size": 4,
            "largest_creature_size": "huge",
            "largest_creature_traversal": {"required": True},
        },
        "rooms": [
            {"id": "entry", "name": "Entry Hall", "type": "entry", "x": 1, "y": 1, "width": 6, "height": 5},
            {"id": "stacks", "name": "Burned Stacks", "type": "combat", "x": 9, "y": 1, "width": 8, "height": 6},
            {"id": "vault", "name": "Forge Vault", "type": "boss", "x": 7, "y": 10, "width": 12, "height": 7},
        ],
        "corridors": [
            {"id": "c1", "connects": ["entry", "stacks"], "width_squares": 3, "path": [[7, 3], [9, 3]]},
            {"id": "c2", "connects": ["stacks", "vault"], "width_squares": 3, "path": [[13, 7], [13, 10]]},
        ],
        "encounters": [
            {"id": "e1", "room_id": "stacks", "role": "skirmish", "enemy_sizes": ["medium", "large"]},
            {"id": "e2", "room_id": "vault", "role": "boss", "enemy_sizes": ["huge"]},
        ],
    }


class ValidateDungeonSpecTests(unittest.TestCase):
    def test_valid_spec_has_no_errors(self):
        validator = load_validator()
        report = validator.validate_spec(valid_spec())
        self.assertEqual([], report["errors"])

    def test_invalid_identity_name_returns_error(self):
        validator = load_validator()
        spec = valid_spec()
        spec["identity"]["name"] = ["Ember Archive"]
        report = validator.validate_spec(spec)
        self.assertFalse(report["ok"])
        self.assertIn("IDENTITY_NAME_INVALID: name must be a non-empty string", report["errors"])

    def test_disconnected_non_secret_room_fails(self):
        validator = load_validator()
        spec = valid_spec()
        spec["rooms"].append(
            {"id": "isolated", "name": "Cut Off Shrine", "type": "combat", "x": 20, "y": 2, "width": 3, "height": 3}
        )
        report = validator.validate_spec(spec)
        self.assertIn("STRUCTURE_UNREACHABLE_ROOM: isolated is not reachable from entry", report["errors"])

    def test_distorted_square_grid_fails(self):
        validator = load_validator()
        spec = valid_spec()
        spec["technical"]["image_dimensions_px"] = [2400, 1728]
        report = validator.validate_spec(spec)
        self.assertIn("GRID_DISTORTED: pixels per square differ across axes", report["errors"])

    def test_huge_creature_requires_three_square_corridors(self):
        validator = load_validator()
        spec = valid_spec()
        spec["corridors"][0]["width_squares"] = 2
        report = validator.validate_spec(spec)
        self.assertIn("TACTICAL_CORRIDOR_TOO_NARROW: c1 width 2 < huge footprint 3", report["errors"])

    def test_huge_boss_room_must_be_playable(self):
        validator = load_validator()
        spec = valid_spec()
        spec["rooms"][2]["width"] = 6
        spec["rooms"][2]["height"] = 5
        report = validator.validate_spec(spec)
        self.assertIn("TACTICAL_BOSS_ROOM_TOO_SMALL: vault must be at least 7x7 for huge boss play", report["errors"])

    def test_overlapping_rooms_are_blocking_structural_errors(self):
        validator = load_validator()
        spec = valid_spec()
        spec["rooms"][1]["x"] = 5
        spec["rooms"][1]["y"] = 3
        report = validator.validate_spec(spec)
        self.assertIn("STRUCTURE_ROOM_OVERLAP: entry overlaps stacks", report["errors"])

    def test_corridor_path_must_physically_attach_to_connected_rooms(self):
        validator = load_validator()
        spec = valid_spec()
        spec["corridors"][0]["path"] = [[7, 3], [8, 3]]
        report = validator.validate_spec(spec)
        self.assertIn("STRUCTURE_CORRIDOR_NOT_ATTACHED: c1 path does not attach to stacks", report["errors"])

    def test_print_without_split_pages_is_blocking_when_map_exceeds_one_page(self):
        validator = load_validator()
        spec = valid_spec()
        spec["technical"]["print"]["split_pages"] = False
        report = validator.validate_spec(spec)
        self.assertIn("PRINT_REQUIRES_SPLIT: map exceeds single-page usable area without split_pages", report["errors"])
        self.assertNotIn("PRINT_REQUIRES_SPLIT: map exceeds single-page usable area without split_pages", report["warnings"])

    def test_hex_grid_requires_orientation(self):
        validator = load_validator()
        spec = valid_spec()
        spec["technical"]["grid_type"] = "hex"
        spec["technical"]["coordinate_system"] = "axial"
        report = validator.validate_spec(spec)
        self.assertIn("GRID_HEX_ORIENTATION_REQUIRED: hex grids require orientation", report["errors"])

    def test_hex_grid_requires_coordinate_system(self):
        validator = load_validator()
        spec = valid_spec()
        spec["technical"]["grid_type"] = "hex"
        spec["technical"]["orientation"] = "pointy"
        report = validator.validate_spec(spec)
        self.assertIn("GRID_HEX_COORDINATE_SYSTEM_REQUIRED: hex grids require coordinate_system", report["errors"])

    def test_valid_hex_spec_allows_diagonal_neighbor_segments(self):
        validator = load_validator()
        spec = valid_spec()
        spec["technical"]["grid_type"] = "hex"
        spec["technical"]["orientation"] = "pointy"
        spec["technical"]["coordinate_system"] = "axial"
        spec["corridors"][0]["path"] = [[7, 3], [8, 4], [9, 4]]
        report = validator.validate_spec(spec)
        self.assertNotIn(
            "STRUCTURE_CORRIDOR_DIAGONAL_SEGMENT: c1 segment [7, 3]->[8, 4] is not orthogonal",
            report["errors"],
        )

    def test_missing_corridors_returns_error_instead_of_crashing(self):
        validator = load_validator()
        spec = valid_spec()
        del spec["corridors"]
        report = validator.validate_spec(spec)
        self.assertFalse(report["ok"])
        self.assertIn("SPEC_MISSING: corridors must be a list", report["errors"])

    def test_invalid_corridor_entry_returns_error_instead_of_crashing(self):
        validator = load_validator()
        spec = valid_spec()
        spec["corridors"] = ["bad"]
        report = validator.validate_spec(spec)
        self.assertFalse(report["ok"])
        self.assertIn("STRUCTURE_CORRIDOR_INVALID: each corridor must be an object", report["errors"])

    def test_invalid_room_id_returns_error_instead_of_crashing(self):
        validator = load_validator()
        spec = valid_spec()
        spec["rooms"][0]["id"] = ["entry"]
        report = validator.validate_spec(spec)
        self.assertFalse(report["ok"])
        self.assertIn("STRUCTURE_ROOM_ID_INVALID: every room id must be a non-empty string", report["errors"])

    def test_invalid_corridor_id_returns_error_instead_of_crashing(self):
        validator = load_validator()
        spec = valid_spec()
        spec["corridors"][0]["id"] = ["c1"]
        report = validator.validate_spec(spec)
        self.assertFalse(report["ok"])
        self.assertIn("STRUCTURE_CORRIDOR_ID_INVALID: every corridor id must be a non-empty string", report["errors"])

    def test_invalid_corridor_connects_member_returns_error_instead_of_crashing(self):
        validator = load_validator()
        spec = valid_spec()
        spec["corridors"][0]["connects"] = ["entry", ["stacks"]]
        report = validator.validate_spec(spec)
        self.assertFalse(report["ok"])
        self.assertIn("STRUCTURE_CORRIDOR_CONNECTS_ROOM_ID_INVALID: c1 connects entries must be room ids", report["errors"])

    def test_invalid_room_geometry_with_encounter_returns_error_instead_of_crashing(self):
        validator = load_validator()
        spec = valid_spec()
        spec["rooms"][2]["width"] = "bad"
        report = validator.validate_spec(spec)
        self.assertFalse(report["ok"])
        self.assertIn("STRUCTURE_ROOM_GEOMETRY_INVALID: vault.width must be a non-negative integer", report["errors"])

    def test_invalid_enemy_sizes_returns_error_instead_of_crashing(self):
        validator = load_validator()
        spec = valid_spec()
        spec["encounters"][0]["enemy_sizes"] = None
        report = validator.validate_spec(spec)
        self.assertFalse(report["ok"])
        self.assertIn("TACTICAL_ENEMY_SIZES_INVALID: e1 enemy_sizes must be a list", report["errors"])

    def test_invalid_print_paper_returns_error_instead_of_crashing(self):
        validator = load_validator()
        spec = valid_spec()
        spec["technical"]["print"]["paper"] = ["Letter"]
        report = validator.validate_spec(spec)
        self.assertFalse(report["ok"])
        self.assertIn("PRINT_PAPER_INVALID: paper must be one of ['A3', 'A4', 'Ledger', 'Letter']", report["errors"])

    def test_invalid_print_margin_returns_error_instead_of_crashing(self):
        validator = load_validator()
        spec = valid_spec()
        spec["technical"]["print"]["margin_inches"] = "bad"
        report = validator.validate_spec(spec)
        self.assertFalse(report["ok"])
        self.assertIn("PRINT_MARGIN_INVALID: margin_inches cannot be negative", report["errors"])

    def test_invalid_grid_type_returns_error_instead_of_crashing(self):
        validator = load_validator()
        spec = valid_spec()
        spec["technical"]["grid_type"] = ["square"]
        report = validator.validate_spec(spec)
        self.assertFalse(report["ok"])
        self.assertIn("GRID_TYPE_INVALID: grid_type must be one of ['hex', 'square']", report["errors"])

    def test_invalid_hex_orientation_returns_error_instead_of_crashing(self):
        validator = load_validator()
        spec = valid_spec()
        spec["technical"]["grid_type"] = "hex"
        spec["technical"]["orientation"] = ["pointy"]
        spec["technical"]["coordinate_system"] = "axial"
        report = validator.validate_spec(spec)
        self.assertFalse(report["ok"])
        self.assertIn("GRID_HEX_ORIENTATION_INVALID: orientation must be one of ['flat', 'flat-top', 'pointy', 'pointy-top']", report["errors"])

    def test_invalid_hex_coordinate_system_shape_returns_error_instead_of_crashing(self):
        validator = load_validator()
        spec = valid_spec()
        spec["technical"]["grid_type"] = "hex"
        spec["technical"]["orientation"] = "pointy"
        spec["technical"]["coordinate_system"] = ["axial"]
        report = validator.validate_spec(spec)
        self.assertFalse(report["ok"])
        self.assertIn("GRID_HEX_COORDINATE_SYSTEM_INVALID: coordinate_system must be one of ['axial', 'offset']", report["errors"])

    def test_invalid_grid_width_returns_error_instead_of_crashing_grid_math(self):
        validator = load_validator()
        spec = valid_spec()
        spec["technical"]["width_squares"] = ["24"]
        report = validator.validate_spec(spec)
        self.assertFalse(report["ok"])
        self.assertIn("GRID_WIDTH_INVALID: width_squares must be a positive integer", report["errors"])

    def test_boolean_grid_width_returns_error(self):
        validator = load_validator()
        spec = valid_spec()
        spec["technical"]["width_squares"] = True
        report = validator.validate_spec(spec)
        self.assertFalse(report["ok"])
        self.assertIn("GRID_WIDTH_INVALID: width_squares must be a positive integer", report["errors"])

    def test_boolean_tile_scale_returns_error(self):
        validator = load_validator()
        spec = valid_spec()
        spec["technical"]["tile_scale_ft"] = True
        report = validator.validate_spec(spec)
        self.assertFalse(report["ok"])
        self.assertIn("GRID_SCALE_INVALID: tile_scale_ft must be positive", report["errors"])

    def test_boolean_print_grid_returns_error(self):
        validator = load_validator()
        spec = valid_spec()
        spec["technical"]["print"]["physical_grid_inches"] = True
        report = validator.validate_spec(spec)
        self.assertFalse(report["ok"])
        self.assertIn("PRINT_GRID_INVALID: physical_grid_inches must be positive", report["errors"])

    def test_boolean_print_margin_returns_error(self):
        validator = load_validator()
        spec = valid_spec()
        spec["technical"]["print"]["margin_inches"] = True
        report = validator.validate_spec(spec)
        self.assertFalse(report["ok"])
        self.assertIn("PRINT_MARGIN_INVALID: margin_inches cannot be negative", report["errors"])

    def test_boolean_room_coordinate_returns_error(self):
        validator = load_validator()
        spec = valid_spec()
        spec["rooms"][0]["y"] = False
        report = validator.validate_spec(spec)
        self.assertFalse(report["ok"])
        self.assertIn("STRUCTURE_ROOM_GEOMETRY_INVALID: entry.y must be a non-negative integer", report["errors"])

    def test_boolean_corridor_path_coordinate_returns_error(self):
        validator = load_validator()
        spec = valid_spec()
        spec["corridors"][0]["path"] = [[7, True], [9, True]]
        report = validator.validate_spec(spec)
        self.assertFalse(report["ok"])
        self.assertIn("STRUCTURE_CORRIDOR_POINT_INVALID: c1 path points must be [x, y]", report["errors"])

    def test_invalid_print_split_pages_returns_error(self):
        validator = load_validator()
        spec = valid_spec()
        spec["technical"]["print"]["split_pages"] = "yes"
        report = validator.validate_spec(spec)
        self.assertFalse(report["ok"])
        self.assertIn("PRINT_SPLIT_PAGES_INVALID: split_pages must be true or false", report["errors"])

    def test_invalid_room_doors_returns_error_instead_of_crashing(self):
        validator = load_validator()
        spec = valid_spec()
        spec["rooms"][0]["doors"] = None
        report = validator.validate_spec(spec)
        self.assertFalse(report["ok"])
        self.assertIn("STRUCTURE_DOORS_INVALID: entry doors must be a list", report["errors"])

    def test_invalid_largest_creature_traversal_returns_error(self):
        validator = load_validator()
        spec = valid_spec()
        spec["corridors"][0]["width_squares"] = 1
        spec["tactical"]["largest_creature_traversal"] = "required"
        report = validator.validate_spec(spec)
        self.assertFalse(report["ok"])
        self.assertIn("TACTICAL_TRAVERSAL_INVALID: largest_creature_traversal must be an object", report["errors"])

    def test_invalid_print_enabled_returns_error(self):
        validator = load_validator()
        spec = valid_spec()
        spec["technical"]["print"]["enabled"] = "true"
        report = validator.validate_spec(spec)
        self.assertFalse(report["ok"])
        self.assertIn("PRINT_ENABLED_INVALID: enabled must be true or false", report["errors"])

    def test_stealth_focus_none_does_not_warn_about_low_support(self):
        validator = load_validator()
        spec = valid_spec()
        spec["tactical"]["stealth_focus"] = "none"
        report = validator.validate_spec(spec)
        self.assertNotIn("TACTICAL_STEALTH_LOW_SUPPORT: stealth_focus is set but no secret or alternate path is declared", report["warnings"])

    def test_cube_hex_coordinate_system_is_rejected_until_supported(self):
        validator = load_validator()
        spec = valid_spec()
        spec["technical"]["grid_type"] = "hex"
        spec["technical"]["orientation"] = "pointy"
        spec["technical"]["coordinate_system"] = "cube"
        report = validator.validate_spec(spec)
        self.assertIn("GRID_HEX_COORDINATE_SYSTEM_INVALID: coordinate_system must be one of ['axial', 'offset']", report["errors"])


if __name__ == "__main__":
    unittest.main()
