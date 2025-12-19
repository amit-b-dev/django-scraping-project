import os
from .navigation import NavigationFlow

class CommonFlow:

    def __init__(self, flow, extract, session):
        self.flow = flow
        self.extract = extract
        self.session = session
        self.cookies = {}
        self.flow = NavigationFlow(self.session)


    def prepare_context(self, reg_no,chasis_no):

        #   Load Home Page
        url_home = "https://vahan.parivahan.gov.in/vahanservice/vahan/ui/statevalidation/homepage.xhtml"
        soup1, view_state1, view_state2 = self.flow.load_homepage(url_home)

        cookies_dict = self.session.cookies.get_dict()
        self.cookies = {
            k: v for k, v in cookies_dict.items()
            if k in ("key", "JSESSIONID") or k.startswith("SERVERID_")
        }

        # # Extract homepage IDs
        # check_box_id, input_id, sele_input_id = self.flow.extract_homepage_ids(soup1)

        # # Submit checkbox
        # self.flow.submit_checkbox(url_home, check_box_id, input_id, sele_input_id,
        #                           reg_no, view_state1, view_state2, self.cookies)

        # Again Proceed
        url_again = "https://vahan.parivahan.gov.in/vahanservice/vahan/ui/usermgmt/login.xhtml?faces-redirect=true"
        view_state, j_id1, j_id2 = self.flow.again_proceed(url_again, self.cookies)

        # Load Login
        url_login = "https://vahan.parivahan.gov.in/vahanservice/vahan/ui/usermgmt/login.xhtml"
        self.flow.load_login_page(url_login, view_state, j_id1, j_id2, self.cookies)

        #  Application Home
        url_app = "https://vahan.parivahan.gov.in/vahanservice/vahan/ui/eapplication/form_eAppCommonHomeLogin.xhtml"
        view_state, soup = self.flow.form_eAppCommonHomeLogin_page(url_app, self.cookies)

        # Select options
        view_state = self.flow.select_registration_no_wise_fun(url_app, view_state, self.cookies)
        view_state = self.flow.select_application(url_app, view_state, self.cookies)
        view_state = self.flow.select_RTO_end(url_app, view_state, self.cookies)

        # Solve Captcha
        for _ in range(10):
            captcha_text,mode, captcha_path, captcha_dir = self.flow.get_captcha(soup, self.cookies)
            view_state, solved = self.flow.enter_captcha(
                url_app, view_state, captcha_text, mode, reg_no, self.cookies
            )
            if solved:
                print('captcha correct')
                # if os.path.exists(captcha_path):
                #     os.remove(captcha_path)
                # if os.path.isdir(captcha_dir):
                #     os.rmdir(captcha_dir)
                break
            print('captcha incorrect - retrying......')


        # Final Application Details
        soup, view_state = self.flow.show_details(view_state, solved, reg_no,chasis_no, self.cookies)

        return soup, view_state,self.cookies
