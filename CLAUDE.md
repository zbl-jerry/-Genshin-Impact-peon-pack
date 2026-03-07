# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Project Does

Generates CESP 1.0 format voice packs for 18 Genshin Impact characters, compatible with the `peon-ping` CLI tool. The build script reads Chinese voice files from a local game asset dump and produces structured packs with `openpeon.json` manifests.

## Build & Install

```bash
# Rebuild all 18 packs from source assets
python3 build_packs.py

# Install to peon-ping's local pack directory
cp -r packs/* ~/.openpeon/packs/
```

**Dependencies:** Python 3.10+, `ffmpeg` (for WAV→MP3 conversion of files >1MB)

**Source assets** are expected at `~/Downloads/yuanshen-chinese/<CharacterChinese>/` with battle audio in a `战斗语音 - Battle/` subdirectory.

## Testing a Pack

```bash
peon packs use nahida
peon preview session.start
peon preview --list

# Rotation mode
peon packs rotation add nahida,furina,hutao
peon rotation round-robin
```

## Architecture

### `build_packs.py`
Single-file build script. Key components:

- **`PACKS` list** — All 18 character definitions. Each entry specifies:
  - `folder`: Chinese character name (matches source asset directory)
  - `name`: Romanized pack name (output directory and manifest `name`)
  - `categories`: Dict mapping 8 CESP category names → list of `(stem, label, subdir)` tuples
    - `subdir=None` → file is in the character root directory
    - `subdir="battle"` → file is in `战斗语音 - Battle/` subdirectory

- **`build_pack()`** — Processes one character: copies/converts audio files, writes `openpeon.json`

- **`copy_or_convert()`** — WAV files >1MB are transcoded to MP3 via ffmpeg (`-qscale:a 4`); smaller files are copied as-is

- **`find_audio_file()`** — Resolves a stem name to a `.wav` path in either the root or battle subdirectory

### Output Structure

```
packs/<name>/
  openpeon.json      # CESP manifest
  icon.png           # Pack-level icon (fallback for all sounds)
  icons/             # Optional: per-category or per-sound icons
  sounds/
    vo_<char>_*.wav  # or .mp3 if converted
```

### CESP Categories (all 8 used per pack)

| Category | Semantic |
|---|---|
| `session.start` | Greetings, appearance lines |
| `task.acknowledge` | Battle skill triggers |
| `task.complete` | Chest open, skill success |
| `task.error` | Heavy hit, low HP lines |
| `input.required` | Idle dialogue |
| `resource.limit` | Low HP frustrated lines |
| `user.spam` | Teammate low HP alerts |
| `session.end` | Night greetings, farewells |

## Icon Configuration (CESP §5.5)

peon-ping resolves icons using a priority chain. Higher entries override lower ones:

| Priority | Location | How to set |
|---|---|---|
| 1 (highest) | Per-sound `icon` field | In each sound entry in `openpeon.json` |
| 2 | Per-category `icon` field | On the category object in `openpeon.json` |
| 3 | Manifest-level `icon` field | Top-level field in `openpeon.json` |
| 4 (fallback) | `icon.png` in pack root | File named exactly `icon.png` |

### Per-sound icon (highest granularity)

```json
{
  "categories": {
    "session.start": {
      "sounds": [
        {
          "file": "sounds/vo_nahida_dialog_greetingMorning.wav",
          "label": "早上好",
          "icon": "icons/morning.png"
        }
      ]
    }
  }
}
```

### Per-category icon

```json
{
  "categories": {
    "task.acknowledge": {
      "icon": "icons/battle.png",
      "sounds": [ ... ]
    }
  }
}
```

### Manifest-level icon (in addition to `icon.png` fallback)

```json
{
  "icon": "icon.png",
  ...
}
```

Icon paths are relative to the pack root directory. HTTP/HTTPS URLs are also supported — peon-ping downloads and caches them automatically.

### In `build_packs.py`

The `PACKS` list entries support optional `icon` keys at two levels:

- **Pack-level**: place `icon.png` in the pack root (already done for all characters)
- **Per-category**: add `"icon"` key alongside `"sounds"` in the category dict written to `openpeon.json`
- **Per-sound**: add `"icon"` to individual sound tuples (requires extending the tuple format from `(stem, label, subdir)` to `(stem, label, subdir, icon)`)

## Scraping Icons with Chrome DevTools MCP

Workflow used to batch-download Q版 thumbnails from Google Images and assign one per sound.

### Step 1: Open Google Images in Chrome DevTools MCP

```python
mcp__chrome-devtools__new_page(url=
  "https://www.google.com/search?q=堆糖+原神纳西妲Q版图片&tbm=isch&hl=zh-CN"
)
```

Use search keywords of the form `"堆糖 原神<角色名>Q版图片"` for consistent chibi-style results.

### Step 2: Extract thumbnails as base64 data URIs

```javascript
// Run via mcp__chrome-devtools__evaluate_script
() => {
  const imgs = document.querySelectorAll('img[src^="data:image"]');
  const results = [];
  for (const img of imgs) {
    if (img.naturalWidth >= 80 && img.naturalHeight >= 80) {
      results.push(img.src);
    }
  }
  return results.slice(0, 20);
}
```

**Important:** This returns ~300KB of base64 data. The MCP tool saves it to a temp file instead of returning it inline. Read that file path from the error message.

### Step 3: Decode, validate, and save with Python

```python
import json, base64, os, re

with open(result_file, 'r') as f:
    outer = json.loads(f.read())
text = outer[0]['text']

# Extract JSON array from markdown code fence
m = re.search(r'```json\n(\[.*?\])\n```', text, re.DOTALL)
urls = json.loads(m.group(1))

for i, uri in enumerate(urls[:N]):
    m2 = re.match(r'^data:image/(\w+);base64,(.+)$', uri, re.DOTALL)
    img_bytes = base64.b64decode(m2.group(2))

    # Validate magic bytes
    if img_bytes[:3] == b'\xff\xd8\xff':   ext = 'jpg'   # JPEG
    elif img_bytes[:8] == b'\x89PNG\r\n\x1a\n': ext = 'png'  # PNG
    else: continue  # skip unknown format

    if len(img_bytes) < 1000: continue  # skip corrupt/tiny files

    with open(f"icons/{name}_{i:02d}.{ext}", 'wb') as f:
        f.write(img_bytes)
```

### Step 4: Write icon paths into openpeon.json

```python
icon_idx = 0
for cat_data in manifest['categories'].values():
    for sound in cat_data['sounds']:
        sound['icon'] = f"icons/{name}_{icon_idx:02d}.jpg"
        icon_idx += 1
```

### Key lessons

- Google Images search results embed **full-resolution thumbnails as inline base64** — no HTTP fetching needed
- Filter by `naturalWidth >= 80` to skip Google UI icons
- The MCP tool auto-saves oversized results to a temp file; parse the outer `[{type, text}]` wrapper, then extract the JSON from the markdown code fence inside `text`
- Always validate **magic bytes** (not just file extension) before saving
- 20 thumbnail images = ~220KB total, well within pack size limits

## Adding a New Character

1. Add an entry to the `PACKS` list in `build_packs.py` following the existing pattern
2. Verify source files exist under `~/Downloads/yuanshen-chinese/<Chinese folder>/`
3. Run `python3 build_packs.py` — missing files are reported as warnings, not errors
4. Copy the new pack to `~/.openpeon/packs/` and test with `peon preview`
