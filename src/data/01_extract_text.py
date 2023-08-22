import argparse

from models.Extractor import *
from utils import clear_files, timeit


@timeit
def run_extractors(read_path, save_path, verbose):
    """
    Runs all extractors.
    
    :param read_path: The path to read the data from.
    :type read_path: str
    :param save_path: The path to save the extracted data to.
    :type save_path: str
    :param verbose: Whether or not to print progress to the console.
    :type verbose: bool

    :return: None
    :rtype: None
    """
    extractors = [
        FullTextExtractor(read_path, save_path, verbose=verbose),
        CleanedTextExtractor(read_path, save_path, verbose=verbose)
    ]

    for extractor in extractors:
        print()
        print("="*50)
        print(f'=== Extracting text with {extractor.__class__.__name__}')
        print("="*50)

        extractor.run()

def main():
    parser = argparse.ArgumentParser(description='Extracts text from html files.')
    parser.add_argument('-r', '--read_path', type=str, default='../../data/raw', help='The path to read the html files from.')
    parser.add_argument('-s', '--save_path', type=str, default='../../data/clean', help='The path to save the extracted text to.')
    parser.add_argument('-v', '--verbose', action='store_true', help='Whether or not to print progress to the console.')
    parser.add_argument('-c', '--clear', action='store_true', help='Whether or not to clear the save_path before running.')
    args = parser.parse_args()

    if args.clear: clear_files(args.save_path)

    run_extractors(args.read_path, args.save_path, args.verbose)

if __name__ == '__main__':
    main()