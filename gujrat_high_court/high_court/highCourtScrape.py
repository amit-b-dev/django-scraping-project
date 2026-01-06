import requests,traceback,re
from .parser import Extractor
from .navigation import NavigationFlow

class GujratHighCourt:
    def __init__(self):
        self.session = requests.Session()
        self.extract = Extractor(self.session)
        self.flow = NavigationFlow(self.session)

    def getCaseDetails(self,case_no):
        try:

            for i in range(10):
                res, cookies = self.flow.loadHomePage()
                captcha_text,captcha_path,captcha_dir = self.flow.getCaptchaImageAndSolver(cookies,res)
                res = self.flow.verifyAndGetChallanDetails(cookies, case_no, captcha_text, captcha_path, captcha_dir)
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



