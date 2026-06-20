# Himalaya Configuration Reference

Configuration file location: `~/.config/himalaya/config.toml`

## Minimal IMAP + SMTP Setup

```toml
[accounts.default]
email = "user@example.com"
display-name = "Your Name"
default = true

# IMAP backend for reading emails
backend.type = "imap"
backend.host = "imap.example.com"
backend.port = 993
backend.encryption.type = "tls"
backend.login = "user@example.com"
backend.auth.type = "password"
backend.auth.raw = "your-password"

# SMTP backend for sending emails
message.send.backend.type = "smtp"
message.send.backend.host = "smtp.example.com"
message.send.backend.port = 587
message.send.backend.encryption.type = "start-tls"
message.send.backend.login = "user@example.com"
backend.auth.type = "password"
message.send.backend.auth.raw = "your-password"

# Folder aliases — required whenever server folder names differ
# from himalaya's canonical names. See "Folder Aliases" below.
folder.aliases.inbox = "INBOX"
folder.aliases.sent = "Sent"
folder.aliases.drafts = "Drafts"
folder.aliases.trash = "Trash"
```

## Password Options

### Raw password (testing only, not recommended)

```toml
backend.auth.raw = "your-password"
```

### Password from command (recommended)

```toml
backend.auth.cmd = "pass show email/imap"
# backend.auth.cmd = "security find-generic-password -a user@example.com -s imap -w"
```

### System keyring (requires keyring feature)

```toml
backend.auth.keyring = "imap-example"
```

Then run `himalaya account configure <account>` to store the password.

## QQ Mail (QQ邮箱) Configuration

QQ Mail requires an **authorization code** (授权码), not the account password.
Generate one at: QQ Mail web → Settings → Account → Enable IMAP/SMTP service.

```toml
[accounts.qq]
email = "yourname@qq.com"
display-name = "Your Name"
default = true

backend.type = "imap"
backend.host = "imap.qq.com"
backend.port = 993
backend.encryption.type = "tls"
backend.login = "yourname@qq.com"
backend.auth.type = "password"
backend.auth.cmd = "echo your-auth-code"

message.send.backend.type = "smtp"
message.send.backend.host = "smtp.qq.com"
message.send.backend.port = 465
message.send.backend.encryption.type = "tls"
message.send.backend.login = "yourname@qq.com"
backend.auth.type = "password"
message.send.backend.auth.cmd = "echo your-auth-code"

[accounts.qq.folder.aliases]
inbox = "INBOX"
sent = "Sent Messages"
drafts = "Drafts"
trash = "Deleted Messages"
```

> **QQ SMTP 465 requires direct SSL (SMTPS), not STARTTLS.** QQ
> Mail's official SMTP port 465 is SMTPS. Using STARTTLS on 465
> causes connection failures/timeouts. In Himalaya TOML, set
> `encryption.type = "tls"` for 465 and `"start-tls"` only for 587.
>
> **Known QQ Mail quirk:** QQ Mail's IMAP server does not return a UID
> after APPEND. Himalaya reports `cannot find UID of appended IMAP
> message` and exits code 1, but SMTP delivery **succeeds** and the copy
> **is** saved to Sent. The error is a false negative — the actual
> delivery worked.
>
> **Workaround:** Use Python `smtplib.SMTP_SSL` to bypass the IMAP
> APPEND step entirely, especially from Hermes gateway or automated
> scripts:
> ```python
> import smtplib, ssl, email
>
> msg = email.message.EmailMessage()
> msg['From'] = 'yourname@qq.com'
> msg['To'] = 'recipient@example.com'
> msg['Subject'] = 'Hello'
> msg.set_content('Body')
>
> ctx = ssl.create_default_context()
> with smtplib.SMTP_SSL('smtp.qq.com', 465, context=ctx) as s:
>     s.login('yourname@qq.com', 'your-auth-code')
>     s.send_message(msg)
> ```

## Gmail Configuration

```toml
[accounts.gmail]
email = "you@gmail.com"
display-name = "Your Name"
default = true

backend.type = "imap"
backend.host = "imap.gmail.com"
backend.port = 993
backend.encryption.type = "tls"
backend.login = "you@gmail.com"
backend.auth.type = "password"
backend.auth.cmd = "pass show google/app-password"

message.send.backend.type = "smtp"
message.send.backend.host = "smtp.gmail.com"
message.send.backend.port = 587
message.send.backend.encoding.type = "start-tls"
message.send.backend.login = "you@gmail.com"
backend.auth.type = "password"
message.send.backend.auth.cmd = "pass show google/app-password"

# Gmail folder mapping. Without these, save-to-Sent fails after
# SMTP delivery succeeds (Gmail's Sent folder is `[Gmail]/Sent Mail`,
# not `Sent`), and `himalaya message send` exits non-zero. Any
# caller that retries on that error code will re-run SMTP — duplicate
# emails to recipients. Always include this block for Gmail.
folder.aliases.inbox = "INBOX"
folder.aliases.sent = "[Gmail]/Sent Mail"
folder.aliases.drafts = "[Gmail]/Drafts"
folder.aliases.trash = "[Gmail]/Trash"
```

**Note:** Gmail requires an App Password if 2FA is enabled.

## iCloud Configuration

```toml
[accounts.icloud]
email = "you@icloud.com"
display-name = "Your Name"

backend.type = "imap"
backend.host = "imap.mail.me.com"
backend.port = 993
backend.encryption.type = "tls"
backend.login = "you@icloud.com"
backend.auth.type = "password"
backend.auth.cmd = "pass show icloud/app-password"

message.send.backend.type = "smtp"
message.send.backend.host = "smtp.mail.me.com"
message.send.backend.port = 587
message.send.backend.encryption.type = "start-tls"
message.send.backend.login = "you@icloud.com"
backend.auth.type = "password"
message.send.backend.auth.cmd = "pass show icloud/app-password"
```

**Note:** Generate an app-specific password at appleid.apple.com

## Folder Aliases

Map himalaya's canonical folder names (`inbox`, `sent`, `drafts`,
`trash`) to whatever the server actually calls them.

> **Don't use the singular `alias` form.** Pre-v1.2.0 docs showed
> `[accounts.NAME.folder.alias]` (singular). v1.2.0 silently
> ignores that sub-section — TOML parses without error, but the
> alias resolver never reads it. Every lookup then falls through
> to the canonical name. On Gmail (where `sent` is actually
> `[Gmail]/Sent Mail`) this means save-to-Sent fails *after* SMTP
> delivery succeeds, and `himalaya message send` exits non-zero.
> Any caller that retries on that error code will re-run the send —
> including SMTP — producing duplicate emails to recipients. Always
> use `folder.aliases.X` (plural).

## Multiple Accounts

```toml
[accounts.personal]
email = "personal@example.com"
default = true
# ... backend config ...

[accounts.work]
email = "work@company.com"
# ... backend config ...
```

Switch accounts with `--account`:

```bash
himalaya --account work envelope list
```

## Notmuch Backend (local mail)

```toml
[accounts.local]
email = "user@example.com"

backend.type = "notmuch"
backend.db-path = "~/.mail/.notmuch"
```

## OAuth2 Authentication (for providers that support it)

```toml
backend.auth.type = "oauth2"
backend.auth.client-id = "your-client-id"
backend.auth.client-secret.cmd = "pass show oauth/client-secret"
backend.auth.access-token.cmd = "pass show oauth/access-token"
backend.auth.refresh-token.cmd = "pass show oauth/refresh-token"
backend.auth.auth-url = "https://provider.com/oauth/authorize"
backend.auth.token-url = "https://provider.com/oauth/token"
```

## Additional Options

### Signature

```toml
[accounts.default]
signature = "Best regards,\nYour Name"
signature-delim = "-- \n"
```

### Downloads directory

```toml
[accounts.default]
downloads-dir = "~/Downloads/himalaya"
```

### Editor for composing

Set via environment variable:

```bash
export EDITOR="vim"
```
