import requests,traceback,re
from .parser import Extractor
from .navigation import NavigationFlow


class TelanganaChalan:
    def __init__(self):
        self.base_url = "https://www.karnatakaone.gov.in/#logi"
        self.session = requests.Session()
        self.extract = Extractor(self.session)
        self.flow = NavigationFlow(self.session)

    def getChallanDetails(self,vehicle_no):
        try:
            res, cookies = self.flow.loadHomePage(vehicle_no)
            res = self.flow.loadWelcomeJsp(cookies)
            for _ in range(10):
                res,csrf_token = self.flow.loadCaptcha(cookies)
                res = self.flow.getCaptchaImage(cookies,csrf_token)
                res = self.flow.captchaSolverAndFetchChallanDetails(cookies,res,csrf_token)
                if res.text == "Invalid Captcha":
                    print('captcha is invalid! retry captcha....')
                    continue
                break
            chalan_details = self.extract.extractChallanDetails(res)

            return {"applications":chalan_details}

        except:
            traceback.print_exc()
            return {"applications":[]}



