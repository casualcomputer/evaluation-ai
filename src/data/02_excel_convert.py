import argparse
import pandas as pd
import os


from utils import get_files, clear_files, timeit

@timeit
def save_excel(read_path, save_path, verbose):
    """
    Puts text files into excel file.
    
    :param read_path: The path to read the data from.
    :type read_path: str
    :param save_path: The path to save the extracted data to.
    :type save_path: str
    :param verbose: Whether or not to print progress to the console.
    :type verbose: bool

    :return: None
    :rtype: None
    """

    files = get_files(read_path)

    #initialization of dataframe
    df = pd.DataFrame(columns=['Agency', 'Content'])

    if verbose: 
    	print(f'Processing {len(files)} files...')
    	print("="*25)

    for i, file in enumerate(files):
            file_id = str(i+1).zfill(len(str(len(files))))

            if ".DS_Store" in file:
            	continue

            with open(file, 'r',encoding='utf-8') as f:
            	file_content = f.read()

            if "cra" in file:
            	label = 'CRA'
            elif "esdc" in file:
            	label = 'ESDC'
            elif "nrc" in file:
            	label = 'NRC'
            else:
            	label = 'HC'

            df = pd.concat([df,pd.DataFrame({'Agency': label, 'Content': file_content}, index=[0])], ignore_index=True)

            if verbose:
            	print(f'{Fore.GREEN}[{file_id}/{len(files)}]: {file}{Style.RESET_ALL}')

    output_path = os.path.join(save_path, 'all.xlsx')

    df.to_excel(output_path, index=False, header = False)



def main():
    parser = argparse.ArgumentParser(description='Loads text file data to excel file.')
    parser.add_argument('-r', '--read_path', type=str, default='../../data/clean/cleaned', help='The path to read the text files from.')
    parser.add_argument('-s', '--save_path', type=str, default='../../data', help='The path to save the extracted excel to.')
    parser.add_argument('-v', '--verbose', action='store_true', help='Whether or not to print progress to the console.')
    parser.add_argument('-c', '--clear', action='store_true', help='Whether or not to clear the save_path before running.')
    args = parser.parse_args()

    if args.clear: clear_files(args.save_path)

    save_excel(args.read_path, args.save_path, args.verbose)

if __name__ == '__main__':
    main()