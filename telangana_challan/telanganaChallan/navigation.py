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
        url="https://echallan.tspolice.gov.in/publicview/"
        res = self.session.get(url)
        time.sleep(0.2)
        soup = BeautifulSoup(res.text, "html.parser")
        cookies = self.session.cookies.get_dict()
        
        return soup,cookies
    
    def loadWelcomeJsp(self,cookies):
        headers = HeaderHelper.loadWelcomeJsp_header()
        url="https://echallan.tspolice.gov.in/publicview/welcome.jsp"
        res = self.session.get(url,headers=headers,cookies=cookies)
        time.sleep(0.2)

        return res
    
    def loadCaptcha(self,cookies):
        headers,params = HeaderHelper.loadCaptcha_header()
        url="https://echallan.tspolice.gov.in/publicview/PendingChallans.do"
        res = self.session.get(url,headers=headers, params=params, cookies=cookies)
        time.sleep(0.2)
        csrf_token = res.text
        return res,csrf_token
    
    def getCaptchaImage(self,cookies,csrf_token):
        headers,params = HeaderHelper.getCaptchaImage_header(csrf_token)
        url="https://echallan.tspolice.gov.in/publicview/GetCaptcha"
        res = self.session.get(url,headers=headers, params=params, cookies=cookies)
        time.sleep(0.2)

        return res
    
    def captchaSolverAndFetchChallanDetails(self,vehicle_no,cookies,res,csrf_token):
        captcha_text,captcha_path,captcha_dir = self.solver.solve(res)
        headers,payloads = HeaderHelper.captchaSolverAndFetchChallanDetails_header(vehicle_no,captcha_text,csrf_token)
        url="https://echallan.tspolice.gov.in/publicview/PendingChallans.do"
        res = self.session.post(url,data=payloads,headers=headers,cookies=cookies)
        if res.text != "Invalid Captcha":
            if os.path.exists(captcha_path):
                os.remove(captcha_path)
            if os.path.isdir(captcha_dir):
                os.rmdir(captcha_dir)

        return res