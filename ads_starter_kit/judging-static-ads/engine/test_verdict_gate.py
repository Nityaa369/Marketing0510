#!/usr/bin/env python3
"""Tests for the packaging gate (verdict_log.gate).

The gate's job is to fail closed. Every test here is really asking one question:
can a defective creative reach a media buyer? The interesting cases are not the
obvious REJECT, they are the ways a gate silently stops gating: a missing verdict
read as consent, or a stale pass authorising bytes it never saw.
"""

import json
import os
import sys
import tempfile
import time
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import verdict_log  # noqa: E402


def iso(offset_sec=0):
    return time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime(time.time() + offset_sec))


class GateBase(unittest.TestCase):
    def setUp(self):
        self.d = tempfile.mkdtemp()
        self.png = os.path.join(self.d, "hr_04_sideincome.png")
        with open(self.png, "wb") as f:
            f.write(b"\x89PNG")
        self.log = os.path.join(self.d, "verdicts.jsonl")

    def write(self, **row):
        row.setdefault("file", "hr_04_sideincome.html")
        row.setdefault("ts", iso())             # judged now, as a real run would
        with open(self.log, "a") as f:
            f.write(json.dumps(row) + "\n")

    def gate(self, **kw):
        return verdict_log.gate(self.png, path=self.log, **kw)


class TestFailsClosed(GateBase):
    def test_no_verdict_at_all_is_a_failure(self):
        """Absence of judgement must never read as approval."""
        ok, detail = self.gate()
        self.assertFalse(ok)
        self.assertIn("never judged", detail)

    def test_missing_log_file_is_a_failure(self):
        ok, _ = verdict_log.gate(self.png, path=os.path.join(self.d, "nope.jsonl"))
        self.assertFalse(ok)

    def test_reject_blocks(self):
        self.write(verdict="REJECT — rethink", rules_fired=["C21", "X1"])
        ok, detail = self.gate()
        self.assertFalse(ok)
        self.assertIn("C21", detail)

    def test_torn_line_does_not_blind_the_gate(self):
        with open(self.log, "a") as f:
            f.write("{not json\n")
        self.write(verdict="REJECT — rethink", rules_fired=["C21"])
        ok, _ = self.gate()
        self.assertFalse(ok)


class TestFreshness(GateBase):
    def test_verdict_older_than_the_file_is_stale(self):
        """A pass authorises the bytes it was computed from, and nothing else."""
        self.write(verdict="ACCEPT", ts=iso(-3600))
        os.utime(self.png, None)                 # touch: file changed after judging
        ok, detail = self.gate()
        self.assertFalse(ok)
        self.assertIn("changed since", detail)

    def test_fresh_accept_passes(self):
        self.write(verdict="ACCEPT")
        ok, _ = self.gate()
        self.assertTrue(ok)

    def test_edit_after_pass_reblocks(self):
        """The obvious way to defeat a gate: pass, then quietly edit."""
        self.write(verdict="ACCEPT")
        self.assertTrue(self.gate()[0])
        time.sleep(1.1)
        with open(self.png, "ab") as f:
            f.write(b"edited")
        self.assertFalse(self.gate()[0])


class TestVerdictKinds(GateBase):
    def test_accept_with_changes_ships(self):
        """One fix note is a note, not a blocker — same as creative_judge's rule."""
        self.write(verdict="ACCEPT WITH CHANGES", reason="1 fix note(s)")
        self.assertTrue(self.gate()[0])

    def test_latest_verdict_wins(self):
        self.write(verdict="REJECT — rethink", ts=iso(+10), rules_fired=["C21"])
        self.write(verdict="ACCEPT", ts=iso(+120))
        self.assertTrue(self.gate()[0])

    def test_a_later_reject_overrides_an_earlier_accept(self):
        self.write(verdict="ACCEPT", ts=iso(+10))
        self.write(verdict="REJECT — rethink", ts=iso(+120), rules_fired=["X1"])
        self.assertFalse(self.gate()[0])

    def test_png_matches_html_verdict_by_stem(self):
        """The log names the HTML; the kit ships the PNG."""
        self.write(verdict="ACCEPT", file="hr_04_sideincome.html")
        self.assertTrue(self.gate()[0])

    def test_other_creatives_verdict_does_not_apply(self):
        self.write(verdict="ACCEPT", file="hr_09_other.html")
        ok, detail = self.gate()
        self.assertFalse(ok)
        self.assertIn("never judged", detail)


class TestOverride(GateBase):
    def test_named_defect_can_be_accepted(self):
        self.write(verdict="REJECT — rethink", rules_fired=["C21"])
        self.assertTrue(self.gate(accept_defects=("C21",))[0])

    def test_override_only_covers_the_named_codes(self):
        self.write(verdict="REJECT — rethink", rules_fired=["C21", "X1"])
        ok, detail = self.gate(accept_defects=("C21",))
        self.assertFalse(ok, "an unlisted defect must still block")
        self.assertIn("X1", detail)

    def test_override_is_recorded(self):
        verdict_log.record_override(self.png, ["C21"], "brand wants it", path=self.log)
        rows = verdict_log.read_all(self.log)
        self.assertEqual(rows[-1]["verdict"], "OVERRIDE")
        self.assertEqual(rows[-1]["overrides"][0]["reason"], "brand wants it")




class TestStemVariants(GateBase):
    """Kits do not name the source and the render the same thing.

    women_ai_r10_sep05 judges src_W3_N18_caregiver.html and ships
    W3_N18_caregiver.png. A literal stem match called that freshly judged creative
    "never judged" — a false block, which is how a gate gets routed around.
    """

    def test_src_prefixed_source_matches_its_render(self):
        self.write(verdict="ACCEPT", file="src_hr_04_sideincome.html")
        ok, detail = self.gate()
        self.assertTrue(ok, detail)

    def test_size_suffixed_render_matches(self):
        png = os.path.join(self.d, "hr_04_sideincome_1080x1350.png")
        with open(png, "wb") as f:
            f.write(b"\x89PNG")
        self.write(verdict="ACCEPT", file="src_hr_04_sideincome.html")
        ok, _ = verdict_log.gate(png, path=self.log)
        self.assertTrue(ok)

    def test_different_creatives_still_do_not_match(self):
        self.write(verdict="ACCEPT", file="src_hr_09_other.html")
        ok, _ = self.gate()
        self.assertFalse(ok, "variant matching must not collapse distinct creatives")


if __name__ == "__main__":
    unittest.main(verbosity=2)
