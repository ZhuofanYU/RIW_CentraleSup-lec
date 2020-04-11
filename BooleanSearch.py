import numpy as np


D1 = "information retrieval and massive data processing"
D2 = "introduction to information retrieval"
D3 = "mining massive dataset"
D4 = "modern information retrieval"
D5 = "search engine information retrieval in practice"
D6 = "information retrieval implementing and evaluating search engine"

Collection = {"DOC1": D1,
            "DOC2": D2,
            "DOC3": D3,
            "DOC4": D4 ,
            "DOC5": D5,
             "DOC6" : D6}

StopWords = ["and", "to","in"]

BooleanOperator = {'AND', 'OR', 'NOT'}


def remove_stop_word(collection):
    filtered_collection = {}

    for key in collection:
        filtered_collection[key] = []
        for word in collection[key].split():
            if word not in StopWords:
                filtered_collection[key].append(word)

    return filtered_collection


# Here we filter the stop words from the Collection
Filtered_Collection = remove_stop_word(Collection)


# Get the vocabulary from the collection to construct the index element matrix
def get_vocabulary(collection):
    vocabulary = []

    for key in collection:
        for word in collection[key]:
            if word not in StopWords:

                if word not in vocabulary:
                    vocabulary.append(word)

    return vocabulary


Vocabulary = get_vocabulary(Filtered_Collection)
TM = np.zeros((len(Filtered_Collection),len(Vocabulary)), dtype=int)

for i,key in enumerate(Filtered_Collection):
    for j in range(len(Vocabulary)):

        if Vocabulary[j] in Filtered_Collection[key]:
            TM[i,j] = 1


# We use this function to process the boolean queries
def boolean_operator_processing(BoolOperator,term1,term2):
    result=[]

    if BoolOperator == "AND":
        for a , b in zip(term1,term2) :
            if a==1 and b==1 :
                result.append(1)
            else :
                result.append(0)
    elif BoolOperator == "OR":
        for a,b in zip(term1,term2):
            if a==0 and b==0 :
                result.append(0)
            else :
                result.append(1)
    elif BoolOperator == "NOT" :
        for b in term1:
            if b == 1:
                result.append(0)
            else :
                result.append(1)

    return result

# Take the query vector
def vectorize(term):

    try:
        j = Vocabulary.index(term)
    except ValueError:
        raise ValueError("Term not in vocabulary!!!")

    return list(TM[:, j])


list_of_documents = []
for key in Filtered_Collection:
    list_of_documents.append(key)


def query_processing(query):

    query = query.split()
    term = query.pop(0)

    result = vectorize(term)
    while len(query) != 0:

        operator = query.pop(0)
        word = query.pop(0)

        if word == "NOT":
            term = query.pop(0)
            compare = vectorize(term)
            compare = boolean_operator_processing(word, compare, [])
            print(operator, result, compare)
            result = boolean_operator_processing(operator, result, compare)
        else:
            compare = vectorize(word)
            print(operator, result, compare)
            result = boolean_operator_processing(operator, result, compare)


    to_return = []
    for k,index in enumerate(result):
        if index == 1:
            to_return.append(list_of_documents[k])

    return to_return

print(query_processing("information AND retrieval AND NOT massive"))







