import requests,traceback,re
from .parser import Extractor
from .navigation import NavigationFlow


class MPChallan:
    def __init__(self):
        self.session = requests.Session()
        self.extract = Extractor(self.session)
        self.flow = NavigationFlow(self.session)

    def getChallanDetails(self,vehicle_no):
        try:
            for i in range(10):
                res, cookies = self.flow.loadHomePage()
                captcha_text,captcha_path,captcha_dir = self.flow.getCaptchaImageAndSolver(cookies,res)
                res = self.flow.verifyAndGetChallanDetails(vehicle_no,cookies,captcha_text,captcha_path,captcha_dir)
                print(f'No of Attempts for captcha solving: {i+1}')
                if "Invalid Captcha Text" in res.text:
                    print('captcha is invalid! retry captcha....')
                    continue
                print('captcha crack')
                break
            chalan_details = self.extract.fetchChallanDetails(res)
            
            return {"applications":chalan_details}

        except:
            traceback.print_exc()
            return {"applications":[]}



