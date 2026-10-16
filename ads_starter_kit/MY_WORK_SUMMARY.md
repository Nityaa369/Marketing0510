# What I do: a briefing for another Claude

I run performance creative for Meta ads at **LawSikho** and **SkillArbitrage**, two Indian
online education brands. My work is building **static ads and their landing pages** for
low-priced live bootcamps, then checking what they cost once they run. Most of my
work happens in a Claude Code workspace (`ads tasks/`), which holds every kit, the SOPs
and the checking tools.

## The business

- **The product:** 3-day live online bootcamps, usually **Rs 10** (price includes GST,
  refundable anytime). They are **live only, with no recordings**. Each camp is the top of
  a funnel into a paid course.
- **The brands, kept separate and never co-branded:**
  - **LawSikho** sells legal careers: data protection/DPDP, arbitration, patents, US paralegal,
    independent director.
  - **SkillArbitrage** sells non-legal careers: content writing, corporate finance, US
    accounting, HR, academic writing, AI for senior professionals, remote work for women,
    consulting.
- **The reader** is an Indian working professional, student, or woman on a career break.
  They see the ad on Facebook or Instagram, often while half asleep, scrolling on a phone.
- **What we measure:** cost per purchase or lead (CPP/CPL) at campaign level, over a 7-day
  window. CTR does not predict cost, so I don't use it to judge an ad.
- **The approver:** **Ramanuj** (founder). Only his approval counts. An in-house "approved"
  label is not evidence.

## What a job looks like

A camp is scheduled (the dates live in a Google Sheet). I build a **kit** for it: a folder
holding a wave of ad + landing page pairs, often 5 to 20 of them, each aimed at a
different **ICP** (a specific reader, e.g. "hospital HR executive" or "company secretary").
Then it ships to the media buyer as a zip.

Work is approved in this order, cheapest rejection first:

1. **ICP list.** Each ICP is scored on severity, frequency, activation, reachability and fit,
   and names the `buying_pressure` behind it: why this person would pay now.
2. **`value_props.md`.** For each ad: the better job on offer, a one-sentence
   plain-English definition of the field, 3+ named deliverables, and the reader's awareness
   level.
3. **`hooks.md`.** The headline text for each ad, approved as a table before anything is
   designed.
4. **One ad + its landing page**, then the rest.
5. **The ship zip:** ads, LPs, `ad_copy.md` (primary text, headlines), a README with the
   launch spec (account, ABO/CBO, budgets, GrowthX funnel slugs), and `manifest.json`.

Ads are rendered from HTML using a shared chassis (`adkit/`) with 11+ named layouts:
notice, search, chat, venn, notify, call, worklist and others. Landing pages follow one
spine, about 1,600 to 1,800 words written as a numbered argument with a sticky CTA. The
pay button opens a GrowthX checkout.

## The rules that matter most (learned from rejections)

1. **Offer a better career. Never threaten.** The reader's current work is an asset they
   trade up with. No regulator or liability fear, no "more admin at the same desk", no AI
   fear, no income promise, no placement guarantee.
2. **No assumed knowledge ("cryptic").** Someone who has never heard of the field must be
   able to say what job they'd be doing. Every ad and page defines the field in one
   ordinary sentence.
3. **First-fold order on the page:** who you are (as a question), then a qualifier row,
   the offer in plain words, the field definition, named deliverables, and finally price,
   dates, live-only and refundable.
4. **Name the ICP first**, in 2 to 6 words, big (the call-out and headline must be at
   least 64px). Say what the reader gains in about 10 words, with the field named. No
   riddles or wordplay.
5. **1 ad = 1 landing page**, shipped together. Each ad gets its own colour palette (a
   measurable distance apart), and the pages in one kit must argue differently. Pages
   that share 80% or more of their sentences are blocked.
6. **The page must be able to take money.** It needs a real checkout, tested in a browser,
   and no disclaimer paragraph above the pay button.
7. **Every claim must be sourced**, and every camp claim must trace to the actual bootcamp
   script. No false "be early" or "no one ahead of you" claims.
8. **House style:** no em-dashes or en-dashes (write "3 to 5 Oct"), no "this is not for you
   if..." blocks, and plain technical English (not literary, not dumbed down).

## The quality gates

Everything goes through `python check_all.py <kit>`, which runs every checker. A gate that
crashed or saw zero files counts as ERROR, never PASS. It covers:

- **Compliance and value props:** `preflight.py`
- **Two-second clarity:** `simplicity.py` (face copy, type size, contrast, alignment)
- **Hook vagueness:** `hook_rules.py`
- **Layout:** `adkit/fit` and `gaps` (overlap, clipping, empty space)
- **Blind readers:** `blind_reader.py` and `closing_reader.py`. Fresh subagents with no
  context read the ad's first fold, or the page's closing CTA, alongside ads we know
  worked, and try to say who it's for, what the job is, and what they'll be able to do.
- **The final static-ad judge:** `creative_judge.py`

The checkers are tuned against Ramanuj's approvals and live cost data. When a rule
disagrees with an ad that was approved or ran cheap, the ad wins and the rule gets fixed.
Anything learned in a build goes back into the tooling or SOPs the same day.

## Analysis work

Besides building, I pull and read performance data:

- **Sources:** Meta Ads (a script on a System User token), GrowthX funnel and lead reports,
  and sometimes Google Ads.
- **Report format:** always day by day. Columns: ad, spend, buyers, CPP, link to the ad.
  No impressions, CTR or CPM.
- **Diagnosing an ad:** judge on 7 days and 20+ buyers, never a part-day. Look at the ad's
  own numbers before rewriting its copy (the same copy on a different design has cost 10x
  more).
- **What we've learned so far:**
  - The ICP is the biggest lever. Naming a specific trained occupation beats clever angles.
  - Pay-chart ads cost about 2.3x the campaign average.
  - Page length doesn't predict conversion.

## Where to find things (in my workspace)

- `AD_CREATION_DIRECTOR.md` is the single guide for building an ad + landing page pair.
- `CLAUDE.md` holds the core rules (Rules 1 to 5) and the handover checklist.
- `SOP/00_CONSTANTS.md` has every decision-changing rule on one page.
- `SOP/01` to `SOP/10` cover process, the launch spec, landing pages, ad copy and design
  styles.
- `CAMPAIGN_MAP.md` lists every campaign and wave, with verdicts.
- `python -m adkit.brief "<ICP>"` shows past performance and the closest earlier ads for a
  reader.

## How to help me well

- Build on evidence: approved ads, live cost, the camp script. Not generic US
  direct-response doctrine. RMBC and similar frameworks give a first draft, not a finished
  ad.
- Run the full check, and report what it found honestly, including failures.
- Keep copy simple, specific and centred on the reader: who they are, the better job, and
  what the field is, in plain words.
