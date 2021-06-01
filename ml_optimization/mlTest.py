from surprise import KNNBasic, KNNWithMeans, KNNWithZScore, accuracy
from surprise import SVD, SVDpp, NMF
from surprise import Dataset
from surprise import Reader
import pandas as pd
import matplotlib.pyplot as plt


def load_sets(base):
    df = pd.read_csv('../Tripadvisor_users.csv')
    reader = Reader(rating_scale=(1, 5))
    data = Dataset.load_from_df(df[['Username', 'Hotel_Name', 'Note']], reader)
    sim_options = {'name': 'cosine', 'ml_optimization': base}
    trainset = data.build_full_trainset()  # Build on entire data set with values
    testset = trainset.build_anti_testset() # Build on data set that has no rating
    return sim_options, trainset, testset


def algos(base):
    sim_options, trainset, testset = load_sets(base)
    knnbasic = KNNBasic(sim_options=sim_options, random_state=1)
    knnbasic.fit(trainset)
    knn_predictions = knnbasic.test(testset)
    knnbasic_error = accuracy.rmse(knn_predictions)

    knnmeans = KNNWithMeans(sim_options=sim_options, random_state=1)
    knnmeans.fit(trainset)
    knnmeans_predictions = knnmeans.test(testset)
    knnmeans_error = accuracy.rmse(knnmeans_predictions)

    knnscore = KNNWithZScore(sim_options=sim_options, random_state=1)
    knnscore.fit(trainset)
    knnscore_predictions = knnscore.test(testset)
    knnscore_error = accuracy.rmse(knnscore_predictions)

    nmf = NMF(random_state=1)
    nmf.fit(trainset)
    nmf_predictions = nmf.test(testset)
    nmf_error = accuracy.rmse(nmf_predictions)

    svd = SVD(random_state=1)
    svd.fit(trainset)
    svd_predictions = svd.test(testset)
    svd_error = accuracy.rmse(svd_predictions)

    svd_pp = SVDpp(random_state=1)
    svd_pp.fit(trainset)
    svd_pp_predictions = svd_pp.test(testset)
    svd_pp_error = accuracy.rmse(svd_pp_predictions)

    return knnbasic_error, knnmeans_error, knnscore_error, nmf_error, svd_error, svd_pp_error


def plot_algos():
    bases = [True, False]
    plt.figure(figsize=(20, 5))
    plt.subplot(1, 2, 1)
    plt.xlabel('Algorithms', fontsize=15)
    plt.ylabel('RMSE Value', fontsize=15)
    plt.grid(ls='dashed')
    plt.title('Comparison of Algorithms on RMSE', loc='center', fontsize=15)
    tuples_user_based = []
    tuples_item_based = []
    for base in bases:
        knnbasic_error, knnmeans_error, knnscore_error, nmf_error, svd_error, svd_pp_error = algos(base)
        x_algo = ['KNN Basic', 'KNN Means', "KNN ZScore", "NMF", "SVD", "SVD++"]  # préparation du plot
        all_algos = [knnbasic_error, knnmeans_error, knnscore_error, nmf_error, svd_error, svd_pp_error]

        if base:
            plt.plot(x_algo, all_algos, label='RMSE User Based', color='darkred', marker='o')
            plt.legend()
            for i in range(len(x_algo)):
                tuple_algo = (x_algo[i], all_algos[i])
                tuples_user_based.append(tuple_algo)
            tuples_user_based.sort(key=lambda x: x[1])

        if not base:
            plt.plot(x_algo, all_algos, label='RMSE Item Based', color='lightcoral', marker='o')
            plt.legend()
            for i in range(len(x_algo)):
                tuple_algo = (x_algo[i], all_algos[i])
                tuples_item_based.append(tuple_algo)
            tuples_item_based.sort(key=lambda x: x[1])

    plt.show()
    print("\n", "Best algos for User Based :\n", "1 -", tuples_user_based[0][0], "with RMSE :", tuples_user_based[0][1])
    print("2 -", tuples_user_based[1][0], "with RMSE :", tuples_user_based[1][1])
    print("3 -", tuples_user_based[2][0], "with RMSE :", tuples_user_based[2][1], "\n")

    print("Best algos for Item Based :\n", "1 -", tuples_item_based[0][0], "with RMSE :", tuples_item_based[0][1])
    print("2 -", tuples_item_based[1][0], "with RMSE :", tuples_item_based[1][1])
    print("3 -", tuples_item_based[2][0], "with RMSE :", tuples_item_based[2][1])


if __name__ == "__main__":
    plot_algos()
