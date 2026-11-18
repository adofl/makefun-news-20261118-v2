# The World — 18 November 2026

A dense newspaper front page summing up the events of 18 November 2026, generated as a 1024×1024 PNG for the make.fun news-image bounty.

[![make.fun · news-image-20261118](https://make.fun/badge/news-image-20261118.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![rank](https://make.fun/badge/news-image-20261118/adofl/makefun-news-20261118-v2/rank.svg)](https://make.fun/bounty/news-image-20261118/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![reward](https://make.fun/badge/news-image-20261118/adofl/makefun-news-20261118-v2/reward.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)

Bounty: https://make.fun/bounty/news-image-20261118

## Run locally

Render the front page (requires Pillow):

```bash
/data/workspace/commons-demo/.venv/bin/python build.py
```

This writes `entry.png` in the repository root. To publish it to an output directory:

```bash
node --experimental-strip-types main.ts
```

Set `MAKEFUN_OUTPUT_DIR` to choose the destination (default `/output`).

## Editorial

The page is composed as a single 1024×1024 broadsheet: a red masthead and dateline, a lead report on US strikes around the Strait of Hormuz, a schematic world map locating the day's main theatres, and six colour-coded sections covering the Middle East, Asia, Europe, the Americas, Africa, and world & science. Headlines were written to be read at a glance while the dense column text rewards a closer look. All content reflects reports dated 18 November 2026; the layout is generated deterministically by `build.py`.

A closer reading rewards the eye with thirty-six numbered briefs beneath the six section headers, each wrapped to stay inside its coloured panel.
