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

class CleanedTextExtractor(Extractor):


    SAVE_FOLDER = 'cleaned'

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
            
            text = self.template_text(content, soup)

            return text

    def template_text(self, soup_content, soup_object):
        #Removing in-text references, figures, tables, and page details since presumably interrupts sequential text processing
        #remove <figure> tags since not text convertible, replace with their alt text. 
        figures = soup_content.find_all('img')
        if figures:
            for figure in figures:
                figure.extract()

        #removes <tables>
        tables = soup_content.find_all('table')
        if tables:
            for table in tables:
                table.extract()

        #remove page details
        pagedetails_tag = soup_content.find('div', class_='pagedetails')
        if pagedetails_tag:
            pagedetails_tag.extract()

        #remove in-text references 
        sup_tags = soup_content.find_all('sup')
        if sup_tags:
            for sup_tag in sup_tags:
                sup_tag.extract()

        #remove aside (i.e footnotes/block inserts)
        aside_tags = soup_content.find_all('aside')
        if aside_tags:
            for aside_tag in aside_tags:
                aside_tag.extract()

        text = ""

        #Initially strip section tags so we can insert out own to standardize formatting across pages 
        section = soup_content.find_all('section')
        for section in soup_content.findAll('section'):
            section.replaceWithChildren()

        return self.convert_toc_to_section_to_text(soup_content, soup_object)

    def convert_toc_to_section_to_text(self, soup_content, soup_object):

        #could add feature to filter based on header title
        headers = soup_content.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
        toc_found = False
        toc_list = ""
        text = ""

        for header in headers:
            header_text = header.get_text().strip().lower()
            if header_text == "table of contents" or header_text == "on this page":
                toc_found = True
                break
        if toc_found:
            next_sibling = header.find_next_sibling()

            #TOC list might not be in the same div as the header, move up until you find it
            if not next_sibling: 
                next_sibling = header.parent
                while next_sibling and not next_sibling.find_next_sibling():
                    next_sibling = next_sibling.parent

            while next_sibling:
                if next_sibling.name == 'ul':
                    break
                elif next_sibling.name == 'div': #check if the text is in the container
                    inner_list = next_sibling.find('ul')
                    if inner_list:
                        next_sibling = inner_list
                        break

                next_sibling = next_sibling.find_next_sibling()

            #Extract the table of contents
            if next_sibling:
                toc_items = next_sibling.find_all('li')
                toc_list = [item.get_text().strip().lower().replace(" ", "").replace("\t", "") for item in toc_items]  

            current_section = None
            sections = []

            #Cycle through headers to look for sections to keep
            for heading in headers:
                header_text = heading.get_text().strip().lower().replace(" ", "").replace("\t", "")

                if header_text in toc_list:
                    # Found a header element (h1, h2, h3, ...) from table of contents
                    current_section = soup_object.new_tag('section')
                    #Add a header tag with the text of the header
                    new_header_tag = soup_object.new_tag(heading.name)
                    new_header_tag.string = heading.get_text()

                    #Make the current heading the starting point
                    current_sibling = heading
                    current_section.append(new_header_tag)

                    #Cycle through up to parent tag until the tag has a sibling (hopefully the associated text)
                    while current_sibling and not current_sibling.find_next_sibling():
                        current_sibling = current_sibling.parent 
                    
                    next_sibling_search = current_sibling.find_next_sibling()
                    while next_sibling_search:
                        #Go through same layer of heading until hit the head or a new heading
                        if next_sibling_search.get_text().strip().lower().replace(" ", "").replace("\t", "") in toc_list:
                            break
                        else:
                            new_inside_tag = soup_object.new_tag(next_sibling_search.name)
                            new_inside_tag.string = next_sibling_search.get_text()
                            current_section.append(new_inside_tag)

                        next_sibling_search = next_sibling_search.find_next_sibling()

                    sections.append(current_section)
                else:
                    current_section = None

            # Replace the old <main> with the new sections
            soup_content.clear()
            for section in sections:
                soup_content.append(section)
            
            sections = soup_content.find_all('section')

            for section in sections:
                text += section.get_text(strip=True, separator='\n') + "\n"
            return text

        else: 
            #No table of contents found (probably a summary and not a report), provide text
            text = soup_content.get_text(separator='\n', strip=True)
            return text
