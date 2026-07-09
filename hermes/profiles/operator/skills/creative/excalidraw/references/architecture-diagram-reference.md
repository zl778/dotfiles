1|---
2|name: architecture-diagram
3|description: "Dark-themed SVG architecture/cloud/infra diagrams as HTML."
4|version: 1.0.0
5|author: Cocoon AI (hello@cocoon-ai.com), ported by Hermes Agent
6|license: MIT
7|dependencies: []
8|platforms: [linux, macos, windows]
9|metadata:
10|  hermes:
11|    tags: [architecture, diagrams, SVG, HTML, visualization, infrastructure, cloud]
12|    related_skills: [concept-diagrams, excalidraw]
13|---
14|
15|# Architecture Diagram Skill
16|
17|Generate professional, dark-themed technical architecture diagrams as standalone HTML files with inline SVG graphics. No external tools, no API keys, no rendering libraries — just write the HTML file and open it in a browser.
18|
19|## Scope
20|
21|**Best suited for:**
22|- Software system architecture (frontend / backend / database layers)
23|- Cloud infrastructure (VPC, regions, subnets, managed services)
24|- Microservice / service-mesh topology
25|- Database + API map, deployment diagrams
26|- Anything with a tech-infra subject that fits a dark, grid-backed aesthetic
27|
28|**Look elsewhere first for:**
29|- Physics, chemistry, math, biology, or other scientific subjects
30|- Physical objects (vehicles, hardware, anatomy, cross-sections)
31|- Floor plans, narrative journeys, educational / textbook-style visuals
32|- Hand-drawn whiteboard sketches (consider `excalidraw`)
33|- Animated explainers (consider an animation skill)
34|
35|If a more specialized skill is available for the subject, prefer that. If none fits, this skill can also serve as a general SVG diagram fallback — the output will just carry the dark tech aesthetic described below.
36|
37|Based on [Cocoon AI's architecture-diagram-generator](https://github.com/Cocoon-AI/architecture-diagram-generator) (MIT).
38|
39|## Workflow
40|
41|1. User describes their system architecture (components, connections, technologies)
42|2. Generate the HTML file following the design system below
43|3. Save with `write_file` to a `.html` file (e.g. `~/architecture-diagram.html`)
44|4. User opens in any browser — works offline, no dependencies
45|
46|### Output Location
47|
48|Save diagrams to a user-specified path, or default to the current working directory:
49|```
50|./[project-name]-architecture.html
51|```
52|
53|### Preview
54|
55|After saving, suggest the user open it:
56|```bash
57|# macOS
58|open ./my-architecture.html
59|# Linux
60|xdg-open ./my-architecture.html
61|```
62|
63|## Design System & Visual Language
64|
65|### Color Palette (Semantic Mapping)
66|
67|Use specific `rgba` fills and hex strokes to categorize components:
68|
69|| Component Type | Fill (rgba) | Stroke (Hex) |
70|| :--- | :--- | :--- |
71|| **Frontend** | `rgba(8, 51, 68, 0.4)` | `#22d3ee` (cyan-400) |
72|| **Backend** | `rgba(6, 78, 59, 0.4)` | `#34d399` (emerald-400) |
73|| **Database** | `rgba(76, 29, 149, 0.4)` | `#a78bfa` (violet-400) |
74|| **AWS/Cloud** | `rgba(120, 53, 15, 0.3)` | `#fbbf24` (amber-400) |
75|| **Security** | `rgba(136, 19, 55, 0.4)` | `#fb7185` (rose-400) |
76|| **Message Bus** | `rgba(251, 146, 60, 0.3)` | `#fb923c` (orange-400) |
77|| **External** | `rgba(30, 41, 59, 0.5)` | `#94a3b8` (slate-400) |
78|
79|### Typography & Background
80|- **Font:** JetBrains Mono (Monospace), loaded from Google Fonts
81|- **Sizes:** 12px (Names), 9px (Sublabels), 8px (Annotations), 7px (Tiny labels)
82|- **Background:** Slate-950 (`#020617`) with a subtle 40px grid pattern
83|
84|```svg
85|<!-- Background Grid Pattern -->
86|<pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">
87|  <path d="M 40 0 L 0 0 0 40" fill="none" stroke="#1e293b" stroke-width="0.5"/>
88|</pattern>
89|```
90|
91|## Technical Implementation Details
92|
93|### Component Rendering
94|Components are rounded rectangles (`rx="6"`) with 1.5px strokes. To prevent arrows from showing through semi-transparent fills, use a **double-rect masking technique**:
95|1. Draw an opaque background rect (`#0f172a`)
96|2. Draw the semi-transparent styled rect on top
97|
98|### Connection Rules
99|- **Z-Order:** Draw arrows *early* in the SVG (after the grid) so they render behind component boxes
100|- **Arrowheads:** Defined via SVG markers
101|- **Security Flows:** Use dashed lines in rose color (`#fb7185`)
102|- **Boundaries:**
103|  - *Security Groups:* Dashed (`4,4`), rose color
104|  - *Regions:* Large dashed (`8,4`), amber color, `rx="12"`
105|
106|### Spacing & Layout Logic
107|- **Standard Height:** 60px (Services); 80-120px (Large components)
108|- **Vertical Gap:** Minimum 40px between components
109|- **Message Buses:** Must be placed *in the gap* between services, not overlapping them
110|- **Legend Placement:** **CRITICAL.** Must be placed outside all boundary boxes. Calculate the lowest Y-coordinate of all boundaries and place the legend at least 20px below it.
111|
112|## Document Structure
113|
114|The generated HTML file follows a four-part layout:
115|1. **Header:** Title with a pulsing dot indicator and subtitle
116|2. **Main SVG:** The diagram contained within a rounded border card
117|3. **Summary Cards:** A grid of three cards below the diagram for high-level details
118|4. **Footer:** Minimal metadata
119|
120|### Info Card Pattern
121|```html
122|<div class="card">
123|  <div class="card-header">
124|    <div class="card-dot cyan"></div>
125|    <h3>Title</h3>
126|  </div>
127|  <ul>
128|    <li>• Item one</li>
129|    <li>• Item two</li>
130|  </ul>
131|</div>
132|```
133|
134|## Output Requirements
135|- **Single File:** One self-contained `.html` file
136|- **No External Dependencies:** All CSS and SVG must be inline (except Google Fonts)
137|- **No JavaScript:** Use pure CSS for any animations (like pulsing dots)
138|- **Compatibility:** Must render correctly in any modern web browser
139|
140|## Template Reference
141|
142|Load the full HTML template for the exact structure, CSS, and SVG component examples:
143|
144|```
145|skill_view(name="architecture-diagram", file_path="templates/template.html")
146|```
147|
148|The template contains working examples of every component type (frontend, backend, database, cloud, security), arrow styles (standard, dashed, curved), security groups, region boundaries, and the legend — use it as your structural reference when generating diagrams.
149|