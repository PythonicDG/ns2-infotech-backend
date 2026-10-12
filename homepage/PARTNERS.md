The homepage partners strip appears between Hero Banner and Overview.

For a new deployment, run after setting up the active Company Profile:

```sh
python manage.py migrate
python manage.py seed_partners
```

The initialization command creates AES, MIA and ADS entries, uses the current
Company Profile logo for MIA, and leaves AES/ADS ready for logo uploads.
Running it again preserves all existing admin edits.

In Django admin, open Homepage > Page sections > Trust / Partners Strip:

- Heading: collaborators text, initially "Collaborators: AES & ADS".
- Subheading: partnership tagline.
- Is active: show or hide the whole strip.
- Partners: add any number of names, upload logos, and write optional descriptions.
- Order: lower numbers appear first.
- Is active on a partner: show or hide that entry.

Use PNG, WebP or JPEG logos; transparent PNG/WebP works well. Entries without
logos display their names. The strip hides if it has no active named partners.
The existing homepage API supplies this content without a separate request.
Public API/browser caching may take up to a minute to show admin changes.
