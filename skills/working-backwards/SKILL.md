---
name: working-backwards
description: Apply the Working Backwards method - draft, coach, or critique a PR/FAQ (optionally a six-page narrative) for a product, feature, service, or internal initiative, then for software ideas hand the PR/FAQ to the build-from-prfaq skill to be built. Use whenever the user mentions working backwards, PR/FAQ, PRFAQ, a future press release, the five customer questions, a six-pager, or wants to pressure-test an idea from the customer's point of view before building it, even if they don't name the method.
---

# Working Backwards

Working Backwards starts from the customer experience you want to exist and works back to what must be built. The main artifact is the PR/FAQ: a one-page press release written as if the product has already launched, followed by frequently asked questions that surface the hard issues. The document is a thinking tool, not marketing copy. Its value is that vague ideas cannot survive being written down in plain customer language, so the job of this skill is to force clarity, not to make an idea sound good.

## Pick the mode

Work out which of these the user wants; if it is unclear, ask once.

- **Draft**: the user has an idea and wants a PR/FAQ written.
- **Coach**: the user wants to be walked through the thinking. Ask the five questions one at a time and push back on weak answers before writing anything.
- **Critique**: the user has an existing PR/FAQ. Review it as a skeptical senior reader would (see Review checklist) and do not rewrite it unless asked.

Draft and Coach continue into Step 4 (handing off to the build) when the idea is software and the session can write and run code. Critique stops at the review.

## Step 1: The five customer questions

Before drafting, get an answer to each. If the user's material already answers one, don't re-ask it.

1. Who is the customer? One specific segment, not "everyone" or "users".
2. What is the customer problem or opportunity? Stated in the customer's words, with how they cope today.
3. What is the most important customer benefit? One, not a list. If there are three, the idea is not focused yet.
4. How do you know what the customer needs or wants? Evidence: data, research, support tickets, anecdotes. Label anything that is a guess.
5. What does the customer experience look like? What the customer actually does, start to finish.

When answers are thin, say so and ask a sharper follow-up rather than filling the gap with plausible-sounding invention. In Draft mode with a user who wants speed, proceed on stated assumptions but list every one of them at the end under "Assumptions to validate". Never invent metrics, research findings, or real customer names; use clearly marked placeholders such as [X% - needs data].

## Step 2: Write the press release

Keep it to about one page. Write for the customer, not for colleagues: no internal jargon, no technology names unless the customer cares about them, no hedging words ("might", "aims to", "best-in-class"). Date it on a realistic future launch day, which forces a view on scope.

Use this structure:

```
# [Headline: product name + the benefit, in words the customer would use]
*[Subheading: one sentence - who the customer is and what they gain]*

**[City] - [Future launch date]** - [Summary paragraph: what launched and the single most important benefit. A reader who stops here should understand the product.]

[Problem paragraph: the customer's problem today, concretely, and why existing options fall short.]

[Solution paragraph: how the product solves that problem. The experience, not the architecture.]

[Leader quote: why the company built this - the conviction behind it, not a feature recap.]

[How it works: what the customer does to get started and use it, in a few sentences.]

[Customer quote: a fictional but believable customer describing the before and after in specific terms. Mark it as illustrative.]

[Call to action: how to get it, where, and price if relevant.]
```

For internal tools or process changes, the same structure works: the customer is the internal team, and the release reads like an internal announcement.

## Step 3: Write the FAQ

The FAQ is where the difficult questions get answered honestly. A FAQ made only of easy questions is a failed FAQ. Split it in two.

**Customer FAQ** - what a customer would ask on reading the release: price, how it differs from what they use now, what it does not do, setup effort, data and privacy, what happens if it goes wrong.

**Internal FAQ** - what leadership, finance, legal, and engineering would ask:
- How big is the opportunity, and how was it estimated?
- What are the unit economics and the investment required?
- What are the hardest technical or operational problems?
- What are the top reasons this fails?
- What are we deliberately not doing in the first version?
- What dependencies, legal, or policy issues exist?
- Why now, and why us?
- How will success be measured, and what result would make us stop?

Answer each directly. Where the answer is unknown, write "Unknown - to find out: [how]" rather than a confident-sounding paragraph. Unknowns flagged clearly are the most useful output of the exercise.

## Review checklist (Critique mode, and self-check before delivering a draft)

- Could a customer read the headline and first paragraph and want it?
- Is there exactly one customer and one primary benefit?
- Is the problem real and evidenced, or asserted?
- Does the solution paragraph describe an experience or just list features?
- Would the customer quote be said by a real person?
- Is anything in the release written for insiders?
- Does the internal FAQ include the questions the author would least like to be asked?
- Are numbers sourced, or marked as placeholders?
- Is the benefit big enough to be worth building? If the honest press release is boring, say so; that is a legitimate and valuable finding.

In Critique mode, lead with the two or three issues that most threaten the idea, quote the specific lines involved, and suggest the question the author needs to answer. Be direct; a polite review that misses the fatal flaw wastes the author's time.

## Output

Deliver the PR/FAQ as a single document: the press release, then Customer FAQ, then Internal FAQ, then "Assumptions to validate" and "Open questions". If the user asks for a specific file format, use it; otherwise use whatever document format the session offers for writing the user will keep and share. When working in a code repository, also save it as `docs/prfaq/<idea-slug>.md` so the build can refer to it.

In "Assumptions to validate", mark each assumption **blocking** or **non-blocking** and give the reason in a few words. The test is about the build, not the business: if this assumption turned out to be wrong, would the code have to be thrown away or substantially redone?

- Blocking: it decides what gets built. Examples: which platform the customer is on, what format their data arrives in, whether a third-party service allows the access the product depends on, whether something is lawful to do with the customer's data.
- Non-blocking: it decides whether the thing is worth shipping or how well it sells, but the same code gets written either way. Examples: market size, price, whether customers will prefer it to an alternative.

Something the user stated as a fact or a requirement is not an assumption; do not gate on it. Mark as blocking only what was guessed in order to fill a gap. When unsure, mark it blocking: a wrongly raised question costs the user one reply, while a wrong build costs the whole run.

If the idea is not software, or the session cannot write and run code, stop here and offer one next step: a critique pass, a six-page narrative, or turning the open questions into a validation plan. Otherwise go on to Step 4.

Expect iteration. Real PR/FAQs go through many revisions, and a revision that narrows the customer or cuts scope is progress.

## Step 4: Hand off to the build (software ideas)

The PR/FAQ is the contract for the build: software gets built until every sentence of it is accurate. This skill's part ends with a PR/FAQ that is fit to be that contract; the `build-from-prfaq` skill does the rest.

**Gate.** Hand off without asking for permission, with two exceptions.

- If any assumption is marked blocking, stop first. List the blocking assumptions, each with the specific question that would settle it and the answer that was assumed, and ask the user to confirm or correct them. They can also say "build anyway"; in that case proceed, and keep the assumption visible in the document. Once answered, update the PR/FAQ and continue without further confirmation.
- If the user asked only for the document, stop after delivering it.

**Hand off.** Make sure the PR/FAQ is saved at `docs/prfaq/<idea-slug>.md`, then invoke the `build-from-prfaq` skill (it may be listed with a plugin prefix, such as `working-backwards:build-from-prfaq`) with that path. It locks the document, derives a build spec from it, has the spec reviewed, and asks the user to approve the build plan before any code is written. Do not start planning or building here, and do not edit the PR/FAQ after handing off: from that point only the user can change it.

If `build-from-prfaq` is not available (this skill was installed on its own, or the session cannot write and run code), stop after delivering the PR/FAQ. Say in one line that the build step is part of the working-backwards plugin for Claude Code, and offer the non-build next steps above.

## Optional: six-page narrative

Write this only when the user asks for a six-pager or narrative, or when the decision is broader than one product (a strategy, an annual plan, a large investment). It complements the PR/FAQ; it does not replace it.

A six-pager is full prose that a room reads silently before discussing, so it must stand alone without a presenter. No bullet-point arguments: bullets hide the reasoning that connects one point to the next, which is exactly what readers need to challenge. Six pages is the ceiling for the body; data and detail go in appendices.

Usual sections, adapted to the subject: context and the question being decided; goals with measurable targets; tenets (the principles that settle trade-offs); current state with data; lessons learned; the proposal and the alternatives rejected, with reasons; risks; what is being asked of the reader. The same rules on evidence apply: no invented numbers, placeholders marked.

---

Based on the Working Backwards process described in Colin Bryar and Bill Carr's book *Working Backwards*. Not affiliated with or endorsed by Amazon.
