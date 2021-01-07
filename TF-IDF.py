import pandas as pd
import json
import math


freq_dict_json = "/home/gillesfloreal/PycharmProjects/NYT_Project/freq_dict_article.json"


start_date = input("Enter the start date")
end_date = input("Enter the end_date")


def get_list_days(date_1, date_2):
    dates = []
    daterange = pd.date_range(start=pd.to_datetime(date_1, dayfirst=True), end=pd.to_datetime(date_2, dayfirst=True))

    for single_date in daterange:
        dates.append(single_date.strftime("%d/%m/%Y"))

    return dates


def get_period_frequency(date_1, date_2):

    period = get_list_days(date_1, date_2)
    period_frequency = {}
    idf_dict = {}
    total_terms = 0
    total_articles = 0
    with open(freq_dict_json) as freq_ref_dict:
        dict_corpus = json.load(freq_ref_dict)

        for date in period:
            if date in dict_corpus:
                idf_dict[date] = dict_corpus[date]
                freq_dict_article = dict_corpus[date]
                # also calculate total terms and articles already so we don't have to loop over the dict too much
                for article in freq_dict_article:
                    total_articles += 1
                    for lemma in freq_dict_article[article]["frequency"]:
                        total_terms += freq_dict_article[article]["frequency"][lemma]
                        if lemma in period_frequency:
                            period_frequency[lemma] += freq_dict_article[article]["frequency"][lemma]
                        else:
                            period_frequency[lemma] = freq_dict_article[article]["frequency"][lemma]

    return period_frequency, total_terms, idf_dict, total_articles


def tf_idf(date_1, date_2):

    freq_dict, total_n_terms, article_dict, article_count = get_period_frequency(date_1, date_2)
    # first calculate tf

    # calculate tf for each individual term
    tf_terms = {}

    for lemma in freq_dict:
        tf_terms[lemma] = freq_dict[lemma]/total_n_terms

    # idf calculation
    # calculate how many times a term appears in an article
    idf_terms = {}
    term_doc_count = {}
    for lemma in tf_terms:
        for date in article_dict:
            for article in article_dict[date]:
                if lemma in article_dict[date][article]["frequency"]:
                    if lemma in term_doc_count:
                        term_doc_count[lemma] += 1
                    else:
                        term_doc_count[lemma] = 1
    # then calculate idf
    for term in term_doc_count:
        idf_terms[term] = math.log(article_count/(term_doc_count[term] + 1))

    tfidf = {}

    # now calculate tf*idf
    for term in tf_terms:
        tfidf[term] = tf_terms[term] * idf_terms[term]

    tfidf_sorted = sorted(tfidf.items(), key=lambda item: item[1], reverse=True)

    # now put the 10 highest scores in a list
    top_ten_list = []
    for i, item in enumerate(tfidf_sorted):
        if i == 10:
            break
        top_ten_list.append(item)

    return top_ten_list








