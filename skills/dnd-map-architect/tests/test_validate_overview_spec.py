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
