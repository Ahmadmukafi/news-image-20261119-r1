# THE WORLD TODAY — 19 November 2026 in one image

[![news-image-20261119](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119)
[![rank](https://make.fun/badge/news-image-20261119/Ahmadmukafi/news-image-20261119-r1/rank.svg)](https://make.fun/bounty/news-image-20261119)
[![reward](https://make.fun/badge/news-image-20261119/Ahmadmukafi/news-image-20261119-r1/reward.svg)](https://make.fun/bounty/news-image-20261119)

A one-page front page summing up Thursday 19 November 2026, drawn entirely
with Python PIL (no photograph, no AI-generated image): every headline is
real, legible text.

- **Lead — VICE CITY OPENS:** Grand Theft Auto VI launches worldwide after
  a 13-year wait, over a hand-drawn Vice City sunset.
- **SUMMIT:** Trump, Xi and Putin meet in Shenzhen — the first-ever
  trilateral summit, on the APEC margins.
- **GULF:** Iran hits a U.S. base in Kuwait; Bahrain is struck again and
  tankers are hit in Hormuz.
- **WASHINGTON:** Democrats nominate Hakeem Jeffries to lead the House —
  set to be the first African-American Speaker.
- **Also today:** Cyclone Akvan nears India's east coast, Voyager 1
  reaches a light-day from Earth, Nvidia halts H-series chips to China,
  and the EU proposes a €45bn Ukraine loan.

## How it runs

`main.ts` (Node 22) only copies the pre-rendered `entry.png` into
`$MAKEFUN_OUTPUT_DIR` (default `/output`). No network, no subprocess, no
drawing at run time — both grader runs write byte-identical output.
`draw.py` is the script that rendered `entry.png` (run it to reproduce it).

Sources: AP · Reuters · BBC · NDTV.
