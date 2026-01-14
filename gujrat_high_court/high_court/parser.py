from bs4 import BeautifulSoup
from datetime import datetime
import re, json, traceback, time, base64
from .headers import HeaderHelper

class Extractor:
    def __init__(self, session):
        self.session = session

    
    def getCaseHeader(self,data):
        try:md = data.get("maindetails", {})
        except:md = None
        try:case_title = f"{md.get('casedesc')} - No. {md.get('casenumber')} of {md.get('caseyear')}"
        except:case_title = None
        try:cnr_no = md.get("ccin")
        except:cnr_no=None
        try:status = md.get("casestatus")
        except:status = None
        return {
            "case_title": case_title,
            "cnr_no": cnr_no,
            "status": status
        }

    def getDisposalDetails(self,data):
        try:md = data.get("maindetails", {})
        except:md = None
        try:disposal_date = md.get("disposaldate")
        except:disposal_date = None
        try:decided_by =  md.get("judges")
        except:decided_by = None
        return {
            "disposal_date": disposal_date,
            "decided_by": decided_by
        }

    def normalize_to_list_helper(self,value):
        if not value:
            return []
        if isinstance(value, list):
            return value
        if isinstance(value, dict):
            return [value]
        return []   # anything else (str, int, etc.)

    def getPartiesTable(self,data):
        litigants = self.normalize_to_list_helper(data.get("litigant"))
        respondents_raw = self.normalize_to_list_helper(data.get("respondant"))
        advocates = self.normalize_to_list_helper(data.get("advocate"))

        petitioners = []
        respondents = []

        # Group advocates by litiganttypecode
        adv_map = {"1": [], "2": []}

        for adv in advocates:
            if not isinstance(adv, dict):
                continue

            code = adv.get("litiganttypecode")
            if code in adv_map:
                adv_map[code].append(
                    f"{adv.get('advocatename')} for: {adv.get('litiganttype')} {adv.get('namelist')}"
                )

        # Petitioners
        for l in litigants:
            petitioners.append({
                "sno": l.get("srno"),
                "name": l.get("litigantname"),
                "advocate_on_record": adv_map["1"]
            })

        # Respondents
        for r in respondents_raw:
            respondents.append({
                "sno": r.get("srno"),
                "name": r.get("respondantname"),
                "advocate_on_record": adv_map["2"]
            })

        return {
            "petitioners": petitioners,
            "respondents": respondents
        }

    def getCaseMeta(self,data):
        
        try:md = data.get("maindetails", {})
        except:md = None
        try:presented_on         =   md.get("presentdate")
        except:presented_on      =   None

        try:registered_on        =   md.get("registrationdate")
        except:registered_on     =   None

        try:bench_category       =   md.get("benchname")
        except:bench_category    =   None

        try:district             =   md.get("districtname")
        except:district          =   None

        try:case_originated_from =   md.get("originname")
        except:case_originated_from =   None

        try:purpose_of_listing   =   md.get("stagename")
        except:purpose_of_listing=   None

        try:
            cls = data.get("classification", {})
            classification= cls.get("description")
            Act = None
        except:
            if len(cls)==2:
                classification = cls[1].get("description")
                Act = cls[0].get("description")
            
        return {
            "presented_on": presented_on,
            "registered_on": registered_on,
            "bench_category": bench_category,
            "district": district,
            "case_originated_from": case_originated_from,
            "purpose_of_listing": purpose_of_listing,
            "classification": classification,
            "Act": Act
        }

    def getCourtProceedings(self,data):
        proceedings = []

        rows = self.normalize_to_list_helper(data.get("linkedmatterscp"))

        for idx, row in enumerate(rows, start=1):
            if not isinstance(row, dict):
                continue

            proceedings.append({
                "sno": idx,
                "notified_date": row.get("PROCEEDINGDATElmcp", "").strip(),
                "court_code": row.get("COURTCODElmcp", "").strip(),
                "board_sr_no": row.get("BOARDSRNOlmcp", "").strip(),
                "stage": row.get("STAGENAMElmcp", "").strip(),
                "action": row.get("ACTIONNAMElmcp", "").strip(),
                "coram": row.get("JUDGESlmcp", "").strip()
            })

        return proceedings

    def convertResRedableform(self,text):
    
        try:
            mainDict = json.loads(text)
            blocks = mainDict.get("data", [])

            if not blocks:
                result="case details are not available"
                return result

            result = {}

            for block in blocks:
                if not isinstance(block, dict) or not block:
                    continue

                for key, value in block.items():
                    if isinstance(value, list) and len(value) == 1:
                        result[key] = value[0]
                    else:
                        result[key] = value
            return result
        except:
            result=[]

    def downloadOrderPdf(self,ccin_no,order_no,order_date,casedetail):
        headers, payload = HeaderHelper.downloadOrderPdf_header(ccin_no,order_no,order_date,casedetail)
        res = self.session.post("https://gujarathc-casestatus.nic.in/gujarathc/OrderHistoryViewDownload", headers=headers, data=payload)
        time.sleep(0.2)
        base64_pdf = base64.b64encode(res.content).decode()
        return base64_pdf

    def availableOrders(self,data):
        available_orders = []
        try:rows = data.get("orderhistory",[])
        except:rows = None
        if rows:
            if isinstance(rows, dict):
                rows = [rows]
            for i in range(len(rows)):
                s_no = str(i+1)
                available_orders.append({
                    "S.No.":s_no,
                    "case_details" : rows[i]['descriptionoh'],
                    "judge_name" : rows[i]['judgesoh'],
                    "order_date" : rows[i]['dsdate'],
                    "cav" : rows[i]['cavjudgement'],
                    "judgement" : None,
                    "questions" : rows[i]['questions'],
                    "transferred" : rows[i]['transferred'],
                    "download_pdf" : self.downloadOrderPdf(rows[i]['ccinoh'],s_no,rows[i]['dsdate'],rows[i]['descriptionoh']),

                })

        return available_orders

    def iaDetails(self,data):
        ia_details = []
        try:rows = data.get("applicationmatters",[])
        except:rows = None
        if rows:
            if isinstance(rows, dict):
                rows = [rows]
            for i in range(len(rows)):
                s_no = str(i+1)
                ia_details.append({
                    "S.No.":s_no,
                    "case_details" : rows[i]['descriptionlm'],
                    "status_name" : rows[i]['statusnamelm'],
                    "disposal_date" : rows[i]['disposaldatelm'],
                })
        return ia_details
    
    def officeDetails(self,data):
        office_details = []
        try:rows = data.get("officedetails",[])
        except:rows = None
        if rows:
            if isinstance(rows, dict):
                rows = [rows]
            for i in range(len(rows)):
                s_no = str(i+1)
                office_details.append({
                    "s.no.":s_no,
                    "filing_date" : rows[i]['FILINGDATE'],
                    "document_name" : rows[i]['DOCUMENTNAME'],
                    "advocate_name" : rows[i]['ADVOCATEDISPLAYNAME'],
                    "court_fee_on_document" : rows[i]['documentfee'],
                    "document_details" : rows[i]['documentdetails'],
                })
        return office_details
    
    def lowerCourtDetails(self,data):
        lower_court_details = []
        try:rows = data.get("lowercourt",[])
        except:rows = None
        if rows:
            if isinstance(rows, dict):
                rows = [rows]
            for i in range(len(rows)):
                s_no = str(i+1)
                lower_court_details.append({
                        "S.No.":s_no,
                        "lower_court_case_detai" : rows[i]['lccasedescription'],
                        "lower_court_name" : rows[i]['lowercourtname'],
                        "judge_name" : rows[i]['lcjudgename'],
                        "judgment_date" : rows[i]['LCJUDGEMENTDATE'],
                    })
        return lower_court_details

    def fetchChallanDetails(self,res):
        try:
            if "Details not Found" in res.text:
                return "case details are not available"
            result = self.convertResRedableform(res.text)
            if result:
                final_response = {
                    
                    "case_header"               : self.getCaseHeader(result),
                    "disposal_details"          : self.getDisposalDetails(result),
                    "parties"                   : self.getPartiesTable(result),
                    "case_meta"                 : self.getCaseMeta(result),
                    "court_proceedings"         : self.getCourtProceedings(result),
                    "available_orders"          : self.availableOrders(result),
                    "ia_details"                : self.iaDetails(result),
                    "office_details"            : self.officeDetails(result),
                    "lower_court_details"       : self.lowerCourtDetails(result),
                    "office_objections"         : [],
                    "connected_matters"         : [],
                    "application_appeal_matters": [],
                    "certified_copy"            : []
                }
                return final_response
            else:
                return []
        except:
            traceback.print_exc()
            return []



    def getCaseMode(self,res,case_mode_code):
        soup = BeautifulSoup(res.text, "html.parser")
        select = soup.find(id="casefr")
        options = select.find_all("option")
        new_code = 1
        for opt in options:
            case_mode = opt.get_text(strip=True)
            if case_mode:
                if str(new_code)==case_mode_code:
                    actual_case_mode_code = opt.get('value')
                    return actual_case_mode_code
                new_code += 1
        return None

    def getCaseCode(self, res, case_type_code):

        data = json.loads(res.text)

        finaldata = data["finaldata"][0]
        case_type_array = finaldata["casetypearray"]
        new_code = 1
        for group in case_type_array:
            for category, cases in group.items():
                for case in cases:
                    if str(new_code)==case_type_code:
                        return str(case["casecode"])
                    new_code += 1

        return None
    


    def getCaseModeData(self,res):
        soup = BeautifulSoup(res.text, "html.parser")
        select = soup.find(id="casefr")
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

    def getCaseTypeData(self, res):

        case_list = []
        data = json.loads(res.text)

        finaldata = data["finaldata"][0]
        case_type_array = finaldata["casetypearray"]
        new_code = 1
        for group in case_type_array:
            for category, cases in group.items():
                for case in cases:
                    case_list.append({
                            "case_type_code": new_code,
                            "case_type": '-'.join((case["casetype"],case["description"])),
                    })
                    new_code += 1
        return case_list
        
