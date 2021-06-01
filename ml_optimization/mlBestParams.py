from surprise import KNNBasic
from surprise import SVD, SVDpp
from surprise import Dataset
from surprise import Reader
from surprise import accuracy
import pandas as pd

df = pd.read_csv('../Tripadvisor_users.csv')

reader = Reader(rating_scale=(1, 5))
data = Dataset.load_from_df(df[['Username', 'Hotel_Name', 'Note']], reader)
trainset = data.build_full_trainset()  # Build on entire data set with values
testset = trainset.build_anti_testset()  # Build on data set that has no rating

def svd_best_params(model):
    list_epochs = []
    list_lr = []
    list_reg = []

    for i in range(20, 30):
        list_epochs.append(i)

    for i in range(5, 10):
        list_lr.append(i/1000)

    for i in range(5, 10):
        list_reg.append(i/100)

    svd_rmse = 1
    best_params_svd = [("n_epochs", 20), ("lr_all", 0.005), ("reg_alls", 0.02)]
    for i in range(len(list_epochs)):
        for j in range(len(list_lr)):
            for k in range(len(list_reg)):
                if model == "SVD":
                    svd = SVD(n_epochs=list_epochs[i], lr_all=list_lr[j], reg_all=list_reg[k], random_state=1)
                    svd.fit(trainset)
                    svd_predictions = svd.test(testset)
                    svd_error = accuracy.rmse(svd_predictions)
                    if svd_error < svd_rmse:
                        svd_rmse = svd_error
                        best_params_svd[0] = ('n_epochs', list_epochs[i])
                        best_params_svd[1] = ('lr_all', list_lr[j])
                        best_params_svd[2] = ('reg_all', list_reg[k])

                if model == "SVDpp":
                    svd = SVDpp(n_epochs=list_epochs[i], lr_all=list_lr[j], reg_all=list_reg[k], random_state=1)
                    svd.fit(trainset)
                    svd_predictions = svd.test(testset)
                    svd_error = accuracy.rmse(svd_predictions)
                    if svd_error < svd_rmse:
                        svd_rmse = svd_error
                        best_params_svd[0] = ('n_epochs', list_epochs[i])
                        best_params_svd[1] = ('lr_all', list_lr[j])
                        best_params_svd[2] = ('reg_all', list_reg[k])
    if model == "SVD":
        print("For SVD : ")
    if model == "SVDpp":
        print("For SVDpp : ")
    print("Best RMSE : ", svd_rmse)
    print("Best Params :\n", best_params_svd)


def knn_best_params():
    list_k = []
    for i in range(1, 10):
        list_k.append(i)
    knn_rmse = 1
    best_params_knn = 1

    for i in list_k:
        knn = KNNBasic(k=i, random_state=1)
        knn.fit(trainset)
        knn_predictions = knn.test(testset)
        knn_error = accuracy.rmse(knn_predictions)
        if knn_error < knn_rmse:
            knn_rmse = knn_error
            best_params_knn = i
    print("Best RMSE for kNN : ", knn_rmse)
    print("Best K for knn : ", best_params_knn)


if __name__ == "__main__":
    svd_best_params("SVD")
    svd_best_params("SVDpp")
    knn_best_params()








