from .headers import HeaderHelper
from .captcha import CaptchaSolver
import time,os,base64
from bs4 import BeautifulSoup

class NavigationFlow:

    def __init__(self, session):
        self.session = session
        self.solver = CaptchaSolver()
    
    def loadHomePage(self):
        url = "https://hcmadras.tn.gov.in/cause_judment_mas.php"
        res = self.session.get(url)
        time.sleep(0.2)
        cookies = self.session.cookies.get_dict()
        
        return res,cookies
    
    def getCaptchText(self, res, cookies):

        headers = HeaderHelper.captcha_header()
        soup = BeautifulSoup(res.text,"html.parser")
        captcha_url = "https://hcmadras.tn.gov.in"+soup.find(id='caseno_captcha_img')['src']
        captcha_res = self.session.get(captcha_url, headers=headers,cookies=cookies)
        time.sleep(0.2)
        captcha_text,captcha_path,captcha_dir = self.solver.solve(captcha_res)

        return captcha_text,captcha_path,captcha_dir
    

    def getCaseDetails(self,cookies, case_code, case_no,case_year, captcha_text,captcha_path,captcha_dir):
        headers,payload = HeaderHelper.getCaseDetails_header(case_code, case_no, case_year, captcha_text)
        res = self.session.post("https://hcmadras.tn.gov.in/cause_judment_action.php", headers=headers,data=payload, cookies=cookies)
        time.sleep(0.2)
        if "Captcha not matching" not in res.text:
            if os.path.exists(captcha_path):
                os.remove(captcha_path)
            if os.path.isdir(captcha_dir):
                os.rmdir(captcha_dir)
        return res
    
    def get_Base64_Encoded_Pdf(self,value_id):
        url="https://hcmadras.tn.gov.in/order_view.php"
        headers,payloads = HeaderHelper.getPDF_Header(value_id)
        res = self.session.post(url, headers=headers,data=payloads)
        time.sleep(0.2)

        base64_pdf = base64.b64encode(res.content).decode()
        return base64_pdf