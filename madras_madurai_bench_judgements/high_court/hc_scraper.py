from venv import logger
from .hcscraper import *
from rest_framework.response import Response
from rest_framework.decorators import api_view
import time
from datetime import datetime

@api_view(['POST'])
def hcMadrasMaduraiBench_API(request):
    try:
        case_type = request.data.get("Case_Type")
        case_no = request.data.get("Case_No")
        case_year = request.data.get("Case_Year")
        if not any([case_type,case_no,case_year]):
            return Response(
                {"status": "error", "message": "All fields must be provided"},
                status=400
            )
        max_retries = 3
        retry_delay = 1
        for attempt in range(max_retries):

            scraper = hcMadrasMaduraiBenchJudgements()

            response = scraper.getCaseDetails(case_type, case_no, case_year)
            applications = response.get("applications", [])
            if applications:   # success → return immediately
                return Response({
                    "status": "success",
                    "data": applications,
                }, status=200)

            logger.warning(f"Attempt {attempt+1}: No data received, retrying...")
            
            if attempt < max_retries - 1:
                time.sleep(retry_delay)

        # After all retries
        return Response({"status": "success", "data": [], "message": "No Record found."})

    except Exception as e:
        logger.error(f"Error in vahan_get_result: {str(e)}", exc_info=True)
        return Response({"status": "error", "message": "Internal server error"}, status=500)

# @api_view(['POST'])
# def vahan_timeline_via_s_no(request):
#     try:
#         vehicle_no = request.data.get("vehicle_no")
#         s_no = request.data.get("s_no")
#         if not vehicle_no:
#             return Response({"status": "error", "message": "vehicle_no is required"}, status=400)

#         max_retries = 3
#         retry_delay = 1
#         for attempt in range(max_retries):

#             # Get ViewState, Captcha, Cookies from your class
#             # view_state, captcha_image, cookies, current_id = Vahan.get_viewstate_and_cookies()

#             # Initialize scraper and use global driver
#             scraper = VahanScraper()
#             response = scraper.form29_via_s_no(vehicle_no,int(s_no))

#             applications = response.get("applications", [])
#             driver = response.get("driver", [])
#             if applications:   # success → return immediately
#                 return Response({
#                     "status": "success",
#                     "data": applications,
#                     # "cookies": cookies,
#                     # "current_id": current_id,
#                     # "total_pages": response.get("total_pages", 1)
#                 }, status=200)
            
#             if not applications and response.get("message") == "Form_29 is not available":
#                 return Response({"status": "success",  
#                                  "data": [],
#                                  "message": "Form_29 is not available",
#                                  }, status=200)
            
#             if not applications and response.get("message") == "s_no is incorrect. please check the s_no":
#                 return Response({"status": "success",  
#                                  "data": [],
#                                  "message": "s_no is incorrect. please check the s_no",
#                                  }, status=200)


#             logger.warning(f"Attempt {attempt+1}: No data received, retrying...")
#             if attempt < max_retries - 1:
#                 time.sleep(retry_delay)

#         # After all retries
#         return Response({"status": "success", "data": [], "message": "No Record found."})

#     except Exception as e:
#         logger.error(f"Error in vahan_get_result: {str(e)}", exc_info=True)
#         return Response({"status": "error", "message": "Internal server error"}, status=500)

# @api_view(['POST'])
# def vahan_transactions_list(request):
#     try:
#         vehicle_no = request.data.get("vehicle_no")
#         if not vehicle_no:
#             return Response({"status": "error", "message": "vehicle_no is required"}, status=400)

#         max_retries = 3
#         retry_delay = 1
#         for attempt in range(max_retries):

#             # Get ViewState, Captcha, Cookies from your class
#             # view_state, captcha_image, cookies, current_id = Vahan.get_viewstate_and_cookies()

#             # Initialize scraper
#             # use global driver
#             scraper = hcMadras()
#             response = scraper.transaction_data(vehicle_no)
            
#             transactions = response.get("transactions", [])
#             if transactions:   # success → return immediately
#                 return Response({
#                     "status": "success",
#                     "data": transactions,
#                     # "cookies": cookies,
#                     # "current_id": current_id,
#                     # "total_pages": response.get("total_pages", 1)
#                 }, status=200)

#             logger.warning(f"Attempt {attempt+1}: No data received, retrying...")
            
#             if attempt < max_retries - 1:
#                 time.sleep(retry_delay)

#         # After all retries
#         return Response({"status": "success", "data": [], "message": "No Record found."})

#     except Exception as e:
#         logger.error(f"Error in vahan_get_result: {str(e)}", exc_info=True)
#         return Response({"status": "error", "message": "Internal server error"}, status=500)
