# Microsoft / Outlook.com Web Login Flow

## Typical Login Sequence (Outlook.com, Microsoft 365, Azure, etc.)

1. Navigate to the target URL (e.g., `https://outlook.live.com/mail/0/`)
2. **Accept cookies** if a cookie consent banner appears (button "接受" / "Accept")
3. Click **登录 / Sign in**
4. Enter the email address → click **下一步 / Next**
5. ⚠️ **Verification step**: Microsoft sends a code to the email. The page changes to "获取用于登录的代码" (Getting a code to sign in). The user must provide this code to continue.
6. After successful verification, password is requested (if applicable)

## Key Pages / States

### State: Email Entry Page
- Textbox: `请输入电子邮件、电话或 Skype` (Enter email/phone/Skype)
- Button: `下一步` (Next)

### State: Verification Required
- Heading: `获取用于登录的代码` (Getting a code to sign in)
- Button: `发送通知` (Send notification — resent code)
- Button: `其他登录方法` (Other sign-in methods)
- The code arrives in the inbox and must be typed/provided by the user

### State: Password Entry
- Password field after email+verification confirmed

## Common Pitfalls

### "Unknown ref" error after navigation
**Symptom**: `browser_type` or `browser_click` fails with "Unknown ref" even though the element is visible.

**Cause**: The DOM snapshot refs become stale after a page transition/navigation or when the page updates dynamically.

**Fix**: Re-run `browser_snapshot()` to refresh refs before interacting with elements after a page change.

### Verification step blocks automation
**Symptom**: The agent cannot proceed past the "获取用于登录的代码" page without user input.

**Cause**: Microsoft requires a code sent to the registered email — this is a manual step.

**Mitigation**: Ask the user for the verification code. Do not attempt to bypass or "guess" the code.

## Reference: zl778@outlook.com Login Notes
- Email: `zl778@outlook.com`
- Verification code is sent to this inbox — user must provide the code to continue