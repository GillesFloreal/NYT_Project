import pandas as pd
import json
import math


freq_dict_json = "/home/gillesfloreal/PycharmProjects/NYT_Project/freq_dict_article.json"
freq_dict_ref = "/home/gillesfloreal/PycharmProjects/NYT_Project/freq_dict_ref.json"

ref_word_count = "/home/gillesfloreal/PycharmProjects/NYT_Project/ref_total_terms.json"

with open(freq_dict_ref, 'r') as f:
    ref_freq_dict = json.load(f)

with open(ref_word_count, 'r') as f:
    ref_term_count = json.load(f)


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
    url_dict = {}

    with open(freq_dict_json) as freq_dict:
        dict_corpus = json.load(freq_dict)

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

                        if lemma in url_dict:
                            url_dict[lemma].append(freq_dict_article[article]["url"])
                        else:
                            url_dict[lemma] = [freq_dict_article[article]["url"]]

    return period_frequency, total_terms, idf_dict, total_articles, url_dict


def tf_idf(date_1, date_2):

    freq_dict, total_n_terms, article_dict, article_count, url_dict = get_period_frequency(date_1, date_2)



    # first calculate tf

    # calculate tf for each individual term
    tf_terms = {}

    for lemma in freq_dict:
        tf_terms[lemma] = 1 + (math.log(freq_dict[lemma]))

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

        idf_terms[term] = math.log(article_count)/(term_doc_count[term] + 1)

    tfidf = {}

    # now calculate tf*idf

    # first calculate log-likelihood
    loglikelihood = {}
    for term in tf_terms:
        ref_term = ref_freq_dict[term]
        ref_total = ref_term_count
        Expected1 = total_n_terms * (freq_dict[term] + ref_term)/(total_n_terms + ref_total)
        Expected2 = ref_total * (freq_dict[term] + ref_term)/(total_n_terms + ref_total)
        t1 = freq_dict[term]* math.log((total_n_terms/Expected1))
        t2 = ref_term * math.log((ref_term/Expected2) + 1)

        Loglike = 2 * (t1 + t2)

        loglikelihood[term] = Loglike
    for term in tf_terms:

        if loglikelihood[term] < 666:  # if the term is not in the 99% percentile, cut off
            tfidf[term] = (tf_terms[term] * idf_terms[term])

    terms_sorted = sorted(tfidf.items(), key=lambda item: item[1], reverse=True)

    # now put the 10 highest scores in a list
    top_ten_list = []
    for i, item in enumerate(terms_sorted):
        if i == 10:
            break
        top_ten_list.append(item)

    return top_ten_list



