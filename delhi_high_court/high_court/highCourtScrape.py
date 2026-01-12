import requests,traceback,re
from .parser import Extractor
from .navigation import NavigationFlow

class HcDelhi:
    def __init__(self):
        self.session = requests.Session()
        self.extract = Extractor(self.session)
        self.flow = NavigationFlow(self.session)

    def getCaseDetails(self, case_code, case_no, case_year):
        try:
            res, cookies = self.flow.loadHomePage()
            actual_case_code = self.extract.get_case_code(res, case_code)
            if not actual_case_code:
                return {"applications": [], "message": "you are enter wrong case code"}
            captcha_text, _token = self.extract.GetCaptchText(res)

            res = self.flow.verifyAndGetChallanDetails(cookies, actual_case_code, case_no,case_year, captcha_text,_token)
            case_details = self.extract.fetchChallanDetails(res)
            if case_details == "case details are not available":
                    return {"applications": [], "message": "case details are not available"}
            return {"applications":case_details}

        except:
            traceback.print_exc()
            return {"applications":[]}
        
    def getCasetypesList(self):
        try:
            res, cookies = self.flow.loadHomePage()
            case_code_list = self.extract.caseTypes(res)

            return {"applications":case_code_list}
        except:
            traceback.print_exc()
            return {"applications":[]}
