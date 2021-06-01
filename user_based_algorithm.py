from surprise import KNNBasic
from surprise import Dataset
from surprise import accuracy
from collections import defaultdict
import pandas as pd
from surprise import Reader
import pickle


def get_users():
    df = pd.read_csv('Tripadvisor_users.csv')
    list_users = df["Username"].to_list()
    list_users = list(dict.fromkeys(list_users))
    return list_users


def user_based_model(n):

    df = pd.read_csv('Tripadvisor_users.csv')

    reader = Reader()
    data = Dataset.load_from_df(df[['Username', 'Hotel_Name', 'Note']], reader)
    sim_options = {'name': 'cosine',
                   'user-based': True,  # compute  similarities between items
                   'k': 4
                   }

    algo = KNNBasic(sim_options=sim_options)

    trainset = data.build_full_trainset()  # Build on entire data set
    algo.fit(trainset)

    testset = trainset.build_anti_testset()

    # Predicting the ratings for testset
    predictions = algo.test(testset)

    erreur = accuracy.rmse(predictions)

    print(erreur)

    similar_n = defaultdict(list)
    for uid, iid, true_r, est, _ in predictions:
        similar_n[uid].append((iid, est))

    # Sort the predictions for each user
    for uid, user_ratings in similar_n.items():
        user_ratings.sort(key=lambda y: y[1], reverse=True)
        similar_n[uid] = user_ratings[:n]
    with open("ressources/predict_user_based.pkl", "wb") as pkl_handle:
        pickle.dump(similar_n, pkl_handle)


def item_based_model(n):

    df = pd.read_csv('Tripadvisor_users.csv')

    reader = Reader()
    data = Dataset.load_from_df(df[['Username', 'Hotel_Name', 'Note']], reader)
    sim_options = {'name': 'cosine',
                   'user-based': False,  # compute  similarities between items
                   'k': 4
                   }
    algo = KNNBasic(sim_options=sim_options)

    trainset = data.build_full_trainset()  # Build on entire data set
    algo.fit(trainset)

    testset = trainset.build_anti_testset()

    # Predicting the ratings for testset
    predictions = algo.test(testset)

    erreur = accuracy.rmse(predictions)

    print(erreur)

    similar_n = defaultdict(list)
    for uid, iid, true_r, est, _ in predictions:
        similar_n[uid].append((iid, est))

    # Sort the predictions for each user
    for uid, user_ratings in similar_n.items():
        user_ratings.sort(key=lambda y: y[1], reverse=True)
        similar_n[uid] = user_ratings[:n]
    with open("ressources/predict_item_based.pkl", "wb") as pkl_handle:
        pickle.dump(similar_n, pkl_handle)


# Print the best 5 hotels
def predict_recommanded(user_id, n, base):

    if base == "item":
        with open("ressources/predict_item_based.pkl", "rb") as pkl_handle:
            pred_user = pickle.load(pkl_handle)
    elif base == "user":
        with open("ressources/predict_user_based.pkl", "rb") as pkl_handle:
            pred_user = pickle.load(pkl_handle)

    # Transpose into a matrix
    tmp = pd.DataFrame.from_dict(pred_user)
    tmp_transpose = tmp.transpose()

    # Recommandation For the User
    results_pred = tmp_transpose.loc[user_id]

    #  Store the recommandations
    recommended_hotels = []
    for x in range(0, n):
        recommended_hotels.append(results_pred[x][0])
    return recommended_hotels


if __name__ == "__main__":
    user_based_model(5)
    item_based_model(5)
