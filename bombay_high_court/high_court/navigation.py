import json
import os
from .headers import HeaderHelper
import time
from bs4 import BeautifulSoup

class NavigationFlow:

    def __init__(self, session):
        self.session = session
    
    def loadHomePage(self):
        url = "https://bombayhighcourt.nic.in/"
        res = self.session.get(url)
        time.sleep(0.2)
        cookies = self.session.cookies.get_dict()
        
        return res,cookies
    
    def loadIndexPage(self):
        headers = HeaderHelper.loadIndexPage_header()
        url = "https://bombayhighcourt.nic.in/index.php"
        res = self.session.get(url, headers=headers)
        time.sleep(0.2)
        
        return res
    
    def loadCaseNoWise(self):
        headers = HeaderHelper.loadCaseNoWise_header()
        url="https://bombayhighcourt.nic.in/ord_qrywebcase.php"
        res = self.session.get(url,headers=headers)
        time.sleep(0.2)
        soup = BeautifulSoup(res.text,'html.parser')
        CSRFName = soup.find("input",{"name":'CSRFName'})['value']
        CSRFToken = soup.find("input",{"name":'CSRFToken'})['value']
        return CSRFName,CSRFToken
    
    def getCaptchaText(self):
        headers = HeaderHelper.getCaptchaText_header()
        res = self.session.get("https://bombayhighcourt.nic.in/bhccaptcha/getcaptest.php", headers=headers)
        time.sleep(0.2)
        cap_code_res1 = json.loads(res.text)
        captcha_text = cap_code_res1['code'].lower()

        return captcha_text
    
    def loadCaseDetails(self, Case_No, CSRFName, CSRFToken,captcha_text):
        headers,payload = HeaderHelper.loadCaseDetails_header(Case_No,CSRFName, CSRFToken,captcha_text)
        url = "https://bombayhighcourt.nic.in/ordqrywebcase_action.php"
        res = self.session.post(url,data=payload,headers=headers)
        time.sleep(0.2)
        return res