import spacy
import json
from own_functions import remove_punctuation_hyphen
import os

nlp = spacy.load('nl_core_news_md')
source_file = "/home/gillesfloreal/PycharmProjects/NYT_Project/scrapingproject/ref_corp.json"
focus_corpus_file = "/home/gillesfloreal/PycharmProjects/NYT_Project/freq_dict_article.json"
freq_dict = {}

# read words from focus corpus, make new dict where all values are 0
with open(focus_corpus_file) as f:
    f_corp = json.load(f)
    for date in f_corp:
        for article in f_corp[date]:
            for lemma in f_corp[date][article]["frequency"]:
                if lemma not in freq_dict:
                    freq_dict[lemma] = 0


source_stoplist = "/home/gillesfloreal/PycharmProjects/NYT_Project/stoplist.json"
with open(source_stoplist) as stopwords:
    stopwords_list = json.load(stopwords)

source_directory = "/home/gillesfloreal/PycharmProjects/NYT_Project/scrapingproject/ref_corp"

for file in os.listdir(source_directory):
    source_ref = "/home/gillesfloreal/PycharmProjects/NYT_Project/scrapingproject/ref_corp/" + file
    with open(source_ref) as f:
        corpus = json.load(f)
        for article in corpus:

            title = article["title"]
            body = article["body"]
            body_no_punct = remove_punctuation_hyphen(body)
            body_no_newline = body_no_punct.replace("\n", " ")
            doc = nlp(body_no_newline)

            freq_dict[title] = {}

            for token in doc:
                lemma = token.lemma_

                if lemma in freq_dict:
                    freq_dict[lemma] += 1

    with open('freq_dict_ref.json', 'w') as outfile:
        json.dump(freq_dict, outfile)




