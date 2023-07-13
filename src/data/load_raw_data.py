from bs4 import BeautifulSoup
import requests
import os

class WebScraper:
    
    SAVE_PATH = '../../data/raw'

    def __init__(self, base_url, prefix, patterns, save_path=SAVE_PATH, verbose=False):
        self.base_url = base_url
        self.prefix = prefix
        self.patterns = patterns
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
        page = requests.get(self.base_url)
        soup = BeautifulSoup(page.content, 'html.parser')
        urls, names = self.get_evaluation_urls(soup)
        names = [name.replace('/', '-') for name in names]

        success = 0
        texts = []
        for i, url in enumerate(urls):
            print(f'[{str(i+1).zfill(3)}/{len(urls)}] {names[i]}')
            texts.append((text := self.extract_full_text(url)))
            if not text:
                continue
            file_path = f'{self.save_path}/{self.prefix}_{str(i).zfill(3)}_{names[i]}.txt'
            self.write_to_file(text, file_path)
            if os.path.exists(file_path):
                success += 1
        file_path = f'{self.save_path}/{self.prefix}_all.txt'
        self.write_to_file('\n'.join(texts), file_path)

        print(f'Saved {success}/{len(urls)} evaluations')

    def get_evaluation_urls(self, soup):
        urls = []
        names = []
        for link in soup.find_all('a'):
            url = link.get('href')
            if url is not None and (url := self.is_evaluation(url)):
                urls.append(url)
                names.append(link.text)
        return urls, names
    
    def is_evaluation(self, url):
        for pattern in self.patterns:
            if pattern in url:
                return 'https://www.canada.ca/' + url
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
        super().__init__(base_url, prefix, patterns, save_path)

class CanadaRevenueAgencyScraper(WebScraper):

    BASE_URL = 'https://www.canada.ca/en/revenue-agency/programs/about-canada-revenue-agency-cra/internal-audit-program-evaluation.html'
    PREFIX = 'cra'
    PATTERNS = ['internal-audit-program-evaluation']

    def __init__(self, base_url=BASE_URL, prefix=PREFIX, patterns=PATTERNS, save_path=WebScraper.SAVE_PATH):
        super().__init__(base_url, prefix, patterns, save_path)

def main():
    # hc_scraper = HealthCanadaScraper()
    # hc_scraper.run()

    cra_scraper = CanadaRevenueAgencyScraper()
    cra_scraper.run()

if __name__ == '__main__':
    main()