from .headers import HeaderHelper
from .captcha import CaptchaSolver
import time,os,base64
from bs4 import BeautifulSoup

class NavigationFlow:

    def __init__(self, session):
        self.session = session
        self.solver = CaptchaSolver()
    
    def loadHomePage(self,court_code):
        
        url = f"https://hcservices.ecourts.gov.in/ecourtindiaHC/index_highcourt.php?state_cd=16&dist_cd=1&court_code={court_code}&stateNm=Calcutta"
        res = self.session.get(url)
        time.sleep(0.2)
        url = f"https://hcservices.ecourts.gov.in/ecourtindiaHC/cases/case_no.php?state_cd=16&dist_cd=1&court_code={court_code}&stateNm=Calcutta"
        res = self.session.get(url)
        time.sleep(0.2)
        cookies = self.session.cookies.get_dict()
        
        return res,cookies
    
    def getCaptchText(self, res, cookies):

        headers = HeaderHelper.captcha_header()
        soup = BeautifulSoup(res.text,"html.parser")
        captcha_url = "https://hcservices.ecourts.gov.in"+soup.find(id='captcha_image')['src']
        captcha_res = self.session.get(captcha_url, headers=headers,cookies=cookies)
        time.sleep(0.2)
        captcha_text = self.solver.solve(captcha_res)

        return captcha_text
    

    def varifyCaptchaAndDetails(self,cookies, court_code, case_code, case_no,case_year, captcha_text):
        headers,payload = HeaderHelper.getCaseDetails_header(court_code, case_code, case_no, case_year, captcha_text)
        res = self.session.post("https://hcservices.ecourts.gov.in/ecourtindiaHC/cases/case_no_qry.php", headers=headers,data=payload, cookies=cookies)
        time.sleep(0.2)
        return res
    

    def oCivilCaseHistory(self,court_code, case_no1, cino, token):
        headers,payload = HeaderHelper.oCivilCaseHistory_header(court_code, case_no1, cino, token)
        res = self.session.post("https://hcservices.ecourts.gov.in/ecourtindiaHC/cases/o_civil_case_history.php", headers=headers,data=payload)
        time.sleep(0.2)
        return res

    def getCaseTypeCode(self,court_code, case_code):

        headers,payload = HeaderHelper.getCaseTypeCode_header(court_code)
        res = self.session.post("https://hcservices.ecourts.gov.in/ecourtindiaHC/cases/case_no_qry.php", headers=headers,data=payload)
        time.sleep(0.2)
        select_list = res.text.split('#')
        actual_case_code = None
        new_code = 1
        for item in select_list[1:]:
            if "~" not in item:
                continue

            name = item.split("~")[1].strip()  # ignore original code

            if name:
                if str(new_code)==case_code:
                    actual_case_code = name.split('(')[-1].replace(')','').strip()
                    return actual_case_code

                new_code += 1
        return actual_case_code

    def getCasetypesList(self,court_code):

        headers,payload = HeaderHelper.getCaseTypeCode_header(court_code)
        res = self.session.post("https://hcservices.ecourts.gov.in/ecourtindiaHC/cases/case_no_qry.php", headers=headers,data=payload)
        time.sleep(0.2)
        select_list = res.text.split('#')

        case_types = []
        new_code = 1
        for item in select_list[1:]:
            if "~" not in item:
                continue

            name = item.split("~")[1].strip()  # ignore original code

            if name:
                case_types.append({
                    "code_code": str(new_code),
                    "case_type": name
                })
                new_code += 1
        return case_types

    # def get_Base64_Encoded_Pdf(self,value_id):
    #     url="https://hcmadras.tn.gov.in/order_view.php"
    #     headers,payloads = HeaderHelper.getPDF_Header(value_id)
    #     res = self.session.post(url, headers=headers,data=payloads)
    #     time.sleep(0.2)

    #     base64_pdf = base64.b64encode(res.content).decode()
    #     return base64_pdf
    