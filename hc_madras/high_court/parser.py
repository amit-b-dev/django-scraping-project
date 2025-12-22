from bs4 import BeautifulSoup
from datetime import datetime
from .code_flow import CodeFlow
import re

class Extractor:
    def __init__(self, session):
        self.session = session
        self.flow = CodeFlow(self.session)

    
    def extract_all_tables(self,res,cookies):
        try:
            soup = BeautifulSoup(res.text,"html.parser")
            sections = [ "CaseDetails", "LowerCourtDetails", "ApplicationsDetails", "ConnectedMatters", "Prayer", "HistoryofCaseHearing", "ListofDocuments", "CaveatDetails", "Notices"]
            all_table = soup.find_all(class_='table_caseno_search')
            orders = soup.find(class_='example11')
            all_tables = []
            Tables={}
            for name, table in zip(sections, all_table):
                Tables[name] = table.find("tbody").find_all("tr")

            case_details = {}
            for row in Tables['CaseDetails']:
                cols = row.find_all(["th", "td"])
                cols = [c.get_text(" ", strip=True) for c in cols]
                if len(cols) == 2:
                    key = cols[0]
                    val = cols[1]
                    if "\n\t\t\t\t\t\t\t" in val:
                        val = re.sub(r"\s+", " ", val).strip()
                    case_details[key] = val

                elif len(cols) == 4:
                    case_details[cols[0]] = cols[1]
                    case_details[cols[2]] = cols[3]

                elif len(cols) == 2 and "Details" in cols[0]:
                    case_details[cols[0]] = cols[1]

            lower_court_details = []
            for row in Tables['LowerCourtDetails']:
                cols = [c.get_text(" ", strip=True) for c in row.find_all(["th"])]
                values = [c.get_text(" ", strip=True) for c in row.find_all(["td"])]
                lower_court_details.append(dict(zip(cols, values)))


            applications_details = []
            for row in Tables['ApplicationsDetails']:
                cols = [c.get_text(" ", strip=True) for c in row.find_all(["th"])]
                values = [c.get_text(" ", strip=True) for c in row.find_all(["td"])]
                applications_details.append(dict(zip(cols, values)))


            Connected_Matters_dict = []
            for row in Tables['ConnectedMatters']:
                cols = [c.get_text(" ", strip=True) for c in row.find_all(["th"])]
                values = [c.get_text(" ", strip=True) for c in row.find_all(["td"])]
                Connected_Matters_dict.append(dict(zip(cols, values)))
            
            prayer={}
            for row in Tables['Prayer']:
                cols = row.find_all(["th", "td"])
                cols = [c.get_text(" ", strip=True) for c in cols]
                key = cols[0]
                val = cols[1]
                prayer[key]=val

            history_of_casehearing = []
            for row in Tables['HistoryofCaseHearing']:
                cols = [c.get_text(" ", strip=True) for c in row.find_all(["th"])]
                values = [c.get_text(" ", strip=True) for c in row.find_all(["td"])]
                history_of_casehearing.append(dict(zip(cols, values)))

            list_of_documents = []
            for row in Tables['ListofDocuments']:
                cols = [c.get_text(" ", strip=True) for c in row.find_all(["th"])]
                values = [c.get_text(" ", strip=True) for c in row.find_all(["td"])]
                list_of_documents.append(dict(zip(cols, values)))

            caveat_details = []
            for row in Tables['CaveatDetails']:
                cols = [c.get_text(" ", strip=True) for c in row.find_all(["th"])]
                values = [c.get_text(" ", strip=True) for c in row.find_all(["td"])]
                caveat_details.append(dict(zip(cols, values)))

            notices = []
            for row in Tables['Notices']:
                cols = [c.get_text(" ", strip=True) for c in row.find_all(["th"])]
                values = [c.get_text(" ", strip=True) for c in row.find_all(["td"])]
                notices.append(dict(zip(cols, values)))

            orders = []
            Orders = soup.find(id='example11')
            cols = [c.get_text(" ", strip=True) for c in Orders.find('thead').find_all('th')]
            for row in Orders.find('tbody').find_all('tr'):
                values = [c.get_text(" ", strip=True) for c in row.find_all(["td"])]
                value_id = row.find('form').find('input')['value']
                base64_pdf = self.flow.get_Base64_Encoded_Pdf(value_id,cookies)
                values[-1]=base64_pdf
                orders.append(dict(zip(cols, values)))

            all_tables.append({
                "case_details":case_details,
                "lower_court_details":lower_court_details,
                "applications_details":applications_details,
                "Connected_Matters_dict":Connected_Matters_dict,
                "Prayer":prayer,
                "history_of_casehearing":history_of_casehearing,
                "list_of_documents":list_of_documents,
                "caveat_details":caveat_details,
                "notices":notices,
                "orders":orders
            })
            return all_tables
        except:
            return []
        