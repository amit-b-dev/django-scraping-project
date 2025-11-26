from django.shortcuts import render
from django.http import HttpResponse
# # warnings.simplefilter("ignore")
# from os import path
import traceback, time
# from pathlib import Path
from selenium import webdriver
# from datetime import datetime, timedelta
# from django.shortcuts import HttpResponse
from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from selenium.webdriver import ActionChains
import requests
import os
from pathlib import Path
import base64
from selenium.common.exceptions import TimeoutException
from datetime import datetime
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.wait import WebDriverWait
from django.http import JsonResponse
from collections import defaultdict
from rest_framework.decorators import api_view
from rest_framework.response import Response
import logging

logger = logging.getLogger(__name__)

base_dir = Path(__file__).resolve().parent.parent

# def setdriver():
#     # options = Options()
#     # # options.add_argument("--headless")
#     # options.set_preference("browser.download.dir",str(BASE_DIR))
#     # driver = webdriver.Firefox(options=options)

#     chrome_options = Options()
#     # chrome_options.add_argument("--headless")
#     chrome_options.add_argument("--start-maximized")
#     driver = webdriver.Chrome(options=chrome_options)
#     return driver

from django.views import View


class Vahan:

    def __init__(self, headless=False):
        chrome_options = Options()
        if headless:
            chrome_options.add_argument("--headless")
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--kiosk-printing")
        self.driver = webdriver.Chrome(options=chrome_options)

    def open_page(self, url):
        """Open the given URL in browser."""
        self.driver.get(url)
        time.sleep(5)

    def close(self):
        """Close the browser properly."""
        self.driver.quit()

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


    def solve_captcha_with_api(self, max_retries=10):
        driver = self.driver
        captcha_dir = "captcha_image"
        captcha_path = os.path.join(captcha_dir, "img.jpg")
        os.makedirs(captcha_dir, exist_ok=True)
    
        for attempt in range(1, max_retries):
            try:
                print(f"\n Solving CAPTCHA (Attempt {attempt}/{max_retries})...")

                # --- Capture CAPTCHA image ---
                captcha = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//img[@id='vhn_cap:ref_captcha']")))
                driver.execute_script("arguments[0].scrollIntoView();", captcha)
                time.sleep(1)
                captcha.screenshot(captcha_path)

                # --- Convert image to base64 for API ---
                with open(captcha_path, "rb") as image_file:
                    base64_image = base64.b64encode(image_file.read()).decode("utf-8")

                # --- Send to OCR API ---
                captcha_text = self.google_ocr(base64_image).strip()
                print(f" OCR Detected CAPTCHA: '{captcha_text}'")

                # --- Input CAPTCHA ---
                captcha_input = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//input[@id='vhn_cap:CaptchaID']")))
                captcha_input.clear()
                captcha_input.send_keys(captcha_text)

                # --- Click 'Show Details' button ---
                show_button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, 'tf_show_button')))
                ActionChains(driver).move_to_element(show_button).pause(0.8).click().perform()
                time.sleep(2)

                # --- Check for CAPTCHA error messages ---
                try:
                    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH,"//span[contains(text(),'Verification Code is missing') or contains(text(),'Verification code does not match')]")))
                    print(" CAPTCHA incorrect or missing — retrying...")
                    continue  # Retry loop

                except TimeoutException:
                    print(" CAPTCHA accepted successfully!")
                    if os.path.exists(captcha_path):
                        os.remove(captcha_path)
                    return True

            except Exception as e:
                print(f" Error on attempt {attempt}: {e}")
                time.sleep(2)

        print(" Failed to solve CAPTCHA after maximum retries.")
        return False

    
    def timeline_data(self,vehicle_no):
        try:
            popup_btn = WebDriverWait(self.driver,20).until(EC.presence_of_element_located((By.CLASS_NAME,'btn-close')))
            self.driver.execute_script('arguments[0].click()',popup_btn)
            # time.sleep(1)
            vehicle_reg_No_btn = WebDriverWait(self.driver,20).until(EC.presence_of_element_located((By.ID,'regnlinkid')))
            self.driver.execute_script('arguments[0].click()',vehicle_reg_No_btn)
            time.sleep(1)

            enter_reg_no = WebDriverWait(self.driver,20).until(EC.presence_of_element_located((By.ID,'regnid')))
            enter_reg_no.send_keys('MH28AB5366')
            # time.sleep(1)

            check_box = WebDriverWait(self.driver,20).until(EC.presence_of_element_located((By.XPATH,"//div[@class='ui-selectbooleancheckbox ui-chkbox ui-widget center-position']")))
            try:check_box.click()
            except:
                print('except')
                self.driver.execute_script('arguments[0].click()',check_box)
            time.sleep(1)

            proceed_btn = WebDriverWait(self.driver,20).until(EC.presence_of_element_located((By.ID,'proccedHomeButtonId')))
            self.driver.execute_script('arguments[0].click()',proceed_btn)
            # time.sleep(1)

            again_proceed_btn = WebDriverWait(self.driver,20).until(EC.presence_of_all_elements_located((By.XPATH,"//div[@class='ui-grid-col-12 right-position']/button[@class='ui-button ui-widget ui-state-default ui-corner-all ui-button-text-only']")))[0]
            self.driver.execute_script('arguments[0].click()',again_proceed_btn)
            # time.sleep(1)

            status_btn = WebDriverWait(self.driver,20).until(EC.presence_of_element_located((By.XPATH,"//a[contains(text(),'Status')]")))
            self.driver.execute_script('arguments[0].click()',status_btn)
            # time.sleep(1)

            reprint_btn = WebDriverWait(self.driver,20).until(EC.presence_of_element_located((By.XPATH,"//a[contains(text(),'Reprint Receipt/Form')]")))
            self.driver.execute_script('arguments[0].click()',reprint_btn)
            # time.sleep(1)

            reprint_receipt_btn = WebDriverWait(self.driver,20).until(EC.presence_of_element_located((By.XPATH,"//a[text()='Reprint Receipt']")))
            self.driver.execute_script('arguments[0].click()',reprint_receipt_btn)
            # time.sleep(1)

            reg_no_wise_btn = WebDriverWait(self.driver,20).until(EC.presence_of_element_located((By.XPATH,"//label[text()='Registration No. Wise']")))
            self.driver.execute_script('arguments[0].click()',reg_no_wise_btn)
            time.sleep(1)

            app_type = WebDriverWait(self.driver,20).until(EC.presence_of_element_located((By.ID,"app_type")))
            try:
                try:self.driver.execute_script('arguments[0].click()',check_box)
                except:ActionChains(self.driver).move_to_element(app_type).pause(0.8).click().perform()
            except:
                app_type.click()
            # time.sleep(4)

            sel_tran = WebDriverWait(self.driver,20).until(EC.presence_of_element_located((By.XPATH,"//li[text()='Application']")))
            self.driver.execute_script('arguments[0].click()',sel_tran)
            # time.sleep(1)

            app_type1 = WebDriverWait(self.driver,20).until(EC.presence_of_element_located((By.ID,"app_type1")))
            try:
                try:self.driver.execute_script('arguments[0].click()',app_type1)
                except:ActionChains(self.driver).move_to_element(app_type1).pause(0.8).click().perform()
            except:
                app_type1.click()
            time.sleep(1)

            sel_app = WebDriverWait(self.driver,20).until(EC.presence_of_element_located((By.XPATH,"//li[text()='RTO END']")))
            self.driver.execute_script('arguments[0].click()',sel_app)
            # time.sleep(1)

            enter_reg_no = WebDriverWait(self.driver,20).until(EC.presence_of_element_located((By.ID,'tf_reg_no11')))
            enter_reg_no.send_keys(vehicle_no)
            # time.sleep(1)

            enter_chasis_no = WebDriverWait(self.driver,20).until(EC.presence_of_element_located((By.ID,'tf_chasis_no1')))
            enter_chasis_no.send_keys('12345')
            # time.sleep(1)

            self.solve_captcha_with_api()

            # captcha = WebDriverWait(self.driver,20).until(EC.presence_of_element_located((By.XPATH,"//img[@id='vhn_cap:ref_captcha']")))
            # captcha.screenshot('captcha_image/img.png')
            # time.sleep(1)

            # captcha_input = WebDriverWait(self.driver,20).until(EC.presence_of_element_located((By.XPATH,"//input[@id='vhn_cap:CaptchaID']")))
            # captcha_input.send_keys('g8num5')
            # time.sleep(15)

            # show_button = WebDriverWait(self.driver,20).until(EC.presence_of_element_located((By.ID,'tf_show_button')))
            # self.driver.execute_script('arguments[0].click()',show_button)
            # from selenium.webdriver import ActionChains

            # ActionChains(self.driver).move_to_element(show_button).pause(1.5).click().perform()
            # # time.sleep(4)


            print_receipt_btn = WebDriverWait(self.driver,20).until(EC.presence_of_all_elements_located((By.XPATH,"//tbody[@id='tabView:tableTax_data']/tr")))[1].find_elements(By.TAG_NAME,'td')[-1].find_element(By.TAG_NAME,'span')
            # time.sleep(4)
            self.driver.execute_script("arguments[0].scrollIntoView();", print_receipt_btn)
            # time.sleep(5)
            ActionChains(self.driver).move_to_element(print_receipt_btn).pause(2).click().perform()
            # time.sleep(2)

            owner_name = WebDriverWait(self.driver,20).until(EC.presence_of_element_located((By.XPATH,"//label[text()='Owner Name: ']/parent::td/following-sibling::td/span"))).text.strip()
            chesis_no = WebDriverWait(self.driver,20).until(EC.presence_of_element_located((By.XPATH,"//label[text()='Chasis No:']/parent::td/following-sibling::td/span"))).text.strip()
            
            print_cmv_form_29 = WebDriverWait(self.driver,1).until(EC.presence_of_element_located((By.XPATH,"//span[text()='Print CMV form_29']")))
            self.driver.execute_script("arguments[0].click()", print_cmv_form_29)
            # time.sleep(10)
            self.driver.switch_to.window(self.driver.window_handles[1])
            # time.sleep(2)
            all_text = WebDriverWait(self.driver,15).until(EC.presence_of_all_elements_located((By.XPATH,"//div[@class='datatable-panel']//b")))
            b_texts = [el.text.strip() for el in all_text if el.text.strip()]
            try:
                formatted_date = datetime.strptime(f"{b_texts[2]} {b_texts[3]} {b_texts[4]}", "%d %b %Y").strftime("%Y-%m-%d")
            except ValueError as e:
                print('error',e)
            
            row_text = lambda id: b_texts[id] if id < len(b_texts) else None
            data = {
                "seller_name": row_text(0),
                "seller_address": row_text(1),
                "sold_date": formatted_date,
                "vehicle_no": row_text(5),
                "maker": row_text(6),
                "chassis_no": row_text(7),
                "engine_no": row_text(8),
                "buyer_name": row_text(9),
                "buyer_father_name": row_text(10),
                "buyer_address": row_text(11),
            }

            print(data)

            return {'applications':data}        
        except:
            traceback.print_exc()
            return None

@api_view(['POST'])
def vahan_timeline(request):
    try:
        vehicle_no = request.data.get("vehicle_no")
        print(vehicle_no,"aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")

        if not vehicle_no:
            return Response({"status": "error", "message": "vehicle_no is required"}, status=400)

        max_retries = 3
        retry_delay = 1

        for attempt in range(max_retries):

            # Get ViewState, Captcha, Cookies from your class
            # view_state, captcha_image, cookies, current_id = Vahan.get_viewstate_and_cookies()

            # Initialize scraper
            scraper = Vahan()
            
            # Open the target URL
            url = "https://vahan.parivahan.gov.in/vahanservice/vahan/ui/statevalidation/homepage.xhtml"
            scraper.open_page(url)

            
            response = scraper.timeline_data(vehicle_no)

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

@api_view(['POST'])
def vahan_detailed_list(request):
    try:
        vehicle_no = request.data.get("vehicle_no")
        print(vehicle_no,"aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")

        if not vehicle_no:
            return Response({"status": "error", "message": "vehicle_no is required"}, status=400)

        max_retries = 3
        retry_delay = 1

        for attempt in range(max_retries):

            # Get ViewState, Captcha, Cookies from your class
            # view_state, captcha_image, cookies, current_id = Vahan.get_viewstate_and_cookies()

            # Initialize scraper
            scraper = Vahan()
            
            # Open the target URL
            url = "https://vahan.parivahan.gov.in/vahanservice/vahan/ui/statevalidation/homepage.xhtml"
            scraper.open_page(url)

            
            response = scraper.timeline_data(vehicle_no)

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
