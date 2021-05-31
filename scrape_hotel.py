from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re
import csv
import math

# Filename
filename = "Tripadvisor_hotels.csv"


# Initialize variables we will use
i = 0
s = 0
results = {}
idList = []
hotelPriceList = []
hotelNoteList = []
hotelTitleList = []
hotelNbrReviewList = []
hotelDestinationList = []
hotelFreeCancelList = []
hotelAddressList = []
hotelLinkList = []
hotelEqpWifiList = []
hotelEqpPoolList = []
hotelEqpClimList = []
url1 = "https://www.tripadvisor.com/Hotels"
cities = {}  # Dictionnary to store the user input


def inputnbr(message):
    while True:
        try:
            city = int(input(message))
        except ValueError:
            print("Not an integer! Try again.")
            continue
        else:
            return city
            break


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
        return r[:find] + repl + r[find+len(sub):]
    return r


# Take user input
nbrCities = inputnbr("How much cities do you want to browse ? ")
for n in range(nbrCities):
    cities["city{0}".format(n)] = input("Enter a city name : ")

# Initialize the navigator
driver = webdriver.Chrome(executable_path='/usr/local/bin/chromedriver')
driver.maximize_window()

# For each city the user entered, do the scrapping
for value in cities.values():
    driver.get(url1)  # Go to tripadvisor/hotels
    acceptBtn = driver.find_elements_by_class_name('evidon-banner-acceptbutton')
    if len(acceptBtn) > 0:
        acceptBtn[0].click()
    searchCity = driver.find_elements_by_class_name('_3qLQ-U8m')[1]  # Search the input section
    searchCity.send_keys(value)
    time.sleep(3)  # Wait for the recommandation to appear
    # Wait for the recommandation to appear and then click on it
    searchCity = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CLASS_NAME, '_1c2ocG0l')))
    searchCity.click()
    time.sleep(10)  # Wait for the page to properly load

    # --  BEGIN SCRAPPING  -- #
    # Get the number of hotels in this page
    nbrHotel = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CLASS_NAME, '_3nOjB60a')))
    nbrHotel = nbrHotel.text
    nbrHotel = re.sub("[^0-9]", "", nbrHotel)  # Get only the numbers
    print("Number of hotels : " + nbrHotel + " at " + value)
    nbrHotel = float(nbrHotel)/30  # Divide by the number of hotels in a page
    nbrHotel = math.ceil(nbrHotel)  # Take the superior round
    nbrHotel = int(nbrHotel)  # Convert in Integer
    print("Number of pages : " + str(nbrHotel))

    for i in range(nbrHotel):

        # Get the url for each page
        nbrHotels = '-'+'oa' + str(i * 30)+'-'
        currentUrl = driver.current_url
        outputUrl = nth_repl(currentUrl, "-", nbrHotels, 2)
        driver.get(outputUrl)
        time.sleep(10)
        # Get the element we are looking for
        boxes = driver.find_elements_by_class_name("prw_rup.prw_meta_hsx_responsive_listing.ui_section.listItem")

        # Get data from each box
        for item in boxes:

            # ID
            s += 1  # Increment ID
            idList.append(s)
            print("Hotel N° : " + str(s))

            # Hotel Name
            hotelName = WebDriverWait(item, 50).until(
                EC.presence_of_element_located((By.CLASS_NAME, "property_title.prominent")))
            hotelTitle = hotelName.text
            hotelTitle = hotelTitle.lstrip()  # Remove spaces before the first character
            hotelTitle = hotelTitle.rstrip()
            hotelTitleList.append(hotelTitle)
            print(hotelTitle)

            # Hotel Url
            hotelLink = driver.find_element_by_link_text(str(hotelTitle)).get_attribute("href")
            hotelLinkList.append(hotelLink)

            # Hotel price
            testPrice = item.find_elements_by_class_name("price-wrap")
            if not testPrice:
                hotelPrice = 'Unknown'
            else:
                hotelPrice = item.find_element_by_class_name("price-wrap")
                hotelPrice = hotelPrice.text
                hotelPrice = re.sub("[^0-9]", "", hotelPrice)
                if hotelPrice == '':
                    hotelPrice = 'Unknown'
            hotelPriceList.append(hotelPrice)

            # Hotel Review
            hotelNbrReview = item.find_element_by_class_name("review_count")
            hotelNbrReview = hotelNbrReview.text
            hotelNbrReview = re.sub("[^0-9]", "", hotelNbrReview)
            hotelNbrReviewList.append(hotelNbrReview)

            # Hotel Note
            if int(hotelNbrReview) == 0:
                hotelNote = '0'
            else:
                hotelNote = item.find_element_by_css_selector("a[class^='ui_bubble']")
                hotelNote = hotelNote.get_attribute("alt")
                hotelNote = re.sub("[^0-9]", "", hotelNote)
                hotelNote = hotelNote[:-1]  # Remove the last character (sur 5)
                # if the number has a " , "
                if len(hotelNote) == 2:
                    hotelNote = hotelNote[:1] + '.' + hotelNote[1:]  # Add a . between the numbers to make it decimal
            hotelNoteList.append(hotelNote)

            # # Hotel Free Cancel
            # testFreeCancel = item.find_elements_by_class_name("message.large_message")
            # if not testFreeCancel:
            #     hotelFreeCancel = False
            # else:
            #     hotelFreeCancel = True
            # hotelFreeCancelList.append(hotelFreeCancel)

            # Hotel Destination
            hotelDestinationList.append(value.capitalize())
# --  END SCRAPPING -- #

# Loop in the link list to get the url for each hotel
# for z in hotelLinkList:
#     if z is not None:
#         # Go to the url
#         driver.get(z)
#
#         # Get the adress
#         hotelAddress = driver.find_element_by_class_name("vEwHDg4B._1WEIRhGY")
#         hotelAddress = hotelAddress.text
#         hotelAddressList.append(hotelAddress)
#
#         # Get the features
#         hotelEquipments = driver.find_elements_by_class_name("_2rdvbNSg")
#         hotelEqpPool = False
#         hotelEqpWifi = False
#         hotelEqpClim = False
#         for equip in hotelEquipments:
#             if equip.text == "Piscine":
#                 hotelEqpPool = True
#             if equip.text == "Internet haut débit gratuit (Wi-Fi)":
#                 hotelEqpWifi = True
#             if equip.text == "Climatisation":
#                 hotelEqpClim = True
#         hotelEqpPoolList.append(hotelEqpPool)
#         hotelEqpWifiList.append(hotelEqpWifi)
#         hotelEqpClimList.append(hotelEqpClim)

# Add the lists in the dictionnary used to fill the CSV
results["ID"] = idList
results["Name"] = hotelTitleList
results["Link"] = hotelLinkList
results["Price"] = hotelPriceList
results["Note"] = hotelNoteList
results["NbrReview"] = hotelNbrReviewList
results["Destination"] = hotelDestinationList
# results["Address"] = hotelAddressList
# results["Free Cancel"] = hotelFreeCancelList
# results["Wifi"] = hotelEqpWifiList
# results["Pool"] = hotelEqpPoolList
# results["Clim"] = hotelEqpClimList

# Open and write in the csv file
with open(filename, 'a', encoding='utf-8') as file:
    writer = csv.writer(file, delimiter=',')
    # writer.writerow(results.keys())  # create keys(column) for each list in results
    writer.writerows(zip(*results.values()))  # create values(rows) for each list in results

# Close navigator and the file
driver.close()
file.close()
