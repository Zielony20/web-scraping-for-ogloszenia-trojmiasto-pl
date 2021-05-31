from bs4 import BeautifulSoup
from numpy import add
import requests
import pandas as pd
from time import sleep

class homeObject:
    
    def __init__(self,link):
        self.page_url = link

        self.page = requests.get(self.page_url)
        soup = BeautifulSoup(self.page.content, 'html.parser')

        self.Piwnica=False 
        self.Miejsce_parkingowe=False 
        self.Dwupoziomowe=False
        self.Balkon=False
        self.Gaz=False
        self.Sila=False
        self.Aneks_kuchenny=False
        self.Kuchnia=False
        self.Woda=False
        self.Kanalizacja=False


        try:
            address = soup.find('div',{'class':'oglField oglField--address'})  
            address = address.find('div',{'class','oglField__container'})
            address = list(address.strings)
            self.address = repr(address[1])
            
        except(TypeError, AttributeError):
            self.address = ''
           
        try:
            property_type = soup.find('div',{'class':'oglField oglField--rodzaj_nieruchomosci'})  
            self.property_type = property_type.find('span',{'class','oglField__value'}).getText()
            
        except(TypeError, AttributeError):
            self.property_type = ''
        
        try:
            number_floors = soup.find('div',{'class':'oglField oglField--l_pieter'})  
            self.number_floors = number_floors.find('span',{'class','oglField__value'}).getText()
            
        except(TypeError, AttributeError):
            self.number_floors = ''
        
        try:
            building_year = soup.find('div',{'class':'oglField oglField--rok_budowy oglField--icon'})  
            self.building_year = building_year.find('span',{'class','oglField__value'}).getText()
            
        except(TypeError, AttributeError):
            self.number_floors = ''
        
        try:
            heating_type = soup.find('div',{'class':'oglField oglField--typ_ogrzewania'})  
            self.heating_type = heating_type.find('span',{'class','oglField__value'}).getText()
            
        except(TypeError, AttributeError):
            self.heating_type = ''
        
        try:
            price_per_meter = soup.find('div',{'class':'oglField oglField--cena_za_m2'})  
            self.price_per_meter = price_per_meter.find('span',{'class','oglDetailsMoney'}).getText()
            
        except(TypeError, AttributeError):
            self.price_per_meter = ''
        
        try:
            license_number = soup.find('div',{'class':'oglField oglField--nr_licencji_posrednika'})  
            self.license_number = license_number.find('span',{'class','oglField__value'}).getText()
            
        except(TypeError, AttributeError):
            self.license_number = ''

        try:
            area = soup.find('div',{'id':'show-powierzchnia', 'class':'oglField'})  
            self.area = area.find('span',{'class','oglField__value'}).getText()
            
        except(TypeError, AttributeError):
            self.area = ''

        try:
            area2 = soup.find('div',{'id':'show-powierzchnia_dzialki', 'class':'oglField'})  
            self.area2 = area2.find('span',{'class','oglField__value'}).getText()
            
        except(TypeError, AttributeError):
            self.area2 = ''


        try:
            rooms_number = soup.find('div',{'class':'oglField oglField--l_pokoi oglField--icon'})  
            self.rooms_number = rooms_number.find('span',{'class','oglField__value'}).getText()
            
        except(TypeError, AttributeError):
            self.rooms_number = ''


        try:
            price = soup.find('div',{'class':'oglField oglField--cena'})  
            self.price = price.find('span',{'class','oglField__value'}).getText()
            
        except(TypeError, AttributeError):
            self.price = ''

        try:
            additional_text = soup.find('div',{'class':'oglField oglField--array'}) 
            additional_text = additional_text.find_all('li',{'class':'oglFieldList__item'}) 
            for addon in additional_text:
                print(addon.getText())


            #self.additional_text = additional_text.find('span',{'class','oglField__value'}).getText()
            
        except(TypeError, AttributeError):
            self.additional_text = ''


    def getAddress(self):
        return self.address
    def getNumberFloors(self):
        return self.number_floors
    def getPropertyType(self):
        return self.property_type
    def getBuildingYear(self):
        return self.building_year
    def getHeatingType(self):
        return self.heating_type
    def getArea(self):
        return self.area
    def getArea2(self):
        return self.area2
    def getLicenseNumber(self):
        return self.license_number
    def getPricePerMeter(self):
        return self.price_per_meter
    def getRoomsNumber(self):
        return self.rooms_number
    def getPrice(self):
        return self.price



class trojmiastopl:
    def __init__(new_pages=500):

        New_houses = []
        d={'house_name':[],'price':[],'price_for_meter':[],'area':[],'link':[]}

        for page_num in range(new_pages):
            sleep(1)
            page_url = "https://ogloszenia.trojmiasto.pl/nieruchomosci-rynek-wtorny/?strona="+str(page_num)
            
            page = requests.get(page_url)
            soup = BeautifulSoup(page.content, 'html.parser')

            homes = soup.find_all("div", {"class": "list__item__wrap__content"})

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

        DetailsHandler = homeObject(link)

        New_house = {'house_name':home_name,
        'price':price,
        'price_for_meter':price_per_meter,
        'area':space,
        'link':link,
        'address':DetailsHandler.getAddress(),
        'year_of_building':DetailsHandler.BuildingYear(),
        'type_of_heating':DetailsHandler.getHeatingType(),
        'state':'',                 #po remoncie lub przed
        'property_type':DetailsHandler.getPropertyType(),
        'floors':DetailsHandler.getNumberFloors(),
        'basement':'',
        'parking':'',
        'two-level':''
        }

        New_houses.append(New_house)

#dh = homeObject('https://ogloszenia.trojmiasto.pl/nieruchomosci-rynek-wtorny/sloneczne-i-przestrzenne-dwupoziomowe-mieszkanie-ogl64294270.html')
dh = homeObject('https://ogloszenia.trojmiasto.pl/nieruchomosci-rynek-wtorny/urokliwy-dom-w-sercu-miasta-ogl64254904.html')

print(dh.getPricePerMeter())
print(dh.getRoomsNumber())














