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

## Adding a New Character

1. Add an entry to the `PACKS` list in `build_packs.py` following the existing pattern
2. Verify source files exist under `~/Downloads/yuanshen-chinese/<Chinese folder>/`
3. Run `python3 build_packs.py` — missing files are reported as warnings, not errors
4. Copy the new pack to `~/.openpeon/packs/` and test with `peon preview`
