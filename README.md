# The World Today — 20 November 2026

[![make.fun · news-image-20261120](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/Azet17/makefun-news-image-20261120/rank.svg)](https://make.fun/bounty/news-image-20261120/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/Azet17/makefun-news-image-20261120/reward.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)

A 1024×1024 newspaper front page that sums up Friday 20 November 2026 in
one image: masthead **THE WORLD TODAY**, the date line, and a 2×3 grid of six
stories from different corners of the day. Every pictogram is drawn in code
with Pillow — no photos, no copied artwork.

## The six stories

1. **Politics — Three leaders, one table.** Trump, Xi and Putin meet in China
   for a first-ever trilateral summit at the APEC meeting in Shenzhen.
   Source: The Times of India.
2. **Justice — UN court: Myanmar committed genocide.** The ICJ rules 9–6 that
   the 2017 crackdown on the Rohingya was genocide — the first time the court
   has found a state responsible. Source: NPR / UN IIMM.
3. **Weather — Cyclone Akvan bears down on Odisha.** 80,000 people evacuated
   as the severe storm nears India's east coast. Source: The Times of India.
4. **Tech — Anthropic's $1.5 trillion debut.** The Claude maker raises a
   record $81bn in the biggest IPO ever and starts trading on the Nasdaq.
   Source: Reuters (via Business Day).
5. **Sport — Nicholls century steadies New Zealand.** An unbeaten 113 lifts
   the hosts to 243 for 5 on day one of the first Test against India in
   Wellington. Source: Jagran Josh.
6. **Markets — Sensex storms past 83,000.** India's benchmark jumps 1.2% to a
   record close at 83,021.75. Source: Reuters.

## How it runs

`draw.py` renders the front page to `entry.png` (Pillow required, only for
the build step). The entrypoint is dependency-free:

```sh
MAKEFUN_OUTPUT_DIR=out python3 main.py
```

`main.py` copies the pre-rendered `entry.png` to `$MAKEFUN_OUTPUT_DIR/entry.png`,
verifies the copy with sha256, and exits 0. It never deletes the output
directory, and two runs write identical bytes.

## License

MIT — see [LICENSE](LICENSE).
