# Taqwa Lantern carousel builder (backup of the Carousels chat workspace, Sun 15 Nov 2026)

Restore to the original paths, then run from there (scripts use absolute paths):
- `tools/carousels/c01/*`  → `/home/claude/c01/` (template `src/tl.py`; C01–C10 v1 builders; verified source JSON)
- `tools/carousels/c11/*`  → `/home/claude/c11/` (picture posts: `src/plates.py`, `src/build_c11.py`, `src/build_c10.py`, `src/captions.py`)
- `payloads/` hold the Buffer payloads and raw-link manifests of the queued posts (C05–C12) as built.

Dependencies (install once):
- `mkdir -p /home/claude/c01/deps && cd /home/claude/c01/deps && npm i @fontsource/amiri @fontsource/amiri-quran @fontsource/marcellus @fontsource/cormorant-garamond @fontsource/noto-serif quran-validator`
  (Quran Arabic comes only from `quran-validator/data/quran-verses.json`, Tanzil Uthmani.)
- Python: playwright (Chromium), pillow, opencv-python-headless, numpy, uharfbuzz, fonttools (`pip install --break-system-packages …`).
- Picture posts also need our Reel masters (frames are cut from them): `G:\My Drive\Taqwa Lantern\Short Form Videos` via the device tools, staged into `/home/claude/tl-media/` as `NN-*.mp4` (the path `plates.py` reads).

Rules and method: project docs `claude/lane-carousels.md` and `claude/carousel-plan.md`.
