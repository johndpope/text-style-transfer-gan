import os
import re
import glob
import math
import string
import random
import numpy as np

data_dir_s1 = './raw_data/bible/DARBY'
data_dir_s2 = './raw_data/bible/YLT'
data_ext = 'txt'
vocab_length = 996

train_file_s1 = 'bible_darby.train.txt'
val_file_s1 = 'bible_darby.valid.txt'
test_file_s1 = 'bible_darby.test.txt'

train_file_s2 = 'bible_ylt.train.txt'
val_file_s2 = 'bible_ylt.valid.txt'
test_file_s2 = 'bible_ylt.test.txt'

files_s1 = list(glob.iglob(os.path.join(data_dir_s1, '**/*' + data_ext), recursive=True))
files_s1.sort(key=lambda x: os.path.basename(x)[:-(len(data_ext)+1)])
files_s2 = list(glob.iglob(os.path.join(data_dir_s2, '**/*' + data_ext), recursive=True))
files_s2.sort(key=lambda x: os.path.basename(x)[:-(len(data_ext)+1)])

transtab = str.maketrans('—', ' ', string.punctuation + '£…')
NUMBER_REGEX = r"""[-+]?[.]?[\d]+(?:,\d\d\d)*[\.]?\d*(?:[eE][-+]?\d+)?"""
vocabulary_s1 = {}
vocabulary_s2 = {}
num_sentences = 0
sentences_s1 = []
sentences_s2 = []

# Calculates the number of sentences
for filepath in files_s1:
    lines = []
    with open(filepath, 'r') as f:
        lines = f.readlines()
        num_sentences += len(lines)

ntrain = int(math.floor(0.75 * num_sentences))
nval = int(math.floor(0.05 * num_sentences))
ntest = num_sentences - ntrain - nval
perm = list(range(num_sentences))
random.shuffle(perm)

print(('Number of sentences:', num_sentences))
print ('ntrain\tnval\tntest')
print(('%d\t%d\t%d' % (ntrain, nval, ntest)))

tot_words_s1 = 0
# reading sentences in first style
for filepath in files_s1:
    lines = []
    with open(filepath, 'r') as f:
        lines = f.readlines()
    for s in lines:
        # web_sites = re.findall(WEB_URL_REGEX, s)
        # for w in web_sites:
        #     s = s.replace(w, '<unk>')
        # emails = re.findall(EMAIL_REGEX, s)
        # for e in emails:
        #     s = s.replace(e, '<unk>')
        numbers = re.findall(NUMBER_REGEX, s)
        for n in numbers:
            s = s.replace(n, ' numtok ')
        txt = str(s).lower().translate(transtab).strip().split()
        sentences_s1.append(txt[1:])
        tot_words_s1 += len(txt) - 1

sentences_s1 = [sentences_s1[i] for i in perm]
unprocessed_train_set_s1 = sentences_s1[:ntrain]

# create dictionary for S1
for sent in unprocessed_train_set_s1:
    for word in sent:
        if word != "unk":
            vocabulary_s1[word] = vocabulary_s1.get(word, 0) + 1

tmp_vocab_s1 = {}
for sent in sentences_s1:
    for word in sent:
        if word != "unk":
            tmp_vocab_s1[word] = tmp_vocab_s1.get(word, 0) + 1

print(("Number of words in vocab of training set for S1:", len(vocabulary_s1)))
print(("Number of words in vocab for S1:", len(tmp_vocab_s1)))
print(("Number of total words in S1:", tot_words_s1))

# printing unknown characters
char_set = []
unk_words = []
for word in list(vocabulary_s1.keys()):
    for c in word:
        if not (ord(c) >= 97 and ord(c) <= 122):
            char_set.append(c)
            unk_words.append(word)

vocab_list_s1 = list(sorted(vocabulary_s1, key=vocabulary_s1.get, reverse=True))[:vocab_length]

processed_dataset_s1 = []

for sent in sentences_s1:
    sent = [word if word in vocab_list_s1 else '<unk>' for word in sent]
    processed_dataset_s1.append(' '.join(sent))

train_set_s1 = processed_dataset_s1[:ntrain]
val_set_s1 = processed_dataset_s1[ntrain:(ntrain+nval)]
test_set_s1 = processed_dataset_s1[(ntrain+nval):]

print(('Writing:', train_file_s1))
with open(train_file_s1, 'w') as f:
    for l in train_set_s1:
        f.write("%s\n" % l)

print(('Writing:', val_file_s1))
with open(val_file_s1, 'w') as f:
    for l in val_set_s1:
        f.write("%s\n" % l)

print(('Writing:', test_file_s1))
with open(test_file_s1, 'w') as f:
    for l in test_set_s1:
        f.write("%s\n" % l)

print ()

tot_words_s2 = 0
# reading sentences in second style
for filepath in files_s2:
    lines = []
    with open(filepath, 'r') as f:
        lines = f.readlines()
    for s in lines:
        numbers = re.findall(NUMBER_REGEX, s)
        for n in numbers:
            s = s.replace(n, ' numtok ')
        txt = str(s).lower().translate(transtab).strip().split()
        sentences_s2.append(txt[1:])
        tot_words_s2 += len(txt) - 1

sentences_s2 = [sentences_s2[i] for i in perm]
unprocessed_train_set_s2 = sentences_s2[:ntrain]

# create dictionary for S2
for sent in unprocessed_train_set_s2:
    for word in sent:
        if word != "unk":
            vocabulary_s2[word] = vocabulary_s2.get(word, 0) + 1

tmp_vocab_s2 = {}
for sent in sentences_s2:
    for word in sent:
        if word != "unk":
            tmp_vocab_s2[word] = tmp_vocab_s2.get(word, 0) + 1

print(("Number of words in vocab for training set for S2:", len(vocabulary_s2)))
print(("Number of words in vocab for S2:", len(tmp_vocab_s2)))
print(("Number of total words in S2:", tot_words_s2))

vocab_list_s2 = list(sorted(vocabulary_s2, key=vocabulary_s2.get, reverse=True))[:vocab_length]

processed_dataset_s2 = []

for sent in sentences_s2:
    sent = [word if word in vocab_list_s2 else '<unk>' for word in sent]
    processed_dataset_s2.append(' '.join(sent))

train_set_s2 = processed_dataset_s2[:ntrain]
val_set_s2 = processed_dataset_s2[ntrain:(ntrain+nval)]
test_set_s2 = processed_dataset_s2[(ntrain+nval):]

print(('Writing:', train_file_s2))
with open(train_file_s2, 'w') as f:
    for l in train_set_s2:
        f.write("%s\n" % l)

print(('Writing:', val_file_s2))
with open(val_file_s2, 'w') as f:
    for l in val_set_s2:
        f.write("%s\n" % l)

print(('Writing:', test_file_s2))
with open(test_file_s2, 'w') as f:
    for l in test_set_s2:
        f.write("%s\n" % l)
