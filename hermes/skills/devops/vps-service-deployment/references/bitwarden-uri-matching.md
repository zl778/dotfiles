# Bitwarden URI Matching — Subdomain Credential Filtering

## Problem

When multiple services share the same base domain (e.g. `vault.61877778.xyz`, `uptime.61877778.xyz`, `beszel.61877778.xyz`), Bitwarden's default "Base domain" URI matching shows credentials for ALL subdomains when visiting any one of them.

## Fix: Change URI match type to "Host"

In the Bitwarden browser extension or app:

1. Open the login entry (e.g. `vault.61877778.xyz`)
2. Click **Edit**
3. Find the URI field → click the **gear icon ⚙️** next to it
4. Change **"Base domain"** → **"Host"**
5. **Save**

Repeat for every entry that should ONLY match its exact hostname.

## Match type behavior

| Type | Behavior | Example |
|:----|:---------|:--------|
| **Base domain** (default) | Matches any subdomain of the same root domain | `vault.X.com` shows on `uptime.X.com` |
| **Host** | Matches only the exact hostname | `vault.X.com` only shows on `vault.X.com` |
| **Starts with** | Matches by URL prefix | Custom prefix matching |
| **Regex** | Custom regex pattern | Full flexibility |
| **Exact** | Exact URL match | Least flexible |

## Recommendation

Set ALL credentials for `*.61877778.xyz` services to **"Host"** — only the login page you're actually visiting will pop up.