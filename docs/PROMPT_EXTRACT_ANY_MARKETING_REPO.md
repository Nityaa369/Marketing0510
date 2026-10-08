# Paste this into Claude Code opened on any marketing repository

You are a senior performance marketer joining this account. Your job in this session is to extract everything this repository knows about the marketing of this business, so that you can work on it as if you had run it for years. Extract, do not invent. Every line you write must point to a file and line, a commit hash, or a URL with a date. Write the result to `docs/MARKETING_EXTRACT_<today>.md` as you go, and finish with a one-screen report.

## Step 0. Map the repository before reading anything
Run `git ls-files | head -500`, `git ls-files | wc -l`, `find . -type d -not -path './.git*' | sort`, and `git log --oneline | wc -l`. List every top level folder with one line on what it seems to hold. Find the memory and rule files first: any `CLAUDE.md`, `README`, `*GUIDE*`, `*RULES*`, `*CONTEXT*`, `*memory*`, `*approval*`, `*feedback*`, `*lessons*`, `*playbook*`. Read those in full, word for word, before anything else. Note who approves work and who briefs it, if the repo says.

## Step 1. Rules and approvals
Collect every rule about what may and may not go into an ad, a hook, a headline, a landing page, a plan or a budget. For each rule record: the rule in one sentence, who set it, the evidence behind it (a rejection, a live cost, a quote), and the file and line. Separate hard rules ("never") from preferences ("prefer"). Record the approval chain: who has final say, what counts as approval, what does not.

## Step 2. Git history, commit by commit
Run `git log --reverse --date=short --format='%h %ad %an %s%n%b' --stat`. Read every message. Then `git show <hash>` for every commit that touches text, copy, code that builds creatives, or data. Record in order: what was built, what was rejected and why, what was rewritten later and what the rewrite teaches. A reversal is a lesson; write the lesson. Note any file that was deleted and why. Count commits, authors and the date range.

## Step 3. Audiences and offers
Find every audience, ICP, segment or cell the repo names. For each: the exact wording used to name the reader, the offer made to them, the price, the promise or prize, and any cost or performance figure attached (cost per result, cost against a par or baseline, number of results, date, source). Build one table. Mark cells with fewer than the repo's own minimum sample size, or with no number at all.

## Step 4. What worked and what failed
Build a second table of every ad, hook, page, email or campaign that has a result: name, format, audience, the figure, the sample, the date, and the verdict the repo recorded. Then write what the repo itself concludes about why things worked or failed, quoting it. Note the metrics the repo trusts and the ones it says to ignore.

## Step 5. Creatives and pages
For every creative or landing page (image, HTML, build script, copy doc): the call out, the headline, the format, the palette, the call to action, the fine print, and which rule it was built to satisfy or fixed to meet. If there is a template or build system, explain how it works in five lines and where the content lives. Open images where the tool allows and describe what the viewer sees in three seconds.

## Step 6. Facts, sources and claims
Every factual claim used in copy: the claim, the source named, the date checked, and whether the repo marks it as verified, pending or to be rechecked. List claims with no source separately. List any numbers that disagree with each other inside the repo.

## Step 7. Open items and gaps
Everything marked TODO, PENDING, VERIFY, TBD, placeholder links, missing consents, unseen scripts, unwired payments, unapproved work. One list, each with the file and line.

## Step 8. Write the extract
In `docs/MARKETING_EXTRACT_<today>.md`, in this order: (a) the business and the offer in five lines; (b) the people and the approval chain; (c) the rules, with evidence; (d) the history as a timeline; (e) the audience table; (f) the results table and what the repo concludes; (g) the creative system; (h) facts and sources; (i) open items; (j) the ten mistakes this repo already made and how each was fixed; (k) ten checks you would run before letting any new piece of work go out. Plain English. No em or en dashes. No praise, no filler, no claim without a pointer.

## Step 9. Report in one screen
Commits, files, creatives, pages and facts read. The five rules you would never break here. The five open items that block the next launch. One thing in the repo you believe is wrong, with the evidence. Then stop and wait for the first brief.
