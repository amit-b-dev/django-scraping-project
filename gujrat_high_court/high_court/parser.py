from bs4 import BeautifulSoup
from datetime import datetime
import re,json

class Extractor:
    def __init__(self, session):
        self.session = session

    
    def get_case_header(self,data):
        md = data.get("maindetails", {})

        return {
            "case_title": f"{md.get('casedesc')} - No. {md.get('casenumber')} of {md.get('caseyear')}",
            "cnr_no": md.get("ccin"),
            "status": md.get("casestatus")
        }

    def get_disposal_details(self,data):
        md = data.get("maindetails", {})

        return {
            "disposal_date": md.get("disposaldate"),
            "decided_by": md.get("judges")
        }

    # def get_parties_table(self,data):
    #     litigant = data.get("litigant", {})
    #     respondant = data.get("respondant", {})
    #     advocates = data.get("advocate", [])

    #     petitioners = []
    #     respondents = []

    #     # Separate advocates by type
    #     petitioner_advs = []
    #     respondent_advs = []

    #     for adv in advocates:
    #         if adv.get("litiganttypecode") == "1":
    #             petitioner_advs.append(
    #                 f"{adv.get('advocatename')} for: {adv.get('litiganttype')} {adv.get('namelist')}"
    #             )
    #         elif adv.get("litiganttypecode") == "2":
    #             respondent_advs.append(
    #                 f"{adv.get('advocatename')} for :{adv.get('litiganttype')} {adv.get('namelist')}"
    #             )

    #     # Petitioner row
    #     if litigant:
    #         petitioners.append({
    #             "sno": litigant.get("srno"),
    #             "name": litigant.get("litigantname"),
    #             "advocate_on_record": petitioner_advs
    #         })

    #     # Respondent row
    #     if respondant:
    #         respondents.append({
    #             "sno": respondant.get("srno"),
    #             "name": respondant.get("respondantname"),
    #             "advocate_on_record": respondent_advs
    #         })

    #     return {
    #         "petitioners": petitioners,
    #         "respondents": respondents
    #     }

    def normalize_to_list(self,value):
        if not value:
            return []
        if isinstance(value, list):
            return value
        if isinstance(value, dict):
            return [value]
        return []   # anything else (str, int, etc.)

    # def get_parties_table(self,data):
    #     litigants = self.normalize_to_list(data.get("litigant"))
    #     respondents_raw = self.normalize_to_list(data.get("respondant"))
    #     advocates = self.normalize_to_list(data.get("advocate"))
    #     # advocates = data.get("advocate", [])

    #     petitioners = []
    #     respondents = []

    #     # Group advocates by litiganttypecode
    #     adv_map = {"1": [], "2": []}

    #     for adv in advocates:
    #         code = adv.get("litiganttypecode")
    #         if code in adv_map:
    #             adv_map[code].append(
    #                 f"{adv.get('advocatename')} for: {adv.get('litiganttype')} {adv.get('namelist')}"
    #             )

    #     # Petitioners
    #     for l in litigants:
    #         petitioners.append({
    #             "sno": l.get("srno"),
    #             "name": l.get("litigantname"),
    #             "advocate_on_record": adv_map["1"]
    #         })

    #     # Respondents
    #     for r in respondents_raw:
    #         respondents.append({
    #             "sno": r.get("srno"),
    #             "name": r.get("respondantname"),
    #             "advocate_on_record": adv_map["2"]
    #         })

    #     return {
    #         "petitioners": petitioners,
    #         "respondents": respondents
    #     }

    def get_parties_table(self,data):
        litigants = self.normalize_to_list(data.get("litigant"))
        respondents_raw = self.normalize_to_list(data.get("respondant"))
        advocates = self.normalize_to_list(data.get("advocate"))

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

    def get_case_meta(self,data):
        md = data.get("maindetails", {})
        cls = data.get("classification", {})

        return {
            "presented_on": md.get("presentdate"),
            "registered_on": md.get("registrationdate"),

            "bench_category": md.get("benchname"),
            "district": md.get("districtname"),

            "case_originated_from": md.get("originname"),
            "purpose_of_listing": md.get("stagename"),

            "classification": cls.get("description")
        }

    # def get_court_proceedings(self,data):
    #     proceedings = []

    #     rows = data.get("linkedmatterscp", [])

    #     for idx, row in enumerate(rows, start=1):
    #         proceedings.append({
    #             "sno": idx,
    #             "notified_date": row.get("PROCEEDINGDATElmcp", "").strip(),
    #             "court_code": row.get("COURTCODElmcp", "").strip(),
    #             "board_sr_no": row.get("BOARDSRNOlmcp", "").strip(),
    #             "stage": row.get("STAGENAMElmcp", "").strip(),
    #             "action": row.get("ACTIONNAMElmcp", "").strip(),
    #             "coram": row.get("JUDGESlmcp", "").strip()
    #         })

    #     return proceedings

    def get_court_proceedings(self,data):
        proceedings = []

        rows = self.normalize_to_list(data.get("linkedmatterscp"))

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

    def get_optional_section(self,data, key, no_data_text):
        value = data.get(key)
        if not value or value == {}:
            return no_data_text
        return value

    def get_other_sections(self,data):
        return {

            "office_objections": self.get_optional_section(
                data,"officeobjection", "NO DATA FOR AVAILABLE ORDERS"),

            "available_orders": self.get_optional_section(
                data, "availableorders", "NO DATA FOR AVAILABLE ORDERS"
            ),

            "connected_matters": self.get_optional_section(
                data, "connectedmatters", "NO DATA FOR CONNECTED MATTERS"
            ),

            "application_appeal_matters": self.get_optional_section(
                data, "applicationappeal", "NO DATA FOR APPLICATION / APPEAL MATTERS"
            ),

            "ia_details": self.get_optional_section(
                data, "iadetails", "NO DATA FOR IA DETAILS"
            ),

            "office_details": self.get_optional_section(
                data, "officedetails", "NO DATA FOR OFFICE DETAILS"
            ),

            "certified_copy": self.get_optional_section(
                data, "certifiedcopy", "NO DATA FOR CERTIFIED COPY"
            ),

            "lower_court_detail": self.get_optional_section(
                data, "lowercourtdetail", "NO DATA FOR LOWERCOURT DETAIL"
            ),

            "fir_details": self.get_optional_section(
                data, "firdetails", "NO DATA FOR FIR DETAILS"
            ),

            "translated_orders_judgments": self.get_optional_section(
                data, "translatedorders", "NO DATA FOR TRANSLATION DETAILS"
            )
        }

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

    def fetchChallanDetails(self,res):
        try:
            if "Details not Found" in res.text:
                return "case details are not available"
            result = self.convertResRedableform(res.text)
            if result:
                final_response = {
                    
                    "case_header"       : self.get_case_header(result),
                    "disposal_details"  : self.get_disposal_details(result),
                    "parties"           : self.get_parties_table(result),
                    "case_meta"         : self.get_case_meta(result),
                    "court_proceedings" : self.get_court_proceedings(result),
                    "other_sections"    : self.get_other_sections(result)
                }
                return final_response
            else:
                return result
        except:
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

        case_list = []
        data = json.loads(res.text)

        finaldata = data["finaldata"][0]
        case_type_array = finaldata["casetypearray"]
        new_code = 1
        for group in case_type_array:
            for category, cases in group.items():
                for case in cases:

                    if str(new_code)==case_type_code:
                        print(case["casecode"])
                        break
                    new_code += 1

        return case_list
    






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

        for group in case_type_array:
            for category, cases in group.items():
                for case in cases:
                    case_list.append({
                            #"case_code": case["casecode"],
                            "case_type_code": new_code,
                            "case_type": '-'.join((case["casetype"],case["description"])),
                    })
                    new_code += 1
        return case_list
        
