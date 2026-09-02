# DESIGN.md — SWĪKRIT
### A Unique Visual Language: "Blueprint Cartography"
For use with Google Stitch (AI UI generation)

---

## 0. Read This First — The Core Design Idea

Do not design this as a generic SaaS dashboard (navy sidebar, white cards, blue buttons — every hackathon team builds this). SWĪKRIT's entire pitch is "a GPS for compliance" — so the UI should feel like **a cartographer's technical blueprint crossed with a wayfinding map**, not a corporate admin panel.

Think: the aesthetic of an architect's blueprint table, an old survey map of Maharashtra, and a modern flight-tracking radar screen — merged into one coherent system. Judges have seen a hundred blue-and-white dashboards this season. They have not seen a compliance tool that looks like a navigation instrument.

---

## 1. Design Concept Name: "The Draftsman's Table"

Every screen should feel like it's laid out on a technical drafting surface — fine grid lines faintly visible in the background, precise measurement-style annotations, and a restrained ink-on-paper color story instead of flat corporate gradients.

---

## 2. Color Palette — "Ink & Amber Survey"

Move away from generic navy/blue entirely. Use this palette instead:

| Role | Color | Hex | Notes |
|---|---|---|---|
| Base / Canvas | Warm paper white | `#F7F4EC` | Not pure white — a warm, slightly aged paper tone. This is the single biggest thing that makes it feel unique instead of "another SaaS app." |
| Primary ink | Deep charcoal-indigo | `#1C2333` | Used for all primary text, node borders, and line work — like fountain pen ink, not flat black |
| Structural lines | Faded blueprint blue | `#3A5A78` at 15–25% opacity | Used ONLY for the background grid and connecting paths — never for text |
| Critical / Action | Burnt amber | `#C6742B` | Reserved exclusively for critical-path indicators, primary CTA buttons, and "attention" states. Because it's used sparingly, it carries real visual weight when it appears. |
| Success / Compliant | Muted sage green | `#5C7A5E` | Never bright green — keep it desaturated to match the paper aesthetic |
| Alert / Gap detected | Muted brick red | `#A8462F` | Never a bright alarm red — stays within the "ink" family |
| Department tags (4 needed) | Terracotta `#B85C3C`, Slate `#5A6B7A`, Ochre `#B8923C`, Moss `#6B7A5A` | Each government department gets one desaturated, earthy tone — never neon or saturated |

**Why this works:** every hackathon default is bright blue-and-white "tech" colors. An aged-paper, ink-and-amber palette immediately signals "this was designed with intention," which is exactly the kind of thing a judge notices in the first three seconds without being able to articulate why.

---

## 3. Typography

- **Headings**: A serif with technical/architectural character — something like *Fraunces*, *Source Serif 4*, or *Lora* at semi-bold weight. Serif headings are the single fastest way to separate this from every other team's sans-serif SaaS look.
- **Body & UI text**: A clean geometric sans — *Inter* or *IBM Plex Sans* — for readability in forms and data.
- **Numeric/data labels** (fees, days, counts): A monospace font — *IBM Plex Mono* or *JetBrains Mono* — styled like measurements on a technical drawing (e.g. "45 DAYS", "₹1,80,000"). This monospace-for-numbers detail is a small touch that reads as highly deliberate.

---

## 4. The Signature Visual Motif: Compass & Survey Lines

This is the one motif that should appear consistently across every screen so the product has a recognizable visual signature:

- A **thin rotating compass rose icon** (minimal line art, not skeuomorphic) appears in a fixed corner of every screen — subtly animated to rotate a few degrees on load, then settle. This reinforces the "wayfinding/GPS" metaphor without saying it in words.
- **Dotted survey-line paths** connect roadmap nodes instead of plain solid arrows — like a route traced on an old survey map, with small tick marks along the path indicating distance/time.
- **Corner registration marks** (small crosshair/plus symbols, like on architectural blueprints or printer's marks) appear in the corners of major cards and panels — a subtle detail that most students would never think to add, and it reads as "professionally designed" instantly.

---

## 5. Background Treatment

Every screen sits on a **faint isometric or orthogonal grid** (the blueprint graph paper look) at very low opacity (3–5%) in the blueprint blue tone. Not a busy pattern — barely perceptible, but present enough that the "drafting table" feeling registers subconsciously.

---

## 6. Component Styling

### Buttons
- Primary CTA: solid burnt amber fill, sharp-ish corners (4px radius, NOT the generic 8–12px rounded-pill everyone uses), small monospace label in uppercase with letter-spacing (e.g. "GENERATE ROADMAP")
- Secondary: outline only, charcoal-indigo border, transparent fill

### Cards / Panels
- Warm paper white background, thin 1px charcoal-indigo border (not a drop shadow — shadows feel generic; a crisp border feels drafted)
- Corner registration marks (see Section 4) on major panels only, not every small card

### Roadmap Nodes (React Flow)
- Shape: rounded rectangle, but with a small triangular "flag" notch on the left edge — like a marker pin merged with a document icon
- Border color = department color (Section 2)
- Critical-path nodes get a double-border treatment in amber, not just a color fill
- Connecting edges: dotted/dashed lines with small perpendicular tick marks at intervals (survey-line style, see Section 4), animated with a subtle "drawing itself in" effect on load rather than snapping in instantly

### Timeline / Gantt View
- Styled like a horizontal ruler — actual tick marks and day-number labels along the top, like a measuring tape, rather than a plain flat bar chart

### Loading / Processing State
- Instead of a generic spinner, animate the compass rose motif slowly rotating, with a monospace status line beneath it that updates through real processing steps (e.g. "SCANNING MPCB REGULATIONS" → "MAPPING MIDC REQUIREMENTS" → "CALCULATING CRITICAL PATH") — this alone creates more "aha" than any spinner ever will, because it shows the system visibly reasoning rather than just waiting.

---

## 7. Iconography

- Line-art only, 1.5px stroke weight, no filled/glyph icons
- Department icons should feel hand-drafted: a factory outline for Factories Act, a leaf/droplet for MPCB (Pollution), a compass/land-plot symbol for MIDC, a flame outline for Fire NOC
- Avoid generic icon packs (no Font Awesome default look) — Stitch should generate custom-feeling line icons consistent with the blueprint aesthetic

---

## 8. Motion & Interaction Principles

- Nothing should "pop" or bounce — all motion should feel measured and precise, like a drafting instrument moving, not a bubbly consumer app
- Roadmap nodes and edges draw themselves in sequence (150–200ms stagger per node) rather than all appearing at once — reinforces the "system is thinking and building your path" feeling
- Hover states reveal a subtle crosshair/measurement tooltip rather than a flat generic tooltip box

---

## 9. What To Explicitly Avoid

- No generic blue-to-purple gradients
- No rounded-pill buttons or bubbly card shadows
- No stock "AI sparkle" icons (✨) — overused in every AI hackathon project this cycle
- No bright saturated colors anywhere — every color in this system is intentionally desaturated/earthy
- No sans-serif-only type system — the serif heading is non-negotiable for the "unique" mandate

---

## 10. One-Line Brief for Stitch (paste this at the top of your prompt)

```
Design SWĪKRIT in a "Blueprint Cartography" style: a warm-paper, ink-and-amber
technical drafting aesthetic — think architect's blueprint table meets an old
survey map meets a modern navigation instrument. Serif headings, monospace
data labels, a faint background grid, dotted survey-line connectors between
nodes, and a rotating compass motif as the recurring signature element.
Explicitly avoid generic blue/white SaaS dashboard styling, rounded-pill
buttons, drop shadows, and gradient buttons — use the exact palette and
component rules in the attached DESIGN.md.
```
