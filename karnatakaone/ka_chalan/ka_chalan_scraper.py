from venv import logger
from .kaChalanScraper import *
from rest_framework.response import Response
from rest_framework.decorators import api_view
import time
from datetime import datetime

@api_view(['POST'])
def send_otp_api(request):
    try:
        mobile_no = request.data.get("mobile_no")
        if not mobile_no:
            return Response(
                {"status": "error", "message": "mobile_no is required"},
                status=400
            )

        scraper = KarnatakaoneChalan()
        response = scraper.send_otp(mobile_no)

        if response.get("status") != "success":
            return Response(response, status=400)

        return Response(response, status=200)

    except Exception as e:
        logger.error("Send OTP error", exc_info=True)
        return Response(
            {"status": "error", "message": "Internal server error"},
            status=500
        )

@api_view(['POST'])
def validate_api(request):
    try:
        reg_no = request.data.get("reg_no")
        otp = request.data.get("OTP")
        PoliceCollectionOfFine_url = request.data.get("PoliceCollectionOfFine_url")
        nexttonext_requests = request.data.get("nexttonext_requests")
        params = request.data.get("params")
        cookies = request.data.get("cookies")

        # if not all([reg_no, otp, PoliceCollectionOfFine_url, nexttonext_requests,params, cookies]):
        #     return Response(
        #         {"status": "error", "message": "Missing required fields"},
        #         status=400
        #     )

        scraper = KarnatakaoneChalan()

        response = scraper.verify_otp_and_fetch_chalan(
            reg_no=reg_no,
            otp=otp,
            PoliceCollectionOfFine_url=PoliceCollectionOfFine_url,
            nexttonext_requests=nexttonext_requests,
            params=params,
            cookies=cookies
        )

        if response.get("status") != "success":
            return Response(response, status=400)

        return Response(response, status=200)

    except Exception:
        logger.error("Validate OTP error", exc_info=True)
        return Response(
            {"status": "error", "message": "Internal server error"},
            status=500
        )


# def karnatakaOneChalanByRegNo(request):
#     try:
#         reg_no = request.data.get("reg_no")
#         if not reg_no:
#             return Response({"status": "error", "message": "vehicle_no is required"}, status=400)

#         max_retries = 3
#         retry_delay = 1
#         for attempt in range(max_retries):
#             # Initialize scraper and use global driver
#             scraper = KarnatakaoneChalan()
#             # Open the target URL
#             response = scraper.reg_no_wise_chalan_data(reg_no)

#             applications = response.get("applications", [])
#             if applications:   # success → return immediately
#                 return Response({
#                     "status": "success",
#                     "data": applications,
#                     # "cookies": cookies,
#                     # "current_id": current_id,
#                     # "total_pages": response.get("total_pages", 1)
#                 }, status=200)
            
#             if not applications and response.get("message") == "Form_29 is not available":
#                 return Response({
#                     "status": "success",  
#                     "data": [],
#                     "message": "Form_29 is not available",
#                 }, status=200)


#             logger.warning(f"Attempt {attempt+1}: No data received, retrying...")
            
#             if attempt < max_retries - 1:
#                 time.sleep(retry_delay)

#         # After all retries
#         return Response({"status": "success", "data": [], "message": "No Record found."})

#     except Exception as e:
#         logger.error(f"Error in vahan_get_result: {str(e)}", exc_info=True)
#         return Response({"status": "error", "message": "Internal server error"}, status=500)
