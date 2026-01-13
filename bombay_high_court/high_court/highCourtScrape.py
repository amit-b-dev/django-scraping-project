import requests,traceback,re
from .parser import Extractor
from .navigation import NavigationFlow

class HcBombay:
    def __init__(self):
        self.session = requests.Session()
        self.extract = Extractor(self.session)
        self.flow = NavigationFlow(self.session)

    def getCaseDetails(self,case_side_code, case_stamp_regno_code, case_type_code, case_no, case_year):
        try:
            print('The Script Is Running.....')
            res, cookies = self.flow.loadHomePage()
            res = self.flow.loadIndexPage()
            CSRFName, CSRFToken, res = self.flow.loadCaseNoWise()
            actual_case_side_code = self.extract.getCaseSideCode(res, case_side_code)
            actual_case_stamp_regno_code = self.extract.getStampAndRegCode(res, case_stamp_regno_code)
            actual_case_type_code = self.extract.getCaseTypeCode(res,case_type_code)

            if not all([actual_case_side_code, actual_case_stamp_regno_code, actual_case_type_code]):
                return {"applications": [], "message": "you are enter wrong input"}

            captcha_text = self.flow.getCaptchaText()
            payload = [actual_case_side_code, actual_case_stamp_regno_code, actual_case_type_code, case_no, case_year]
            
            res = self.flow.loadCaseDetails(payload, CSRFName, CSRFToken, captcha_text)
            if "File Not Found" in res.text:
                return {"applications": [], "message": "you are enter wrong input"}

            case_details = self.extract.fetchCaseDetails(res)
            if case_details == "case details are not available":
                    return {"applications": [], "message": "case details are not available"}

            return {"applications":case_details}

        except:
            traceback.print_exc()
            return {"applications":[]}



    def getCaseSideList(self):
        try:
            res, cookies = self.flow.loadHomePage()
            res = self.flow.loadIndexPage()
            CSRFName, CSRFToken, res = self.flow.loadCaseNoWise()
            case_side_list = self.extract.getCaseSideData(res)

            return {"applications":case_side_list}
        except:
            traceback.print_exc()
            return {"applications":[]}
        
    def getStampAndRegList(self):
        try:
            res, cookies = self.flow.loadHomePage()
            res = self.flow.loadIndexPage()
            CSRFName, CSRFToken, res = self.flow.loadCaseNoWise()
            case_stamp_reg_list = self.extract.getStampAndRegData(res)

            return {"applications":case_stamp_reg_list}
        except:
            traceback.print_exc()
            return {"applications":[]}

    def getCaseTypeList(self):
        try:
            res, cookies = self.flow.loadHomePage()
            res = self.flow.loadIndexPage()
            CSRFName, CSRFToken, res = self.flow.loadCaseNoWise()
            case_type_list = self.extract.getCaseTypeData(res)

            return {"applications":case_type_list}
        except:
            traceback.print_exc()
            return {"applications":[]}

