# foodbridge

## Run it
```
./run.sh                      # creates backend/.env from .env.example, installs deps, starts the API
```
- Member app: http://127.0.0.1:8000
- Staff website: not built yet. See `staff-portal/README.md` for where it plugs in.

## Default administrator (works in the member app; the future staff site signs in with it via /api/admin/login)
- Email: `admin@foodbridge.sg`
- Password: `FoodBridge@Admin2026`

Created automatically on first start. Change it in `backend/.env` (`ADMIN_EMAIL`, `ADMIN_PASSWORD`) before going live. In production (`ENVIRONMENT=production`) the server refuses to start with the default password. Note: the admin account is only created if it does not exist yet, so to change an existing database's admin password use `python -m app.manage_admin --email you@x.com --password-stdin`.

## What changed: no email verification
- Creating an account now activates it and signs the person in immediately (`REQUIRE_EMAIL_VERIFICATION=false`).
- Accounts left in the old "pending verification" state activate on their next correct sign-in.
- Sign-in never asks for email verification. Set `REQUIRE_EMAIL_VERIFICATION=true` to bring the old behaviour back.
- "Forgot password" still needs SMTP settings in `.env`, since it has to send an email.

## Where the API keys go
| What | Where |
|---|---|
| Google Maps (browser map) | `frontend/config.js` -> `mapsKey` (and optional `mapId`). Enable *Maps JavaScript API*, restrict to your site. |
| Google Routes (directions) | `backend/.env` -> `GOOGLE_ROUTES_API_KEY` (server only, never in the frontend) |
| OneMap (SG postcode/address search) | `backend/.env` -> `ONEMAP_EMAIL`, `ONEMAP_PASSWORD` |
| Food data API | `backend/.env` -> `FOOD_DATA_API_URL`, `FOOD_DATA_API_KEY`; map its fields in `backend/app/food_data.py` (`FIELD_MAP`) |
| Staff site URL / origin | `frontend/config.js` -> `staffUrl`; `backend/.env` -> `STAFF_ORIGINS` |

## Loading food data
1. Edit `FIELD_MAP` / `TYPE_MAP` in `backend/app/food_data.py` to match your API's JSON.
2. With the server running: `cd backend && python -m app.food_data` (add `--publish` to skip review).
3. Imported records stay PENDING until published (`--publish`, or the staff site once it exists).
Set `DEMO_DATA=false` once real data is in. Run `python -m app.retire_demo` to withdraw the sample listings.

## Production
Use PostgreSQL (`DATABASE_URL`), `ENVIRONMENT=production`, HTTPS, serve `frontend/` via `nginx.conf`, and run `python -m app.scheduler` for backups/expiry.

## Layout
`backend/app` API · `frontend` member web app · `staff-portal` reserved for the staff site · `account-pages` email-link pages · `nginx.conf`

Search the code for `TODO` to find every spot that still needs a key or decision.
