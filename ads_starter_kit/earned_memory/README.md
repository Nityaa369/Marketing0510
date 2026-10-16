# earned_memory

132 notes, one fact each, recording what was learned from specific builds: what the reviewer
said, what a measurement showed, and what to do differently next time. `MEMORY.md` is the
index. Each note carries its own `description` line, so skimming the index is usually enough
to find the one you need.

**Read these before arguing with a rule.** Most rules in `SOP/` and
`AD_CREATION_DIRECTOR.md` are a compression of several of these notes, and the note keeps the
evidence the rule dropped: the ad name, the cost, the date, the exact words.

Four kinds, marked in each note's `metadata.type`:

- `feedback` - guidance given on how the work should be done, with the why. The largest group.
- `project` - the state of an ongoing piece of work, or a campaign's history.
- `user` - who the people involved are.
- `reference` - pointers to external sources, sheets and dashboards.

**These are dated observations, not standing law.** A note reflects what was true when it was
written. If one names a file, a function or a flag, check it still exists before acting on it.
Where a note and a current SOP disagree, the SOP wins and the note tells you what the SOP is
for.

## Making them your own memory

They came out of Ruchika's project memory, which is per machine and per user, so they do not
travel into yours automatically. Two ways to use them:

1. **Leave them here and read them.** They are plain markdown in a folder Claude can search.
   This is enough for most work: ask Claude to search `earned_memory/` for the topic you are
   about to touch.
2. **Import the ones you want into your own memory**, so they load in every future session
   without being asked for. If your Claude Code has the `import-memory` skill, point it at
   this folder. Otherwise copy the files you want into your own project memory directory and
   add a one-line pointer for each in your own `MEMORY.md`.

Do not import all 132 blindly. The ones worth having loaded on day one are the standing
preferences, not the campaign histories:

- `feedback_ad_clarity_rules.md` - the clarity rules, with the verdicts behind them
- `feedback_icp_named_first.md` - name the audience before the hook
- `feedback_half_asleep_callouts.md` - who the call-out is written for
- `feedback_house_ad_formula.md` - the two-part hook and the believable artefact
- `feedback_only_ramanuj_approval_counts.md` - whose approval is evidence
- `feedback_run_every_gate.md` - never a subset of the gates
- `feedback_landing_page_standard.md` and `project_21_step_lp_spine.md` - the page
- `feedback_simple_technical_english.md` - the voice
- `feedback_every_statement_must_be_sourced.md` - claims trace to the camp script
- `feedback_blind_gates_catch_what_regex_cannot.md` - why the blind readers exist
