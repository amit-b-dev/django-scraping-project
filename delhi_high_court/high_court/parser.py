from bs4 import BeautifulSoup
from datetime import datetime
import re,json

class Extractor:
    def __init__(self, session):
        self.session = session

    def get_case_type(self, soup, case_type: str):
        select = soup.find(id="case_type")
        if not select:
            return []

        options = select.find_all("option")
        case_type_norm = case_type.strip().lower()
        for opt in options:
            if opt.get_text(strip=True).lower() == case_type_norm:
                case_value = opt.get("value")
                return case_value
        return None

    def selectCodeAndGetCaptchText(self,res, case_type):
        soup = BeautifulSoup(res.text, "html.parser")
        captcha_text = soup.find(id="captcha-code").get_text(strip=True)
        _token = soup.find("input",{"name":"_token"})['value']
        case_code = self.get_case_type(soup,case_type)
        return case_code,captcha_text,_token

    def fetchChallanDetails(self, res):
        try:
            case_details = []
            if not res or not res.text:
                return {}
            
            soup = BeautifulSoup(res.text,'html.parser')

            tbl = soup.find(id="s_judgeTable")
            if tbl:
                tbl_row_header = tbl.find('thead').find_all('tr')
                key = [i.get_text(strip=True) for i in tbl_row_header[0].find_all("th")]

                tbl_row_value = tbl.find('tbody').find_all('tr')
                for row in range(len(tbl_row_value)):
                    value = [i.get_text(strip=True) for i in tbl_row_value[row].find_all("td")]
                    case_details.append(dict(zip(key,value)))
                
                if not tbl_row_value:
                    return "case details not found"
            return case_details
        except:
            return []

