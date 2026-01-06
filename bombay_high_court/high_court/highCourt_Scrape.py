from venv import logger
from .highCourtScrape import *
from rest_framework.response import Response
from rest_framework.decorators import api_view
import time
from datetime import datetime

@api_view(['POST'])
def highCourt_API(request):
    try:
        Case_No = request.data.get("Case_No")
        if not Case_No:
            return Response(
                {"status": "error", "message": "mobile_no and reg no is required"},
                status=400
            )
        max_retries = 3
        retry_delay = 1
        for attempt in range(max_retries):

            scraper = HcBombay()

            response = scraper.getCaseDetailsByCaseNo(Case_No)
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
