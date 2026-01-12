import os
from .headers import HeaderHelper
import time
from bs4 import BeautifulSoup

class NavigationFlow:

    def __init__(self, session):
        self.session = session
    
    def loadHomePage(self):
        url = "https://delhihighcourt.nic.in/app/case-number"
        res = self.session.get(url)
        time.sleep(0.2)
        cookies = self.session.cookies.get_dict()
        
        return res,cookies

    def verifyAndGetChallanDetails(self,cookies, case_code, case_no,case_year, captcha_text, _token):
        headers,payload = HeaderHelper.verifyAndGetChallanDetails_header(case_code, case_no, case_year, captcha_text, _token)
        res = self.session.post("https://delhihighcourt.nic.in/app/case-number", headers=headers,data=payload, cookies=cookies)
                
        return res
    
