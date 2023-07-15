from bs4 import BeautifulSoup
import requests
import os

class WebScraper:
    
    SAVE_PATH = '../../data/raw'

    def __init__(self, base_url, prefix, patterns, p_patterns=None, save_path=SAVE_PATH, verbose=False):
        self.base_url = base_url
        self.prefix = prefix
        self.patterns = patterns
        self.p_patterns = p_patterns
        self.save_path = save_path
        self.verbose = verbose
    
    def run(self):
        self.clear_data()
        self.scrape_evaluations()

    def clear_data(self):
        for file in os.listdir(self.save_path):
            if file.startswith(self.prefix):
                os.remove(os.path.join(self.save_path, file))

    def scrape_evaluations(self):
        urls, names = self.get_evaluation_urls()
        names = [name.replace('/', '-') for name in names]

        success = 0
        texts = []
        for i, url in enumerate(urls):
            print(f'[{str(i+1).zfill(3)}/{len(urls)}] {names[i]}')
            text = self.extract_full_text(url)
            if not text:
                continue
            texts.append(text)
            file_path = f'{self.save_path}/{self.prefix}_{str(i+1).zfill(3)}_{names[i]}.txt'
            self.write_to_file(text, file_path)
            if os.path.exists(file_path):
                success += 1
        file_path = f'{self.save_path}/{self.prefix}_all.txt'
        self.write_to_file('\n'.join(texts), file_path)

        print(f'Saved {success}/{len(urls)} evaluations')

    def get_evaluation_urls(self):
        urls = []
        names = []
        if self.p_patterns is not None:
            p_urls, _ = self.get_urls(self.base_url, self.p_patterns)
            for p_url in p_urls:
                _urls, _names = self.get_urls(p_url, self.patterns)
                urls += _urls
                names += _names
        else:
            urls, names = self.get_urls(self.base_url, self.patterns)
        return urls, names

    def get_urls(self, url, pattern, url_prefix='https://www.canada.ca/'):
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        urls = []
        names = []

        for link in soup.find_all('a'):
            url = link.get('href')
            if self.is_match(url, pattern):
                urls.append(url_prefix + url)
                names.append(link.text)
        return urls, names

    def is_match(self, url, patterns):
        if url is None:
            return False
        for pattern in patterns:
            if pattern in url:
                return True
        return False

    def extract_full_text(self, url):
        try:
            #exctract text from
            page = requests.get(url)
            soup = BeautifulSoup(page.content, 'html.parser')
            content = soup.find('main', class_='container')
            #concatenate all text with \n
            text = content.get_text(separator='\n', strip=True)
            return text
        except Exception as e:
            # print(f'Failed to load "{url}"')
            print(e)
            return False
    
    def write_to_file(self, text, file_path):
        fp = open(file_path, 'w', encoding='utf-8')
        try:
            fp.write(text)
            fp.close()
            return True
        except Exception as e:
            print(e)
            fp.close()
            if os.path.exists(file_path):
                os.remove(file_path)
            return False

class HealthCanadaScraper(WebScraper):
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
    
    def __init__(self, base_url=BASE_URL, prefix=PREFIX, patterns=PATTERNS, save_path=WebScraper.SAVE_PATH):
        super().__init__(base_url, prefix, patterns, save_path=save_path)

class CanadaRevenueAgencyScraper(WebScraper):
    BASE_URL = 'https://www.canada.ca/en/revenue-agency/programs/about-canada-revenue-agency-cra/internal-audit-program-evaluation.html'
    PREFIX = 'cra'
    PATTERNS = ['evaluation']
    P_PATTERNS = ['internal-audit-program-evaluation']
    
    def __init__(self, p_patterns=P_PATTERNS, base_url=BASE_URL, prefix=PREFIX, patterns=PATTERNS, save_path=WebScraper.SAVE_PATH):
        super().__init__(base_url, prefix, patterns, p_patterns=p_patterns, save_path=save_path)

class NaturalResourcesCanadaScraper(WebScraper):
    #REQUIRED
    BASE_URL = 'https://natural-resources.canada.ca/transparency/reporting-and-accountability/plans-and-performance-reports/strategic-evaluation-division/year/782'
    PREFIX = 'nrc'
    PATTERNS = ['evaluation']
    P_PATTERNS = ['/evaluation-reports-', 'strategic-evaluation-division/year/2020']

    def __init__(self, base_url=BASE_URL, prefix=PREFIX, patterns=PATTERNS, p_patterns=P_PATTERNS, save_path=WebScraper.SAVE_PATH):
        super().__init__(base_url, prefix, patterns, p_patterns=p_patterns, save_path=save_path)

    def get_urls(self, url, pattern, url_prefix=''):
        return super().get_urls(url, pattern, url_prefix=url_prefix)

class EmploymentSocialDevelopmentCanadaScraper(WebScraper):
    BASE_URL = 'https://www.canada.ca/en/employment-social-development/corporate/reports/evaluations.html'
    PREFIX = 'esdc'
    PATTERNS = ['evaluations', 'neutral-assessment-evaluation-function', 'labour-market-low-income-seniors']
    
    def __init__(self, base_url=BASE_URL, prefix=PREFIX, patterns=PATTERNS, save_path=WebScraper.SAVE_PATH):
        super().__init__(base_url, prefix, patterns, save_path=save_path)
    
def scrape_health_canada():
    print('Scraping data from Health Canada')
    hc_scraper = HealthCanadaScraper()
    hc_scraper.run()

def scrape_cra():
    print('Scraping data from Canada Revenue Agency')
    cra_scraper = CanadaRevenueAgencyScraper()
    cra_scraper.run()

def scrape_nrc():
    print('Scraping data from Natural Resources Canada')
    nrc_scraper = NaturalResourcesCanadaScraper()
    nrc_scraper.run()

def scrape_esdc():
    print('Scraping data from Employment Social Development Canada')
    esdc_scraper = EmploymentSocialDevelopmentCanadaScraper()
    esdc_scraper.run()

def main():
    scrape_health_canada()
    scrape_cra()
    scrape_nrc()
    scrape_esdc()

if __name__ == '__main__':
    main()