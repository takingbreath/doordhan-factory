# silver01 (E14): a chart explainer on real TradingView screens

Template for a reel where a real chart is the hero and Pandey (or another anchor) talks around it.
Copy this folder to work/<slug>/, change the slug and the numbers, and run `bash finish.sh`.

- **tv/plate_*.png:** native TradingView captures of the user's own layout (the saved "Claude" layout, MCX:SILVER1! weekly),
  with the BUY/SELL box and the volume row painted out. WIDE is the whole picture; ZOOM is TradingView's own zoom on a section.
  gfx.py's `View(...)` holds the calibration (price to pixel); check it against the candle bodies before trusting it.
- **gfx.py:** draws one chart card per frame: the plate on a white page, then the marks (trendline, support, rings, arrows, tags)
  on the times in `T` and `LIFE`. Marks fade after their step; only the lines that carry the argument stay.
- **build.py:** the edit: a split-screen opening (B-roll above, anchor below), the chart windows, a cat shot, the anchor's
  other lines, the end card. It writes chart_windows.json.
- **make_final.sh:** two passes. The old-TV look runs on the non-chart parts; the chart runs clean (look none); an ffmpeg
  `overlay=enable='between(...)'` puts the clean chart over the looked edit.
- **qc_repairs.json / qc_manifest.json:** the gate's lip-sync shifts and the manifest (prefinish file, rebuild command).
