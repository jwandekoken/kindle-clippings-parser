import os
import unicodedata
import re


def read_clippings(filename):
    """
    Reads clippings from a large text file separated by "==========".

    Args:
        filename (str): The path to the text file.

    Returns:
        list: A list of clippings (as strings).
    """

    clippings = []
    current_clipping = []

    with open(filename, "r") as file:
        for line in file:
            if line.strip() == "==========":
                # Separator found, store the current clipping (if not empty)
                if current_clipping:
                    clippings.append("".join(current_clipping))
                    current_clipping = []  # Reset for the next clipping
            else:
                current_clipping.append(line)

    # Store the last clipping (if any)
    if current_clipping:
        clippings.append("".join(current_clipping))

    return clippings


def separate_clippings_by_title(clippings):
    """
    Separates a list of clippings into a dictionary based on book titles.

    Args:
        clippings (list): A list of strings, where each string is a clipping.

    Returns:
        dict: A dictionary where keys are book titles and values are lists of clippings for that book.
    """

    book_dict = {}
    current_book = None

    for clipping in clippings:
        # Extract the title from the first line of the clipping
        title = clipping.splitlines()[0].strip()

        # If the title is different from the current book, start a new list
        if title != current_book:
            current_book = title
            book_dict[current_book] = []

        # Add the clipping to the list for the current book
        book_dict[current_book].append(clipping)

    return book_dict


def clean_title(title):
    """Cleans a title string to make it suitable for filenames."""

    normalized_title = (
        unicodedata.normalize("NFKD", title).encode("ASCII", "ignore").decode()
    )

    safe_title = normalized_title.replace("/", "-").replace(
        ":", "_"
    )  # ... add more replacements

    safe_title = re.sub(r"[^\w\s-]", "", title)

    return safe_title


def save_clippings_to_md_files(book_dict, output_dir="clippings"):
    """
    Saves clippings from a dictionary to individual Markdown (.md) files.

    Args:
        book_dict (dict): A dictionary where keys are book titles and values are lists of clippings.
        output_dir (str, optional): The directory to save the Markdown files. Defaults to "clippings".
    """

    os.makedirs(
        output_dir, exist_ok=True
    )  # Create the output directory if it doesn't exist

    for title, clippings in book_dict.items():
        filename = clean_title(title) + ".md"  # Use the cleaned title
        filepath = os.path.join(output_dir, filename)

        # Check if the file exists
        if os.path.exists(filepath):
            # Append new clippings to an existing file
            mode = "a"  # Append mode
        else:
            # Create a new file
            mode = "w"  # Write mode

        with open(filepath, mode, encoding="utf-8") as file:
            for clipping in clippings:
                file.write("\n")
                file.write(clipping)
                file.write("\n---\n")  # Add the separator


if __name__ == "__main__":
    clippings = read_clippings("My Clippings.txt")
    book_dict = separate_clippings_by_title(clippings)
    save_clippings_to_md_files(book_dict)
