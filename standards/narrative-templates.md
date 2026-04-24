# Narrative templates

Reference for the `narrative_template` field in `deck.md`. Each template is a spine for the deck's argument. Pick the one that matches the deck's shape.

See [`../SPEC.md`](../SPEC.md) for how templates fit into the overall `deck.md` format.

---

## `pyramid` — Pyramid Principle

**Purpose.** Present a governing thought supported by MECE arguments, each proven by slides. This is the McKinsey/Minto approach: start with the answer, then justify it top-down.

**When to use.** Any deck over 10 slides. Multiple parallel arguments. Decks where different readers may skim to different sections and still need to get the point.

**Required fields.**
- `governing_thought` — the one-sentence answer to the deck's question
- `question` — the question the deck answers (recommended)
- `key_line` — a list of MECE arguments, each with `supporting_slides` (recommended)
- `mece_check` — a one-liner explaining why the arguments are MECE (recommended)
- `situation`, `complication`, `resolution` — the opening narrative arc (optional)

**Canonical example.**

```yaml
question: "How do we restore growth to 20%+ by Q2 2026?"
governing_thought: "Three levers — organic, paid mix, reactivation — will recover growth in two quarters at $4M."

situation:    "Growth is our #1 KPI. Board committed to 20% YoY in 2026."
complication: "Q3 2025 growth fell 34% YoY. Acquisition, not retention, is the cause."
resolution:   "Rebuild organic, rebalance paid mix, reactivate dormant users."

key_line:
  - argument: "Organic collapsed; content engine can restore 30% channel share by Q2"
    supporting_slides: [3, 4, 5]
  - argument: "Paid mix is over-concentrated in Meta; reallocation recovers 15% of CAC"
    supporting_slides: [6, 7]
  - argument: "180-day dormant cohort is large and responsive to lifecycle campaigns"
    supporting_slides: [8, 9]

mece_check: "The three levers cover the acquisition funnel (organic) + paid mix + reactivation. No fourth channel at our scale; no overlap between levers."
```

**Pitfalls.**
- Non-MECE key lines (overlapping arguments).
- Missing `mece_check` (no self-audit that the key line covers the ground).
- Body slides that don't ladder up to any argument (orphans).
- Governing thought that restates the question instead of answering it.

---

## `scr` — Situation / Complication / Resolution

**Purpose.** Classic consulting narrative arc. Set up shared reality, expose the problem, propose the resolution. Ideal when the answer is simple enough that full pyramid structure would be overkill.

**When to use.** Short decks (3–10 slides). One-shot updates. Situations where a single resolution is proposed (not multiple alternatives).

**Required fields.**
- `situation` — what the audience already accepts as true
- `complication` — what's wrong, what changed, what's at stake
- `resolution` — what you're recommending

**Canonical example.**

```yaml
situation:    "Growth is our #1 KPI for 2026."
complication: "Q3 growth fell 34% YoY — acquisition broke, not retention."
resolution:   "Three levers will recover growth in two quarters."
```

**Pitfalls.**
- Situations the audience doesn't actually accept (starting from a contested premise).
- Complications that aren't news to the audience.
- Resolutions that don't follow from the complication.
- Stretching SCR to cover a deck that really wants pyramid.

---

## `problem-solution` — Problem / Solution / Why now

**Purpose.** Pitch structure. Establish a problem worth solving, present the solution, justify timing. Optimized for proposals, investments, and external pitches.

**When to use.** Client proposals. Funding pitches. Project charters. Internal asks-for-buy-in.

**Required fields.**
- `problem` — what's broken or underserved
- `solution` — the proposed approach
- `why_now` — why this is the moment to act

**Canonical example.**

```yaml
problem:  "Mid-market B2B companies lose 40% of trial users before activation; current tooling addresses only enterprise."
solution: "Self-serve onboarding platform with built-in activation tracking and intervention triggers."
why_now:  "Mid-market SaaS spend grew 3× in 2025; incumbents focus enterprise-up, leaving a clear window."
```

**Pitfalls.**
- Problem statements that describe the solution in disguise ("companies don't use our tool").
- `why_now` justifications that aren't actually time-bound ("the market is big").
- Solutions broader than the problem.

---

## `update` — Plan / Actual / Next

**Purpose.** Status reporting structure. What did we say we'd do, what did we do, what's next. For steering committees, retros, and check-ins.

**When to use.** Project status updates. Quarterly reviews. Retrospectives. Anywhere the audience needs to compare planned and actual state and agree on next steps.

**Required fields.**
- `plan` — what was planned
- `actual` — what actually happened
- `next` — what's next

**Canonical example.**

```yaml
plan:   "Ship v1 of the onboarding platform by end of Q3; 50 pilot customers onboarded."
actual: "Shipped v1 on schedule; onboarded 38 pilots. Activation rate 62% (target 70%)."
next:   "Iterate on activation flow based on pilot feedback; target 75% activation in Q4; expand to 120 customers."
```

**Pitfalls.**
- `actual` that omits bad news (undermines trust).
- `next` that doesn't address gaps identified in `actual`.
- Vague `plan` that's hard to hold anyone to.

---

## Choosing a template

- Single clear recommendation, short deck → `scr`
- Multiple supporting arguments, longer deck → `pyramid`
- External audience, asking for buy-in or investment → `problem-solution`
- Recurring check-in with a stakeholder group → `update`

A template is a starting point, not a cage. If your deck needs elements from multiple templates, default to `pyramid` and add the SCR arc inside it — pyramid supports this via optional `situation`/`complication`/`resolution` fields.
