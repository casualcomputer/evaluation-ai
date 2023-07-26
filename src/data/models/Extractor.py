import os

from bs4 import BeautifulSoup
from colorama import Fore, Style
from utils import get_files, write_to_file


class Extractor:
    """
    Base class for all extractors.

    :ivar read_path: The path to read the data from.
    :type read_path: str
    :ivar save_path: The path to save the extracted data to.
    :type save_path: str
    :ivar verbose: Whether or not to print progress to the console.
    :type verbose: bool
    """


    def __init__(self, read_path, save_path, verbose=True):
        self.read_path = read_path
        self.save_path = save_path
        self.verbose = verbose


    def run(self):
        """
        Runs the extractor for all files in self.read_path.
        Each extraction is saved to self.save_path.

        :return: None
        :rtype: None
        """


        files = get_files(self.read_path)
        if self.verbose: 
            print(f'Extracting from {len(files)} files...')
            print("="*25)


        for i, file in enumerate(files):
            file_id = str(i+1).zfill(len(str(len(files))))

            text = self.extract(file)
            if not text:
                success = False
            else:
                file_path = self.gen_file_path(file)
                success = write_to_file(text, file_path)

            if self.verbose:
                color = Fore.GREEN if success else Fore.RED
                print(f'{color}[{file_id}/{len(files)}]: {file}{Style.RESET_ALL}')

    
    def extract(self, file_path):
        """
        Extracts the full text from a file.

        :param file_path: The path to the file to extract the text from.
        :type file_path: str

        :return: extracted text from the file
        :rtype: str
        """

        raise NotImplementedError
    
    
    def gen_file_path(self, file_path):
        """
        Generates absolute path for the file.

        :param file_path: The path to the file to generate the name for.
        :type file_path: str

        :return: The generated path.
        :rtype: str
        """

        base = os.path.basename(file_path)
        file_path = os.path.join(self.save_path, f'{base}.txt')
        return file_path


class FullTextExtractor(Extractor):


    SAVE_FOLDER = 'full'

    def __init__(self, read_path, base_save_path, verbose=True):
        save_path = os.path.join(base_save_path, self.SAVE_FOLDER)
        super().__init__(read_path, save_path, verbose=verbose)
    

    def extract(self, file_path):
        with open(file_path, 'r') as f:
            try:
                soup = BeautifulSoup(f.read(), 'lxml')
            except:
                soup = BeautifulSoup(f.read(), 'html.parser')
            
            if not soup:
                return None

            content = soup.find('main', class_='container')
            if not content:
                return None
            
            text = content.get_text(separator='\n', strip=True)

            return text
