# BlueBubbles REST API Endpoints

Useful API endpoints for debugging BlueBubbles connectivity and checking messages.

Auth: `?password=<PASSWORD>` (query param) on every request.

## Ping

```bash
curl -s 'http://<SERVER_URL>/api/v1/ping?password=<PASSWORD>'
# → {"status":200,"message":"Ping received!","data":"pong"}
```

## Server Info

```bash
curl -s 'http://<SERVER_URL>/api/v1/server/info?password=<PASSWORD>'
# Shows private_api, helper_connected status
```

## List Chats

```bash
curl -s -X POST 'http://<SERVER_URL>/api/v1/chat/query?password=<PASSWORD>' \
  -H 'Content-Type: application/json' \
  -d '{"limit":100,"offset":0,"with":["participants"]}'
# Returns chat list with GUIDs, participants, identifiers
```

## Get Chat Messages

```bash
# Replace <GUID> with URL-encoded chat GUID (e.g. any%3B-%3Buser%40me.com)
curl -s 'http://<SERVER_URL>/api/v1/chat/<GUID>/message?password=<PASSWORD>&limit=10'
# Most useful fields: text, isFromMe, dateCreated, handle.address
```

## Create New Chat

```bash
curl -s -X POST 'http://<SERVER_URL>/api/v1/chat/new?password=<PASSWORD>' \
  -H 'Content-Type: application/json' \
  -d '{"addresses":["+861234567890"],"message":"Hello","tempGuid":"temp-<TIMESTAMP>"}'
```

## Send Message

```bash
# Field name is "message" not "text"
curl -s -X POST 'http://<SERVER_URL>/api/v1/message/text?password=<PASSWORD>' \
  -H 'Content-Type: application/json' \
  -d '{"chatGuid":"any;-;user@me.com","message":"Hello","tempGuid":"temp-<TIMESTAMP>"}'
```

Note: the `chatGuid` format `any;-;user@me.com` uses the `any` service type which may cause osascript failures in Messages.app. If timing out, try creating a new chat first via `/api/v1/chat/new`.

## Webhook Management

```bash
# List registered webhooks
curl -s 'http://<SERVER_URL>/api/v1/webhook?password=<PASSWORD>'

# Delete a webhook by ID
curl -s -X DELETE 'http://<SERVER_URL>/api/v1/webhook/<ID>?password=<PASSWORD>'
```

## Notes

- `chat/query` with `"with":["participants"]` is the most reliable way to find chat GUIDs
- Chat GUID format: `any;-;<address>` (e.g. `any;-;user@me.com`)
- `isFromMe=true` means the message was sent FROM this Mac (not received)
- `dateCreated` is Unix epoch in milliseconds
- The Hermes gateway's webhook listener runs on `http://127.0.0.1:8645/bluebubbles-webhook`
