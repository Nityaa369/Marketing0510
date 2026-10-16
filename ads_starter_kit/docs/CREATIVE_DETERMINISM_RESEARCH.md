# How other people make creative work repeatable with Claude

Research note, 24 Aug 2026. Written against this folder's own evidence
(`CAMPAIGN_MAP.md`, `RAMANUJ_FEEDBACK.md`, the WhatsApp approval log,
645 shipped landing pages) cross-referenced with outside practice.

---

## 1. The premise needs one correction

Creativity is not deterministic, and neither is the model. Even at temperature 0 an LLM is
not reproducible: the output depends on the *batch* your request happens to land in on the
GPU, because reduction kernels are not batch-invariant. Identical prompt, different
neighbours in the batch, different tokens. Bit-identical output needs custom kernels and
costs roughly 34% throughput. Nobody in a marketing workflow is doing that.

So the people who get consistent creative out of Claude are not controlling the sampler.
**They move the decisions out of the generation step.**

The rule they all converge on, from ad-ops platforms to spec-driven engineering:

> Freeze everything that can be decided in advance. Let the model vary only the wording.

Bannerflow, Celtra, Storyteq and Zuuvi exist to do exactly this in the ad world: one
approved master, brand rules locked, every variant inherits. On the engineering side the
same pattern is called spec-driven development. Same idea: the spec is approved, then
execution is mechanical.

**This folder already knows this.** `CLAUDE.md` says it outright: *"Write this file before
the creative, not after it... one wrong line throws away a whole kit."* The problem is that
the tooling makes the wrong order the easy one. `preflight.py --scaffold` reads
`value_props.md` **out of ads that already exist**. The gate is built, and it is installed
downstream of the thing it is supposed to protect.

---

## 2. Where the back-and-forth actually comes from

Every rejection in the log is at the **idea** layer:

- "the beginning is cryptic - can this be better?"
- "Very complicated / Very cryptic / Why cryptic / Rest cryptic"
- "the flipping burger thing is not clear as a hook - who are you talking to and why"
- "This does not clearly convey what we are proposing"
- "the LPs do not talk about building a solo consulting business in the first fold"

Not one of those is about a colour, a crop, a font, or a payment button. They are all
answerable from four lines of plain text.

But they are *discovered* at the asset layer, after the PNG is rendered and a 549-line
landing page is written. So the unit of rework is a whole kit. That is the entire cost
structure of the problem.

**The fix is not better prompting. It is moving the approval to the cheapest artifact that
can carry the decision.**

---

## 3. The measured waste

Three landing pages from the Section A kit:

| file | lines | bytes |
|---|---|---|
| `lp_01_ai_discount.html` | 549 | 54,801 |
| `lp_02_per_article.html` | 549 | 60,594 |
| `lp_03_rate_never_moves.html` | 550 | 71,868 |

Strip digits and diff LP1 against LP2: **60 differing lines out of 549.** About 89% of
every landing page in this folder is byte-identical boilerplate.

At roughly 15k output tokens per page and 645 pages in the tree, that is on the order of
**9M output tokens spent, of which the large majority is the model retyping the same
chassis.** The genuinely new content per page is the roughly 60-line delta, call it 800
tokens.

This is not a prompting problem. It is an architecture problem: the model is being used as
a text renderer for a job a template call does for free. The Ad Lab's `build_tool.py`
(deleted 28 Sep 2026) showed the right shape once existed here; `adkit` is where it lives now.

Outside research agrees on where agentic token cost hides: review and reflection loops are
the single largest source of waste in multi-agent systems, and 40 to 60% of tool-result
tokens are removable with no loss in quality. Reading 645 HTML files into context to
"check" them is the same mistake in a different costume.

---

## 4. What the good practitioners actually do

Five things, in order of how much they matter here.

### 4.1 Approve a spec sheet, never a draft

One text document, all ICPs, four lines each. Nothing rendered. Ramanuj reads 40 blocks in
one pass and strikes through the ones that are cryptic or that offer the wrong job. Then
build only what survived.

This is precisely the `value_props.md` block that already exists (`better_job`,
`field_definition`, `deliverables`), just moved to the front and sent as the deliverable of
round one.

Cost of a rejection drops from *one kit* to *one paragraph*.

### 4.2 Examples beat rules

The single largest cause of voice drift is zero-shot prompting: asking for "our brand voice"
without showing it. Anthropic's own guidance is blunt about this. Showing two or three
examples is more reliable than describing the format in words, and few-shot is the standard
fix when output is inconsistent run to run.

`CLAUDE.md` is 300 lines of rules and about four examples. Rules say what not to do. They do
not transfer *cadence*. There are 17 approved Section A pairs and 64 logged verdicts sitting
in this repo that are not being used as exemplars.

A `GOLDEN/` directory of six to eight approved ads, copy blocks quoted verbatim, each with
one line on why it passed, is worth more than the next 100 lines of rulebook.

### 4.3 Split the pipeline into hard gates and soft gates

The industrial pattern is two layers, and the standing criticism of skills-only approaches is
exactly that they are upstream-only: they influence generation but provide no downstream
quality gate, no drift detection, nothing that *catches* an off-brand output.

- **Hard gate, deterministic, scripted.** Em-dashes, `href="#"`, `PAYMENT_LINK_PENDING`,
  hedge above CTA, missing field definition, crop bounds. This is `preflight.py`. It works.
  It should never cost a model token.
- **Soft gate, judged.** Is the hook cryptic, is the job one anyone wants, is the biggest
  line naming the prize. This needs a model, but a cheap, isolated, fresh-context one.

`judging-static-ads/engine/creative_judge.py` is already the second layer. It is not wired in
front of handover.

### 4.4 The comprehension test should be run by someone who knows nothing

This is the direct mechanical answer to "cryptic," and it is the highest-value change in
this note.

"Cryptic" is not a taste judgement. It is a measurable failure: a reader who does not already
know the field cannot name the job. That is testable without a human.

Give a subagent with **no brief, no ICP list, no kit context** nothing but the first fold, and
make it answer three questions:

1. Who is this addressed to?
2. What job would I be doing?
3. What will I be able to do on the last day that I cannot do today?

If it cannot answer all three from the fold alone, the ad is cryptic by definition rather than
by opinion. Nine times out of ten the missing piece is step 4 of the first-fold structure, the
one-sentence field definition, exactly as `CLAUDE.md` predicts.

A judge that shares context with the writer will always pass its own work. The isolation is
the whole trick.

### 4.5 Stabilise the prefix so the cache does the work

Pin the system prompt, house rules and golden examples at the front of every run and put all
the varying material at the tail. Reported to cut input cost by more than half on multi-turn
work. Note that response prefilling, the older trick for this, is no longer supported on
Claude 4.6 and later; use structured output and the fixed-prefix layout instead.

---

## 5. Hooks that are not complex

The doctrine is unanimous and matches Rule 2 already in `CLAUDE.md`. What outside practice
adds is mostly *sequencing* and *diagnostics*.

**Classify before writing.** The strongest published ad-copy skill forces four decisions
before a single word: funnel position, awareness level, strategy (sell the click vs sell the
solution), format. A hook is only good relative to an awareness level. Curiosity hooks for
unaware traffic, contrarian for problem-aware and sceptical, social proof for solution-aware
and up. Writing hooks before fixing awareness level is what produces ten variations of the
same bland opener.

**Clarity beats cleverness, and this is not a style preference.** Wordplay imposes a decode
step. A reader who has to decode has already scrolled. Three seconds is the budget.

**One job per hook.** Make one promise, or surface one proof point, or clarify one offer, or
remove one objection. Not two.

**Facts, not adjectives.** Specifics over generalities, self-interest over cleverness.

**No throat-clearing.** "In today's fast-paced world", "Have you ever wondered" is filler that
signals the writer had nothing. Cut to the tension.

**Name the prize, not the pain.** This folder's own V10 finding from the rejected v1 statics
says the same thing independently: the biggest line on the ad must name the prize, not the
pain plus a statistic. It agrees with Rule 1, offer a better job and never threaten.

The house test stays the one already written down, and it is a good one:

> Could someone who has never heard of this field tell you what job they would be doing?

Section 4.4 is how to run it without spending Ramanuj's attention.

---

## 6. What to change here, ranked

1. **Invert the spec gate.** Write `value_props.md` first and send only that for round one
   approval. Make `preflight.py --scaffold` generate an empty skeleton from an ICP list
   rather than from finished ads, so the cheap path is also the correct one.
2. **Template the landing pages.** One chassis, one data file, one renderer. The model writes
   the roughly 60-line delta as data; Python writes the HTML. This alone removes the large
   majority of output tokens in this workflow.
3. **Build `GOLDEN/`.** Six to eight approved pairs, verbatim, one line each on why. Load it
   at the front of every kit run. Retire an equivalent length of prose rules.
4. **Wire the blind comprehension check** into handover, ahead of Ramanuj, as a fresh-context
   subagent that sees only the first fold. Fail closed.
5. **Keep hard checks out of the model.** Anything a regex can decide should never reach a
   token. `preflight.py` already does this; do not let judged review creep into its job.
6. **Log verdicts as training data, not archaeology.** `creative_verdicts.jsonl` and the
   approve/reject marks in `CAMPAIGN_MAP.md` are the golden set. Ramanuj asked for exactly
   this on 12 Aug: *"Share with claude what i approved and what i rejected. And ask why i
   rejected what i rejected."*

---

## Sources

- Thinking Machines Lab, *Defeating Nondeterminism in LLM Inference* — https://thinkingmachines.ai/blog/defeating-nondeterminism-in-llm-inference/
- Zan, *Setting the temperature to zero will make an LLM deterministic?* — https://www.zansara.dev/posts/2026-03-24-temp-0-llm/
- Anthropic, *Increase output consistency* — https://docs.anthropic.com/en/docs/test-and-evaluate/strengthen-guardrails/keep-claude-in-character
- Anthropic, *Prefill Claude's response for greater output control* — https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prefill-claudes-response
- Anthropic, *Prompt engineering best practices for 2026* — https://claude.com/blog/best-practices-for-prompt-engineering
- Rob Palmer, *Claude Code Ad Copy Skill* — https://robpalmer.com/blog/claude-code-ad-copy-skill
- Markup AI, *Claude Skill and the Brand Voice Gap* — https://markup.ai/blog/claude-skill-and-brand-voice/
- Stormy AI, *Claude Projects for Brand Voice Consistency* — https://stormy.ai/blog/claude-projects-social-media-brand-voice-consistency-2026
- CreativeComplete, *AI Ad Creative Production: The Agency Guide* — https://www.creativecomplete.com/blog/ai-ad-creative-production-guide/
- Wireflow, *How to Scale Ad Creative Production with AI* — https://www.wireflow.ai/blog/scale-ad-creative-production
- Glean, *How to optimize token efficiency in agentic systems* — https://www.glean.com/perspectives/how-to-optimize-token-efficiency-in-agentic-systems
- MachineLearningMastery, *Identifying Token Costs Hiding in Your Agentic Loop* — https://machinelearningmastery.com/identifying-token-costs-hiding-in-your-agentic-loop/
- mdflow, *Eval Rubrics for AI Agents: Golden Sets and LLM Judges* — https://mdflow.cz/blog/eval-rubrics-for-ai-agents
- Arize, *LLM as a Judge* — https://arize.com/guides/llm-as-a-judge/
- Wrixon, *Clarity vs Cleverness in Copywriting* — https://wrixon.com/clarity-cleverness-copywriting/
- Aden's Lab, *50 Direct-Response Meta Ad Headlines* — https://www.adenslab.com/blog/direct-response-meta-ad-headlines-copy-paste
