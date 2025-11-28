from .e_court_helper import *

@api_view(['POST'])
def e_court_services_cnr_no(request):
    try:
        CNR_No = request.data.get("CNR_No")
        if not CNR_No:
            return Response({"status": "error", "message": "vehicle_no is required"}, status=400)

        max_retries = 3
        retry_delay = 1
        for attempt in range(max_retries):

            scraper = e_court_services()
            response = scraper.search_cnr(CNR_No)

            applications = response.get("applications", [])
            if applications:   # success → return immediately
                return Response({
                    "status": "success",
                    "data": applications,
                    # "cookies": cookies,
                    # "current_id": current_id,
                    # "total_pages": response.get("total_pages", 1)
                }, status=200)
            
            logger.warning(f"Attempt {attempt+1}: No data received, retrying...")
            if attempt < max_retries - 1:
                time.sleep(retry_delay)

        # After all retries
        return Response({"status": "success", "data": [], "message": "No Record found."})

    except Exception as e:
        logger.error(f"Error in e_court_services_get_result: {str(e)}", exc_info=True)
        return Response({"status": "error", "message": "Internal server error"}, status=500)
