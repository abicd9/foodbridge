# staff-portal  (reserved)

TODO: the separate staff website goes here (or deploy it anywhere and leave this folder empty).

Option A - served by this API at /staff/: drop the built site in this folder (it needs an index.html).
  The API only mounts /staff when staff-portal/index.html exists, so an empty folder is fine.
  Override the location with STAFF_PORTAL_DIR in backend/.env.

Option B - separate origin (e.g. https://staff.yourdomain.com): host it separately and list its origin in
  STAFF_ORIGINS in backend/.env so the browser may call this API (CORS).

The staff site talks to the same API the member app uses. Already available for it:
  POST /api/admin/login, POST /api/admin/logout
  GET  /api/admin/services | reports | changes | sources | quarantine | duplicates | operations | organisations | providers
  PATCH /api/admin/services/{id}, POST /api/admin/services/{id}/publish
  POST /api/admin/{reports|changes}/{id}/decision, POST /api/admin/import, GET /api/admin/audit
Sign-in: send {"email","password"}; use the returned token as 'Authorization: Bearer <token>'.
