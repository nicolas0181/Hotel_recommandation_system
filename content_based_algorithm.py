import pandas as pd
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import pickle


def get_hotels():
    df = pd.read_csv('Tripadvisor_hotels.csv')
    df = df.drop_duplicates(subset='Name', keep="last")
    df = df[df["Description"] != "-"]
    df = df.dropna()
    list_hotels = df["Name"]
    list_hotels.drop_duplicates()
    list_hotels = list_hotels.to_list()
    list_hotels = list(dict.fromkeys(list_hotels))
    return list_hotels


def get_important_words(df):
    # nltk.download("stopwords")
    en_stopwords = stopwords.words('english')
    en_stopwords.append(["hotel", "hôtel", "hostel"])
    list_desc = df.to_list()
    new_list_desc = []
    for desc in list_desc:
        new_desc = ""
        if type(desc) == str:
            for word in desc.split():
                only_alpha = ""
                for char in word:
                    if char.isalpha():
                        only_alpha += char
                only_alpha = only_alpha.lower()
                if only_alpha not in en_stopwords and only_alpha != "":
                    new_desc += only_alpha + " "
        new_list_desc.append(new_desc)
    new_df = pd.Series(new_list_desc)

    return new_df


def cosine_similar():

    df_hotels = pd.read_csv("Tripadvisor_hotels.csv")

    # Drop hotels with no description
    df_hotels = df_hotels[df_hotels["Description"] != "-"]
    df_hotels = df_hotels.dropna()
    df_hotels = df_hotels.drop_duplicates(subset='Name', keep="last")
    X = df_hotels["Description"]
    X_filtered = get_important_words(X)
    tfidf = TfidfVectorizer()

    # Apply fit_transform to document: csr_mat
    description_vetorized = tfidf.fit_transform(X_filtered.values.astype('U'))

    cosine_sim = linear_kernel(description_vetorized, description_vetorized)

    pkl_filename = "ressources/content_based_model.pkl"
    with open(pkl_filename, 'wb') as file:
        pickle.dump(cosine_sim, file)


def pickle_model():
    with open("ressources/content_based_model.pkl", 'rb') as file:
        pickle_model = pickle.load(file)

    df_hotels = pd.read_csv("Tripadvisor_hotels.csv")
    df_hotels = df_hotels[df_hotels["Description"] != "-"]
    df_hotels = df_hotels.dropna()
    df_hotels = df_hotels.drop_duplicates(subset='Name', keep="last")
    hotel_titles = df_hotels["Name"]
    indices = pd.Series(df_hotels.index, index=hotel_titles).drop_duplicates()

    return indices, pickle_model, df_hotels


def content_recommender(name, n, indices, cosine_sim, df_hotels):
    # Obtain the indice hotel that matches the name
    idx = indices[name]
    # Get the pairwise similarity scores of all hotels with that hotel
    # Convert it into a list of tuples
    sim_scores = list(enumerate(cosine_sim[idx]))
    # Sort the hotels based on the cosine similarity scores

    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    # Get scores of the n most similar hotels . Ignore the first hotels car similarity = 1 (le meme)
    sim_scores = sim_scores[1:n+1]
    # Get the hotels indices
    hotels_indices = [i[0] for i in sim_scores]
    # Return the n most similar hotels
    return df_hotels['Name'].iloc[hotels_indices], df_hotels['Destination'].iloc[hotels_indices]


if __name__ == "__main__":
    cosine_similar()  # fit the model and save it
    #print(get_hotels())
    #get_important_words()

