# Magic eBook Renamer
# @author Aman Sharma
# @version 10-09-2022
# @credits github@paulocheue (epub-meta) https://github.com/paulocheque/epub-meta
#          stackexchange@sam (epub answer) https://ebooks.stackexchange.com/a/8605

import os
import glob
import epub_meta
from datetime import datetime

# global variables
book_name_TEST = r"[insert a path of epub here to test]"


# Debug method, renames single given eBook
def rename_epub():
    metadata = epub_meta.get_epub_metadata(book_name_TEST, read_cover_image=True, read_toc=True)
    return metadata


# Main method, renames all epub books in directory with their metadata
def rename_folder(dir_name):
    # Create session report
    now = datetime.now()
    dt_string = now.strftime("%d-%m-%Y %H-%M-%S")
    print("date and time =", dt_string)
    dt_string = dir_name + "\\" + dt_string
    report = open(dt_string + ".txt", "x")
    report.write("Renaming Report \n" + dt_string)

    for File in glob.glob(dir_name + "\\*.epub"):
        try:
            report.write("File: " + File + "\n")
            book = epub_meta.get_epub_metadata(File, read_cover_image=True, read_toc=True)
            title = ''.join(book.title) + " by " + ''.join(book.authors)

            checker = dir_name + "\\" + title + ".epub"

            # Make string Windows safe, remove unavailable characters
            char_to_replace = {':': '',
                               '*': '',
                               '<': '',
                               '>': '',
                               '|': '',
                               '/': '',
                               '?': ''}

            # Iterate over all key-value pairs
            for key, value in char_to_replace.items():
                # Replace key character with value character in string
                title = title.replace(key, value)

            # Validate a file too long (Windows path should be less than 256 chars)
            if len(checker) > 255:
                print("Title Bigger than allowed \n")
                book_char_length = len(File) - len(os.path.basename(os.path.normpath(File))) + 4 + len(
                    ''.join(book.authors))
                title_char_allowance = 255 - book_char_length
                title = ''.join(book.title)[:title_char_allowance] + " by " + ''.join(book.authors)

            os.rename(File, dir_name + "\\" + title + ".epub")
        except OSError:
            print("Title Bigger than allowed \n")
            book_char_length = len(File) - len(os.path.basename(os.path.normpath(File))) + 4 + len(
                ''.join(book.authors))

            title_char_allowance = 180 - book_char_length
            # print("DEBUG CHAR ALLOWANCE " + str(title_char_allowance))
            new_title = ''.join(book.title[:title_char_allowance])

            print(" DEBUG NEW TITLE: " + new_title)
            title = new_title + " by " + ''.join(book.authors)

            report.write("File too big error " + File + "\n")
            os.rename(File, dir_name + "\\" + title + ".epub")
        except KeyError:
            report.write("KeyError " + File + "\n")
            continue
        except FileExistsError:
            report.write("FileExistsError " + File + "\n")
            continue


# Main
def main():
    print("EPUB RENAMER\nVersion 1.0")
    directory = input("Enter Directory Name: ")
    rename_folder(directory)


if __name__ == '__main__':
    main()
