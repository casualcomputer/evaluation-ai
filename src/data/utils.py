import os
import re
import time

from colorama import Fore, Style


def clear_files(base_folder, patterns=""):
    """
    Clears all files in the base_folder folder and subfolder, as long as it matches the pattern(s).

    :param base_folder: The base folder to clear. Subfolders are also cleared.
    :type base_folder: str
    :param patterns: The pattern(s) to match.
    :type patterns: str or list of str (or regex)
    
    :return: None
    :rtype: None 
    """

    if isinstance(patterns, str):
        patterns = [patterns]
    for file in get_files(base_folder, patterns):
        os.remove(file)

def get_files(base_folder, pattern=""):
    """
    Gets all files in the base_folder folder and subfolder, as long as it matches the pattern(s).

    :param base_folder: The base folder to clear. Subfolders are also cleared.
    :type base_folder: str
    :param pattern: The pattern(s) to match.
    :type pattern: str or list of str (or regex)
    
    :return: A list of absolute file paths.
    :rtype: list of str
    """

    files = []
    if isinstance(pattern, str):
        pattern = [pattern]
    for file in os.listdir(base_folder):
        file_path = os.path.join(base_folder, file)
        if os.path.isfile(file_path):
            for p in pattern:
                if file.startswith(p):
                    files.append(file_path)
                    break
        elif os.path.isdir(file_path):
            files += get_files(file_path, pattern)

    files = [os.path.abspath(file) for file in files]
    return files


def timeit(method):
    """
    Decorator to measure the execution time of a method.
    Prints the execution time to the console.

    :param method: The method to measure.
    :type method: function

    :return: The wrapped method.
    :rtype: function
    """
    def timed(*args, **kw):
        start_time = time.time()
        result = method(*args, **kw)
        end_time = time.time()
        print(f'{Fore.BLUE}{method.__name__} took {end_time - start_time} seconds{Style.RESET_ALL}')
        return result
    return timed


def clean_filename(filename):
    """
    Removes invalid characters from a filename.

    :param filename: The filename to clean.
    :type filename: str

    :return: The cleaned filename.
    :rtype: str
    """

    # Regular expression to match any invalid characters
    invalid_char_re = re.compile(r'[\\/:*?"<>|]')
    clean_name = re.sub(invalid_char_re, '_', filename)
    return clean_name


def write_to_file(text, file_path, verbose=True):
    """
    Writes text to file. 
    If ensures the directory exists. 
    If the file already exists, it is overwritten.
    If an error occurs but the file has already been created, the file is deleted.

    :param text: The text to write.
    :type text: str
    :param file_path: The path to the file.
    :type file_path: str
    :param verbose: If True, prints error messages.
    :type verbose: bool

    :return: True if successful, False otherwise.
    :rtype: bool
    """

    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    fp = open(file_path, 'w', encoding='utf-8')
    try:
        fp.write(text)
        fp.close()
        return True
    except Exception as e:
        if verbose: print(e)
        fp.close()
        if os.path.exists(file_path):
            os.remove(file_path)
        return False
        

def is_match(text, patterns):
    """
    Checks if any of the patterns is in the text.

    :param text: The text to search in.
    :type text: str
    :param patterns: The patterns to search for.
    :type patterns: list of str

    :return: True if any of the patterns is in the text, False otherwise.
    :rtype: bool
    """
    if text is None:
        return False
    for pattern in patterns:
        if pattern in text:
            return True
    return False