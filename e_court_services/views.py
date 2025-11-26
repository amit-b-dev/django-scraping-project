from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.wait import WebDriverWait
import os,requests,base64,warnings,logging,traceback,time,re
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from rest_framework.decorators import api_view
from rest_framework.response import Response
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from django.http import HttpResponse
from django.http import JsonResponse
from collections import defaultdict
from django.shortcuts import render
from selenium import webdriver
from datetime import datetime
from pathlib import Path
from bs4 import BeautifulSoup
import json
from lxml import html

warnings.simplefilter("ignore")
warnings.filterwarnings("ignore") 
logger = logging.getLogger(__name__)


class Vahan:

    BASE = "https://services.ecourts.gov.in/ecourtindia_v6/"
    IMG_BASE = "https://services.ecourts.gov.in"

    def __init__(self):

        self.session = requests.Session()
        self.headers = {
            "User-Agent": "Mozilla/5.0"
        }
        self.app_token = ""
        self.cookies = {}

        r = self.session.get(self.BASE, headers=self.headers)
        self.cookies = self.session.cookies.get_dict()

    def google_ocr(self,base64_image):
    
        api_key = "AIzaSyDCNRpug2TxiTP407h3frQH0GUH3LkFVoE"

        # Remove the "data:image/jpeg;base64," prefix if present
        if base64_image.startswith("data:image"):
            base64_image = base64_image.split(",")[1]

        url = f"https://vision.googleapis.com/v1/images:annotate?key={api_key}"
        payload = {
            "requests": [
                {
                    "image": {"content": base64_image},
                    "features": [{"type": "TEXT_DETECTION"}],
                }
            ]
        }
        headers = {"Content-Type": "application/json"}
        response = requests.post(url, json=payload, headers=headers)
        result = response.json()
        
        # Check for errors in the response
        if "error" in result:
            print("Error in API response:", result["error"]["message"])
            return ""
        
        try:
            if "responses" in result and "textAnnotations" in result["responses"][0]:
                return result["responses"][0]["textAnnotations"][0]["description"]
            else:
                print("No text detected in the image.")
                return ""
        except (KeyError, IndexError) as e:
            print("Unexpected response format:", result)
            return ""

    def get_captcha(self):
        try:
            captcha_dir = "captcha_image"
            captcha_path = os.path.join(captcha_dir, "img.jpg")
            os.makedirs(captcha_dir, exist_ok=True)

            """Fetch new captcha + app_token."""
            url = self.BASE + "casestatus/getCaptcha"
            data = {
                "ajax_req": "true",
                "app_token": ""
            }
            
            r = self.session.post(url, data=data, headers=self.headers)
            print("Captcha Status:", r.status_code)
            
            j = r.json()
            self.app_token = j.get("app_token")
            
            # Extract <img src="">
            html = j["div_captcha"]
            img_path = re.search(r'src="([^"]+)"', html).group(1)
            img_url = self.IMG_BASE + img_path
            
            time.sleep(1)
            img = self.session.get(img_url, headers=self.headers).content
            with open(captcha_path, "wb") as f:
                f.write(img)
            
            with open(captcha_path, "rb") as f:
                base64_image = base64.b64encode(f.read()).decode()
            
            captcha_text = self.google_ocr(base64_image).strip()
            print(f" OCR Detected CAPTCHA: '{captcha_text}'")
            
            print("Captcha saved: captcha.jpg")
            
            return self.app_token, captcha_text
        except:
            traceback.print_exc()
    
    def download_pdf(self,r,tree,h,pdf_no,t_no):
        try:
            pdf_dir = "pdf_folder"
            os.makedirs(pdf_dir, exist_ok=True)

            tables = tree.xpath("//table[@class='order_table table ']")
            rows = tables[t_no].xpath(".//tr")
            tds = rows[1].xpath("./td")
            a_tag = tds[2].xpath(".//a[contains(@onclick, 'displayPdf')]")[pdf_no]
            onclick = a_tag.xpath("./@onclick")[0]
            params = re.findall(r"'(.*?)'", onclick)
            j = r.json()
            app_token_pdf = j.get("app_token")

            normal_v   = params[0]
            case_val   = params[1]
            court_code = params[2]
            filename   = params[3]
            appFlag    = params[4]
            app_token  = app_token_pdf

            payload = {
                "normal_v": normal_v,
                "case_val": case_val,
                "court_code": court_code,
                "filename": filename,
                "appFlag": appFlag,
                "ajax_req": "true",
                "app_token": app_token
            }
            headers = {
                "User-Agent": "Mozilla/5.0",
                "X-Requested-With": "XMLHttpRequest",
                "Referer": "https://services.ecourts.gov.in/",
                "Origin": "https://services.ecourts.gov.in"
            }

            pdf_url = "https://services.ecourts.gov.in/ecourtindia_v6/home/display_pdf"
            pdf_response = self.session.post(pdf_url, data=payload, headers=headers)
            res_pdf = json.loads(pdf_response.text)
            full_pdf_url = self.BASE+res_pdf['order']
            pdf_name = str(h)+'_'+full_pdf_url.split('/')[-1]
            pdf_path = os.path.join(pdf_dir,pdf_name)
            time.sleep(0.5)
            img = self.session.get(full_pdf_url, headers=self.headers).content
            with open(pdf_path, "wb") as f:
                f.write(img)
            print("pdf downloaded successfully")
            
            j = pdf_response.json()
            app_token_pdf = j.get("app_token")
            return app_token_pdf
        except:
            traceback.print_exc()
            print("pdf issue")

    def get_case_history_status(self,r,tree,Order_Date,Court_Number,app_token1,srno):
        
        a_tag = tree.xpath("//a[@class='fw-bold text-underline text-success fst-italic']")
        parts=re.search(r"display_case_acknowlegement\('([^']+)'", a_tag[0].xpath("./@onclick")[0]).group(1).split('&')
        result = {"path": parts[0], **{p.split("=",1)[0]: p.split("=",1)[1] for p in parts[1:]}}

        url = "https://services.ecourts.gov.in/ecourtindia_v6/home/viewBusiness"
        payload = {
            "court_code": result['court_code'],
            "state_code": result['state_code'],
            "dist_code": result['state_code'],
            "nextdate1": "",
            "case_number1": result['cino'],
            "disposal_flag": "Disposed",
            "businessDate": Order_Date,
            "national_court_code": result['national_court_code'],
            "court_no": Court_Number,
            "search_by": "cnr",
            "srno": srno,
            "ajax_req": "true",
            "app_token": app_token1
        }

        headers = {
            "X-Requested-With": "XMLHttpRequest",
            "User-Agent": "Mozilla/5.0",
            "Referer": "https://services.ecourts.gov.in/",
            "Origin": "https://services.ecourts.gov.in",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
        }

        # MUST use valid session cookies

        r = self.session.post(url, data=payload, headers=headers)

        print(r.text)

    def search_cnr(self, cnr_no):
        try:
            app_token,captcha_text = self.get_captcha()

            """Search case details by CNR."""
            url = self.BASE + "cnr_status/searchByCNR/"
            form = {
                "cino": cnr_no,
                "fcaptcha_code": captcha_text,
                "ajax_req": "true",
                "app_token": app_token
            }
            
            r = self.session.post(url, data=form, headers=self.headers)        
            print("Search status:", r.status_code)

            res = json.loads(r.text)
            html_data = res["casetype_list"]
            tree = html.fromstring(html_data)

            tree.xpath("//td[contains(normalize-space(),'Filing Number')]/following-sibling::td[1]")[0].text.strip()
            case_type = tree.xpath("//td[contains(normalize-space(), 'Case Type')]/following-sibling::td[1]")[0].text_content().strip()

            filing_number = tree.xpath("//td[contains(normalize-space(),'Filing Number')]/following-sibling::td[1]")[0].text_content().strip()
            filing_date = tree.xpath("//td[contains(normalize-space(),'Filing Date')]/following-sibling::td[1]")[0].text_content().strip()
            registration_number = tree.xpath("//td[contains(normalize-space(),'Registration Number')]/following-sibling::td[1]")[0].text_content().strip()
            registration_date = tree.xpath("//td[contains(normalize-space(),'Registration Date')]/following-sibling::td[1]")[0].text_content().strip()
            cnr_number = tree.xpath("//td[contains(normalize-space(),'CNR Number')]/following-sibling::td[1]")[0].text_content().strip()
            e_filno = tree.xpath("//td[contains(normalize-space(),'e-Filno')]/following-sibling::td[1]")[0].text_content().strip()
            e_filing_date = tree.xpath("//td[contains(normalize-space(),'e-Filing Date')]/following-sibling::td[1]")[0].text_content().strip()

            First_Hearing_Date = tree.xpath("//td[contains(normalize-space(),'First Hearing Date')]/following-sibling::td[1]")[0].text_content().strip()
            Decision_Date = tree.xpath("//td[contains(normalize-space(),'Decision Date')]/following-sibling::td[1]")[0].text_content().strip()
            Case_Status  = tree.xpath("//td[contains(normalize-space(),'Case Status')]/following-sibling::td[1]")[0].text_content().strip()
            Nature_of_Disposal = tree.xpath("//td[contains(normalize-space(),'Nature of Disposal')]/following-sibling::td[1]")[0].text_content().strip()
            Judge = tree.xpath("//td[contains(normalize-space(),'Court Number and Judge')]/following-sibling::td[1]")[0].text_content().strip().split('-')[0]
            Court_Number = tree.xpath("//td[contains(normalize-space(),'Court Number and Judge')]/following-sibling::td[1]")[0].text_content().strip().split('-')[1]
            party_and_advocate = tree.xpath("//table[@class='table table-bordered Petitioner_Advocate_table']//tr/td")[0].text_content().replace("\xa0", " ").strip()
            party_name = party_and_advocate.lower().split('advocate-')[0].split(')')[1].strip()
            advocate_name = party_and_advocate.lower().split('advocate-')[1].strip()

            Respondent_and_Advocate = tree.xpath("//table[@class='table table-bordered Respondent_Advocate_table']//tr/td")[0].text_content().replace("\xa0", " ").strip()
            Under_Act = tree.xpath("//table[@id='act_table']//tr/td")[0].text_content().strip()
            Under_Section = tree.xpath("//table[@id='act_table']//tr/td")[0].text_content().strip()
            
            case_history = []
            for h in tree.xpath("//table[@class='history_table table ']//tbody/tr"):
                tds = h.xpath("./td")
                judge = tds[0].text_content().strip()
                business_on_date = tds[1].text_content().strip()
                hearing_date = tds[2].text_content().strip()
                purpose = tds[3].text_content().strip()

                case_history.append({
                    "judge": judge,
                    "business_on_date": business_on_date,
                    "hearing_date": hearing_date,
                    "purpose": purpose
                })
            
            Interim_Orders = []
            tables = tree.xpath("//table[@class='order_table table ']")
            rows = tables[0].xpath(".//tr")
            for h in range(1,len(rows)):
                tds = rows[h].xpath("./td")
                Order_Number = tds[0].text_content().strip()
                Order_Date = tds[1].text_content().strip()
                Order_Details = tds[2].text_content().strip()

                Interim_Orders.append({
                    "Order_Number": Order_Number,
                    "Order_Date": Order_Date,
                    "Order_Details": Order_Details
                })
                # app_token1 = self.download_pdf(r,tree,h,0,t_no=0)
                # srno=str(h-1)                
                # self.get_case_history_status(r,tree,Order_Date,Court_Number,app_token1,srno)
                


            Final_Orders_Judgements = []
            tables = tree.xpath("//table[@class='order_table table ']")
            rows = tables[1].xpath(".//tr")
            for h in range(1,len(rows)):
                tds = rows[h].xpath("./td")
                Order_Number = tds[0].text_content().strip()
                Order_Date = tds[1].text_content().strip()
                Order_Details = tds[2].text_content().strip()

                Final_Orders_Judgements.append({
                    "Order_Number": Order_Number,
                    "Order_Date": Order_Date,
                    "Order_Details": Order_Details
                })

                self.download_pdf(r,tree,h,1,t_no=1)
            

            
            # tree = html.fromstring(html_data)

            data = {
                    "Decision_Date": Decision_Date,
                    "Case_Status": Case_Status,
                    "Nature_of_Disposal": Nature_of_Disposal,
                    "Court_Number_and_Judge": '',
                    "party_name": party_name,
                    "advocate_name": advocate_name,
                    "Under_Act": Under_Act,
                    "Under_Section": Under_Section,
                    "case_type": case_type,
                    "filing_number": filing_number,
                    "filing_date": filing_date,
                    "registration_number": registration_number,
                    "registration_date": registration_date,
                    "cnr_number": cnr_number,
                    "e_filno": e_filno,
                    "e_filing_date": e_filing_date,
                    "First_Hearing_Date": First_Hearing_Date,
                    "case_history": case_history,
                    "Interim_Orders": Interim_Orders,
                    "Final_Orders_Judgements":Final_Orders_Judgements
                }

            return {"applications": data}
        except:
            traceback.print_exc()


@api_view(['POST'])
def e_court_services_cnr_no(request):
    try:
        CNR_No = request.data.get("CNR_No")
        if not CNR_No:
            return Response({"status": "error", "message": "vehicle_no is required"}, status=400)

        max_retries = 3
        retry_delay = 1
        for attempt in range(max_retries):

            scraper = Vahan()
            response = scraper.search_cnr(CNR_No)

            applications = response.get("applications", [])
            if applications:   # success → return immediately
                return Response({
                    "status": "success",
                    "data": applications,
                    # "cookies": cookies,
                    # "current_id": current_id,
                    # "total_pages": response.get("total_pages", 1)
                }, status=200)
            
            logger.warning(f"Attempt {attempt+1}: No data received, retrying...")
            if attempt < max_retries - 1:
                time.sleep(retry_delay)

        # After all retries
        return Response({"status": "success", "data": [], "message": "No Record found."})

    except Exception as e:
        logger.error(f"Error in vahan_get_result: {str(e)}", exc_info=True)
        return Response({"status": "error", "message": "Internal server error"}, status=500)
