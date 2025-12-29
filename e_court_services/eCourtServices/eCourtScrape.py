import requests,traceback,re
from .parser import Extractor
from .navigation import NavigationFlow


class ECourtServices:
    def __init__(self):
        self.session = requests.Session()
        self.extract = Extractor(self.session)
        self.flow = NavigationFlow(self.session)

    def getCaseDetails(self,cnr_no):
        try:
            res, cookies = self.flow.loadHomePage()
            app_token,captcha_text = self.flow.getCaptchaText(res,cookies)
            res = self.flow.getCaseDetailsPage(cookies,cnr_no,captcha_text,app_token)
            chalan_details = self.extract.fetchCaseDetails(res,cookies)

            return {"applications":chalan_details}

        except:
            traceback.print_exc()
            return {"applications":[]}



