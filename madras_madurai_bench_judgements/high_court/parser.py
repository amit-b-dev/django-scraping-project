from bs4 import BeautifulSoup
from datetime import datetime
from .navigation import NavigationFlow
from .headers import HeaderHelper
import base64

class Extractor:
    def __init__(self, session):
        self.session = session
        self.flow = NavigationFlow(self.session)
    
    def getCaseTypeCode(self, res, case_code):
        soup = BeautifulSoup(res.text, "html.parser")
        select = soup.find(id="RegCase_type")
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

    def caseTypes(self, res):
        soup = BeautifulSoup(res.text, "html.parser")
        select = soup.find(id="RegCase_type")
        options = select.find_all("option")
        new_code = 1
        case_types = []
        for opt in options[1:]:
            case_type = opt.get_text(strip=True)
            if case_type:
                case_types.append({
                    "code_code":str(new_code),
                    "case_type":case_type
                })
                new_code += 1
        return case_types
    
    def fetchCaseDetails(self,res):
        try:
            if "NO SEARCH RESULTS FOUND" in res.text:
                return "case details are not available"
            
            soup = BeautifulSoup(res.text,"html.parser")
            case_details = []
            tbl = soup.find(id="judment_case_no")
            if tbl:
                tbl_row_header = tbl.find('thead').find_all('tr')
                key = [i.get_text(strip=True) for i in tbl_row_header[0].find_all("th")]

                tbl_row_value = tbl.find('tbody').find_all('tr')
                for row in range(len(tbl_row_value)):
                    values = [i.get_text(strip=True) for i in tbl_row_value[row].find_all("td")]
                    value_id = tbl_row_value[row].find('form').find('input')['value']
                    base64_pdf = self.flow.get_Base64_Encoded_Pdf(value_id)
                    values[-1]=base64_pdf
                    case_details.append(dict(zip(key,values)))

            return case_details
        except:
            case_details=[]