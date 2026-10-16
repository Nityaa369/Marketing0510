#!/usr/bin/env python3
"""Named palettes for ad faces and their matching landing pages.

Rule 4 (CLAUDE.md): every ad gets its own colour palette, and the landing page
mirrors its ad's. Keeping the register here rather than re-typing hex codes in
each kit is what makes "one palette per ad" checkable instead of hopeful --
Kit.render() refuses to build two faces on the same palette.

The first eleven are lifted byte-for-byte from
IndependentDirector_Wave1_MediaBuyer_12-14Sep/gen_ads.py, which shipped. The
rest are built to the same recipe: a near-white paper `page`, a dark saturated
`accent` that clears 4.5:1 on white, an almost-black `ink`, white `card`, and a
`line` that is the accent desaturated to about 15% -- so a new one can be added
without guessing.

`soft` is the landing page's tint block background (SOP/05 .box); it is derived
from `page` when a palette does not carry one.

`bright` was added 1 Sep 2026 for the borrowed social formats in
`adkit/layouts_social.py`, which do not sit on paper: `duo` needs a DARK
saturated ground because white type sits directly on it, and `pixel` needs a
BRIGHT one because near-black type sits directly on it. Both are checked against
the type that actually lands on them rather than against white. A palette
without a `bright` falls back to `page`, so nothing that already shipped moves.
"""

PALETTES = {
    "clay":     dict(page="#F4F1EB", accent="#7A4A1E", ink="#211D18", card="#FFFFFF", line="#DED3C2"),
    "pine":     dict(page="#EDF2F0", accent="#106046", ink="#152420", card="#FFFFFF", line="#CBDCD4"),
    "navy":     dict(page="#F0F1F4", accent="#1F4E86", ink="#171B22", card="#FFFFFF", line="#CFD6E0"),
    "rust":     dict(page="#F7EFEC", accent="#96331F", ink="#231816", card="#FFFFFF", line="#E3CFC8"),
    "teal":     dict(page="#E9F2F6", accent="#0E6079", ink="#12212A", card="#FFFFFF", line="#C4D8E2"),
    "ochre":    dict(page="#F5F1E5", accent="#7E5A0E", ink="#221D12", card="#FFFFFF", line="#DFD3B4"),
    "plum":     dict(page="#F6ECF1", accent="#7A2A5C", ink="#241621", card="#FFFFFF", line="#E2CBD8", bright="#5B1D45"),
    "olive":    dict(page="#F1F3E8", accent="#4C6819", ink="#1B2011", card="#FFFFFF", line="#D2DBBC", bright="#2C3D12"),
    "slate":    dict(page="#EEF0F3", accent="#3B4657", ink="#171A20", card="#FFFFFF", line="#CFD5DD"),
    "claret":   dict(page="#F6EDEF", accent="#6E2233", ink="#221417", card="#FFFFFF", line="#E0C8CE", bright="#54182A"),
    "ink":      dict(page="#F2F1EE", accent="#243043", ink="#15181E", card="#FFFFFF", line="#D3D5DA", bright="#9BE0FA"),
    "forest":   dict(page="#EBF1EC", accent="#255B33", ink="#141D17", card="#FFFFFF", line="#C9DBCE", bright="#CDEF5B"),
    "brick":    dict(page="#F7EEEA", accent="#8A3A16", ink="#241A14", card="#FFFFFF", line="#E4CFC4", bright="#FFD9A8"),
    "indigo":   dict(page="#EFF0F6", accent="#37357A", ink="#16161F", card="#FFFFFF", line="#D0D1E2", bright="#282657"),
    "moss":     dict(page="#F0F2EA", accent="#55631D", ink="#1B1E12", card="#FFFFFF", line="#D6DBC1", bright="#E9F58C"),
    "wine":     dict(page="#F5EDF0", accent="#5E2540", ink="#1F141A", card="#FFFFFF", line="#DEC9D3", bright="#46182F"),
    "cocoa":    dict(page="#F5EFE9", accent="#5A3A24", ink="#1E1611", card="#FFFFFF", line="#E0D2C4"),
    # Four added 17 Sep 2026: the US Accounting search wave needed 21 faces and the register
    # held 17. Same recipe as above; each accent clears 4.5:1 against white.
    "cobalt":   dict(page="#EEF2FA", accent="#1D56B0", ink="#131A26", card="#FFFFFF", line="#CCD8EE"),
    "berry":    dict(page="#F8EDF2", accent="#A0245D", ink="#24141C", card="#FFFFFF", line="#E6C9D6"),
    "grape":    dict(page="#F2EFF8", accent="#58399E", ink="#1B1626", card="#FFFFFF", line="#D6CDE8"),
    "carmine":  dict(page="#F8EEEC", accent="#A8231C", ink="#261514", card="#FFFFFF", line="#E8CBC7"),
    # Three added 21 Sep 2026. "Every ad gets its own colour palette" was being read
    # as "no two accents share a hex", and the CF notify wave passed that while three
    # pairs sat under CIELAB dE 12, about where two colours stop being told apart at
    # a glance: rust/brick 9.0, pine/forest 9.8, slate/ink 10.0. An exhaustive swap
    # search over every assignment of 19 of the then-21 palettes topped out at 9.8,
    # so the register itself was too crowded in the red-brown, green and slate
    # families and needed widening, not reshuffling.
    #
    # Placed in the hue gaps the register left (used hues ran 3-41, 72-81, 136-160,
    # 194-217, 242-258, 322-347): fern at 95, brass at 50, iris at 272.
    #
    # Chosen by treating dE >= 12 as a CONSTRAINT and then picking the colour
    # closest to the register's own centre of gravity (sat 0.71, val 0.47, measured
    # over the existing 21). Maximising dE instead - the first attempt - drove every
    # pick to the saturation ceiling and produced #068006 and #991299: electric
    # green and vivid magenta that cleared the floor and looked like a different
    # brand beside #96331F rust. All three below sit at sat 0.70, val 0.46-0.48.
    "fern":     dict(page="#EBF5E4", accent="#457523", ink="#1F241C", card="#FFFFFF", line="#C0DBAD"),
    "iris":     dict(page="#EDE4F5", accent="#4F2375", ink="#201C24", card="#FFFFFF", line="#C6ADDB"),
    "brass":    dict(page="#F5F2E4", accent="#7A6C24", ink="#24221C", card="#FFFFFF", line="#DBD4AD"),
    # 22 Sep 2026, DataProtection non-lawyer batch (22 faces): the 24 above cannot give 22 accents
    # at CIELAB dE >= 12 (pine/forest 9.8, slate/ink 10.0). These two clear 12.7 against the other
    # 20 and sit at the register's average chroma - the floor first, then the most house-like pick.
    "terracotta": dict(page="#F7EFED", accent="#944234", ink="#241816", card="#FFFFFF", line="#E6D0CB"),
    "violet":     dict(page="#F2F0F7", accent="#6F5194", ink="#1C1726", card="#FFFFFF", line="#D9D0E6"),
    # 22 Sep 2026, Academic Writing 24-26 Oct translate wave (30 faces). The register's own note
    # says it cannot give even 22 accents at CIELAB dE >= 12. Searched: keep every register
    # accent that clears dE 13 against the rest, then fill from candidates at the register's
    # centre of gravity (sat 0.70, val 0.36 to 0.57) in the hue gaps, each clearing 4.8:1 for
    # white type. 30 faces at a minimum pairwise dE of 13.0. `merlot` is ad 01's approved wine.
    # page = accent mixed 96% to white, line = 82%, ink = accent mixed 88% to black.
    "merlot": dict(page="#FAF6F7", accent="#7A1D31", ink="#18060A", card="#FFFFFF", line="#E7D6DA"),
    "oxblood": dict(page="#FAF7F6", accent="#782C24", ink="#180907", card="#FFFFFF", line="#E7D9D8"),
    "leaf": dict(page="#F7FAF6", accent="#3D7824", ink="#0C1807", card="#FFFFFF", line="#DCE7D8"),
    "jade": dict(page="#F6FAF7", accent="#24783D", ink="#07180C", card="#FFFFFF", line="#D8E7DC"),
    "lagoon": dict(page="#F6FAF9", accent="#24786F", ink="#071816", card="#FFFFFF", line="#D8E7E5"),
    "orchid": dict(page="#FAF6FA", accent="#782478", ink="#180718", card="#FFFFFF", line="#E7D8E7"),
    "fuchsia": dict(page="#FBF7F9", accent="#942C75", ink="#1E0917", card="#FFFFFF", line="#ECD9E6"),
    "bronze": dict(page="#F8F8F6", accent="#5C491C", ink="#120F06", card="#FFFFFF", line="#E2DED6"),
    "bottle": dict(page="#F6F8F6", accent="#225C1C", ink="#071206", card="#FFFFFF", line="#D7E2D6"),
    "spruce": dict(page="#F6F8F8", accent="#1C5C5C", ink="#061212", card="#FFFFFF", line="#D6E2E2"),
    "midnight": dict(page="#F6F7F8", accent="#1C355C", ink="#060B12", card="#FFFFFF", line="#D6DBE2"),
    "aubergine": dict(page="#F8F6F8", accent="#551C5C", ink="#110612", card="#FFFFFF", line="#E0D6E2"),
}

ORDER = list(PALETTES)


def get(name_or_dict):
    """Accept a register name or a literal palette dict. Fills in `soft`."""
    if isinstance(name_or_dict, dict):
        p = dict(name_or_dict)
    else:
        if name_or_dict not in PALETTES:
            raise KeyError(
                "unknown palette %r. Known: %s" % (name_or_dict, ", ".join(ORDER)))
        p = dict(PALETTES[name_or_dict])
    for k in ("page", "accent", "ink"):
        if k not in p:
            raise KeyError("palette is missing %r" % k)
    p.setdefault("card", "#FFFFFF")
    p.setdefault("line", "#D8D8D8")
    p.setdefault("soft", p["page"])
    return p


def nth(i):
    """The i-th palette in register order, for kits that do not care which."""
    return ORDER[i % len(ORDER)]
