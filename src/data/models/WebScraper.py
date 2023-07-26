import os

import requests
from bs4 import BeautifulSoup
from colorama import Fore, Style
from utils import clean_filename, clear_files, is_match, write_to_file


class BaseWebScraper:
    """
    A class for scraping evaluation reports and saving them locally. 
    By default can support 2 levels of nested urls (base -> [eval] OR base -> [eval_url] -> [eval]).

    :cvar SAVE_PATH: The base path to save the scraped data to.
    :type SAVE_PATH: str
    :ivar base_url: The base url to start scraping from.
    :type base_url: str
    :ivar prefix: The prefix to use for the file names.
    :type prefix: str
    :ivar patterns: The patterns to match the evaluation urls.
    :type patterns: list
    :ivar p_patterns: The patterns to match the urls of the pages containing the evaluation urls.
    :type p_patterns: list
    :ivar save_path: The path to save the scraped data to.
    :type save_path: str
    :ivar verbose: If True, prints error messages.
    :type verbose: bool
    """
    
    
    SAVE_PATH = '../../data'


    def __init__(self, base_url, prefix, patterns, p_patterns=None, save_path=SAVE_PATH, verbose=True):
        self.base_url = base_url
        self.prefix = prefix
        self.patterns = patterns
        self.p_patterns = p_patterns
        self.save_path = save_path
        self.verbose = verbose
    

    def run(self, clear_first=False):
        """
        Runs the scraper.

        :param clear_first: If True, clears all files (starting with self.prefix) within self.save_path before scraping.
        :type clear_first: bool

        :return: None
        :rtype: None        
        """
        if clear_first: clear_files(self.save_path, self.prefix)

        urls = self.get_evaluation_urls()
        for i, url in enumerate(urls):
            file_id = str(i+1).zfill(len(str(len(urls))))
            success = self.scrape_full_html(url, file_id)

            if self.verbose:
                color = Fore.GREEN if success else Fore.RED
                print(f'{color}[{file_id}/{len(urls)}]: {url}{Style.RESET_ALL}')


    def get_evaluation_urls(self):
        """
        Gets the urls of the evaluation reports. 
        Check for nested urls if p_patterns is not None.

        :return: The urls of the evaluation reports.
        :rtype: list
        """

        urls = []
        if self.p_patterns is not None:
            p_urls = self.get_urls(self.base_url, self.p_patterns)
            if self.verbose: print(f'Found {len(p_urls)} urls containing evaluation urls\nExtracting evaluation urls...')
            
            for p_url in p_urls:
                _urls = self.get_urls(p_url, self.patterns)
                urls += _urls
        else:
            urls = self.get_urls(self.base_url, self.patterns)

        if self.verbose: print(f'Found {len(urls)} evaluation urls')
        if self.verbose: print(f'{"="*25}\n')

        return urls


    def get_urls(self, url, patterns, url_prefix='https://www.canada.ca/', parser='lxml'):
        """
        Gets the urls from a page that match the given patterns.

        :param url: The url of the page to scrape.
        :type url: str
        :param patterns: The patterns to match the urls.
        :type patterns: list
        :param url_prefix: The prefix to add to the urls.
        :type url_prefix: str
        :param parser: The parser to use for BeautifulSoup.
        :type parser: str

        :return: The urls that match the patterns.
        :rtype: list
        """

        try:
            page = requests.get(url)
        except Exception as e:
            if self.verbose: print(e)
            return []
        
        try:
            soup = BeautifulSoup(page.content, parser)
        except Exception as e:
            print(e)
            soup = BeautifulSoup(page.content, 'html.parser')
            
        if not soup:
            return []
        
        urls = []

        for link in soup.find_all('a'):
            url = link.get('href')
            if is_match(url, patterns):
                urls.append(url_prefix + url)
        return urls


    def scrape_full_html(self, url, file_id):
        """
        Scrapes the full html of the page and saves it to a file.

        :param url: The url of the page to scrape.
        :type url: str
        :param file_id: The id of the file.
        :type file_id: str

        :return: True if successful, False otherwise.
        :rtype: bool
        """
        soup = self.ext_full_html(url)
        if soup:
            file_path = self.file_path('full', file_id, soup.title.string)
            if os.path.isfile(file_path): os.remove(file_path)
            write_to_file(str(soup), file_path)
            return True
        return False


    def file_path(self, file_type, file_id, title, extension='html'):
        """
        Gets the path to save the file to.
        Path format will be: {save_path}/{file_type}/{prefix}_{file_id}_{title}.{extension}
        
        :param file_type: The type of file to save.
        :type file_type: str
        :param file_id: The id of the file.
        :type file_id: str
        :param title: The title of the file.
        :type title: str
        :param extension: The extension of the file.
        :type extension: str

        :return: The path to save the file to.
        :rtype: str
        """
        file_name = f'{self.prefix}_{file_id}_{title}.{extension}'
        file_name = clean_filename(file_name)
        return os.path.join(self.save_path, file_type, file_name)


    def ext_full_html(self, url, parser='lxml'):
        """
        Extracts the full html of the page.

        :param url: The url of the page to scrape.
        :type url: str
        :param parser: The parser to use for BeautifulSoup.
        :type parser: str

        :return: The full html of the page.
        :rtype: BeautifulSoup
        """

        try:
            page = requests.get(url)
        except Exception as e:
            return None

        try:
            #exctract text from
            soup = BeautifulSoup(page.content, parser)
        except Exception as e:
            print(e)
            soup = BeautifulSoup(page.content, 'html.parser')

        return soup
    

class HealthCanadaScraper(BaseWebScraper):
    BASE_URL = 'https://www.canada.ca/en/health-canada/corporate/transparency/corporate-management-reporting/evaluation.html'
    PREFIX = 'hc'
    PATTERNS = [
        'evaluation/results-',
        'evaluation/summary',
        'evaluation-reports/',
        'evaluations/',
        'reporting/summary',
        'reporting/evaluation',
        'publications.gc.ca/'
    ]
    

    def __init__(self, base_url=BASE_URL, prefix=PREFIX, patterns=PATTERNS, save_path=BaseWebScraper.SAVE_PATH, verbose=True):
        super().__init__(base_url, prefix, patterns, save_path=save_path, verbose=verbose)


class CanadaRevenueAgencyScraper(BaseWebScraper):
    BASE_URL = 'https://www.canada.ca/en/revenue-agency/programs/about-canada-revenue-agency-cra/internal-audit-program-evaluation.html'
    PREFIX = 'cra'
    PATTERNS = ['evaluation']
    P_PATTERNS = ['internal-audit-program-evaluation']
    

    def __init__(self, p_patterns=P_PATTERNS, base_url=BASE_URL, prefix=PREFIX, patterns=PATTERNS, save_path=BaseWebScraper.SAVE_PATH, verbose=True):
        super().__init__(base_url, prefix, patterns, p_patterns=p_patterns, save_path=save_path, verbose=verbose)


class NaturalResourcesCanadaScraper(BaseWebScraper):
    BASE_URL = 'https://natural-resources.canada.ca/transparency/reporting-and-accountability/plans-and-performance-reports/strategic-evaluation-division/year/782'
    PREFIX = 'nrc'
    PATTERNS = ['evaluation']
    P_PATTERNS = ['/evaluation-reports-', 'strategic-evaluation-division/year/2020']


    def __init__(self, base_url=BASE_URL, prefix=PREFIX, patterns=PATTERNS, p_patterns=P_PATTERNS, save_path=BaseWebScraper.SAVE_PATH, verbose=True):
        super().__init__(base_url, prefix, patterns, p_patterns=p_patterns, save_path=save_path, verbose=verbose)


    def get_urls(self, url, pattern, url_prefix=''):
        return super().get_urls(url, pattern, url_prefix=url_prefix)

class EmploymentSocialDevelopmentCanadaScraper(BaseWebScraper):
    BASE_URL = 'https://www.canada.ca/en/employment-social-development/corporate/reports/evaluations.html'
    PREFIX = 'esdc'
    PATTERNS = ['evaluations', 'neutral-assessment-evaluation-function', 'labour-market-low-income-seniors']
    
    
    def __init__(self, base_url=BASE_URL, prefix=PREFIX, patterns=PATTERNS, save_path=BaseWebScraper.SAVE_PATH, verbose=True):
        super().__init__(base_url, prefix, patterns, save_path=save_path, verbose=verbose)