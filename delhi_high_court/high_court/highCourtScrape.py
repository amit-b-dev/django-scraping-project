import requests,traceback,re
from .parser import Extractor
from .navigation import NavigationFlow

class HcDelhi:
    def __init__(self):
        self.session = requests.Session()
        self.extract = Extractor(self.session)
        self.flow = NavigationFlow(self.session)

    def getCaseDetails(self, case_type, case_no, case_year):
        try:
            res, cookies = self.flow.loadHomePage()
            case_code, captcha_text, _token = self.extract.selectCodeAndGetCaptchText(res, case_type)

            res = self.flow.verifyAndGetChallanDetails(cookies, case_code, case_no,case_year, captcha_text,_token)
            case_details = self.extract.fetchChallanDetails(res)
            
            return {"applications":case_details}

        except:
            traceback.print_exc()
            return {"applications":[]}



