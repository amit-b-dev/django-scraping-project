from venv import logger
from .highCourtScrape import *
from rest_framework.response import Response
from rest_framework.decorators import api_view
import time
from datetime import datetime

@api_view(['POST'])
def highCourt_API(request):
    try:
        case_code = request.data.get("Case_Code").strip()
        case_no = request.data.get("Case_No").strip()
        case_year = request.data.get("Case_Year").strip()
        if not any([case_code,case_no,case_year]):
            return Response(
                {"status": "error", "message": "All fields must be provided"},
                status=400
            )
        max_retries = 3
        retry_delay = 1
        for attempt in range(max_retries):

            scraper = HcDelhi()

            response = scraper.getCaseDetails(case_code, case_no, case_year)
            applications = response.get("applications", [])
            if applications:   # success → return immediately
                return Response({
                    "status": "success",
                    "data": applications,
                }, status=200)
            
            if not applications and response.get("message") == "you are enter wrong case code":
                return Response({"status": "success",  
                                 "data": [],
                                 "message": "you are enter wrong case code",
                                 }, status=200)
            
            if not applications and response.get("message") == "case details are not available":
                return Response({"status": "success",  
                                 "data": [],
                                 "message": "case details are not available",
                                 }, status=200)

            logger.warning(f"Attempt {attempt+1}: No data received, retrying...")
            
            if attempt < max_retries - 1:
                time.sleep(retry_delay)

        # After all retries
        return Response({"status": "success", "data": [], "message": "No Record found."})

    except Exception as e:
        logger.error(f"Error in vahan_get_result: {str(e)}", exc_info=True)
        return Response({"status": "error", "message": "Internal server error"}, status=500)

@api_view(['Get'])
def caseTypeList_API(request):
    try:
        max_retries = 3
        retry_delay = 1
        for attempt in range(max_retries):

            scraper = HcDelhi()

            response = scraper.getCasetypesList()
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
