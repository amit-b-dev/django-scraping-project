import requests,traceback,re
from .parser import Extractor
from .navigation import NavigationFlow

class KarnatakaHighCourtJudgements:
    def __init__(self):
        self.session = requests.Session()
        self.extract = Extractor(self.session)
        self.flow = NavigationFlow(self.session)

    def getCaseDetails(self,bench_code, case_code, case_no, case_year):
        try:

            for i in range(10):
                res, cookies = self.flow.loadHomePage()
                actual_bench_code = self.extract.getBenchTypeCode(res, bench_code)
                actual_case_code = self.extract.getCaseTypeCode(res, case_code)

                if not all([actual_bench_code, actual_case_code]):
                    return {"applications": [], "message": "you are enter wrong case code or bench code"}

                captcha_text,captcha_path,captcha_dir = self.flow.getCaptchaImageAndSolver(cookies,res)
                res = self.flow.verifyAndGetChallanDetails(cookies, actual_bench_code, actual_case_code, case_no,case_year, captcha_text, captcha_path, captcha_dir)
                print(f'No of Attempts for captcha solving: {i+1}')
                if res.text=='2':
                    print('captcha is invalid! retry captcha....')
                    continue
                print('captcha crack')
                break

            case_details = self.extract.fetchChallanDetails(res)
            if case_details == "case details are not available":
                return {"applications": [], "message": "case details are not available"}
            
            return {"applications":case_details}

        except:
            traceback.print_exc()
            return {"applications":[]}
        

    def getBenchtypesList(self):
        try:
            res, cookies = self.flow.loadHomePage()
            bench_code_list = self.extract.benchTypes(res)

            return {"applications":bench_code_list}
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




