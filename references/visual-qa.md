# Visual QA Checklist

Use this file when browser preview or screenshot comparison is available.

## Required comparison passes

Complete at least these three passes:

### Pass 1: Structure and composition

Check:

- section order and boundaries
- content widths and container alignment
- grid structure and column balance
- proportions of major blocks
- spacing between large regions
- image crop and focal point

Adjust the implementation until the composition is recognizably close before polishing details.

### Pass 2: Fine visual fidelity

Check:

- typography size, weight, line height, and tracking
- colours and contrast
- borders, shadows, and radii
- card padding and intra-component spacing
- button and input sizing
- icon sizing and placement
- imagery weight relative to text

Use arbitrary values or small custom CSS when the built-in scale is not close enough.

### Pass 3: Responsive behaviour

Check desktop, tablet, and mobile layouts for:

- overflow or clipped content
- awkward wrapping
- broken hierarchy after stacking
- distorted media
- oversized or undersized touch targets
- sudden spacing jumps

If only a desktop reference exists, keep the same hierarchy and emphasis while reflowing cleanly for smaller screens.

## Completion rule

Do not stop at the first working draft. Keep iterating until remaining differences are minor enough that they can be explained briefly in the final report.

If screenshot-based comparison is unavailable, say that verification was based on static inspection only.
