import requests,traceback,re
from .parser import Extractor
from .navigation import NavigationFlow

class GujratHighCourt:
    def __init__(self):
        self.session = requests.Session()
        self.extract = Extractor(self.session)
        self.flow = NavigationFlow(self.session)

    def getCaseDetails(self,case_mode_code, case_type_code, case_no, case_year):
        try:

            for i in range(10):
                res, cookies = self.flow.loadHomePage()
                actual_case_mode_code = self.extract.getCaseMode(res,case_mode_code)
                # case_mode = self.extract.getCaseModeData(res)
                res = self.flow.loadCaseTypeData(res)
                actual_case_type_code = self.extract.getCaseCode(res,case_type_code)
                # case_list = self.extract.getCaseTypeData(res)
                captcha_text,captcha_path,captcha_dir = self.flow.getCaptchaImageAndSolver(cookies,res)
                res = self.flow.verifyAndGetChallanDetails(cookies, actual_case_mode_code, actual_case_type_code, case_no, case_year, captcha_text, captcha_path, captcha_dir)
                print(f'No of Attempts for captcha solving: {i+1}')
                if "Invalid Captcha" in res.text:
                    print('captcha is invalid! retry captcha....')
                    continue
                print('captcha crack')
                break
            case_details = self.extract.fetchChallanDetails(res)
            
            return {"applications":case_details}

        except:
            traceback.print_exc()
            return {"applications":[]}
        

    def getBenchtypesList(self):
        try:
            res, cookies = self.flow.loadHomePage()
            case_mode_list = self.extract.getCaseModeData(res)

            return {"applications":case_mode_list}
        except:
            traceback.print_exc()
            return {"applications":[]}
        
    def getCasetypesList(self):
        try:
            res, cookies = self.flow.loadHomePage()
            case_type_list = self.extract.getCaseTypeData(res)

            return {"applications":case_type_list}
        except:
            traceback.print_exc()
            return {"applications":[]}



