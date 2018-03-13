import numpy as np
import nltk
from nltk.tokenize import word_tokenize # using sent_tokenize won't work
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

def preprocess(file_name):

    file = open(file_name,"r")

    if file.mode == 'r':
        content = file.read()

    sentences = content.split(".")
    words = []
    for i,j in enumerate(sentences):
        words.append(word_tokenize(j))

    stop_words = set(stopwords.words('english'))

    ps = PorterStemmer()

    for i in range(np.shape(words)[0]):
        words[i] = [w for w in words[i] if not w in stop_words and w.isalpha()] # Removes stop_words and punctuations

    pos_tagged = np.copy(words)
    # ner_tags = np.copy(words)

    # POS Tagging
    
    try:
        for i,j in enumerate(words):
            pos_tagged[i] = []
            for p,q in enumerate(nltk.pos_tag(j)):
                pos_tagged[i].append(q[1])
    except Exception as e:
        print(str(e))
    save_name = file_name.split(".")[0] + "_pos." + file_name.split(".")[1]
    file_new = open(save_name2,"w+")
    for i in range(np.shape(pos_tagged)[0]):
    for j in pos_tagged[i]:
        file_new.write(j+" ")
    file_new.write("\n")
    file_new.close()
    # NER Tagging
    """
    try:
        for i,j in enumerate(words):
            tagged = nltk.pos_tag(words[i])
            ner_tags[i] = nltk.ne_chunk(tagged, binary=False)
    except Exception as e:
        print(str(e))
    """

    # for i in range(np.shape(words)[0]): # Perform stemming only after POS and NER Tagging
    #     for j,a in enumerate(words[i]):
    #         words[i][j] = ps.stem(a)

    # save_name = file_name.split(".")[0] + "_words." + file_name.split(".")[1]

    # file_new = open(save_name,"w+")
    # for i in range(np.shape(words)[0]):
    # for j in words[i]:
    #     file_new.write(j+" ")
    # file_new.write("\n")
    # file_new.close()

    file.close()

names=open("names.txt", "r")
file_names=names.read()
nm=file_names.split()
for f in nm:
    print(f)
    preprocess(f)
