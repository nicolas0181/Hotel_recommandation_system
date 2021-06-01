from bs4 import BeautifulSoup
import requests
import pandas as pd
import csv
import os
import time
import re

MAX_THREADS = 30


# Print iterations progress bar
def print_progress_bar(iteration, total, prefix='', suffix='', decimals=1, length=100, fill='█', print_end=""):
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + '-' * (length - filled_length)
    print(f'\r{prefix} |{bar}| {percent}% {suffix} {iteration}/{total}', end=print_end)
    # Print New Line on Complete
    if iteration == total:
        print()


def nth_repl(r, sub, repl, nth):
    find = r.find(sub)
    # If find is not -1 we have found at least one match for the substring
    k = find != -1
    # loop util we find the nth or we find no match
    while find != -1 and k != nth:
        # find + 1 means we start searching from after the last match
        find = r.find(sub, find + 1)
        k += 1
    # If k is equal to r we found nth match so replace
    if k == nth:
        return r[:find] + repl + r[find + len(sub):]
    return r


def check_csv_exist(filename):
    if os.path.exists(filename):
        append_write = 'a'  # append if already exists
    else:
        append_write = 'w'  # make a new file if not
    return append_write


def get_city_selection(hotel_df):
    city_selection = hotel_df["Destination"]
    return city_selection


def get_list_cities(city_selection):
    list_cities = city_selection.drop_duplicates()
    list_cities = list_cities.dropna()
    list_cities = list_cities.to_list()
    return list_cities


def ask_city_scrape(list_cities):
    for city in list_cities:
        print(city)
    while True:
        try:
            city_to_scrape = input()
            if city_to_scrape in list_cities:
                print("Vous avez choisi de scrapper : " + city_to_scrape)
                break
            else:
                print("Veuillez choisir une ville de cette liste (sensible à la casse)")
        except ValueError:
            print(ValueError)
    return city_to_scrape


def get_list_link(selection, city, hotel_df, min_review):
    hotel_df_country = hotel_df[selection == city]
    hotel_review = hotel_df_country["NbrReview"]
    hotel_review_country = hotel_df_country[hotel_review > min_review]
    list_link = hotel_review_country["Link"].tolist()
    return list_link


def get_execution_time(start):
    end = time.time()
    duration = round(end - start)
    print("Temps d'execution : " + str(duration) + " secondes")


def scrape_1():

    # Filename to parse
    list_hotel_filename = 'Tripadvisor_hotels.csv'
    # Filename to create
    user_filename = "Tripadvisor_users.csv"

    print(check_csv_exist(user_filename))

    col_list_link = ["ID", "Name", "Link", "NbrReview", "Destination"]
    hotel_df = pd.read_csv(list_hotel_filename, usecols=col_list_link)

    print("Quelle ville souhaitez-vous scrapper parmi ces villes : ")
    time.sleep(1)

    # Ask the user to input the city to scrape
    ask_city = ask_city_scrape(get_list_cities(get_city_selection(hotel_df)))
    city_to_scrape = ask_city
    list_link = get_list_link(get_city_selection(hotel_df), ask_city, hotel_df, min_review=250)
    print("\n")
    print("Préciser le début et la fin (" + str(len(list_link)) + " hôtels disponibles à " + city_to_scrape + ") : ")
    print("Début : ")
    begin = int(input())
    print("Fin : ")
    end = int(input())
    print("\n")
    print("******************************************")
    print("Run sur les hôtels de : " + city_to_scrape)
    print("******************************************")
    print("Vous allez scrapper les hôtels allant de : " + str(begin) + " à " + str(end) + " sur " + str(
        len(list_link)) + ".")
    print("******************************************")
    print("\n")

    hotel_name_list = []
    user_name_list = []
    user_link_list = []
    contribution_nbr_list = []
    note_list = []
    destination_list = []
    title_comment_list = []
    comment_list = []
    results = {}
    nbr_iter = 0


    for k in range(begin, end):
        nbr_iter += 1
        print("- Hôtel n° : " + str(nbr_iter) + " sur " + str(end - begin) + " sur ce run.")
        page = requests.get(list_link[k])
        soup = BeautifulSoup(page.text, 'html.parser')
        page_num = soup.find_all("a", {"class": "pageNum"})
        if len(page_num) > 0:
            page_num = page_num[-1]
            page_num = page_num.text
            page_num = int(page_num)
        else:
            page_num = 1
        nbr_review = page_num * 5
        print(str(nbr_review) + " avis à récupérer pour cette hôtel")

        hotel_name = soup.find("h1", {"class": "_1mTlpMC3"})
        hotel_name = hotel_name.text
        print("Hôtel actuel : " + hotel_name)

        # Initialize Progress Bar
        print_progress_bar(0, page_num - 2, prefix='Progress:', suffix='Complete')

        for i in range(page_num - 1):

            # Update Progress Bar
            print_progress_bar(i, page_num - 2, prefix='Progress:', suffix='Complete')

            # Get the url to parse
            nbr_avis = '-' + 'or' + str(i * 5) + '-'
            output_url = nth_repl(list_link[k], "-", nbr_avis, 2)
            page2 = requests.get(output_url)
            soup2 = BeautifulSoup(page2.text, 'html.parser')

            boxes = soup2.find_all("div", {"class": "_2wrUUKlw _3hFEdNs8"})

            for item in boxes:

                # Hotel and username
                hotel_name_list.append(hotel_name)
                user_name = item.find("a", {"class": "ui_header_link _1r_My98y"})
                user_name = user_name.text
                user_name_list.append(user_name)

                # Link user
                user_link = item.find("a", {"class": "ui_header_link _1r_My98y"})
                user_link = user_link['href']
                user_link = "https://www.tripadvisor.com" + user_link
                user_link_list.append(user_link)

                # Contribution number
                contribution_nbr_test = item.find_all("span", {"class": "_1fk70GUn"})
                if len(contribution_nbr_test) > 0:
                    contribution_nbr = contribution_nbr_test[0].text
                else:
                    contribution_nbr = 1
                contribution_nbr_list.append(contribution_nbr)

                # Note
                note = item.find("span", class_=re.compile("^ui_bubble"))
                note = note['class']
                note = note[1]
                note = re.sub("[^0-9]", "", note)
                note = note[:1] + '.' + note[1:]
                note_list.append(note)

                # Destination
                destination_list.append(ask_city)

                # Comment
                comment = item.find("q", {"class": "IRsGHoPm"})
                comment = comment.text
                comment_list.append(comment)

                # Title
                title = item.find("a", {"class": "ocfR3SKN"})
                title = title.text
                title_comment_list.append(title)

        # Fill the dictionnary with the lists
        results["Hotel_Name"] = hotel_name_list
        results["Username"] = user_name_list
        results["Link"] = user_link_list
        results["Contribution_Number"] = contribution_nbr_list
        results["Note"] = note_list
        results["Destination"] = destination_list
        results["Comment"] = comment_list
        results["Title_Comment"] = title_comment_list

        csv_edit = check_csv_exist(user_filename)
        # Handle file write/append
        with open(user_filename, csv_edit, encoding='utf-8') as file:
            writer = csv.writer(file, delimiter=',')
            if csv_edit == 'w':
                writer.writerow(results.keys()) # create keys(column) for each list in results
            writer.writerows(zip(*results.values()))  # create values(rows) for each list in results
        file.close()


if __name__ == "__main__":

    start_time = time.time()
    scrape_1()
    get_execution_time(start_time)
