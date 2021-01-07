import spacy
import json
from own_functions import remove_punctuation_hyphen
from own_functions import convert_date


nlp = spacy.load('nl_core_news_md')
source_file = "/home/gillesfloreal/PycharmProjects/NYT_Project/scrapingproject/MO_klimaat_test.json"
freq_dict = {}

source_stoplist = "/home/gillesfloreal/PycharmProjects/NYT_Project/stoplist.json"
with open(source_stoplist) as stopwords:
    stopwords_list = json.load(stopwords)


with open(source_file) as f:
    corpus = json.load(f)
    for article in corpus:

        date = convert_date(article["date"])
        title = article["title"]

        body = article["body"]
        body_no_punct = remove_punctuation_hyphen(body)
        body_no_newline = body_no_punct.replace("\n", " ")
        doc = nlp(body_no_newline)

        if date not in freq_dict:
            freq_dict[date] = {}

        freq_dict[date][title] = {}

        freq_dict[date][title]["url"] = article["url"]
        freq_dict[date][title]["frequency"] = {}

        for token in doc:
            lemma = token.lemma_
            if lemma not in stopwords_list and lemma.isdigit() is False and lemma != " " and lemma != "e":
                if lemma in freq_dict[date][title]["frequency"]:
                    freq_dict[date][title]["frequency"][lemma] += 1
                else:
                    freq_dict[date][title]["frequency"][lemma] = 1

    with open('freq_dict_article.json', 'w') as outfile:
        json.dump(freq_dict, outfile)




