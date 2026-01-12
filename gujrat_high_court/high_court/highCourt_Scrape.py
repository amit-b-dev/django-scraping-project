from venv import logger
from .highCourtScrape import *
from rest_framework.response import Response
from rest_framework.decorators import api_view
import time
from datetime import datetime

@api_view(['POST'])
def highCourt_API(request):
    try:
        case_mode = request.data.get("Case_Mode")
        case_type = request.data.get("case_type")
        case_no = request.data.get("Case_No")
        case_year = request.data.get("Case_Year")
        if not all([case_mode, case_type, case_no, case_year]):
            return Response(
                {"status": "error", "message": "all fields are required"},
                status=400
            )
        max_retries = 3
        retry_delay = 1
        for attempt in range(max_retries):

            scraper = GujratHighCourt()

            response = scraper.getCaseDetails(case_mode, case_type, case_no, case_year)
            applications = response.get("applications", [])
            if applications:   # success → return immediately
                return Response({
                    "status": "success",
                    "data": applications,
                }, status=200)
            
            if not applications and response.get("message") == "you are enter wrong case code or bench code":
                return Response({"status": "success",  
                                 "data": [],
                                 "message": "you are enter wrong case code or bench code",
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
