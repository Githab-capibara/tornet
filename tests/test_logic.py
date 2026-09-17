"""Unit tests for Tornet's deterministic logic.

These tests avoid network / Tor / root and instead pin down the pure
helpers that drive the CLI. They exist because a small mistake in
interval parsing, country mapping or kill-switch state would corrupt
the main rotation loop that ships to users.

Run with:  python -m pytest tests/ -q
"""

import os
import sys
import importlib
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

# Import the package once and reuse the real module object so that the
# helpers read from the actual source, not a stale copy.
import tornet  # noqa: F401  (ensures package import works)
importlib.invalidate_caches()
tornet_mod = importlib.import_module("tornet.tornet")


class TestParseInterval(unittest.TestCase):
    """parse_interval: the heartbeat of the rotation loop."""

    def test_plain_integer(self):
        self.assertEqual(tornet_mod.parse_interval("60"), 60)

    def test_integer_object(self):
        # main() feeds argparse default '60' (str), but tests pass int
        self.assertEqual(tornet_mod.parse_interval(30), 30)

    def test_range_returns_value_in_bounds(self):
        for _ in range(50):
            v = tornet_mod.parse_interval("30-120")
            self.assertIsInstance(v, int)
            self.assertGreaterEqual(v, 30)
            self.assertLessEqual(v, 120)

    def test_range_single_value(self):
        self.assertEqual(tornet_mod.parse_interval("5-5"), 5)

    def test_invalid_string_raises_systemexit(self):
        with self.assertRaises(SystemExit) as ctx:
            tornet_mod.parse_interval("abc")
        self.assertEqual(ctx.exception.code, 8)

    def test_invalid_range_raises_systemexit(self):
        with self.assertRaises(SystemExit) as ctx:
            tornet_mod.parse_interval("30-")
        self.assertEqual(ctx.exception.code, 8)


class TestParseSchedule(unittest.TestCase):
    """parse_schedule: converts '5m' style strings to seconds."""

    def test_seconds(self):
        self.assertEqual(tornet_mod.parse_schedule("30s"), 30)

    def test_minutes(self):
        self.assertEqual(tornet_mod.parse_schedule("5m"), 300)

    def test_hours(self):
        self.assertEqual(tornet_mod.parse_schedule("2h"), 7200)

    def test_days(self):
        self.assertEqual(tornet_mod.parse_schedule("1d"), 86400)

    def test_invalid_unit(self):
        with self.assertRaises(SystemExit) as ctx:
            tornet_mod.parse_schedule("10w")
        self.assertEqual(ctx.exception.code, 12)


class TestCountryMapping(unittest.TestCase):
    def test_known_country_resolves_name(self):
        self.assertEqual(
            tornet_mod.get_country_name("US"), "United States")

    def test_unknown_country_returns_upper(self):
        # Unknown codes fall back to the upper-cased input.
        self.assertEqual(tornet_mod.get_country_name("zz"), "ZZ")

    def test_case_insensitive_lookup(self):
        self.assertEqual(tornet_mod.get_country_name("de"), "Germany")


class TestKillSwitchStateDetection(unittest.TestCase):
    """toggle_kill_switch relies on grepping 'TORNET-KILLSWITCH' in
    `iptables -L` output. Verify the marker string the function uses is
    stable so a rename can't silently disable it."""

    def test_marker_string_is_stable(self):
        marker = "TORNET-KILLSWITCH"
        # Import source and assert the marker still appears verbatim.
        src = Path(tornet_mod.__file__).read_text()
        self.assertIn(marker, src)


class TestConfigLoadSave(unittest.TestCase):
    """load_config / save_config: YAML + JSON round-trip."""

    def test_yaml_roundtrip(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "c.yml"
            p.write_text("a:\n  b: 1\n")
            self.assertEqual(tornet_mod.load_config(str(p)), {"a": {"b": 1}})
            tornet_mod.save_config(str(p), {"x": [1, 2]})
            self.assertEqual(tornet_mod.load_config(str(p)), {"x": [1, 2]})

    def test_json_roundtrip(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "c.json"
            p.write_text('{"k": true}')
            self.assertEqual(tornet_mod.load_config(str(p)), {"k": True})
            tornet_mod.save_config(str(p), {"k": False, "n": 5})
            self.assertEqual(
                tornet_mod.load_config(str(p)), {"k": False, "n": 5})

    def test_missing_file_returns_empty_dict(self):
        self.assertEqual(
            tornet_mod.load_config("/nonexistent/config.yml"), {})

    def test_unsupported_format_warns_returns_empty(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "c.toml"
            p.write_text("x = 1")
            self.assertEqual(tornet_mod.load_config(str(p)), {})


class TestConfiguredCountryFile(unittest.TestCase):
    """get_current_country reads/writes a marker file."""

    def test_reads_configured_country(self):
        old = Path(tornet_mod.CURRENT_COUNTRY_FILE)
        tmp = Path(tempfile.mktemp(suffix=".country"))
        try:
            tmp.write_text("JP")
            import unittest.mock as m
            with m.patch.object(tornet_mod, "CURRENT_COUNTRY_FILE", str(tmp)):
                self.assertEqual(tornet_mod.get_current_country(), "JP")
        finally:
            if tmp.exists():
                tmp.unlink()
            _ = old  # keep reference to original

    def test_returns_auto_when_no_file(self):
        import unittest.mock as m
        missing = "/nonexistent/current_country"
        with m.patch.object(tornet_mod, "CURRENT_COUNTRY_FILE", missing):
            self.assertEqual(
                tornet_mod.get_current_country(), "Auto (Random)")


if __name__ == "__main__":
    unittest.main()
