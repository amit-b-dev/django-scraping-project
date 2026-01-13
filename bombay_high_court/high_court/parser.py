from bs4 import BeautifulSoup
from datetime import datetime
import re,json

class Extractor:
    def __init__(self, session):
        self.session = session

    def fetchCaseDetails(self,res):

        soup = BeautifulSoup(res.text,'html.parser')
        no_orders_available = soup.find(class_="text-red")
        if no_orders_available:
            return "case details are not available"
    
        table_data = []
        all_tr = soup.find(class_="table-responsive").find_all('tr')
        for i in range(1,len(all_tr)-1):
                values = [j.get_text(strip=True).replace('Click to View','') for j in all_tr[i].find_all('td')]
                short_file_url = all_tr[i].find_all('td')[-1].find('a')['href']
                complete_file_url = f"https://bombayhighcourt.nic.in/{short_file_url}"
                table_data.append({
                    "CORAM":values[0],
                    "ORDER/JUDGEMENT DATE":values[1],
                    "PAGES":values[2],
                    "UPLOAD DATE":values[3],
                    "File":complete_file_url,
                })
        return table_data
    

    def getCaseSideCode(self, res, case_side_code):
        soup = BeautifulSoup(res.text, "html.parser")
        select = soup.find("select",{"name":"m_sideflg"})
        options = select.find_all("option")
        new_code = 1
        for opt in options:
            bench_type = opt.get_text(strip=True)
            if bench_type:
                if str(new_code)==case_side_code:
                    actual_case_side_code = opt.get('value')
                    return actual_case_side_code

                new_code += 1
        return None
    
    def getStampAndRegCode(self, res, case_stamp_regno_code):
        soup = BeautifulSoup(res.text, "html.parser")
        select = soup.find("select",{"name":"m_sr"})
        options = select.find_all("option")
        new_code = 1
        for opt in options:
            bench_type = opt.get_text(strip=True)
            if bench_type:
                if str(new_code)==case_stamp_regno_code:
                    actual_case_stamp_regno_code = opt.get('value')
                    return actual_case_stamp_regno_code
                new_code += 1
        return None
    
    def getCaseTypeCode(self, res, case_type_code):
        soup = BeautifulSoup(res.text, "html.parser")
        select = soup.find("select",{"name":"m_skey"})
        options = select.find_all("option")
        new_code = 1
        for opt in options:
            bench_type = opt.get_text(strip=True)
            if bench_type:
                if str(new_code)==case_type_code:
                    actual_case_type_code = opt.get('value')
                    return actual_case_type_code
                new_code += 1
        return None
    
# FOR CASE GET REQUESTS APIs
    def getCaseSideData(self,res):
        soup = BeautifulSoup(res.text, "html.parser")
        select = soup.find("select",{"name":"m_sideflg"})
        options = select.find_all("option")
        new_code = 1
        case_modes = []
        for opt in options:
            bench_type = opt.get_text(strip=True)
            if bench_type:
                case_modes.append({
                    "code_code":str(new_code),
                    "bench_type":bench_type
                })
                new_code += 1
        return case_modes
    
    def getCaseTypeData(self,res):
        soup = BeautifulSoup(res.text, "html.parser")
        select = soup.find("select",{"name":"m_skey"})
        options = select.find_all("option")
        new_code = 1
        case_modes = []
        for opt in options:
            bench_type = opt.get_text(strip=True)
            if bench_type:
                case_modes.append({
                    "code_code":str(new_code),
                    "bench_type":bench_type
                })
                new_code += 1
        return case_modes
    
    def getStampAndRegData(self,res):
        soup = BeautifulSoup(res.text, "html.parser")
        select = soup.find("select",{"name":"m_sr"})
        options = select.find_all("option")
        new_code = 1
        case_modes = []
        for opt in options:
            bench_type = opt.get_text(strip=True)
            if bench_type:
                case_modes.append({
                    "code_code":str(new_code),
                    "bench_type":bench_type
                })
                new_code += 1
        return case_modes
    