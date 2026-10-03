# TODO

Carried over from issue #1 of the previous repository ("Image Feedback UI & Functionality Roadmap", opened 25 May 2025), then extended with the open work on the catalogue and the image pipeline.

## Image feedback (from issue #1)

The old viewer was a Picbreeder-style rater for a 4,999-image set, with ratings and comments stored in Supabase. The new site is static and has no backend, so most feedback items are not planned. Status against the new `index.html`:

| Item | Status |
|---|---|
| Store filenames exactly as written (`ComfyUI_00003_.png`, not corrupted names) | Done by design. The site reads exact paths from `index.jsonl` and no longer stores names by hand. |
| Log click coordinates on images | Not planned. Needs a backend. |
| Show a marker where an image was clicked | Not planned. Only useful with click logging. |
| Tooltip with existing comments and ratings on hover | Not planned. Needs stored feedback. |
| Heatmap of popular click areas | Not planned. |
| Indicator for images that have comments | Not planned. |
| Paginate in batches of 100 | Done differently. Experiments are browsed by run, the archive by contact sheet (400 images each), and described images by page (10 each). |
