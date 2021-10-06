# _____TF-IDF libraries_____
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

# _____helper Libraries_____
import pickle
import json
import random

def talk_to_cb_primary(test_set_sentence, minimum_score , json_file_path , tfidf_vectorizer_pikle_path ,tfidf_matrix_train_pikle_path):
   
   
    test_set = (test_set_sentence, "")

    try:
        ##--------------to use------------------#
        f = open(tfidf_vectorizer_pikle_path, 'rb')
        tfidf_vectorizer = pickle.load(f)
        f.close()

        f = open(tfidf_matrix_train_pikle_path, 'rb')
        tfidf_matrix_train = pickle.load(f)
        f.close()
        # ----------------------------------------#
    except:
        # ---------------to train------------------#
        tfidf_vectorizer , tfidf_matrix_train = train_chat(json_file_path , tfidf_vectorizer_pikle_path , tfidf_matrix_train_pikle_path)
        # -----------------------------------------#

    tfidf_matrix_test = tfidf_vectorizer.transform(test_set)

    cosine = cosine_similarity(tfidf_matrix_test, tfidf_matrix_train)

    cosine = np.delete(cosine, 0)
    max = cosine.max()
    response_index = 0
    if (max > minimum_score):
        new_max = max - 0.01
        list = np.where(cosine > new_max)
        response_index = random.choice(list[0])
    else :
        return "sorry I can't understand what you want to say" , 0

    j = 0

    with open(json_file_path, "r") as sentences_file:
        reader = json.load(sentences_file)
        for row in reader:
            j += 1  # we begin with 1 not 0 &    j is initialized by 0
            if j == response_index:
                return row["response"], max
                break



def train_chat(json_file_path, tfidf_vectorizer_pikle_path , tfidf_matrix_train_pikle_path):
        
        i = 0
        sentences = []
        sentences.append('No you')
        sentences.append('No you')

        with open(json_file_path, "r") as sentences_file:
            reader = json.load(sentences_file)
            for row in reader:
                sentences.append(row["message"])
                i += 1

        tfidf_vectorizer = TfidfVectorizer()
        tfidf_matrix_train = tfidf_vectorizer.fit_transform(sentences)  # finds the tfidf score with normalization

        f = open(tfidf_vectorizer_pikle_path, 'wb')
        pickle.dump(tfidf_vectorizer, f)
        f.close()

        f = open(tfidf_matrix_train_pikle_path, 'wb')
        pickle.dump(tfidf_matrix_train, f)
        f.close()

        return tfidf_vectorizer , tfidf_matrix_train
        # -----------------------------------------#


def previous_chats(query,opt=True):
    minimum_score = 0.7
    file = "data/student.json"
    tfidf_vectorizer_pikle_path = "data/student_tfidf_vectorizer.pickle"
    tfidf_matrix_train_path = "data/student_tfidf_matrix_train.pickle"
    query_response, score = talk_to_cb_primary(query , minimum_score , file , tfidf_vectorizer_pikle_path , tfidf_matrix_train_path)
    if query_response!="student" or (query_response=="student" and opt==False):
        file="data/guest.json"
        tfidf_vectorizer_pikle_path = "data/guest_tfidf_vectorizer.pickle"
        tfidf_matrix_train_path = "data/guest_tfidf_matrix_train.pickle"
        query_response, score = talk_to_cb_primary(query , minimum_score , file , tfidf_vectorizer_pikle_path , tfidf_matrix_train_path)
    if query_response=="sorry I can't understand what you want to say":
        	file="data/previous_chats.json"
        	tfidf_vectorizer_pikle_path = "data/previous_tfidf_vectorizer.pickle"
        	tfidf_matrix_train_path = "data/previous_tfidf_matrix_train.pickle"
        	query_response, score = talk_to_cb_primary(query , minimum_score , file , tfidf_vectorizer_pikle_path , tfidf_matrix_train_path)

    
    return query_response

