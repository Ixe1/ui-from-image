---
name: ui-from-image
description: Convert one or more webpage/app UI screenshots into a high-fidelity responsive implementation, either as a standalone page or by adapting an existing frontend. Prioritize exact viewport matching, typography/icon audits, explicit spacing and colour matching, browser screenshot comparison, and repeated refinement until no obvious mismatches remain. Handle missing assets by using supplied files, generating them when explicitly requested and available, or otherwise using placeholders plus a single copy-paste code block containing one standalone generation prompt per remaining asset.
---

## Mission

Treat the provided reference image(s) as the visual source of truth.

Accuracy beats speed. Do not stop at "close enough". The task is not finished when the page merely works; it is finished when the rendered result is a close visual match and there are no obvious mismatches left.

Bias toward more verification passes rather than fewer. If there is a realistic chance that text is wrong, a control is crowded, spacing is fragile, or a layout bug is hidden by one viewport, keep iterating.

Do not describe the result as "good enough", "ready to ship", or equivalent unless all mandatory verification and reporting steps in this skill are complete and no known visible mismatch remains beyond clearly stated minor uncertainty.

## Default output

Unless the repo already dictates another structure, use:
- `index.html`
- `styles.css`
- `script.js`

If adapting an existing frontend/framework, follow the repo's file structure while keeping markup, styling, and behavior as cleanly separated as the framework allows.

## Operating mode

- For standalone work, default to plain HTML/CSS/JS unless the environment already includes a styling system the user wants to keep.
- Reuse the repo's existing Tailwind/DaisyUI setup when present.
- If the repo already has a different established styling system, do not introduce Tailwind/DaisyUI as a competing second system unless the user explicitly asks for it.
- If Tailwind/DaisyUI are already available or explicitly requested, treat them as implementation tools rather than design authority. Override defaults whenever the screenshot differs.
- First achieve fidelity at the exact reference dimensions of the primary screenshot.
- For desktop webpage work, do not treat a narrow mockup or POC screenshot as the final real-page desktop width. After the reference-size pass, prefer adapting the layout to a real desktop viewport around `1900px` wide, allowing roughly `1900px` rather than `1920px` to account for a scrollbar and normal browser chrome.
- Only after the reference-size version is visually close should you derive tablet/mobile behavior.
- When the user supplies a newer or revised screenshot, the latest screenshot becomes the source of truth.

## High-fidelity rules

- Match layout, spacing, typography, line height, letter spacing, colours, borders, border opacity, shadows, gradients, border radius, imagery crop/aspect ratio, and visual hierarchy as closely as possible.
- Use explicit values for widths, heights, max-widths, padding, margin, gap, border radius, font size, line height, tracking, and shadow when defaults are not close enough.
- Treat text fidelity as a layout problem as well as a content problem. If text is clipped, crowded, truncated, wrapped incorrectly, or pushes nearby controls out of alignment, the page is not done.
- Treat every visible detail as required, including micro-details:
  - small logos and button icons
  - search icons
  - dropdown carets
  - pagination chevrons
  - active nav underlines / glows
  - status dots
  - bullet colours
  - card icons
  - star/favorite icons
  - divider lines
  - subtle corner radii differences
  - text opacity changes
- Missing a small icon or logo inside a control is a fidelity failure, not a minor omission.
- Do not redesign, simplify, embellish, or "improve" the UI unless required for responsiveness or because the reference is genuinely ambiguous.
- Do not silently rely on DaisyUI typography, button styles, input styles, or spacing scale if they do not match the reference.

## Existing frontend adaptation mode

When working inside an existing frontend or design system:
- Inspect the current codebase before creating new structures.
- Reuse existing layout shells, shared components, utility patterns, typography tokens, spacing scales, breakpoints, icon conventions, and theme variables wherever they can faithfully express the reference.
- Prefer adapting a nearby existing page or section over creating a parallel implementation from scratch.
- Do not introduce duplicate components, conflicting design tokens, or a second styling system unless the user explicitly asks for it.
- If the screenshot conflicts with the established design system, preserve the screenshot's page-level composition while staying as consistent as possible with the current tokens/components, unless the user explicitly says the screenshot should override the current design language.

## Reference intake and breakpoint handling

- Record the exact dimensions of each reference image before coding.
- For the primary fidelity pass, render the page at the exact reference viewport size in CSS pixels whenever possible.
- If the reference desktop image is substantially narrower than a modern desktop viewport, treat that width as a composition/style reference rather than the final real-page desktop width. Preserve the screenshot's structure, hierarchy, spacing intent, and visual language, then expand and validate the actual desktop implementation at about `1900px` viewport width.
- If multiple reference images are provided for desktop/tablet/mobile, treat each as authoritative for its breakpoint.
- If only a desktop reference exists, infer tablet/mobile layouts by preserving hierarchy, ordering, and visual balance without inventing new sections or interactions.
- If text is legible, reproduce it exactly, including punctuation and small helper labels.
- If text is unclear, use the closest reasonable approximation and report the uncertainty.
- If the screenshot shows a cropped region of a page rather than a full page, match the visible region first.

## Viewport honesty and scaling safety

- Treat browser zoom, OS DPI scaling, and device pixel ratio as environmental factors that the implementation must tolerate, not as excuses to distort the layout.
- When Playwright or similar browser automation is available, treat automation-controlled screenshots captured at an explicit viewport size as the primary fidelity reference for comparison.
- Do not treat a headed browser window as the source of truth for pixel fidelity when OS DPI scaling, browser zoom, window chrome, or desktop compositor behavior may affect what the human sees on screen.
- On Windows in particular, assume non-default desktop scaling or browser zoom can make a headed browser visually misleading even when the underlying page layout is correct in CSS pixels.
- If Playwright reports that it opened a `chrome` or `msedge` browser/channel, that is still Playwright-driven verification. Do not describe this as "switching away from Playwright" unless browser automation was actually abandoned.
- Do not use CSS `zoom`, root-level `transform: scale(...)`, synthetic wrapper scaling, or similar viewport hacks to make the implementation screenshot look closer to the reference.
- Do not "fix" width, crowding, or fold-position mismatches by shrinking the entire page or inflating the canvas.
- Solve screenshot mismatches with real layout changes:
  - correct container widths
  - correct grid and flex sizing
  - correct gaps and paddings
  - correct font sizes and line heights
  - correct control heights and intrinsic widths
  - correct responsive breakpoints
- If a browser-specific mismatch appears, first suspect invalid layout assumptions, overflow, or scaling hacks in the implementation before blaming the user's environment.
- If there is a mismatch between a headed browser window and a Playwright screenshot taken at the calibrated viewport, trust the screenshot first for fidelity work and investigate the implementation with additional screenshot passes before attributing the difference to the user's machine.
- When reporting fidelity status, distinguish between:
  - expected reflow differences caused by user/browser zoom preferences, and
  - genuine layout bugs such as horizontal overflow, incorrect width calculations, broken wrapping, or fragile breakpoint behavior.

## Preflight checklist

Before implementing, explicitly inspect and inventory:

1. Page sections and their order
2. Grid / column structure and approximate width ratios
3. Major containers and card boundaries
4. All text blocks and labels
5. All visible controls and interactive states
6. All icons, logos, badges, chips, status dots, separators, and decorative marks
7. All image assets and background graphics
8. Typography groupings (hero title, body copy, pills, buttons, table headers, table rows, side cards, notices, etc.)
9. Primary, secondary, muted, success, warning, danger, and accent colours
10. Likely responsive intent
11. Any regions where copy length, chip count, or control density make crowding likely
12. Any rows or panels that must remain on one line at the reference breakpoint

Do not start coding until you have a working mental map of every visually meaningful element.

## Typography audit

Typography is a first-class fidelity target.

- Inspect the repo for existing font sources first:
  - global CSS
  - Tailwind config
  - DaisyUI theme config
  - design tokens
  - existing page components
  - local font files
- If an existing project font matches the reference, use it.
- If the reference appears to use a custom or non-default font and the exact font is unavailable, choose the closest available option and report that limitation explicitly.
- Do not default to generic DaisyUI/body typography without checking.
- Set typography explicitly for each visual group:
  - logo text
  - nav links
  - pills / badges
  - hero heading
  - lead paragraph
  - stat labels
  - stat values
  - helper text
  - filter chips
  - form labels
  - table headers
  - table rows
  - sidebar headings
  - notifications / timestamps
  - primary and secondary buttons
- Check not only font family, but also:
  - size
  - weight
  - line height
  - letter spacing
  - case
  - colour / opacity
- Validate text wrapping and line breaks at the reference width. If a heading or paragraph wraps differently from the screenshot, fix it.
- Validate text integrity for controls and dense UI:
  - no unintended truncation
  - no clipped ascenders/descenders
  - no vertical squashing from incorrect line height or control height
  - no label/helper text collisions
  - no placeholder text overflowing its field

## Iconography and completeness audit

Before declaring the page done, verify that every visually meaningful icon or mark from the reference is represented in the DOM.

This includes:
- logo marks
- brand icons inside buttons
- search icons
- dropdown carets
- stat-card icons
- status indicators
- map / notification bullets
- table favorite icons
- pagination arrows
- close / reset / filter icons
- any subtle inline symbols

Rules:
- Small UI icons count as assets and must not be omitted.
- Prefer existing repo icons or simple inline SVGs for small UI icons.
- Do not add a new icon library unless the repo already uses one or the user explicitly asks for it.
- For common brand marks used in UI controls (for example Discord), use a clean inline SVG or existing icon component unless the repo already has an appropriate asset.

## Layout fitting and crowding rules

For the reference breakpoint:
- Recreate the screenshot's composition before making responsive adaptations.
- Do not solve crowding by prematurely redesigning, deleting, shrinking, or reflowing major groups.
- Do not solve crowding by scaling the whole page with CSS or by relying on browser zoom assumptions.
- First exhaust fidelity-preserving options:
  - match the reference viewport size
  - correct container widths and side-column widths
  - tighten or loosen gaps to the measured values
  - use the correct font size and line height
  - use correct control widths and min-widths
  - use the correct track sizing for each grid column instead of evenly distributing everything
  - give dense controls the width they actually need before shrinking neighboring elements
  - use wrapping only where the screenshot already implies wrapping
  - inspect whether the reference actually uses multiple rows
- Only move controls to additional rows at the reference breakpoint if:
  - the screenshot explicitly shows multiple rows, or
  - the user provides a revised screenshot showing the updated structure.
- If controls still feel crowded after a pass, assume the proportions are still wrong and continue iterating. Do not normalize crowding as "good enough."
- For narrower breakpoints, reflow cleanly while preserving hierarchy and visual balance.

## Colour, surface, and effects audit

- Match primary surfaces, secondary surfaces, muted surfaces, borders, glows, shadows, gradients, and text opacities as closely as possible.
- When possible, sample or estimate colours from the reference instead of inventing new values.
- Pay attention to:
  - background gradients
  - subtle border alpha
  - panel transparency
  - hover/active emphasis that is visible in the reference
  - contrast differences between main content and sidebar cards
  - accent colour consistency across badges, live indicators, buttons, and highlights

## Asset handling workflow

First, inventory every visible asset required by the page:
- logos
- hero images
- thumbnails / cards
- maps
- avatars
- icons
- illustrations
- background graphics
- any other non-text visual elements

For each asset, choose exactly one path.

### 1) User supplied the asset

- Visually inspect it before use.
- Use it where appropriate.
- Crop, resize, pad, trim, or mask it as needed to match the reference composition.
- Preserve aspect ratio; never distort it.
- Use `object-fit: cover` or `contain` as appropriate.
- If the asset is low-resolution or otherwise imperfect, get as close as possible and note the limitation.

### 2) Asset is missing and the user did not ask to generate it

- Use a clearly labeled placeholder with the correct approximate dimensions, aspect ratio, border radius, placement, and visual weight.
- If you create or synthesize a temporary stand-in asset yourself instead of a generic placeholder, still treat that asset as missing for reporting purposes unless the user explicitly asked you to generate it.
- Never silently substitute a stand-in, proxy illustration, or synthetic replacement and then omit it from the final missing-assets report.
- Also prepare one separate, ready-to-use generation prompt for each missing asset.
- Do not collapse multiple assets into one combined prompt.
- Each prompt must remain standalone, but in the final response all still-missing asset prompts must be grouped together inside one single fenced `text` code block for easy copy/paste into another AI/LLM.
- Separate asset prompts inside that block with a clear divider such as `---`.
- Each prompt must include:
  - asset name / suggested filename
  - purpose in the UI
  - desired subject/content
  - composition / framing
  - style / mood
  - colours / lighting
  - target aspect ratio or dimensions
  - transparency/background requirements if relevant
  - key "avoid" notes

### 3) Asset is missing and the user explicitly asked to generate or edit it

- If image generation/editing is available in the active environment, generate or edit the asset and integrate it into the page.
- Save generated assets in the repo's existing asset location, or a sensible folder such as `assets/generated/` if no convention exists.
- Validate that the asset fits the layout visually and dimensionally.
- Re-crop, regenerate, or iterate if needed until the asset works in context.
- If image generation/editing is not available, fall back to placeholders plus one standalone generation prompt per missing asset, and output all such prompts together inside one single fenced `text` code block.

## Asset-specific guidance

- Simple UI icons are not a reason to leave a blank area. Implement them with inline SVG or existing repo icons when possible.
- For brand logos or proprietary-looking marks that are not provided, use placeholders unless the user explicitly wants a temporary generated stand-in.
- For hero images, thumbnail images, maps, and other prominent visuals, match crop, focal point, aspect ratio, and visual weight as closely as possible.
- If the reference includes repeated thumbnail cards, pay attention to consistent crop and corner radius across all items.

## Implementation workflow

1. Inspect the reference image(s) and build the preflight inventory.
2. If an existing codebase is present, inspect the most relevant pages/components/tokens/icons first and decide what to reuse.
3. Build a first pass that is already visually close.
4. Run or preview the page.
5. Capture an implementation screenshot at the exact reference viewport size.
6. Compare the implementation screenshot against the reference.
7. Make a written mismatch list before editing. Focus on the largest visual errors first, then the micro-details.
8. Repeat screenshot, mismatch list, and fixes until there are no obvious mismatches left.
9. Before finishing, do at least one explicit "fragility pass" focused only on:
   - crowded rows
   - clipped or squashed text
   - overlapping elements
   - controls that look too narrow for their content
   - suspiciously tight spacing that may break at slightly different widths
10. For repeated UI structures such as card grids, table rows, stat tiles, nav items, or repeated buttons, do one explicit alignment pass and verify that shared baselines, footer rows, button positions, chip rows, and media crops are consistent across siblings.

## Mandatory visual verification workflow

When browser and screenshot tools are available, the following passes are mandatory.

If the page is too tall to inspect reliably in a single screenshot, capture segmented screenshots that collectively cover the whole page. Prefer top / middle / bottom coverage or more segments as needed. Do not assume unseen lower sections are correct.

For tall pages, the preferred verification pattern is:
- capture one full-page or tallest-practical screenshot artifact when tooling supports it, to understand overall vertical rhythm, section spacing, and macro composition across the whole document
- also capture segmented viewport screenshots that cover the page from top to bottom with intentional scroll positions
- visually inspect the segmented screenshots yourself; do not rely on the full-page artifact alone for lower sections, because tall captures can hide crowding, clipped text, sticky overlaps, or small alignment errors
- make sure the segmented set covers the entire page without leaving unverified gaps between scroll positions
- when a section is especially dense or fragile, add extra local screenshots for that region rather than assuming the nearest segment is sufficient

Treat the full-page screenshot as a macro-composition aid and the segmented screenshots as the authoritative visual inspection set for tall-page fidelity.

### Pass 0 - viewport calibration
- Use the exact primary reference dimensions for the first comparison pass.
- Make sure the page is captured at the correct route/state and comparable scroll position.
- Do not judge fidelity from a different width and then claim a match.
- Keep viewport calibration honest: do not use CSS `zoom`, wrapper scaling, or screenshot-only transforms to force the composition into place.
- Prefer automation screenshots captured at explicit CSS viewport dimensions over visual judgment from a headed browser window.
- If headed mode is used for convenience, use it for interaction/debugging only; do not treat the live window as the authoritative fidelity check when a direct Playwright screenshot is available.

### Pass 1 - macro composition
Check:
- overall page width and margins
- main vs sidebar width ratio
- hero split ratios
- card widths and heights
- section spacing
- alignment of top nav, hero, filter area, table, and sidebar
- absence of horizontal overflow or suspicious whole-page shrink/stretch behavior
- no rows that appear denser, tighter, or more compressed than the reference

### Pass 2 - typography and copy
Check:
- font family choice
- font size
- weight
- line height
- tracking
- text colour / opacity
- exact copy
- exact line breaks / wrapping
- no truncated, clipped, or visibly squashed text
- no copy mismatches in small labels, helper text, timestamps, badge text, placeholders, or table metadata

### Pass 3 - iconography and control completeness
Check:
- every icon, logo, caret, bullet, dot, and star
- button leading/trailing icons
- search icon presence and placement
- inline helper icons
- stat-card icons
- missing micro-details

### Pass 4 - colour and surface treatment
Check:
- gradients
- surface tints
- borders
- border opacity
- shadows
- glows
- pill fills
- badge colours
- table row separators
- muted text tones

### Pass 5 - spacing and fine geometry
Check:
- paddings
- margins
- gaps
- border radii
- chip sizes
- input heights
- button heights
- row heights
- image crop framing
- icon size inside controls
- no overlapping layers, clipped corners, or compressed control interiors
- no fields/buttons/selects that are narrower than the reference unless the screenshot clearly shows it
- alignment consistency across repeated components
- matched footer/button baselines across peer cards where the reference implies alignment
- no sibling card or tile whose CTA, stat row, badge row, or title block sits visibly higher or lower than its peers without an explicit reason in the reference

### Pass 6 - responsive behavior
After the reference-size version is close:
- for desktop webpages, include a preferred wide-desktop validation pass at about `1900px` viewport width unless the user explicitly asks for a different desktop target
- do not assume the reference screenshot's narrower width is the correct production desktop width; if the screenshot is a POC, translate it into a stable real-page layout at the preferred wide-desktop viewport while keeping its composition and design language
- test tablet and mobile widths
- if feasible, sanity-check at one alternate desktop condition as well, such as a slightly narrower desktop width or a browser zoomed-out view, to catch fragile layout assumptions
- if a user’s environment is known to use non-default zoom or DPI scaling, include one sanity check that approximates that condition when practical
- preserve hierarchy and balance
- avoid overflow, clipped controls, awkward wrapping, and distorted media
- do not let the responsive version drift so far that it no longer resembles the same design language
- when reporting results, distinguish environment-related rendering differences from genuine layout bugs; do not use DPI scaling or browser zoom as a blanket excuse for visible geometry mistakes

### Pass 7 - final completeness review
Before finishing, verify:
- every visible section exists
- every visible icon exists
- every visible text label exists
- every supplied asset is used correctly
- every remaining missing asset has a placeholder and, if needed, an entry in the single asset-prompt code block
- no obvious crowding, clipping, overlap, or layout fragility remains in the verified views

Continue iterating beyond these passes if needed. Do not stop at the first working draft.

## Optional helper script

If this skill includes `scripts/compare_screenshots.py` and Python is available, use it after capturing the implementation screenshot at the reference size.

Preferred usage:
`python <path-to-codex-home>/skills/ui-from-image/scripts/compare_screenshots.py path/to/reference.png path/to/implementation.png --out-dir .codex-artifacts/ui-diff`

Notes:
- The helper script lives in the installed skill directory, not the target repo, unless you copied it into the repo yourself.
- Best practice is to compare screenshots at the same dimensions without resizing.
- Use `--fit` only as a fallback when your candidate screenshot size is slightly off and you need a quick diagnostic.
- Use the generated diff images and metrics to locate hot spots, but do not optimize only to the number; visual judgment still matters.

## Responsive requirements

- The result must work cleanly on desktop, tablet, and mobile.
- Avoid overflow, broken wrapping, clipped content, distorted media, and awkward spacing jumps.
- Preserve the desktop composition where possible, then reflow/stack cleanly on smaller screens.
- Keep interactive elements touch-friendly.
- Do not hide important content unless the reference clearly implies it.

## Behaviour

- Add JS only for visible behaviour implied by the reference.
- If no JS is needed, still create `script.js` with a short comment.
- Do not add unrelated features, animations, or libraries.

## Final report

At the end, briefly report:
1. what was implemented
2. what was reused/adapted vs newly created
3. which supplied assets were used
4. which assets were generated and integrated
5. which placeholders remain
6. if any assets are still missing, include exactly one fenced `text` code block containing all remaining asset-generation prompts
7. which visual comparison passes were completed
8. any remaining uncertainties or tiny mismatches
9. if any temporary stand-ins or synthetic replacements were used for missing assets, state that explicitly and list them alongside the missing-assets reporting

### Single asset-prompt block rules

- Use exactly one fenced `text` code block for all still-missing asset prompts.
- Omit the block entirely if no asset-generation prompts are needed.
- Do not spread asset prompts across multiple code blocks or normal prose.
- Inside the block, keep each asset prompt standalone and clearly separated with `---`.
- Start the block with:

Generate each asset below as a separate image file. Do not combine multiple assets into one image.

- Then use this structure for each asset:

---
asset_name: ...
suggested_filename: ...
purpose_in_ui: ...
target_dimensions_or_aspect_ratio: ...
background_requirements: ...
prompt: ...
avoid: ...
---

## Definition of done

The task is done only when all of the following are true:

- The rendered page is a close visual match to the reference image(s).
- The primary reference-size screenshot has been matched first before responsive adaptation.
- Desktop/tablet/mobile layouts are coherent and stable.
- At least one additional sanity-check view beyond the primary desktop screenshot has been checked when tooling makes that practical.
- Existing project patterns are reused where appropriate.
- Typography has been explicitly audited and does not merely rely on framework defaults.
- Text is correct and does not appear clipped, truncated, squashed, or incorrectly wrapped in the verified views.
- Iconography and micro-details have been explicitly audited and no obvious small UI elements are missing.
- Supplied assets are used appropriately.
- Explicitly requested generated assets are integrated when possible.
- Remaining missing assets are represented by accurate placeholders plus standalone generation prompts grouped into one single fenced `text` code block.
- No obvious horizontal overflow, overlapping elements, or crowding-related regressions remain in the verified views.
- Separate HTML/CSS/JS files are used for standalone work, or the implementation is cleanly integrated into the repo's existing structure for framework-based projects.

