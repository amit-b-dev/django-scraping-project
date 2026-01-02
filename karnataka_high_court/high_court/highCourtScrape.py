import requests,traceback,re
from .parser import Extractor
from .navigation import NavigationFlow

class MPChallan:
    def __init__(self):
        self.session = requests.Session()
        self.extract = Extractor(self.session)
        self.flow = NavigationFlow(self.session)

    def getCaseDetails(self,bench_name, case_type, case_no, case_year):
        try:

            for i in range(10):
                res, cookies = self.flow.loadHomePage()
                bench_code, case_code = self.extract.selectCode(bench_name, case_type)
                captcha_text,captcha_path,captcha_dir = self.flow.getCaptchaImageAndSolver(cookies,res)
                res = self.flow.verifyAndGetChallanDetails(cookies, bench_code, case_code, case_no,case_year, captcha_text, captcha_path, captcha_dir)
                print(f'No of Attempts for captcha solving: {i+1}')
                if res.text=='2':
                    print('captcha is invalid! retry captcha....')
                    continue
                print('captcha crack')
                break
            case_details = self.extract.fetchChallanDetails(res)
            
            return {"applications":case_details}

        except:
            traceback.print_exc()
            return {"applications":[]}



