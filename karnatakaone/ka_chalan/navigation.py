import os,re
from bs4 import BeautifulSoup
from .headers import HeaderHelper
import time

class NavigationFlow:

    def __init__(self, session):
        self.session = session
    
    def load_home_page(self, url):
        res = self.session.get(url)
        cookies = self.session.cookies.get_dict()
        
        return cookies

    def guestLoginWithOutMob(self,cookies):
        headers = HeaderHelper.guestLoginWithOutMob_header()
        res = self.session.get("https://www.karnatakaone.gov.in/Home/GuestLoginWithOutMob",headers=headers,cookies=cookies)
        time.sleep(0.2)
        cookies = self.session.cookies.get_dict()

        return res,cookies
    
    def showCityList(self,cookies):
        headers = HeaderHelper.showCityList_header()
        res = self.session.get("https://www.karnatakaone.gov.in/PortalHome/ShowCityList",headers=headers,cookies=cookies)
        time.sleep(0.2)
        cookies = self.session.cookies.get_dict()

        return res,cookies
    
    def selectCity(self,cookies):
        headers = HeaderHelper.selectCity_header()
        res = self.session.get("https://www.karnatakaone.gov.in/PortalHome/Index/Bengaluru",headers=headers,cookies=cookies)
        time.sleep(0.2)
        # cookies = self.session.cookies.get_dict()
        # soup=BeautifulSoup(res.text,"html.parser")

        return res
    
    def serviceList(self,cookies):
        headers = HeaderHelper.serviceList_header()
        res = self.session.get("https://www.karnatakaone.gov.in/PortalHome/ServiceList",headers=headers,cookies=cookies)
        time.sleep(0.2)
        # soup=BeautifulSoup(res.text,"html.parser")
        # cookies = self.session.cookies.get_dict()

        return res

    def selectPoliceFineUrl(self,cookies,PoliceCollectionOfFine_url):
        headers = HeaderHelper.selectPoliceCollectionFine_header()
        res = self.session.get(PoliceCollectionOfFine_url,headers=headers,cookies=cookies)
        time.sleep(0.2)
        # soup=BeautifulSoup(res.text,"html.parser")
        # cookies = self.session.cookies.get_dict()

        return res

    def sendOTP(self,cookies,PoliceCollectionOfFine_url,params):
        headers = HeaderHelper.sendOTP_header(PoliceCollectionOfFine_url)
        res = self.session.get("https://www.karnatakaone.gov.in/PoliceCollectionOfFine/SendOTP",headers=headers,cookies=cookies,params=params)
        time.sleep(0.2)
        # soup=BeautifulSoup(res.text,"html.parser")
        # cookies = self.session.cookies.get_dict()

        return res

    def validateOTP(self,cookies,PoliceCollectionOfFine_url,params):
        headers = HeaderHelper.otpValidation_header(PoliceCollectionOfFine_url)
        res = self.session.get("https://www.karnatakaone.gov.in/PoliceCollectionOfFine/ValidateOTP",headers=headers,cookies=cookies,params=params)
        time.sleep(0.2)
        # soup=BeautifulSoup(res.text,"html.parser")
        # cookies = self.session.cookies.get_dict()

        return res

    def policeFineDetailsPage(self,cookies,PoliceCollectionOfFine_url,nexttonext_requests):
        headers,payloads = HeaderHelper.PoliceFineDetails_header(PoliceCollectionOfFine_url,nexttonext_requests)
        res = self.session.post("https://www.karnatakaone.gov.in/PoliceCollectionOfFine/PoliceCollectionOfFineLogin",headers=headers,data=payloads,cookies=cookies)
        time.sleep(0.2)
        res = self.session.post("https://www.karnatakaone.gov.in/PoliceCollectionOfFine/PoliceCollectionOfFineLogin",headers=headers,data=payloads,cookies=cookies)
        time.sleep(0.2)

        # soup=BeautifulSoup(res.text,"html.parser")
        # cookies = self.session.cookies.get_dict()

        return res

    def getAllChalanDetails(self,cookies,params,token):
        headers = HeaderHelper.searchRegNoWise_header(token)
        res = self.session.post("https://www.karnatakaone.gov.in/PoliceCollectionOfFine/PoliceFine_Details",headers=headers,cookies=cookies,params=params)
        time.sleep(0.2)
        # soup=BeautifulSoup(res.text,"html.parser")
        # cookies = self.session.cookies.get_dict()

        return res
