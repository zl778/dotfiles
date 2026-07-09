---
name: hugo-site-setup
description: "Set up a Hugo static site with PaperMod theme, GitHub, and Cloudflare Pages — full workflow from init to deployment."
version: 1.0.0
created_by: agent
platforms: [macos, linux]
---

# Hugo Site Setup (PaperMod + GitHub + Cloudflare Pages)

Full workflow for initializing a Hugo static site, installing PaperMod,
configuring it, writing content, and deploying via GitHub + Cloudflare Pages.

## Prerequisites

- Hugo installed (`brew install hugo` or from [gohugo.io](https://gohugo.io))
- Git installed
- `gh` CLI installed and authenticated (`gh auth status`)
- Cloudflare account (for Pages deployment)

## Step-by-Step

### 1. Initialize the Hugo Site

```bash
hugo new site <project-name>
cd <project-name>
git init
git branch -m main
```

> Hugo v0.158+ uses `hugo.toml` (TOML format). Older versions use `config.toml`.

### 2. Install PaperMod Theme

```bash
git submodule add --depth=1 https://github.com/adityatelange/hugo-PaperMod themes/PaperMod
```

### 3. Configure `hugo.toml`

Basic configuration for PaperMod:

```toml
baseURL = 'https://yourdomain.com/'
locale = 'zh-cn'
title = 'Your Site Title'
theme = 'PaperMod'

[params]
  defaultTheme = 'auto'
  ShowReadingTime = true
  ShowPostNavLinks = true
  ShowBreadCrumbs = true
  ShowCodeCopyButtons = true
  ShowWordCount = true
  UseHugoToc = true
  comments = false

  [params.homeInfoParams]
    Title = 'Welcome 👋'
    Content = 'Your tagline here'

  # Social icons (TOML array-of-tables format)
  [[params.socialIcons]]
    name = 'github'
    url = 'https://github.com/username'
  [[params.socialIcons]]
    name = 'email'
    url = 'mailto:user@example.com'

[[menu.main]]
  identifier = 'posts'
  name = '博客'
  url = '/posts/'
  weight = 10

[[menu.main]]
  identifier = 'about'
  name = '关于'
  url = '/about/'
  weight = 20

[[menu.main]]
  identifier = 'search'
  name = '搜索'
  url = '/search/'
  weight = 30

[outputs]
  home = ['HTML', 'RSS', 'JSON']
```

> **Pitfall**: `homeInfoParams` is a **TOML section/table** (`[params.homeInfoParams]`), NOT a boolean.
> Setting `homeInfoParams = true` causes a template error (`can't evaluate field Title in type bool`).

### 4. Create Content Structure

```bash
mkdir -p content/posts
echo '.DS_Store\n.hugo_build.lock\nresources/\npublic/' > .gitignore
```

**First post** (`content/posts/hello-world.md`):
```markdown
---
title: 'First Post'
date: 2026-01-01T00:00:00+08:00
draft: false
tags:
  - welcome
---

Content here...
```

**About page** (`content/about.md`):
```markdown
---
title: 'About'
date: 2026-01-01T00:00:00+08:00
---

Your about content...
```

**Search page** (`content/search.md`) — REQUIRED for PaperMod's search feature:
```markdown
---
title: 'Search'
layout: 'search'
---
```

### 5. Build & Preview

```bash
# Production build
hugo --gc --minify

# Local preview with drafts
hugo server --buildDrafts --bind 0.0.0.0 --port 1313
```

> Hugo v0.158+ deprecation warnings (benign):
> - `.Language.LanguageDirection` → `.Language.Direction`
> - `.Language.LanguageCode` → `.Language.Locale`

### 6. Push to GitHub

```bash
# Create repo via gh CLI
gh repo create <repo-name> --private --push --source .

# Or manually:
git remote add origin git@github.com:username/repo.git
git add -A
git commit -m "initial: Hugo site with PaperMod"
git push -u origin main
```

### 7. Deploy to Cloudflare Pages

1. Go to [Cloudflare Dashboard](https://dash.cloudflare.com/) → **Workers & Pages** → **Create** → **Pages** → **Connect to Git**
2. Authorize GitHub → select the repo
3. Build settings:
   - **Build command**: `hugo --gc --minify`
   - **Build output**: `public`
4. **Environment variables** (if needed): `HUGO_VERSION = 0.163.0` (pin to match local version)
5. Add custom domain in Cloudflare Pages dashboard
6. Add DNS record (if using subdomain): `blog CNAME your-project.pages.dev`

## User-specific Preferences (this user)

- Chinese locale (`zh-cn`) for content
- PaperMod is the preferred theme
- Projects stored under OneDrive: `/Users/liangzhu/Library/CloudStorage/OneDrive-个人/2026-02-12 pistachio26/`
- Domain: `61877778.xyz` (Cloudflare)
- GitHub: `zl778` (SSH auth)

## Troubleshooting

| Issue | Fix |
|-------|-----|
| `homeInfoParams = true` error | Change to TOML table `[params.homeInfoParams]` with Title/Content fields |
| Build fails: missing theme | Ensure theme is installed: `ls themes/PaperMod/` |
| Search page 404 | Create `content/search.md` with `layout: 'search'` frontmatter |
| Cloudflare deploy fails | Pin `HUGO_VERSION` env var in Pages dashboard to match local version |
| DNS not resolving | Add CNAME record in Cloudflare DNS, ensure orange cloud (proxied) is enabled |
