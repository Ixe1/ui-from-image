# Examples

This directory is intended to hold a small before-and-after example pair for the `ui-from-image` skill.

Recommended files:

- `concept-source.png`: the original generated UI concept image used as the visual source of truth
- `implementation-full-page.png`: a full-height screenshot of the implemented webpage created from that concept

Why this pair is useful:

- it shows the kind of input the skill starts from
- it shows the quality bar for the implemented result
- it gives the repository a concrete example without requiring readers to infer the workflow from text alone

Suggested capture standard for `implementation-full-page.png`:

- capture the full page height, not just the first viewport
- use Playwright or another browser automation tool so the capture is consistent and repeatable
- avoid browser zoom or CSS scaling hacks during capture
- prefer the final, polished page state rather than an intermediate draft

Once both images are available, they can be referenced directly from the top-level README.
