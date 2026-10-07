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

## The ten ads in this folder: one per ICP cell

One ad per cell of the wave 3 shortlist (`docs/ICPs_NCA_Wave3_31Oct-2Nov2026.md`). Each has
its own validation hook (the call-out names the reader's situation in their words) and its own
offer-specific prize line (the "Value proposition (plain head)" column, with the same-desk heads
on cells 8 and 10 replaced as that table records). Numbers for cells 4 and 5 stay in targeting.

| Stem | ICP | Hook | Prize |
|---|---|---|---|
| nca_sky_01_broad_thinking_about_canada | Lawyers who want to practise in Canada (broad capture) | A lawyer who keeps thinking about Canada? | You could practise law in Canada with your Indian LLB. |
| nca_sky_02_final_year_student | Final-year law students | A final-year law student? | Graduate in India. Start a Canadian law career. |
| nca_sky_03_fresh_graduate | Fresh law graduates (LLB done, not yet practising) | LLB done, not yet practising? | Your Indian LLB can take you to practise in Canada. |
| nca_sky_04_newly_enrolled_advocate | Newly enrolled advocates (0 to 2 years in targeting, never on the face) | A newly enrolled advocate? | You could qualify for Canada alongside your first years in court. |
| nca_sky_05_experienced_advocate | Experienced advocates (5+ years in targeting, never on the face) | An experienced advocate? | Keep your practice. Add a Canadian licence. |
| nca_sky_06_litigator | Litigators and court lawyers | In court every week? | You could qualify to serve Canadian clients from India. |
| nca_sky_07_corporate_contract_lawyer | Corporate and contract lawyers | A corporate or contract lawyer? | Qualify in Canada. Draft for Canadian clients too. |
| nca_sky_08_law_firm_associate | Law firm associates | A law firm associate? | You could qualify as a Canadian lawyer. |
| nca_sky_09_moving_to_canada | Lawyers planning to move abroad (IELTS, PR plans) | A lawyer planning to move to Canada? | Take your law career with you. |
| nca_sky_10_in_house_counsel | In-house counsel | In-house counsel at an Indian company? | You could become a Canada-qualified lawyer. |

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

Half-asleep test on nca_sky_05_experienced_advocate: in 3 seconds, who is it for (an experienced advocate), what
job (practise law in Canada), why say yes (Rs 10, refundable, we show you how). Pass.

## Landing pages (added 7 Oct 2026)

`landing/build_lp.py` builds one page per ad on the 21-step spine from
`creatives/NCA_LandingTemplate_31Oct-2Nov/template.py`, with a skyline first fold that repeats
the ad's hook and prize word for word, the route pillars in the ad's words, and the ad palette.
`landing/pages/` is the launch copy; `landing/preview/` highlights open items; `landing/GAPS.md`
lists them. The pay link is `#PAYMENT_LINK_PENDING` everywhere and blocks launch.

**No disclaimer, on instruction (7 Oct).** The launch pages end with a live-only sign-off, not
the legal block. Flag for Ramanuj: Ruchika's 21-step order and his Rule 5 both place the one
disclaimer at the very end of the page, and the dropped block carried "we do not promise
admission, a licence, a job or an income". Dropping it entirely is a legal exposure call that
only he can clear. The preview copies keep every open-item marker.
