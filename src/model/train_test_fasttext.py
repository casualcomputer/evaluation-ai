import os
import fasttext


def train_fasttext(path, dept_type):
	model = fasttext.train_unsupervised(path+'/'+dept_type+'_all_text.txt')
	print(model.get_nearest_neighbors('cancer'))


def text_concat(r_path): 

	cra_evals_text =  ''
	esdc_evals_text =  ''
	hc_evals_text =  ''
	nrc_evals_text =  ''

	w_path = '../../data/concat/cleaned'

	for file in os.listdir(r_path):

		full_path = os.path.join(r_path, file)
		file_text = ''

		if not file.startswith('.'):
			with open(full_path, 'r', encoding='utf-8') as file_extract:
				file_text = file_extract.read()

		if file.startswith('cra'):
			cra_evals_text += file_text + "\n"

		elif file.startswith('esdc'):
			esdc_evals_text += file_text + "\n"

		elif file.startswith('hc'):
			hc_evals_text += file_text + "\n"

		elif file.startswith('nrc'):
			nrc_evals_text += file_text + "\n"
	
	with open(w_path+'/cra_all_text.txt', 'w', encoding='utf-8') as output_file:
		output_file.write(cra_evals_text)

	with open(w_path+'/esdc_all_text.txt', 'w', encoding='utf-8') as output_file:
		output_file.write(esdc_evals_text)

	with open(w_path+'/hc_all_text.txt', 'w', encoding='utf-8') as output_file:
		output_file.write(hc_evals_text)
	
	with open(w_path+'/nrc_all_text.txt', 'w', encoding='utf-8') as output_file:
		output_file.write(nrc_evals_text)



def main():

	super_read_path = '../../data/clean/cleaned'
	super_concat_path = '../../data/concat/cleaned'
	#text_concat(super_read_path)

	train_fasttext(super_concat_path, 'hc')



if __name__ == '__main__':
    main()