# TODO

Carried over from issue #1 of the previous repository ("Image Feedback UI & Functionality Roadmap", opened 25 May 2025), then extended with the open work on the catalogue and the image pipeline.

## Image feedback (from issue #1)

The old viewer was a Picbreeder-style rater for a 4,999-image set, with ratings and comments stored in Supabase. The new site is static and has no backend, so most feedback items are not planned. Status against the new `index.html`:

| Item | Status |
|---|---|
| Store filenames exactly as written (`ComfyUI_00003_.png`, not corrupted names) | Done by design. The site reads exact paths from `index.jsonl` and no longer stores names by hand. |
