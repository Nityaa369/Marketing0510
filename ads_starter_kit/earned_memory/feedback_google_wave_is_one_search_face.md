---
name: feedback-google-wave-is-one-search-face
description: "Google cannot run carousels, so a Meta carousel wave gets a twin wave of single faces in the search layout, same readers and same LPs"
metadata:
  node_type: memory
  type: feedback
  originSessionId: aa0c007e-3e70-4ea6-a4e7-b40c8fc6743d
  modified: 2026-09-24T07:55:33.392Z
---

Ruchika, 24 Sep 2026, on the two Tech Law carousel zips: *"create search ad style single
ads for google since we cannot launch carousels there. the lps will remain the same."*

The Google twin of a carousel wave is built like this:

- **One face per reader**, `layout="search"` from `adkit`. It is the only layout in the repo
  that carries a whole argument on one face: the reader's own query in a search bar, then
  the offer card. On Google the device is literally true.
- **Nothing selling is re-decided.** Reader, offer, take-aways and landing page come from
  the carousel wave; only the container changes. `hooks.md`, `value_props.md` and `ad_copy.md`
  are GENERATED from the carousel kit's approved files, never retyped.
- **The definition goes on the face**, unlike a Meta face. A Google reader has not seen the
  account before, so the field cannot be assumed.
- **Same LPs, same slugs, nothing to redeploy.** The pages ship inside the kit only so it is
  self-contained and the gates can run.
- **Google also needs words**: authored headlines (<=40 chars) and descriptions (<=90) per
  ad in `ad_copy.md`. Author them; never cut the face's copy to length, which ends a line
  mid-phrase and produces exactly the riddle the face avoids.

Expect `creative_judge` C21 ("anchor copy over 600 chars") on every face. A full-content
single face runs ~1,150 characters by construction; it is a with-changes note, not a reject,
and the whole wave carries it.

Ruchika restated the copy bar in the same breath: *"direct, easy to understand, no riddles,
someone half asleep should be able to get it."* See [[feedback-half-asleep-callouts]],
[[feedback-callout-no-riddles]] and [[feedback-search-layout]].
