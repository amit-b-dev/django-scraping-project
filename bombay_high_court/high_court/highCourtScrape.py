import requests,traceback,re
from .parser import Extractor
from .navigation import NavigationFlow

class HcBombay:
    def __init__(self):
        self.session = requests.Session()
        self.extract = Extractor(self.session)
        self.flow = NavigationFlow(self.session)

    def getCaseDetailsByCaseNo(self,Case_No):
        try:
            for _ in range(10):
                res, cookies = self.flow.loadHomePage()
                res = self.flow.loadIndexPage()
                CSRFName,CSRFToken = self.flow.loadCaseNoWise()
                captcha_text = self.flow.getCaptchaText()
                res = self.flow.loadCaseDetails(Case_No, CSRFName, CSRFToken,captcha_text)
                if "File Not Found" in res.text:
                    print("INVALID INPUT")
                    case_details = "INVALID INPUT"
                    continue
                break
            case_details = self.extract.fetchCaseDetails(res)

            return {"applications":case_details}

        except:
            traceback.print_exc()
            return {"applications":[]}



