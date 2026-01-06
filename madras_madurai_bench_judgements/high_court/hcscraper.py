import requests,traceback
from .parser import Extractor
from .navigation import NavigationFlow

class hcMadrasMaduraiBenchJudgements:
    def __init__(self):
        self.session = requests.Session()
        self.flow = NavigationFlow(self.session)
        self.extract = Extractor(self.session)


    def getCaseDetails(self, case_type, case_no, case_year):
        try:
            for i in range(5):
                res, cookies = self.flow.loadHomePage()
                case_code = self.extract.getCaseTypeCode(res, case_type)
                captcha_text,captcha_path,captcha_dir = self.flow.getCaptchText(res,cookies)
                res = self.flow.getCaseDetails(cookies, case_code, case_no,case_year, captcha_text,captcha_path,captcha_dir)
                if "Captcha not matching" in res.text:
                    print(f"Attempt {i+1}: captcha incorrect, retrying...")
                    continue
                break

            case_details = self.extract.fetchCaseDetails(res)
            
            return {"applications":case_details}
        except:
            traceback.print_exc()
            return {"applications":[]}

