import os
from .headers import HeaderHelper
from .captcha import CaptchaSolver
import time
from bs4 import BeautifulSoup

class NavigationFlow:

    def __init__(self, session):
        self.session = session
        self.solver = CaptchaSolver()
    
    def loadHomePage(self):
        url = "https://echallan.jhpolice.gov.in/payment/payonline"
        res = self.session.get(url)
        time.sleep(0.2)
        cookies = self.session.cookies.get_dict()
        
        return res,cookies
    
    def searchChallanDetails(self,vehicle_no,cookies,res):

        soup = BeautifulSoup(res.text,'html.parser')
        captcha_text = soup.find(class_="col-sm-1").find(class_="input-group").get_text(strip=True)

        headers,payload = HeaderHelper.searchChallanDetails_header(vehicle_no,captcha_text)
        url="https://echallan.jhpolice.gov.in/payment/payonline/search_challan"
        res = self.session.post(url,headers=headers, data=payload, cookies=cookies)

        return res