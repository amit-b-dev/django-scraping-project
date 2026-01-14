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
        url = "https://ksat.karnataka.gov.in/ksatweb/public/getcasestatus"
        res = self.session.get(url)
        time.sleep(0.2)
        # soup = BeautifulSoup(res.text, "html.parser")
        cookies = self.session.cookies.get_dict()
        
        return res,cookies
    
    def getCaptchaImageAndSolver(self,cookies,res):
        headers,params = HeaderHelper.getCaptchaImage_header()
        url="https://judiciary.karnataka.gov.in/captcha.php"
        res = self.session.get(url,headers=headers, params=params, cookies=cookies)
        captcha_text,captcha_path,captcha_dir = self.solver.solve(res)
        print("captcha_text=",captcha_text)

        # if res.text != "Invalid Captcha":
        #     if os.path.exists(captcha_path):
        #         os.remove(captcha_path)
        #     if os.path.isdir(captcha_dir):
        #         os.rmdir(captcha_dir)

        return captcha_text,captcha_path,captcha_dir
    
    def verifyAndGetChallanDetails(self,cookies, actual_bench_code, actual_case_code, case_no,case_year, captcha_text, captcha_path, captcha_dir):
        headers,payload = HeaderHelper.verifyAndGetChallanDetails_header(actual_bench_code, actual_case_code, case_no, case_year, captcha_text)
        res = self.session.post("https://judiciary.karnataka.gov.in/rep_judgment_detailscasebc.php", headers=headers,data=payload, cookies=cookies)
        if res.text!="2":
            if os.path.exists(captcha_path):
                os.remove(captcha_path)
            if os.path.isdir(captcha_dir):
                os.rmdir(captcha_dir)
                
        return res