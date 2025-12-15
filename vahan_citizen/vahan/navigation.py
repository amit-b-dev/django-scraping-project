import time, re, os
from bs4 import BeautifulSoup

from .headers import HeaderHelper
from .captcha import CaptchaSolver
from .headers import HeaderHelper


class NavigationFlow:
    def __init__(self, session):
        self.session = session
        self.solver = CaptchaSolver()

    def load_homepage(self,url):
        res = self.session.get(url, headers=HeaderHelper.home_page_header_fun())
        time.sleep(0.1)

        soup = BeautifulSoup(res.text, "html.parser")

        view_state1 = soup.find("input", {"id": "j_id1:javax.faces.ViewState:0"})["value"]
        view_state2 = soup.find("input", {"id": "j_id1:javax.faces.ViewState:15"})["value"]
        return soup, view_state1, view_state2

    def extract_homepage_ids(self, soup):
        check_box_id = soup.find(class_='ui-selectbooleancheckbox ui-chkbox ui-widget center-position')['id']
        input_id = soup.find(id='homepageformid').find_all('input')[1]['name']
        sele_input_id = soup.find(class_='ui-selectonemenu ui-widget ui-state-default ui-corner-all') \
                            .find('select')['id']
        return check_box_id, input_id, sele_input_id

    def submit_checkbox(self,url, check_box_id, input_id, sele_input_id,
                        reg_no, view_state1, view_state2, cookies):

        check_box_header,check_box_payload,proceed_btn_payload = HeaderHelper.check_box_header_fun(
            check_box_id, input_id, sele_input_id, reg_no, view_state1, view_state2
        )

        self.session.post(url, headers=check_box_header, data=check_box_payload, cookies=cookies)
        time.sleep(0.1)
        self.session.post(url, headers=check_box_header, data=proceed_btn_payload, cookies=cookies)
        time.sleep(0.1)

    def again_proceed(self,url, cookies):
        res = self.session.get(url, headers=HeaderHelper.again_proceed_btn_fun(),cookies=cookies)
        soup4 = BeautifulSoup(res.text, "html.parser")
        j_id1 = soup4.select_one("input[type=hidden][name*=j_idt]")['value']
        view_state = soup4.find("input", {"id": "j_id1:javax.faces.ViewState:0"}).get("value")
        tag = soup4.find("a", string="Reprint Receipt")
        onclick = tag.get("onclick")
        j_id2 = re.search(r"'(j_idt\d+)'", onclick).group(1)
        return view_state,j_id1,j_id2
    
    def load_login_page(self,url, view_state,j_id1,j_id2, cookies):
        userlogin_header,userlogin_payload = HeaderHelper.userlogin_fun(view_state,j_id1,j_id2)
        res = self.session.post(url, headers=userlogin_header, data=userlogin_payload, cookies=cookies)
        time.sleep(0.1)
        return res
    
    def form_eAppCommonHomeLogin_page(self,url, cookies):
        res = self.session.get(url, headers=HeaderHelper.form_eAppCommonHomeLogin_header(),cookies=cookies)
        time.sleep(0.1)
        soup = BeautifulSoup(res.text, "html.parser")
        view_state = soup.find("input", {"id": "j_id1:javax.faces.ViewState:0"}).get("value")
        return view_state,soup

    def select_registration_no_wise_fun(self, url, view_state, cookies):
        header, payload = HeaderHelper.registration_no_wise(view_state)
        r7 = self.session.post(url, headers=header,data=payload,cookies=cookies)
        time.sleep(0.1)
        match = re.search(r'<update id="j_id1:javax\.faces\.ViewState:0"><!\[CDATA\[(.*?)\]\]>',r7.text,re.S)
        view_state = match.group(1)

        return view_state
    
    def select_application(self,url,view_state, cookies):
        header,payload=HeaderHelper.select_application_header(view_state)
        res = self.session.post(url, headers=header,data=payload,cookies=cookies)
        time.sleep(0.1)
        xml = res.text
        match = re.search(r'<update id="j_id1:javax\.faces\.ViewState:0"><!\[CDATA\[(.*?)\]\]>',xml,re.S)
        view_state = match.group(1)

        return view_state
    
    def select_RTO_end(self,url,view_state, cookies):
        header,payload=HeaderHelper.select_RTO_end_header(view_state)
        r9 = self.session.post(url, headers=header,data=payload,cookies=cookies)
        time.sleep(0.1)
        xml = r9.text
        match = re.search(r'<update id="j_id1:javax\.faces\.ViewState:0"><!\[CDATA\[(.*?)\]\]>',xml,re.S)
        view_state = match.group(1)
        return view_state
    
    def get_captcha(self,soup, cookies):
        tag = soup.find("input", {"name": "vhn_cap:CaptchaID"})
        onblur_text = tag.get("onblur")
        match = re.search(r"CLIENT_BEHAVIOR_RENDERING_MODE':'(\w+)'", onblur_text)
        mode = match.group(1)

        captcha_tag = soup.find("img", id="vhn_cap:ref_captcha")
        captcha_url = "https://vahan.parivahan.gov.in" + captcha_tag["src"]
        header = HeaderHelper.captcha_img()
        img_res = self.session.get(captcha_url, headers=header,cookies=cookies)
        time.sleep(0.1)
        captcha_text,captcha_path,captcha_dir = self.solver.solve(img_res)
        return captcha_text,mode, captcha_path, captcha_dir
    
    def enter_captcha(self,url,view_state,captcha_text,mode,reg_no, cookies):
        
        header,payload=HeaderHelper.captcha_requests(view_state,captcha_text,mode,reg_no)
        r10 = self.session.post(url, data=payload, headers=header,cookies=cookies)
        time.sleep(0.1)
        xml = r10.text
        match = re.search(r'<update id="j_id1:javax\.faces\.ViewState:0"><!\[CDATA\[(.*?)\]\]>',xml,re.S)
        view_state = match.group(1)

        soup_xml = BeautifulSoup(r10.text, "xml")
        html_fragment = soup_xml.find("update", {"id": "vhn_cap:CaptchaID"}).string
        soup_html = BeautifulSoup(html_fragment, "html.parser")
        captcha_text = soup_html.find("input")["value"]

        return view_state, captcha_text

    def show_details(self, view_state, captcha_text, reg_no, cookies):
        print("Enter show details function.....")
        header,payload=HeaderHelper.click_on_show_details_fun(view_state,captcha_text,reg_no)
        url = "https://vahan.parivahan.gov.in/vahanservice/vahan/ui/eapplication/form_eAppCommonHomeLogin.xhtml"
        r11 = self.session.post(url, data=payload, headers=header,cookies=cookies)
        time.sleep(0.1)
        soup = BeautifulSoup(r11.text, "html.parser")
        view_state = soup.find("input", {"id": "j_id1:javax.faces.ViewState:0"}).get("value")
        return soup,view_state
    
    def open_receipt_page(self,url,view_state, dynamic_id, cookies):
        header,payload=HeaderHelper.click_on_print_receipt(view_state,dynamic_id)
        r12 = self.session.post(url, data=payload, headers=header,cookies=cookies)
        time.sleep(0.1)
    
    def get_print_receipt_page(self,url,cookies):
        print("Enter get_print_receipt_page function.....")

        header=HeaderHelper.print_receipt_page_header()
        r12 = self.session.post(url, headers=header,cookies=cookies)
        time.sleep(0.1)
        soup = BeautifulSoup(r12.text, "html.parser")
        return soup

    def get_form_29_data(self,url,view_state,form_29_btn_id,trans_id,cookies):
        print("Enter get_form_29_data function.....")
        
        header,payload=HeaderHelper.form_29_data_header(view_state,form_29_btn_id,trans_id)
        r15 = self.session.post(url, data=payload, headers=header,cookies=cookies)
        time.sleep(0.1)
        soup = BeautifulSoup(r15.text, "html.parser")
        return soup
    
    def get_all_pages_soup_for_transaction_data(self,soup,view_state,cookies):
        print("Enter get_all_pages_soup function.....")
        url = "https://vahan.parivahan.gov.in/vahanservice/vahan/ui/eapplication/form_eAppCommonHomeLogin.xhtml"
        view_state = soup.find("input", {"id": "j_id1:javax.faces.ViewState:0"}).get("value")
        pages = soup.find(class_='ui-paginator-pages').find_all('a')
        last_page_no = soup.find(id='tabView:tableTax_data').find_all('tr')[-1].find('td').get_text(strip=True)
        all_pages_soup = []
        all_pages_soup.append(soup)
        for _ in range(1,len(pages)):
            header,payload=HeaderHelper.pagination_header(view_state,last_page_no)
            res = self.session.post(url, data=payload, headers=header,cookies=cookies)
            time.sleep(0.1)
            soup_xml = BeautifulSoup(res.text, "xml")
            html_fragment = soup_xml.find("update", {"id": "tabView:tableTax"}).string
            soup = BeautifulSoup(html_fragment, "html.parser")
            all_pages_soup.append(soup)
            last_page_no = soup.find_all('tr')[-1].find('td').get_text(strip=True)
        return all_pages_soup

    def get_all_pages_soup(self,soup,view_state,cookies,upd_s_no):
        print("Enter get_all_pages_soup function.....")
        upd_s_no+=1
        url = "https://vahan.parivahan.gov.in/vahanservice/vahan/ui/eapplication/form_eAppCommonHomeLogin.xhtml"
        view_state = soup.find("input", {"id": "j_id1:javax.faces.ViewState:0"}).get("value")
        pages = soup.find(class_='ui-paginator-pages').find_all('a')
        last_page_no = soup.find(id='tabView:tableTax_data').find_all('tr')[-1].find('td').get_text(strip=True)
        all_pages_soup = []
        all_pages_soup.append(soup)
        for _ in range(1,len(pages)):
            if upd_s_no<=int(last_page_no):
                break
            header,payload=HeaderHelper.pagination_header(view_state,last_page_no)
            res = self.session.post(url, data=payload, headers=header,cookies=cookies)
            xml = res.text
            match = re.search(r'<update id="j_id1:javax\.faces\.ViewState:0"><!\[CDATA\[(.*?)\]\]>',xml,re.S)
            view_state = match.group(1)
            time.sleep(0.1)
            soup_xml = BeautifulSoup(res.text, "xml")
            html_fragment = soup_xml.find("update", {"id": "tabView:tableTax"}).string
            soup = BeautifulSoup(html_fragment, "html.parser")
            all_pages_soup.append(soup)
            last_page_no = soup.find_all('tr')[-1].find('td').get_text(strip=True)

        return all_pages_soup,view_state
