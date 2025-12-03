from .vahan_helper import *

# print("🔥 Starting global Vahan driver...")
# GLOBAL_VAHAN_DRIVER = Vahan().driver
# print("🔥 Global Vahan driver ready!")

@api_view(['POST'])
def vahan_timeline(request):
    try:
        vehicle_no = request.data.get("vehicle_no")
        if not vehicle_no:
            return Response({"status": "error", "message": "vehicle_no is required"}, status=400)

        max_retries = 3
        retry_delay = 1
        for attempt in range(max_retries):
            
            # Initialize scraper
            scraper = Vahan()
            response = scraper.timeline_data(vehicle_no)

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
        logger.error(f"Error in vahan_get_result: {str(e)}", exc_info=True)
        return Response({"status": "error", "message": "Internal server error"}, status=500)

@api_view(['POST'])
def vahan_timeline_via_s_no(request):
    try:
        vehicle_no = request.data.get("vehicle_no")
        s_no = request.data.get("s_no")
        if not vehicle_no:
            return Response({"status": "error", "message": "vehicle_no is required"}, status=400)

        max_retries = 3
        retry_delay = 1
        for attempt in range(max_retries):

            # Initialize scraper
            scraper = Vahan()
            response = scraper.timeline_data_via_s_no(vehicle_no,s_no)

            applications = response.get("applications", [])
            if applications:   # success → return immediately
                return Response({
                    "status": "success",
                    "data": applications,
                    # "cookies": cookies,
                    # "current_id": current_id,
                    # "total_pages": response.get("total_pages", 1)
                }, status=200)
            
            if not applications and response.get("message") == "s_no is incorrect. please check the s_no":
                return Response({"status": "success",  
                                 "data": [],
                                 "message": "s_no is incorrect. please check the s_no",
                                 }, status=200)


            logger.warning(f"Attempt {attempt+1}: No data received, retrying...")
            
            if attempt < max_retries - 1:
                time.sleep(retry_delay)

        # After all retries
        return Response({"status": "success", "data": [], "message": "No Record found."})

    except Exception as e:
        logger.error(f"Error in vahan_get_result: {str(e)}", exc_info=True)
        return Response({"status": "error", "message": "Internal server error"}, status=500)

@api_view(['POST'])
def vahan_transactions_list(request):
    try:
        vehicle_no = request.data.get("vehicle_no")
        if not vehicle_no:
            return Response({"status": "error", "message": "vehicle_no is required"}, status=400)

        max_retries = 3
        retry_delay = 1
        for attempt in range(max_retries):

            # Initialize scraper
            scraper = Vahan()
            response = scraper.transaction_data(vehicle_no)
            transactions = response.get("transactions", [])
            if transactions:   # success → return immediately
                return Response({
                    "status": "success",
                    "data": transactions,
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
        logger.error(f"Error in vahan_get_result: {str(e)}", exc_info=True)
        return Response({"status": "error", "message": "Internal server error"}, status=500)
