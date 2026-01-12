from bs4 import BeautifulSoup
from datetime import datetime
from .navigation import NavigationFlow
from .headers import HeaderHelper
from lxml import html
import base64, re, traceback

class Extractor:
    def __init__(self, session):
        self.session = session
        self.flow = NavigationFlow(self.session)
    
    # def get_case_type(self, soup, case_type: str):
    #     select = soup.find(id="case_type")
    #     if not select:
    #         return []

    #     options = select.find_all("option")
    #     case_type_norm = case_type.strip().lower()
    #     for opt in options:
    #         if opt.get_text(strip=True).lower() == case_type_norm:
    #             case_value = opt.get("value")
    #             return case_value
    #     return None
    
    # def getCaseTypeCode(self,res, case_type):
    #     soup = BeautifulSoup(res.text, "html.parser")
    #     case_code = self.get_case_type(soup,case_type)
    #     return case_code
    
    def payloadData(self,res):
        try:
            case_no1=cino=token=check = None
            if '\ufeff'==res.text or not res.text:
                return case_no1, cino, token, "case details are not available"
            case_no1 = cino = token = None
            lists1   = res.text.split("~")
            case_no1 = lists1[0].replace('\ufeff','').strip()
            cino     = lists1[3].strip()
            token    = lists1[-1].replace('##','').strip()
        except:pass
            
        return case_no1,cino,token,check
    
    def case_details(self,tree):
        CaseDetails = []
        Case_Type=Filing_Number=Registration_Number=CNR_Number=None
        
        try:Case_Type = tree.xpath("//label[normalize-space()='Case Type']/ancestor::span[2]")[0].text_content().replace("\xa0", "").split(":")[1].strip()
        except:Case_Type=None

        try:Filing_Number = tree.xpath("//label[normalize-space()='Filing Number']/ancestor::span[1]/following-sibling::text()[1]")[0].replace("\xa0", "").replace(":",'').strip()
        except:Filing_Number=None
        
        try:Filing_Date = tree.xpath("//label[normalize-space()='Filing Date']/parent::span/text()[normalize-space()]")[0].replace("\xa0", "").replace(":",'').strip()
        except:Filing_Date=None
        
        try:Registration_Number = tree.xpath("//span[normalize-space()='Registration Number']/following-sibling::label")[0].text_content().replace("\xa0", "").replace(":",'').strip()
        except:Registration_Number=None
        
        try:Registration_Date = tree.xpath("//label[normalize-space()='Registration Date']/following-sibling::label")[0].text_content().replace("\xa0", "").replace(":",'').strip()
        except:Registration_Date=None
        
        try:CNR_Number = tree.xpath("//label[normalize-space()='CNR Number']/ancestor::span[1]/following-sibling::text()[1]")[0].replace("\xa0", "").replace(":",'').strip()
        except:CNR_Number=None

        CaseDetails={
            "case type":Case_Type,
            "filing number":Filing_Number,
            "filing date":Filing_Date,
            "registration number":Registration_Number,
            "registration date":Registration_Date,
            "CNR Number":CNR_Number,
        }
        return CaseDetails
    
    def clean(self, text):
        if not text:
            return ""
        return re.sub(r"\s+", " ", text.replace("\xa0", " ")).strip()

    def extract_dynamic_case_status(self,tree):
        data = {}

        labels = tree.xpath(
            "//div[contains(@style,'background-color:#FBF6D9')]//label"
        )

        for label in labels:
            strongs = label.xpath(".//strong")

            if len(strongs) < 2:
                continue

            key = self.clean(strongs[0].text_content())
            value = self.clean(strongs[-1].text_content().replace(":", ""))

            if not key:
                continue

            # normalize key → snake_case
            norm_key = (
                key.lower()
                .replace(" ", "_")
                .replace("-", "_")
            )

            data[norm_key] = value

        return data

    def petitioner_respondent_advocate(self,tree):
        try:petitioner = tree.xpath("//span[contains(@class,'Petitioner_Advocate_table')]/text()[normalize-space()][1]")[0].split(')')[1].strip()
        except:petitioner = None
        try:advocate = tree.xpath("//span[contains(@class,'Petitioner_Advocate_table')]//text()[contains(.,'Advocate')]")[0].replace("Advocate-", "").replace("\xa0", "").strip()    
        except:advocate = None
        try:respondent = tree.xpath("//span[contains(@class,'Respondent_Advocate_table')]/text()[normalize-space()][1]")[0].split(')')[1].strip()
        except:respondent = None

        acts = []
        rows = tree.xpath("//table[@id='act_table']//tr[td]")
        if rows:
            for row in rows:
                tds = row.xpath("./td/text()")
                acts.append({
                    "under_act": tds[0].strip(),
                    "under_section": tds[1].strip()
                })

        petitioner_and_advocate = {
            "petitioner": petitioner,
            "advocate": advocate
        }
        respondent_and_advocate = {
            "petitioner": respondent,
            "advocate": None
        }

        return petitioner_and_advocate,respondent_and_advocate,acts
    
    def ia_details(self,tree):
        ia_list = []

        rows = tree.xpath("//table[contains(@class,'IAheading')]//tr[td]")

        if rows:
            for row in rows:
                tds = row.xpath("./td")

                ia_number = tds[0].xpath("normalize-space(text()[1])")
                parties = tds[1].text_content().strip()
                filing_date = tds[2].text_content().strip()
                next_date = tds[3].text_content().strip()
                status = tds[4].text_content().strip()

                ia_list.append({
                    "ia_number": ia_number,
                    "party": parties,
                    "filing_date": filing_date,
                    "next_date": next_date,
                    "status": status
                })

        return ia_list
    
    def case_conversion(self,tree):
        case_conversions = []

        rows = tree.xpath("//table[contains(@class,'tbl_case_conversion')]//tr[td]")

        for row in rows:
            tds = row.xpath("./td")

            old_case = tds[0].text_content().replace("\xa0", "").strip()
            new_case = tds[1].text_content().replace("\xa0", "").strip()
            date = tds[2].text_content().replace("\xa0", "").strip()

            case_conversions.append({
                "old_case_name": old_case,
                "new_case_name": new_case,
                "date": date
            })

        return case_conversions
    
    def dailyStatus(self, values):

        dailyStatus_Data = {}
        case_number=petitioner=respondent=date=Business=Next_Purpose=Next_Hearing_Date=None
        headers,payload = HeaderHelper.dailyStatus_header(values)
        res1 = self.session.post("https://hcservices.ecourts.gov.in/ecourtindiaHC/cases/s_show_business.php", headers=headers, data=payload)
        
        tree1 = html.fromstring(res1.text)
        in_the_court_of = tree1.xpath("//span[b[contains(normalize-space(),'In The Court Of')]]")[0].text_content().split(':')[1].strip()
        case_number = tree1.xpath("//span[b[contains(normalize-space(),'Case Number')]]")[0].text_content().split(':')[1].strip()
        text = tree1.xpath("//span[b[contains(normalize-space(),'Versus')]]")[0].text_content().strip()
        if "Versus" in text:
            petitioner = text.split("Versus")[0].strip()
            respondent = text.split("Versus")[1].strip()
        date = tree1.xpath("//span[b[contains(normalize-space(),'Date')]]")[0].text_content().split(':')[1].strip()

        dailyStatus_Data={
            "in_the_court_of": in_the_court_of,
            "case_number": case_number,
            "petitioner": petitioner,
            "respondent": respondent,
            "date": date
        }
        rows = tree1.xpath("//tr[@id='tr_print']/preceding-sibling::tr")
        for i in range(len(rows)):
            tds = rows[i].xpath(".//td")
            if len(tds)==3:
                key = tds[0].text_content().strip().lower()
                value = tds[2].text_content().strip()
                dailyStatus_Data[key] = value

        return dailyStatus_Data
        
    def history_of_Case_Hearing(self,tree):
        history = []

        rows = tree.xpath("//table[@class='history_table']/tr")
        for row in rows:
            tds = row.xpath("./td")
            if len(tds) < 5:
                continue
            
            row_data={
                "cause_list_type": tds[0].text_content().strip(),
                "judge": tds[1].text_content().strip(),
                "business_on_date": tds[2].text_content().strip(),
                "hearing_date": tds[3].text_content().strip(),
                "purpose_of_hearing": tds[4].text_content().strip(),
            }
            if row_data["business_on_date"]:
                onclick = tds[2].xpath(".//a/@onclick")
                if onclick:
                    values = re.findall(r"'([^']*)'", onclick[0])
                    if len(values) == 10:
                        row_data["dailyStatus_Data"] = self.dailyStatus(values)
            
            history.append(row_data)

        return history
    
    def get_Base64_Encoded_Pdf(self,pdf_link):
        base64_pdf = None
        headers = HeaderHelper.getPDF_Header()
        res = self.session.get(pdf_link, headers=headers)
        base64_pdf = base64.b64encode(res.content).decode()
        return base64_pdf
    
    def order_table1(self,tree):
        orders = []

        order_table = tree.xpath(
            "//table[contains(@class,'order_table')][.//strong[contains(normalize-space(),'Order Number')]]")
        
        if order_table:
            rows = order_table[0].xpath(".//tr[td][position()>1]")

            for row in rows:
                tds = row.xpath("./td")

                order_no = tds[0].text_content().replace("\xa0", "").strip()
                order_on = tds[1].text_content().replace("\xa0", "").strip()
                judge = tds[2].text_content().replace("\xa0", "").strip()
                order_date = tds[3].text_content().replace("\xa0", "").strip()

                pdf_link = "https://hcservices.ecourts.gov.in/ecourtindiaHC/cases/"+tds[4].xpath(".//a/@href")[0]
                base64_pdf = self.get_Base64_Encoded_Pdf(pdf_link)

                orders.append({
                    "order_number": order_no,
                    "order_on": order_on,
                    "judge": judge,
                    "order_date": order_date,
                    "order_pdf": base64_pdf or ''
                })

        return orders

    def objections(self,tree):
        objections_list = []

        objections = tree.xpath(
            "//table[contains(@class,'order_table')][.//b[normalize-space()='Scrutiny Date']]"
        )

        if objections:
            rows = objections[0].xpath(".//tr[td][position()>1]")

            for row in rows:
                tds = row.xpath("./td")

                objections_list.append({
                    "sr_no": tds[0].text_content().strip(),
                    "scrutiny_date": tds[1].text_content().strip(),
                    "objection": tds[2].text_content().strip(),
                    "compliance_date": tds[3].text_content().strip(),
                    "receipt_date": tds[4].text_content().strip()
                })

        return objections_list
    
    def order2(self,tree):
        Orders_list = []

        Orders = tree.xpath(
            "//table[contains(@class,'order_table')][.//b[normalize-space()='Old Case Name']]"
        )

        if Orders:
            rows = Orders[0].xpath(".//tr")

            for row in range(1,len(rows)):
                tds = rows[row].xpath("./td")

                Orders_list.append({
                    "Old Case Name": tds[0].text_content().strip(),
                    "New Case Name": tds[1].text_content().strip(),
                    "Date": tds[2].text_content().strip(),
                })

        return Orders_list
    
    def extract_subordinate_court_information(self,tree):
        data = {}
        container = tree.xpath("//span[contains(@class,'Lower_court_table')]")
        if not container:
            return data
        container = container[0]
        spans = container.xpath(".//span[@style[contains(.,'inline-block')]]")
        for span in spans:
            key = span.text_content().strip().rstrip(":")
            label = span.xpath("following-sibling::label[1]")

            if not key or not label:
                continue
            if label:
                label1 = label[0].xpath(".//span")
                if len(label1) == 2:
                    value = '--'
                    data[key] = value
                else:
                    value = label[0].text_content().replace(":", "").replace("\xa0", " ").strip()
                    data[key] = value
        return data

    def category_details(self,tree):
        data = {}
        container = tree.xpath("//table[.//*[normalize-space()='Category']]//tr")
        if not container:
            return data
        for span in range(len(container)):
            tds = container[span].xpath('.//td')
            if tds:
                key = tds[0].text_content().strip().lower()
                value = tds[1].text_content().strip()
                data[key]=value
        return data

    def documents(self,tree):
        documents = []

        all_rows = tree.xpath(
            "//table[.//label[normalize-space()='Document No.']]"
        )
        if all_rows:
            rows =all_rows[0].xpath(".//tr")
            for row in range(1,len(rows)):
                tds = rows[row].xpath("./td")

                documents.append({
                    "sr_no": tds[0].text_content().strip(),
                    "document_no": tds[1].text_content().strip(),
                    "date_of_receiving": tds[2].text_content().strip(),
                    "filed_by": tds[3].text_content().strip(),
                    "advocate_name": tds[4].text_content().strip(),
                    "document_filed": tds[5].text_content().strip()
                })

        return documents
    

    def fetchCaseDetails(self,res):
        try:
            final_data = []
            if "NO SEARCH RESULTS FOUND" in res.text:
                return "case details are not available"
            
            tree = html.fromstring(res.text)
            case_details = self.case_details(tree)
            # case_status = self.case_status(tree)
            case_status = self.extract_dynamic_case_status(tree)
            petitioner_and_advocate,respondent_and_advocate,acts = self.petitioner_respondent_advocate(tree)
            subordinate_court_information = self.extract_subordinate_court_information(tree)
            ia_details = self.ia_details(tree)
            case_conversion = self.case_conversion(tree)
            history_of_Case_Hearing = self.history_of_Case_Hearing(tree)
            order_table1 = self.order_table1(tree)
            category_details = self.category_details(tree)
            objections = self.objections(tree)
            order2 = self.order2(tree)
            documents = self.documents(tree)
            
            final_data={
                "case_details":case_details,
                "case_status":case_status,
                "petitioner_and_advocate":petitioner_and_advocate,
                "respondent_and_advocate":respondent_and_advocate,
                "acts":acts,
                "subordinate_court_information":subordinate_court_information or [],
                "ia_details":ia_details,
                "case_conversion":case_conversion,
                "history_of_Case_Hearing":history_of_Case_Hearing,
                "order_table1":order_table1,
                "category_details":category_details,
                "objections":objections,
                "order2":order2,
                "documents":documents
            }

            return final_data
        except:
            case_details=[]
            traceback.print_exc()
