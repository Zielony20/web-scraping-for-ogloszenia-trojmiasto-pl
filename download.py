from bs4 import BeautifulSoup
import requests
import pandas as pd
from time import sleep
d={'hause_name':[],
'price':[],
'price_for_meter':[],
'area':[],
'link':[]}
New_houses = []


new_pages = True
page_num = 0
while(new_pages):
    sleep(1)
    page_url = "https://ogloszenia.trojmiasto.pl/nieruchomosci-rynek-wtorny/?strona="+str(page_num)
    print(page_url)
    print(len(New_houses))
    page_num+=1
    if(page_num==500):
        new_pages=False
    page = requests.get(page_url)
    soup = BeautifulSoup(page.content, 'html.parser')

    homes = soup.find_all("div", {"class": "list__item__wrap__content"})

    #list__item__wrap__content
    #class="list__item list--item--premium list--item--withPrice"
    #list__item__content__title__name link
    #list__item__details__icons__element details--icons--element--powierzchnia
    #list__item__details__icons__element details--icons--element--l_pokoi
    #list__item__details__icons__element details--icons--element--pietro
    #list__item__details__icons__element__desc
    #p list__item__price__value
    #p list__item__details__info details--info--price
    #print(homes)

    #print(list_all[2].get_text())
    for home in homes:

        try:
            home_name = home.find("a", {"class": "list__item__content__title__name link"})
            link=home_name["href"]
            home_name=home_name.get_text()
        except(TypeError, AttributeError):
            home_name = ''
            link = ''
        try:    
            price = home.find("p", {"class": "list__item__price__value"}).get_text()
        except(TypeError, AttributeError):
            price=''
        try:
            price_per_meter=home.find("p", {"class": "list__item__details__info details--info--price"}).get_text()
        except(TypeError, AttributeError):
            price_per_meter=''
        try:
            space = home.find("li", {"class": "list__item__details__icons__element details--icons--element--powierzchnia"}).find("p", {"class": "list__item__details__icons__element__desc"}).get_text()
        except(TypeError, AttributeError):
            space=''

    #    rooms = home.find("li", {"class": "list__item__details__icons__element details--icons--element--l_pokoi"}).find("p", {"class": "list__item__details__icons__element__desc"})
    #    floor = home.find("li", {"class": "list__item__details__icons__element details--icons--element--pietro"}).find("p", {"class": "list__item__details__icons__element__desc"})

        #print("Nazwa:",home_name)
        #print("Cena:",price.get_text())
        #print("Cena za metr:",price_per_meter.get_text())
        #print("Powierzchnia:",space.get_text())
        #print("Link:",link)

        New_house = {'hause_name':home_name,
        'price':price,
        'price_for_meter':price_per_meter,
        'area':space,
        'link':link}
        print(New_house)

        New_houses.append(New_house)
        
    #    print("Pokoje:",rooms.get_text())
    #    print("Piętro:",floor.get_text())
    #    print("---------------------------------")
    #print(page.content)
New_houses = pd.DataFrame(New_houses)
print(New_houses)
New_houses.to_csv("MieszkaniaGdańsk.csv")

