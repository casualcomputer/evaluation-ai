import argparse

from models.WebScraper import *
from utils import timeit


@timeit
def run_scrapers(save_path, verbose, clear_first=False):
    """
    Runs all scrapers.

    :param save_path: The path to save the raw html files to.
    :type save_path: str
    :param verbose: Whether or not to print progress to the console.
    :type verbose: bool
    :param clear_first: If True, clears all files (starting with self.prefix) within self.save_path before scraping.
    :type clear_first: bool

    :return: None
    :rtype: None
    """
    scrapers = [
        HealthCanadaScraper(save_path=save_path, verbose=verbose),
        CanadaRevenueAgencyScraper(save_path=save_path, verbose=verbose),
        NaturalResourcesCanadaScraper(save_path=save_path, verbose=verbose),
        EmploymentSocialDevelopmentCanadaScraper(save_path=save_path, verbose=verbose)
    ]

    for scraper in scrapers:
        print()
        print("="*50)
        print(f'=== Extracting text with {scraper.__class__.__name__}')
        print("="*50)
        
        scraper.run(clear_first=clear_first)


def main():
    parser = argparse.ArgumentParser(description='Scrapes evaluation reports and saves raw html files.')
    parser.add_argument('-s', '--save_path', type=str, default='../../data/raw', help='The path to save the raw html files to.')
    parser.add_argument('-v', '--verbose', action='store_true', help='Whether or not to print progress to the console.')
    parser.add_argument('-c', '--clear', action='store_true', help='Whether or not to clear the save_path before running.')
    args = parser.parse_args()
    
    run_scrapers(args.save_path, args.verbose, args.clear)


if __name__ == '__main__':
    main()