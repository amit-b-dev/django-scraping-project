import base64
from bs4 import BeautifulSoup
from datetime import datetime
from lxml import html
import re,json, traceback, time
from .headers import HeaderHelper
from .xpath import Xpath


class Extractor:
    def __init__(self, session):
        self.session = session

    def safe(self,value, default=""):
        return value if value not in (None, "") else default

    def parseAjaxHtml(self, r, html_key=''):
        try:
            j = r.json()
            app_token = j.get("app_token")
            html_data = j.get(html_key, "")
            tree = html.fromstring(html_data) if html_data else None
            return tree, app_token
        except Exception:
            return None, None
    
    def download_pdf(self,app_token,tree,h,pdf_no,t_no):
        try:
            tables = tree.xpath("//table[@class='order_table table ']")
            rows = tables[t_no].xpath(".//tr")
            tds = rows[1].xpath("./td")
            a_tag = tds[2].xpath(".//a[contains(@onclick, 'displayPdf')]")[pdf_no]
            onclick = a_tag.xpath("./@onclick")[0]
            params = re.findall(r"'(.*?)'", onclick)

            headers,payload=HeaderHelper.getPdfDetails_header(params,app_token)
            pdf_url = "https://services.ecourts.gov.in/ecourtindia_v6/home/display_pdf"
            r = self.session.post(pdf_url, data=payload, headers=headers)
            res_pdf = json.loads(r.text)
            full_pdf_url = "https://services.ecourts.gov.in/ecourtindia_v6/"+res_pdf['order']

            res = self.session.get(full_pdf_url)
            time.sleep(0.2)
            base64_pdf = base64.b64encode(res.content).decode()
            tree, app_token = self.parseAjaxHtml(r)
            return app_token,base64_pdf
        except:
            return None,None

    def get_case_history_status(self,r,tree,Order_Date,Court_Number,app_token,srno,cookies):
        try:
            data=None
            a_tag = tree.xpath("//a[@class='fw-bold text-underline text-success fst-italic']")
            parts=re.search(r"display_case_acknowlegement\('([^']+)'", a_tag[0].xpath("./@onclick")[0]).group(1).split('&')
            result = {"path": parts[0], **{p.split("=",1)[0]: p.split("=",1)[1] for p in parts[1:]}}

            headers,payload=HeaderHelper.viewBusiness_header(result,Order_Date,Court_Number,srno,app_token)
            url = "https://services.ecourts.gov.in/ecourtindia_v6/home/viewBusiness"
            r = self.session.post(url, data=payload, headers=headers)
            time.sleep(0.2)

            key="data_list"
            tree, app_token = self.parseAjaxHtml(r,key)

            data = {}
            data["in_the_court_of"] = tree.xpath("//b[text()='In the court of ']/parent::span")[0].text_content().split(':')[1].strip()
            data["CNR_Number"] = tree.xpath("//b[text()=' CNR Number ']/parent::span")[0].text_content().split(':')[1].strip()
            data["Case_Number"] = tree.xpath("//b[text()='Case Number ']/parent::span")[0].text_content().split(':')[1].strip()
            data["party1"] = tree.xpath("//b[text()='  versus  ']/parent::span")[0].text_content().split('versus')[0].strip()
            data["party2"] = tree.xpath("//b[text()='  versus  ']/parent::span")[0].text_content().split('versus')[1].strip()
            data['date'] = Order_Date
            
            data["Business"] = tree.xpath("//b[text()='Business']/parent::td/parent::tr/td[3]")[0].text_content().strip()
            data["Nature of Disposal"] = tree.xpath("//b[text()='Nature of Disposal']/parent::td/parent::tr/td[3]")[0].text_content().strip()
            data["Disposal Date"] = tree.xpath("//b[text()='Disposal Date']/parent::td/parent::tr/td[3]")[0].text_content().strip()

            return app_token,data
        except:
            # traceback.print_exc()
            return app_token,data
    

    def fetchCaseDetails(self,r,cookies):
        try:
            key="casetype_list"
            tree, app_token = self.parseAjaxHtml(r,key)

            tree.xpath(Xpath.FILING_NUMBER)[0].text.strip()
            case_type = tree.xpath(Xpath.CASE_TYPE)[0].text_content().strip()

            filing_number = tree.xpath(Xpath.FILING_NUMBER)[0].text_content().strip()
            filing_date = tree.xpath(Xpath.FILING_DATE)[0].text_content().strip()
            registration_number = tree.xpath(Xpath.REGISTRATION_NUMBER)[0].text_content().strip()
            registration_date = tree.xpath(Xpath.REGISTRATION_DATE)[0].text_content().strip()
            cnr_number = tree.xpath(Xpath.CNR_NUMBER)[0].text_content().strip()
            e_filno = tree.xpath(Xpath.E_FILNO)[0].text_content().strip()
            e_filing_date = tree.xpath(Xpath.E_FILING_DATE)[0].text_content().strip()

            First_Hearing_Date = tree.xpath(Xpath.FIRST_HEARING_DATE)[0].text_content().strip()
            Decision_Date = tree.xpath(Xpath.DECISION_DATE)[0].text_content().strip()
            Case_Status  = tree.xpath(Xpath.CASE_STATUS)[0].text_content().strip()
            Nature_of_Disposal = tree.xpath(Xpath.NATURE_OF_DISPOSAL)[0].text_content().strip()
            Court_Number = tree.xpath(Xpath.COURT_AND_JUDGE)[0].text_content().strip().split('-')[0]
            judge = tree.xpath(Xpath.COURT_AND_JUDGE)[0].text_content().strip().split('-')[1]
            party_and_advocate = tree.xpath(Xpath.PETITIONER_ADVOCATE)[0].text_content().replace("\xa0", " ").strip()
            party_name = party_and_advocate.lower().split('advocate-')[0].split(')')[1].strip()
            advocate_name = party_and_advocate.lower().split('advocate-')[1].strip()

            Respondent_and_Advocate = tree.xpath(Xpath.RESPONDENT_ADVOCATE)[0].text_content().replace("\xa0", " ").split(')')[1].strip()
            Under_Act = tree.xpath(Xpath.UNDER_ACT)[0].text_content().strip()
            Under_Section = tree.xpath(Xpath.UNDER_SECTION)[1].text_content().strip()
            
            case_history = []
            rows = tree.xpath(Xpath.HISTORY_ROWS)
            for h in range(len(rows)):
                tds = rows[h].xpath("./td")
                judge = tds[0].text_content().strip()
                business_on_date = tds[1].text_content().strip()
                hearing_date = tds[2].text_content().strip()
                purpose = tds[3].text_content().strip()

                app_token,data = self.get_case_history_status(r,tree,business_on_date,Court_Number,app_token,str(h),cookies)

                case_history.append({
                    "judge": judge,
                    "business_on_date": business_on_date,
                    "hearing_date": hearing_date,
                    "purpose": purpose,
                    "daily_status":data
                })

            Interim_Orders = []
            tables = tree.xpath(Xpath.INTRIM_ROWS)
            rows = tables[0].xpath(".//tr")
            for h in range(1,len(rows)):
                tds = rows[h].xpath("./td")
                Order_Number = tds[0].text_content().strip()
                Order_Date = tds[1].text_content().strip()
                Order_Details = tds[2].text_content().strip()
                
                app_token,base64_pdf = self.download_pdf(app_token,tree,h,0,t_no=0)

                Interim_Orders.append({
                    "Order_Number": Order_Number,
                    "Order_Date": Order_Date,
                    "Order_Details": Order_Details,
                    "pdf_url":base64_pdf
                })

            Final_Orders_Judgements = []
            tables = tree.xpath(Xpath.FINAL_ORDERS_JUDGEMENTS)
            rows = tables[1].xpath(".//tr")
            for h in range(1,len(rows)):
                tds = rows[h].xpath("./td")
                Order_Number = tds[0].text_content().strip()
                Order_Date = tds[1].text_content().strip()
                Order_Details = tds[2].text_content().strip()

                app_token,base64_pdf = self.download_pdf(app_token,tree,h,1,t_no=1)

                Final_Orders_Judgements.append({
                    "Order_Number": Order_Number,
                    "Order_Date": Order_Date,
                    "Order_Details": Order_Details,
                    "pdf_url":base64_pdf
                })

            
            data = {
                "Decision_Date": self.safe(Decision_Date),
                "Case_Status": self.safe(Case_Status),
                "Nature_of_Disposal": self.safe(Nature_of_Disposal),
                "Court_Number": self.safe(Court_Number),
                "judge": self.safe(judge),

                "party_name": self.safe(party_name),
                "advocate_name": self.safe(advocate_name),
                "Respondent_and_Advocate": self.safe(Respondent_and_Advocate),

                "Under_Act": self.safe(Under_Act),
                "Under_Section": self.safe(Under_Section),

                "case_type": self.safe(case_type),
                "filing_number": self.safe(filing_number),
                "filing_date": self.safe(filing_date),
                "registration_number": self.safe(registration_number),
                "registration_date": self.safe(registration_date),
                "cnr_number": self.safe(cnr_number),
                "e_filno": self.safe(e_filno),
                "e_filing_date": self.safe(e_filing_date),
                "First_Hearing_Date": self.safe(First_Hearing_Date),

                "case_history": case_history or [],
                "Interim_Orders": Interim_Orders or [],
                "Final_Orders_Judgements": Final_Orders_Judgements or []
            }

            return data
        except:
            data=[]

