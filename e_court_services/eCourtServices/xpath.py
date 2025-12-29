class Xpath:
    CASE_TYPE = "//td[contains(normalize-space(),'Case Type')]/following-sibling::td[1]"
    FILING_NUMBER = "//td[contains(normalize-space(),'Filing Number')]/following-sibling::td[1]"
    FILING_DATE = "//td[contains(normalize-space(),'Filing Date')]/following-sibling::td[1]"
    REGISTRATION_NUMBER = "//td[contains(normalize-space(),'Registration Number')]/following-sibling::td[1]"
    REGISTRATION_DATE = "//td[contains(normalize-space(),'Registration Date')]/following-sibling::td[1]"
    CNR_NUMBER = "//td[contains(normalize-space(),'CNR Number')]/following-sibling::td[1]"
    E_FILNO = "//td[contains(normalize-space(),'e-Filno')]/following-sibling::td[1]"
    E_FILING_DATE = "//td[contains(normalize-space(),'e-Filing Date')]/following-sibling::td[1]"

    FIRST_HEARING_DATE = "//td[contains(normalize-space(),'First Hearing Date')]/following-sibling::td[1]"
    DECISION_DATE = "//td[contains(normalize-space(),'Decision Date')]/following-sibling::td[1]"
    CASE_STATUS = "//td[contains(normalize-space(),'Case Status')]/following-sibling::td[1]"
    NATURE_OF_DISPOSAL = "//td[contains(normalize-space(),'Nature of Disposal')]/following-sibling::td[1]"
    COURT_AND_JUDGE = "//td[contains(normalize-space(),'Court Number and Judge')]/following-sibling::td[1]"

    # --- Parties ---
    PETITIONER_ADVOCATE = "//table[@class='table table-bordered Petitioner_Advocate_table']//tr/td"
    RESPONDENT_ADVOCATE = "//table[@class='table table-bordered Respondent_Advocate_table']//tr/td"

    # --- Acts ---
    UNDER_ACT = "//table[@id='act_table']//tr/td"
    UNDER_SECTION = "//table[@id='act_table']//tr/td"

    # --- Case History ---
    HISTORY_ROWS = "//table[@class='history_table table ']//tbody/tr"
    INTRIM_ROWS = "//table[@class='order_table table ']"
    FINAL_ORDERS_JUDGEMENTS = "//table[@class='order_table table ']"
    
