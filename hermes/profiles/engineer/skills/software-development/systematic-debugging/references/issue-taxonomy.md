1|# Issue Taxonomy
2|
3|Use this taxonomy to classify issues found during dogfood QA testing.
4|
5|## Severity Levels
6|
7|### Critical
8|The issue makes a core feature completely unusable or causes data loss.
9|
10|**Examples:**
11|- Application crashes or shows a blank white page
12|- Form submission silently loses user data
13|- Authentication is completely broken (can't log in at all)
14|- Payment flow fails and charges the user without completing the order
15|- Security vulnerability (e.g., XSS, exposed credentials in console)
16|
17|### High
18|The issue significantly impairs functionality but a workaround may exist.
19|
20|**Examples:**
21|- A key button does nothing when clicked (but refreshing fixes it)
22|- Search returns no results for valid queries
23|- Form validation rejects valid input
24|- Page loads but critical content is missing or garbled
25|- Navigation link leads to a 404 or wrong page
26|- Uncaught JavaScript exceptions in the console on core pages
27|
28|### Medium
29|The issue is noticeable and affects user experience but doesn't block core functionality.
30|
31|**Examples:**
32|- Layout is misaligned or overlapping on certain screen sections
33|- Images fail to load (broken image icons)
34|- Slow performance (visible loading delays > 3 seconds)
35|- Form field lacks proper validation feedback (no error message on bad input)
36|- Console warnings that suggest deprecated or misconfigured features
37|- Inconsistent styling between similar pages
38|
39|### Low
40|Minor polish issues that don't affect functionality.
41|
42|**Examples:**
43|- Typos or grammatical errors in text content
44|- Minor spacing or alignment inconsistencies
45|- Placeholder text left in production ("Lorem ipsum")
46|- Favicon missing
47|- Console info/debug messages that shouldn't be in production
48|- Subtle color contrast issues that don't fail WCAG requirements
49|
50|## Categories
51|
52|### Functional
53|Issues where features don't work as expected.
54|
55|- Buttons/links that don't respond
56|- Forms that don't submit or submit incorrectly
57|- Broken user flows (can't complete a multi-step process)
58|- Incorrect data displayed
59|- Features that work partially
60|
61|### Visual
62|Issues with the visual presentation of the page.
63|
64|- Layout problems (overlapping elements, broken grids)
65|- Broken images or missing media
66|- Styling inconsistencies
67|- Responsive design failures
68|- Z-index issues (elements hidden behind others)
69|- Text overflow or truncation
70|
71|### Accessibility
72|Issues that prevent or hinder access for users with disabilities.
73|
74|- Missing alt text on meaningful images
75|- Poor color contrast (fails WCAG AA)
76|- Elements not reachable via keyboard navigation
77|- Missing form labels or ARIA attributes
78|- Focus indicators missing or unclear
79|- Screen reader incompatible content
80|
81|### Console
82|Issues detected through JavaScript console output.
83|
84|- Uncaught exceptions and unhandled promise rejections
85|- Failed network requests (4xx, 5xx errors in console)
86|- Deprecation warnings
87|- CORS errors
88|- Mixed content warnings (HTTP resources on HTTPS page)
89|- Excessive console.log output left from development
90|
91|### UX (User Experience)
92|Issues where functionality works but the experience is poor.
93|
94|- Confusing navigation or information architecture
95|- Missing loading indicators (user doesn't know something is happening)
96|- No feedback after user actions (e.g., button click with no visible result)
97|- Inconsistent interaction patterns
98|- Missing confirmation dialogs for destructive actions
99|- Poor error messages that don't help the user recover
100|
101|### Content
102|Issues with the text, media, or information on the page.
103|
104|- Typos and grammatical errors
105|- Placeholder/dummy content in production
106|- Outdated information
107|- Missing content (empty sections)
108|- Broken or dead links to external resources
109|- Incorrect or misleading labels
110|