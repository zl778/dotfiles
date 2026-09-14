1|# Pretext Patterns
2|
3|Copy-pasteable snippets for the most common pretext demo shapes. Each pattern is self-contained — drop into an HTML `<script type="module">` after importing from `https://esm.sh/@chenglou/pretext@0.0.6`.
4|
5|## 1. Flow around an obstacle (variable-width column)
6|
7|The signature pretext move. Row-by-row ask "how wide is the corridor here?" and let pretext break lines accordingly.
8|
9|```js
10|const prepared = prepareWithSegments(TEXT, FONT);
11|const LINE_H = 24;
12|
13|function drawFlow(ctx, obstacle /* {x,y,r} */, COL_X, COL_W, H) {
14|  let cursor = { segmentIndex: 0, graphemeIndex: 0 };
15|  let y = 72;
16|  while (y < H - 40) {
17|    const dy = y - obstacle.y;
18|    const inBand = Math.abs(dy) < obstacle.r;
19|    let x = COL_X, w = COL_W;
20|    if (inBand) {
21|      const half = Math.sqrt(obstacle.r ** 2 - dy ** 2);
22|      const leftW  = Math.max(0, (obstacle.x - half) - COL_X);
23|      const rightW = Math.max(0, (COL_X + COL_W) - (obstacle.x + half));
24|      if (leftW >= rightW) { x = COL_X;                 w = leftW  - 12; }
25|      else                 { x = obstacle.x + half + 12; w = rightW - 12; }
26|      if (w < 40) { y += LINE_H; continue; } // skip rather than squeeze
27|    }
28|    const range = layoutNextLineRange(prepared, cursor, w);
29|    if (!range) break;
30|    const line = materializeLineRange(prepared, range);
31|    ctx.fillText(line.text, x, y);
32|    cursor = range.end;
33|    y += LINE_H;
34|  }
35|}
36|```
37|
38|**Obstacle variants:** circles (above), rectangles (use `Math.max(0, …)` on the row-segment), multiple obstacles (sort segments and emit the wider remaining lane), animated obstacles (recompute every frame — pretext is fast enough).
39|
40|## 2. Text-as-geometry game (word-bricks with collision)
41|
42|Use `layoutWithLines` to get stable line rects, then treat each word as an axis-aligned box for physics.
43|
44|```js
45|const prepared = prepareWithSegments(WORDS.join(" "), FONT);
46|const { lines } = layoutWithLines(prepared, FIELD_W, 28);
47|
48|// Build brick rects: split each line on spaces and measure word-by-word.
49|const bricks = [];
50|let y = 50;
51|for (const line of lines) {
52|  let x = 10;
53|  for (const word of line.text.split(" ")) {
54|    const wPx = ctx.measureText(word).width; // or use walkLineRanges per word
55|    bricks.push({ x, y, w: wPx, h: 24, text: word, hp: 1 });
56|    x += wPx + ctx.measureText(" ").width;
57|  }
58|  y += 28;
59|}
60|```
61|
62|Collision: standard AABB vs the ball. When `hp` drops to 0, the brick is "eaten." For the aesthetic: fade brick opacity with hp, trail particles from the letters on impact.
63|
64|## 3. Shatter / explode typography
65|
66|Use `walkLineRanges` + a manual grapheme walk to get `(x, y)` for every glyph, then spawn particles.
67|
68|```js
69|const prepared = prepareWithSegments(TEXT, FONT);
70|const particles = [];
71|let y = 100;
72|walkLineRanges(prepared, COL_W, (line) => {
73|  // materialize so we get per-grapheme positions
74|  const range = materializeLineRange(prepared, line);
75|  const seg = new Intl.Segmenter(undefined, { granularity: "grapheme" });
76|  let x = COL_X;
77|  for (const { segment } of seg.segment(range.text)) {
78|    const w = ctx.measureText(segment).width;
79|    particles.push({ ch: segment, x, y, vx: 0, vy: 0, homeX: x, homeY: y });
80|    x += w;
81|  }
82|  y += LINE_H;
83|});
84|
85|// On click, kick particles outward from click point; ease them back to (homeX, homeY).
86|canvas.addEventListener("click", (e) => {
87|  for (const p of particles) {
88|    const dx = p.x - e.clientX, dy = p.y - e.clientY;
89|    const d = Math.hypot(dx, dy) || 1;
90|    const force = 400 / (d * 0.2 + 1);
91|    p.vx += (dx / d) * force;
92|    p.vy += (dy / d) * force;
93|  }
94|});
95|
96|function tick(dt) {
97|  for (const p of particles) {
98|    p.vx *= 0.92; p.vy *= 0.92;
99|    p.vx += (p.homeX - p.x) * 0.06;
100|    p.vy += (p.homeY - p.y) * 0.06;
101|    p.x += p.vx * dt; p.y += p.vy * dt;
102|  }
103|}
104|```
105|
106|## 4. ASCII mask as moving obstacle
107|
108|The "cool demos" money pattern: rasterize an ASCII logo, sprite, or bitmap into a cell buffer, then convert the occupied cells into per-row obstacle spans. Pretext lays the paragraphs around those spans, so the text actually opens around the moving ASCII object instead of being visually overpainted.
109|
110|See `templates/donut-orbit.html` in this skill for a full implementation. Treat it as an example, not the canonical scene: it shows how to derive spans from an ASCII logo, project a wire shape into obstacle rows, keep text selectable in a DOM layer, and hide tuning controls behind `?dev`. Key structure:
111|
112|```js
113|const CELL_W = 12, CELL_H = 15;
114|const cols = Math.ceil(W / CELL_W), rows = Math.ceil(H / CELL_H);
115|const asciiMask = new Uint8Array(cols * rows);
116|const obstacleRows = Array.from({ length: rows }, () => []);
117|
118|function rasterizeLogo(time) {
119|  asciiMask.fill(0);
120|  for (const r of obstacleRows) r.length = 0;
121|
122|  for (const block of logoBlocks(time)) {
123|    const r0 = Math.floor(block.y0 / CELL_H);
124|    const r1 = Math.ceil(block.y1 / CELL_H);
125|    for (let r = r0; r <= r1; r++) {
126|      obstacleRows[r]?.push([block.x0 - 18, block.x1 + 22]);
127|      // Fill asciiMask cells here for drawing.
128|    }
129|  }
130|
131|  mergeRowSpans(obstacleRows);
132|}
133|
134|function drawParagraphs(prepared) {
135|  let cursor = { segmentIndex: 0, graphemeIndex: 0 };
136|  for (let y = yStart; y < yEnd; y += LINE_H) {
137|    const spans = obstacleRows[Math.floor(y / CELL_H)];
138|    for (const [x0, x1] of freeIntervalsAround(spans)) {
139|      const range = layoutNextLineRange(prepared, cursor, x1 - x0);
140|      if (!range) return;
141|      ctx.fillText(materializeLineRange(prepared, range).text, x0, y);
142|      cursor = range.end;
143|    }
144|  }
145|}
146|```
147|
148|The important bit is that the ASCII geometry is not decorative only. The same moving spans that draw the logo or draggable object also carve the line intervals passed to `layoutNextLineRange`.
149|
150|### Measured spans beat magic padding
151|
152|When a logo or bitmap is rasterized into cells, measure the actual occupied cells per row and then add a small halo. Do not use one giant bounding box. Tight measured spans make the text read as if it is flowing around the letter shapes.
153|
154|```js
155|const rowMin = new Float32Array(rows).fill(Infinity);
156|const rowMax = new Float32Array(rows).fill(-Infinity);
157|
158|for (const cell of visibleCells) {
159|  rowMin[cell.row] = Math.min(rowMin[cell.row], cell.x);
160|  rowMax[cell.row] = Math.max(rowMax[cell.row], cell.x + CELL_W);
161|}
162|
163|for (let row = 0; row < rows; row++) {
164|  if (!Number.isFinite(rowMin[row])) continue;
165|  obstacleRows[row].push([rowMin[row] - halo, rowMax[row] + halo]);
166|}
167|```
168|
169|For sharp pixel-art letters, smooth adjacent rows before pushing spans. A 1-2 row halo usually prevents code/prose from touching corners without losing the letter silhouette.
170|
171|### Morphing shapes need morphing obstacles
172|
173|If the visible object morphs (sphere to cube, logo to particles, etc.), tween the collision field too. A convincing demo uses the same `mix` value for both the rendered buffer and the pretext obstacle rows.
174|
175|```js
176|function pushMorphedRows(aRows, bRows, mix) {
177|  for (let row = 0; row < rows; row++) {
178|    const a = aRows[row] ?? [centerX, centerX];
179|    const b = bRows[row] ?? [centerX, centerX];
180|    obstacleRows[row].push([
181|      a[0] + (b[0] - a[0]) * mix,
182|      a[1] + (b[1] - a[1]) * mix,
183|    ]);
184|  }
185|}
186|```
187|
188|Without this, the artwork may morph while the text still wraps around the old shape, which breaks the pretext effect.
189|
190|### Separate visual layers from collision
191|
192|Use separate canvases when visual treatment should not affect layout. For example, fade an ASCII object with CSS opacity on its own canvas layer, but keep its obstacle rows controlled by explicit shape state. Fading glyph intensity or scaling obstacle spans often looks like the object is shrinking instead of fading.
193|
194|## 5. Editorial multi-column with shared cursor
195|
196|Classic magazine layout: three columns, text flows from the end of column 1 into the top of column 2, etc. Pretext makes this trivial because the cursor is portable between `layoutNextLineRange` calls.
197|
198|```js
199|const prepared = prepareWithSegments(ARTICLE, FONT);
200|let cursor = { segmentIndex: 0, graphemeIndex: 0 };
201|
202|for (const col of [COL1, COL2, COL3]) {
203|  let y = col.y;
204|  while (y < col.y + col.h) {
205|    const range = layoutNextLineRange(prepared, cursor, col.w);
206|    if (!range) return;
207|    const line = materializeLineRange(prepared, range);
208|    ctx.fillText(line.text, col.x, y);
209|    cursor = range.end;
210|    y += LINE_H;
211|  }
212|}
213|```
214|
215|Add pull quotes by treating them as obstacles in the middle column and using pattern #1 around them.
216|
217|## 6. Multiline shrink-wrap (tightest-fitting card)
218|
219|Given a max width, find the **smallest** container width that still produces the same line count. Useful for chat bubbles, quote cards, tooltip sizing.
220|
221|```js
222|const prepared = prepareWithSegments(text, FONT);
223|const { lineCount, maxLineWidth } = measureLineStats(prepared, MAX_W);
224|// card width = maxLineWidth + padding; card height = lineCount * LINE_H + padding
225|```
226|
227|For a demo that *visualizes* this, render the card shrinking from `MAX_W` down to `maxLineWidth` over a second — the line count stays constant but the right edge pulls in.
228|
229|## 7. Kinetic typography
230|
231|Animate per-line transforms over time. `layoutWithLines` gives you stable lines; index `i` drives the timing offset.
232|
233|```js
234|const { lines } = layoutWithLines(prepared, W - 80, 40);
235|function frame(t) {
236|  for (let i = 0; i < lines.length; i++) {
237|    const phase = t * 0.001 - i * 0.15;
238|    const y = 100 + i * 40 + Math.sin(phase) * 12;
239|    const opacity = 0.4 + 0.6 * Math.max(0, Math.sin(phase));
240|    ctx.globalAlpha = opacity;
241|    ctx.fillText(lines[i].text, 40, y);
242|  }
243|}
244|```
245|
246|Variants: Star Wars crawl (perspective skew per line), wave (sine y-offset), bounce (ease-in-out arrival), glitch (per-glyph random offset using `Intl.Segmenter`).
247|
248|## 8. Font stack patterns
249|
250|| Vibe | Font string | Palette hint |
251||------|-------------|--------------|
252|| Editorial / serious | `17px/1.4 "Iowan Old Style", Georgia, serif` | bone `#e8e6df` on charcoal `#0c0d10` |
253|| CRT / terminal | `600 13px "JetBrains Mono", ui-monospace, monospace` | amber `hsl(38 60% 62%)` on `#07070a` |
254|| Humanist / modern | `500 17px Inter, ui-sans-serif, system-ui, sans-serif` | off-white `#f3efe6` on deep-navy `#0b1020` |
255|| Display / poster | `700 64px "Playfair Display", serif` | hot-red `#ff4130` on cream `#f0ebe0` |
256|| Engineering | `14px "IBM Plex Mono", monospace` | neon-green `#7cff7c` on near-black `#0a0a0c` |
257|
258|Always load the web font explicitly (Google Fonts link tag or `@font-face`) so the canvas measurement matches the CSS render.
259|