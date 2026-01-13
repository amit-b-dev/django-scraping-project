from venv import logger
from .highCourtScrape import *
from rest_framework.response import Response
from rest_framework.decorators import api_view
import time
from datetime import datetime

@api_view(['POST'])
def highCourt_API(request):
    try:
        case_side = request.data.get("Case_Side")
        Case_Stamp_RegNo = request.data.get("Case_Stamp/RegNo")
        case_type = request.data.get("Case_Type")
        case_no = request.data.get("Case_No")
        case_year = request.data.get("Case_Year")
        if not all([case_side, Case_Stamp_RegNo, case_type, case_no, case_year]):
            return Response(
                {"status": "error", "message": "all fields are required"},
                status=400
            )

        max_retries = 3
        retry_delay = 1
        for attempt in range(max_retries):

            scraper = HcBombay()

            response = scraper.getCaseDetails(case_side, Case_Stamp_RegNo, case_type, case_no, case_year)
            applications = response.get("applications", [])
            if applications:   # success → return immediately
                return Response({
                    "status": "success",
                    "data": applications,
                }, status=200)
            
            if not applications and response.get("message") == "you are enter wrong input":
                return Response({"status": "success",  
                                 "data": [],
                                 "message": "you are enter wrong input",
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


@api_view(['GET'])
def caseTypeList_API(request):
    try:
        max_retries = 3
        retry_delay = 1
        for attempt in range(max_retries):

            scraper =HcBombay()

            response = scraper.getCaseTypeList()
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

@api_view(['GET'])
def caseSideList_API(request):
    try:
        max_retries = 3
        retry_delay = 1
        for attempt in range(max_retries):

            scraper = HcBombay()

            response = scraper.getCaseSideList()
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

@api_view(['GET'])
def stampAndRegList_API(request):
    try:
        max_retries = 3
        retry_delay = 1
        for attempt in range(max_retries):

            scraper = HcBombay()

            response = scraper.getStampAndRegList()
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
