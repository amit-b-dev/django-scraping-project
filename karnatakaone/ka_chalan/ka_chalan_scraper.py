from venv import logger
from .kaChalanScraper import *
from rest_framework.response import Response
from rest_framework.decorators import api_view
import time
from datetime import datetime

@api_view(['POST'])
def send_otp_api(request):
    try:
        vehicle_no = request.data.get("vehicle_no")
        mobile_no = request.data.get("mobile_no")
        if not vehicle_no or not mobile_no:
            return Response(
                {"status": "error", "message": "mobile_no and reg no is required"},
                status=400
            )
        max_retries = 3
        retry_delay = 1
        for attempt in range(max_retries):

            scraper = KarnatakaoneChalan()

            response = scraper.send_otp(vehicle_no,mobile_no)
            if response.get("vehicle_no"):
                return Response(response, status=200)

            if response.get("status") == "error":
                return Response(response, status=400)

            logger.warning(f"Attempt {attempt+1}: No data received, retrying...")
            
            if attempt < max_retries - 1:
                time.sleep(retry_delay)

        # After all retries
        return Response({"status": "success", "data": [], "message": "No Record found."})

    except Exception as e:
        logger.error(f"Error in vahan_get_result: {str(e)}", exc_info=True)
        return Response({"status": "error", "message": "Internal server error"}, status=500)

@api_view(['POST'])
def validate_api(request):
    try:
        vehicle_no = request.data.get("vehicle_no")
        otp = request.data.get("OTP")
        PoliceCollectionOfFine_url = request.data.get("PoliceCollectionOfFine_url")
        nexttonext_requests = request.data.get("nexttonext_requests")
        params = request.data.get("params")
        cookies = request.data.get("cookies")

        if not all([vehicle_no, otp, PoliceCollectionOfFine_url, nexttonext_requests,params, cookies]):
            return Response({"status": "error", "message": "fields are required"}, status=400)

        max_retries = 3
        retry_delay = 1
        for attempt in range(max_retries):

            scraper = KarnatakaoneChalan()

            response = scraper.verify_otp_and_fetch_chalan(
                vehicle_no=vehicle_no,
                otp=otp,
                PoliceCollectionOfFine_url=PoliceCollectionOfFine_url,
                nexttonext_requests=nexttonext_requests,
                params=params,
                cookies=cookies
            )
            applications = response.get("applications", [])
            if applications:
                return Response({
                        "status": "success",
                        "data": applications,
                    }, status=200)
            
            if not applications and response.get("message", [])=="Please Enter Correct OTP":
                return Response({
                    "status": "success",
                    "applications": [],
                    "message": "Please Enter Correct OTP"
                })
            
            logger.warning(f"Attempt {attempt+1}: No data received, retrying...")
            
            if attempt < max_retries - 1:
                time.sleep(retry_delay)

        # After all retries
        return Response({"status": "success", "data": [], "message": "No Record found."})

    except Exception as e:
        logger.error(f"Error in vahan_get_result: {str(e)}", exc_info=True)
        return Response({"status": "error", "message": "Internal server error"}, status=500)


# def karnatakaOneChalanByRegNo(request):
#     try:
#         vehicle_no = request.data.get("vehicle_no")
#         if not vehicle_no:
#             return Response({"status": "error", "message": "vehicle_no is required"}, status=400)

#         max_retries = 3
#         retry_delay = 1
#         for attempt in range(max_retries):
#             # Initialize scraper and use global driver
#             scraper = KarnatakaoneChalan()
#             # Open the target URL
#             response = scraper.vehicle_no_wise_chalan_data(vehicle_no)

            # applications = response.get("applications", [])
            # if applications:   # success → return immediately
                # return Response({
                #     "status": "success",
                #     "data": applications,
                #     # "cookies": cookies,
                #     # "current_id": current_id,
                #     # "total_pages": response.get("total_pages", 1)
                # }, status=200)
            
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

    # except Exception as e:
    #     logger.error(f"Error in vahan_get_result: {str(e)}", exc_info=True)
    #     return Response({"status": "error", "message": "Internal server error"}, status=500)
