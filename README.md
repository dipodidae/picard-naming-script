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

### Attribution
Original by Bob Swift (rdswift). Fork and refactor by dipodidae (2025-11-10).

### License
GPLv3. See `LICENSE`.

### Links
Picard: https://picard.musicbrainz.org/
Plugin: https://github.com/rdswift/picard-plugins
Scripting docs: https://picard-docs.musicbrainz.org/en/appendices/scripting.html

