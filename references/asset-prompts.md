# Asset Prompt Checklist

Use this file only when one or more visual assets are missing.

## Placeholder rule

If the asset is missing and the user did not explicitly ask to generate or edit it:

- insert a clearly labeled placeholder
- match the approximate dimensions, aspect ratio, border radius, placement, and visual weight from the screenshot
- keep the placeholder honest; it should signal that the real asset is still missing

## Standalone prompt rule

Write exactly one standalone generation prompt per missing asset.

Never:

- combine multiple missing assets into one prompt
- assume a brand logo or proprietary mark can be invented unless the user explicitly asked for a temporary stand-in
- leave out composition or aspect ratio guidance

Every prompt must include:

- asset name or suggested filename
- purpose in the UI
- desired subject or content
- composition or framing
- style or mood
- colours or lighting
- target aspect ratio or dimensions
- transparency or background requirements when relevant
- key avoid notes

## Prompt template

Use this structure:

`Asset name / filename:` `example-name.png`

`Purpose in UI:` Short sentence describing where it appears and why it matters.

`Prompt:` Create `example-name.png` for [purpose]. Show [subject/content]. Frame it as [composition/framing]. Match a [style/mood] look with [colour/lighting notes]. Output at [aspect ratio or dimensions]. Use [transparent/background requirement]. Avoid [specific things to avoid].

## Quality bar

The prompt should be usable on its own without any extra project context. Someone reading only the prompt should understand what to generate and how the result should fit the UI.
