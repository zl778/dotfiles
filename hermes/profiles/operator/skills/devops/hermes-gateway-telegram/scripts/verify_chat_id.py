#!/usr/bin/env python3
"""
Verify a Telegram chat ID by calling the Bot API's getChat endpoint.

Usage:
  python3 verify_chat_id.py <bot_token> <chat_id>

Returns exit code 0 if the bot can see the chat, 1 if not.
"""
import requests
import sys

def verify_chat_id(token: str, chat_id: str):
    """Try the ID as given, then try negative if it looks positive."""
    attempts = [chat_id]
    raw = chat_id.lstrip("-")
    if chat_id == raw:
        attempts.append(f"-{raw}")       # positive → try negative
        attempts.append(f"-100{raw}")    # positive → try supergroup format
    else:
        attempts.append(raw)             # negative → try positive

    for cid in attempts:
        try:
            r = requests.get(
                f"https://api.telegram.org/bot{token}/getChat",
                params={"chat_id": cid},
                timeout=10,
            )
            data = r.json()
            if data.get("ok"):
                result = data["result"]
                print(f"✅ Chat found!")
                print(f"   ID:    {result['id']}")
                print(f"   Type:  {result.get('type')}")
                print(f"   Title: {result.get('title', '(no title)')}")
                return True
        except requests.RequestException as e:
            print(f"⚠️  API error for {cid}: {e}")

    print(f"❌ Chat '{chat_id}' not found — bot cannot see this chat.")
    print(f"   Verify: (1) bot is in the group, (2) privacy mode is off,")
    print(f"   (3) the ID is correct (use @get_id_bot inside the group).")
    return False

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(f"Usage: {sys.argv[0]} <bot_token> <chat_id>")
        sys.exit(1)
    success = verify_chat_id(sys.argv[1], sys.argv[2])
    sys.exit(0 if success else 1)
