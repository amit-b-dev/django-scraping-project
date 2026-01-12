import requests,traceback
from .parser import Extractor
from .navigation import NavigationFlow

class hcMadrasJudgements:
    def __init__(self):
        self.session = requests.Session()
        self.flow = NavigationFlow(self.session)
        self.extract = Extractor(self.session)

    def getCaseDetails(self, case_code, case_no, case_year):
        try:
            for i in range(5):
                res, cookies = self.flow.loadHomePage()
                actual_case_code = self.extract.getCaseTypeCode(res, case_code)
                if not actual_case_code:
                    return {"applications": [], "message": "you are enter wrong case code"}
                captcha_text = self.flow.getCaptchText(res,cookies)
                res = self.flow.getCaseDetails(cookies, actual_case_code, case_no,case_year, captcha_text)
                if "Captcha not matching" in res.text:
                    print(f"Attempt {i+1}: captcha incorrect, retrying...")
                    continue
                break

            case_details = self.extract.fetchCaseDetails(res)
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
