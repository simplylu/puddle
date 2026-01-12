## About
Puddle searches and analyzes AI models across Huggingface, CivitAI, and Shakker AI platforms based on keywords. It collects statistics on model usage, downloads, bookmarks, and other metrics to provide insights into model popularity and trends.

Originally created to analyze the landscape of open-source models used for adult content generation.
## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd AI
```

2. Install dependencies using uv:
```bash
uv sync
```

Alternatively, using pip:
```bash
pip install -r requirements.txt
```


## Setup

Before running the script for the first time:

1. Copy `keywords.txt.sample` to `keywords.txt`
2. Copy `.env.sample` to `.env` and add your Huggingface API Key

```bash
cp keywords.txt.sample keywords.txt
# Add the keywords you want to have to keywords.txt
cp .env.sample .env
# Edit .env and add your HUGGINGFACE_API_KEY
```

## Usage

The `puddle.py` script provides a command-line interface to search for AI models across multiple platforms (Huggingface, CivitAI, and Shakker AI), collect statistics, and analyze the results.

### Available Commands

- **`search`** - Search for models using keywords on specified platforms
- **`stats`** - Generate statistics from previously collected search data
- **`merge`** - Combine statistics from all platforms into a single file (Excel, CSV, or JSON)
- **`full`** - Run the complete workflow: search all keywords, generate stats, and merge results
- **`show`** - Display statistics and analytics from the merged data file

### Examples
![](help.png)
```bash
# Search for a specific keyword on all platforms
python puddle.py search --site all --keyword "nature"

# Search all keywords from keywords.txt on CivitAI
python puddle.py search --site civitai --keyword all

# Generate statistics for Huggingface data
python puddle.py stats --site huggingface

# Merge all statistics into a CSV file
python puddle.py merge --output statistics.csv

# Run full workflow and save as Excel
python puddle.py full --output statistics.xlsx

# Show statistics with top 30 keywords and 15 models per category with the option to blur nsfw data
python puddle.py show --input statistics.xlsx --top-keywords 30 --models-per-download 15 --blur
```

## Example Output
```txt
==================================================
Statistics Summary
Keywords: v*g*n*, s*xy, p*rn, br**sts, b**bs, t*ts, sl*t, *ss, *n*l, bdsm, *rg*sm, m*st*rb*t**n, p*ssy, f*ck
Total Models: 1,354
==================================================

Huggingface:
  Total Models: 242
  Downloads: 985,859
  Bookmarks: 267

Civitai:
  Total Models: 871
  Downloads: 12,744,950
  Bookmarks: 283,838
  Thumbs Up: 1,140,708
  Thumbs Down: 1,294
  Tips: 22,989,693

Shakker:
  Total Models: 241
  Downloads: 12,405
  Comments: 247
  Runs: 1,818,037.0
==================================================

Top 20 Models by Downloads Per Hour
==================================================
                                              name      source  downloadCount  hours_since_creation  downloads_per_hour    tag
                                    Pony Realism 🔮     civitai         486792          15719.741509           30.966921   porn
                                          MeinaMix     civitai         499947          25681.510639           19.467196   sexy
✨ JANKU Trained + NoobAI + RouWei Illustrious XL ✨     civitai         145029           7815.383829           18.556862   sexy
                Realism Illustrious By Stable Yogi     civitai         182473           9966.432784           18.308757   sexy
                          iNiverse Mix(SFW & NSFW)     civitai         285858          18382.595928           15.550470   sexy
Hands XL + SD 1.5 + F1D + Pony + Illustrious + zit     civitai         256876          18958.347838           13.549493   sexy
                           pornmasterPro_noobV3VAE huggingface          72847           5594.511557           13.021155   porn
                                     Nova Furry XL     civitai         175789          13987.711838           12.567388   sexy
                              AnyLoRA - Checkpoint     civitai         289549          24599.627048           11.770463   sexy
                                  XXMix_9realistic     civitai         253582          23925.114374           10.598988   sexy
                            Doll Likeness - by EDG     civitai         254650          24042.343580           10.591730   sexy
                                            Photon     civitai         224468          22841.954236            9.827005   sexy
                                  NSFW MASTER FLUX     civitai         115288          12243.710053            9.416100 vagina
                    pornworks-sexy-beauty-v04-sdxl huggingface         107861          11659.203779            9.251146   sexy
                             Hairstyles Collection     civitai         198547          23095.405808            8.596818   sexy
                         STYLES | PONY & ANIMAGINE     civitai         120556          14568.276375            8.275241   sexy
                                 PerfectDeliberate     civitai         200447          24574.599860            8.156674   sexy
                  Analog Madness - Realistic model     civitai         207451          25589.513355            8.106876   sexy
                                         sexyToons huggingface         173132          21608.957946            8.012048   sexy
                            Illustrious Style Pack     civitai          70850           9279.937228            7.634750   sexy
==================================================
Total Downloads per Hour Across All Models: 839.27

Top 20 Most Used Keywords in Model Names
==================================================
p*ny                              121
styl*                             117
sdxl                              109
l*r*                              107
s*xy                               96
*ll*str***s                        76
br**sts                            76
xl                                 73
*n*m*                              60
fl*x                               54
p*rn                               51
g*rl                               44
r**l*st*c                          43
p*rnm*st*r                         43
&                                  38
+                                  38
**                                 38
nsfw                               37
*l                                 37
m*x                                32
==================================================

Total unique keywords: 2733
Total tokens analyzed: 6197
```