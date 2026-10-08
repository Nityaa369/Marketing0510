# Paste this into Claude Code on any marketing repository. Output: one zip a new Claude can learn from.

You are a senior performance marketer. Build a self-contained learning kit from this repository (and any files I upload in this session) so that a brand new Claude session, with no access to this repo, can read the kit and work on this account as if it had run it for years. Extract, never invent. Every statement in the kit points to a file and line, a commit hash, or a URL with a date. Finish by producing a zip and telling me where it is.

## Part A. Gather (do all of it, in this order)

A1. Map the repo: `git ls-files | wc -l`, `find . -type d -not -path './.git*' | sort`, `git log --oneline | wc -l`. One line per top level folder. Then find and read, word for word, every memory and rule file: `CLAUDE.md`, any `README`, and any file whose name contains GUIDE, RULES, CONTEXT, memory, approval, feedback, lessons, playbook, learned. Note who approves work and who briefs it.

A2. Mine git: `git log --reverse --date=short --format='%h %ad %an %s%n%b' --stat`, then `git show <hash>` for every commit touching text, copy, creative build code or data. Record what was built, what was rejected and why, what was rewritten and what the rewrite teaches. A reversal is a lesson. Also read every uploaded file I give you (zips, docs, exports, chat logs) as primary sources and cite them by filename.

A3. Collect, each with its pointer: every rule (hard "never" rules separate from preferences, each with the rejection, cost or quote behind it); every audience or ICP with its exact wording, offer, price, prize and any cost figure with sample size and date; every ad, hook, page or campaign with a recorded result and the repo's verdict; every creative and landing page (call out, headline, format, palette, CTA, fine print, the rule it serves); every factual claim with source and check date; every number that disagrees with another number; every open item (TODO, PENDING, VERIFY, placeholder link, missing consent, unseen script, unapproved work).

## Part B. Build the kit folder `LEARNING_KIT_<account>_<today>/` with exactly these files

1. `00_START_HERE.md`: what this kit is, the business and offer in five lines, the people and the approval chain, how to read the kit in order, and the three things a new session must never do here. Under 400 words.
2. `01_RULES.md`: every rule, grouped hard then soft, each as one sentence followed by its evidence and pointer. Include the order in which work should be judged, if the repo has one, and the exact verdict format the approver expects.
3. `02_HISTORY_TIMELINE.md`: the account history, dated, from first commit or earliest upload to today. One paragraph per phase, with the lesson at the end of each.
4. `03_AUDIENCES.md`: the audience table (name as worded, offer, price, prize, cost figure, sample, date, source) and a short note on which cells are proven, thin or untested.
5. `04_RESULTS_EVIDENCE.md`: every result with figure, sample, date, verdict, and the repo's own explanation. State which metrics are trusted and which are ignored here, with the reason.
6. `05_CREATIVE_SYSTEM.md`: how creatives and pages are built (templates, build scripts, gates, checks), the formats used, the design rules, and one worked example of a face and its page. Copy the build scripts and templates into `creative_system/` as files.
7. `06_FACTS_AND_SOURCES.md`: every claim with source, date and status (verified, pending, recheck). Unsourced claims in their own list. Contradictions in their own list.
8. `07_OPEN_ITEMS.md`: every blocker and gap, each with pointer, grouped by what unblocks it.
9. `08_MISTAKES_AND_FIXES.md`: the mistakes this account already made and the fix for each, so they are not repeated.
10. `09_PRELAUNCH_CHECKLIST.md`: the checks to run before any new piece goes out, derived only from the rules and mistakes above.
11. `10_GLOSSARY.md`: every internal term, acronym, product name, audience label and metric name, one line each.
12. `history/GIT_LOG.txt` (full `git log --reverse --stat`) and `history/GIT_TEXT_DIFFS.txt` (`git log --reverse -p` restricted to text files: md, txt, py, html, json, csv). These let a new session re-derive anything you summarised.
13. `samples/`: the final version of every creative image (PNG or JPG) and every landing page HTML, named as in the repo. If images push the zip over 25 MB, keep the ten most important and list the rest in `samples/INDEX.md` with their repo paths.
14. `sources/`: copies of every uploaded primary source, unchanged, plus `sources/INDEX.md` saying what each is.
15. `BOOTSTRAP_PROMPT.md`: the prompt a new Claude pastes first. It must say: read `00_START_HERE.md`, then files 01 to 10 in order, then skim `history/` and `samples/`; adopt the rules in `01_RULES.md` as standing instructions; end every critique in the approver's verdict format; treat everything in the kit as the account's record and everything outside it as unverified; and report in one screen (what was read, five rules never to break, five blockers, one thing believed wrong with evidence) before taking a brief.

Writing rules for the kit: plain English, short sentences, no em or en dashes, no praise, no filler, tables only where the row count makes them clearer than a list, every claim with a pointer.

## Part C. Check and ship

C1. Verify: every file in Part B exists and is non-empty; every pointer you cite resolves (`grep` for a sample of 20); no sentence in the kit lacks a pointer or a source; no secrets, tokens, personal phone numbers or emails are inside (grep for `@`, `token`, `key`, `password`, ten digit numbers) and redact any you find, noting the redaction in `00_START_HERE.md`.

C2. Zip the folder as `LEARNING_KIT_<account>_<today>.zip`. Report its size and file count. If it is over 25 MB, make `..._text.zip` (everything except samples and sources) and `..._media.zip` (samples and sources) so each is under 25 MB.

C3. Report in one screen: commits, files, creatives, pages, facts and uploads read; the zip path and size; the five rules; the five blockers; one thing you believe is wrong in the repo, with evidence. Then stop.
