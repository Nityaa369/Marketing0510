---
name: feedback-whatsapp-status-fakes-frequency
description: "High campaign frequency on this account is WhatsApp Status, not audience fatigue; split by publisher_platform before calling fatigue. Ad-set reach from the API is also unreliable."
metadata:
  node_type: memory
  type: feedback
  originSessionId: ca6c6075-c746-4476-a92c-4c0a0b45026d
  modified: 2026-09-24T13:04:44.862Z
---

On 24 Sep 2026 I told Ruchika that Legal AI, Contract Drafting, SQE, Senior AI, Data Privacy
and Criminal Litigation needed new ads because of their campaign frequency (7.5 to 14 over
7 days). Broken down by `publisher_platform`, every one of those numbers came from
**WhatsApp Status**:
- WhatsApp Status took 76-85% of impressions but only 3-6% of spend.
- Its frequency was 20 to 262.
- On Instagram and Facebook, where the money goes, frequency was 2.2 to 3.5 for all 18 live
  campaigns.

WhatsApp Status also had Data Privacy's cheapest buyers (Rs 80, n=49), so it is not waste.

Also: `<adset>/insights` reach was impossible on the same day. The DP healthcare ad set
reported 994k reach, while its own ads summed to 125k. Campaign-level and ad-level reach
agree with each other; ad-set reach does not. Every DP ad set was broad (all India, 22-65,
Advantage+ audience, ~490-575M estimated), so "narrow audience" was never the cause.

**Why:** a fatigue call built on frequency sends the team to build ads, or widen targeting,
that nothing needs.

**How to apply:** before any frequency or fatigue claim, pull `breakdowns=publisher_platform`
and judge frequency on Instagram and Facebook only. Do the same for CTR, because Status
impressions dilute it. Never use ad-set-level reach; use ad or campaign level.
`daily_report.py`'s FREQ_* flags use the blended number and share this flaw.

Related: [[feedback-daily-report-chat-style]], [[feedback-contradiction-means-failed-test]], [[project-dpdp-history-and-icps]]
