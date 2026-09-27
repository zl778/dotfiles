1|# Dogfood QA Report
2|
3|**Target:** {target_url}
4|**Date:** {date}
5|**Scope:** {scope_description}
6|**Tester:** Hermes Agent (automated exploratory QA)
7|
8|---
9|
10|## Executive Summary
11|
12|| Severity | Count |
13||----------|-------|
14|| 🔴 Critical | {critical_count} |
15|| 🟠 High | {high_count} |
16|| 🟡 Medium | {medium_count} |
17|| 🔵 Low | {low_count} |
18|| **Total** | **{total_count}** |
19|
20|**Overall Assessment:** {one_sentence_assessment}
21|
22|---
23|
24|## Issues
25|
26|<!-- Repeat this section for each issue found, sorted by severity (Critical first) -->
27|
28|### Issue #{issue_number}: {issue_title}
29|
30|| Field | Value |
31||-------|-------|
32|| **Severity** | {severity} |
33|| **Category** | {category} |
34|| **URL** | {url_where_found} |
35|
36|**Description:**
37|{detailed_description_of_the_issue}
38|
39|**Steps to Reproduce:**
40|1. {step_1}
41|2. {step_2}
42|3. {step_3}
43|
44|**Expected Behavior:**
45|{what_should_happen}
46|
47|**Actual Behavior:**
48|{what_actually_happens}
49|
50|**Screenshot:**
51|MEDIA:{screenshot_path}
52|
53|**Console Errors** (if applicable):
54|```
55|{console_error_output}
56|```
57|
58|---
59|
60|<!-- End of per-issue section -->
61|
62|## Issues Summary Table
63|
64|| # | Title | Severity | Category | URL |
65||---|-------|----------|----------|-----|
66|| {n} | {title} | {severity} | {category} | {url} |
67|
68|## Testing Coverage
69|
70|### Pages Tested
71|- {list_of_pages_visited}
72|
73|### Features Tested
74|- {list_of_features_exercised}
75|
76|### Not Tested / Out of Scope
77|- {areas_not_covered_and_why}
78|
79|### Blockers
80|- {any_issues_that_prevented_testing_certain_areas}
81|
82|---
83|
84|## Notes
85|
86|{any_additional_observations_or_recommendations}
87|