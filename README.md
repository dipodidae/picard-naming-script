## Picard Naming Script

Enhanced file naming script for MusicBrainz Picard. Generates clean, consistent paths and filenames based on release metadata (album type, artists, year, labels) with safe cross‑platform sanitization.

### What it does
* Detects album type: Classical, Soundtrack, Single, Other, Standard
* Builds predictable folder structure (handles Various / Unknown Artists)
* Adds featured artists / composers where appropriate
* Trims and pads disc / track numbers
* Sanitizes problematic characters and collapses duplicates

### Requirements
* Picard (current release)
* Additional Artists Variables plugin enabled

### Quick install
1. Open Picard → Options → File Naming
2. Paste contents of `naming.pts`
3. (Optional) Enable a script: `$set(_isClassical,1)` for classical releases

### Key settings (edit at top of script)
```
_minDiscPadLength    # disc number padding minimum
_minTrackPadLength   # track number padding minimum
_maxAlbumTitleLength # album title truncation limit
_maxTrackTitleLength # track title truncation limit
_maxTrackFilenameLength # whole filename limit
```
Flags (set to `1` to enable):
```
_includeReleaseYear _includeDisambiguation _includeLabel
_includeCatalogNumber _groupByExtension _noArtistSort _sortOnFirstName
```

Special folder / placeholder texts are customizable (`_CLASSICAL_FOLDER`, `_UNKNOWN_ARTIST_TEXT`, etc.).

### Examples

#### Standard Album
**Input tags:**
- Album Artist: Bathory
- Album: Bathory
- Date: 1984-10-02
- Track 1: Storm Of Damnation (Intro)
- Track 2: Hades

**Output:**
```
Bathory - 1984 - Bathory/01 - Storm Of Damnation (Intro).flac
Bathory - 1984 - Bathory/02 - Hades.flac
```

#### Various Artists Compilation
**Input tags:**
- Album Artist: Various Artists
- Album: Speed Kills (The Very Best In Speed Metal)
- Date: 1985
- Track 1: Metal Merchants (by Hallows Eve)
- Track 2: A Lesson In Violence (by Exodus)

**Output:**
```
[Various Artists]/1985 - Speed Kills (The Very Best In Speed Metal)/01 - Hallows Eve - Metal Merchants.flac
[Various Artists]/1985 - Speed Kills (The Very Best In Speed Metal)/02 - Exodus - A Lesson In Violence.flac
```

#### Classical Release
**Input tags:**
- Album: Piano Concerto No. 1
- Date: 2020
- Track: Piano Concerto No. 1 in B-flat minor, Op. 23 - I. Allegro non troppo
- Artist: Martha Argerich
- Composer: Pyotr Ilyich Tchaikovsky
- `_isClassical` flag enabled

**Output:**
```
[Classical]/2020 - Piano Concerto No. 1/01 - Piano Concerto No. 1 in B-flat minor, Op. 23 - I. Allegro non troppo [Pyotr Ilyich Tchaikovsky].flac
```

#### Soundtrack
**Input tags:**
- Album Artist: Popol Vuh
- Album: Nosferatu
- Secondary Type: soundtrack
- Date: 1978
- Track 1: Mantra (6:14)
- Track 2: Morning Sun Rays (3:20)

**Output:**
```
[Soundtracks]/1978 - Nosferatu/01 - Popol Vuh - Mantra.flac
[Soundtracks]/1978 - Nosferatu/02 - Popol Vuh - Morning Sun Rays.flac
```

#### Unmatched Files (No MusicBrainz Data)
**Input tags:**
- Artist: Stormqueen
- Album: Battle of Britain [demo]
- Date: 1980
- Track: Battle of Britain

**Output:**
```
Stormqueen - 1980 - Battle of Britain [demo]/01 - Battle of Britain.flac
```

### Attribution
Original by Bob Swift (rdswift). Fork and refactor by dipodidae (2025-11-10).

### License
GPLv3. See `LICENSE`.

### Links
Picard: https://picard.musicbrainz.org/
Plugin: https://github.com/rdswift/picard-plugins
Scripting docs: https://picard-docs.musicbrainz.org/en/appendices/scripting.html

