---
name: hugo-static-site
description: "Initialize, configure, theme, and deploy Hugo static sites — PaperMod setup, content creation, Cloudflare Pages deployment."
version: 1.0.0
---

# Hugo Static Site (PaperMod + Cloudflare Pages)

Initialize a Hugo blog/site, install the PaperMod theme, configure it, create content, push to GitHub, and auto-deploy via Cloudflare Pages.

**Prerequisites:**
- Hugo installed (`brew install hugo`)
- GitHub CLI (`gh auth status`)
- Cloudflare account with Pages enabled

---

## 1. Initialize Site

```bash
hugo new site <project-name>
cd <project-name>
git init
git branch -m main
```

Hugo v0.163+ uses `hugo.toml` (not `config.toml`).

## 2. Install PaperMod Theme

```bash
git submodule add --depth=1 https://github.com/adityatelange/hugo-PaperMod themes/PaperMod
```

## 3. Configure `hugo.toml`

Key settings for PaperMod:

```toml
baseURL = 'https://<your-domain>/'
buildFuture = true           # REQUIRED if post dates are near today's date
locale = 'zh-cn'             # or 'en-us'
title = '<Your Name>'
theme = 'PaperMod'

[params]
  defaultTheme = 'auto'
  ShowReadingTime = true
  ShowCodeCopyButtons = true
  UseHugoToc = true
  comments = false

  # Homepage greeting (NOT a boolean — must be a section)
  [params.homeInfoParams]
    Title = 'Hi, I am ...'
    Content = 'Welcome to my site'

  # Social icons
  [[params.socialIcons]]
    name = 'github'
    url = 'https://github.com/<user>'

# Menu
[[menu.main]]
  identifier = 'posts'
  name = '博客'
  url = '/posts/'
  weight = 10

[[menu.main]]
  identifier = 'search'
  name = '搜索'
  url = '/search/'
  weight = 20

[outputs]
  home = ['HTML', 'RSS', 'JSON']
```

**Pitfalls:**
- `homeInfoParams` must be a TOML section (`[params.homeInfoParams]` with `Title`/`Content`), NOT `homeInfoParams = true` — that causes a template error.
- `buildFuture = true` is needed when post dates are close to or past the current time. Without it, Hugo silently skips posts with future dates (the `hugo list all` command shows them, but they don't appear in `public/`).

## 4. Create Content

Create a search page for PaperMod:

```markdown
---
title: '搜索'
layout: 'search'
---
```

Create a normal post:

```markdown
---
title: 'Post Title'
date: YYYY-MM-DDTHH:MM:SS+08:00
draft: false
tags: [tag1, tag2]
categories:
  - 分类名
description: '...'
---

Content here...
```

### Migrating from Obsidian

When moving a note from Obsidian vault to Hugo:
1. Find the note via `find .../PKM/ -name '*keyword*'`
2. Read the content
3. Strip Obsidian-specific HTML (`<font color="...">`, etc.)
4. Convert to standard markdown with Hugo frontmatter
5. Write to `content/posts/<slug>.md`

## 5. Build & Test

```bash
hugo --gc --minify              # Static build
hugo server --buildDrafts       # Live preview at http://localhost:1313
```

Check individual post rendering:
```bash
hugo list all                   # Verify pages are recognized
find public -name '*.html' | sort  # Check output files
```

## 6. Deploy to Cloudflare Pages

### Via Cloudflare Dashboard
1. Go to Cloudflare Dashboard → **Workers & Pages**
2. Click **Create application** → **Pages** → **Connect to Git**
3. Select GitHub repo → configure:

| Setting | Value |
|---------|-------|
| Framework preset | `Hugo` |
| Build command | `hugo --gc --minify` |
| Build output directory | `public` |
| Production branch | `main` |

4. Enable auto-deploy
5. After first deploy → **Custom domains** → add `blog.<your-domain>.xyz`

### Git Disconnect Fix
If a yellow warning says "此项目已与您的 Git 帐户断开连接":
1. Click **Manage** or **Disconnect** then reconnect
2. Re-authorize GitHub
3. The next push auto-triggers deploy

## 7. Content Git Workflow

```bash
git add -A
git commit -m '描述更新内容'
git push
```

Cloudflare Pages auto-deploys on every push to `main`.
