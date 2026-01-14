from bs4 import BeautifulSoup
from datetime import datetime
import re,json

class Extractor:
    def __init__(self, session):
        self.session = session
       
    # def get_bench_code(self, soup, bench_name: str):
    #     select = soup.find(id="db_bench")
    #     if not select:
    #         return []

    #     options = select.find_all("option")
    #     bench_name_norm = bench_name.strip().lower()
    #     for opt in options:
    #         if opt.get_text(strip=True).lower() == bench_name_norm:
    #             bench_value = opt.get("value")
    #             return bench_value
    #     return None

    # def get_case_type(self, soup, case_type: str):
    #     select = soup.find(id="cmbcasetype")
    #     if not select:
    #         return []

    #     options = select.find_all("option")
    #     case_type_norm = case_type.strip().lower()
    #     for opt in options:
    #         if opt.get_text(strip=True).lower() == case_type_norm:
    #             case_value = opt.get("value")
    #             return case_value
    #     return None

    # def selectCode(self,res, bench_name, case_type):
    #     soup = BeautifulSoup(res.text, "html.parser")
    #     bench_code = self.get_bench_code(soup,bench_name)
    #     case_code = self.get_case_type(soup,case_type)
    #     return bench_code,case_code

    def getCaseTypeCode(self, res, case_code):
        soup = BeautifulSoup(res.text, "html.parser")
        select = soup.find(id="cmbcasetype")
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

    def getBenchTypeCode(self, res, bench_code):
        soup = BeautifulSoup(res.text, "html.parser")
        select = soup.find(id="db_bench")
        options = select.find_all("option")
        new_code = 1
        for opt in options:
            case_type = opt.get_text(strip=True)
            if case_type:
                if str(new_code)==bench_code:
                    case_code = opt.get('value')
                    return case_code
                
                new_code += 1
        return None

    def caseTypes(self, res):
        soup = BeautifulSoup(res.text, "html.parser")
        select = soup.find(id="cmbcasetype")
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
    
    def benchTypes(self, res):
        soup = BeautifulSoup(res.text, "html.parser")
        select = soup.find(id="db_bench")
        options = select.find_all("option")
        new_code = 1
        bench_types = []
        for opt in options:
            bench_type = opt.get_text(strip=True)
            if bench_type:
                bench_types.append({
                    "code_code":str(new_code),
                    "bench_type":bench_type
                })
                new_code += 1
        return bench_types
    
    def fetchChallanDetails(self, res):
        try:
            if not res or not res.text:
                return []

            if "No Data Found" in res.text:
                return "case details are not available"

            soup = BeautifulSoup(res.text, "html.parser")
            case_details = {}

            rows = soup.find_all(class_="row")
            for row in range(len(rows)-2):
                key_tag = rows[row].find(class_="col-md-3")
                value_tag = rows[row].find(class_="col-md-8")

                if not key_tag or not value_tag:
                    continue

                key = key_tag.get_text(strip=True)
                value = value_tag.get_text(strip=True)

                if value == "-" or value == "" or value == "NONE - none":
                    value = None

                case_details[key] = value

            return case_details
        except:
            return []

