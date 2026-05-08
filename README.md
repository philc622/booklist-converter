# CSV Conversion Mapping

This project provides a Python script to convert CSV files from a source format to a target format (similar to Goodreads export).

## Column Mapping

The following table describes how each column in the target format is derived from the source format.

| Target Column | Source Column / Logic |
| :--- | :--- |
| **Book Id** | `Reading List ID` |
| **Title** | `Title` + `: ` + `Subtitle` (if `Subtitle` exists) |
| **Author** | Primary author from `Authors`, reformatted to "First Last" |
| **Author l-f** | Primary author from `Authors`, kept as "Last, First" |
| **Additional Authors** | Remaining authors from `Authors` |
| **ISBN** | N/A (or derived if possible, but currently skipped or left empty) |
| **ISBN13** | `="` + `ISBN-13` + `"` (spreadsheet format to preserve leading zeros) |
| **My Rating** | `Rating` (defaults to 0 if empty) |
| **Publisher** | `Publisher` |
| **Binding** | N/A (left empty) |
| **Number of Pages** | `Page Count` |
| **Year Published** | Year extracted from `Publication Date` |
| **Original Publication Year** | N/A (left empty) |
| **Date Read** | `Finished Reading` (reformatted to `YYYY/MM/DD`) |
| **Date Added** | `Started Reading` (reformatted to `YYYY/MM/DD`) |
| **Bookshelves** | Derived from `Exclusive Shelf` or `Lists` |
| **Bookshelves with positions** | N/A (left empty) |
| **Exclusive Shelf** | `read` if finished, `currently-reading` if started, `unfinished` if DNF, else `to-read` |
| **My Review** | `Notes` (or left empty if no notes) |
| **Spoiler** | N/A (left empty) |
| **Private Notes** | N/A (left empty) |
| **Read Count** | 1 if `Finished Reading` is set, else 0 |
| **Owned Copies** | 0 |

## Transformation Details

- **Authors**: The source `Authors` column often contains multiple authors separated by semicolons (e.g., `Kleppmann, Martin; Riccomini, Chris`). The first one is treated as the primary author.
- **Dates**: Dates are converted from `YYYY-MM-DD` to `YYYY/MM/DD`.
- **ISBN**: ISBNs are wrapped in `=""...""` to ensure they are treated as strings in spreadsheet software.
