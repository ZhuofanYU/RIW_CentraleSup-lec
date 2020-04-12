import matplotlib.pyplot as plt
from tqdm import tqdm
import pickle as pkl
import math
import numpy as np
import nltk
import os

path_queries = "./test/dev_queries/"
path_out = "./test/dev_output/"


Vocabulary = pkl.load(open("Vocabulary.pkl", "rb"))
Freq_Vocabulary = pkl.load(open("Freq_Vocabulary.pkl", "rb"))
Collection = pkl.load(open("Collection.pkl", "rb"))
Absolute_Values = pkl.load(open("Absolute_Values.pkl", "rb"))
TF_IDF = pkl.load(open("TF_IDF.pkl", "rb"))


def load_queries():
    queries = {}
    for r, d, f in os.walk(path_queries):
        for file in f:
            with open(path_queries + file, 'r') as f:
                query = f.readline()
                queries[file[-1]] = query.strip('\n')
    return queries


def load_output():
    solutions = {}
    for r, d, f in os.walk(path_out):
        for file in f:
            solutions[file[0]] = []
            with open(path_out + file, 'r') as f:
                lines = f.readlines()
                for solution in lines:
                    solutions[file[0]].append(solution.strip('\n'))
    return solutions


def precision_interpolate(precision: list):
    result = []
    for i in range(len(precision)):
        result.append(max(precision[i:]))
    return result


def evaluate(id=0, nb=100, threshold=0):
    nb_total = 0
    nb_total_rappel = 0
    nb_correct = 0
    correct = []
    for query_id in tqdm(collection_queries.keys()):
        if id == 0:
            answers = search(
                collection_queries[query_id], nb, threshold=threshold)
            nb_total += len(answers)
            nb_total_rappel += len(collection_output[query_id])
            for answer in answers.keys():
                if answer in collection_output[query_id]:
                    # print('correct: {}'.format(answers[answer]))
                    nb_correct += 1

        elif query_id == str(id):
            answers = search(
                collection_queries[query_id], nb, threshold=threshold)
            nb_total += len(answers)
            nb_total_rappel += len(collection_output[query_id])
            for answer in answers.keys():
                if answer in collection_output[query_id]:
                    # print('correct: {}'.format(answers[answer]))
                    nb_correct += 1
    if nb_total == 0:
        nb_total = 1
    if nb_total_rappel == 0:
        nb_total_rappel = 1
    precision = nb_correct/nb_total
    rappel = nb_correct / nb_total_rappel
    print("number of correct files: {}".format(nb_correct))
    print("precision:{},rappel:{}".format(precision, rappel))
    return [precision, rappel]


def evaluate_threshold(id=0, nb=100000, threshold=0):
    threshold_correct = []
    threshold_wrong = []
    nb_correct = []
    nb_wrong = []
    cnt_correct = 0
    cnt_wrong = 0
    if id == 0:
        for query_id in tqdm(collection_queries.keys()):
            answers = search(
                collection_queries[query_id], nb=nb, threshold=threshold)
            for answer in answers.keys():
                if answer in collection_output[query_id]:
                    # print('correct: {}'.format(answers[answer]))
                    cnt_correct += 1
                    nb_correct.append(cnt_correct)
                    threshold_correct.append(answers[answer])
                else:
                    # print('wrong: {}'.format(answers[answer]))
                    cnt_wrong += 1
                    nb_wrong.append(cnt_wrong)
                    threshold_wrong.append(answers[answer])
    else:
        query_id = str(id)
        answers = search(
            collection_queries[query_id], nb=nb, threshold=threshold)
        for answer in answers.keys():
            if answer in collection_output[query_id]:
                # print('correct: {}'.format(answers[answer]))
                cnt_correct += 1
                nb_correct.append(cnt_correct)
                threshold_correct.append(answers[answer])
            else:
                # print('wrong: {}'.format(answers[answer]))
                cnt_wrong += 1
                nb_wrong.append(cnt_wrong)
                threshold_wrong.append(answers[answer])

    max_x = 1.55
    fig, ax = plt.subplots(figsize=(8, 4))
    n_correct, bins_correct, patches_correct = ax.hist(
        threshold_correct, label='pertinent', bins=1000, cumulative=True)
    n_wrong, bins_wrong, patches_wrong = ax.hist(
        threshold_wrong, label='non-pertinent', bins=1000, cumulative=True)
    # print(n_correct)
    ax.grid(True)
    ax.legend(loc='center left')
    ax.set_ylabel('Cumulate number')

    index = 0
    for i in range(len(bins_wrong)):
        if bins_wrong[i] >= 1.55 and bins_correct[i] >= 1.55:
            index = i
            break
    if index != 0:
        ax.set_ylim(0, int(1.7*max(n_correct[index], n_wrong[index])))
    #print(max(n_correct[index], n_wrong[index]))
    #ax.set_ylim(0, 1.7*max(n_correct[index], n_wrong[index]))

    x = []
    precision = []
    rappel = []
    i = 1.2
    while i <= max_x:
        result = evaluate(id=0, threshold=i)
        x.append(i)
        precision.append(result[0])
        rappel.append(result[1])
        i += 0.01
    ax2 = ax.twinx()
    ax2.plot(x, precision, color='r', label='précision')
    precision_inter = precision_interpolate(precision)
    ax2.plot(x, precision_inter, color='b', label='précision interpolée')
    ax2.plot(x, rappel, color='g', label='rappel')
    # ax2.set_ylabel('Percentage(%)')
    ax2.legend()

    plt.xlabel('score')
    plt.xlim(1.2, max_x)
    plt.show()
    """plt.plot(threshold_correct, y, alpha=0.6)
    plt.ylabel("cnt")
    plt.xlabel("threshold")
    plt.title("Thredshold-cnt")
    # plt.ylim(0, 1)
    # plt.xlim(0, 1)
    plt.show()"""


collection_queries = load_queries()
collection_output = load_output()


def preprocess_query(query):

    processed_query = {}

    tokenizer = nltk.tokenize.RegexpTokenizer(r'\w+')
    stop_words = nltk.corpus.stopwords.words('english')
    lematizer = nltk.stem.WordNetLemmatizer()
    steamer = nltk.stem.PorterStemmer()

    query = tokenizer.tokenize(query)

    query_no_stop_words = []
    for word in query:
        if word not in stop_words:
            query_no_stop_words.append(word)

    query = query_no_stop_words
    query = [lematizer.lemmatize(word) for word in query]
    query = [steamer.stem(word) for word in query]

    for word in query:

        try:
            idf = math.log(len(Collection) / Freq_Vocabulary[word], 10)
            tf = query.count(word)
            processed_query[word] = tf*idf
        except KeyError:
            pass

    return processed_query


def search(query, nb=10, threshold=0):

    query = preprocess_query(query)

    abs_query = 0.000001
    for word in query:
        abs_query = abs_query + query[word]**2
    abs_query = math.sqrt(abs_query)

    Score = []
    for document in Collection:

        dot_product = 0
        for word in query:
            try:
                dot_product = dot_product + TF_IDF[document, word]*query[word]
            except KeyError:
                pass

        angle = math.acos(dot_product/(Absolute_Values[document]*abs_query))
        Score.append((document, angle))

    Query_Results = sorted(Score, key=lambda x: x[1])

    i = 0
    results = {}
    for result in Query_Results:

        if threshold != 0:
            if result[1] <= threshold:
                results[result[0]] = result[1]
        else:
            if i == nb:
                break
            results[result[0]] = result[1]
            i = i + 1
    return results


# evaluate(id=8)
# evaluate(threshold=0.5)
# query = search("stanford students")
# print(query)
"""
cnt = 10
print("cnt = {}".format(cnt))
evaluate(cnt)
cnt = 50
print("cnt = {}".format(cnt))
evaluate(cnt)

cnt = 100
print("cnt = {}".format(cnt))

cnt = 400
print("cnt = {}".format(cnt))
evaluate(cnt)
cnt = 2000
print("cnt = {}".format(cnt))
evaluate(cnt)
cnt = 5000
print("cnt = {}".format(cnt))
evaluate(cnt)
"""


def plotPrecisionRappel(id):
    data = []
    data_inter = []
    # plt.figure(figsize=(8, 4))
    cnt = 10
    while cnt < 100000:
        result = evaluate(nb=cnt, id=str(id))
        cnt = int(cnt * 1.1)
        data.append([result[1], result[0]])
    data = sorted(data, key=(lambda x: x[0]))
    precision = []
    precision_inter = []
    rappel = []
    for i in range(len(data)):
        rappel.append(data[i][0])
        precision.append(data[i][1])
    for i in range(len(data)):
        precision_inter.append(max(precision[i:]))
    plt.scatter(rappel, precision, alpha=0.6, label='rappel-précision')
    plt.plot(rappel, precision_inter, alpha=0.8, color='r',
             label='rappel-précision interpolée')
    plt.ylabel("precision")
    plt.xlabel("Rappel")
    plt.title("Query " + str(id))
    plt.ylim(0, 1)
    plt.xlim(0, 1)
    plt.legend()
    plt.show()
