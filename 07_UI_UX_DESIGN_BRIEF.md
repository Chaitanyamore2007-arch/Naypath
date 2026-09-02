# UI/UX Design Brief — SWĪKRIT
### For use with Google Stitch (AI UI generation)

## Brand Direction
- **Tone**: Serious, institutional-grade, trustworthy — this is a government-facing compliance tool, not a consumer app. Avoid playful colors or rounded cartoonish elements.
- **Color palette**: Deep navy/indigo primary (#1E3A5F or similar), warm amber/gold accent (#D4A017) for highlights and critical-path indicators, white/off-white background, muted gray for secondary text.
- **Typography**: Clean sans-serif (Inter or similar). Avoid decorative fonts.
- **Reference feel**: Think government digital services (like India's own DigiLocker or UMANG) crossed with a modern SaaS analytics dashboard (like Linear or Notion).

## Screens Required

### 1. Landing / Input Screen
- Hero headline: "Your complete compliance roadmap. Before you file anything."
- Form fields: Industry type (dropdown/searchable), District (dropdown — Maharashtra districts), Investment scale (slider or input, in ₹ crores), Unit size (radio: small/medium/large)
- Primary CTA button: "Generate Roadmap"
- Subtle animated loading state after submission (12-second processing feel — use a progress indicator, not a spinner, to convey "real work happening")

### 2. Roadmap Visualization Screen (Core Screen)
- Full-width interactive node graph (this will be built with React Flow in code — Stitch should mock the visual style: rounded rectangle nodes, connecting lines showing dependencies, color-coded by department)
- Legend showing department color coding
- Critical path highlighted (thicker border or amber color)
- Sidebar or top bar showing: Total estimated days, Total estimated fees, Number of clearances
- Each node shows: Clearance name, Department icon, Estimated days badge

### 3. Clearance Detail Panel (Modal or Slide-in Drawer)
- Triggered by clicking a roadmap node
- Shows: Full clearance name, Department, Required documents (checklist style), Fee structure, Estimated timeline, Common rejection reasons, Contact office

### 4. Document Upload & Audit Screen
- Drag-and-drop upload zone (PDF only badge visible)
- List of uploaded files with status indicators
- "Run Compliance Audit" CTA
- Results view: Gap report as a card list — each gap shows severity (color-coded: red=high, amber=medium, green=compliant), issue description, recommendation

### 5. Gantt Timeline View
- Horizontal timeline bars for each clearance, positioned by sequence and duration
- Critical path bars highlighted in amber
- Department color coding consistent with roadmap screen

## Interaction Notes
- All transitions should feel fast and confident — no more than 300ms for UI animations, longer only for the intentional "processing" state
- Mobile responsiveness is secondary priority (see PRD scope) — design desktop-first at 1440px width, but ensure the layout doesn't visually break at 768px

## Accessibility
- Sufficient color contrast for text on colored backgrounds (WCAG AA minimum)
- Color should never be the only indicator of severity/status — pair with icons or text labels
