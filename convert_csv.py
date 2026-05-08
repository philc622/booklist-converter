import csv
import re
from datetime import datetime

def reformat_author(author_str):
    """
    Converts "Last, First" to "First Last" and returns both formats.
    If no comma is present, assumes "First Last".
    """
    author_str = author_str.strip()
    if not author_str:
        return "", ""

    if ',' in author_str:
        parts = author_str.split(',', 1)
        last = parts[0].strip()
        first = parts[1].strip()
        return f"{first} {last}", f"{last}, {first}"
    else:
        # Assume "First Last"
        parts = author_str.rsplit(' ', 1)
        if len(parts) == 2:
            first = parts[0].strip()
            last = parts[1].strip()
            return author_str, f"{last}, {first}"
        else:
            return author_str, author_str

def convert_date(date_str):
    """
    Converts YYYY-MM-DD to YYYY/MM/DD.
    """
    if not date_str:
        return ""
    try:
        # source format is YYYY-MM-DD
        dt = datetime.strptime(date_str, '%Y-%m-%d')
        return dt.strftime('%Y/%m/%d')
    except ValueError:
        return date_str

def main():
    source_file = 'source_format.csv'
    target_file = 'converted_output.csv'

    target_columns = [
        'Book Id', 'Title', 'Author', 'Author l-f', 'Additional Authors',
        'ISBN', 'ISBN13', 'My Rating', 'Publisher', 'Binding',
        'Number of Pages', 'Year Published', 'Original Publication Year',
        'Date Read', 'Date Added', 'Bookshelves', 'Bookshelves with positions',
        'Exclusive Shelf', 'My Review', 'Spoiler', 'Private Notes',
        'Read Count', 'Owned Copies'
    ]

    try:
        with open(source_file, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)

            with open(target_file, mode='w', encoding='utf-8', newline='') as out_f:
                writer = csv.DictWriter(out_f, fieldnames=target_columns)
                writer.writeheader()

                for row in reader:
                    # Authors processing
                    authors_raw = row.get('Authors', '')
                    # Split by semicolon
                    author_list = [a.strip() for a in authors_raw.split(';') if a.strip()]

                    primary_author = author_list[0] if author_list else ""
                    author_fl, author_lf = reformat_author(primary_author)

                    additional_authors = []
                    for a in author_list[1:]:
                        fl, _ = reformat_author(a)
                        additional_authors.append(fl)

                    # Title and Subtitle concatenation
                    title = row.get('Title', '')
                    subtitle = row.get('Subtitle', '')
                    if subtitle:
                        full_title = f"{title}: {subtitle}"
                    else:
                        full_title = title

                    # ISBN13 formatting for spreadsheets
                    isbn13_raw = row.get('ISBN-13', '')
                    isbn13 = f'="{isbn13_raw}"' if isbn13_raw else ""

                    # Date formatting
                    finished_date = row.get('Finished Reading', '')
                    started_date = row.get('Started Reading', '')

                    date_read = convert_date(finished_date)
                    if not started_date and finished_date:
                        date_added = date_read
                    else:
                        date_added = convert_date(started_date)

                    # Exclusive Shelf and Bookshelves logic
                    dnf = row.get('Did Not Finish', '').upper()

                    exclusive_shelf = "to-read"
                    bookshelves = ""

                    if dnf in ['Y', 'YES']:
                        exclusive_shelf = "read"
                        bookshelves = "unfinished"
                    elif finished_date:
                        exclusive_shelf = "read"
                        bookshelves = "read"
                    elif started_date:
                        exclusive_shelf = "currently-reading"
                        bookshelves = "currently-reading"
                    else:
                        exclusive_shelf = "to-read"
                        bookshelves = "to-read"

                    # Year Published extraction
                    pub_date = row.get('Publication Date', '')
                    year_published = ""
                    if pub_date:
                        match = re.search(r'\d{4}', pub_date)
                        if match:
                            year_published = match.group(0)

                    # Read Count
                    read_count = "1" if (finished_date or dnf in ['Y', 'YES']) else "0"

                    target_row = {
                        'Book Id': row.get('Reading List ID', ''),
                        'Title': full_title,
                        'Author': author_fl,
                        'Author l-f': author_lf,
                        'Additional Authors': ", ".join(additional_authors),
                        'ISBN': "", # Not provided in source as separate from ISBN13
                        'ISBN13': isbn13,
                        'My Rating': row.get('Rating', '0') if row.get('Rating') else '0',
                        'Publisher': row.get('Publisher', ''),
                        'Binding': "", # Not available in source
                        'Number of Pages': row.get('Page Count', ''),
                        'Year Published': year_published,
                        'Original Publication Year': "",
                        'Date Read': date_read,
                        'Date Added': date_added,
                        'Bookshelves': bookshelves,
                        'Bookshelves with positions': f"{bookshelves} (#1)" if bookshelves else "",
                        'Exclusive Shelf': exclusive_shelf,
                        'My Review': row.get('Notes', ''),
                        'Spoiler': "",
                        'Private Notes': "",
                        'Read Count': read_count,
                        'Owned Copies': "0"
                    }
                    writer.writerow(target_row)
        print(f"Successfully converted {source_file} to {target_file}")
    except FileNotFoundError:
        print(f"Error: {source_file} not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
