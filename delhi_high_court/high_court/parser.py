from bs4 import BeautifulSoup
from datetime import datetime
import re,json

class Extractor:
    def __init__(self, session):
        self.session = session

    def get_case_code(self, res, case_code):
        soup = BeautifulSoup(res.text, "html.parser")
        select = soup.find(id="case_type")
        options = select.find_all("option")
        new_code = 1
        for opt in options[1:]:
            case_type = opt.get_text(strip=True)
            if case_type:
                if str(new_code)==case_code:
                    case_code = opt.get('value')
                    return case_code
                
                new_code += 1
        return None

    def GetCaptchText(self,res):
        soup = BeautifulSoup(res.text, "html.parser")
        captcha_text = soup.find(id="captcha-code").get_text(strip=True)
        _token = soup.find("input",{"name":"_token"})['value']
        return captcha_text,_token
    
    def caseTypes(self, res):
        soup = BeautifulSoup(res.text, "html.parser")
        select = soup.find(id="case_type")
        options = select.find_all("option")
        new_code = 1
        case_types = []
        for opt in options[1:]:
            case_type = opt.get_text(strip=True)
            if case_type:
                case_types.append({
                    "case_code":str(new_code),
                    "case_type":case_type
                })
                new_code += 1
        return case_types

    def fetchChallanDetails(self, res):
        try:
            case_details = []
            if not res or not res.text:
                return []
            
            soup = BeautifulSoup(res.text,'html.parser')

            tbl = soup.find(id="s_judgeTable")
            if tbl:
                # tbl_row_header = tbl.find('thead').find_all('tr')
                # key = [i.get_text(strip=True) for i in tbl_row_header[0].find_all("th")]

                tbl_row_value = tbl.find('tbody').find_all('tr')
                for row in range(len(tbl_row_value)):
                    value = [i.get_text(strip=True) for i in tbl_row_value[row].find_all("td")]
                    # case_details.append(dict(zip(key,value)))
                    a_tag = tbl_row_value[row].find_all('a')
                    if a_tag:
                        pdf_link = a_tag[0]['href']
                    else:
                        pdf_link = None
                    case_details.append({
                        "S.No.": value[0],
                        "Case No.": value[1],
                        "Date of Judgment": value[2],
                        "Party": value[3],
                        "Corrigendum": value[4],
                        "Date of Uploading": value[5],
                        "Remark": value[6],
                        "Order": pdf_link,
                    })


                
                if not tbl_row_value:
                    return "case details are not available"
            return case_details
        except:
            return []

