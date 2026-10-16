"""Zip a SHIP folder into the file that actually gets sent.

Added 4 Sep 2026. `make_ship.py` built the folder and then stopped, so the last
step -- the one that produces the thing a person receives -- was done by hand
every time. Twice that went wrong in ways nobody would notice until the recipient
opened it:

  * PowerShell's `Compress-Archive` writes **backslash** path separators. That is
    off-spec for the ZIP format; Windows unpacks it, and a Mac unpacks it as ten
    files literally named "ads\\47_transfer_pricing.png" in one flat folder.
  * a rebuild of the folder left an older zip beside it, so the newest faces were
    in the folder and the previous ones were in the file being sent.

`shutil.make_archive` writes forward slashes on every platform, so this is both
the fix and the reason the step belongs in code rather than in a habit.

WHAT SHIPS: exactly the six items of the SHIP format (SOP/01) -- README.md,
ad_copy_wN.md, ads/, landing_pages/, manifest.json, kit_meta.json. This module
verifies that before writing anything, so a stray html/ or spec.py cannot ride
along into a zip going to a media buyer.
"""

import os
import shutil
import zipfile

SHIP_ITEMS = {"README.md", "ads", "landing_pages", "manifest.json", "kit_meta.json"}


def zip_ship(folder, quiet=False, allow=()):
    """Zip `folder` next to itself. Returns the path of the zip written.

    `allow` names extra top-level items a kit ships ON PURPOSE. Added 17 Sep 2026: for
    the US Accounting 10-12 Oct search wave Ruchika asked for the kit's .py and .md files
    in the zip too ("add the py and md files to the zip too"). They ride in one `source/`
    folder so the six deploy items stay exactly as the pipeline reads them. Anything not
    named here is still refused, so a stray html/ cannot slip in by accident."""
    folder = os.path.abspath(folder.rstrip("/\\"))
    parent, name = os.path.dirname(folder), os.path.basename(folder)
    if not os.path.isdir(folder):
        raise SystemExit("no such ship folder: %s" % folder)

    present = set(os.listdir(folder))
    extra = {x for x in present
             if x not in SHIP_ITEMS and not x.startswith("ad_copy_") and x not in set(allow)}
    missing = SHIP_ITEMS - present
    if missing:
        raise SystemExit("SHIP format: %s is missing %s"
                         % (name, ", ".join(sorted(missing))))
    if extra:
        raise SystemExit("SHIP format: %s carries working files that must not "
                         "ship: %s" % (name, ", ".join(sorted(extra))))

    out = os.path.join(parent, name + ".zip")
    if os.path.exists(out):
        os.remove(out)            # never leave a stale zip beside a fresh folder
    shutil.make_archive(os.path.join(parent, name), "zip", parent, name)

    with zipfile.ZipFile(out) as z:
        names = z.namelist()
    bad = [n for n in names if "\\" in n]
    if bad:
        raise SystemExit("zip wrote %d backslash path(s); it will not unpack "
                         "correctly on macOS" % len(bad))
    if not quiet:
        n_ads = sum(1 for n in names if "/ads/" in n and n.endswith(".png"))
        n_lps = sum(1 for n in names if "/landing_pages/" in n and n.endswith(".html"))
        print("zip: %s" % out)
        print("     %d files, %d ads, %d landing pages, %d KB, forward slashes"
              % (len(names), n_ads, n_lps, os.path.getsize(out) // 1024))
    return out


if __name__ == "__main__":
    import sys
    for f in sys.argv[1:]:
        zip_ship(f)
