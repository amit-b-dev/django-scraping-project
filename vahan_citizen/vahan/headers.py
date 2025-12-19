class HeaderHelper:

    def home_page_header_fun(): 
        home_page_header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:145.0) Gecko/20100101 Firefox/145.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
        }
        return home_page_header

    def check_box_header_fun(check_box_id, input_id, sele_input_id, reg_no, view_state1, view_state2):
        check_box_header = {
            "User-Agent": "Mozilla/5.0",
            "Faces-Request": "partial/ajax",
            "X-Requested-With": "XMLHttpRequest",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Referer" :"https://vahan.parivahan.gov.in/vahanservice/vahan/ui/statevalidation/homepage.xhtml"
            }
        check_box_payload = {
            "javax.faces.partial.ajax": "true",
            "javax.faces.source": check_box_id,
            "javax.faces.partial.execute": check_box_id,
            "javax.faces.partial.render": "proccedHomeButtonId",
            "javax.faces.behavior.event": "change",
            "javax.faces.partial.event": "change",

            "homepageformid": "homepageformid",
            input_id: "",
            sele_input_id: "en",
            "regnid": reg_no,
            "state_cd_filter": "",
            "fit_c_office_to_filter": "",
            check_box_id+"_input": "on",   # checkbox
            "abc": "abc",
            "javax.faces.ViewState": view_state1
            }
        proceed_btn_payload = {
            "javax.faces.partial.ajax": "true",
            "javax.faces.source": "proccedHomeButtonId",
            "javax.faces.partial.execute": "@all",
            "javax.faces.partial.render": "regnid+facelesslist+portaldownMsgPnl+mainhomepagepnl+leftmenupnlid+leftmenupnlidservdown",

            "proccedHomeButtonId": "proccedHomeButtonId",

            "homepageformid": "homepageformid",
            input_id: "",
            sele_input_id: "en",
            "regnid": reg_no,
            "state_cd_filter": "",
            "fit_c_office_to_filter": "",
            check_box_id: "on",
            "abc": "abc",
            "javax.faces.ViewState": view_state1,
            "javax.faces.ViewState": view_state2,
            "pmtchk_input": "-1",
            "nocregnno": ""
            }
        return check_box_header,check_box_payload,proceed_btn_payload
    
    def again_proceed_btn_fun():
        again_proceed_btn_header = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "en-US,en;q=0.5",
            "Connection": "keep-alive",
            "Host": "vahan.parivahan.gov.in",
            "Priority": "u=0, i",
            "Referer": "https://vahan.parivahan.gov.in/vahanservice/vahan/ui/statevalidation/homepage.xhtml",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-User": "?1",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0",
            }
        return again_proceed_btn_header
    
    def userlogin_fun(view_state,j_id1,j_id2):
        userlogin_header = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "en-US,en;q=0.5",
        "Connection": "keep-alive",
        "Content-Type": "application/x-www-form-urlencoded",
        "Host": "vahan.parivahan.gov.in",
        "Origin": "https://vahan.parivahan.gov.in",
        "Referer": "https://vahan.parivahan.gov.in/vahanservice/vahan/ui/usermgmt/login.xhtml?faces-redirect=true",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0",
        "Priority": "u=0, i"
        }
        userlogin_payload = {
        "loginForm": "loginForm",
        j_id1: j_id1,
        "javax.faces.ViewState": view_state,
        "InputEnter": "",
        j_id2: j_id2,
        "pur_cd": "952",
        }
        return userlogin_header,userlogin_payload

    def form_eAppCommonHomeLogin_header():
        header = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "en-US,en;q=0.5",
        "Connection": "keep-alive",
        "Content-Type": "application/x-www-form-urlencoded",
        "Host": "vahan.parivahan.gov.in",
        "Origin": "https://vahan.parivahan.gov.in",
        "Referer": "https://vahan.parivahan.gov.in/vahanservice/vahan/ui/usermgmt/login.xhtml?faces-redirect=true",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0",
        "Priority": "u=0, i"
        }
        return header

    def registration_no_wise(view_state):
        payload = {
            "javax.faces.partial.ajax": "true",
            "javax.faces.source": "statusRadio1",
            "javax.faces.partial.execute": "statusRadio1",
            "javax.faces.partial.render": "rcpt_pnl tf_regen_panel_One",
            "javax.faces.behavior.event": "change",
            "javax.faces.partial.event": "change",
            "form_eapp": "form_eapp",
            "statusRadio1": "4",
            "app_type_input": "-1",
            "app_type1_input": "-1",
            "tf_tran_rep1": "",
            "vhn_cap:CaptchaID": "",
            "javax.faces.ViewState": view_state,
        }

        header = {
            "Accept": "application/xml, text/xml, */*; q=0.01",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "en-US,en;q=0.5",
            "Connection": "keep-alive",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Faces-Request": "partial/ajax",
            "Host": "vahan.parivahan.gov.in",
            "Origin": "https://vahan.parivahan.gov.in",
            "Priority": "u=0",
            "Referer": "https://vahan.parivahan.gov.in/vahanservice/vahan/ui/eapplication/form_eAppCommonHomeLogin.xhtml",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": "Mozilla/5.0",
            "X-Requested-With": "XMLHttpRequest",
        }
        return header,payload
    
    def select_application_header(view_state):
        payload = {
            "javax.faces.partial.ajax": "true",
            "javax.faces.source": "app_type",
            "javax.faces.partial.execute": "app_type",
            "javax.faces.partial.render": "rcpt_pnl tf_regen_panel_One",
            "javax.faces.behavior.event": "change",
            "javax.faces.partial.event": "change",
            "form_eapp": "form_eapp",
            "statusRadio1": "4",
            "app_type_input": "950",
            "app_type1_input": "-1",
            "tf_tran_rep1": "",
            "vhn_cap:CaptchaID": "",
            "javax.faces.ViewState": view_state,
        }

        header = {
            "Accept": "application/xml, text/xml, */*; q=0.01",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "en-US,en;q=0.5",
            "Connection": "keep-alive",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Faces-Request": "partial/ajax",
            "Host": "vahan.parivahan.gov.in",
            "Origin": "https://vahan.parivahan.gov.in",
            "Priority": "u=0",
            "Referer": "https://vahan.parivahan.gov.in/vahanservice/vahan/ui/eapplication/form_eAppCommonHomeLogin.xhtml",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": "Mozilla/5.0",
            "X-Requested-With": "XMLHttpRequest",
        }
        return header,payload
    
    def select_RTO_end_header(view_state):
        payload = {
            "javax.faces.partial.ajax": "true",
            "javax.faces.source": "app_type1",
            "javax.faces.partial.execute": "app_type1",
            "javax.faces.partial.render": "pnlgrd_eapp tf_reg_no tf_reg_no1 tf_chasis_no",
            "javax.faces.behavior.event": "change",
            "javax.faces.partial.event": "change",
            "form_eapp": "form_eapp",
            "statusRadio1": "4",
            "app_type_input": "950",
            "app_type1_input": "13",
            "tf_reg_no11": "",
            "tf_chasis_no1": "",
            "vhn_cap:CaptchaID": "",
            "javax.faces.ViewState": view_state,
        }
        header = {
            "Accept": "application/xml, text/xml, */*; q=0.01",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "en-US,en;q=0.5",
            "Connection": "keep-alive",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Faces-Request": "partial/ajax",
            "Host": "vahan.parivahan.gov.in",
            "Origin": "https://vahan.parivahan.gov.in",
            "Priority": "u=0",
            "Referer": "https://vahan.parivahan.gov.in/vahanservice/vahan/ui/eapplication/form_eAppCommonHomeLogin.xhtml",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": "Mozilla/5.0",
            "X-Requested-With": "XMLHttpRequest",
        }
        return header,payload
    
    def captcha_requests(view_state, captcha_text,mode,reg_no,chasis_no="12345"):
    
        header = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "en-US,en;q=0.5",
        "Connection": "keep-alive",
        "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
        "Faces-Request": "partial/ajax",
        "Host": "vahan.parivahan.gov.in",
        "Origin": "https://vahan.parivahan.gov.in",
        "Referer": "https://vahan.parivahan.gov.in/vahanservice/vahan/ui/eapplication/form_eAppCommonHomeLogin.xhtml",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:145.0) Gecko/20100101 Firefox/145.0",
        }

        payload = {
        "form_eapp": "form_eapp",
        "statusRadio1": "4",
        "app_type_input": "950",
        "app_type1_input": "13",
        "tf_reg_no11": reg_no,
        "tf_chasis_no1": chasis_no,
        "vhn_cap:CaptchaID": captcha_text,
        "javax.faces.ViewState": view_state,
        "javax.faces.source": "vhn_cap:CaptchaID",
        "javax.faces.partial.event": "blur",
        "javax.faces.partial.execute": "vhn_cap:CaptchaID",
        "javax.faces.partial.render": "vhn_cap:CaptchaID",
        "CLIENT_BEHAVIOR_RENDERING_MODE": mode,
        "javax.faces.behavior.event": "blur",
        "javax.faces.partial.ajax": "true",
        }
        
        return header,payload

    def click_on_show_details_fun(view_state, captcha_text,reg_no, chasis_no):
    
        header = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "en-US,en;q=0.5",
            "Connection": "keep-alive",
            "Content-Type": "application/x-www-form-urlencoded",
            "Host": "vahan.parivahan.gov.in",
            "Origin": "https://vahan.parivahan.gov.in",
            "Priority": "u=0, i",
            "Referer": "https://vahan.parivahan.gov.in/vahanservice/vahan/ui/eapplication/form_eAppCommonHomeLogin.xhtml",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-User": "?1",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:145.0) Gecko/20100101 Firefox/145.0"
        }

        payload = {
            "form_eapp": "form_eapp",
            "statusRadio1": "4",
            "app_type_input": "950",
            "app_type1_input": "13",
            "tf_reg_no11": reg_no,
            "tf_chasis_no1": chasis_no,
            "vhn_cap:CaptchaID": captcha_text,
            "tf_show_button": "",
            "javax.faces.ViewState": view_state,
        }
        
        return header,payload
    
    def click_on_print_receipt(view_state, dynamic_id):
    
        header = {
            "Accept": "application/xml, text/xml, */*; q=0.01",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "en-US,en;q=0.9",
            "Connection": "keep-alive",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Faces-Request": "partial/ajax",
            "Host": "vahan.parivahan.gov.in",
            "Origin": "https://vahan.parivahan.gov.in",
            "Referer": "https://vahan.parivahan.gov.in/vahanservice/vahan/ui/eapplication/form_eAppCommonHomeLogin.xhtml",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
            "X-Requested-With": "XMLHttpRequest",
        }
        payload = {
            "javax.faces.partial.ajax": "true",
            "javax.faces.source": dynamic_id,
            "javax.faces.partial.execute": "@all",
            dynamic_id: dynamic_id,
            "form_eapp": "form_eapp",
            "tabView_activeIndex": "0",
            "javax.faces.ViewState": view_state
        }
        
        return header,payload

    def print_receipt_page_header():
    
        header = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "en-US,en;q=0.5",
            "Connection": "keep-alive",
            "Host": "vahan.parivahan.gov.in",
            "Priority": "u=0, i",
            "Referer": "https://vahan.parivahan.gov.in/vahanservice/vahan/ui/eapplication/form_eAppCommonHomeLogin.xhtml",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-User": "?1",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0"
        }
        
        return header

    def form_29_data_header(view_state,form_29_btn_id,tans_id):
    
        header = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "en-US,en;q=0.5",
            "Connection": "keep-alive",
            "Content-Type": "application/x-www-form-urlencoded",
            "Host": "vahan.parivahan.gov.in",
            "Origin": "https://vahan.parivahan.gov.in",
            "Priority": "u=0, i",
            "Referer": "https://vahan.parivahan.gov.in/vahanservice/vahan/ui/eapplication/formFeeRecieptPrintReport.xhtml",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-User": "?1",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0"
        }

        payload = {
            "fee_receipt": "fee_receipt",
            "easeofuseRating_input": "0",
            "userIntRating_input": "0",
            "oninePayRating_input": "0",
            "seravailRating_input": "0",
            form_29_btn_id: "",
            "javax.faces.ViewState":view_state,
            "rcptNo": tans_id,
            "formName": "Form_29_TO"
        }

        return header,payload
    
    def captcha_img():
        header = {
            "Accept": "image/avif,image/webp,image/png,image/svg+xml,image/*;q=0.8,*/*;q=0.5",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "en-US,en;q=0.5",
            "Connection": "keep-alive",
            "Host": "vahan.parivahan.gov.in",
            "Referer": "https://vahan.parivahan.gov.in/vahanservice/vahan/ui/eapplication/form_eAppCommonHomeLogin.xhtml",
            "Sec-Fetch-Dest": "image",
            "Sec-Fetch-Mode": "no-cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:145.0) Gecko/20100101 Firefox/145.0",
            "Priority": "u=5, i"
        }
        return header

    def pagination_header(view_state,last_page_no="15",rows_per_page="15"):
        header = {
            "Accept": "application/xml, text/xml, */*; q=0.01",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "en-US,en;q=0.5",
            "Connection": "keep-alive",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Faces-Request": "partial/ajax",
            "Host": "vahan.parivahan.gov.in",
            "Origin": "https://vahan.parivahan.gov.in",
            "Priority": "u=0",
            "Referer": "https://vahan.parivahan.gov.in/vahanservice/vahan/ui/eapplication/form_eAppCommonHomeLogin.xhtml",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:145.0) Gecko/20100101 Firefox/145.0",
            "X-Requested-With": "XMLHttpRequest"
        }

        payload = {
            "javax.faces.partial.ajax": "true",
            "javax.faces.source": "tabView:tableTax",
            "javax.faces.partial.execute": "tabView:tableTax",
            "javax.faces.partial.render": "tabView:tableTax",

            "tabView:tableTax": "tabView:tableTax",
            "tabView:tableTax_pagination": "true",
            "tabView:tableTax_first":last_page_no,      # starting index of next page
            "tabView:tableTax_rows": rows_per_page,       # rows per page
            "tabView:tableTax_skipChildren": "true",
            "tabView:tableTax_encodeFeature": "true",

            "form_eapp": "form_eapp",
            "tabView_activeIndex": "0",

            "javax.faces.ViewState": view_state
        }
        
        return header, payload
