# working-backwards

A Claude skill for the Working Backwards method: write the press release and FAQ for a product before building it, then build only what the press release promised.

## What it does

- **Draft** a PR/FAQ from an idea: a one-page press release, customer and internal FAQs, and a list of assumptions to validate.
- **Coach** you through the five customer questions one at a time, pushing back on weak answers before anything is written.
- **Critique** an existing PR/FAQ as a skeptical senior reader would.
- **Build** software ideas test-first. Each promise in the press release becomes an acceptance criterion with a test, and the final report checks the build against the release.
- **Six-page narrative**, on request.

It does not invent metrics, research, or customers. Gaps are marked as placeholders or open questions.

## Install

In Claude Code:

```
/plugin marketplace add JBell87/working-backwards
/plugin install working-backwards@working-backwards
```

Or copy `skills/working-backwards/` into `~/.claude/skills/` (or a project's `.claude/skills/`). In the Claude apps, upload the same folder as a skill.

## Use

Ask in plain words:

- "Working backwards on this idea: ..."
- "Coach me through a PR/FAQ for ..."
- "Review my PR/FAQ before I send it"

## The build step and Superpowers

For software ideas, the skill continues from the PR/FAQ into a build. If [Superpowers](https://github.com/obra/superpowers) is installed, it hands the PR/FAQ to that plugin's brainstorming, planning, and test-driven-development skills. If not, it runs a plain test-first loop itself.

```
/plugin install superpowers@claude-plugins-official
```

**The blocking gate.** The build starts without asking, unless the PR/FAQ rests on a guess that decides *what gets built* (for example the customer's platform or data format). Those are marked "blocking" and the skill asks about them first. Guesses that only affect whether the idea is worth shipping (market size, price) do not stop the build.

## Examples

- [`examples/draft-and-build.md`](examples/draft-and-build.md): a PR/FAQ for a small command-line tool, its acceptance criteria, and the build report. The code and tests it produced are in [`examples/overdue/`](examples/overdue/).
- [`examples/critique.md`](examples/critique.md): a review of a deliberately weak PR/FAQ.

## Status

Early. The draft, critique, and built-in build loop have been exercised on the examples above. The Superpowers handoff, coach mode, and six-page narrative have not yet been tested.

## Licence and credits

MIT. Based on the Working Backwards process described in Colin Bryar and Bill Carr's book *Working Backwards*. Not affiliated with or endorsed by Amazon. Superpowers is a separate open-source project by Jesse Vincent.
