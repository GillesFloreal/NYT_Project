import json
import os
from own_functions import remove_punctuation_hyphen
import spacy

source_directory = "/home/gillesfloreal/PycharmProjects/NYT_Project/scrapingproject/ref_corp"
nlp = spacy.load('nl_core_news_md')

total_n_terms = 0

source_stoplist = "/home/gillesfloreal/PycharmProjects/NYT_Project/stoplist.json"
with open(source_stoplist) as stopwords:
    stopwords_list = json.load(stopwords)

for file in os.listdir(source_directory):
    source_ref = "/home/gillesfloreal/PycharmProjects/NYT_Project/scrapingproject/ref_corp/" + file
    with open(source_ref) as f:
        corpus = json.load(f)
        for article in corpus:

            body = article["body"]
            body_no_punct = remove_punctuation_hyphen(body)
            body_no_newline = body_no_punct.replace("\n", " ")
            doc = nlp(body_no_newline)

            for token in doc:
                lemma = token.lemma_
                if lemma not in stopwords_list and lemma.isdigit() is False and lemma != " " and lemma != "e":
                    total_n_terms += 1

with open('ref_total_terms', 'w') as count:
    json.dump(total_n_terms, count)