# Services CMS

Run `python manage.py migrate` to install the schema and initial MIA / AES / ADS content. In Django Admin, edit **Services page**, **Partners**, **Services** and **Value pillars**. Order and active flags control the public listing; uploaded logos and a hero image are optional. Text brand marks are shown until verified logos are uploaded. JSON list fields accept values such as `["PLC", "SCADA"]`.

The configured database already has a legacy `services.0001_initial` marker and old PageSection tables. The new schema begins at `0002_alliance_schema`, preserving those tables and avoiding migration-history resets. Fresh databases use the same sequence.

## Photography

All page photographs are managed by this app. Under **Services page → Hero photography**, upload the main photograph and set its alt text, caption and crop position. Under **Services → [service] → Service photography**, do the same for each capability. Both editors show an image preview. Clear an image to remove it; the hero then uses the alliance blueprint and the service uses its text layout. No frontend image URL is hardcoded.

Migration `0005` fills empty image fields using existing MIA training and equipment media when those files exist in the configured storage. It preserves editor-selected photographs. On deployments without those files, upload images in Admin. Images, captions and crop settings are exposed by `/api/services/`; allow up to five minutes for the frontend CMS cache to refresh after edits.

`GET /api/services/` returns hero, partners, services, pillars and contact objects. Media URLs are absolute and support remote storage URLs. Responses include ETags, a 60-second browser cache and a 300-second shared cache. Edits change the ETag once cache freshness expires. A missing page returns an uncached 503.

The Next.js route uses `API_BASE_URL` (server-only) or the existing `NEXT_PUBLIC_API_BASE_URL`, fetching with a five-minute content revalidation interval. The existing root layout remains dynamic, so the route is server-rendered with cached CMS data. Initial content is used on API outages. Initial data lives in `initial_content.json`; preserve this migration seed file. The frontend copy is an outage fallback, not a live CMS sync target.

Corporate inquiries use a clearly labelled WhatsApp handoff to Ashutosh. The website does not persist a lead or assert delivery. Users review and send the message in WhatsApp. Call links include the Indian country code. Change the WhatsApp field with its country code included.

Only enter verified credentials, metrics and commitments. Initial figures represent three brands, five named control technologies, two career pathways, four services and one named contact. Placement outcomes are not guaranteed.

Validation: `python manage.py test services`. A test database is required; tests do not modify the production database.
