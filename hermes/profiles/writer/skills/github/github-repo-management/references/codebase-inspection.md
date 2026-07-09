1|---
2|name: codebase-inspection
3|description: "Inspect codebases w/ pygount: LOC, languages, ratios."
4|version: 1.0.0
5|author: Hermes Agent
6|license: MIT
7|platforms: [linux, macos, windows]
8|metadata:
9|  hermes:
10|    tags: [LOC, Code Analysis, pygount, Codebase, Metrics, Repository]
11|    related_skills: [github-repo-management]
12|prerequisites:
13|  commands: [pygount]
14|---
15|
16|# Codebase Inspection with pygount
17|
18|Analyze repositories for lines of code, language breakdown, file counts, and code-vs-comment ratios using `pygount`.
19|
20|## When to Use
21|
22|- User asks for LOC (lines of code) count
23|- User wants a language breakdown of a repo
24|- User asks about codebase size or composition
25|- User wants code-vs-comment ratios
26|- General "how big is this repo" questions
27|
28|## Prerequisites
29|
30|```bash
31|pip install --break-system-packages pygount 2>/dev/null || pip install pygount
32|```
33|
34|## 1. Basic Summary (Most Common)
35|
36|Get a full language breakdown with file counts, code lines, and comment lines:
37|
38|```bash
39|cd /path/to/repo
40|pygount --format=summary \
41|  --folders-to-skip=".git,node_modules,venv,.venv,__pycache__,.cache,dist,build,.next,.tox,.eggs,*.egg-info" \
42|  .
43|```
44|
45|**IMPORTANT:** Always use `--folders-to-skip` to exclude dependency/build directories, otherwise pygount will crawl them and take a very long time or hang.
46|
47|## 2. Common Folder Exclusions
48|
49|Adjust based on the project type:
50|
51|```bash
52|# Python projects
53|--folders-to-skip=".git,venv,.venv,__pycache__,.cache,dist,build,.tox,.eggs,.mypy_cache"
54|
55|# JavaScript/TypeScript projects
56|--folders-to-skip=".git,node_modules,dist,build,.next,.cache,.turbo,coverage"
57|
58|# General catch-all
59|--folders-to-skip=".git,node_modules,venv,.venv,__pycache__,.cache,dist,build,.next,.tox,vendor,third_party"
60|```
61|
62|## 3. Filter by Specific Language
63|
64|```bash
65|# Only count Python files
66|pygount --suffix=py --format=summary .
67|
68|# Only count Python and YAML
69|pygount --suffix=py,yaml,yml --format=summary .
70|```
71|
72|## 4. Detailed File-by-File Output
73|
74|```bash
75|# Default format shows per-file breakdown
76|pygount --folders-to-skip=".git,node_modules,venv" .
77|
78|# Sort by code lines (pipe through sort)
79|pygount --folders-to-skip=".git,node_modules,venv" . | sort -t$'\t' -k1 -nr | head -20
80|```
81|
82|## 5. Output Formats
83|
84|```bash
85|# Summary table (default recommendation)
86|pygount --format=summary .
87|
88|# JSON output for programmatic use
89|pygount --format=json .
90|
91|# Pipe-friendly: Language, file count, code, docs, empty, string
92|pygount --format=summary . 2>/dev/null
93|```
94|
95|## 6. Interpreting Results
96|
97|The summary table columns:
98|- **Language** — detected programming language
99|- **Files** — number of files of that language
100|- **Code** — lines of actual code (executable/declarative)
101|- **Comment** — lines that are comments or documentation
102|- **%** — percentage of total
103|
104|Special pseudo-languages:
105|- `__empty__` — empty files
106|- `__binary__` — binary files (images, compiled, etc.)
107|- `__generated__` — auto-generated files (detected heuristically)
108|- `__duplicate__` — files with identical content
109|- `__unknown__` — unrecognized file types
110|
111|## Pitfalls
112|
113|1. **Always exclude .git, node_modules, venv** — without `--folders-to-skip`, pygount will crawl everything and may take minutes or hang on large dependency trees.
114|2. **Markdown shows 0 code lines** — pygount classifies all Markdown content as comments, not code. This is expected behavior.
115|3. **JSON files show low code counts** — pygount may count JSON lines conservatively. For accurate JSON line counts, use `wc -l` directly.
116|4. **Large monorepos** — for very large repos, consider using `--suffix` to target specific languages rather than scanning everything.
117|