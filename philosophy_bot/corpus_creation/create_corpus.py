import glob
import pickle
import markovify

def read_files(files):
    file_list = []
    for file in files:
        with open(file) as f:
            file_list.append(f.read())
    return file_list

files = glob.glob('./corpora_processed/*.txt')
corpora_files = read_files(files)
markov_models = [markovify.Text(corpus) for corpus in corpora_files]
full_philosophy_model = markovify.combine(markov_models)

with open('philosophy_bot.pkl', 'wb') as f:
    pickle.dump(full_philosophy_model, f, protocol = 2)

#Link: https://www.gutenberg.org/ebooks/search/?query=philosophy&go=Go