import os
from .headers import HeaderHelper
from .captcha import CaptchaSolver
import time, json, re
from bs4 import BeautifulSoup
from lxml import html

class NavigationFlow:

    def __init__(self, session):
        self.session = session
        self.solver = CaptchaSolver()
    
    def loadHomePage(self):
        url = "https://services.ecourts.gov.in/ecourtindia_v6/"
        res = self.session.get(url)
        time.sleep(0.2)
        cookies = self.session.cookies.get_dict()
        
        return res,cookies
    
    def getCaptchaText(self,res,cookies):

        soup = BeautifulSoup(res.text,'html.parser')
        app_token = soup.find(id="app_token")['value']

        headers,payload = HeaderHelper.getCaptchaText_Header(app_token)
        url="https://services.ecourts.gov.in/ecourtindia_v6/casestatus/getCaptcha"
        res = self.session.post(url, headers=headers, data=payload, cookies=cookies)
        j = res.json()
        app_token = j.get("app_token")
        html = j["div_captcha"]
        img_path = re.search(r'src="([^"]+)"', html).group(1)
        img_url = "https://services.ecourts.gov.in/" + img_path
        res = self.session.get(img_url, headers=headers)
        captcha_text,captcha_path,captcha_dir = self.solver.solve(res)

        return app_token,captcha_text
    
 
    def getCaseDetailsPage(self,cookies,cnr_no,captcha_text,app_token):

        headers,payload = HeaderHelper.getCaseDetailsPage_Header(cnr_no,captcha_text,app_token)
        url="https://services.ecourts.gov.in/ecourtindia_v6/cnr_status/searchByCNR/"
        res = self.session.post(url, headers=headers, data=payload, cookies=cookies)

        return res