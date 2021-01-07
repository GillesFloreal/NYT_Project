import json
import os
from own_functions import remove_punctuation_hyphen

source_directory = "/home/gillesfloreal/PycharmProjects/NYT_Project/scrapingproject/MO_klimaat_test.json"
os.mkdir("/home/gillesfloreal/PycharmProjects/NYT_Project/articles_txt")
target_directory = "/home/gillesfloreal/PycharmProjects/NYT_Project/articles_txt"

with open(source_directory) as f:
    corpus = json.load(f)
    word_count = 0
    article_count = 1
    for article in corpus:

        body = article["body"]
        body_no_punct = remove_punctuation_hyphen(body)
        word_list = body_no_punct.split()
        article_word_count = len(word_list)
        word_count += article_word_count

        new_item_name = "article_" + str(article_count)
        new_item = os.path.join(target_directory, new_item_name)
        with open(new_item, 'w') as new_file:
            new_file.write("word count: " + str(article_word_count) + "\n")
            for key in article:
                text = f"{key}: {article[key]}\n"
                new_file.write(text)

        article_count += 1





