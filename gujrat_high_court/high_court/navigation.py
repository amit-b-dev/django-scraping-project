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
        url = "https://gujarathc-casestatus.nic.in/gujarathc/"
        res = self.session.get(url)
        time.sleep(0.2)
        # soup = BeautifulSoup(res.text, "html.parser")
        res = self.session.post("https://gujarathc-casestatus.nic.in/gujarathc/ui-pages/caseDetails.jsp")

        cookies = self.session.cookies.get_dict()
        
        return res,cookies

    def loadCaseTypeData(self,res):
        res = self.session.post("https://gujarathc-casestatus.nic.in/gujarathc/GetCaseTypeDataOnLoad")
        return res
    
    def getCaptchaImageAndSolver(self,cookies,res):
        headers,params = HeaderHelper.getCaptchaImage_header()
        url="https://gujarathc-casestatus.nic.in/gujarathc/CaptchaServlet"
        res = self.session.get(url,headers=headers, params=params, cookies=cookies)
        captcha_text,captcha_path,captcha_dir = self.solver.solve(res)
        print("captcha_text=",captcha_text)

        # if res.text != "Invalid Captcha":
        #     if os.path.exists(captcha_path):
        #         os.remove(captcha_path)
        #     if os.path.isdir(captcha_dir):
        #         os.rmdir(captcha_dir)

        return captcha_text,captcha_path,captcha_dir
    
    def verifyAndGetChallanDetails(self,cookies, case_mode, case_type, case_no, case_year, captcha_text, captcha_path, captcha_dir):
        # caseMode="R"
        # caseType="1"
        # year="1994"
        # ccin = caseMode+"#"+caseType+"#"+case_no+"#"+year
        headers,payload = HeaderHelper.verifyAndGetChallanDetails_header(captcha_text,case_mode, case_type, case_no, case_year)

        res = self.session.post("https://gujarathc-casestatus.nic.in/gujarathc/GetData", headers=headers,data=payload, cookies=cookies)
        if "Invalid Captcha" not in res.text:
            if os.path.exists(captcha_path):
                os.remove(captcha_path)
            if os.path.isdir(captcha_dir):
                os.rmdir(captcha_dir)
                
        return res