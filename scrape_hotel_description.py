from bs4 import BeautifulSoup
import requests
import pandas as pd

df = pd.read_csv("Tripadvisor_hotels.csv", index_col=False)

links = df["Link"]

description_list = []

for index, url in enumerate(links):
    print("N°", index, " , Url: ", url)
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    try:
        desc = soup.find("div", {"class": "cPQsENeY"})
        desc = desc.text
        print("Description : ", desc, "\n")
        description_list.append(desc)
    except:
        print("Erreur: pas de description !")
        description_list.append("-")

print(description_list)

df["Description"] = description_list
df.to_csv("Trip_hotels_desc.csv", index=False)
print(df.head())
