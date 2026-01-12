from django.urls import path
from .high_court.hc_scraper import hcCalcultta_original_side_API, hcCalcultta_appellate_side_API, hcCalcultta_Circuit_bench_at_jalpaiguri_API,hcCalcultta_circuit_bench_at_port_blair_API, get_Appellate_side_case_type_list_API, get_original_side_case_type_list_API,get_Circuit_bench_at_jalpaiguri_case_type_list_API, get_circuit_bench_at_port_blair_case_type_list_API

urlpatterns = [
    path('v1/hc-calcutta/original-side/case_no', hcCalcultta_original_side_API, name="hcCalcultta_original_side_API"),

    path('v1/hc-calcutta/appellate-side/case_no', hcCalcultta_appellate_side_API, name="highCourt_API"),

    path('v1/hc-calcutta/circuit-bench-jalpaiguri/case_no', hcCalcultta_Circuit_bench_at_jalpaiguri_API, name="hcCalcultta_CircuitBenchAtJalpaiguri_API"),

    path('v1/hc-calcutta/circuit-bench-port-blair/case_no', hcCalcultta_circuit_bench_at_port_blair_API, name="hcCalcultta_circuit_bench_at_port_blair_API"),

    # FOR CASE TYPE DROP DOWN LIST

    path('v1/hc-calcutta/appellate-side/case-type-list', get_Appellate_side_case_type_list_API, name="get_Appellate_side_case_type_list_API"),
    
    path('v1/hc-calcutta/original_side/case-type-list', get_original_side_case_type_list_API, name="get_original_side_case_type_list_API"),

    path('v1/hc-calcutta/circuit-bench-jalpaiguri/case-type-list', get_Circuit_bench_at_jalpaiguri_case_type_list_API, 
    name="get_Circuit_bench_at_jalpaiguri_case_type_list_API"),

    path('v1/hc-calcutta/circuit-bench-port-blair/case-type-list', get_circuit_bench_at_port_blair_case_type_list_API, 
    name="get_circuit_bench_at_port_blair_case_type_list_API"),
]
