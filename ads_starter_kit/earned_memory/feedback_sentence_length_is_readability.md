---
name: feedback_sentence_length_is_readability
description: "readibility id dtill bad in this section" after the type was already fixed - the fault was 54-word sentences and 27-word headings, now L7
metadata:
  type: feedback
---

Ruchika reported the landing pages were unreadable. I fixed measure, leading and the
display face, and she came back pointing at the **closing fold**: *"readibility id dtill
badin this section"*, quoting a 27-word two-sentence heading and a 54-word paragraph with
a colon and a seven-item list run into prose.

**Why:** typography was only half of it. A page can sit at 19px, 1.65 leading and 65
characters a line and still be unreadable because the SENTENCES are too long. No gate in
the repo measured sentence length; nine of them passed that fold.

The ceilings are fitted on the seven CF pages of 15-17 Aug, the only landing pages here
with a measured conversion rate (9.3% to 20.7%):

| | converted | wave 6 before |
|---|---|---|
| longest body sentence | **34 words** | 54 |
| over 40 words | 0 of 623 | 64 (3.2%) |
| longest heading | **14 words** | 37 |
| headings over 16 words | 0 of 77 | 23 of 520 |

**How to apply:** `L7` in `adkit/lp_spine.py` blocks a body sentence over 34 words and a
heading over 16. Three constructions break it, all list-shaped: a colon with the list run
into prose (make the colon a full stop and give the list its own verb), a heading carrying
both *who you are* and *what this does* (heading keeps the clause naming the reader, the
rest drops to a lede), and a day's agenda in one breath. Multi-sentence headings are NOT
the rule - the converting pages have seven of them. Length is.

Also: **the closing fold does not carry the document inventory.** The kit's constant
delivery sentence was printed twice per page, once in the offer section where it belongs
and again in the last 200 pixels before the pay button. See [[feedback_closing_fold_is_ungated]]
and [[feedback_closing_fold_names_the_reader_first]].
