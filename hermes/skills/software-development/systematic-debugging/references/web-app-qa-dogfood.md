1|---
2|name: dogfood
3|description: "Exploratory QA of web apps: find bugs, evidence, reports."
4|version: 1.0.0
5|platforms: [linux, macos, windows]
6|metadata:
7|  hermes:
8|    tags: [qa, testing, browser, web, dogfood]
9|    related_skills: []
10|---
11|
12|# Dogfood: Systematic Web Application QA Testing
13|
14|## Overview
15|
16|This skill guides you through systematic exploratory QA testing of web applications using the browser toolset. You will navigate the application, interact with elements, capture evidence of issues, and produce a structured bug report.
17|
18|## Prerequisites
19|
20|- Browser toolset must be available (`browser_navigate`, `browser_snapshot`, `browser_click`, `browser_type`, `browser_vision`, `browser_console`, `browser_scroll`, `browser_back`, `browser_press`)
21|- A target URL and testing scope from the user
22|
23|## Inputs
24|
25|The user provides:
26|1. **Target URL** — the entry point for testing
27|2. **Scope** — what areas/features to focus on (or "full site" for comprehensive testing)
28|3. **Output directory** (optional) — where to save screenshots and the report (default: `./dogfood-output`)
29|
30|## Workflow
31|
32|Follow this 5-phase systematic workflow:
33|
34|### Phase 1: Plan
35|
36|1. Create the output directory structure:
37|   ```
38|   {output_dir}/
39|   ├── screenshots/       # Evidence screenshots
40|   └── report.md          # Final report (generated in Phase 5)
41|   ```
42|2. Identify the testing scope based on user input.
43|3. Build a rough sitemap by planning which pages and features to test:
44|   - Landing/home page
45|   - Navigation links (header, footer, sidebar)
46|   - Key user flows (sign up, login, search, checkout, etc.)
47|   - Forms and interactive elements
48|   - Edge cases (empty states, error pages, 404s)
49|
50|### Phase 2: Explore
51|
52|For each page or feature in your plan:
53|
54|1. **Navigate** to the page:
55|   ```
56|   browser_navigate(url="https://example.com/page")
57|   ```
58|
59|2. **Take a snapshot** to understand the DOM structure:
60|   ```
61|   browser_snapshot()
62|   ```
63|
64|3. **Check the console** for JavaScript errors:
65|   ```
66|   browser_console(clear=true)
67|   ```
68|   Do this after every navigation and after every significant interaction. Silent JS errors are high-value findings.
69|
70|4. **Take an annotated screenshot** to visually assess the page and identify interactive elements:
71|   ```
72|   browser_vision(question="Describe the page layout, identify any visual issues, broken elements, or accessibility concerns", annotate=true)
73|   ```
74|   The `annotate=true` flag overlays numbered `[N]` labels on interactive elements. Each `[N]` maps to ref `@eN` for subsequent browser commands.
75|
76|5. **Test interactive elements** systematically:
77|   - Click buttons and links: `browser_click(ref="@eN")`
78|   - Fill forms: `browser_type(ref="@eN", text="test input")`
79|   - Test keyboard navigation: `browser_press(key="Tab")`, `browser_press(key="Enter")`
80|   - Scroll through content: `browser_scroll(direction="down")`
81|   - Test form validation with invalid inputs
82|   - Test empty submissions
83|
84|6. **After each interaction**, check for:
85|   - Console errors: `browser_console()`
86|   - Visual changes: `browser_vision(question="What changed after the interaction?")`
87|   - Expected vs actual behavior
88|
89|### Phase 3: Collect Evidence
90|
91|For every issue found:
92|
93|1. **Take a screenshot** showing the issue:
94|   ```
95|   browser_vision(question="Capture and describe the issue visible on this page", annotate=false)
96|   ```
97|   Save the `screenshot_path` from the response — you will reference it in the report.
98|
99|2. **Record the details**:
100|   - URL where the issue occurs
101|   - Steps to reproduce
102|   - Expected behavior
103|   - Actual behavior
104|   - Console errors (if any)
105|   - Screenshot path
106|
107|3. **Classify the issue** using the issue taxonomy (see `references/issue-taxonomy.md`):
108|   - Severity: Critical / High / Medium / Low
109|   - Category: Functional / Visual / Accessibility / Console / UX / Content
110|
111|### Phase 4: Categorize
112|
113|1. Review all collected issues.
114|2. De-duplicate — merge issues that are the same bug manifesting in different places.
115|3. Assign final severity and category to each issue.
116|4. Sort by severity (Critical first, then High, Medium, Low).
117|5. Count issues by severity and category for the executive summary.
118|
119|### Phase 5: Report
120|
121|Generate the final report using the template at `templates/dogfood-report-template.md`.
122|
123|The report must include:
124|1. **Executive summary** with total issue count, breakdown by severity, and testing scope
125|2. **Per-issue sections** with:
126|   - Issue number and title
127|   - Severity and category badges
128|   - URL where observed
129|   - Description of the issue
130|   - Steps to reproduce
131|   - Expected vs actual behavior
132|   - Screenshot references (use `MEDIA:<screenshot_path>` for inline images)
133|   - Console errors if relevant
134|3. **Summary table** of all issues
135|4. **Testing notes** — what was tested, what was not, any blockers
136|
137|Save the report to `{output_dir}/report.md`.
138|
139|## Tools Reference
140|
141|| Tool | Purpose |
142||------|---------|
143|| `browser_navigate` | Go to a URL |
144|| `browser_snapshot` | Get DOM text snapshot (accessibility tree) |
145|| `browser_click` | Click an element by ref (`@eN`) or text |
146|| `browser_type` | Type into an input field |
147|| `browser_scroll` | Scroll up/down on the page |
148|| `browser_back` | Go back in browser history |
149|| `browser_press` | Press a keyboard key |
150|| `browser_vision` | Screenshot + AI analysis; use `annotate=true` for element labels |
151|| `browser_console` | Get JS console output and errors |
152|
153|## Tips
154|
155|- **Always check `browser_console()` after navigating and after significant interactions.** Silent JS errors are among the most valuable findings.
156|- **Use `annotate=true` with `browser_vision`** when you need to reason about interactive element positions or when the snapshot refs are unclear.
157|- **Test with both valid and invalid inputs** — form validation bugs are common.
158|- **Scroll through long pages** — content below the fold may have rendering issues.
159|- **Test navigation flows** — click through multi-step processes end-to-end.
160|- **Check responsive behavior** by noting any layout issues visible in screenshots.
161|- **Don't forget edge cases**: empty states, very long text, special characters, rapid clicking.
162|- When reporting screenshots to the user, include `MEDIA:<screenshot_path>` so they can see the evidence inline.
163|