"""adkit - the shared ad-face chassis and landing-page spine for this account.

One copy of the things every kit was re-deriving: the 1080x1350 face, the ten-
section landing page, the Chrome render call, the palette register, and a fit
gate for the defect class no other checker in this repo can see.

    from adkit import Kit, Camp

See adkit/README.md for the measurement that justifies it and for the two-file
kit template.
"""
from .chassis import Kit, Ad, css, W, H, SCALES, callout_px, head_px
from .lp_spine import Camp
from .spec import Spec
from .palettes import PALETTES, get as palette
from . import fit, verdicts, golden

__all__ = ["Kit", "Ad", "Camp", "Spec", "css", "fit", "palette", "PALETTES",
           "W", "H", "SCALES", "callout_px", "head_px", "verdicts", "golden"]
