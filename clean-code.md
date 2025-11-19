# Clean Code TaggerScript

## Table of Contents

1. [Introduction](#introduction)
2. [Variables](#variables)
3. [Functions](#functions)
4. [Script Structure](#script-structure)
5. [Naming Conventions](#naming-conventions)
6. [Comments](#comments)
7. [Error Handling](#error-handling)
8. [Performance](#performance)
9. [Testing](#testing)

## Introduction

TaggerScript principles adapted from Robert C. Martin's *Clean Code* for MusicBrainz Picard scripting. This guide helps you write readable, maintainable, and efficient scripts for file naming and tagging operations.

TaggerScript is used in two contexts:
- **File naming scripts**: Control how files are named and organized
- **Tagging scripts**: Manipulate metadata tags

Not every principle must be strictly followed, but they represent best practices developed through collective experience.

## **Variables**

### Use meaningful and descriptive variable names

**Bad:**

```taggerscript
$set(a,%albumartist%)
$set(t,%title%)
$set(d,%date%)
```

**Good:**

```taggerscript
$set(main_artist,%albumartist%)
$set(track_title,%title%)
$set(release_year,%date%)
```

**[⬆ back to top](#table-of-contents)**

### Use consistent vocabulary for the same type of data

**Bad:**

```taggerscript
$set(performer_name,%artist%)
$set(artist_data,%albumartist%)
$set(musician_info,%composer%)
```

**Good:**

```taggerscript
$set(track_artist,%artist%)
$set(album_artist,%albumartist%)
$set(composer_artist,%composer%)
```

**[⬆ back to top](#table-of-contents)**

### Avoid mental mapping with single-letter variables

Variables in TaggerScript should be explicit about their content.

**Bad:**

```taggerscript
$set(a,%artist%)
$set(t,%title%)
$set(n,%tracknumber%)
```

**Good:**

```taggerscript
$set(artist_name,%artist%)
$set(song_title,%title%)
$set(track_number,%tracknumber%)
```

**[⬆ back to top](#table-of-contents)**

### Don't add unneeded context

If your variable naming scheme already indicates the domain, don't repeat it.

**Bad:**

```taggerscript
$set(music_track_artist,%artist%)
$set(music_track_title,%title%)
$set(music_track_album,%album%)
```

**Good:**

```taggerscript
$set(artist,%artist%)
$set(title,%title%)
$set(album,%album%)
```

**[⬆ back to top](#table-of-contents)**

## **Functions**

### Functions should do one thing

Break complex scripts into logical sections using intermediate variables.

**Bad:**

```taggerscript
$set(filename,$replace($replace($replace($lower(%album%),.,-),/,-),\,-) - $replace($replace($num(%tracknumber%,2),.,-),/,-) - $replace($replace(%title%,.,-),/,-))
```

**Good:**

```taggerscript
$set(_clean_album,$replace($replace($lower(%album%),.,-),/,-))
$set(_clean_album,$replace(%_clean_album%,\,-))
$set(_track_num,$num(%tracknumber%,2))
$set(_clean_title,$replace($replace(%title%,.,-),/,-))
$set(filename,%_clean_album% - %_track_num% - %_clean_title%)
```

**[⬆ back to top](#table-of-contents)**

### Use explanatory intermediate variables

Rather than nesting multiple function calls, use intermediate variables to make logic clear.

**Bad:**

```taggerscript
$if($and($gt($len(%artist%),0),$gt($len(%album%),0)),$set(valid,1),$set(valid,0))
```

**Good:**

```taggerscript
$set(_has_artist,$gt($len(%artist%),0))
$set(_has_album,$gt($len(%album%),0))
$set(_is_valid,$and(%_has_artist%,%_has_album%))
$if(%_is_valid%,$set(valid,1),$set(valid,0))
```

**[⬆ back to top](#table-of-contents)**

### Avoid deeply nested conditionals

Use early returns (setting final values early) or intermediate boolean variables.

**Bad:**

```taggerscript
$if($gt($len(%album%),0),
    $if($eq(%albumartist%,Various Artists),
        $if($gt($len(%artist%),0),
            $set(folder,%album%/%artist%),
            $set(folder,%album%/Unknown)
        ),
        $set(folder,%albumartist%/%album%)
    ),
    $set(folder,Unknown)
)
```

**Good:**

```taggerscript
$set(_has_album,$gt($len(%album%),0))
$set(_is_various,$eq(%albumartist%,Various Artists))
$set(_has_artist,$gt($len(%artist%),0))

$if($not(%_has_album%),
    $set(folder,Unknown),
    $if(%_is_various%,
        $if(%_has_artist%,
            $set(folder,%album%/%artist%),
            $set(folder,%album%/Unknown)
        ),
        $set(folder,%albumartist%/%album%)
    )
)
```

**[⬆ back to top](#table-of-contents)**

### Encapsulate complex conditionals

Give meaningful names to complex boolean logic.

**Bad:**

```taggerscript
$if($and($gt($len(%date%),3),$eq($left(%date%,2),19)),$set(century,19th),$set(century,20th))
```

**Good:**

```taggerscript
$set(_is_19th_century,$and($gt($len(%date%),3),$eq($left(%date%,2),19)))
$if(%_is_19th_century%,$set(century,19th),$set(century,20th))
```

**[⬆ back to top](#table-of-contents)**

### Avoid negative conditionals

Positive logic is easier to understand.

**Bad:**

```taggerscript
$set(_not_empty,$not($eq($len(%artist%),0)))
$if(%_not_empty%,$set(has_artist,yes))
```

**Good:**

```taggerscript
$set(_is_empty,$eq($len(%artist%),0))
$if($not(%_is_empty%),$set(has_artist,yes))
```

Or better:

```taggerscript
$set(_has_artist,$gt($len(%artist%),0))
$if(%_has_artist%,$set(has_artist,yes))
```

**[⬆ back to top](#table-of-contents)**

### Use appropriate functions for the task

Choose the right function for the operation you need.

**Bad:**

Using complex string manipulation when simpler functions exist:

```taggerscript
$set(year,$substr(%date%,0,4))
```

**Good:**

```taggerscript
$set(year,$left(%date%,4))
```

**[⬆ back to top](#table-of-contents)**

## **Script Structure**

### Organize scripts logically

Group related operations together and order them sensibly.

**Bad:**

```taggerscript
$set(filename,%title%)
$set(album_clean,$lower(%album%))
$set(filename,%artist% - %filename%)
$set(artist_clean,$lower(%artist%))
$set(filename,%filename% - %tracknumber%)
```

**Good:**

```taggerscript
// Clean and normalize artist name
$set(artist_clean,$lower(%artist%))

// Clean and normalize album name
$set(album_clean,$lower(%album%))

// Build filename from components
$set(filename,%artist% - %title% - %tracknumber%)
```

**[⬆ back to top](#table-of-contents)**

### Separate concerns

Keep file naming separate from tag manipulation when possible.

**Bad:**

```taggerscript
$set(artist,$upper(%artist%))
$set(filename,%artist% - %title%)
$set(album,$upper(%album%))
```

**Good:**

```taggerscript
// Tag manipulation
$set(artist,$upper(%artist%))
$set(album,$upper(%album%))

// File naming
$set(filename,%artist% - %title%)
```

**[⬆ back to top](#table-of-contents)**

### Use consistent patterns

Establish patterns for common operations and use them consistently.

**Bad:**

```taggerscript
$set(clean_artist,$replace(%artist%,/,-))
$set(safe_album,$replace($replace(%album%,/,-),\,-))
$set(title_clean,$replace(%title%,/,-))
```

**Good:**

```taggerscript
// Define a consistent cleaning pattern
$set(_clean_artist,$replace($replace(%artist%,/,-),\,-))
$set(_clean_album,$replace($replace(%album%,/,-),\,-))
$set(_clean_title,$replace($replace(%title%,/,-),\,-))
```

**[⬆ back to top](#table-of-contents)**

## **Naming Conventions**

### Use underscore prefix for temporary variables

Distinguish working variables from final tag values.

**Bad:**

```taggerscript
$set(temp,%artist%)
$set(working_value,$lower(%temp%))
$set(artist,%working_value%)
```

**Good:**

```taggerscript
$set(_temp,%artist%)
$set(_working_value,$lower(%_temp%))
$set(artist,%_working_value%)
```

**[⬆ back to top](#table-of-contents)**

### Use descriptive names for boolean flags

Make boolean variable names clearly indicate what they test.

**Bad:**

```taggerscript
$set(flag,$gt($len(%artist%),0))
$if(%flag%,$set(result,yes))
```

**Good:**

```taggerscript
$set(_has_artist,$gt($len(%artist%),0))
$if(%_has_artist%,$set(result,yes))
```

**[⬆ back to top](#table-of-contents)**

### Use consistent capitalization

Choose either snake_case or camelCase and stick with it.

**Bad:**

```taggerscript
$set(trackNumber,%tracknumber%)
$set(album_name,%album%)
$set(ArtistName,%artist%)
```

**Good (snake_case):**

```taggerscript
$set(track_number,%tracknumber%)
$set(album_name,%album%)
$set(artist_name,%artist%)
```

**[⬆ back to top](#table-of-contents)**

## **Comments**

### Only comment complex business logic

TaggerScript doesn't have native comments, but you can document your scripts externally or use descriptive variable names.

**Bad:**

External documentation:
```
// Set a to artist
// Set t to title
// Set n to track number
```

Script:
```taggerscript
$set(a,%artist%)
$set(t,%title%)
$set(n,%tracknumber%)
```

**Good:**

External documentation:
```
// Normalize artist, title, and track number for filename
// Format: Artist - Title - ##
```

Script with self-documenting variable names:
```taggerscript
$set(_normalized_artist,$replace(%artist%,/,-))
$set(_normalized_title,$replace(%title%,/,-))
$set(_padded_track,$num(%tracknumber%,2))
$set(filename,%_normalized_artist% - %_normalized_title% - %_padded_track%)
```

**[⬆ back to top](#table-of-contents)**

### Document complex regex or replace patterns

Explain non-obvious character replacements.

**Bad:**

```taggerscript
$set(safe,$replace($replace($replace(%title%,:,),.,-),/,-))
```

**Good:**

External documentation:
```
// Remove colons, replace dots with dashes, replace slashes with dashes
// This ensures Windows-safe filenames
```

```taggerscript
$set(_no_colons,$replace(%title%,:,))
$set(_safe_dots,$replace(%_no_colons%,.,-))
$set(_safe_slashes,$replace(%_safe_dots%,/,-))
$set(safe,%_safe_slashes%)
```

**[⬆ back to top](#table-of-contents)**

## **Error Handling**

### Provide fallback values

Always handle cases where expected data might be missing.

**Bad:**

```taggerscript
$set(folder,%albumartist%/%album%)
```

**Good:**

```taggerscript
$set(_artist,$if($gt($len(%albumartist%),0),%albumartist%,Unknown Artist))
$set(_album,$if($gt($len(%album%),0),%album%,Unknown Album))
$set(folder,%_artist%/%_album%)
```

**[⬆ back to top](#table-of-contents)**

### Validate data before use

Check data meets expectations before processing.

**Bad:**

```taggerscript
$set(year,$left(%date%,4))
```

**Good:**

```taggerscript
$set(_has_date,$gt($len(%date%),3))
$set(year,$if(%_has_date%,$left(%date%,4),0000))
```

**[⬆ back to top](#table-of-contents)**

### Handle multi-value variables appropriately

Be aware that some variables contain multiple values.

**Bad:**

```taggerscript
$set(artist_name,%artist%)
```

**Good:**

```taggerscript
// Use first artist for primary artist field
$set(primary_artist,$getmulti(%artist%,0))

// Or join all artists with semicolons
$set(all_artists,$join(%artist%, ; ))
```

**[⬆ back to top](#table-of-contents)**

## **Performance**

### Don't repeat expensive operations

Store the result of complex operations in variables.

**Bad:**

```taggerscript
$set(folder,$replace($replace($replace($lower(%album%),:,),.,-),/,-))
$set(filename,$replace($replace($replace($lower(%album%),:,),.,-),/,-) - %title%)
```

**Good:**

```taggerscript
$set(_clean_album,$replace($replace($replace($lower(%album%),:,),.,-),/,-))
$set(folder,%_clean_album%)
$set(filename,%_clean_album% - %title%)
```

**[⬆ back to top](#table-of-contents)**

### Avoid unnecessary string operations

Don't manipulate strings if you don't need to.

**Bad:**

```taggerscript
$set(artist,$lower($upper($lower(%artist%))))
```

**Good:**

```taggerscript
$set(artist,$lower(%artist%))
```

**[⬆ back to top](#table-of-contents)**

### Use appropriate multi-value functions

Use multi-value specific functions when working with multi-value tags.

**Bad:**

```taggerscript
$set(num_artists,$len($join(%artist%,;)))
```

**Good:**

```taggerscript
$set(num_artists,$lenmulti(%artist%))
```

**[⬆ back to top](#table-of-contents)**

## **Testing**

### Test with various data scenarios

**Test cases to consider:**

1. **Complete metadata**: All expected fields populated
2. **Missing data**: Test with missing artist, album, title
3. **Special characters**: Test with Unicode, slashes, colons
4. **Multi-value fields**: Test with multiple artists, genres
5. **Various Artists albums**: Test compilation handling
6. **Edge cases**: Empty strings, very long strings

**Example test scenarios:**

```taggerscript
// Script to test
$set(_has_artist,$gt($len(%artist%),0))
$set(folder,$if(%_has_artist%,%artist%,Unknown))
```

**Test with:**
- Normal case: artist = "The Beatles" → folder = "The Beatles"
- Empty case: artist = "" → folder = "Unknown"
- Multi-value: artist = ["John Lennon", "Paul McCartney"] → folder = "John Lennon; Paul McCartney"

**[⬆ back to top](#table-of-contents)**

### Validate output format

Ensure your scripts produce valid filesystem paths and tag values.

**Checklist:**
- No invalid filename characters (`: * ? " < > |`)
- No leading/trailing spaces
- Reasonable length (under filesystem limits)
- Proper escaping of special characters

```taggerscript
// Good: Comprehensive sanitization
$set(_temp,$replace($replace($replace(%title%,:,-),?,),",-))
$set(_temp,$replace($replace($replace(%_temp%,<,-),>,-),|,-))
$set(_temp,$trim(%_temp%))
$set(safe_title,$if($gt($len(%_temp%),200),$truncate(%_temp%,200),%_temp%))
```

**[⬆ back to top](#table-of-contents)**

---

## Quick Reference

### Common Patterns

**Safely clean a string for filenames:**
```taggerscript
$set(_safe,$replace($replace($replace(%input%,:,),/,-),\,-))
$set(_safe,$trim(%_safe%))
$set(output,$if($gt($len(%_safe%),0),%_safe%,Unknown))
```

**Check if variable has content:**
```taggerscript
$set(_has_value,$gt($len(%variable%),0))
```

**Format track number with leading zeros:**
```taggerscript
$set(track_formatted,$num(%tracknumber%,2))
```

**Handle Various Artists:**
```taggerscript
$set(_is_various,$eq(%albumartist%,Various Artists))
$set(folder_artist,$if(%_is_various%,%artist%,%albumartist%))
```

**First letter for alphabetical folders:**
```taggerscript
$set(first_letter,$upper($firstalphachar(%albumartist%)))
$set(folder,%first_letter%/%albumartist%/%album%)
```

**[⬆ back to top](#table-of-contents)**

---

## Conclusion

Clean TaggerScript follows the same principles as clean code in any language:
- **Clarity over cleverness**
- **Explicit over implicit**
- **Simple over complex**
- **Maintainable over minimal**

Remember that scripts are read more often than they're written. Future you (or other users) will appreciate clear, well-structured scripts.

**[⬆ back to top](#table-of-contents)**
