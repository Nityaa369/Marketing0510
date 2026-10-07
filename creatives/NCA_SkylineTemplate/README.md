# NCA Canada skyline template (permanent)

Built 7 Oct 2026 from the supplied "A lawyer who keeps thinking about Canada?" face
(`reference/original.webp`). Status: DRAFT for Ramanuj. Not approved.

## What stays fixed

Header (LawSikho logo, NCA Canada Bootcamp mark), the maple leaf skyline art, the three route
pillars (NCA exams, then Canadian bar, then practise in Canada), the "We show you how." sticker,
the terms band (Rs 10 refundable; 3 days, 9 hours, live online), the JOIN NOW button with the
Rs 10 burst, and the footer (dates, live online, Rs 10 incl. GST). All cut from the reference ad
into `assets/`.

## What changes per ad

Only two lines, set in `ads.json`:

- `hook`: the call-out question. Names the reader first. Wrap the red words in `<em>`.
- `prize`: the value proposition. Names what they become. Wrap the red words in `<em>`.

The type grows to fill its box for short hooks and shrinks for long ones (no empty gap under the
prize line, nothing pushed off the canvas). Keep hooks under about 8 words.

## Build

```
python3 build.py            # renders every entry in ads.json
python3 build.py other.json # renders another list
```

Writes `html/<stem>.html` and `ads/<stem>.png` (1080 x 1350, rendered at 2x). Needs the
Chromium headless shell and the Inter font. Any default in `template.py` `DEFAULTS` can be
overridden per entry, but do not do that inside one wave: one look, two moving lines.

## The five ads in this folder

| Stem | Hook | Prize |
|---|---|---|
| nca_sky_01_final_year | A final-year law student? | You could practise law in Canada. |
| nca_sky_02_thinking_about_canada | A lawyer who keeps thinking about Canada? | You could practise law in Canada. |
| nca_sky_03_newly_enrolled | A newly enrolled advocate? | You could practise law in Canada too. |
| nca_sky_04_experienced_advocate | An experienced advocate? | You could practise law in Canada too. |
| nca_sky_05_in_court_weekly | In court every week? | You could practise law in Canada as well. |

Hooks 01 to 04 are the ones supplied. 05 is from `docs/HOOKS_NCA_QUESTION_TYPE_2026-10-07.md`
(hook 6). Ad 03's supplied prize line "You could build a Canada option too" was replaced: "a
Canada option" does not name a job (Ramanuj, 21 Sep: "where does it say ... the prize is").

## Critique of the supplied design, against Ramanuj's record

Judged in the standing order. The template fixes items 4 to 6 by default; 1 and 7 need a
decision.

1. **Who.** "A lawyer who keeps thinking about Canada?" is a lawyer (occupation) plus a wish.
   It passed the blind read at 6.0 in the hooks doc, so it is kept, but it is an aspiration
   hook, and aspiration ICPs index 1.05 against 0.98 for plain occupations. The occupation hooks
   (final-year student, newly enrolled, experienced advocate) are the safer cells. Audience
   choice is Ramanuj's call.
2. **Offer.** New, better career in the same craft. Pass.
3. **Prize.** "You could practise law in Canada." names the move and what they become. Pass.
4. **Clarity.** The reference defined NCA as "Checks your eligibility", which does not say what
   NCA is. The template uses the standing gloss: "Canada's check on your Indian law degree."
5. **Rules.** Three faults in the reference, all fixed in the template:
   - "Canada's legal market ~CAD 38B (approx Rs 2.3 lakh crore)" is a market stat on the face.
     Blind readers scored stat reasons lowest (7 Oct), market facts belong on the landing page
     with a source, and our own fact sheet puts the law firm market at about CAD 21 to 22
     billion (IBISWorld, VERIFY), not 38. The band now carries the risk remover instead.
   - "31 OCT – 2 NOV" uses an en dash. Now "31 Oct to 2 Nov". Note that Ramanuj (13 Aug) puts
     dates on the landing page, not the face; the footer dates are a config value if he wants
     them off.
   - "Dramatised email. Not a real learner." on the supplied student and advocate faces belongs
     to the email format only. Dropped here.
   - "India's No.1 Legal upskilling Platform" in the logo lock-up is an unsourced claim. It is
     baked into the logo asset; replace `assets/logo_lawsikho.png` with the plain logo if asked.
6. **Design.** Light background, own palette, big type, visible buy button. Pass. No person in
   the art, so the Indian-faces rule is not triggered. The layout has no live cost evidence yet:
   nothing like it has run. Judge it only after 20 results in a 7-day window.
7. **Landing page.** None shipped. 1 ad = 1 page; build five pages on the 21-step spine
   (`creatives/NCA_LandingTemplate_31Oct-2Nov/`) before launch, each first fold repeating its
   ad's hook and prize word for word.

**Verdict: fix first.** Top fixes: (1) decide which hooks go live (occupation cells first),
(2) five landing pages, (3) confirm dates on or off the face.

Half-asleep test on nca_sky_04: in 3 seconds, who is it for (an experienced advocate), what
job (practise law in Canada), why say yes (Rs 10, refundable, we show you how). Pass.
