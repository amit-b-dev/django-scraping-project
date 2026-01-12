import requests,traceback
from .parser import Extractor
from .navigation import NavigationFlow

class HcCulculttaAppellateSide:
    def __init__(self):
        self.session = requests.Session()
        self.flow = NavigationFlow(self.session)
        self.extract = Extractor(self.session)

    def getCaseDetails(self, case_code, case_no, case_year, court_code):
        try:
            for i in range(5):
                res, cookies = self.flow.loadHomePage(court_code)
                actual_case_code = self.flow.getCaseTypeCode(court_code,case_code)
                if not actual_case_code:
                    return {"applications": [], "message": "you are enter wrong case code"}
                captcha_text,captcha_path,captcha_dir = self.flow.getCaptchText(res,cookies)
                res = self.flow.varifyCaptchaAndDetails(cookies, court_code, actual_case_code, case_no,case_year, captcha_text,captcha_path,captcha_dir)
                if "Captcha not matching" in res.text:
                    print(f"Attempt {i+1}: captcha incorrect, retrying...")
                    continue
                break
            case_no1,cino,token, check = self.extract.payloadData(res)
            if not check:
                res = self.flow.oCivilCaseHistory(court_code, case_no1, cino, token)
                case_details = self.extract.fetchCaseDetails(res)
            else:
                case_details = check
            if case_details == "case details are not available":
                return {"applications": [], "message": "case details are not available"}
            
            return {"applications":case_details}
        except:
            traceback.print_exc()
            return {"applications":[]}

    def get_case_types_list(self, court_code):
        try:
            res, cookies = self.flow.loadHomePage(court_code)
            case_types = self.flow.getCasetypesList(court_code)
            return {"applications":case_types}
        except:
            return {"applications":[]}
