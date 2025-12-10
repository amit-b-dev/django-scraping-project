# scraper.py
import time, traceback
from bs4 import BeautifulSoup
from .navigation import NavigationFlow
from .parser import Extractor
import requests
from .common_flow import CommonFlow

class VahanScraper:
    def __init__(self):

        self.session = requests.Session()
        self.cookies = {}
        self.flow = NavigationFlow(self.session)
        self.extract = Extractor(self.session)
        self.common = CommonFlow(self.flow, self.extract, self.session)

    def init_homePage(self):
        url="https://vahan.parivahan.gov.in/vahanservice/vahan/ui/statevalidation/homepage.xhtml"
        soup1, view_state1, view_state2 = self.flow.load_homepage(url)
        cookies_dict = self.session.cookies.get_dict()
        self.cookies = {
                k: v for k, v in cookies_dict.items()
                if k in ("key", "JSESSIONID") or k.startswith("SERVERID_")
            }
        return  soup1, view_state1, view_state2,self.cookies
    
    def timeline_data(self, reg_no):
        try:
            print("Enter timeline data function.....")

            soup,view_state = self.common.prepare_context(reg_no)
            # Extract table, receipt button
            dynamic_id, trans_id, all_tr = self.extract.extract_receipt_button(soup)

            # POST requests print receipt
            url = "https://vahan.parivahan.gov.in/vahanservice/vahan/ui/eapplication/form_eAppCommonHomeLogin.xhtml"
            self.flow.open_receipt_page(url,view_state, dynamic_id, self.cookies)

            # get print receipt page
            url="https://vahan.parivahan.gov.in/vahanservice/vahan/ui/eapplication/formFeeRecieptPrintReport.xhtml"
            soup = self.flow.get_print_receipt_page(url, self.cookies)

            # Load receipt page
            table_data = self.extract.print_receipt_data(soup)
            return {"applications": table_data}

        except Exception:
            traceback.print_exc()
            return {"applications": []}

    def transaction_data(self, reg_no):
        try:
            print("Enter transaction_data function.....")
            soup,view_state = self.common.prepare_context(reg_no)

            # Extract table, receipt button
            transactions = self.extract.get_all_transaction_data(soup)
            
            return {"transactions": transactions}
        except Exception:
            traceback.print_exc()
            return {"applications": []}

    def form29_via_s_no(self, reg_no, s_no):
        try:
            print("Enter form29_via_s_no function.....")

            soup,view_state = self.common.prepare_context(reg_no)
            
            # Extract table rows
            all_tr = self.extract.get_all_transacton_rows(soup)

            # check the s_no is correct or not
            upd_s_no=int(s_no)-1
            if len(all_tr)<int(s_no):
                print("❌ please check the s_no")
                return {"applications": None, "message": "s_no is incorrect. please check the s_no"}
            
            # Extract dynamic_id, trans_id all_tr
            dynamic_id, trans_id, all_tr = self.extract.extract_receipt_button(soup,upd_s_no)

            # POST requests print receipt
            url = "https://vahan.parivahan.gov.in/vahanservice/vahan/ui/eapplication/form_eAppCommonHomeLogin.xhtml"
            self.flow.open_receipt_page(url,view_state, dynamic_id, self.cookies)

            # get print receipt page
            url="https://vahan.parivahan.gov.in/vahanservice/vahan/ui/eapplication/formFeeRecieptPrintReport.xhtml"
            soup = self.flow.get_print_receipt_page(url, self.cookies)

            # Load receipt page
            form_29_btn_id, view_state = self.extract.extract_form_29_button(soup)

            url="https://vahan.parivahan.gov.in/vahanservice/vahan/ui/eapplication/formFeeRecieptPrintReport.xhtml"
            soup = self.flow.get_form_29_data(url,view_state,form_29_btn_id,trans_id,self.cookies)

            # Extract form 29
            data = self.extract.extract_form29(soup)

            return {"applications": data}

        except Exception:
            traceback.print_exc()
            return {"applications": []}
