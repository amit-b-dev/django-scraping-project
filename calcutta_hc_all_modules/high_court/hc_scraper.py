from venv import logger
from .hcscraper import *
from rest_framework.response import Response
from rest_framework.decorators import api_view
import time
from datetime import datetime

@api_view(['POST'])
def hcCalcultta_original_side_API(request):
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

            scraper = HcCulculttaAppellateSide()

            court_code="1"
            response = scraper.getCaseDetails(case_code, case_no, case_year,court_code)
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

@api_view(['POST'])
def hcCalcultta_appellate_side_API(request):
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

            scraper = HcCulculttaAppellateSide()

            court_code="3"
            response = scraper.getCaseDetails(case_code, case_no, case_year, court_code)
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

@api_view(['POST'])
def hcCalcultta_Circuit_bench_at_jalpaiguri_API(request):
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

            scraper = HcCulculttaAppellateSide()

            court_code="2"
            response = scraper.getCaseDetails(case_code, case_no, case_year,court_code)
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

@api_view(['POST'])
def hcCalcultta_circuit_bench_at_port_blair_API(request):
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

            scraper = HcCulculttaAppellateSide()

            court_code="4"
            response = scraper.getCaseDetails(case_code, case_no, case_year,court_code)
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


@api_view(['GET'])
def get_original_side_case_type_list_API(request):
    try:
        max_retries = 3
        retry_delay = 1
        for attempt in range(max_retries):

            scraper = HcCulculttaAppellateSide()

            court_code="1"
            response = scraper.get_case_types_list(court_code)
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

@api_view(['GET'])
def get_Appellate_side_case_type_list_API(request):
    try:
        max_retries = 3
        retry_delay = 1
        for attempt in range(max_retries):

            scraper = HcCulculttaAppellateSide()

            court_code="3"
            response = scraper.get_case_types_list(court_code)
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

@api_view(['GET'])
def get_Circuit_bench_at_jalpaiguri_case_type_list_API(request):
    try:
        max_retries = 3
        retry_delay = 1
        for attempt in range(max_retries):

            scraper = HcCulculttaAppellateSide()

            court_code="2"
            response = scraper.get_case_types_list(court_code)
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

@api_view(['GET'])
def get_circuit_bench_at_port_blair_case_type_list_API(request):
    try:
        max_retries = 3
        retry_delay = 1
        for attempt in range(max_retries):

            scraper = HcCulculttaAppellateSide()

            court_code="4"
            response = scraper.get_case_types_list(court_code)
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

