## Picard Naming Script

[![Validate TaggerScript](https://github.com/dipodidae/picard-naming-script/actions/workflows/validate.yml/badge.svg)](https://github.com/dipodidae/picard-naming-script/actions/workflows/validate.yml)
[![Lint TaggerScript](https://github.com/dipodidae/picard-naming-script/actions/workflows/lint.yml/badge.svg)](https://github.com/dipodidae/picard-naming-script/actions/workflows/lint.yml)

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
- Album Artist: The Beatles
- Album: Abbey Road
- Date: 1969-09-26
- Track 1: Come Together
- Track 2: Something

**Output:**
```
Beatles, The - 1969 - Abbey Road/01 - Come Together.flac
Beatles, The - 1969 - Abbey Road/02 - Something.flac
```

#### Various Artists Compilation
**Input tags:**
- Album Artist: Various Artists
- Album: Now That's What I Call Music! 85
- Date: 2013
- Track 1: Royals (by Lorde)
- Track 2: Wake Me Up (by Avicii)

**Output:**
```
[Various Artists]/2013 - Now That's What I Call Music! 85/01 - Lorde - Royals.flac
[Various Artists]/2013 - Now That's What I Call Music! 85/02 - Avicii - Wake Me Up.flac
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
- Album Artist: Various Artists
- Album: The Lion King (Original Motion Picture Soundtrack)
- Secondary Type: soundtrack
- Date: 1994
- Track: Circle of Life (by Carmen Twillie & Lebo M.)

**Output:**
```
[Soundtracks]/1994 - The Lion King (Original Motion Picture Soundtrack)/01 - Carmen Twillie & Lebo M. - Circle of Life.flac
```

#### Single
**Input tags:**
- Album Artist: Taylor Swift
- Album: Anti-Hero
- Primary Type: single
- Total Tracks: 1
- Date: 2022
- Track: Anti-Hero

**Output:**
```
Swift, Taylor - 2022 - [~Singles~]/01 - Anti-Hero.flac
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

