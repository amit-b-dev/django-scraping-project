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
        url = "https://echallan.mponline.gov.in/"
        res = self.session.get(url)
        time.sleep(0.2)
        # soup = BeautifulSoup(res.text, "html.parser")
        cookies = self.session.cookies.get_dict()
        
        return res,cookies
    
    def getCaptchaImageAndSolver(self,cookies,res):
        headers = HeaderHelper.getCaptchaImageAndSolver_header()
        url="https://echallan.mponline.gov.in/new-captcha"
        res = self.session.get(url,headers=headers,cookies=cookies)
        captcha_text,captcha_path,captcha_dir = self.solver.solve(res)
        print("captcha_text=",captcha_text)

        # if res.text != "Invalid Captcha":
        #     if os.path.exists(captcha_path):
        #         os.remove(captcha_path)
        #     if os.path.isdir(captcha_dir):
        #         os.rmdir(captcha_dir)

        return captcha_text,captcha_path,captcha_dir
    
    def verifyAndGetChallanDetails(self,vehicle_no,cookies,captcha_text,captcha_path,captcha_dir):
        csrf_token = cookies['csrf_cookie']
        headers,files = HeaderHelper.verifyAndGetChallanDetails_header(vehicle_no, captcha_text, csrf_token)

        res = self.session.post("https://echallan.mponline.gov.in/api/get-challans-details",headers=headers,files=files)
        if "Invalid Captcha Text" not in res.text:
            if os.path.exists(captcha_path):
                os.remove(captcha_path)
            if os.path.isdir(captcha_dir):
                os.rmdir(captcha_dir)
        return res