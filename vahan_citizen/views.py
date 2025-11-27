from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.wait import WebDriverWait
import os,requests,base64,warnings,logging,traceback,time
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

warnings.simplefilter("ignore")
warnings.filterwarnings("ignore") 

logger = logging.getLogger(__name__)
# base_dir = Path(__file__).resolve().parent.parent

class Vahan:

    def __init__(self, driver=None):

        if driver:
            self.driver = driver
        else:
            chrome_options = Options() 
            chrome_options.add_argument("--headless=new")          # modern headless
            # chrome_options.add_argument("--kiosk-printing")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--log-level=3")           # remove logs
            chrome_options.add_argument("--silent")                # remove warnings
            chrome_options.add_argument("--disable-logging")       # suppress logging
            chrome_options.add_experimental_option("excludeSwitches", ["enable-logging", "enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            chrome_options.add_argument("--window-size=1280,800")

            self.driver = webdriver.Chrome(options=chrome_options)

    def reset_browser_session(self):
        try:
            # Delete cookies
            self.driver.delete_all_cookies()

            # Clear storage
            self.driver.execute_script("window.localStorage.clear();")
            self.driver.execute_script("window.sessionStorage.clear();")

            # Clear cache
            self.driver.execute_cdp_cmd('Network.clearBrowserCache', {})
            self.driver.execute_cdp_cmd('Network.clearBrowserCookies', {})

            # Optional deep-clean
            self.driver.execute_script("""
            indexedDB.databases().then(dbs => {
                dbs.forEach(db => indexedDB.deleteDatabase(db.name));
            });
            """)
            self.driver.execute_script("""
            caches.keys().then(keys => {
                keys.forEach(key => caches.delete(key));
            });
            """)

            print("🔥 Browser session fully reset (fresh state).")
        except Exception as e:
            print("Error while resetting session:", e)

    def open_page(self, url):
        """Open the given URL in browser."""
        self.driver.get(url)
        # time.sleep(5)

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

    def clean_captcha(self, captcha_path):
        import cv2
        import numpy as np

        img = cv2.imread(captcha_path)
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        lower_yellow = np.array([20, 80, 80])
        upper_yellow = np.array([35, 255, 255])
        mask = cv2.inRange(hsv, lower_yellow, upper_yellow)

        # Skip inpainting if no line
        if cv2.countNonZero(mask) < 50:
            cv2.imwrite(captcha_path, img)
            return

        cleaned = cv2.inpaint(img, mask, 3, cv2.INPAINT_NS)   # faster
        cv2.imwrite(captcha_path, cleaned)

    def solve_captcha_with_api(self, max_retries=10):
        driver = self.driver
        captcha_dir = "captcha_image"
        captcha_path = os.path.join(captcha_dir, "img.jpg")
        os.makedirs(captcha_dir, exist_ok=True)

        error_xpath = "//span[contains(text(),'Verification Code is missing') or contains(text(),'Verification code does not match')]"
        success_xpath = "//tbody[@id='tabView:tableTax_data']/tr"   # element that appears ONLY when captcha is correct

        for attempt in range(1, max_retries + 1):
            try:
                print(f"\n Solving CAPTCHA (Attempt {attempt}/{max_retries})...")

                # ---------------- GET CAPTCHA IMAGE ----------------
                captcha = WebDriverWait(driver, 15).until(
                    EC.presence_of_element_located((By.ID, "vhn_cap:ref_captcha"))
                )

                driver.execute_script("arguments[0].scrollIntoView();", captcha)
                time.sleep(0.15)

                captcha.screenshot(captcha_path)
                self.clean_captcha(captcha_path)

                with open(captcha_path, "rb") as f:
                    base64_image = base64.b64encode(f.read()).decode()

                captcha_text = self.google_ocr(base64_image).strip()
                print(f" OCR Detected CAPTCHA: '{captcha_text}'")

                # ---------------- ENTER CAPTCHA ----------------
                captcha_input = driver.find_element(By.ID, "vhn_cap:CaptchaID")
                captcha_input.clear()
                captcha_input.send_keys(captcha_text)

                # ---------------- CLICK SHOW BUTTON ----------------
                show_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.ID, 'tf_show_button'))
                )
                driver.execute_script("arguments[0].scrollIntoView();", show_button)
                ActionChains(driver).move_to_element(show_button).pause(0.2).click().perform()
                time.sleep(0.2)

                # ---------------- SMART FAST CHECK ----------------
                start = time.time()
                timeout = 0.6   

                while time.time() - start < timeout:

                    # SUCCESS (No Wait)
                    if driver.find_elements(By.XPATH, success_xpath):
                        print(" CAPTCHA accepted instantly! ✓")
                        if os.path.exists(captcha_path):
                            os.remove(captcha_path)
                        return True

                    # ERROR (Instant retry)
                    if driver.find_elements(By.XPATH, error_xpath):
                        print(" CAPTCHA incorrect — retrying... ✗")
                        break

                    time.sleep(0.03)  # 30ms micro wait

                # If loop ended without success & without error → treat as error
                # This happens when Vahan is slow or OCR wrong
                print(" No success detected — retrying...")
                continue

            except Exception as e:
                print("Error:", e)
                continue

        # After all retries
        print("Failed after max retries.")
        return False
    
    def navigate_to_reprint(self, vehicle_no):
        try:

            def safe_click(element):
                """Try JS click → normal click → ActionChains click."""
                try:
                    self.driver.execute_script("arguments[0].click()", element)
                except:
                    try:
                        ActionChains(self.driver).move_to_element(element).pause(0.3).click().perform()
                    except:
                        element.click()

            # ---------------------------- CLOSE POPUP -----------------------------
            popup_btn = WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Close']")))
            try:
                popup_btn.click()
                # self.driver.execute_script('arguments[0].click()',popup_btn)
            except:
                pass
            time.sleep(0.4)
            # safe_click(popup_btn)

            # ---------------------------- ENTER REG NO ----------------------------
            reg_input = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.ID, 'regnid'))
            )
            try:reg_input.send_keys("MH28AB5366")
            except:
                time.sleep(0.1)
                popup_btn = WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Close']")))
                popup_btn.click()
            time.sleep(0.2)

            # ---------------------------- CLICK CHECKBOX ---------------------------
            checkbox = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH,"//div[@class='ui-selectbooleancheckbox ui-chkbox ui-widget center-position']")))
            checkbox.click()

            # ---------------------------- PROCEED BUTTON ---------------------------
            for _ in range(15):
                try:
                    proceed_btn = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.ID, 'proccedHomeButtonId')))
                    if "disabled" not in proceed_btn.get_attribute("class"):
                        break
                    time.sleep(0.1)
                except:
                    pass

            safe_click(proceed_btn)
            time.sleep(0.3)

            again_proceed = WebDriverWait(self.driver, 20).until(EC.presence_of_all_elements_located((By.XPATH,"//div[@class='ui-grid-col-12 right-position']/button")))[0]
            safe_click(again_proceed)

            # ---------------------------- NAVIGATION MENU --------------------------
            safe_click(WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//a[normalize-space(text())='Status']"))))
            safe_click(WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(),'Reprint Receipt/Form')]"))))
            safe_click(WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//a[text()='Reprint Receipt']"))))
            safe_click(WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//label[text()='Registration No. Wise']"))))

            # ---------------------------- SELECT DROPDOWNS ------------------------
            app_type = WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='ui-outputpanel ui-widget']/div[@class='ui-grid-row top-space']//div[@id='app_type']")))
            try:
                app_type.click()
                self.driver.execute_script('arguments[0].click()',app_type)
            except:
                pass
            # safe_click(app_type)

            time.sleep(0.5)
            app_option = WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//li[text()='Application']")))
            safe_click(app_option)
            time.sleep(0.5)

            self.driver.find_element(By.ID, "app_type1").click()
            self.driver.find_element(By.XPATH, "//li[contains(text(),'RTO END')]").click()

            # ---------------------------- ENTER VEHICLE + CHASSIS -------------------
            reg2 = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.ID, 'tf_reg_no11')))
            reg2.send_keys(vehicle_no)

            chassis_input = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.ID, 'tf_chasis_no1')))
            chassis_input.send_keys("12345")

            # ---------------------------- SOLVE CAPTCHA ----------------------------
            self.solve_captcha_with_api()

            return True
        except:
            traceback.print_exc()
            return False

    def timeline_data(self, vehicle_no):
        try:
            if not self.navigate_to_reprint(vehicle_no):
                return {}

            # extract form 29
            rows = WebDriverWait(self.driver,20).until(
                EC.presence_of_all_elements_located((By.XPATH,"//tbody[@id='tabView:tableTax_data']/tr"))
            )
            print_btn = rows[0].find_elements(By.TAG_NAME,'td')[-1].find_element(By.TAG_NAME,'span')
            self.driver.execute_script("arguments[0].scrollIntoView()", print_btn)
            print_btn.click()

            owner_name = WebDriverWait(self.driver,10).until(EC.presence_of_element_located((By.XPATH,"//label[text()='Owner Name: ']/parent::td/following-sibling::td/span"))).text.strip()
            chesis_no = self.driver.find_element(By.XPATH,"//label[text()='Chasis No:']/parent::td/following-sibling::td/span").text.strip()
            application_and_receipt_no = self.driver.find_element(By.XPATH,"//label[text()='Application No./RECEIPT No:']/parent::td/following-sibling::td/span").text.strip()
            receipt_date = self.driver.find_element(By.XPATH,"//label[text()='Receipt Date:']/parent::td/following-sibling::td/span").text.strip()
            vehicle_class = self.driver.find_element(By.XPATH,"//label[text()='Vehicle Class:']/parent::td/following-sibling::td/span").text.strip()
            vehicle_no = self.driver.find_element(By.XPATH,"//label[text()='Vehicle No:']/parent::td/following-sibling::td/span").text.strip()
            vehicle_registration_date = self.driver.find_element(By.XPATH,"//label[text()='Vehicle Registration Date:']/parent::td/following-sibling::td/span").text.strip()
            payment_transaction_no = self.driver.find_element(By.XPATH,"//label[text()='Payment Transaction No:']/parent::td/following-sibling::td/span").text.strip()
            grn_no = self.driver.find_element(By.XPATH,"//label[text()='GRN No:']/parent::td/following-sibling::td/span").text.strip()
            bank_reference_number = self.driver.find_element(By.XPATH,"//label[text()='Bank Reference Number:']/parent::td/following-sibling::td/span").text.strip()
            servicing_authority = self.driver.find_element(By.XPATH,"//label[text()='Servicing Authority:']/parent::td/following-sibling::td/span").text.strip()
            
            headers = self.driver.find_elements(By.XPATH, "//div[@class='ui-datatable-tablewrapper']//thead/tr//span")
            columns = [h.text.strip() for h in headers]
            rows = self.driver.find_elements(By.XPATH, "//div[@class='ui-datatable-tablewrapper']//tbody/tr")
            table_rows = []
            for row in rows:
                cols = row.find_elements(By.TAG_NAME, "td")
                row_data = [col.text.strip() for col in cols]
                table_rows.append(row_data)
            fee_details = [dict(zip(columns, row)) for row in table_rows]

            grand_total = self.driver.find_element(By.XPATH,"//span[text()='GRAND TOTAL (in Rs):']/following-sibling::span").text.strip()
            
            final_data = {
                    "owner_name": owner_name,
                    "chesis_no": chesis_no,
                    "application_and_receipt_no": application_and_receipt_no,
                    "receipt_date": receipt_date,
                    "vehicle_class": vehicle_class,
                    "vehicle_no": vehicle_no,
                    "vehicle_registration_date": vehicle_registration_date,
                    "payment_transaction_no": payment_transaction_no,
                    "grn_no": grn_no,
                    "bank_reference_number": bank_reference_number,
                    "servicing_authority": servicing_authority,
                    "fees_details":fee_details,
                    "grand_total":grand_total

                }

            return {"applications": final_data}

        except:
            traceback.print_exc()
            return {}

    def transaction_data(self, vehicle_no):
        try:
            if not self.navigate_to_reprint(vehicle_no):
                return {}

            rows = WebDriverWait(self.driver,20).until(
                EC.presence_of_all_elements_located((By.XPATH,"//tbody[@id='tabView:tableTax_data']/tr"))
            )

            transactions = []
            for tr in rows:
                tds = tr.find_elements(By.TAG_NAME,"td")
                if len(tds) < 7:
                    continue

                transaction = {
                    "Sl No": tds[0].text.strip(),
                    "Regn No": tds[1].text.strip(),
                    "Trans Desc": tds[2].text.strip(),
                    "Trans ID": tds[3].text.strip(),
                    "Trans Amt": tds[4].text.strip(),
                    "Trans Date": tds[5].text.strip(),
                    "Status": tds[6].text.strip()
                }
                transactions.append(transaction)

            return {"transactions": transactions}

        except:
            traceback.print_exc()
            return {}

    def timeline_data_via_s_no(self, vehicle_no,s_no):
        try:
            upd_s_no=int(s_no)-1
            if not self.navigate_to_reprint(vehicle_no):
                return {}

            # extract form 29
            rows = WebDriverWait(self.driver,20).until(
                EC.presence_of_all_elements_located((By.XPATH,"//tbody[@id='tabView:tableTax_data']/tr"))
            )
            if len(rows)<int(s_no):
                print("❌ please check the s_no")
                return {"applications": None, "message": "s_no is incorrect. please check the s_no"}
            print_btn = rows[upd_s_no].find_elements(By.TAG_NAME,'td')[-1].find_element(By.TAG_NAME,'span')
            self.driver.execute_script("arguments[0].scrollIntoView()", print_btn)
            print_btn.click()

            # owner_name = WebDriverWait(self.driver,20).until(EC.presence_of_element_located((By.XPATH,"//label[text()='Owner Name: ']/parent::td/following-sibling::td/span"))).text.strip()
            # chesis_no = WebDriverWait(self.driver,20).until(EC.presence_of_element_located((By.XPATH,"//label[text()='Chasis No:']/parent::td/following-sibling::td/span"))).text.strip()
            # print(owner_name)

            try:
                form29_btn = WebDriverWait(self.driver,2).until(EC.element_to_be_clickable((By.XPATH,"//span[text()='Print CMV form_29']")))
            except:
                print("❌ Form_29 not available for this vehicle")
                return {"applications": None, "message": "Form_29 is not available"}
            
            form29_btn = WebDriverWait(self.driver,10).until(EC.element_to_be_clickable((By.XPATH,"//span[text()='Print CMV form_29']")))
            self.driver.execute_script("arguments[0].scrollIntoView()", form29_btn)
            form29_btn.click()

            self.driver.switch_to.window(self.driver.window_handles[1])

            labels = WebDriverWait(self.driver,15).until(

                EC.presence_of_all_elements_located((By.XPATH,"//div[@class='datatable-panel']//b"))
            )
            txt = [el.text.strip() for el in labels]

            data = {
                "seller_name": txt[0],
                "seller_address": txt[1],
                "sold_date": txt[2] + " " + txt[3] + " " + txt[4],
                "vehicle_no": txt[5],
                "maker": txt[6],
                "chassis_no": txt[7],
                "engine_no": txt[8],
                "buyer_name": txt[9],
                "buyer_father_name": txt[10],
                "buyer_address": txt[11],
            }

            return {"applications": data}

        except:
            traceback.print_exc()
            return {}



print("🔥 Starting global Vahan driver...")
GLOBAL_VAHAN_DRIVER = Vahan().driver
print("🔥 Global Vahan driver ready!")

@api_view(['POST'])
def vahan_timeline(request):
    try:
        vehicle_no = request.data.get("vehicle_no")
        if not vehicle_no:
            return Response({"status": "error", "message": "vehicle_no is required"}, status=400)

        max_retries = 3
        retry_delay = 1
        for attempt in range(max_retries):

            # Get ViewState, Captcha, Cookies from your class
            # view_state, captcha_image, cookies, current_id = Vahan.get_viewstate_and_cookies()

            # Initialize scraper and use global driver
            scraper = Vahan(driver=GLOBAL_VAHAN_DRIVER)

            # Open the target URL
            url = "https://vahan.parivahan.gov.in/vahanservice/vahan/ui/statevalidation/homepage.xhtml"
            scraper.open_page(url)
            response = scraper.timeline_data(vehicle_no)

            driver=GLOBAL_VAHAN_DRIVER
            if len(driver.window_handles)>1:
                driver.close()
                driver.switch_to.window(driver.window_handles[0])
            scraper.reset_browser_session()


            applications = response.get("applications", [])
            if applications:   # success → return immediately
                return Response({
                    "status": "success",
                    "data": applications,
                    # "cookies": cookies,
                    # "current_id": current_id,
                    # "total_pages": response.get("total_pages", 1)
                }, status=200)
            
            if not applications and response.get("message") == "Form_29 is not available":
                return Response({
                    "status": "success",  
                    "data": [],
                    "message": "Form_29 is not available",
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
def vahan_timeline_via_s_no(request):
    try:
        vehicle_no = request.data.get("vehicle_no")
        s_no = request.data.get("s_no")
        if not vehicle_no:
            return Response({"status": "error", "message": "vehicle_no is required"}, status=400)

        max_retries = 3
        retry_delay = 1
        for attempt in range(max_retries):

            # Get ViewState, Captcha, Cookies from your class
            # view_state, captcha_image, cookies, current_id = Vahan.get_viewstate_and_cookies()

            # Initialize scraper and use global driver
            scraper = Vahan(driver=GLOBAL_VAHAN_DRIVER)

            # Open the target URL
            url = "https://vahan.parivahan.gov.in/vahanservice/vahan/ui/statevalidation/homepage.xhtml"
            scraper.open_page(url)
            response = scraper.timeline_data_via_s_no(vehicle_no,s_no)

            driver=GLOBAL_VAHAN_DRIVER
            if len(driver.window_handles)>1:
                driver.close()
                driver.switch_to.window(driver.window_handles[0])
            scraper.reset_browser_session()


            applications = response.get("applications", [])
            if applications:   # success → return immediately
                return Response({
                    "status": "success",
                    "data": applications,
                    # "cookies": cookies,
                    # "current_id": current_id,
                    # "total_pages": response.get("total_pages", 1)
                }, status=200)
            
            if not applications and response.get("message") == "Form_29 is not available":
                return Response({"status": "success",  
                                 "data": [],
                                 "message": "Form_29 is not available",
                                 }, status=200)
            
            if not applications and response.get("message") == "s_no is incorrect. please check the s_no":
                return Response({"status": "success",  
                                 "data": [],
                                 "message": "s_no is incorrect. please check the s_no",
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
def vahan_transactions_list(request):
    try:
        vehicle_no = request.data.get("vehicle_no")
        if not vehicle_no:
            return Response({"status": "error", "message": "vehicle_no is required"}, status=400)

        max_retries = 3
        retry_delay = 1
        for attempt in range(max_retries):

            # Get ViewState, Captcha, Cookies from your class
            # view_state, captcha_image, cookies, current_id = Vahan.get_viewstate_and_cookies()

            # Initialize scraper
            # use global driver
            scraper = Vahan(driver=GLOBAL_VAHAN_DRIVER)

            # Open the target URL
            url = "https://vahan.parivahan.gov.in/vahanservice/vahan/ui/statevalidation/homepage.xhtml"
            start_time2 = datetime.now()
            scraper.open_page(url)
            response = scraper.transaction_data(vehicle_no)

            driver=GLOBAL_VAHAN_DRIVER
            scraper.reset_browser_session()


            transactions = response.get("transactions", [])
            if transactions:   # success → return immediately
                return Response({
                    "status": "success",
                    "data": transactions,
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
