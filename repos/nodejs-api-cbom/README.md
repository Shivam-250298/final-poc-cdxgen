# Node.js CBOM POC

Small Express REST API with five cryptographic examples, no database.

| Endpoint | Algorithm |
|---|---|
| POST /hash | SHA-256 |
| POST /password | PBKDF2-HMAC-SHA256 |
| POST /encrypt and /decrypt | AES-256-GCM |
| POST /sign | RSA-2048 and SHA-256 |
| POST /hmac | HMAC-SHA256 |

## Run
Node.js 20+ required.

```bash
npm install
npm test
npm start
```

## Examples

```bash
curl http://localhost:3000/health
curl -X POST localhost:3000/hash -H 'Content-Type: application/json' -d '{"text":"hello"}'
curl -X POST localhost:3000/password -H 'Content-Type: application/json' -d '{"password":"demo"}'
curl -X POST localhost:3000/encrypt -H 'Content-Type: application/json' -d '{"text":"employee"}'
curl -X POST localhost:3000/sign -H 'Content-Type: application/json' -d '{"text":"hello"}'
curl -X POST localhost:3000/hmac -H 'Content-Type: application/json' -d '{"text":"hello","secret":"demo"}'
```

Use encryption response fields as JSON input for POST /decrypt.

## CBOM
Check `cbom --help` for your installed cdxgen version. If supported, run `cbom -o cbom.json .` and inspect actual cryptographic-asset components. Source-level detection is not guaranteed.

**POC only.** The encryption key is returned in the response to simplify testing. Do not deploy publicly or send sensitive data.
