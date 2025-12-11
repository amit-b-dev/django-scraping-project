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
            dynamic_id, trans_id, all_tr = self.extract.extract_receipt_button_for_timeline(soup)

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

            all_pages_soup = self.flow.get_all_pages_soup(soup,view_state,self.cookies)
            transactions,all_tr_for_s_no = self.extract.get_all_transaction_data(all_pages_soup)

            return {"transactions": transactions}
        except Exception:
            traceback.print_exc()
            return {"applications": []}

    def form29_via_s_no(self, reg_no, s_no):
        try:
            print("Enter form29_via_s_no function.....")
            upd_s_no=int(s_no)-1

            soup,view_state = self.common.prepare_context(reg_no)
            all_pages_soup = self.flow.get_all_pages_soup(soup,view_state,self.cookies)
            transactions,all_tr_for_s_no = self.extract.get_all_transaction_data(all_pages_soup)
            dynamic_id, trans_id = self.extract.extract_receipt_button(all_tr_for_s_no,upd_s_no)

            # POST requests print receipt
            url = "https://vahan.parivahan.gov.in/vahanservice/vahan/ui/eapplication/form_eAppCommonHomeLogin.xhtml"
            self.flow.open_receipt_page(url,view_state, dynamic_id, self.cookies)

            # get print receipt page
            url="https://vahan.parivahan.gov.in/vahanservice/vahan/ui/eapplication/formFeeRecieptPrintReport.xhtml"
            soup = self.flow.get_print_receipt_page(url, self.cookies)

            # Load receipt page
            form_29_btn_id, view_state,form_29_exists_or_not = self.extract.extract_form_29_button(soup)
            if form_29_exists_or_not:
                return {"applications": None, "message": "form 29 is not available"}
            
            url="https://vahan.parivahan.gov.in/vahanservice/vahan/ui/eapplication/formFeeRecieptPrintReport.xhtml"
            soup = self.flow.get_form_29_data(url,view_state,form_29_btn_id,trans_id,self.cookies)

            # Extract form 29
            data = self.extract.extract_form29(soup)

            return {"applications": data}

        except Exception:
            traceback.print_exc()
            return {"applications": []}

    # def form29_via_s_no1(self, reg_no):
    #     try:
    #         print("Enter form29_via_s_no function.....")

    #         soup,view_state = self.common.prepare_context(reg_no)

    #         # Extract table, receipt button
    #         upd_s_no = self.extract.get_all_transaction_data1(soup)
    #         if upd_s_no:
    #         # Extract dynamic_id, trans_id all_tr
    #             dynamic_id, trans_id, all_tr = self.extract.extract_receipt_button(soup,int(upd_s_no))

    #             # POST requests print receipt
    #             url = "https://vahan.parivahan.gov.in/vahanservice/vahan/ui/eapplication/form_eAppCommonHomeLogin.xhtml"
    #             self.flow.open_receipt_page(url,view_state, dynamic_id, self.cookies)

    #             # get print receipt page
    #             url="https://vahan.parivahan.gov.in/vahanservice/vahan/ui/eapplication/formFeeRecieptPrintReport.xhtml"
    #             soup = self.flow.get_print_receipt_page(url, self.cookies)

    #             # Load receipt page
    #             form_29_btn_id, view_state = self.extract.extract_form_29_button(soup)

    #             url="https://vahan.parivahan.gov.in/vahanservice/vahan/ui/eapplication/formFeeRecieptPrintReport.xhtml"
    #             soup = self.flow.get_form_29_data(url,view_state,form_29_btn_id,trans_id,self.cookies)

    #             # Extract form 29
    #             data = self.extract.extract_form29(soup)
                
    #             return {"applications": data}

    #         else:
    #             return {"applications": None, "message": "Form_29 is not available"}
            
    #     except Exception:
    #         traceback.print_exc()
    #         return {"applications": []}
