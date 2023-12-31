from bs4 import BeautifulSoup as soup

from urllib.request import urlopen as ureq

from matplotlib import pyplot as plt

from matplotlib import dates as m_dates

import numpy as np

import plotting as plot

from datetime import date, timedelta  

import requests

import pandas as pd

ini = date(2020,2,15)  

class CovidData():

    def __init__(self,country) -> None:

        self.myurl="https://www.worldometers.info/coronavirus/country/{}/".format(country.lower())#can accept any country name
        self.response=requests.get(self.myurl)#gets the page data
        
        if self.response.url=="https://www.worldometers.info/404.shtml":#404 error
            
            raise(Exception("Invalid country name"))#404 means no such country exists
            
        self.pagehtml=self.response.text#actual contents of website
        self.response.close()#close connection
        self.pagesoup = soup(self.pagehtml,"lxml")#Beautiful soup syntax
        self.body = self.pagesoup.body#find first body tag
        self.finddiv=self.body.find_all("div",{"class":"maincounter-number"})#find all div inside body with class=maincounter-number
        self.forgraphs=self.body.find_all("div",{"class":"col-md-12"})#find all divs with that particular class

    
        

    def last_update(self):#returns string
        lastupdate=self.body.find("div",{"style":"font-size:13px; color:#999; text-align:center"})
        return lastupdate.string

    def total_cases(self):#return string of total cases up till now
        totalcases=self.finddiv[0]
        return totalcases.span.string

    def deaths(self):#return string of total deaths up till now
        deaths=self.finddiv[1]
        return deaths.span.string

    def recovered(self):#return string of total recoveries up till now
        recovered=self.finddiv[2]
        return recovered.span.string

    def getdata(self,n):#finds list of data points using string manipuation

        script=self.forgraphs[n].find("script")

        datastart=str(script).find("data")

        findbrackets1=str(script)[datastart:].find("[")
        findbrackets2=str(script)[datastart:].find("]")

        datastr=str(script)[datastart:][findbrackets1+1:findbrackets2]
        data=[int(i) for i in datastr.split(",") if i !="null" and i!=""]#exclude those values with null ""
        return data

    def total_case_data(self):#returns a list of total cases per day(cumulative)
        # script=forgraphs[0].find("script")

        return self.getdata(0)

    def daily_new_case_data(self):

        return self.getdata(1)

    def active_case_data(self):

        return self.getdata(2)
    
    def deaths_data(self):

        return self.getdata(3)


class Population:

    def __init__(self,country) -> None:

        self.country=country.lower().title()

        self.pop_df = pd.read_csv("population_by_country_2020.csv")
        # Taken from https://www.kaggle.com/tanuprabhu/population-by-country-2020
    
    def get_population(self):

        try:

            pop= self.pop_df.loc[self.pop_df["Country (or dependency)"]==self.country]
            return int(pop["Population (2020)"])

        except:

            raise(Exception("Invalid country name"))

        


if __name__=="__main__":

    try:
        print("Enter Country Name: ")
        name = input()
        d1=CovidData(name)
        print(d1.last_update())
        print("Total Coronavirus cases:",d1.total_cases())
        print("Deaths:",d1.deaths())
        print("Recovered:",d1.recovered())
        #print("List of  cumulative cases daywise",d1.total_case_data())
        #print("List of new daily cases:",d1.daily_new_case_data())
        #print("List of active cases daywise:",d1.active_case_data())
        #print("List of  cumulative deaths daywise:",d1.deaths_data())
        print("Enter:\n1 - Cumlative cases Daywise\n2 - New Daily Cases\n3 - Active Cases\n4 - Deaths")
        i = int(input(""))
        print("Enter the color of the graph\nr - red\no - orange\ny - yellow\nb - blue\ng - green")
        c = str(input())
        if (i == 1):
            plot.plotweb(list(d1.total_case_data),name,c)
        elif (i == 2):
            plot.plotweb(list(d1.daily_new_case_data()),name,c)
        elif (i == 3):
            plot.plotweb(list(d1.active_case_data()),name,c)
        elif (i == 4):
            plot.plotweb(list(d1.deaths_data()),name,c)

        
    except Exception as t:
        print(t)

    try:

        p= Population("finland")
        print(p.get_population())
    except Exception as e:
        print(e)